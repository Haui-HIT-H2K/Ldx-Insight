---
sidebar_position: 1
title: CI/CD cho Backend Spring Boot
---

# CI/CD cho Backend Spring Boot

## Tổng quan

Hệ thống CI/CD cho Backend Spring Boot được thiết kế để tự động hóa quy trình build, test và deploy ứng dụng lên AWS EC2 mỗi khi có code mới được push lên nhánh `main`.

## Kiến trúc CI/CD

```
┌─────────────────┐
│  GitHub Push    │
│  (main branch)  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ GitHub Actions  │
│  (CI/CD Workflow)│
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ↓         ↓
┌──────┐  ┌──────┐
│ Build│  │ Test │
│ JAR  │  │(Skip)│
└──┬───┘  └──┬───┘
   │         │
   └────┬────┘
        │
        ↓
┌─────────────────┐
│  Copy to EC2    │
│  (SCP Action)   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Run Deploy     │
│  Script (SSH)   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  AWS EC2        │
│  (Production)   │
└─────────────────┘
```

## Công nghệ sử dụng

### 1. GitHub Actions
- **Mục đích**: CI/CD pipeline automation
- **Workflow file**: `.github/workflows/deploy-backend.yml`
- **Trigger**: Push vào nhánh `main`

### 2. AWS EC2
- **Mục đích**: Server production để chạy Spring Boot application
- **OS**: Linux (Ubuntu/Amazon Linux)
- **Access**: SSH qua private key

### 3. Termius
- **Mục đích**: SSH client để quản lý và monitor EC2
- **Tính năng**: 
  - SSH connection
  - File transfer
  - Log viewing
  - Terminal access

## Quy trình CI/CD chi tiết

### Bước 1: Trigger Workflow

Workflow được kích hoạt tự động khi:
- Code được push lên nhánh `main`
- Pull request được merge vào `main`

```yaml
on:
  push:
    branches:
      - main
```

### Bước 2: Checkout Code

```yaml
- name: 1. Checkout code
  uses: actions/checkout@v4
```

GitHub Actions checkout code từ repository về runner.

### Bước 3: Setup JDK 17

```yaml
- name: 2. Set up JDK 17
  uses: actions/setup-java@v4
  with:
    java-version: '17'
    distribution: 'corretto'
```

Cài đặt JDK 17 (Amazon Corretto) trên GitHub Actions runner.

### Bước 4: Build Project

```yaml
- name: 3. Build project with Maven
  run: mvn clean package -DskipTests
  working-directory: ./backend/ldx-insight-backend
```

- Chạy Maven build để tạo JAR file
- Skip tests để tăng tốc độ deploy (có thể bật lại nếu cần)
- Output: `target/ldx-insight-backend-0.0.1-SNAPSHOT.jar`

### Bước 5: Prepare Deployment Package

```yaml
- name: 4. Prepare artifacts for deployment
  run: |
    mkdir -p deploy_package
    cp backend/ldx-insight-backend/target/ldx-insight-backend-*.jar deploy_package/
    cp scripts/deploy.sh deploy_package/
```

Tạo package chứa:
- JAR file đã build
- Deploy script (`deploy.sh`)

### Bước 6: Copy to EC2

```yaml
- name: 5. Copy deploy package to EC2
  uses: appleboy/scp-action@v0.1.7
  with:
    host: ${{ secrets.EC2_HOST }}
    username: ${{ secrets.EC2_USERNAME }}
    key: ${{ secrets.EC2_PRIVATE_KEY }}
    port: 22
    source: "deploy_package/"
    target: "/home/${{ secrets.EC2_USERNAME }}/app"
```

Sử dụng SCP để copy package lên EC2:
- **Source**: `deploy_package/` (trên GitHub runner)
- **Target**: `/home/{username}/app/deploy_package/` (trên EC2)

### Bước 7: Run Deploy Script

