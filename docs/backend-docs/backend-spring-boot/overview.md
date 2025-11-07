---
sidebar_position: 1
title: Tổng quan về Ldx-Insight Backend
---

# Tổng quan về Ldx-Insight Backend

## Giới thiệu

**Ldx-Insight Backend** là một RESTful API service được xây dựng bằng Spring Boot, cung cấp các chức năng quản lý và truy cập dữ liệu mở (Open Data). Hệ thống được thiết kế để hỗ trợ việc tìm kiếm, quản lý và phân tích các bộ dữ liệu công khai.

## Mục đích

Hệ thống backend này phục vụ cho dự án **Ldx-Insight** - một nền tảng khám phá và truy cập các bộ dữ liệu công khai, được phát triển cho cuộc thi **Olympic Tin học 2025**.

## Chức năng chính

### 1. Quản lý Dataset
- Tìm kiếm và lọc datasets theo từ khóa, category
- Xem chi tiết dataset
- Tạo, cập nhật, xóa datasets (dành cho Admin)
- Theo dõi số lượt xem và tải xuống

### 2. Xác thực và Phân quyền
- Đăng ký tài khoản mới
- Đăng nhập/Đăng xuất
- Quản lý JWT token qua HttpOnly cookie
- Phân quyền theo role (USER, ADMIN)

### 3. Thống kê
- Thống kê tổng quan: tổng số datasets, views, downloads
- Lấy danh sách tất cả categories

### 4. API Documentation
- Tích hợp Swagger/OpenAPI để tự động tạo tài liệu API
- Truy cập tại: `http://localhost:8080/swagger-ui/index.html`

## Kiến trúc tổng quan

Hệ thống được xây dựng theo mô hình **Layered Architecture** (Kiến trúc phân lớp):

```
┌─────────────────────────────────────┐
│         Controller Layer            │  ← REST API Endpoints
├─────────────────────────────────────┤
│         Service Layer               │  ← Business Logic
├─────────────────────────────────────┤
│         Repository Layer             │  ← Data Access
├─────────────────────────────────────┤
│         MongoDB Database            │  ← Data Storage
└─────────────────────────────────────┘
```

## Công nghệ Core

- **Framework**: Spring Boot 3.3.1
- **Database**: MongoDB
- **Security**: Spring Security + JWT
- **API Documentation**: SpringDoc OpenAPI (Swagger)
- **Mapping**: MapStruct
- **Language**: Java 17

## API Base URL

- **Development**: `http://localhost:8080`
- **API Prefix**: `/api/v1`

## Các Module chính

1. **Authentication Module** (`/api/v1/auth`)
   - Register, Login, Logout
   - JWT token management

2. **Dataset Module** (`/api/v1/datasets`)
   - CRUD operations
   - Search & Filter
   - Download tracking

3. **Statistics Module** (`/api/v1/stats`)
   - Summary statistics
   - Category listing

## Tính năng bảo mật

- JWT-based authentication
- HttpOnly cookie để lưu trữ token
- CORS configuration
- Password encryption (BCrypt)
- Role-based access control

## Database Collections

- **datasets**: Lưu trữ thông tin các bộ dữ liệu
- **users**: Lưu trữ thông tin người dùng

## Development Status

Hệ thống đang trong giai đoạn phát triển và được thiết kế để dễ dàng mở rộng và bảo trì.

