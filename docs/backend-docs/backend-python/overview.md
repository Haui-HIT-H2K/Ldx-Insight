---
sidebar_position: 1
title: Tổng quan về Backend Python (OpenHub Crawler)
---

# Tổng quan về Backend Python (OpenHub Crawler)

## Giới thiệu

**OpenHub Crawler** là một hệ thống Python được thiết kế để tự động crawl và thu thập dữ liệu từ các cổng dữ liệu mở (Open Data Portals) của các tỉnh thành tại Việt Nam. Hệ thống này đóng vai trò quan trọng trong việc tích hợp dữ liệu từ nhiều nguồn khác nhau vào cơ sở dữ liệu Open Linked Hub của dự án Ldx-Insight.

## Mục tiêu

### 1. Thu thập dữ liệu tự động
- Crawl metadata và resources từ các open data portals
- Hỗ trợ nhiều định dạng portal khác nhau (CKAN, custom APIs)
- Tự động hóa quy trình thu thập dữ liệu định kỳ

### 2. Chuẩn hóa dữ liệu
- Chuyển đổi các định dạng khác nhau (CSV, XLS, XLSX) thành JSON
- Tổ chức dữ liệu theo cấu trúc thống nhất
- Lưu trữ metadata và resources một cách có tổ chức

### 3. Tích hợp với hệ thống
- Cung cấp dữ liệu đã được chuẩn hóa cho Backend Spring Boot
- Hỗ trợ việc xây dựng Open Linked Hub database
- Đảm bảo tính nhất quán và chất lượng dữ liệu

## Các cổng dữ liệu được hỗ trợ

Hiện tại hệ thống hỗ trợ crawl từ các cổng dữ liệu mở sau:

1. **Đồng Tháp Open Data** (`dong-thap`)
   - URL: `https://opendata.dongthap.gov.vn`
   - API: Custom REST API

2. **Hồ Chí Minh Open Data** (`hcm`)
   - Portal: CKAN-based hoặc custom API
   - Hỗ trợ nhiều datasets và resources

3. **Đà Nẵng Open Data** (`da-nang`)
   - Portal: CKAN-based hoặc custom API
   - Tích hợp với hệ thống dữ liệu mở của thành phố

4. **Thanh Hóa Open Data** (`thanh-hoa`)
   - Portal: CKAN-based hoặc custom API
   - Thu thập dữ liệu địa phương

## Kiến trúc tổng thể

Hệ thống được thiết kế theo mô hình **Agent-based Architecture** với các thành phần chính:

```
┌─────────────────────────────────────────┐
│         CrawlAgentManager                │
│  (Orchestrates multiple connectors)      │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ↓                     ↓
┌──────────┐        ┌──────────┐
│ Portal   │        │ Portal   │
│Connector │        │Connector │
│(DongThap)│        │  (HCM)   │
└────┬─────┘        └────┬─────┘
     │                   │
     └──────────┬────────┘
                │
                ↓
     ┌──────────────────┐
     │  HTTP Client     │
     │  (httpx)         │
     └────────┬─────────┘
              │
              ↓
     ┌──────────────────┐
     │  Open Data Portal │
     │  (External API)   │
     └───────────────────┘
              │
              ↓
     ┌──────────────────┐
     │  Local Repository │
     │  (Storage)        │
     └───────────────────┘
              │
              ↓
     ┌──────────────────┐
     │  Transform        │
     │  (Normalize)       │
     └───────────────────┘
```

## Quy trình hoạt động

### 1. Khởi tạo và cấu hình
- Load các portal connectors từ registry
- Khởi tạo HTTP clients cho từng portal
- Thiết lập local storage repository

### 2. Crawl Metadata
- Lấy danh sách topics/categories
- Paginate qua danh sách datasets
- Fetch chi tiết từng dataset
- Lưu metadata vào JSON files

### 3. Download Resources
- Tải các resource files (CSV, XLS, XLSX, PDF, etc.)
- Phân loại resources theo category
- Lưu vào thư mục có cấu trúc

### 4. Normalize Data
- Chuyển đổi CSV/XLS/XLSX thành JSON
- Chuẩn hóa format dữ liệu
- Lưu normalized data vào thư mục riêng

### 5. Lưu trữ và báo cáo
- Tổ chức dữ liệu theo cấu trúc thư mục
- Ghi log quá trình crawl
- Tạo crawl history records

## Tính năng chính

### 1. Multi-Portal Support
- Hỗ trợ nhiều portal cùng lúc
- Mỗi portal có connector riêng
- Dễ dàng thêm portal mới

### 2. Retry Mechanism
- Tự động retry khi request thất bại
- Exponential backoff
- Configurable retry attempts

### 3. Data Normalization
- Chuyển đổi CSV/XLS/XLSX → JSON
- Giữ nguyên JSON format
- Hỗ trợ nhiều định dạng file

### 4. Scheduled Crawling
- Hỗ trợ cron-based scheduling
- Chạy định kỳ tự động
- Background job processing

### 5. Error Handling
- Graceful error handling
- Logging chi tiết
- Continue on failure

## Công nghệ sử dụng

- **Python 3.x**: Ngôn ngữ lập trình chính
- **httpx**: HTTP client library
- **pydantic**: Data validation và modeling
- **pandas**: Data processing và transformation
- **APScheduler**: Task scheduling
- **rich**: Console output formatting
- **tenacity**: Retry mechanism

## Cấu trúc thư mục

```
ai/
├── scripts/
│   └── run_agents.py          # Entry point script
├── src/
│   └── openhub_crawler/
│       ├── agents.py          # Agent manager và registry
│       ├── client.py          # HTTP client wrappers
│       ├── endpoints.py       # API endpoint definitions
│       ├── models.py          # Pydantic data models
│       ├── storage.py         # Local repository management
│       ├── transform.py       # Data normalization
│       └── portals/
│           ├── base.py       # Portal connector interface
│           ├── ckan.py       # CKAN portal utilities
│           ├── dongthap.py   # Đồng Tháp connector
│           ├── hcm.py         # HCM connector
│           ├── danang.py      # Đà Nẵng connector
│           └── thanhhoa.py    # Thanh Hóa connector
├── storage/                   # Crawled data storage
│   ├── {portal-slug}/
│   │   ├── metadata/
│   │   ├── resources/
│   │   └── normalized/
└── logs/                      # Application logs
```

## Lợi ích

### 1. Tự động hóa
- Giảm thiểu công việc thủ công
- Chạy định kỳ không cần can thiệp
- Tự động xử lý lỗi và retry

### 2. Mở rộng
- Dễ dàng thêm portal mới
- Modular architecture
- Plugin-based connectors

### 3. Tin cậy
- Error handling tốt
- Logging chi tiết
- Data validation

### 4. Hiệu quả
- Batch processing
- Parallel downloads (có thể mở rộng)
- Efficient storage organization

## Use Cases

1. **Daily Data Sync**: Đồng bộ dữ liệu hàng ngày từ các portals
2. **Initial Data Import**: Import dữ liệu ban đầu vào hệ thống
3. **Data Updates**: Cập nhật dữ liệu khi có thay đổi
4. **Backup**: Lưu trữ local copy của dữ liệu

## Tương lai

- Hỗ trợ thêm nhiều portals
- Parallel crawling
- Incremental updates
- Data quality checks
- Integration với Backend Spring Boot API

