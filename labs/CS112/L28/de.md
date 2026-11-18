# Lab CS112 L28 — Tổng ôn: kiểm ba hệ thức truy hồi bằng tỉ số, và một bẫy tham lam

Cần: Python 3.11 trở lên. Tạo `tong_on.py` (số liệu minh hoạ, khác ví dụ trong bài).

**Phần 1 — hệ thức truy hồi**: với `n = 2**k`, `T(1) = 1`, ba hệ thức

- `A`: `T(n) = 3*T(n/2) + n`
- `B`: `T(n) = 2*T(n/2) + n*n`
- `C`: `T(n) = T(n/2) + 1`

Viết hàm tính `T(n)` đệ quy có nhớ (từ điển) cho từng hệ thức. Dùng định lý thợ trên giấy để chọn hàm chuẩn `g(n)` cho mỗi hệ thức (lũy thừa của `n`, hoặc `log2(n)`), rồi in, cho `n = 1024` và `n = 1048576`, giá trị `T(n)` và tỉ số `T(n) / g(n)` làm tròn 3 chữ số thập phân. Nếu chọn `g` đúng bậc, hai tỉ số ở hai cỡ gần nhau.

**Phần 2 — bẫy tham lam**: mệnh giá `1, 6, 10`, đổi `12`: in số đồng của tham lam (đồng lớn nhất còn vừa, lặp lại) và của quy hoạch động.

In đúng bốn dòng:

```
A: T(1024) = <số>, T(1048576) = <số>, ti so: <số>, <số>
B: T(1024) = <số>, T(1048576) = <số>, ti so: <số>, <số>
C: T(1024) = <số>, T(1048576) = <số>, ti so: <số>, <số>
Doi 12 voi 1, 6, 10: tham lam <số> dong, quy hoach dong <số> dong
```

Chạy: `python tong_on.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L28 tong_on.py`.
