---
sidebar_position: 5
title: Bài toán mô hình & công thức huấn luyện
---

# Bài toán mô hình & công thức huấn luyện

Tài liệu này mô tả cách đặc tả bài toán, lựa chọn mô hình, hàm mất mát, chỉ số đánh giá và pipeline huấn luyện để dự báo/chẩn đoán **chỉ số chuyển đổi số (CĐS)** theo địa phương và theo thời gian.

## 1) Đặc tả bài toán

- Kiểu bài toán: Hồi quy (Regression) trên dữ liệu bảng (tabular) và/hoặc chuỗi thời gian (time series).
- Đầu vào (đặc trưng X):
  - x1: Số dịch vụ công trực tuyến (DVCTT) mức độ 3/4 theo địa phương.
  - x2: Tỷ lệ dân số dùng Internet/băng rộng cố định.
  - x3: Số lượng bộ dữ liệu mở, mức độ cập nhật (tần suất/thời gian gần nhất).
  - x4: Lượt truy cập/tải dữ liệu mở, mức độ quan tâm chủ đề.
  - x5: Các chỉ báo KT-XH liên quan (nếu có, chuẩn hóa theo đầu người).
- Đầu ra (mục tiêu y): Điểm tổng hợp CĐS (hoặc một chỉ số thành phần) theo địa phương, theo kỳ t (tháng/quý/năm).

## 2) Tiền xử lý & Chuẩn hóa dữ liệu

- Chuẩn hóa giá trị thiếu: median imputation hoặc KNN imputer.
- Chuẩn hóa thang đo: StandardScaler (z-score) hoặc MinMaxScaler nếu dùng mô hình nhạy cảm thang đo.
- Tạo đặc trưng thời gian: lag features y(t−1), y(t−2), rolling mean/var.
- One-hot cho biến phân loại (nếu có).

## 3) Lựa chọn mô hình

- Hồi quy tabular: RandomForestRegressor / XGBoostRegressor (mạnh với phi tuyến, ít yêu cầu chuẩn hóa thang đo).
- Chuỗi thời gian: ARIMA/SARIMA cho tuyến tính; Prophet cho xu hướng/mùa vụ; LSTM (roadmap) khi dữ liệu đủ dài.

## 4) Hàm mất mát & tối ưu

- Hồi quy: tối thiểu hóa sai số tuyệt đối trung bình (MAE) hoặc bình phương trung bình (MSE).

Công thức:

```
MSE = (1/N) * Σ_{i=1..N} (ŷ_i - y_i)^2
MAE = (1/N) * Σ_{i=1..N} |ŷ_i - y_i|
R2  = 1 - [Σ (y_i - ŷ_i)²] / [Σ (y_i - ȳ)²]
```

Trong đánh giá báo cáo, ưu tiên MAE (dễ diễn giải theo “điểm” chênh lệch) và bổ sung R2 để đo độ phù hợp.

## 5) Chiến lược đánh giá

- K-fold cross-validation (k=5) cho tabular khi dữ liệu không có phụ thuộc thời gian mạnh.
- TimeSeriesSplit cho chuỗi thời gian (train trên quá khứ, test trên tương lai).
- Báo cáo: MAE, RMSE, R² theo fold/split; biểu đồ residuals và actual vs. predicted.

## 6) Pipeline huấn luyện (pseudo)

```python
# 1) Load & join dữ liệu chuẩn hóa từ normalized/ hoặc MongoDB
X, y = load_features_targets()

# 2) Split / CV
from sklearn.model_selection import TimeSeriesSplit
cv = TimeSeriesSplit(n_splits=5)  # hoặc KFold

# 3) Model
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=400, max_depth=None, random_state=42)

# 4) Train & evaluate
from sklearn.metrics import mean_absolute_error, r2_score
mae_scores, r2_scores = [], []
for train_idx, test_idx in cv.split(X):
    X_tr, X_te = X.iloc[train_idx], X.iloc[test_idx]
    y_tr, y_te = y.iloc[train_idx], y.iloc[test_idx]
    model.fit(X_tr, y_tr)
    y_pred = model.predict(X_te)
    mae_scores.append(mean_absolute_error(y_te, y_pred))
    r2_scores.append(r2_score(y_te, y_pred))

print("MAE(mean)", sum(mae_scores)/len(mae_scores))
print("R2(mean)", sum(r2_scores)/len(r2_scores))

# 5) Fit toàn bộ & lưu mô hình (serving)
model.fit(X, y)
import joblib; joblib.dump(model, "model_cds_rf.joblib")
```

## 7) Lựa chọn đặc trưng (feature importance)

- Với RF/XGBoost: dùng `feature_importances_` để xếp hạng đặc trưng.
- Với ARIMA: kiểm tra ACF/PACF và độ dừng (ADF test).
- Loại bỏ đặc trưng ít đóng góp, tránh overfitting, giảm độ phức tạp.

## 8) Triển khai mô hình (serving)

- Cách 1: Tạo **FastAPI/Flask** service nhận JSON và trả dự báo (endpoint `/api/v1/ml/diagnosis`).
- Cách 2: Nhúng nội suy trong Backend Spring Boot (gọi Python qua gRPC/HTTP hoặc dùng mô hình đã chuyển ONNX – roadmap).

## 9) Khuyến nghị dữ liệu tối thiểu

- Ít nhất 24–36 kỳ quan sát theo địa phương (theo tháng) để mô hình time series ổn định.
- Đảm bảo đồng bộ hóa thời điểm các biến đầu vào (cùng kỳ).
- Mỗi đặc trưng ≥ 80% giá trị hợp lệ; nếu thiếu nhiều, áp dụng kỹ thuật suy diễn phù hợp.

## 10) Lộ trình nâng cao

- Thử nghiệm **LightGBM/CatBoost** cho tabular có tương tác phi tuyến mạnh.
- **Multitask learning**: dự báo đồng thời nhiều chỉ số CĐS thành phần.
- **Explainability**: SHAP để giải thích đóng góp đặc trưng theo từng dự báo.
