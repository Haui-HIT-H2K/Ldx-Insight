---
sidebar_position: 2
title: Thiết kế hệ thống Frontend
---

# Thiết kế hệ thống Frontend

## Tổng quan kiến trúc

Ứng dụng frontend tuân theo kiến trúc **Nuxt 4 Layered** gồm các tầng chính: routing (pages), layout, components, state (Pinia) và service (plugins/composables). Nuxt đảm nhiệm SSR/ISR, routing động, đồng thời cung cấp convention giúp cấu trúc gọn gàng.

## Sơ đồ kiến trúc

```
┌─────────────────────────────┐
│ Browser / Client            │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Nuxt Pages & Layouts        │
│  (Vue components)           │
└──────────────┬──────────────┘
               │ (emit events / props)
               ▼
┌─────────────────────────────┐
│ UI Components & Composables │
│  - Nuxt UI components       │
│  - Custom components        │
└──────────────┬──────────────┘
               │ (mutate state)
               ▼
┌─────────────────────────────┐
│ Pinia Stores                │
│  - app.ts, auth.ts          │
└──────────────┬──────────────┘
               │ (call services)
               ▼
┌─────────────────────────────┐
│ Plugins / API Client        │
│  - plugins/http.ts          │
│  - composables/useApi.ts    │
└──────────────┬──────────────┘
               │ (HTTP request)
               ▼
┌─────────────────────────────┐
│ Backend REST API            │
└─────────────────────────────┘
```

## Cấu trúc thư mục chính

```
frontend/
├── nuxt.config.ts
├── src/
│   ├── app.vue                 # Root component
│   ├── app.config.ts           # App-wide configuration
│   ├── assets/css/main.css     # Global styles
│   ├── components/             # Reusable UI components
│   │   └── app/AppHeader.vue
│   ├── layouts/
│   │   ├── default.vue
│   │   └── blank.vue
│   ├── pages/
│   │   ├── index.vue           # Trang chủ
│   │   ├── data/index.vue      # Danh sách dataset
│   │   ├── data/[id].vue       # Chi tiết dataset động
│   │   ├── users/[id].vue      # Trang người dùng
│   │   └── [...slug].vue       # Catch-all (404 hoặc dynamic)
│   ├── plugins/http.ts         # Axios instance & interceptors
│   ├── stores/
│   │   ├── app.ts              # Global app state
│   │   └── auth.ts             # Auth state, token
│   ├── composables/useApi.ts   # Helper gọi API
│   ├── middleware/auth.ts      # Guard route yêu cầu auth
│   ├── types/                  # Kiểu dữ liệu TypeScript
│   └── utils/                  # Helper (cookie, format)
└── public/                     # Static assets (favicon, robots)
```

## Routing & Layout

- Routing dựa trên cấu trúc `pages/` (file-based routing).
- `layouts/default.vue` bao gồm header, footer, content slot.
- `layouts/blank.vue` dùng cho trang đặc biệt (ví dụ trang đăng nhập modal hoặc error).
- Catch-all route (`pages/[...slug].vue`) xử lý 404 hoặc redirect động.

## State Management (Pinia)

- `app` store: quản lý theme, loading state, cấu hình chung.
- `auth` store: lưu thông tin người dùng, token JWT, helper login/logout.
- Pinia tích hợp với Nuxt qua module `@pinia/nuxt`, cho phép SSR friendly state hydration.

## API Layer

- `plugins/http.ts`: tạo axios client với `baseURL`, interceptors để gắn JWT từ cookie hoặc store.
- `composables/useApi.ts`: wrapper cung cấp hàm `get`, `post`, `put`, `delete` typed.
- Tự động inject vào components thông qua `useApi()`.

## Middleware

- `middleware/auth.ts`: kiểm tra trạng thái đăng nhập trước khi vào route yêu cầu quyền hạn (ví dụ trang quản trị).
- Có thể mở rộng thêm middleware cho logging hoặc i18n.

## Types & Models

- `types/api.type.ts`: định nghĩa kiểu request/response chung.
- `types/dataset.type.ts`, `types/user.type.ts`, `types/auth.type.ts`: mô tả schema dataset, user, JWT response.
- Giúp IDE gợi ý và tránh lỗi runtime.

## Asset & Styling

- Sử dụng **Tailwind CSS v4.1** với file config `tailwind.config.js` và entry `assets/css/main.css`.
- Kết hợp **Nuxt UI** (dựa trên Radix + Tailwind) để dùng component sẵn có.
- Có thể custom theme thông qua `app.config.ts` và tokens của Nuxt UI.

## Quy trình render

1. Khi truy cập route, Nuxt xác định layout và component tương ứng.
2. `asyncData`/`useAsyncData` được gọi để fetch dữ liệu (nếu SSR).
3. Pinia store được hydrate với dữ liệu fetch.
4. Component render ra HTML, Nuxt gửi về client (SSR) hoặc CSR.
5. Client rehydrate và tiếp tục xử lý tương tác (SPA experience).

## Bảo mật phía client

- Token lưu trong cookie HttpOnly (qua backend), hạn chế XSS.
- Middleware kiểm tra quyền; hạn chế truy cập route admin.
- Axios interceptors refresh token hoặc redirect login khi 401.

## Testing & Quality

- Đề xuất sử dụng: `vitest` cho unit test component/composable.
- `eslint` + `prettier` + `stylelint` (kết hợp plugin tailwind) cho style consistency.
- `nuxt typecheck` (`vue-tsc`) để đảm bảo type safety.

## Khả năng mở rộng

- Có thể split modules bằng `src/modules/` hoặc `server/api/` khi thêm API edge.
- Hỗ trợ lazy-load components (`defineAsyncComponent`) cho trang nặng.
- Sử dụng `route rules` của Nuxt để cấu hình caching/ISR riêng cho từng route.
