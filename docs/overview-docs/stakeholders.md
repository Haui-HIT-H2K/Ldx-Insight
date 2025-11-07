---
sidebar_position: 5
title: Nhóm người dùng & use case
---

# Nhóm người dùng & Use Case

Việc xác định rõ đối tượng sử dụng giúp định hướng phát triển tính năng cũng như ưu tiên trải nghiệm người dùng. Dưới đây là ba nhóm chính mà Ldx-Insight hướng tới.

## 1. Cán bộ chuyển đổi số địa phương

- **Mục tiêu**: Theo dõi chỉ số ICT, đánh giá tiến độ chuyển đổi số tại địa phương.
- **Nhu cầu**:
  - Truy cập bảng thống kê, biểu đồ tổng hợp theo tỉnh/thành, lĩnh vực.
  - Tải dữ liệu thô để đưa vào báo cáo nội bộ.
  - Nhận cảnh báo khi dữ liệu mới được cập nhật.
- **Tính năng liên quan**:
  - Trang dashboard chính, module thống kê (`/api/v1/stats`).
  - Chức năng download dataset (`/datasets/{id}/download`).
  - Hệ thống phân quyền để hạn chế thao tác ghi/xóa.

## 2. Nhà phát triển & startup GovTech

- **Mục tiêu**: Tích hợp dữ liệu mở vào ứng dụng của họ mà không cần xây dựng pipeline thu thập riêng.
- **Nhu cầu**:
  - REST API ổn định, tài liệu rõ ràng.
  - Dataset đã chuẩn hóa, dễ phân tích.
  - Thống kê metadata (số lượng dataset, category).
- **Tính năng liên quan**:
  - Swagger/OpenAPI, public endpoints `/api/v1/datasets`.
  - Bộ tài liệu Developer (tại Docusaurus).
  - CORS cấu hình mở cho domain tin cậy.

## 3. Nhà nghiên cứu & sinh viên

- **Mục tiêu**: Khai thác dữ liệu để tạo báo cáo, luận văn, mô hình dự đoán.
- **Nhu cầu**:
  - Dataset lịch sử, nhất quán, nhiều định dạng.
  - Hỗ trợ mô tả dữ liệu (schema, nguồn gốc).
  - Hướng dẫn cài đặt nhanh để chạy backend/ML cục bộ.
- **Tính năng liên quan**:
  - Tài liệu `Backend Spring Boot/installation`, `Backend Python/installation`.
  - Dataset detail API với metadata.
  - Lộ trình tích hợp ML API.

## Các use case tiêu biểu

| Use case | Mô tả | Luồng hệ thống |
|----------|-------|----------------|
| Tra cứu dataset | Cán bộ truy tìm bộ dữ liệu theo từ khóa và tải file | Frontend Nuxt → Backend `/datasets/search` → MongoDB → trả kết quả → download URL |
| Theo dõi tải xuống | Admin xem tổng số lượt tải | Backend tăng `downloadCount`, frontend hiển thị thông tin thống kê |
| Đồng bộ dữ liệu mới | Operator chạy crawler cho Đồng Tháp | CLI `run_agents.py` → portal API → chuẩn hóa → MongoDB → update hiển thị |
| Tích hợp API | Startup gọi API lấy category | Client → `/api/v1/datasets/categories` → backend trả danh sách |
| Phân tích nâng cao | Nhà nghiên cứu export dữ liệu để chạy ML | Frontend/CLI → download resource JSON/CSV → sử dụng notebook ML |

## Quyền hạn & bảo mật

| Vai trò | Quyền |
|---------|-------|
| **Anonymous** | Gọi các API công khai, xem dữ liệu, tải dataset |
| **User đã đăng nhập** | (Roadmap) lưu dataset yêu thích, nhận thông báo |
| **Admin** | Quản lý người dùng, tạo/ sửa/ xóa dataset (đã mở API nhưng cần cân nhắc bật lại kiểm soát) |

Việc hiểu rõ các nhóm người dùng giúp nhóm phát triển ưu tiên tính năng phù hợp và chuẩn bị tài liệu hỗ trợ hiệu quả. Roadmap sẽ tiếp tục mở rộng để đáp ứng thêm nhu cầu của từng đối tượng.
