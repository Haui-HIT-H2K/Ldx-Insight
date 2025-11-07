---
sidebar_position: 4
title: Hướng dẫn cài đặt và chạy Frontend
---

# Hướng dẫn cài đặt và chạy Frontend

## Yêu cầu hệ thống

- **Node.js**: 20.x (theo `package.json` engines)
- **npm**: 10.x (đi kèm Node 20)
- **Git**: để clone repository
- **VS Code / WebStorm** (khuyến nghị) với plugin Vue/Nuxt

## Bước 1: Clone và cài đặt

```bash
git clone <repository-url>
cd Ldx-Insight/frontend

# Cài đặt dependencies
npm install
```

Nếu sử dụng pnpm/yarn/bun có thể thay thế bằng lệnh tương ứng.

## Bước 2: Cấu hình environment

Tạo file `.env` hoặc `.env.local` (không commit) với nội dung:

```bash
NUXT_PUBLIC_API_BASE=http://localhost:8080/api/v1
API_BASE_URL=http://localhost:8080/api/v1
```

- `NUXT_PUBLIC_API_BASE`: Dùng cho request phía client (public).
- `API_BASE_URL`: Dùng cho request phía server (SSR/Nitro). Có thể bỏ nếu không dùng server routes.
- Khi deploy production, giá trị này trỏ đến domain backend thật.

## Bước 3: Chạy development server

```bash
npm run dev
```

- Server mặc định chạy ở `http://localhost:3000`.
- Hỗ trợ HMR (Hot Module Replacement).
- Có thể thêm flag `--host` để truy cập từ thiết bị khác trong LAN.

## Bước 4: Build production

```bash
npm run build
```

- Tạo output trong `.output/` (Nitro) và `.nuxt/`.
- Dùng `npm run preview` để chạy server preview (Nitro) tại cục bộ.

## Bước 5: Kiểm tra chất lượng

Khuyến nghị bổ sung các script sau (nếu chưa có):

```bash
npm run lint      # ví dụ chạy eslint
npm run typecheck # sử dụng vue-tsc kiểm tra types
npm run test      # vitest hoặc jest nếu cấu hình
```

## Cấu hình Tailwind & Nuxt UI

- Tailwind đã được khai báo trong `tailwind.config.js` và import ở `assets/css/main.css`.
- Có thể chạy `npx tailwindcss -i ./src/assets/css/main.css -o ./dist/output.css --watch` nếu cần build thủ công.
- `@nuxt/ui` tự động scan class Tailwind, không cần cấu hình thêm.

## Plugin Axios

- Kiểm tra `plugins/http.ts` để đảm bảo baseURL lấy từ env:

```ts
const config = useRuntimeConfig();
const api = $fetch.create({
  baseURL: config.public.apiBase
});
```

- Khi chạy local, backend phải chạy tại `http://localhost:8080` (hoặc chỉnh env).

## Deploy thủ công (không qua Vercel)

1. Build dự án: `npm run build`.
2. Copy thư mục `.output` lên server.
3. Chạy bằng Node:
   ```bash
   node .output/server/index.mjs
   ```
4. Reverse proxy bằng Nginx/Caddy để phục vụ qua HTTPS.

## Deploy trên Vercel

- Kết nối repo trong Vercel Dashboard.
- Cấu hình project: Root `frontend`, Build command `npm run build`, Output `.output/public` (Nuxt tự detect).
- Thiết lập environment variables trong Vercel (`NUXT_PUBLIC_API_BASE`, `API_BASE_URL`).
- Mỗi lần push lên `main`, Vercel tự động deploy.

## Tích hợp với backend local

- Chạy backend Spring Boot: `mvn spring-boot:run` tại `backend/ldx-insight-backend`.
- Đảm bảo CORS cho `http://localhost:3000` (đã cấu hình trong `SecurityConfig`).
- Frontend gọi API qua axios (cùng base URL).

## Debug

- Sử dụng **Nuxt DevTools** (`npx nuxi devtools enable`) để xem state, route, component.
- Chrome DevTools để monitor network/API.
- Kiểm tra log trong console server khi chạy `npm run dev`.

## Troubleshooting

| Lỗi | Nguyên nhân | Khắc phục |
|-----|-------------|-----------|
| `ERR_MODULE_NOT_FOUND` | Cài đặt thiếu module | Xóa `node_modules` và `package-lock.json`, chạy `npm install` |
| 404 API | Sai `NUXT_PUBLIC_API_BASE` | Kiểm tra `.env`, console log baseURL |
| CORS error | Backend chưa allow domain | Bổ sung origin vào `SecurityConfig` |
| Unable to resolve path `~/` | Sai alias TypeScript | Kiểm tra `tsconfig.json` (`paths: { "~/*": ["./src/*"] }`) |
| Tailwind chưa chạy | Quên import CSS | Đảm bảo `css: ['~/assets/css/main.css']` trong `nuxt.config.ts` |

## Lưu ý khi commit

- Không commit `.env*`, `node_modules`, `.output`, `.nuxt` (đã trong `.gitignore`).
- Format code trước khi push: `npm run format` (`prettier`).
- Viết commit message rõ ràng (ví dụ Conventional Commits).

## Roadmap vận hành

- Bổ sung CI check (GitHub Actions) để run lint + typecheck trước khi deploy.
- Tích hợp Sentry cho error tracking.
- Theo dõi Core Web Vitals bằng Vercel Analytics hoặc Lighthouse CI.
