# Lab CS112 L23 — Sắp xếp nhanh: đếm so sánh, ca tệ nhất, cận dưới và sắp xếp đếm

Cần: Python 3.11 trở lên. Tạo `nhanh.py` (số liệu minh hoạ, khác ví dụ trong bài).

1. Viết `phan_hoach(a, lo, hi)` đúng như bài (chốt `p = a[hi]`, `i = lo - 1`, duyệt `j` từ `lo` tới `hi - 1`, nếu `a[j] <= p` thì tăng `i` và đổi chỗ `a[i]`, `a[j]`; cuối cùng đổi `a[i+1]` với `a[hi]`, trả về `i + 1`) và `sap_nhanh(a, lo, hi)` gọi đệ quy hai bên chốt (không gọi cho đoạn có `lo >= hi`). Dùng hai biến đếm: số phép so sánh `a[j] <= p`, và độ sâu đệ quy lớn nhất (lời gọi ngoài cùng tính là tầng 1; chỉ đếm lời gọi có `lo < hi`).
2. Với `a = [7, 3, 9, 1, 8, 2, 6, 4]`: phân hoạch một lần trên bản sao, in mảng sau đó, vị trí chốt và số so sánh; rồi sắp xếp nhanh toàn bộ một bản sao khác, in tổng số so sánh và độ sâu.
3. Với mảng đã sắp `[1, 2, 3, 4, 5, 6, 7, 8]`: in tổng số so sánh và độ sâu.
4. In cận dưới `ceil(log2(n!))` của số so sánh tệ nhất cho `n = 8` (dùng `math.factorial` và `math.ceil(math.log2(...))`).
5. Sắp xếp đếm cho `b = [2, 0, 3, 2, 1, 0, 2, 3, 1]` với khoá `0..3`: đếm số lần, ghi ra mảng đã sắp, in mảng.

In đúng năm dòng:

```
Phan hoach: <mảng sau phân hoạch>, chot o vi tri <q>, <số so sánh> so sanh
Sap nhanh: tong <số> so sanh, do sau <số>
Da sap: tong <số> so sanh, do sau <số>
Can duoi n = 8: <số>
Sap xep dem: <mảng đã sắp>
```

Cú pháp cần dùng (nếu chưa gặp): một biến đếm dùng chung cho mọi lời gọi đệ quy. Cách một: đặt `dem = [0]` ngoài hàm, trong hàm viết `dem[0] += 1`. Cách hai: đặt `so_sanh = 0` ngoài hàm, rồi dòng đầu của hàm viết `global so_sanh` (cho phép hàm sửa biến bên ngoài), sau đó `so_sanh += 1`. Nếu thiếu dòng `global`, Python báo lỗi vì cho rằng `so_sanh` là biến mới của hàm. Hàm vắng dòng `return` trả về `None`.

Chạy: `python nhanh.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L23 nhanh.py`.
