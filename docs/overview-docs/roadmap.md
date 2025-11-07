---
sidebar_position: 6
title: Lộ trình phát triển
---

# Lộ trình phát triển Ldx-Insight

Tài liệu này tổng hợp kế hoạch ngắn hạn và trung hạn để mở rộng hệ thống, dựa trên hiện trạng mã nguồn và nhu cầu thực tế.

## Giai đoạn 1 – Hoàn thiện nền tảng

- ✅ Backend Spring Boot: Hoàn thiện API datasets, auth JWT, thống kê.
- ✅ Frontend Nuxt: Dashboard, tìm kiếm, tải dataset.
- ✅ OpenHub Crawler: Thu thập dữ liệu Đồng Tháp, HCM, Đà Nẵng, Thanh Hóa.
- ✅ CI/CD: Deploy backend (GitHub Actions + EC2), frontend (Vercel), docs (GH Pages).
- ✅ Tài liệu hóa: Backend, Frontend, Infrastructure, Cloud.

## Giai đoạn 2 – Cải thiện trải nghiệm & vận hành 

| Hạng mục | Công việc chính |
|----------|-----------------|
| Monitoring | Tích hợp CloudWatch hoặc Prometheus/Grafana, log tập trung. |
| Security | Bật lại RBAC chi tiết cho API quản trị, thêm rate limit (Cloudflare). |
| Testing | Unit test (JUnit, Vitest), integration test pipeline CI. |
| Crawler | Hỗ trợ incremental update, đồng bộ metadata trực tiếp vào MongoDB. |
| Frontend | Bổ sung biểu đồ (Nuxt UI chart), bộ lọc nâng cao, internationalization. |

## Giai đoạn 3 – ML & phân tích nâng cao 

- Xây dựng microservice ML/AI:
  - Thuật toán dự báo chỉ số chuyển đổi số (Regression/Forecasting).
  - API `/api/v1/ml/diagnosis` trả kết quả phân tích.
  - Sử dụng dữ liệu chuẩn hóa từ crawler.
- Dashboard phân tích nâng cao:
  - Heatmap theo tỉnh/thành, trend line theo thời gian.
  - Export báo cáo PDF/Excel.
- Data quality pipeline:
  - Kiểm tra schema, detect missing values, scoring chất lượng dữ liệu.

## Giai đoạn 4 – Mở rộng hệ sinh thái

- **Hạ tầng**: Container hóa (Docker), orchestration bằng ECS/EKS, autoscaling backend.
- **Data lakes**: Đồng bộ dữ liệu chuẩn hóa sang kho phân tích (BigQuery/Snowflake).
- **Marketplace**: Cho phép bên thứ ba đăng ký API key, theo dõi usage.
- **Community**: Công bố API SDK (JavaScript/Python), template tích hợp nhanh.

## Hạng mục luôn duy trì

- Cập nhật lỗ hổng bảo mật (dependency updates, CVE).
- Backup định kỳ MongoDB Atlas và snapshot EC2.
- Kiểm tra cost AWS/Vercel/Atlas hàng tháng.
- Nâng cấp tài liệu Docusaurus theo thay đổi kiến trúc.

## Ghi chú triển khai

- Các nhiệm vụ nên được theo dõi thông qua GitHub Projects hoặc Jira.
- Ưu tiên các hạng mục mang lại giá trị nhanh (quick win) trước.
- Áp dụng pull request review để đảm bảo chất lượng mã nguồn.
