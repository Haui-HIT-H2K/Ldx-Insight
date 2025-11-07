---
sidebar_position: 4
title: Cài đặt & vận hành ML/AI (Crawler)
---

# Cài đặt & vận hành ML/AI (Crawler)

## Yêu cầu hệ thống

- Python 3.10+
- pip / venv (hoặc conda)
- Quyền ghi thư mục `storage/` và `logs/`

## Cài đặt

```bash
cd ai
python -m venv venv
# Windows
./venv/Scripts/Activate.ps1
# macOS/Linux
source venv/bin/activate

# Cài package
pip install -U pip
pip install httpx pydantic pandas apscheduler tenacity rich openpyxl xlrd
```

(Tùy chọn) Tạo `requirements.txt`:

```txt
httpx>=0.25.0
pydantic>=2.0.0
pandas>=2.0.0
apscheduler>=3.10.0
tenacity>=8.2.0
rich>=13.0.0
openpyxl>=3.1.0
xlrd>=2.0.0
```

## Chạy crawler một lần

```bash
python scripts/run_agents.py --connectors dong-thap,hcm,da-nang
```

Chỉ định nơi lưu trữ:

```bash
python scripts/run_agents.py --storage-root ./storage
```

## Lập lịch (cron)

Chạy mỗi ngày lúc 2:00 sáng:

```bash
python scripts/run_agents.py --schedule-cron "0 2 * * *"
```

## Cấu trúc output

```
storage/
└── <portal-slug>/
    ├── metadata/
    │   ├── topics.json
    │   ├── dataset_pages/page_XXX.json
    │   └── datasets/<id>.json
    ├── resources/<category>/<parent_id>/<filename>
    └── normalized/<parent_id>/<resource_id>.json
```

## Tích hợp với Backend

- Backend đọc dữ liệu từ MongoDB Atlas hoặc ingest file JSON normalized.
- API `/api/v1/datasets/*` cung cấp truy vấn/chi tiết/download.

## Troubleshooting

- Kết nối API lỗi: kiểm tra mạng; tenacity tự retry; thử giảm `limit`.
- XLS/XLSX đọc lỗi: cài `openpyxl` và `xlrd` đúng phiên bản.
- Thiếu quyền ghi: đảm bảo quyền thư mục `storage/`, `logs/`.

## Roadmap ML

- Bổ sung notebook tiền xử lý feature engineering.
- Huấn luyện RandomForest/XGBoost, lưu mô hình (joblib/pickle).
- Phục vụ mô hình qua FastAPI; tích hợp endpoint `/api/v1/ml/diagnosis`.
