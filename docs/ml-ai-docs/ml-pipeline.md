---
sidebar_position: 6
title: Cài đặt & Vận hành ML Pipeline (nohup)
---

# Cài đặt & Vận hành ML Pipeline

## Yêu cầu hệ thống

- Hệ điều hành Linux (hoặc macOS)
- Python 3.10+
- `pip` / `venv`
- Quyền ghi thư mục để lưu trữ logs, database, và artifacts.

---

## 1. Cài đặt Môi trường Python

Bạn cần một môi trường ảo duy nhất để chứa tất cả các thư viện.

```
pip apache-airflow mlflow scikit-learn pandas pendulum
```

---

## 2. Cấu hình và Chạy Services

### A. Khởi chạy MLflow Server

1.  **Chạy MLflow server bằng `nohup`:**

    ```
    nohup mlflow server --host 0.0.0.0 --allowed-hosts "localhost,34.87.86.201,34.87.86.201:5000" > mlflow.log 2>&1 &
    ```

2.  **Kiểm tra:**
    - Truy cập Giao diện MLflow tại: `http://<dia_chi_ip_may_chu>:5000`
    - Xem log: `tail -f mlflow.log`
    - Tìm PID (Process ID) để `kill` nếu cần: `ps aux | grep "mlflow server"`

### B. Khởi chạy Airflow

1.  **Cấu hình thư mục DAGs:**
    Mặc định, Airflow tìm DAGs trong `~/airflow/dags`. Viết file cấu hình của dag airflow và lưu vào thư mục trên

2.  **Chạy Airflow Webserver bằng `nohup`:**
    Chạy `nohup airflow api-server --port 8080 > airflow.log 2>&1 &` và sau đó kiểm tra log trong `airflow.log`.

3.  **Kiểm tra:**
    - Truy cập Giao diện Airflow: `http://<dia_chi_ip_may_chu>:8080` (Đăng nhập bằng tài khoản admin).
    - Xem log: `tail -f airflow_webserver.log` hoặc `tail -f airflow_scheduler.log`.
    - Tìm PIDs: `ps aux | grep "airflow webserver"` và `ps aux | grep "airflow scheduler"`.

---

## 3. Vận hành Pipeline

1.  **Mở Giao diện Airflow:** `http://<ip_may_chu>:8080`.
2.  **Kích hoạt:** Tìm DAG của bạn và gạt nút "Un-pause" (từ ⏸️ sang ▶️).
3.  **Theo dõi:** DAG sẽ tự động chạy theo lịch. Bạn cũng có thể nhấn nút "Trigger" (▶️) để chạy thủ công.
4.  **Kiểm tra MLflow:** Mở `http://<ip_may_chu>:5000`. Bạn sẽ thấy "Experiment" mới xuất hiện sau khi task `train_model` chạy.

---
