---
sidebar_position: 1
title: Tổng quan ML/AI (OpenHub Crawler & Phân tích)
---

# Tổng quan ML/AI

## Mục tiêu

- Thu thập và chuẩn hóa dữ liệu mở từ nhiều cổng địa phương (crawler).
- Tạo dữ liệu huấn luyện phục vụ mô hình **chẩn đoán/dự báo chỉ số chuyển đổi số** (CĐS).
- Cung cấp kết quả phân tích cho Backend/Frontend qua kho dữ liệu đã chuẩn hóa.

## Thành phần từ mã nguồn `ai/`

- `scripts/run_agents.py`: CLI entry-point, lập lịch và chạy nhiều connector.
- `src/openhub_crawler/agents.py`: Quản lý registry connectors (Đồng Tháp, HCM, Đà Nẵng, Thanh Hóa), chạy lần lượt và trả `AgentResult`.
- `src/openhub_crawler/client.py`: HTTP client (httpx) gọi API cổng dữ liệu (Đồng Tháp), có retry bằng tenacity.
- `src/openhub_crawler/models.py`: Pydantic models cho Topic, Dataset, Resource.
- `src/openhub_crawler/storage.py`: Tổ chức repository local (metadata, resources, normalized) + phân loại định dạng.
- `src/openhub_crawler/transform.py`: Chuẩn hóa CSV/XLS/XLSX → JSON line; giữ nguyên JSON.
- `src/openhub_crawler/portals/*.py`: Các connector cổng dữ liệu (ckan/dongthap/danang/hcm/thanhhoa).

## Dữ liệu đầu ra

- Metadata JSON (topics, dataset pages, dataset detail) theo cấu trúc thống nhất.
- File tài nguyên (CSV/XLSX/JSON) đã được phân loại và (khi hỗ trợ) chuẩn hóa thành JSON line.
- Nhật ký crawl (`logs/openhub.log`, `crawl_history.jsonl`) phục vụ theo dõi, kiểm chứng.

## Vai trò trong pipeline ML

- Cung cấp dữ liệu đầu vào đã làm sạch/chuẩn hóa cho bước tiền xử lý ML.
- Có thể bổ sung notebook/serving API cho mô hình dự báo (roadmap) dựa trên dữ liệu normalized.
