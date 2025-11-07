---
sidebar_position: 2
title: Thiết kế hệ thống Backend Python
---

# Thiết kế hệ thống Backend Python

## Kiến trúc tổng thể

Hệ thống OpenHub Crawler được thiết kế theo mô hình **Agent-based Architecture** với các lớp (layers) rõ ràng, tách biệt trách nhiệm và dễ dàng mở rộng.

## Các thành phần chính

### 1. Agent Layer (Lớp Agent)

#### CrawlAgentManager
- **Trách nhiệm**: Điều phối và quản lý các portal connectors
- **Chức năng**:
  - Quản lý registry của các connectors
  - Thực thi crawl jobs cho nhiều portals
  - Tổng hợp kết quả crawl
  - Quản lý storage paths

#### AgentRegistry
- **Trách nhiệm**: Registry pattern để quản lý các connectors
- **Chức năng**:
  - Đăng ký các portal connectors
  - Cung cấp interface để truy cập connectors
  - Liệt kê các connectors có sẵn

### 2. Portal Connector Layer (Lớp Kết nối Portal)

#### PortalConnector (Interface)
- **Trách nhiệm**: Định nghĩa interface cho các portal connectors
- **Methods**:
  - `run_full_crawl(repository)`: Thực thi crawl đầy đủ
  - `describe()`: Mô tả connector

#### Portal Implementations
- **DongThapConnector**: Kết nối với Đồng Tháp Open Data
- **HoChiMinhConnector**: Kết nối với HCM Open Data
- **DaNangConnector**: Kết nối với Đà Nẵng Open Data
- **ThanhHoaConnector**: Kết nối với Thanh Hóa Open Data

Mỗi connector:
- Implement `PortalConnector` interface
- Có `slug` và `display_name` riêng
- Xử lý logic crawl cụ thể cho portal đó

### 3. Client Layer (Lớp HTTP Client)

#### HTTP Clients
- **DongThapOpenDataClient**: Client cho Đồng Tháp API
- **CkanClient**: Client chung cho CKAN-based portals

**Tính năng**:
- Retry mechanism với exponential backoff
- Error handling
- Type-safe API calls
- Session management

### 4. Data Layer (Lớp Dữ liệu)

#### Models (Pydantic)
- **DatasetSummary**: Tóm tắt dataset
- **DatasetDetail**: Chi tiết dataset
- **DatasetResource**: Resource trong dataset
- **TopicSummary**: Danh mục/topic

**Lợi ích**:
- Type safety
- Data validation
- Serialization/deserialization

#### Storage (Local Repository)
- **LocalDataRepository**: Quản lý local storage
- **Cấu trúc thư mục**:
  ```
  storage/
  └── {portal-slug}/
      ├── metadata/
      │   ├── topics.json
      │   ├── dataset_pages/
      │   └── datasets/
      ├── resources/
      │   ├── csv/
      │   ├── xlsx/
      │   ├── pdf/
      │   └── ...
      └── normalized/
          └── {dataset_id}/
  ```

### 5. Transform Layer (Lớp Chuyển đổi)

#### Normalization
- **Chức năng**: Chuyển đổi các định dạng file thành JSON
- **Hỗ trợ**:
  - CSV → JSON
  - XLS/XLSX → JSON
  - JSON → JSON (format lại)

#### Resource Classification
- Phân loại resources theo category
- Xác định extension và format
- Tạo safe filenames

## Luồng dữ liệu (Data Flow)

### 1. Crawl Workflow

```
User/CLI
  ↓
run_agents.py
  ↓
CrawlAgentManager
  ↓
AgentRegistry.get(connector_slug)
  ↓
PortalConnector.run_full_crawl()
  ↓
HTTP Client (API calls)
  ↓
Open Data Portal
  ↓
Response (JSON/File)
  ↓
LocalDataRepository.save()
  ↓
Transform.normalize_resource()
  ↓
Storage (Local filesystem)
```

### 2. Detailed Crawl Process

```
1. Initialize Repository
   └── LocalDataRepository.prepare()
       └── Create directory structure

2. Fetch Topics
   └── client.list_topics()
       └── repository.save_topics()

3. Paginate Datasets
   └── For each page:
       ├── client.search_datasets()
       └── repository.save_dataset_page()

4. Process Each Dataset
   └── For each dataset:
       ├── client.get_dataset_detail()
       ├── repository.save_dataset_detail()
       └── For each resource:
           ├── client.download_resource_file()
           ├── repository.resource_destination()
           ├── transform.normalize_resource()
           └── repository.normalized_destination()

5. Generate Statistics
   └── CrawlStats
       ├── datasets_processed
       └── resources_downloaded
```

