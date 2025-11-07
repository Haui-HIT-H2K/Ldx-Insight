"""Connector implementation for Dong Thap open data portal."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import List, Optional

from ..client import DongThapOpenDataClient
from ..models import DatasetResource, DatasetResourceFile
from ..mongo_sink import MongoSink
from ..storage import DownloadedResource, LocalDataRepository, classify_resource
from ..transform import normalize_resource
from .base import CrawlStats, PortalConnector


class DongThapConnector:
    """Portal-specific connector for the Đồng Tháp open-data platform.

    Responsibilities:
        - Enumerate topics and datasets via `DongThapOpenDataClient`.
        - Persist listing pages and dataset detail to a `LocalDataRepository`.
        - Download all dataset resources and trigger normalization for supported types.

    Attributes:
        slug (str): Stable identifier used for storage paths.
        display_name (str): Human-friendly portal name used in logs.
        client (DongThapOpenDataClient): Underlying API client.
    """
    slug = "dong-thap"
    display_name = "Đồng Tháp Open Data"

    def __init__(self) -> None:
        """Instantiate the underlying API client."""
        self.client = DongThapOpenDataClient()
        self.mongo_sink: Optional[MongoSink] = None
        self._current_run_id: Optional[str] = None

    def describe(self) -> str:
        """Return a human friendly name for logging.

        Returns:
            str: A short descriptor like "Đồng Tháp Open Data (dong-thap)".
        """
        return f"{self.display_name} ({self.slug})"

    def attach_mongo_sink(self, sink: MongoSink | None) -> None:
        """Attach Mongo persistence."""
        self.mongo_sink = sink

    def set_run_context(self, run_id: str | None) -> None:
        """Set the current crawl run identifier."""
        self._current_run_id = run_id

    @property
    def province_label(self) -> str:
        """Return province label used for persistence."""
        return getattr(self, "province", self.display_name)

    def run_full_crawl(self, repository: LocalDataRepository) -> CrawlStats:
        """Fetch all metadata and resources exposed by the portal.

        Steps:
            1) Ensure repository structure exists.
            2) Save topics snapshot.
            3) Page through dataset summaries and persist each page.
            4) For each dataset:
               - Fetch detail
               - Download resources
               - Normalize supported files
               - Save detail with resource manifests
            5) Aggregate crawl stats.

        Args:
            repository (LocalDataRepository): Target repository to write metadata and files.

        Returns:
            CrawlStats: Totals for processed datasets and downloaded resources.

        Side Effects:
            Writes under `metadata/`, `resources/`, and `normalized/` within `repository`.
        """
        repository.prepare()
        stats = CrawlStats()
        fetched_at = datetime.now(UTC).isoformat()

        topics = self.client.list_topics()
        repository.save_topics(topics, fetched_at=fetched_at)

        offset = 0
        limit = 100
        while True:
            datasets, total = self.client.search_datasets_with_total(limit=limit, offset=offset)
            if not datasets:
                break
            repository.save_dataset_page(page_index=offset // limit, datasets=datasets, fetched_at=fetched_at)
            for summary in datasets:
                detail = self.client.get_dataset_detail(summary.parent_id)
                downloaded_resources = self._download_resources(
                    detail.resources,
                    detail.parent_id,
                    repository,
                    fetched_at,
                )
                repository.save_dataset_detail(
                    detail,
                    fetched_at=fetched_at,
                    resources=downloaded_resources,
                )
                self._persist_dataset_metadata(detail, fetched_at)
                stats.datasets_processed += 1
                stats.resources_downloaded += len(downloaded_resources)
            offset += limit
            if offset >= total:
                break

        self.client.close()
        return stats

    def _download_resources(
        self,
        resources: List[DatasetResource],
        parent_id: int,
        repository: LocalDataRepository,
        fetched_at: str,
    ) -> List[DownloadedResource]:
        """Download resource files, normalize supported ones, and record metadata.

        Logic:
            - Skip entries without `resource_id` or filename.
            - Classify each file to a `ResourceCategory`.
            - Resolve deterministic destination path in the repository.
            - If file exists, skip download but attempt normalization.
            - If not, download then attempt normalization.
            - Collect `DownloadedResource` records.

        Args:
            resources (List[DatasetResource]): Resource entries from dataset detail.
            parent_id (int): Dataset identifier used for path layout.
            repository (LocalDataRepository): Repository for storage and path resolution.

        Returns:
            List[DownloadedResource]: One entry per processed resource.
        """
        downloaded: List[DownloadedResource] = []
        for resource in resources:
            file_meta = resource.file
            if not isinstance(file_meta, DatasetResourceFile):
                continue
            if not resource.resource_id or not file_meta.name:
                continue
            category = classify_resource(file_meta)
            destination = repository.resource_destination(parent_id, file_meta.name, category)
            dataset_key = str(parent_id)
            if destination.exists():
                normalized_path = normalize_resource(
                    repository,
                    dataset_key,
                    str(resource.resource_id),
                    destination,
                    category,
                )
                downloaded.append(
                    DownloadedResource(
                        resource_id=str(resource.resource_id),
                        filename=file_meta.name,
                        category=category,
                        local_path=destination,
                        normalized_path=normalized_path,
                    )
                )
                self._persist_resource_metadata(parent_id, resource, downloaded[-1], fetched_at)
                continue
            final_path = self.client.download_resource_file(parent_id, resource.resource_id, destination)
            normalized_path = normalize_resource(
                repository,
                dataset_key,
                str(resource.resource_id),
                Path(final_path),
                category,
            )
            downloaded.append(
                DownloadedResource(
                    resource_id=str(resource.resource_id),
                    filename=file_meta.name,
                    category=category,
                    local_path=final_path,
                    normalized_path=normalized_path,
                )
            )
            self._persist_resource_metadata(parent_id, resource, downloaded[-1], fetched_at)
        return downloaded

    def _persist_dataset_metadata(self, detail, fetched_at: str) -> None:
        """Upsert dataset metadata into MongoDB if configured."""
        if not self.mongo_sink or not self._current_run_id:
            return
        dataset_id = str(detail.parent_id)
        payload = detail.model_dump(mode="json", by_alias=True)
        if payload is None:
            payload = {}
        payload.setdefault("title", detail.title)
        payload.setdefault("description", detail.description)
        if detail.topic and isinstance(detail.topic, dict):
            category_name = detail.topic.get("name")
        else:
            category_name = getattr(detail.topic, "name", None)
        if category_name:
            payload["category"] = category_name
        payload["source"] = self.display_name
        payload["provider"] = detail.author or self.display_name
        payload["dataUrl"] = self._dataset_page_url(detail.parent_id)
        self.mongo_sink.upsert_dataset(
            slug=self.slug,
            province=self.province_label,
            dataset_id=dataset_id,
            dataset=payload,
            fetched_at=fetched_at,
            run_id=self._current_run_id,
        )

    def _persist_resource_metadata(
        self,
        parent_id: int,
        resource: DatasetResource,
        downloaded: DownloadedResource,
        fetched_at: str,
    ) -> None:
        """Upsert resource metadata if Mongo sink is configured."""
        if not self.mongo_sink or not self._current_run_id:
            return
        resource_payload = {
            "id": resource.resource_id,
            "format": None,
            "url": self._resource_download_url(parent_id, resource.resource_id),
        }
        file_meta = resource.file if isinstance(resource.file, DatasetResourceFile) else None
        if isinstance(file_meta, DatasetResourceFile):
            resource_payload["format"] = file_meta.format
        self.mongo_sink.upsert_resource(
            slug=self.slug,
            province=self.province_label,
            dataset_id=str(parent_id),
            resource=resource_payload,
            downloaded=downloaded,
            fetched_at=fetched_at,
            run_id=self._current_run_id,
        )

    @staticmethod
    def _dataset_page_url(parent_id: int) -> str:
        """Construct a human-viewable dataset page URL."""
        return f"https://opendata.dongthap.gov.vn/dataset/{parent_id}"

    @staticmethod
    def _resource_download_url(parent_id: int, resource_id: int | None) -> str:
        """Construct the resource download endpoint used on the portal."""
        if resource_id is None:
            return ""
        return (
            "https://opendata.dongthap.gov.vn/xhr/admin/dataset/"
            f"download-file?parent_id={parent_id}&resource_id={resource_id}&account="
        )


__all__ = ["DongThapConnector"]
