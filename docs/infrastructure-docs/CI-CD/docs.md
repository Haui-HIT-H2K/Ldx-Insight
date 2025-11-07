---
sidebar_position: 2
title: CI/CD cho Documentation (Docusaurus)
---

# CI/CD cho Documentation (Docusaurus)

## Tổng quan

Hệ thống CI/CD cho Documentation được thiết kế để tự động build và deploy website Docusaurus lên GitHub Pages mỗi khi có thay đổi trong thư mục `docs` được push lên nhánh `main`.

## Kiến trúc CI/CD

```
┌─────────────────┐
│  GitHub Push    │
│  (main branch)  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ GitHub Actions  │
│  (CI/CD Workflow)│
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ↓         ↓
┌──────┐  ┌──────┐
│Setup │  │Install│
│Node.js│  │Deps  │
└──┬───┘  └──┬───┘
   │         │
   └────┬────┘
        │
        ↓
┌─────────────────┐
│  Build Docs     │
│  (Docusaurus)   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Upload Artifact │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Deploy to      │
│  GitHub Pages   │
└─────────────────┘
```

## Công nghệ sử dụng

### 1. GitHub Actions
- **Mục đích**: CI/CD pipeline automation
- **Workflow file**: `.github/workflows/deploy-docs.yml`
- **Trigger**: Push vào nhánh `main`

### 2. Docusaurus
- **Version**: 3.9.2
- **Mục đích**: Static site generator cho documentation
- **Framework**: React-based
- **Features**: 
  - Multi-doc support
  - Mermaid diagrams
  - Search functionality
  - Dark mode

### 3. GitHub Pages
- **Mục đích**: Hosting static website
- **URL**: `https://Haui-HIT-NhoNguoiYeuCu.github.io/Ldx-Insight/`
- **Deployment**: Tự động từ GitHub Actions

### 4. Node.js
- **Version**: 20.x
- **Mục đích**: Runtime cho Docusaurus build process

## Quy trình CI/CD chi tiết

### Bước 1: Trigger Workflow

Workflow được kích hoạt tự động khi:
- Code được push lên nhánh `main`
- Có thay đổi trong thư mục `docs/`

```yaml
on:
  push:
    branches: ["main"]
```

### Bước 2: Set Permissions

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

Cấp quyền cho workflow:
- **contents: read**: Đọc repository
- **pages: write**: Ghi vào GitHub Pages
- **id-token: write**: Xác thực với GitHub Pages

### Bước 3: Checkout Code

```yaml
- name: Checkout
  uses: actions/checkout@v4
```

GitHub Actions checkout code từ repository về runner.

### Bước 4: Setup Node.js

```yaml
- name: Set up Node.js
  uses: actions/setup-node@v4
  with:
    node-version: "20"
    cache: "npm"
    cache-dependency-path: "docs/package-lock.json"
```

- Cài đặt Node.js version 20
- Enable npm cache để tăng tốc độ install
- Cache dựa trên `docs/package-lock.json`

### Bước 5: Install Dependencies và Build

```yaml
- name: Install and Build
  run: |
    npm ci
    npm run build
  working-directory: ./docs
```

**Chi tiết**:
- `npm ci`: Clean install (xóa node_modules và cài lại từ package-lock.json)
- `npm run build`: Build Docusaurus site thành static files
- `working-directory: ./docs`: Chạy trong thư mục docs
- Output: `docs/build/` chứa các file static HTML, CSS, JS

### Bước 6: Upload Artifact

```yaml
- name: Upload artifact
  uses: actions/upload-pages-artifact@v3
  with:
    path: ./docs/build
```

- Upload thư mục `build` lên GitHub Actions artifact
- Artifact này sẽ được sử dụng ở bước deploy

### Bước 7: Deploy to GitHub Pages

```yaml
- name: Deploy to GitHub Pages
  id: deployment
  uses: actions/deploy-pages@v4
```

