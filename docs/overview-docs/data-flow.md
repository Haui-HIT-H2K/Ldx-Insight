---
sidebar_position: 4
title: Vòng đời dữ liệu
---

# Vòng đời dữ liệu trong Ldx-Insight

Tài liệu này mô tả hành trình của dữ liệu từ lúc được thu thập tại các cổng dữ liệu mở cho đến khi hiển thị trên dashboard và cung cấp API cho bên thứ ba.

## 1. Thu thập (Ingest)

1. **Lập lịch**: `scripts/run_agents.py` (APScheduler) chạy theo cron hoặc thủ công.
2. **Chọn nguồn**: Người vận hành xác định connectors cần chạy (`dong-thap`, `hcm`, `da-nang`, `thanh-hoa`).
3. **Crawler thực thi**:
   - Gọi API portal bằng `httpx`, áp dụng retry với `tenacity`.
   - Lấy danh sách topic, dataset, resource.
   - Tải file dữ liệu (CSV/XLSX/JSON) về `storage/<slug>/resources`.
4. **Chuẩn hóa**: `transform.normalize_resource` chuyển đổi sang JSON line khi có thể.
5. **Ghi log**: `logs/openhub.log`, `crawl_history.jsonl` lưu metadata lượt crawl.

## 2. Lưu trữ (Store)

- Metadata dataset và resources được serialize thành JSON và lưu trong MongoDB Atlas (Collections `datasets`, `categories`, v.v.).
- Các thông tin người dùng, token, thống kê được backend Spring Boot quản lý trong MongoDB.
- File nguồn (CSV/XLSX) được lưu tạm trên EC2 hoặc storage riêng để phục vụ tải xuống.

## 3. Xử lý (Process)

- Backend Spring Boot sử dụng `DatasetServiceImpl` để truy vấn MongoDB, tính toán thống kê, tăng lượt download.
- `GlobalExceptionHandler` chuẩn hóa thông báo lỗi.
- JWT Service tạo/giải mã token, gán quyền dựa trên `User.role`.
- ML/AI modules (roadmap) đọc dữ liệu chuẩn hóa để huấn luyện mô hình.

## 4. Phân phối API (Expose)

- API công khai dưới namespace `/api/v1`:
  - `/auth/*`: đăng ký, đăng nhập, làm mới token.
  - `/datasets/*`: lấy danh sách, chi tiết, download link, thống kê.
  - `/stats/*`: cung cấp số liệu tổng hợp.
- Swagger (Springdoc) mô tả endpoints cho lập trình viên.
- CORS cấu hình cho phép frontend (Vercel, localhost) truy cập.

## 5. Hiển thị (Present)

- Nuxt frontend sử dụng Pinia store và Axios plugin để gọi API.
- Dữ liệu render thành bảng, biểu đồ, card thống kê.
- Người dùng có thể tìm kiếm dataset, lọc theo category, xem tải xuống.
- Download URL được backend trả về (JSON) để frontend kích hoạt tải file.

## 6. Theo dõi & Phản hồi (Feedback)

- `downloadCount` trong dataset tăng khi người dùng tải.
- Lịch sử crawl cho biết nguồn nào thành công/thất bại -> điều chỉnh lịch.
- Logs deploy/app hỗ trợ debug và tối ưu quy trình.

## 7. Roadmap dữ liệu nâng cao

- **Incremental update**: Chỉ crawl những dataset thay đổi (dựa trên timestamp).
- **Data quality**: Kiểm tra schema, phát hiện bất thường, bổ sung metadata chất lượng.
- **Data catalog**: Gắn tag, mô tả chi tiết cho dataset.
- **Analytics pipeline**: Đồng bộ dữ liệu chuẩn hóa sang engine phân tích (BigQuery/Snowflake) nếu cần.
