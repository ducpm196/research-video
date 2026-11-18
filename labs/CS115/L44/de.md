# Lab CS115 L44 — Khoảng tin cậy cho tỉ lệ đúng và so sánh ghép cặp

Cần: Python 3 (chỉ `import math`). Tạo tệp `tincay.py` (số minh hoạ, khác ví dụ trong bài). Dùng `1.96` cho mức 95%. Làm tròn mọi số thực 4 chữ số thập phân bằng `round(..., 4)`.

1. Một mô hình đúng `420` trên `500` mẫu. Mỗi mẫu là một số 0 hoặc 1 (Bernoulli): `p = 420/500`, độ lệch chuẩn `sqrt(p * (1 - p))`, sai số chuẩn `độ lệch chuẩn / sqrt(500)`. In `khoang tin cay 95% cho ti le dung 420/500: [<cận dưới>, <cận trên>]` với `p ∓ 1.96 * sai số chuẩn`.
2. So sánh hai mô hình A và B trên cùng `200` mẫu: cả hai cùng đúng `140`, chỉ A đúng `10`, chỉ B đúng `20`, cả hai sai `30`. Hiệu mỗi mẫu `d = đúng_B - đúng_A` là `+1` trên 20 mẫu, `-1` trên 10 mẫu, `0` trên 170 mẫu. In `cot ghep cap: B hon A tren 20 mau, A hon B tren 10 mau`.
3. In `trung binh hieu: <mean d>`; `sai so chuan cua hieu: <sqrt(mean(d^2) - mean(d)^2) / sqrt(200)>`; `khoang tin cay 95% cua hieu: [<dưới>, <trên>]`; rồi `chua du bang chung: True` nếu khoảng chứa số 0.
4. Cỡ mẫu cần để nửa độ rộng khoảng tin cậy của một tỉ lệ `p = 0.9` bằng `0.01`: `n = 1.96**2 * p * (1 - p) / 0.01**2`, làm tròn LÊN (`math.ceil`). In `mau can cho nua do rong 0.01 (p=0.9): <n>`.

Chạy: `python tincay.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L44 tincay.py`.
