# Lab CS112 L20 — Dãy con tăng dài nhất và xâu con chung dài nhất

Cần: Python 3.11 trở lên. Tạo `lis_lcs.py` (số liệu minh hoạ, khác ví dụ trong bài).

**Phần 1 — dãy con tăng dài nhất (tăng hẳn)**: `a = [9, 4, 7, 2, 8, 11, 3, 10, 5, 12]`.
1. Lập bảng `L[i]` (độ dài dãy con tăng hẳn dài nhất kết thúc tại `a[i]`, `L[i] = 1 + max(L[j])` qua mọi `j < i` với `a[j] < a[i]`, không có `j` thì `1`). Đếm số lần so sánh `a[j] < a[i]` (mỗi cặp `j < i` một lần).
2. Truy vết một dãy: bắt đầu ở chỉ số `i` NHỎ NHẤT đạt `max(L)`; rồi lùi: chọn `j < i` NHỎ NHẤT có `a[j] < a[i]` và `L[j] == L[i] - 1`; lặp tới khi `L == 1`; in dãy đọc xuôi.
3. Vét cạn: thử mọi tập con KHÁC RỖNG của các chỉ số, tức kích thước `r` từ 1 tới `n` (`itertools.combinations(range(n), r)`; không đếm tập rỗng), lấy độ dài lớn nhất của một dãy con tăng hẳn; số tập con đã thử là `2**n - 1`.

**Phần 2 — xâu con chung dài nhất**: `X = "THUATTOAN"`, `Y = "TOANTHUAT"`. Lập bảng `c` kích thước `(len(X)+1) x (len(Y)+1)`; truy vết từ ô cuối: hai ký tự bằng nhau thì lấy và đi chéo; khác nhau thì đi lên nếu `c[i-1][j] >= c[i][j-1]`, ngược lại sang trái.

In đúng năm dòng:

```
L: <10 số của bảng L, cách nhau một dấu cách>
LIS: <độ dài> qua <dãy, cách nhau dấu cách>; so sanh bang: <số lần so sánh>
Vet can LIS: <độ dài lớn nhất> (<số tập con đã thử> tap con)
LCS: <độ dài> qua <xâu chung>
Bang = vet can: CO
```

(dòng cuối `CO` nếu độ dài LIS của bảng bằng của vét cạn, ngược lại `KHONG`).

Cú pháp cần dùng (nếu chưa gặp): "tập con" là chọn một số phần tử của dãy (có thể không chọn gì, hoặc chọn hết). `from itertools import combinations` rồi `list(combinations(range(3), 2))` ra `[(0, 1), (0, 2), (1, 2)]`: mọi cách chọn 2 chỉ số trong 0, 1, 2, theo thứ tự tăng.

Chạy: `python lis_lcs.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L20 lis_lcs.py`.
