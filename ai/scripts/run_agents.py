#!/usr/bin/env python3
"""Run OpenHub crawler agents for configured portals."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable, List

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "src"))

from openhub_crawler.agents import CrawlAgentManager


LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "openhub.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("openhub_crawler")


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for running the OpenHub crawler.

    Returns:
        argparse.Namespace: Parsed arguments containing:
            - connectors (str): Comma-separated list of connector slugs to run.
            - storage_root (Path): Base path for storing crawled data and metadata.
            - schedule_cron (str): Optional cron expression for scheduled runs.
    """
    parser = argparse.ArgumentParser(description="Run OpenHub crawler agents")
    parser.add_argument(
        "--connectors",
        type=str,
        default="",
        help="Comma separated connector slugs to run (default: all)",
    )
    parser.add_argument(
        "--storage-root",
        type=Path,
        default=ROOT / "storage",
        help="Base directory for storing metadata and resources.",
    )
    parser.add_argument(
        "--schedule-cron",
        type=str,
        default="",
        help="Cron expression for recurring runs (e.g. '0 2 * * *'). If omitted, runs once.",
    )
    return parser.parse_args()


def resolve_connectors(manager: CrawlAgentManager, connectors_arg: str) -> List[str]:
    """
    Validate and resolve the list of connectors to execute.

    Args:
        manager (CrawlAgentManager): Manager instance that provides connector registry access.
        connectors_arg (str): Comma-separated connector slugs provided from CLI.

    Returns:
        List[str]: Valid list of connector slugs to crawl.

    Raises:
        SystemExit: If an unknown connector slug is provided.
    """
    available = manager.registry.list()
    if not connectors_arg:
        return list(available)
    requested = [slug.strip() for slug in connectors_arg.split(",") if slug.strip()]
    for slug in requested:
        if slug not in available:
            raise SystemExit(f"Unknown connector '{slug}'. Available: {', '.join(available)}")
    return requested


def run_job(manager: CrawlAgentManager, connectors: Iterable[str]) -> None:
    """
    Execute a single crawl job across specified connectors.

    Args:
        manager (CrawlAgentManager): The agent manager controlling all crawler instances.
        connectors (Iterable[str]): List or iterable of connector slugs to run.

    Behavior:
        - Logs start and end time for each crawl session.
        - Runs each connector using the manager.
        - Writes crawl summary to history log via `_write_history`.
    """
    connectors_list = list(connectors)
    log.info("Starting crawl for connectors: %s", ", ".join(connectors_list))
    started_at = datetime.now(UTC)
    results = manager.run_connectors(connectors_list)
    finished_at = datetime.now(UTC)
    for result in results:
        log.info(
            "Connector %s completed: datasets=%s resources=%s",
            result.connector_slug,
            result.datasets_processed,
            result.resources_downloaded,
        )
    _write_history(connectors_list, results, started_at, finished_at)


def _write_history(connectors: List[str], results, started_at: datetime, finished_at: datetime) -> None:
    """
    Record crawl execution details into a persistent JSON lines history log.

    Args:
        connectors (List[str]): List of connector slugs that were executed.
        results (List[Any]): Collection of crawl result objects, convertible via `asdict`.
        started_at (datetime): UTC datetime when the crawl started.
        finished_at (datetime): UTC datetime when the crawl finished.

    Behavior:
        Appends an entry to `logs/crawl_history.jsonl` with crawl metadata:
        - connectors
        - timestamps
        - duration
        - result summaries
    """
    history_path = LOG_DIR / "crawl_history.jsonl"
    entry = {
        "connectors": connectors,
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "duration_seconds": (finished_at - started_at).total_seconds(),
        "results": [asdict(result) for result in results],
    }
    with history_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False))
        fh.write("\n")


def main() -> None:
    """
    Entry point for running the OpenHub crawler.

    Workflow:
        1. Parse command-line arguments.
        2. Initialize `CrawlAgentManager`.
        3. Resolve connector list to run.
        4. If a cron expression is provided, schedule recurring jobs.
        5. Otherwise, execute the crawl job once.

    Behavior:
        - Logs lifecycle events to console and log file.
        - Handles graceful termination via KeyboardInterrupt.
    """
    args = parse_args()
    manager = CrawlAgentManager(repository_root=args.storage_root)
    connectors = resolve_connectors(manager, args.connectors)

    if args.schedule_cron:
        trigger = CronTrigger.from_crontab(args.schedule_cron)
        scheduler = BlockingScheduler()
        scheduler.add_job(run_job, trigger, args=[manager, connectors], id="openhub_crawl")
        log.info("Scheduler started for connectors %s with cron '%s'", ", ".join(connectors), args.schedule_cron)
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            log.info("Scheduler terminated")
    else:
        run_job(manager, connectors)


if __name__ == "__main__":
    main()
