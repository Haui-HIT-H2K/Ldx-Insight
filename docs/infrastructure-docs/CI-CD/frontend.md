---
sidebar_position: 3
title: CI/CD cho Frontend (Nuxt.js + Vercel)
---

# CI/CD cho Frontend (Nuxt.js + Vercel)

## Tổng quan

Hệ thống CI/CD cho Frontend được thiết kế để tự động build và deploy ứng dụng Nuxt.js lên Vercel mỗi khi có code mới được push lên repository. Vercel tích hợp sẵn với GitHub để tự động hóa toàn bộ quy trình CI/CD mà không cần cấu hình GitHub Actions.

## Kiến trúc CI/CD

```
┌─────────────────┐
│  GitHub Push    │
│  (any branch)   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Vercel Webhook │
│  (Auto-trigger) │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ↓         ↓
┌──────┐  ┌──────┐
│Install│  │ Build │
│Deps  │  │Nuxt.js│
└──┬───┘  └──┬───┘
   │         │
   └────┬────┘
        │
        ↓
┌─────────────────┐
│  Deploy to      │
│  Vercel Edge    │
│  Network        │
└─────────────────┘
```

## Công nghệ sử dụng

### 1. Vercel
- **Mục đích**: Platform để deploy và host frontend
- **Tính năng**:
  - Automatic deployments từ GitHub
  - Preview deployments cho mỗi PR
  - Edge Network (CDN global)
  - Serverless functions support
  - Environment variables management
  - Analytics và monitoring

### 2. Nuxt.js
- **Version**: 4.2.0
- **Mục đích**: Vue.js framework cho SSR/SSG
- **Build output**: Static files hoặc serverless functions
- **Deployment mode**: 
  - Static Site Generation (SSG)
  - Server-Side Rendering (SSR)
  - Hybrid rendering

### 3. GitHub Integration
- **Mục đích**: Source code repository
- **Integration**: Tự động qua Vercel Dashboard
- **Branches**:
  - `main`: Production deployment
  - Feature branches: Preview deployments

## Quy trình CI/CD với Vercel

### Bước 1: Kết nối Repository với Vercel