- Deploy artifact lên GitHub Pages
- Tự động cập nhật website tại URL đã cấu hình
- Sử dụng GitHub Pages Actions (không cần gh-pages branch)

## Cấu hình Docusaurus

### docusaurus.config.ts

File cấu hình chính của Docusaurus:

```typescript
const config: Config = {
  title: "Ldx-Insight",
  tagline: "Hệ thống chia sẻ thông tin nguồn mở Ldx-Insight",
  
  url: "https://Haui-HIT-NhoNguoiYeuCu.github.io",
  baseUrl: "/Ldx-Insight/",
  
  organizationName: "Haui-HIT-NhoNguoiYeuCu",
  projectName: "Ldx-Insight",
  
  // ... other config
};
```

**Quan trọng**:
- `baseUrl`: Phải khớp với repository name (`/Ldx-Insight/`)
- `url`: GitHub Pages URL
- `organizationName` và `projectName`: Dùng để generate URL

### Multi-docs Setup

Docusaurus được cấu hình với nhiều doc instances:

```typescript
plugins: [
  ["@docusaurus/plugin-content-docs", {
    id: "overview",
    path: "overview-docs",
    routeBasePath: "overview",
    sidebarPath: "./sidebarsOverview.ts",
  }],
  ["@docusaurus/plugin-content-docs", {
    id: "backend",
    path: "backend-docs",
    routeBasePath: "backend",
    sidebarPath: "./sidebarsBackend.ts",
  }],
  // ... more plugins
]
```

Mỗi plugin tạo một section documentation riêng:
- `/overview/`: System Overview docs
- `/backend/`: Backend documentation
- `/frontend/`: Frontend documentation
- `/ml-ai/`: ML/AI documentation
- `/infrastructure/`: Infrastructure documentation

## Cấu hình GitHub Pages

### 1. Enable GitHub Pages

1. Vào repository Settings
2. Pages → Build and deployment
3. Source: **GitHub Actions**

### 2. Environment Setup

Workflow tự động tạo environment `github-pages`:
```yaml
environment:
  name: github-pages
  url: ${{ steps.deployment.outputs.page_url }}
```

### 3. URL Structure

Sau khi deploy, website sẽ có URL:
```
https://Haui-HIT-NhoNguoiYeuCu.github.io/Ldx-Insight/
```

Các section:
- `https://Haui-HIT-NhoNguoiYeuCu.github.io/Ldx-Insight/overview/`
- `https://Haui-HIT-NhoNguoiYeuCu.github.io/Ldx-Insight/backend/`
- `https://Haui-HIT-NhoNguoiYeuCu.github.io/Ldx-Insight/frontend/`
- etc.

## Local Development

### Cài đặt dependencies

```bash
cd docs
npm install
```

### Chạy development server

```bash
npm start
```

Website sẽ chạy tại: `http://localhost:3000`

### Build local

```bash
npm run build
```

Output trong thư mục `build/`

### Preview build

```bash
npm run serve
```

Serve static files từ thư mục `build/`

## Monitoring và Troubleshooting

### Kiểm tra trạng thái deployment

1. **GitHub Actions**:
   - Vào tab "Actions" trong GitHub repository
   - Xem workflow "Deploy Docusaurus Docs to GitHub Pages"
   - Kiểm tra logs từng step

2. **GitHub Pages**:
   - Settings → Pages
   - Xem deployment history
   - Kiểm tra URL và status

### Các lỗi thường gặp

#### 1. Lỗi: Build failed - Module not found

**Nguyên nhân**:
- Dependencies chưa được cài đặt
- package-lock.json không sync với package.json

**Giải pháp**:
```bash
cd docs
rm -rf node_modules package-lock.json
npm install
```

#### 2. Lỗi: Broken links

**Nguyên nhân**:
- File markdown bị xóa nhưng vẫn được reference
- Đường dẫn sai trong sidebar config

**Giải pháp**:
- Kiểm tra `onBrokenLinks: "throw"` trong config
- Sửa các broken links hoặc set `onBrokenLinks: "warn"`

