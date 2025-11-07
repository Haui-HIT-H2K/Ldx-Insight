---
sidebar_position: 4
title: Hướng dẫn cài đặt và chạy Backend Python
---

# Hướng dẫn cài đặt và chạy Backend Python

## Yêu cầu hệ thống

### Phần mềm cần thiết

1. **Python**
   - Version: **Python 3.8+** (khuyến nghị 3.10+)
   - Download: [Python Downloads](https://www.python.org/downloads/)
   - Kiểm tra: `python --version` hoặc `python3 --version`

2. **pip** (Python Package Manager)
   - Thường đi kèm với Python
   - Kiểm tra: `pip --version` hoặc `pip3 --version`
   - Update: `pip install --upgrade pip`

3. **Git** (Optional)
   - Để clone repository
   - Download: [Git Downloads](https://git-scm.com/downloads)

## Các bước cài đặt

### Bước 1: Clone Repository

```bash
git clone <repository-url>
cd Ldx-Insight/ai
```

### Bước 2: Tạo Virtual Environment

**Khuyến nghị**: Luôn sử dụng virtual environment để tránh conflict dependencies.

#### Windows:
```powershell
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
.\venv\Scripts\Activate.ps1
```

#### Linux/macOS:
```bash
# Tạo virtual environment
python3 -m venv venv

# Kích hoạt virtual environment
source venv/bin/activate
```

### Bước 3: Cài đặt Dependencies

Tạo file `requirements.txt` với nội dung:

```txt
httpx>=0.25.0
pydantic>=2.0.0
pandas>=2.0.0
apscheduler>=3.10.0
tenacity>=8.2.0
rich>=13.0.0
openpyxl>=3.1.0  # For Excel file support
xlrd>=2.0.0      # For .xls file support
```

Cài đặt:

```bash
pip install -r requirements.txt
```

Hoặc cài đặt từng package:

```bash
pip install httpx pydantic pandas apscheduler tenacity rich openpyxl xlrd
```

### Bước 4: Cấu hình Environment Variables (Optional)

Tạo file `.env` (nếu cần):

```bash
# .env
STORAGE_ROOT=./storage
LOG_DIR=./logs
```

Hoặc set environment variables:

**Windows (PowerShell)**:
```powershell
$env:STORAGE_ROOT="./storage"
$env:LOG_DIR="./logs"
```

**Linux/macOS**:
```bash
export STORAGE_ROOT=./storage
export LOG_DIR=./logs
```

### Bước 5: Kiểm tra Cài đặt

```bash
# Kiểm tra Python version
python --version

# Kiểm tra packages đã cài
pip list

# Test import
python -c "import httpx, pydantic, pandas, apscheduler, tenacity; print('All packages installed successfully!')"
```

## Cấu trúc thư mục sau khi cài đặt

```
ai/
├── venv/                    # Virtual environment (không commit)
├── src/
│   └── openhub_crawler/    # Source code
├── scripts/
│   └── run_agents.py       # Entry point
├── storage/                # Crawled data (tự động tạo)
├── logs/                   # Log files (tự động tạo)
├── requirements.txt        # Dependencies
└── .gitignore             # Git ignore rules
```

## Chạy ứng dụng

### 1. Chạy một lần (One-time run)

Chạy tất cả connectors:

```bash
python scripts/run_agents.py
```

Chạy connector cụ thể:

```bash
python scripts/run_agents.py --connectors dong-thap
```

Chạy nhiều connectors:

```bash
python scripts/run_agents.py --connectors dong-thap,hcm,da-nang
```

### 2. Chạy với Storage Root tùy chỉnh

```bash
python scripts/run_agents.py --storage-root /path/to/storage
```

### 3. Chạy định kỳ (Scheduled)

Chạy mỗi ngày lúc 2:00 AM:

```bash
python scripts/run_agents.py --schedule-cron "0 2 * * *"
```

Cron expression format: `minute hour day month day-of-week`

Ví dụ:
- `0 2 * * *`: Mỗi ngày lúc 2:00 AM
- `0 */6 * * *`: Mỗi 6 giờ
- `0 0 * * 0`: Mỗi Chủ nhật lúc midnight

### 4. Xem Help

```bash
python scripts/run_agents.py --help
```

## Cấu hình nâng cao

### 1. Custom Storage Location

```bash
python scripts/run_agents.py --storage-root /mnt/data/openhub
```

### 2. Logging Configuration

Chỉnh sửa `scripts/run_agents.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Thay đổi level
    format="[%(asctime)s] %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "openhub.log", encoding="utf-8"),
    ],
)
```

### 3. Retry Configuration

Chỉnh sửa trong `src/openhub_crawler/client.py`:

```python
@retry(
    wait=wait_exponential(multiplier=1, min=1, max=8),
    stop=stop_after_attempt(5)  # Tăng số lần retry
)
```

## Troubleshooting

### 1. Lỗi: ModuleNotFoundError

**Nguyên nhân**: Package chưa được cài đặt hoặc virtual environment chưa được kích hoạt.

**Giải pháp**:
```bash
# Kích hoạt virtual environment
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\Activate.ps1  # Windows

# Cài đặt lại dependencies
pip install -r requirements.txt
```

### 2. Lỗi: Permission denied

**Nguyên nhân**: Không có quyền tạo thư mục hoặc ghi file.

**Giải pháp**:
```bash
# Linux/macOS: Cấp quyền
chmod +x scripts/run_agents.py

# Windows: Chạy PowerShell as Administrator
```

### 3. Lỗi: pandas không đọc được Excel

**Nguyên nhân**: Thiếu `openpyxl` hoặc `xlrd`.

**Giải pháp**:
```bash
pip install openpyxl xlrd
```

### 4. Lỗi: Connection timeout

**Nguyên nhân**: Network issues hoặc portal không accessible.

**Giải pháp**:
- Kiểm tra internet connection
- Kiểm tra portal URL có đúng không
- Tăng timeout trong client code

### 5. Lỗi: Out of memory

**Nguyên nhân**: File quá lớn hoặc quá nhiều datasets.

**Giải pháp**:
- Xử lý từng dataset một
- Sử dụng chunking cho large files
- Tăng memory limit

## Development Setup

### 1. Install Development Dependencies

```bash
pip install pytest pytest-cov black isort mypy pylint
```

### 2. Code Formatting

```bash
# Format code với black
black src/ scripts/

# Sort imports
isort src/ scripts/
```

### 3. Linting

```bash
# Run pylint
pylint src/

# Run mypy (type checking)
mypy src/
```

### 4. Testing

```bash
# Run tests
pytest

# Với coverage
pytest --cov=src --cov-report=html
```

## Production Deployment

### 1. Systemd Service (Linux)

Tạo file `/etc/systemd/system/openhub-crawler.service`:

```ini
[Unit]
Description=OpenHub Crawler Service
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/Ldx-Insight/ai
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python scripts/run_agents.py --schedule-cron "0 2 * * *"
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable và start:

```bash
sudo systemctl enable openhub-crawler
sudo systemctl start openhub-crawler
sudo systemctl status openhub-crawler
```

### 2. Cron Job

Thêm vào crontab:

```bash
crontab -e
```

Thêm dòng:

```
0 2 * * * cd /path/to/Ldx-Insight/ai && /path/to/venv/bin/python scripts/run_agents.py >> /path/to/logs/cron.log 2>&1
```

### 3. Docker (Optional)

Tạo `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "scripts/run_agents.py"]
```

Build và run:

```bash
docker build -t openhub-crawler .
docker run -v $(pwd)/storage:/app/storage openhub-crawler
```

## Monitoring

### 1. Log Files

- **Location**: `logs/openhub.log`
- **Format**: `[timestamp] LEVEL message`
- **Rotation**: Có thể cấu hình với `logging.handlers.RotatingFileHandler`

### 2. Crawl History

- **Location**: `logs/crawl_history.jsonl`
- **Format**: JSON Lines (mỗi dòng là một JSON object)
- **Content**: Crawl metadata, timestamps, results

### 3. Storage Structure

Kiểm tra storage:

```bash
# Xem cấu trúc
tree storage/

# Xem số lượng datasets
find storage/ -name "*.json" | wc -l

# Xem kích thước
du -sh storage/
```

## Best Practices

1. **Luôn sử dụng virtual environment**
2. **Pin dependency versions** trong production
3. **Backup storage** định kỳ
4. **Monitor logs** để phát hiện lỗi sớm
5. **Test trước khi deploy** production
6. **Document custom configurations**
7. **Regular updates** cho security patches

