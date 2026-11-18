# Lab CS112 L24 — Dijkstra, Bellman–Ford và chu trình âm

Cần: Python 3.11 trở lên. Tạo `ngan_nhat.py` (số liệu minh hoạ, khác ví dụ trong bài). Đồ thị có hướng, mỗi cạnh là `(u, v, w)` (từ `u` tới `v`, trọng số `w`).

**Đồ thị 1** (mọi `w >= 0`), đỉnh xuất phát `S`:
`(S, A, 7), (S, B, 2), (B, A, 3), (A, C, 1), (B, C, 8), (C, D, 2), (B, D, 9)`

1. Viết Dijkstra: chốt đỉnh chưa chốt có `d` nhỏ nhất (hoà thì theo thứ tự tên `S, A, B, C, D`), nới các cạnh đi ra. In `Chot: ` và thứ tự chốt, `d: ` và `d` của `S, A, B, C, D` (dạng `S=0 A=5 …`), `Duong toi D: ` đường từ `S` tới `D` (lần ngược theo cạnh đã làm `d` giảm lần cuối) kèm ` = ` độ dài.

**Đồ thị 2** (có cạnh âm), đỉnh xuất phát `S`, các cạnh theo đúng thứ tự này:
`(A, C, 2), (B, A, -2), (S, A, 2), (S, B, 3)`

2. Chạy Dijkstra (như bước 1) và Bellman–Ford (lặp tối đa `n - 1 = 3` vòng, mỗi vòng nới mọi cạnh theo thứ tự trên, dừng khi một vòng không đổi gì). In `Canh am: Dijkstra d[A] = <số>, Bellman-Ford d[A] = <số>, so vong co doi: <số vòng có ít nhất một cạnh nới được>`.

**Đồ thị 3**: `(S, A, 1), (A, B, 1), (B, A, -3)`.

3. Chạy Bellman–Ford `n - 1` vòng rồi thêm một vòng kiểm: còn cạnh nới được thì in `Chu trinh am: CO`, ngược lại `Chu trinh am: KHONG`.

Phải in đúng năm dòng theo mẫu:

```
Chot: ...
d: ...
Duong toi D: ... = ...
Canh am: Dijkstra d[A] = ..., Bellman-Ford d[A] = ..., so vong co doi: ...
Chu trinh am: ...
```

Cú pháp cần dùng (nếu chưa gặp): `min(con, key=lambda v: (d[v], dinh.index(v)))` lấy đỉnh `v` trong `con` có cặp `(d[v], vị trí của v trong danh sách dinh)` nhỏ nhất, tức `d` nhỏ nhất, hoà thì đỉnh đứng trước trong `dinh`; `dinh.index("B")` là vị trí của `"B"` trong danh sách `dinh`. Để lần ngược đường đi, ghi `cha[v] = u` mỗi khi `d[v]` giảm, rồi từ `D` lấy `cha` liên tiếp tới `S`. Vô cùng: `float("inf")`.

Chạy: `python ngan_nhat.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L24 ngan_nhat.py`.
