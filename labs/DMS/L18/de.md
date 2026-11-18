# Lab DMS L18 — Công thức Euler, giới hạn 3V − 6 và tô màu tham lam bằng chương trình

Viết `phang.py` (Python 3.11 trở lên); chạy: `python phang.py`.

In đúng tám dòng (không dấu):
1–3. Với đồ thị phẳng liên thông có `(V, E)` = `(10, 15)`, `(7, 6)`, `(12, 30)`: in `V=<V> E=<E>: F=<số mặt>` với `F = 2 - V + E` (công thức Euler `V - E + F = 2`).
4–6. Với đồ thị đơn mà ta chỉ biết số đỉnh `V` và số cạnh `E` (không có danh sách cạnh) với `(V, E)` = `(7, 19)`, `(8, 18)`, `(6, 9)`: in `V=<V> E=<E>: khong phang` nếu `E > 3*V - 6`, ngược lại `V=<V> E=<E>: chua ket luan` (bất đẳng thức đúng thì chưa đủ để kết luận phẳng; ví dụ `(6, 9)` là bài toán ba nhà ba nguồn, không phẳng).
7. Đồ thị "vương miện" 4 cặp (8 đỉnh): đỉnh `('a', i)` và `('b', i)` với `i` từ 0 đến 3; `('a', i)` kề `('b', j)` khi `i != j`. Tô màu tham lam (đi lần lượt từng đỉnh, tô màu nhỏ nhất, bắt đầu từ 0, chưa bị đỉnh kề đã tô dùng), theo hai thứ tự: xen kẽ `a0, b0, a1, b1, ...` và `a0, a1, a2, a3, b0, b1, b2, b3`. In `do thi 4 cap (8 dinh): xen ke <số màu> mau, a truoc b sau <số màu> mau` (số màu = màu lớn nhất đã dùng cộng 1).
8. Chu trình 5 đỉnh (đỉnh i kề đỉnh (i+1) mod 5), tô tham lam theo thứ tự 0, 1, 2, 3, 4: in `chu trinh 5 dinh: tham lam <số màu> mau, can tren <bậc lớn nhất + 1>`.

Hai đỉnh gọi là kề nhau khi có một cạnh nối chúng.

Gợi ý cú pháp cho dòng 7–8 (có thể viết bằng vòng lặp thường nếu quen hơn):
- Tập màu của các đỉnh kề đã tô: `{mau[u] for u in ke[v] if u in mau}` nghĩa là: với mỗi đỉnh `u` kề `v` mà đã có trong từ điển `mau`, lấy màu `mau[u]`, gom thành một tập. Tương đương: `da_dung = set()`, `for u in ke[v]:`, `if u in mau:`, `da_dung.add(mau[u])`.
- Màu nhỏ nhất chưa dùng: `c = 0`, rồi `while c in da_dung: c = c + 1`.
- Danh sách đỉnh `[('a', i) for i in range(n)]` lập các cặp `('a', 0)`, `('a', 1)`, ... ; từ điển kề `{v: [u for u in dinh if u[0] != v[0] and u[1] != v[1]] for v in dinh}` ghi, với mỗi đỉnh `v`, danh sách các đỉnh khác hàng và khác chỉ số.

Chấm: `bash labs/cham.sh DMS L18 phang.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
