---
sidebar_position: 3
title: Cloudflare
---

# Cloudflare

## Vai trò trong hệ thống

Cloudflare được sử dụng để tăng cường hiệu suất và bảo mật cho front-end (Vercel) và các endpoint backend công khai. Các chức năng chính:

- CDN toàn cầu giúp giảm latency.
- DNS management với giao diện thân thiện.
- SSL/TLS miễn phí và tự động gia hạn.
- Bảo vệ trước DDoS và các mối đe dọa tầng ứng dụng.

## Kiến trúc tích hợp

```
Người dùng ─► Cloudflare CDN ─► Vercel (Frontend)
                           └► AWS EC2 (Backend API)
```

## DNS Management

- Quản lý domain: `ldx-insight.com` (ví dụ).
- Record quan trọng:
  - `A` hoặc `CNAME` trỏ đến Vercel (`cname.vercel-dns.com`).
  - `A` trỏ đến Elastic IP của EC2 (nếu expose trực tiếp).
  - `TXT` records cho xác thực (GitHub Pages, email, etc.).
- Bật **Proxy (orange cloud)** cho các record cần CDN/Firewall.

## SSL/TLS

- Sử dụng chế độ **Full** hoặc **Full (strict)**.
- Cấu hình **Always Use HTTPS** và **HSTS** (tùy chọn).
- Tự động trên Vercel thông qua Cloudflare nếu dùng CNAME + proxy.

## Firewall & Security

- **Firewall Rules**: Chặn IP đáng ngờ, chỉ allow IP Việt Nam (nếu cần).
- **Rate Limiting**: Giới hạn số request mỗi IP trong khoảng thời gian nhất định cho API.
- **Bot Management** (nếu dùng gói Pro/E+).
- **WAF Managed Rules**: Bật rule-set mặc định để chống OWASP Top 10.

## Page Rules / Transform Rules

- **Page Rules** (3 rule miễn phí):
  - `https://ldx-insight.com/*` → Bật `Always Online`, `Cache Level` = Standard.
  - `https://api.ldx-insight.com/*` → Bật `Cache Level` = Bypass để không cache API.
- **Transform Rules**: Thêm/ghi đè header (ví dụ `X-Forwarded-Proto`).

## Cache Strategy

- Tắt cache cho các endpoint API (bằng Rule hoặc response headers `Cache-Control: no-store`).
- Cho phép cache static assets của frontend (CSS, JS).
- Sử dụng **Automatic Platform Optimization (APO)** nếu dùng WordPress (không áp dụng ở đây).

## Zero Trust / Access (tùy chọn)

- Có thể cấu hình Cloudflare Access để bảo vệ môi trường staging.
- Sử dụng MFA, Google/Microsoft SSO cho team.

## Logging và Analytics

- **Analytics Dashboard**: Theo dõi lượt truy cập, top countries, response status.
- **Security Analytics**: Xem các request bị chặn.
- **Logpush** (tùy chọn): Đẩy log sang S3/BigQuery/SIEM.

## Quy trình cập nhật cấu hình

1. Thực hiện thay đổi DNS hoặc rules trong Cloudflare Dashboard.
2. Kiểm tra propagation bằng `nslookup` / `dig`.
3. Kiểm tra SSL (https://www.ssllabs.com/ssltest/).
4. Kiểm tra Cloudflare cache bằng response header `cf-cache-status`.

## Lộ trình mở rộng

- **Workers**: Viết logic edge để rewrite request, authenticate, hoặc xử lý A/B testing.
- **KV / Durable Objects**: Lưu trữ lightweight data gần user.
- **Image Optimization**: Tối ưu ảnh cho frontend.
- **R2 Storage**: Lưu file tĩnh không bị egress fee.
