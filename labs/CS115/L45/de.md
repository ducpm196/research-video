# Lab CS115 L45 — Một bước Adam và phạt L2 đi qua phép chia

Cần: Python 3 (chỉ `import math`). Tạo tệp `adam.py`. Số minh hoạ: `eta = 0.001`, `beta1 = 0.9`, `beta2 = 0.999`, độ mạnh phạt `lam = 0.0001`, hai trọng số A và B cùng bằng `1.0`. Gradient của hàm mất mát tại A luôn là `10.0`, tại B luôn là `0.1` (không đổi qua các bước). Không dùng `eps` (bỏ số hạng 1e-8 cho gọn).

1. Chạy Adam đúng 3 bước (`k = 1, 2, 3`) cho từng trọng số, bắt đầu với `m = 0` và `s = 0`. Mỗi bước:
   - `m = beta1 * m + (1 - beta1) * g`, `s = beta2 * s + (1 - beta2) * g * g`
   - hiệu chỉnh độ lệch: `m_hc = m / (1 - beta1 ** k)`, `s_hc = s / (1 - beta2 ** k)`
   - độ dài bước: `eta * m_hc / math.sqrt(s_hc)`, làm tròn bằng `round(..., 6)`.

   In `buoc Adam A (g=10): [<b1>, <b2>, <b3>]` rồi `buoc Adam B (g=0.1): [<b1>, <b2>, <b3>]` (danh sách in đúng như `print` của Python).
2. In `can s A: <số>` và `can s B: <số>`: căn của `s_hc` sau bước 3, làm tròn 4 chữ số thập phân bằng `round(..., 4)`.
3. Phạt L2 đi qua phép chia của Adam: số hạng phạt `lam * w` bị chia cho căn của `s_hc`, rồi nhân `eta`. Suy giảm tách rời thì trừ thẳng `eta * lam * w`, không chia. Với `w = 1.0` của từng trọng số, in bốn dòng `phat L2 keo ve 0 A: <số>`, `phat L2 keo ve 0 B: <số>`, `tach roi keo ve 0 A: <số>`, `tach roi keo ve 0 B: <số>`. Mỗi số in bằng `f"{x:.1e}"` (dạng khoa học một chữ số thập phân, ví dụ `1.0e-08`).
4. In `ti so B chia A, phat L2: <số>` và `ti so B chia A, tach roi: <số>` (số của B chia số của A, làm tròn 2 chữ số thập phân bằng `round(..., 2)`).

Chạy: `python adam.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L45 adam.py`.
