---
sidebar_position: 3
title: Công nghệ sử dụng - Frontend
---

# Công nghệ sử dụng - Frontend

## Framework & Runtime

### Nuxt 4
- **Vai trò**: Framework chính xây dựng SPA/SSR trên nền Vue 3.
- **Tính năng chính**: File-based routing, server-side rendering, Nitro server, composables.
- **Cấu hình**: `nuxt.config.ts` khai báo modules (`@nuxt/ui`, `@pinia/nuxt`, `@vueuse/nuxt`, `@nuxt/image`).

### Vue 3
- Composition API, `<script setup>`, reactive state.
- Hỗ trợ TypeScript tốt, tích hợp Pinia dễ dàng.

### Vite (bundler mặc định)
- Build nhanh, HMR tốc độ cao.
- Tích hợp TypeScript, PostCSS, Tailwind.

## State & Data Layer

### Pinia
- Store thế hệ mới thay Vuex.
- Module `auth` và `app` quản lý trạng thái toàn cục.
- Hỗ trợ SSR thông qua `@pinia/nuxt` plugin.

### Axios
- HTTP client, cấu hình trong `plugins/http.ts`.
- Interceptor gắn base URL (`NUXT_PUBLIC_API_BASE`), header Authorization.

### @vueuse/core
- Bộ composable tiện ích (localStorage, media query, device detection).
- Giúp giảm boilerplate khi làm việc với browser API.

## UI & Styling

### Tailwind CSS 4.x
- Utility-first CSS framework.
- Định nghĩa trong `tailwind.config.js` và import qua `assets/css/main.css`.
- Dễ tuỳ biến theme.

### @nuxt/ui
- Component library dựa trên Radix + Tailwind.
- Cung cấp button, table, form, modal theo chuẩn Nuxt.

### @nuxt/icon & iconify
- Hỗ trợ sử dụng icon (ví dụ bộ `lucide`) trực tiếp trong component.

## TypeScript & Tooling

- **TypeScript 5.6**: Bật strict mode, cải thiện DX.
- **vue-tsc**: Type checking cho component Vue.
- **tsconfig.json**: Alias `~` trỏ tới `src/`.

## Content & Media

### @nuxt/image
- Tối ưu ảnh, lazy load, responsive.
- Tích hợp tốt với các provider CDN (Cloudflare, Vercel).

## Form & Validation (khuyến nghị)

- Có thể dùng `vee-validate` hoặc `zod` kết hợp với composable `useForm` (chưa tích hợp sẵn, roadmap).

## Linting & Formatting

- **Prettier** + `prettier-plugin-tailwindcss` giúp sort class.
- `.prettierrc`, `.prettierignore` đã cấu hình.
- Khuyến nghị thêm ESLint/Vitest cho chất lượng code.

## DevOps & Deployment

- **Vercel**: Build và deploy tự động khi push.
- CI/CD: Không cần GitHub Actions cho frontend (Vercel tự động).
- Monitoring: Vercel Analytics, Cloudflare Analytics.

## Thư viện phụ trợ

| Thư viện | Công dụng |
|----------|-----------|
| `@vueuse/nuxt` | Auto import composables VueUse |
| `@nuxt/content` (optional) | Render content/markdown nếu cần |
| `@nuxt/image` | Tối ưu hình ảnh |
| `@nuxt/ui` | UI components |
| `@nuxt/icon` | Icon component |
| `pinia` | State management |
| `axios` | HTTP client |
| `vue-router` | Router (bên trong Nuxt) |
| `vueuse` | Utility composables |

## Environment Variables

- `NUXT_PUBLIC_API_BASE`: Base URL cho REST API.
- `API_BASE_URL` (server only): Dùng khi cần request từ server (SSR/Nitro) đến backend.
- `NUXT_PUBLIC_APP_NAME`, `NUXT_PUBLIC_ANALYTICS` (tùy chọn): cấu hình hiển thị.

## Sử dụng công nghệ trong dự án

- Mỗi page sử dụng `useAsyncData` để fetch dataset.
- Pinia lưu danh sách dataset, user state để các component truy cập.
- Tailwind & Nuxt UI tạo layout responsive, colours consistent với brand.
- Axios plugin tự động xử lý token, refresh flow.
- Nuxt middleware `auth` bảo vệ route admin.

## Roadmap công nghệ

- Bổ sung Vitest + Playwright cho E2E testing.
- Sử dụng Nuxt Devtools để debug state.
- Tích hợp PWA (`@vite-pwa/nuxt`).
- Áp dụng GraphQL (nếu backend mở rộng) qua `urql` hoặc `apollo`. 
