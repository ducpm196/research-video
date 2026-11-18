# Lab CS112 L15 — Cận dưới của bốn thành phố và chu trình tối ưu

Cần: Python 3.11 trở lên (không cần thư viện ngoài). Tạo `tsp4.py` (số liệu minh hoạ, khác ví dụ trong bài). Ma trận chi phí 4 thành phố, hàng i cột j là chi phí đi từ i tới j (thành phố đánh số từ 0 trong mã), đường chéo là vô cùng:

```
INF  3 11 13
14 INF 14  7
15  6 INF  2
 8  3  5 INF
```

Viết chương trình: đặt `INF = float("inf")`, khai ma trận bằng danh sách lồng nhau, rồi

1. tìm số nhỏ nhất của mỗi hàng, trừ đi; trên ma trận MỚI tìm số nhỏ nhất của mỗi cột (không phải trên ma trận gốc);
2. in `min hang: [...]`, `min cot: [...]` (hai danh sách số nguyên) và `LB goc: <tổng hai loại rút gọn>`;
3. vét cạn mọi thứ tự ghé ba thành phố còn lại, chỉ số 1, 2, 3 trong mã (dùng `itertools.permutations`) rồi in `Toi uu: <chi phí> qua <thứ tự thành phố đánh số từ 1, bắt đầu và kết thúc ở 1>`, ví dụ `qua 1 3 2 4 1`;
4. in `LB <= toi uu: CO` nếu cận dưới không vượt chi phí tối ưu, ngược lại `KHONG`;
5. tính cận dưới của hai nút con của gốc: nút "đi từ thành phố 1 tới thành phố j" (chỉ số `0` tới `j - 1`): lấy `R` là ma trận đã rút gọn (hàng rồi cột) ở bước 1, gán `INF` cho cả hàng `0`, cả cột `j - 1` và ô `C[j - 1][0]`, rút gọn lại (hàng rồi cột, bỏ qua hàng hay cột chỉ toàn `INF`), cận con = cận gốc + `R[0][j - 1]` + lượng rút gọn mới. In `Nut con 1->2: <cận>` và `Nut con 1->3: <cận>`.

Chạy: `python tsp4.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L15 tsp4.py`.