```yaml
- name: 6. Run deploy script on EC2
  uses: appleboy/ssh-action@v1.0.3
  with:
    host: ${{ secrets.EC2_HOST }}
    username: ${{ secrets.EC2_USERNAME }}
    key: ${{ secrets.EC2_PRIVATE_KEY }}
    port: 22
    script: |
      cd /home/${{ secrets.EC2_USERNAME }}/app/deploy_package
      chmod +x deploy.sh
      nohup bash deploy.sh > deploy.log 2>&1 &
```

SSH vào EC2 và chạy deploy script:
- Di chuyển vào thư mục deploy
- Cấp quyền thực thi cho script
- Chạy script trong background với `nohup`

## Deploy Script (deploy.sh)

Script deploy thực hiện các bước sau:

### 1. Tìm và dừng process cũ

```bash
PID=$(pgrep -f "ldx-insight-backend-.*.jar")

if [ -n "$PID" ]
then
  echo "[DEPLOY] Tìm thấy process cũ, PID: $PID. Đang dừng..."
  kill $PID 
  sleep 5 
  echo "[DEPLOY] Đã dừng process cũ."
else
  echo "[DEPLOY] Không tìm thấy process cũ. Bỏ qua bước dừng."
fi
```

- Tìm process đang chạy bằng pattern `ldx-insight-backend-*.jar`
- Nếu tìm thấy, kill process và đợi 5 giây
- Nếu không tìm thấy, bỏ qua bước này

### 2. Khởi động ứng dụng mới

```bash
echo "[DEPLOY] Khởi động ứng dụng Spring Boot..."
nohup java -jar ldx-insight-backend-*.jar > app.log 2>&1 &
```

- Chạy JAR file với `java -jar`
- Redirect output vào `app.log`
- Chạy trong background với `nohup` và `&`

## Cấu hình GitHub Secrets

Để workflow hoạt động, cần cấu hình các secrets sau trong GitHub:

### 1. EC2_HOST
- **Mô tả**: IP address hoặc domain của EC2 instance
- **Ví dụ**: `ec2-xx-xx-xx-xx.compute-1.amazonaws.com` hoặc `123.45.67.89`

### 2. EC2_USERNAME
- **Mô tả**: Username để SSH vào EC2
- **Ví dụ**: `ubuntu`, `ec2-user`, `admin`

### 3. EC2_PRIVATE_KEY
- **Mô tả**: Private key (SSH key) để authenticate
- **Format**: Toàn bộ nội dung file `.pem` hoặc private key
- **Lưu ý**: Bao gồm cả `-----BEGIN RSA PRIVATE KEY-----` và `-----END RSA PRIVATE KEY-----`

### Cách thêm Secrets

1. Vào GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Thêm từng secret với tên và giá trị tương ứng

## Sử dụng Termius để quản lý EC2

### Kết nối EC2 qua Termius

1. **Tạo Host mới**:
   - Name: `Ldx-Insight Backend`
   - Address: `{EC2_HOST}`
   - Port: `22`
   - Username: `{EC2_USERNAME}`

2. **Cấu hình SSH Key**:
   - Chọn "Use Key"
   - Import private key file (`.pem`)

3. **Connect**: Click "Connect" để kết nối

### Các thao tác thường dùng

#### 1. Kiểm tra ứng dụng đang chạy

```bash
ps aux | grep ldx-insight-backend
```

Hoặc:

```bash
pgrep -f "ldx-insight-backend-.*.jar"
```

#### 2. Xem logs ứng dụng

```bash
# Xem log real-time
tail -f /home/{username}/app/deploy_package/app.log

# Xem log deploy
tail -f /home/{username}/app/deploy_package/deploy.log

# Xem 100 dòng cuối
tail -n 100 /home/{username}/app/deploy_package/app.log
```

#### 3. Kiểm tra port đang lắng nghe

```bash
# Kiểm tra port 8080
netstat -tuln | grep 8080

# Hoặc
ss -tuln | grep 8080
```

#### 4. Dừng ứng dụng thủ công

```bash
# Tìm PID
PID=$(pgrep -f "ldx-insight-backend-.*.jar")

# Kill process
kill $PID
```

#### 5. Khởi động lại ứng dụng

```bash
cd /home/{username}/app/deploy_package
nohup java -jar ldx-insight-backend-*.jar > app.log 2>&1 &
```

