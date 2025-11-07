---
sidebar_position: 3
title: Kiến trúc hệ thống
---

# Kiến trúc hệ thống Ldx-Insight

## Tổng quan

Ldx-Insight được thiết kế theo kiến trúc **đa dịch vụ** (polyglot) kết hợp giữa Python và Java nhằm tận dụng thế mạnh của từng ngôn ngữ:

- **Data Collector (Python)**: thu thập và chuẩn hóa dữ liệu từ các cổng dữ liệu mở địa phương.
- **Backend API (Spring Boot)**: cung cấp REST API, quản lý người dùng và dữ liệu lưu trữ.
- **Frontend (Nuxt)**: hiển thị dashboard, thống kê và công cụ khám phá dữ liệu.
- **Infrastructure Layer**: AWS EC2, MongoDB Atlas, Vercel, Cloudflare đảm bảo vận hành.

## Sơ đồ kiến trúc logic

```
         ┌─────────────────────────────┐
         │   Nguồn dữ liệu mở         │
         │ (Đồng Tháp, HCM, Đà Nẵng)  │
         └───────────────┬────────────┘
                         │ (API/CSV)
                         ▼
┌────────────────────────────────────────────┐
│  Data Collector (Python / OpenHub Crawler) │
│  - Agents & connectors per portal          │
│  - Chuẩn hóa -> JSON                       │
│  - Lưu file & ghi log                      │
└───────────────┬────────────────────────────┘
                │ (Bulk JSON)
                ▼
┌────────────────────────────────────────────┐
│         MongoDB Atlas (ldx-insight)        │
│  - users, datasets, categories, ...        │
└───────────────┬────────────────────────────┘
                │ (Spring Data MongoDB)
                ▼
┌────────────────────────────────────────────┐
│  Backend API (Spring Boot 3)               │
│  - Auth, JWT, Role                         │
│  - Dataset CRUD, download, stats           │
│  - Swagger / OpenAPI                       │
└───────────────┬────────────────────────────┘
                │ (REST/JSON + Cookie JWT)
                ▼
┌────────────────────────────────────────────┐
│  Frontend (Nuxt 4) / Vercel + Cloudflare   │
│  - Dashboard, search, filters              │
│  - Pinia + Axios + Nuxt UI                 │
└────────────────────────────────────────────┘
```

## Các lớp chức năng

| Lớp | Thành phần | Vai trò |
|-----|------------|---------|
| **Data** | OpenHub Crawler, MongoDB Atlas | Thu thập, chuẩn hóa, lưu trữ dữ liệu. |
| **Service** | Spring Boot backend | Cung cấp API, bảo mật, xử lý nghiệp vụ. |
| **Presentation** | Nuxt frontend | Giao diện người dùng, trực quan hóa dữ liệu. |
| **Ops** | CI/CD (GitHub Actions, Vercel), Cloudflare | Tự động deploy, CDN, bảo vệ hạ tầng. |

## Công nghệ chính

- **Backend**: Spring Boot 3.3, Java 17, Spring Security 6, JWT, MapStruct, Springdoc.
- **Data Collector**: Python 3.10+, httpx, pandas, pydantic, APScheduler, tenacity.
- **Frontend**: Nuxt 4, Vue 3, Pinia, Tailwind CSS 4, Nuxt UI.
- **Database**: MongoDB Atlas (Replica Set, JSON document store).
- **Hosting**: EC2 (backend), Vercel (frontend), Cloudflare (CDN/DNS), GitHub Actions (CI/CD).

## Giao tiếp giữa các dịch vụ

1. **Crawler → MongoDB**: Qua driver pymongo (hoặc SDK), dữ liệu JSON được ghi theo schema thống nhất.
2. **Backend → MongoDB**: Thông qua Spring Data MongoDB repository, cung cấp repository pattern, query DSL.
3. **Frontend → Backend**: Sử dụng Axios với cookie JWT; SecurityConfig cho phép các endpoint công khai cần thiết.
4. **Ops**: GitHub Actions deploy backend qua SSH/SCP; Vercel build frontend; Cloudflare proxy request toàn cầu.

## Yêu cầu phi chức năng

- **Performance**: API dưới 300ms cho truy vấn dataset phổ biến.
- **Scalability**: Crawler thiết kế theo connectors có thể mở rộng, backend stateless (scale out bằng nhiều EC2 instance), frontend CDN phân phối.
- **Security**: JWT, role-based access, CORS cấu hình, secrets quản lý qua env.
- **Observability**: Logging tập trung (app.log, deploy.log), lịch sử crawl JSONL.

## Roadmap kiến trúc

- Tách crawler thành microservice riêng deploy qua Docker.
- Bổ sung event streaming (Kafka) cho cập nhật real-time.
- Container hóa backend (Docker + ECS/EKS) để auto scale.
- Triển khai monitoring (Prometheus/Grafana, CloudWatch) và alerting.
