---
sidebar_position: 2
title: MongoDB Atlas
---

# MongoDB Atlas

## Tổng quan

MongoDB Atlas được sử dụng làm cơ sở dữ liệu chính cho **Ldx-Insight**, lưu trữ dữ liệu người dùng, dataset metadata và các nội dung liên quan. Việc sử dụng Atlas giúp giảm tải việc quản trị cơ sở hạ tầng và cung cấp các tính năng bảo mật, scaling, backup tự động.

## Cấu hình Cluster

- **Cluster Tier**: Khuyến nghị `M10` trở lên cho môi trường production (Replica Set).
- **Region**: Chọn khu vực gần người dùng (ví dụ `ap-southeast-1` - Singapore) để giảm độ trễ.
- **Replica Set**: Tối thiểu 3 nodes để đảm bảo high availability.
- **Storage**: SSD với auto-scaling dung lượng.
- **Backup**: Bật Continuous Backups hoặc Snapshot hằng ngày.

## Database & Collections

```
ldx-insight
├── users
├── datasets
├── categories
├── download_logs
└── statistics
```

- `users`: Lưu thông tin tài khoản, hashed password, role.
- `datasets`: Chứa metadata dataset do crawler cung cấp hoặc người dùng tạo.
- `categories`: Danh sách category phục vụ API `getAllCategories`.
- `download_logs`: (tùy chọn) lưu lại lịch sử tải xuống.
- `statistics`: Dữ liệu phục vụ phần thống kê.

## Kết nối từ Spring Boot

- Sử dụng **Spring Data MongoDB**.
- Connection string trong `application.properties` hoặc environment:
  ```properties
  spring.data.mongodb.uri=${MONGODB_URI}
  ```
- `MONGODB_URI` được cung cấp bởi Atlas dạng:
  ```
  mongodb+srv://<username>:<password>@ldx-insight-cluster.xxxxxx.mongodb.net/ldx-insight?retryWrites=true&w=majority
  ```
- Lưu ý encode password nếu chứa ký tự đặc biệt.

## Bảo mật

### 1. Network Access
- Bật **IP Access List**: chỉ allow IP của EC2, Vercel, và các môi trường dev cần thiết.
- Sử dụng **Private Endpoint** (tùy chọn) nếu chạy trong VPC.

### 2. Database Users
- Tạo user chuyên biệt `ldx-backend` với role `readWrite` trên database `ldx-insight`.
- Không dùng user admin cho ứng dụng.

### 3. TLS/SSL
- Atlas bắt buộc TLS, Spring Boot mặc định hỗ trợ TLS.
- Đảm bảo driver sử dụng TLS 1.2+.

### 4. Secret Management
- Không commit URI vào repo.
- Dùng GitHub Secrets, Vercel env, hoặc AWS SSM Parameter Store để lưu credentials.

## Monitoring

- **Atlas Metrics**: CPU, memory, storage, active connections.
- **Alerting**: Cấu hình alert cho threshold (CPU > 80%, storage > 80%).
- **Performance Advisor**: Theo dõi gợi ý index.

## Indexing Strategy

- `users.username`: unique index.
- `datasets.slug` hoặc `datasets.datasetId`: unique index.
- `datasets.category`: index để filter nhanh.
- `download_logs.datasetId`: index cho truy vấn thống kê.

Ví dụ tạo index trong Spring Data:
```java
@CompoundIndex(name = "dataset_slug_idx", def = "{'slug' : 1}", unique = true)
```

## Data Ingestion từ OpenHub Crawler

- Crawler có thể push dữ liệu trực tiếp hoặc thông qua backend API.
- Khi đẩy vào Atlas, cần chuẩn hóa schema về cùng cấu trúc.
- Sử dụng **Bulk Write** để giảm số lần round-trip.

## Sao lưu và khôi phục

- Atlas tự động snapshot hàng ngày (theo tier).
- Có thể export snapshot về S3 nếu cần.
- Kiểm tra định kỳ khả năng restore bằng việc tạo cluster test từ snapshot.

## Lộ trình mở rộng

- **Sharding**: Khi dataset lớn và cần phân vùng theo category hoặc province.
- **Analytic Nodes**: Dùng để chạy báo cáo nặng mà không ảnh hưởng cluster chính.
- **Serverless Instance**: Phù hợp cho workload ít.
- **Data Lake**: Tích hợp với S3 để phân tích dữ liệu lớn.
