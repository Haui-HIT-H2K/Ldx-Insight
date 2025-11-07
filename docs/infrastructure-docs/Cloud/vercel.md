---
sidebar_position: 4
title: Vercel Deployment
---

# Vercel Deployment

## Tổng quan

Vercel được sử dụng để deploy frontend (Nuxt.js) của dự án Ldx-Insight. Nền tảng hỗ trợ CI/CD tự động qua GitHub integration, cung cấp CDN toàn cầu và SSL mặc định.

## Kiến trúc triển khai

```
GitHub Repo (branch main)
        │  Webhook
        ▼
Vercel Build Pipeline
        │  (npm install, nuxt build)
        ▼
Global Edge Network
        │
 Người dùng truy cập
```

## Cấu hình Project

- **Framework Preset**: Nuxt.
- **Root Directory**: `frontend`.
- **Build Command**: `npm run build`.
- **Output Directory**: `.output` (Nuxt 3/4 default).
- **Install Command**: `npm install`.
- **Development Command**: `npm run dev` (local preview via `vercel dev`).

## Environment Variables

Thiết lập trong Vercel Dashboard (`Project Settings → Environment Variables`):

| Key | Environment | Mô tả |
| --- | ----------- | ----- |
| `NUXT_PUBLIC_API_BASE` | All | Base URL cho API public |
| `API_BASE_URL` | Production/Preview | URL backend Spring Boot |
| `NODE_ENV` | All | `production` hoặc `development` |

Có thể đồng bộ env từ `.env` bằng `vercel env pull`.

## Deployment Types

- **Production**: Tự động từ `main`. Domain ví dụ `https://ldx-insight.vercel.app`.
- **Preview**: Tự động cho mỗi Pull Request/branch (`https://ldx-insight-git-feature.vercel.app`).
- **Development**: Chạy local với `vercel dev`.

## Custom Domain

1. Add Domain trong Vercel (`ldx-insight.com`).
2. Cấu hình DNS (qua Cloudflare):
   - `CNAME @` → `cname.vercel-dns.com`.
   - `CNAME www` → `cname.vercel-dns.com`.
3. Bật `www` redirect nếu cần.
4. SSL tự động.

## Routing và Headers

Sử dụng file `vercel.json` (tùy chọn) để cấu hình thêm:

```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "https://api.ldx-insight.com/$1" }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "SAMEORIGIN" },
        { "key": "X-Content-Type-Options", "value": "nosniff" }
      ]
    }
  ]
}
```

## Build Logs và Monitoring

- **Build Logs**: Hiển thị trực tiếp trên Vercel dashboard.
- **Analytics**: Theo dõi page views, Core Web Vitals.
- **Speed Insights**: Gợi ý tối ưu tốc độ.
- **Error Tracking**: Tích hợp Sentry hoặc Logtail (nếu cần).

## Best Practices

1. **Pin package versions** trong `package.json`.
2. **Kiểm tra preview deployments** trước khi merge.
3. **Bật `Ignore Build Step`** nếu không có thay đổi frontend (dùng `vercel.json`).
4. **Xóa preview cũ** để tiết kiệm quota (nếu dùng gói miễn phí).
5. **Giới hạn Environment Variables** theo environment.

## CLI Commands hữu ích

```bash
# Đăng nhập
vercel login

# Link project cục bộ với Vercel
vercel link

# Deploy preview
vercel

# Deploy production
vercel --prod

# Pull environment variables
vercel env pull .env.local
```

## Lộ trình nâng cấp

- **Edge Middleware**: Chạy logic xác thực nhẹ tại edge.
- **Image Optimization**: Sử dụng Vercel Image Optimization.
- **ISR (Incremental Static Regeneration)**: Có thể bật trong Nuxt để cache trang.
- **Observability**: Tích hợp với Log Drains (Datadog, New Relic).
- **Serverless Functions**: Triển khai API nhỏ tại edge nếu cần.
