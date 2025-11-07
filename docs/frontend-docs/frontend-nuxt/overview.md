---
sidebar_position: 1
title: Tổng quan về Frontend (Nuxt)
---

# Tổng quan về Frontend (Nuxt)

## Giới thiệu

Frontend của **Ldx-Insight** được xây dựng bằng **Nuxt 4** (Vue 3), đóng vai trò là cổng giao tiếp chính với người dùng. Ứng dụng cung cấp giao diện hiện đại để khám phá bộ dữ liệu mở, đăng ký/đăng nhập, quản lý tài khoản và tương tác với các dịch vụ phân tích.

## Mục tiêu

- **Trải nghiệm người dùng liền mạch**: Giao diện responsive, tốc độ cao, tối ưu cho nhiều thiết bị.
- **Tích hợp chặt chẽ với backend**: Giao tiếp qua REST API bảo vệ JWT, đồng bộ trạng thái với hệ thống Spring Boot.
- **Khả năng mở rộng**: Dễ dàng thêm module mới (ví dụ dashboard, phân tích dữ liệu) mà không phá vỡ kiến trúc hiện tại.

## Tính năng chính

- Tra cứu dataset, lọc theo danh mục và xem chi tiết.
- Quản lý tài khoản, chứng thực và lưu trạng thái đăng nhập bằng cookie.
- Tích hợp biểu đồ, bảng và các thành phần UI có sẵn từ **Nuxt UI**.
- Hỗ trợ đa ngôn ngữ (tương lai) và tuỳ biến theme theo thiết kế hệ thống.
- Kết nối tới OpenHub Crawler và backend qua endpoint cấu hình được.

## Luồng hoạt động tổng quát

```
Người dùng → Trình duyệt → Nuxt App → axios plugin → Backend API → MongoDB Atlas
```

1. Người dùng truy cập trang web được deploy trên Vercel.
2. Nuxt app render SSR/ISR hoặc CSR tùy context.
3. Các request HTTP đi qua `~/plugins/http.ts` để gắn base URL, header JWT.
4. API backend trả dữ liệu JSON cho frontend.
5. Pinia store cập nhật trạng thái và render lại giao diện.

## Module chính trong ứng dụng

- **Pages**: Định nghĩa routing (ví dụ `pages/index.vue`, `pages/data/[id].vue`).
- **Layouts**: Khung giao diện chung (`layouts/default.vue`, `layouts/blank.vue`).
- **Components**: Thành phần tái sử dụng cho header, bảng dữ liệu, form.
- **Stores**: Pinia store (`stores/app.ts`, `stores/auth.ts`) quản lý app state.
- **Composables**: Hook tiện ích (`composables/useApi.ts`) đóng gói logic gọi API.
- **Plugins**: cấu hình axios, interceptor, hoặc thư viện bên thứ ba.

## Triển khai & môi trường

- Deploy trên **Vercel**, tích hợp GitHub để tự động build khi push.
- Sử dụng environment variables (`NUXT_PUBLIC_API_BASE`) để định nghĩa backend API.
- Cloudflare được dùng làm CDN/DNS, đảm bảo SSL/TLS và caching cho static assets.

## Roadmap

- Thêm module phân tích dữ liệu trực quan hoá.
- Tích hợp bảo mật nâng cao (reCAPTCHA, rate limiting phía client).
- Cải thiện i18n và accessibility.
