---
sidebar_position: 3
title: Công nghệ sử dụng - Backend Python
---

# Công nghệ sử dụng - Backend Python

## Runtime và Ngôn ngữ

### Python 3.x
- **Version**: Python 3.8+ (khuyến nghị 3.10+)
- **Mục đích**: Ngôn ngữ lập trình chính
- **Lý do chọn**: 
  - Rich ecosystem cho data processing
  - Excellent libraries cho HTTP, data manipulation
  - Easy to learn và maintain
- **Features sử dụng**:
  - Type hints
  - Dataclasses
  - Path objects (pathlib)
  - Async support (có thể mở rộng)

## HTTP và Networking

### httpx
- **Version**: Latest stable
- **Mục đích**: HTTP client library
- **Tính năng**:
  - Synchronous và asynchronous support
  - Connection pooling
  - Timeout management
  - Request/response streaming
- **Lý do chọn**: Modern alternative to requests, better performance

### tenacity
- **Version**: Latest stable
- **Mục đích**: Retry mechanism
- **Tính năng**:
  - Exponential backoff
  - Configurable retry attempts
  - Custom retry conditions
- **Usage**: Wrap API calls với retry logic

## Data Processing

### pandas
- **Version**: Latest stable
- **Mục đích**: Data manipulation và transformation
- **Tính năng sử dụng**:
  - Read CSV files: `pd.read_csv()`
  - Read Excel files: `pd.read_excel()`
  - Convert to dict: `df.to_dict(orient='records')`
- **Lý do chọn**: Industry standard cho data processing

### pydantic
- **Version**: v2.x
- **Mục đích**: Data validation và modeling
- **Tính năng**:
  - Type validation
  - Data serialization/deserialization
  - Model validation
  - JSON schema generation
- **Models sử dụng**:
  - `DatasetSummary`
  - `DatasetDetail`
  - `DatasetResource`
  - `TopicSummary`

## Task Scheduling

### APScheduler (Advanced Python Scheduler)
- **Version**: Latest stable
- **Mục đích**: Task scheduling và cron jobs
- **Tính năng**:
  - Cron-based scheduling
  - Blocking scheduler
  - Job persistence (có thể cấu hình)
- **Usage**: Schedule recurring crawl jobs

## Logging và Console

### logging (Standard Library)
- **Mục đích**: Application logging
- **Configuration**:
  - File handler: `logs/openhub.log`
  - Console handler: stdout
  - Format: `[%(asctime)s] %(levelname)s %(message)s`

### rich
- **Version**: Latest stable
- **Mục đích**: Rich console output
- **Tính năng**:
  - Colored output
  - Progress bars
  - Tables
  - Markdown support
- **Usage**: Enhanced CLI output (optional)

## File I/O và Path Management

### pathlib (Standard Library)
- **Mục đích**: Path manipulation
- **Tính năng**:
  - Cross-platform paths
  - Path operations
  - File existence checks

### json (Standard Library)
- **Mục đích**: JSON serialization/deserialization
- **Usage**: 
  - Save metadata
  - Load/save normalized data
  - Crawl history

## Data Structures

### dataclasses (Standard Library)
- **Mục đích**: Simple data containers
- **Usage**:
  - `CrawlStats`
  - `AgentResult`
  - `DownloadedResource`

### typing (Standard Library)
- **Mục đích**: Type hints
- **Features**:
  - Type annotations
  - Generic types
  - Protocol types
  - Optional types

### enum (Standard Library)
- **Mục đích**: Enumerations
- **Usage**: `ResourceCategory` enum

## Utilities

### argparse (Standard Library)
- **Mục đích**: Command-line argument parsing
- **Usage**: CLI interface trong `run_agents.py`

### datetime (Standard Library)
- **Mục đích**: Date/time handling
- **Usage**: Timestamps, crawl history

### urllib.parse (Standard Library)
- **Mục đích**: URL manipulation
- **Usage**: Build absolute URLs

## Development Tools

### Type Checking
- **mypy** (optional): Static type checking
- **pyright** (optional): Type checking

### Code Formatting
- **black**: Code formatter
- **isort**: Import sorting

### Linting
- **pylint**: Code quality
- **flake8**: Style guide enforcement
- **ruff**: Fast linter (modern alternative)

## Dependencies Summary

### Core Dependencies
```python
httpx          # HTTP client
pydantic       # Data validation
pandas         # Data processing
apscheduler    # Task scheduling
tenacity       # Retry mechanism
rich           # Console output (optional)
```

### Standard Library
```python
pathlib        # Path operations
json           # JSON handling
logging        # Logging
dataclasses    # Data containers
typing         # Type hints
enum           # Enumerations
argparse       # CLI parsing
datetime       # Date/time
urllib.parse   # URL manipulation
```

## Version Compatibility

### Python Version
- **Minimum**: Python 3.8
- **Recommended**: Python 3.10+
- **Tested**: Python 3.10, 3.11, 3.12

### Operating Systems
- **Linux**: Fully supported
- **macOS**: Fully supported
- **Windows**: Supported (with path handling)

## Performance Considerations

### 1. HTTP Client
- **httpx**: Efficient connection pooling
- **Timeout**: Configurable per request
- **Streaming**: For large file downloads

### 2. Data Processing
- **pandas**: Optimized C implementations
- **Memory**: Efficient for large datasets
- **Chunking**: Có thể implement cho very large files

### 3. File I/O
- **pathlib**: Efficient path operations
- **Streaming**: For large file writes
- **Buffering**: Automatic buffering

## Security Considerations

### 1. Input Validation
- **pydantic**: Automatic validation
- **Type safety**: Type hints prevent errors
- **Sanitization**: Safe filename generation

### 2. HTTP Security
- **HTTPS**: Enforced for external APIs
- **Timeout**: Prevent hanging requests
- **Error handling**: Không expose sensitive info

### 3. File System
- **Path traversal**: Prevented by pathlib
- **Safe filenames**: Sanitize user input
- **Permissions**: Respect file permissions

## Future Technology Considerations

### 1. Async Support
- **aiohttp** hoặc **httpx async**: Async HTTP
- **asyncio**: Concurrent crawling
- **Performance**: Faster với nhiều portals

### 2. Database Integration
- **SQLAlchemy**: ORM cho metadata storage
- **MongoDB**: Document storage
- **PostgreSQL**: Relational data

### 3. Message Queue
- **Celery**: Distributed task queue
- **Redis**: Message broker
- **RabbitMQ**: Alternative broker

### 4. Monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Sentry**: Error tracking

### 5. Containerization
- **Docker**: Containerization
- **Docker Compose**: Multi-container setup
- **Kubernetes**: Orchestration (nếu scale lớn)

## Best Practices

### 1. Dependency Management
- Sử dụng `requirements.txt` hoặc `pyproject.toml`
- Pin versions cho production
- Regular updates cho security

### 2. Type Safety
- Sử dụng type hints
- Validate với pydantic
- Type checking trong CI/CD

### 3. Error Handling
- Comprehensive error handling
- Retry mechanisms
- Graceful degradation

### 4. Logging
- Structured logging
- Appropriate log levels
- Log rotation

### 5. Testing
- Unit tests
- Integration tests
- Mock external dependencies

