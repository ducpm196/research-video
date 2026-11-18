# Lab CS115 L21 — Ma trận nhầm lẫn và các chỉ số

Cần: Python 3 (không cần thư viện ngoài), `from fractions import Fraction`. Tạo tệp `danhgia.py`. Hai danh sách (1 = có, 0 = không; số minh hoạ, khác ví dụ trong bài):

```python
that = [1] * 5 + [0] * 15
doan = [1, 1, 1, 1, 0] + [1, 1, 1] + [0] * 12
```

1. Đếm bốn ô: `TP` (thật 1, đoán 1), `FP` (thật 0, đoán 1), `FN` (thật 1, đoán 0), `TN` (thật 0, đoán 0). In `TP=<a> FP=<b> FN=<c> TN=<d>`.
2. Dùng `Fraction`: `ti le dung` = (TP + TN) chia tổng; `do chuan xac` = TP chia (TP + FP); `do phu` = TP chia (TP + FN); `F1` = trung bình điều hoà `2 * P * R / (P + R)`. In bốn dòng `ti le dung: <phân số>`, `do chuan xac: <phân số>`, `do phu: <phân số>`, `F1: <phân số>`.
3. Mô hình lười luôn đoán 0: in `mo hinh luoi (luon bao 0): ti le dung <phân số>, do phu <phân số>`.
4. In `trung binh cong cua hai chi so: <phân số>` (trung bình cộng của độ chuẩn xác và độ phủ) để thấy F1 nhỏ hơn.

Chạy: `python danhgia.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L21 danhgia.py`.
