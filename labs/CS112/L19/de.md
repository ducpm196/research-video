# Lab CS112 L19 — Nhân chuỗi sáu ma trận: bảng theo đoạn, ngoặc và vét cạn

Cần: Python 3.11 trở lên. Tạo `chuoi.py` (số liệu minh hoạ, khác ví dụ trong bài). Sáu ma trận `A1 … A6`, chỉ số từ 1, `A_i` có cỡ `p[i-1] x p[i]` với `p = (7, 4, 9, 5, 8, 3, 6)`.

1. Lập bảng `m[i][j]` (số phép nhân số ít nhất cho `A_i … A_j`, `m[i][i] = 0`) điền theo độ dài đoạn tăng dần, `m[i][j] = min` qua mọi chỗ cắt `k` (`i <= k < j`) của `m[i][k] + m[k+1][j] + p[i-1] * p[k] * p[j]`. Đếm số lần tính biểu thức trong dấu `min` (mỗi cặp `(đoạn, k)` một lần).
2. Truy vết chỗ cắt tốt nhất (nhiều chỗ cắt cùng cho giá trị nhỏ nhất thì lấy `k` nhỏ nhất) rồi dựng chuỗi ngoặc: đoạn một ma trận viết `A<i>`, đoạn dài hơn viết `(` trái, một dấu cách, phải `)`.
3. Vét cạn: liệt kê mọi cách đặt ngoặc bằng đệ quy (với mỗi chỗ cắt, ghép mọi cách của nửa trái với mọi cách của nửa phải), tính số phép nhân của từng cách bằng công thức `a * b * c`, lấy số cách và giá trị nhỏ nhất.

In đúng năm dòng:

```
So phep nhan it nhat: <m[1][6]>
Dat ngoac: <chuỗi ngoặc>
So lan thu cho cat: <số lần đếm ở bước 1>
Vet can: <số cách> cach, nho nhat <giá trị>
Vet can = bang: CO
```

(dòng cuối `CO` nếu giá trị nhỏ nhất của vét cạn bằng `m[1][6]`, ngược lại `KHONG`).

Chạy: `python chuoi.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L19 chuoi.py`.
