---
sidebar_position: 0
title: Tổng quan Hạ tầng
---

# Tổng quan hạ tầng Ldx-Insight

Hệ thống **Ldx-Insight** được triển khai trên mô hình đa nền tảng nhằm đảm bảo tính linh hoạt, khả năng mở rộng và độ tin cậy. Phần này cung cấp cái nhìn tổng quan về các thành phần hạ tầng cốt lõi, cách chúng phối hợp với nhau và các tiêu chuẩn vận hành chung.

## Mục tiêu hạ tầng

- **Độ tin cậy cao**: Luôn sẵn sàng phục vụ người dùng với thời gian downtime tối thiểu.
- **Hiệu năng ổn định**: Tối ưu tốc độ phản hồi cho cả API và giao diện web.
- **Bảo mật**: Bảo vệ dữ liệu người dùng, hạn chế truy cập trái phép, mã hóa giao tiếp.
- **Dễ mở rộng**: Có thể tăng quy mô nhanh chóng khi nhu cầu tăng.
- **Tự động hóa**: CI/CD giúp triển khai nhanh, giảm thiểu lỗi thủ công.

## Các thành phần chính

| Thành phần | Mô tả ngắn |
|------------|-----------|
| **CI/CD** | Automate build & deploy cho backend, frontend và docs (GitHub Actions, Vercel). |
| **Cloud** | Triển khai trên AWS EC2, MongoDB Atlas, Cloudflare CDN và Vercel Edge Network. |
| **Giám sát & Logging** | Sử dụng log app, deploy log, Cloudflare analytics; roadmap bổ sung CloudWatch/Prometheus. |
| **Security** | TLS, Firewall, IP whitelist, quản lý secrets qua GitHub/Vercel/AWS. |

## Kiến trúc tổng quát

```
              ┌──────────────┐
              │   GitHub     │
              │  Repository  │
              └──────┬───────┘
                     │
          ┌──────────▼──────────┐
          │      CI/CD          │
          │  (GitHub Actions,   │
          │      Vercel)        │
          └────────┬────────────┘
                   │                Build & Deploy
         ┌─────────▼──────────┐
         │      Backend       │   HTTPS/API
         │ (AWS EC2 + MongoDB │<────────────┐
         │      Atlas)        │             │
         └─────────┬──────────┘             │
                   │                        │
          ┌────────▼────────┐               │
          │   Frontend      │───────────────┘
          │   (Vercel)      │  CDN/SSL qua Cloudflare
          └─────────────────┘
```

## Nội dung tài liệu hạ tầng

- **CI/CD**: Chi tiết pipeline deploy backend (AWS EC2), docs (GitHub Pages) và frontend (Vercel).
- **Cloud**: Mô tả cấu hình AWS, MongoDB Atlas, Cloudflare và Vercel.
- **Logging & Monitoring** *(roadmap)*: Tích hợp CloudWatch, log streaming.
- **Security** *(roadmap)*: Chính sách bảo mật, secret management, backup.

## Quy trình vận hành chung

1. Commit/push code lên GitHub.
2. GitHub Actions build và deploy backend hoặc docs.
3. Vercel tự động build và publish frontend.
4. Cloudflare phân phối nội dung với SSL/TLS và firewall.
5. MongoDB Atlas lưu trữ dữ liệu, EC2 chạy dịch vụ Spring Boot.
6. Team theo dõi log, metrics và backup định kỳ.

## Tiêu chuẩn & best practices

- Sử dụng **Infrastructure as Code** (ghi chú roadmap Terraform/CloudFormation).
- Quản lý secrets qua `GitHub Secrets`, `Vercel Environment Variables`, `AWS SSM` (tùy chọn).
- Backup dữ liệu Atlas và snapshot EC2 theo chu kỳ.
- Theo dõi chi phí cloud, tối ưu tài nguyên khi cần.
- Định kỳ kiểm tra bảo mật (security audit, penetration test).

## Lộ trình phát triển hạ tầng

- Thêm monitoring tập trung (Prometheus/Grafana, CloudWatch).
- Tự động hóa backup và restore test.
- Đa khu vực (multi-region) cho backend và database.
- Triển khai container/kubernetes khi tải tăng.
- Zero Trust access với Cloudflare Access hoặc IAM chi tiết.

---

Sử dụng các mục con để tìm hiểu chi tiết từng thành phần, từ pipeline triển khai cho tới cấu hình cloud cụ thể và kế hoạch mở rộng trong tương lai.
