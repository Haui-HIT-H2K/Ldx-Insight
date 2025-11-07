---
sidebar_position: 2
title: Kiến trúc ML/AI & Crawler
---

# Kiến trúc ML/AI & Crawler

## Sơ đồ logic

```
Cổng dữ liệu mở
  └─► HTTP API / Files (CSV/XLSX/JSON)
        └─► Client (httpx + retry)
              └─► Portal Connector (dong-thap/ckan/...)
                    └─► Agent Manager (registry, run_connectors)
                          └─► Local Repository (metadata/resources/normalized)
                                └─► Normalize (CSV/XLSX → JSON line)
                                      └─► MongoDB Atlas / Dataset cho ML
```

## Các lớp chính

- **Agent Layer** (`agents.py`):
  - `AgentRegistry`: đăng ký và liệt kê connectors.
  - `CrawlAgentManager`: chạy các connectors, trả về `AgentResult` (datasets_processed, resources_downloaded).

- **Connector Layer** (`portals/*.py`):
  - `PortalConnector` (protocol) trong `portals/base.py` quy định `run_full_crawl()`.
  - Thực thi theo portal, gom metadata + tải resource + gọi normalize.

- **Client Layer** (`client.py`, `ckan.py`):
  - Gọi API portal (Đồng Tháp/custom hoặc CKAN) bằng httpx.
  - `tenacity` retry exponential backoff; `raise_for_status()` đảm bảo tính đúng đắn.

- **Data Layer** (`models.py`, `storage.py`, `transform.py`):
  - Pydantic models (Topic, Dataset, Resource...).
  - Repository local: `metadata/`, `resources/`, `normalized/`.
  - Chuẩn hóa CSV/XLS/XLSX/JSON về JSON line (khi hỗ trợ).

## Tích hợp ML (roadmap)

- Tạo module `ml/` (notebooks + pipelines) đọc từ `normalized/` hoặc MongoDB.
- Mô hình gợi ý: RandomForest, XGBoost, ARIMA/LSTM theo đặc thù chuỗi thời gian.
- Triển khai API model serving (FastAPI/Flask) hoặc nhúng vào Backend.

## Tính mở rộng

- Thêm portal mới: tạo class connector mới, đăng ký vào `AgentRegistry`.
- Thêm chuẩn hóa: mở rộng `transform.normalize_resource()` cho các định dạng khác.
- Thêm đích lưu trữ: mở rộng `LocalDataRepository` sang S3/MinIO.
