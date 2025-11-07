---
sidebar_position: 1
title: AWS Cloud Infrastructure
---

# AWS Cloud Infrastructure

## Tổng quan

Hạ tầng AWS phục vụ cho **Ldx-Insight** chủ yếu tập trung vào việc triển khai và vận hành backend Spring Boot trên EC2, quản lý file artifact, giám sát và bảo mật. Các thành phần dưới đây mô tả cấu trúc hiện tại cùng các tiêu chuẩn vận hành.

## Kiến trúc triển khai

```
GitHub Actions (deploy-backend.yml)
        │  SSH + SCP
        ▼
┌─────────────────────────────┐
│ AWS EC2 (Ubuntu/Linux)      │
│  - Java 17 + Maven runtime  │
│  - Docker (optional)        │
│  - systemd / nohup          │
└──────────────┬──────────────┘
               │
               ▼
       Spring Boot JAR
        ldx-insight-backend
```

### Thành phần chính

- **EC2 Instance**: Máy chủ ảo chạy Ubuntu (hoặc Amazon Linux) dành cho backend.
- **Security Group**: Cho phép inbound trên port 22 (SSH) và 8080/80/443 tùy cấu hình reverse proxy.
- **IAM**: Quản lý key pair SSH (dạng `.pem`) và giới hạn quyền truy cập.
- **Elastic IP (tùy chọn)**: Dùng để đảm bảo IP cố định cho bản build production.

## Triển khai với GitHub Actions

File `.github/workflows/deploy-backend.yml` định nghĩa pipeline:

1. **Checkout code**.
2. **Setup JDK 17**.
3. **Maven build** với `mvn clean package -DskipTests`.
4. **Chuẩn bị artifact**: copy JAR và script `deploy.sh` vào `deploy_package/`.
5. **SCP artifact lên EC2** bằng `appleboy/scp-action`.
6. **SSH vào EC2** và chạy `deploy.sh` trong chế độ `nohup`.

### Biến môi trường / Secrets yêu cầu

- `EC2_HOST`: Public DNS hoặc IP của instance.
- `EC2_USERNAME`: Thông thường là `ubuntu` (Ubuntu) hoặc `ec2-user` (Amazon Linux).
- `EC2_PRIVATE_KEY`: Private key SSH tương ứng với key pair đã add vào EC2.

## Cấu trúc thư mục trên EC2

```
/home/<user>/app/
├── deploy_package/
│   ├── ldx-insight-backend-<version>.jar
│   ├── deploy.sh
│   └── deploy.log
└── storage/ (tùy theo nhu cầu lưu trữ)
```

### Script `deploy.sh`

- Dừng tiến trình cũ (tìm PID JAR đang chạy).
- Chạy JAR mới bằng `nohup java -jar ... > app.log 2>&1 &`.
- Ghi log tiến trình vào `app.log`.

## Bảo mật và vận hành

- **SSH Key Management**: Lưu trữ private key trong GitHub Secrets; tắt SSH password login.
- **Security Group**: Chỉ mở port cần thiết; hạn chế IP SSH.
- **OS Patching**: Thường xuyên cập nhật gói bằng `apt update && apt upgrade`.
- **Monitoring** (khuyến nghị): Cài đặt CloudWatch Agent hoặc sử dụng Prometheus/node_exporter.
- **Backup**: Snapshot định kỳ EBS volume hoặc sử dụng AMI.

## Giám sát và Log

- **Log ứng dụng**: `/home/<user>/app/deploy_package/app.log`.
- **Log deploy**: `/home/<user>/app/deploy_package/deploy.log`.
- **System log**: `/var/log/syslog`, `/var/log/auth.log`.

## Quy trình khắc phục sự cố

1. SSH vào instance bằng Termius hoặc CLI.
2. Kiểm tra trạng thái process: `ps aux | grep ldx-insight` hoặc `pgrep -f ldx-insight`.
3. Xem log ứng dụng: `tail -f app.log`.
4. Kiểm tra port: `sudo ss -tulnp | grep 8080`.
5. Nếu cần khởi động lại:
   ```bash
   pkill -f ldx-insight-backend
   nohup java -jar ldx-insight-backend-*.jar > app.log 2>&1 &
   ```

## Lộ trình nâng cấp

- Sử dụng **AWS System Manager Parameter Store** để quản lý secrets.
- Thêm **Application Load Balancer** cho high availability.
- Chuyển sang **ECS / EKS** nếu muốn container hóa.
- Triển khai **Auto Scaling Group** để tự động scale khi tải cao.
