# Lab CS115 L12 — Nhân nhiều xác suất nhỏ: tích tràn về 0, tổng lôgarit thì không

Cần: Python 3 (chỉ `import math`). Tạo tệp `xacsuat.py`. Mỗi xác suất bằng `0.2` (số minh hoạ, khác ví dụ trong bài).

1. Với `N` lần lượt là `50`, `500`, `5000`: tính tích `t` bằng vòng lặp (`t = 1.0`, rồi `t = t * 0.2` đúng `N` lần) và tổng lôgarit `s = N * math.log(0.2)`. In `N=<N> tich=<t> tong ln=<s>`, trong đó `<t>` in bằng `f"{t:.3e}"` nếu `t > 0`, ngược lại in `0.0`, và `<s>` làm tròn 2 chữ số thập phân bằng `round(s, 2)`.
2. Đổi tổng lôgarit của `N = 50` ngược lại bằng hàm mũ: in `e mu tong ln (N=50): <math.exp(s)>` với định dạng `:.3e`.
3. In `ln2 + ln3 = <a>, ln6 = <b>` với `a = math.log(2) + math.log(3)`, `b = math.log(6)`, mỗi số làm tròn 4 chữ số.
4. Kiểm đạo hàm của `ln(x^2 + 1)` tại `x = 1` bằng bước nhỏ `(f(x + h) - f(x - h)) / (2*h)` với `h = 0.0001`, làm tròn 4 chữ số; in `dao ham ln(x^2+1) tai 1: <số>`.

Chạy: `python xacsuat.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L12 xacsuat.py`.