1. **Đăng nhập Vercel**:
   - Truy cập [vercel.com](https://vercel.com)
   - Đăng nhập bằng GitHub account

2. **Import Project**:
   - Click "Add New" → "Project"
   - Chọn repository `Ldx-Insight`
   - Vercel tự động detect Nuxt.js

3. **Cấu hình Project**:
   - **Framework Preset**: Nuxt.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (hoặc tự động)
   - **Output Directory**: `.output` (Nuxt 3+)
   - **Install Command**: `npm install`

### Bước 2: Automatic Deployment

Sau khi kết nối, Vercel tự động:

1. **Webhook Setup**: Tự động tạo webhook trong GitHub
2. **Auto Deploy**: Mỗi push sẽ trigger deployment
3. **Build Process**: Chạy build command
4. **Deploy**: Deploy lên Vercel Edge Network

### Bước 3: Build Process

Vercel tự động chạy:

```bash
# Install dependencies
npm install

# Build application
npm run build
```

**Nuxt.js build process**:
1. Compile TypeScript → JavaScript
2. Bundle Vue components
3. Generate routes
4. Optimize assets
5. Create output trong `.output/`

### Bước 4: Deployment

- **Production**: Deploy từ nhánh `main`
- **Preview**: Deploy từ feature branches và PRs
- **URL**: 
  - Production: `https://ldx-insight.vercel.app`
  - Preview: `https://ldx-insight-git-{branch}.vercel.app`

## Cấu hình Vercel

### 1. Project Settings

Trong Vercel Dashboard → Project Settings:

#### General
- **Project Name**: `ldx-insight-frontend`
- **Framework**: Nuxt.js
- **Root Directory**: `frontend`

#### Build & Development Settings
```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "outputDirectory": ".output"
}
```

#### Environment Variables
- `API_BASE_URL`: Backend API URL
- `NUXT_PUBLIC_API_BASE`: Public API base URL
- Các biến môi trường khác

### 2. vercel.json (Optional)

Có thể tạo file `vercel.json` trong root để cấu hình:

```json
{
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/.output",
  "devCommand": "cd frontend && npm run dev",
  "installCommand": "cd frontend && npm install",
  "framework": "nuxtjs",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/"
    }
  ]
}
```

### 3. Nuxt.js Configuration

File `nuxt.config.ts`:

```typescript
export default defineNuxtConfig({
  srcDir: 'src/',
  modules: ['@nuxt/ui', '@pinia/nuxt', '@vueuse/nuxt', '@nuxt/image'],
  
  // Runtime config cho environment variables
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || '/api',
    },
  },
});
```

## Environment Variables

### Cấu hình trong Vercel

1. Vào Project Settings → Environment Variables
2. Thêm variables cho từng environment:

**Production**:
- `API_BASE_URL`: `https://api.ldx-insight.com`
- `NUXT_PUBLIC_API_BASE`: `https://api.ldx-insight.com/api/v1`

**Preview**:
- `API_BASE_URL`: `http://localhost:8080`
- `NUXT_PUBLIC_API_BASE`: `http://localhost:8080/api/v1`

**Development**:
- `API_BASE_URL`: `http://localhost:8080`
- `NUXT_PUBLIC_API_BASE`: `http://localhost:8080/api/v1`

### Sử dụng trong Code

```typescript
// nuxt.config.ts
runtimeConfig: {
  public: {
    apiBase: process.env.NUXT_PUBLIC_API_BASE || '/api',
  },
}

// Trong component/composable
const config = useRuntimeConfig()
const apiBase = config.public.apiBase
```

## Deployment Types

### 1. Production Deployment

- **Trigger**: Push vào nhánh `main`
- **URL**: Production domain (ví dụ: `ldx-insight.vercel.app`)
- **Status**: Live và public
- **Cache**: Aggressive caching

### 2. Preview Deployment

- **Trigger**: 
  - Push vào feature branch
  - Open/update Pull Request
- **URL**: `https://ldx-insight-git-{branch-name}.vercel.app`
- **Status**: Temporary, tự động xóa sau khi merge/close
- **Cache**: No cache

### 3. Development Deployment

- **Trigger**: Manual từ Vercel CLI
- **URL**: Development URL
- **Status**: For testing

## Vercel CLI (Local Development)

### Cài đặt Vercel CLI

```bash
npm i -g vercel
```

### Login

```bash
vercel login
```

### Link Project

```bash
cd frontend
vercel link
```

### Deploy

```bash
# Preview deployment
vercel

# Production deployment
vercel --prod
```

### Environment Variables

```bash
# Add environment variable
vercel env add API_BASE_URL

# List environment variables
vercel env ls

# Pull environment variables
vercel env pull .env.local
```

## Monitoring và Logs

### 1. Vercel Dashboard

- **Deployments**: Xem tất cả deployments
- **Analytics**: Traffic, performance metrics
- **Logs**: Real-time function logs
- **Speed Insights**: Core Web Vitals

### 2. Xem Logs

**Trong Dashboard**:
1. Vào Project → Deployments
2. Click vào deployment
3. Tab "Functions" hoặc "Logs"

**Qua CLI**:
```bash
vercel logs [deployment-url]
```

### 3. Analytics

Vercel Analytics tự động track:
- Page views
- Unique visitors
- Performance metrics
- Core Web Vitals (LCP, FID, CLS)

## Troubleshooting

### 1. Build Failed

**Nguyên nhân**:
- Dependencies issues
- TypeScript errors
- Build command sai

**Giải pháp**:
- Kiểm tra logs trong Vercel Dashboard
- Test build local: `npm run build`
- Kiểm tra Node.js version (Vercel dùng Node 20.x)

### 2. Environment Variables không hoạt động

**Nguyên nhân**:
- Variable chưa được set
- Wrong environment (production vs preview)
- Variable name sai

**Giải pháp**:
- Kiểm tra trong Vercel Dashboard → Environment Variables
- Đảm bảo variable có prefix `NUXT_PUBLIC_` nếu cần public
- Redeploy sau khi thêm variables

### 3. API calls failed (CORS)

**Nguyên nhân**:
- Backend CORS chưa allow Vercel domain
- API URL sai

**Giải pháp**:
- Thêm Vercel domain vào CORS config của backend
- Kiểm tra `API_BASE_URL` environment variable
- Sử dụng absolute URL cho API calls

### 4. 404 trên routes

**Nguyên nhân**:
- Nuxt routing config sai
- Rewrites chưa được cấu hình

**Giải pháp**:
- Kiểm tra `nuxt.config.ts`
- Thêm rewrites trong `vercel.json` nếu cần
- Đảm bảo pages được đặt đúng trong `src/pages/`

### 5. Slow build times

**Nguyên nhân**:
- Dependencies quá lớn
- Build process không tối ưu

**Giải pháp**:
- Enable build cache trong Vercel
- Optimize dependencies
- Sử dụng `.vercelignore` để exclude files không cần

## Best Practices

### 1. Environment Management

- **Separate environments**: Production, Preview, Development
- **Secure variables**: Không commit secrets
- **Public variables**: Sử dụng `NUXT_PUBLIC_` prefix

### 2. Performance

- **Image optimization**: Sử dụng `@nuxt/image`
- **Code splitting**: Nuxt tự động code split
- **Static generation**: Sử dụng SSG khi có thể
- **Edge caching**: Tận dụng Vercel Edge Network

### 3. Security

- **Environment variables**: Không expose trong client code
- **API keys**: Chỉ dùng server-side
- **CORS**: Cấu hình đúng trong backend

### 4. Monitoring

- **Enable Analytics**: Bật Vercel Analytics
- **Error tracking**: Tích hợp Sentry nếu cần
- **Performance monitoring**: Theo dõi Core Web Vitals

### 5. Git Workflow

- **Branch strategy**:
  - `main`: Production
  - `develop`: Staging
  - Feature branches: Preview
- **PR reviews**: Review trước khi merge
- **Commit messages**: Rõ ràng, descriptive

## Custom Domain

### 1. Thêm Custom Domain

1. Vào Project Settings → Domains
2. Add domain: `ldx-insight.com`
3. Follow DNS instructions
4. Vercel tự động setup SSL certificate

### 2. DNS Configuration

**A Record** hoặc **CNAME**:
```
Type: CNAME
Name: @ (hoặc www)
Value: cname.vercel-dns.com
```

### 3. SSL Certificate

- Vercel tự động cung cấp SSL certificate
- Auto-renewal
- HTTPS enforced

## Advanced Features

### 1. Serverless Functions

Nuxt.js có thể tạo API routes:

```typescript
// server/api/hello.ts
export default defineEventHandler((event) => {
  return { message: 'Hello from Vercel!' }
})
```

Vercel tự động deploy như serverless functions.

### 2. Edge Functions

Deploy functions lên Edge Network:

```typescript
// server/api/edge.ts
export default defineEventHandler({
  edge: true
}, (event) => {
  return { message: 'Hello from Edge!' }
})
```

### 3. Incremental Static Regeneration (ISR)

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  nitro: {
    prerender: {
      routes: ['/'],
      crawlLinks: true,
    }
  }
})
```

### 4. Redirects và Rewrites

Trong `vercel.json`:

```json
{
  "redirects": [
    {
      "source": "/old",
      "destination": "/new",
      "permanent": true
    }
  ],
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://api.example.com/:path*"
    }
  ]
}
```

## CI/CD Workflow Summary

### Automatic Flow

```
Developer pushes code
    ↓
GitHub webhook triggers Vercel
    ↓
Vercel installs dependencies
    ↓
Vercel runs build command
    ↓
Vercel deploys to Edge Network
    ↓
Website live (production/preview)
```

### Manual Deployment

```bash
# Via CLI
vercel --prod

# Via Dashboard
# Click "Redeploy" trong Vercel Dashboard
```

## So sánh với GitHub Actions

| Feature | Vercel | GitHub Actions |
|---------|--------|----------------|
| Setup | Tự động, không cần config | Cần tạo workflow file |
| Preview Deployments | Tự động cho mỗi PR | Cần cấu hình |
| Build Time | Optimized, cached | Depends on runner |
| Edge Network | Global CDN | N/A |
| Cost | Free tier available | Free cho public repos |
| Configuration | Minimal | Full control |

## Tài liệu tham khảo

- [Vercel Documentation](https://vercel.com/docs)
- [Nuxt.js Deployment](https://nuxt.com/docs/getting-started/deployment)
- [Vercel CLI](https://vercel.com/docs/cli)
- [Nuxt.js Configuration](https://nuxt.com/docs/guide/going-further/runtime-config)