#### 6. Kiểm tra disk space

```bash
df -h
```

#### 7. Kiểm tra memory usage

```bash
free -h
```

## Monitoring và Troubleshooting

### Kiểm tra trạng thái deployment

1. **GitHub Actions**:
   - Vào tab "Actions" trong GitHub repository
   - Xem workflow runs và logs

2. **EC2 qua Termius**:
   - SSH vào EC2
   - Kiểm tra logs: `tail -f app.log`
   - Kiểm tra process: `ps aux | grep java`

### Các lỗi thường gặp

#### 1. Lỗi: Connection refused khi SSH

**Nguyên nhân**:
- Security Group chưa mở port 22
- EC2 instance chưa khởi động
- IP address sai

**Giải pháp**:
- Kiểm tra Security Group trong AWS Console
- Đảm bảo port 22 (SSH) được allow từ IP của bạn
- Kiểm tra EC2 instance status

#### 2. Lỗi: Permission denied

**Nguyên nhân**:
- SSH key không đúng
- Username sai
- File permissions không đúng

**Giải pháp**:
- Kiểm tra lại private key trong GitHub Secrets
- Đảm bảo username đúng (ubuntu/ec2-user)
- Kiểm tra file permissions: `chmod 400 key.pem`

#### 3. Lỗi: Port 8080 đã được sử dụng

**Nguyên nhân**:
- Process cũ chưa được dừng
- Port bị conflict

**Giải pháp**:
```bash
# Tìm và kill process
PID=$(pgrep -f "ldx-insight-backend")
kill -9 $PID

# Hoặc kill process trên port 8080
lsof -ti:8080 | xargs kill -9
```

#### 4. Lỗi: JAR file không tìm thấy

**Nguyên nhân**:
- Build failed
- File không được copy đúng

**Giải pháp**:
- Kiểm tra GitHub Actions logs
- Kiểm tra file trong `/home/{username}/app/deploy_package/`
- Re-run workflow nếu cần

#### 5. Lỗi: MongoDB connection failed

**Nguyên nhân**:
- MongoDB chưa được cài đặt trên EC2
- Connection string sai
- Security Group chưa mở port MongoDB

**Giải pháp**:
- Cài đặt MongoDB trên EC2 hoặc sử dụng MongoDB Atlas
- Kiểm tra `MONGO_URI` environment variable
- Mở port 27017 trong Security Group (nếu dùng local MongoDB)

## Best Practices

### 1. Security

- **Không commit secrets**: Luôn dùng GitHub Secrets
- **Rotate keys**: Định kỳ thay đổi SSH keys
- **Limit access**: Chỉ cho phép IP cần thiết trong Security Group
- **Use HTTPS**: Đảm bảo MongoDB connection dùng SSL/TLS

### 2. Monitoring

- **Log rotation**: Cấu hình log rotation để tránh đầy disk
- **Health checks**: Thêm health check endpoint
- **Alerts**: Setup alerts cho disk space, memory, CPU

### 3. Backup

- **Database backup**: Backup MongoDB định kỳ
- **Configuration backup**: Lưu trữ cấu hình quan trọng
- **Disaster recovery plan**: Có kế hoạch phục hồi

### 4. Performance

- **JVM options**: Tối ưu JVM heap size
- **Connection pooling**: Cấu hình connection pool cho MongoDB
- **Caching**: Sử dụng caching khi cần

## Cải tiến tương lai

1. **Blue-Green Deployment**: Zero-downtime deployment
2. **Docker**: Containerize application
3. **Kubernetes**: Orchestration nếu scale lớn
4. **CI Tests**: Bật lại tests trong CI pipeline
5. **Staging Environment**: Thêm môi trường staging
6. **Automated Rollback**: Tự động rollback nếu health check fail
7. **Monitoring Tools**: Tích hợp CloudWatch, Prometheus
8. **Load Balancer**: Thêm load balancer cho high availability

## Tài liệu tham khảo

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Spring Boot Deployment](https://spring.io/guides/gs/spring-boot-for-azure/)
- [Termius Documentation](https://docs.termius.com/)