#### 3. Lỗi: Permission denied khi deploy

**Nguyên nhân**:
- Permissions chưa được set đúng
- GitHub Pages chưa được enable

**Giải pháp**:
- Kiểm tra permissions trong workflow file
- Enable GitHub Pages trong repository settings
- Đảm bảo sử dụng GitHub Actions làm source

#### 4. Lỗi: Base URL không đúng

**Nguyên nhân**:
- `baseUrl` trong config không khớp với repository name
- Thiếu trailing slash

**Giải pháp**:
```typescript
// Đúng
baseUrl: "/Ldx-Insight/",  // Có trailing slash

// Sai
baseUrl: "/Ldx-Insight",   // Thiếu trailing slash
```

#### 5. Lỗi: Build timeout

**Nguyên nhân**:
- Build quá lâu
- Dependencies quá lớn

**Giải pháp**:
- Kiểm tra cache đã được enable
- Tối ưu dependencies
- Kiểm tra build logs để tìm bottleneck

#### 6. Lỗi: Mermaid diagrams không hiển thị

**Nguyên nhân**:
- Theme Mermaid chưa được cấu hình
- Markdown syntax sai

**Giải pháp**:
```typescript
// Đảm bảo có trong config
themes: ["@docusaurus/theme-mermaid"],
markdown: { mermaid: true },
```

## Best Practices

### 1. Content Management

- **File naming**: Sử dụng kebab-case cho file names
- **Frontmatter**: Luôn thêm frontmatter với `sidebar_position` và `title`
- **Images**: Lưu images trong `static/img/`
- **Links**: Sử dụng relative paths cho internal links

### 2. Performance

- **Image optimization**: Compress images trước khi commit
- **Code splitting**: Docusaurus tự động code split
- **Lazy loading**: Images được lazy load tự động

### 3. SEO

- **Meta tags**: Cấu hình trong `docusaurus.config.ts`
- **Sitemap**: Tự động generate
- **Structured data**: Tự động thêm

### 4. Version Control

- **Commit messages**: Rõ ràng, mô tả thay đổi
- **Branch strategy**: 
  - `main`: Production docs
  - Feature branches: Cho major changes
- **Review process**: Review trước khi merge

### 5. Documentation Quality

- **Consistency**: Giữ format nhất quán
- **Examples**: Thêm code examples khi có thể
- **Diagrams**: Sử dụng Mermaid cho diagrams
- **Screenshots**: Thêm screenshots khi cần

## Workflow Customization

### Thêm build step tùy chỉnh

```yaml
- name: Custom build step
  run: |
    # Your custom commands
    npm run custom-script
  working-directory: ./docs
```

### Thêm test step

```yaml
- name: Test documentation
  run: |
    npm run typecheck
    npm run lint
  working-directory: ./docs
```

### Conditional deployment

```yaml
- name: Deploy to GitHub Pages
  if: github.ref == 'refs/heads/main'
  uses: actions/deploy-pages@v4
```

### Multiple environments

```yaml
jobs:
  deploy-staging:
    if: github.ref == 'refs/heads/develop'
    # ... staging config
  
  deploy-production:
    if: github.ref == 'refs/heads/main'
    # ... production config
```

## Cải tiến tương lai

1. **Preview Deployments**: Deploy preview cho mỗi PR
2. **Automated Testing**: Test broken links, syntax errors
3. **Performance Monitoring**: Track page load times
4. **Analytics**: Tích hợp Google Analytics hoặc Plausible
5. **Search Enhancement**: Cải thiện search functionality
6. **Multi-language**: Hỗ trợ nhiều ngôn ngữ
7. **Versioning**: Version documentation theo releases
8. **Automated Screenshots**: Tự động generate screenshots

## Tài liệu tham khảo

- [Docusaurus Documentation](https://docusaurus.io/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Docusaurus Deployment Guide](https://docusaurus.io/docs/deployment)