## Package Structure

```
src/openhub_crawler/
├── __init__.py
│
├── agents.py              # Agent management
│   ├── AgentRegistry
│   ├── CrawlAgentManager
│   └── AgentResult
│
├── client.py              # HTTP clients
│   └── DongThapOpenDataClient
│
├── endpoints.py           # API endpoints
│   └── Endpoint definitions
│
├── models.py              # Data models
│   ├── TopicSummary
│   ├── DatasetSummary
│   ├── DatasetDetail
│   └── DatasetResource
│
├── storage.py             # Storage management
│   ├── LocalDataRepository
│   ├── ResourceCategory
│   └── DownloadedResource
│
├── transform.py           # Data transformation
│   └── normalize_resource()
│
└── portals/               # Portal connectors
    ├── base.py           # PortalConnector interface
    ├── ckan.py           # CKAN utilities
    ├── dongthap.py       # Đồng Tháp connector
    ├── hcm.py            # HCM connector
    ├── danang.py         # Đà Nẵng connector
    └── thanhhoa.py       # Thanh Hóa connector
```

## Design Patterns

### 1. Registry Pattern
- **AgentRegistry**: Quản lý các connectors
- Cho phép đăng ký và truy cập connectors động

### 2. Strategy Pattern
- **PortalConnector**: Mỗi portal có strategy riêng
- Dễ dàng thêm portal mới mà không ảnh hưởng code hiện tại

### 3. Repository Pattern
- **LocalDataRepository**: Tách biệt logic storage
- Dễ dàng thay đổi storage backend

### 4. Factory Pattern
- **CrawlAgentManager**: Tạo repositories cho từng connector
- Quản lý lifecycle của connectors

## Error Handling Strategy

### 1. Retry Mechanism
- Sử dụng `tenacity` library
- Exponential backoff
- Configurable retry attempts

### 2. Graceful Degradation
- Continue on connector failure
- Log warnings cho unimplemented connectors
- Return empty stats thay vì crash

### 3. Logging
- Structured logging
- File và console output
- Crawl history tracking

## Extension Points

### 1. Thêm Portal Mới

```python
# 1. Tạo connector class
class NewPortalConnector:
    slug = "new-portal"
    display_name = "New Portal"
    
    def run_full_crawl(self, repository):
        # Implementation
        pass

# 2. Đăng ký trong AgentRegistry
self._connectors["new-portal"] = NewPortalConnector()
```

### 2. Thêm Resource Format

```python
# Trong transform.py
if category == ResourceCategory.NEW_FORMAT:
    # Normalization logic
    pass
```

### 3. Custom Storage Backend

```python
# Implement repository interface
class CustomRepository:
    def save_dataset_detail(self, ...):
        # Custom implementation
        pass
```

## Performance Considerations

### 1. Sequential Processing
- Hiện tại: Sequential crawl cho từng portal
- Tương lai: Có thể parallelize

### 2. Caching
- Metadata caching để tránh duplicate requests
- File existence checks trước khi download

### 3. Batch Operations
- Batch save operations
- Efficient file I/O

## Security Considerations

### 1. Input Validation
- Pydantic models validate input
- Safe filename generation
- Path traversal prevention

### 2. Error Messages
- Không expose sensitive information
- Generic error messages cho external failures

### 3. Resource Limits
- Timeout cho HTTP requests
- File size limits (có thể thêm)

## Testing Strategy

### 1. Unit Tests
- Test từng component riêng lẻ
- Mock HTTP clients
- Test data models

### 2. Integration Tests
- Test full crawl workflow
- Test với mock portals
- Test storage operations

### 3. End-to-End Tests
- Test với real portals (optional)
- Validate output structure

## Monitoring và Observability

### 1. Logging
- Structured logs
- Log levels (DEBUG, INFO, WARNING, ERROR)
- File và console output

### 2. Metrics
- Crawl statistics
- Success/failure rates
- Processing times

### 3. History Tracking
- Crawl history trong JSONL format
- Timestamps và durations
- Result summaries

