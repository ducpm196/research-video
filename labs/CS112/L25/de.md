# Lab CS112 L25 — Cây khung nhỏ nhất: hai thuật toán, hợp–tìm và vét cạn

Cần: Python 3.11 trở lên. Tạo `cay_khung.py` (số liệu minh hoạ, khác ví dụ trong bài). Đồ thị VÔ HƯỚNG, sáu đỉnh `A…F`, mười cạnh (mọi trọng số khác nhau):

`A-B 4, A-C 7, B-C 2, B-D 9, C-D 5, C-E 8, D-E 3, D-F 6, E-F 10, A-F 11`

1. **Xét cạnh từ nhẹ đến nặng**: sắp cạnh theo trọng số tăng dần; dùng cấu trúc hợp–tìm (`find` có nén đường đi, `union` gắn gốc nhóm nhỏ hơn vào gốc nhóm lớn hơn) để chỉ lấy cạnh nối hai nhóm khác nhau. In `Kruskal: ` các cạnh đã lấy theo thứ tự lấy, mỗi cạnh dạng `X-Y(w)` (`X` đứng trước `Y` theo thứ tự chữ cái), cách nhau một dấu cách, rồi `, tong <tổng>`.
2. **Mở rộng cây từ A**: mỗi bước thêm cạnh nhẹ nhất có đúng một đầu trong cây (không cần đống: duyệt hết các cạnh). In `Prim tu A: ` các cạnh theo thứ tự thêm (cùng dạng) rồi `, tong <tổng>`.
3. **Vét cạn**: duyệt mọi bộ `n - 1 = 5` trong 10 cạnh (`itertools.combinations`), giữ bộ nối được cả sáu đỉnh (kiểm bằng hợp–tìm: không cạnh nào nối hai đỉnh đã cùng nhóm). In `Vet can: <số cây khung> cay khung, nho nhat <tổng>`.
4. In `Cung tong: CO` nếu ba tổng bằng nhau, ngược lại `KHONG`.

Gợi ý hợp–tìm (nếu chưa gặp): giữ hai danh sách `cha` (cha của mỗi đỉnh, ban đầu mỗi đỉnh là cha của chính nó) và `size` (số đỉnh của nhóm, ban đầu 1 ở mỗi gốc); `find(x)` đi theo `cha` tới gốc (gán lại `cha` của các đỉnh trên đường về gốc để nén đường đi); `union(a, b)` tìm hai gốc, nếu khác nhau thì gắn gốc có `size` nhỏ hơn vào gốc kia rồi cộng `size`, và trả về `True`; nếu cùng gốc trả về `False`. Đừng dùng `all(union(...) for ...)` để lặp: `all` dừng ngay ở phần tử `False` đầu tiên, nên các phép gắn sau không chạy.

Chạy: `python cay_khung.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L25 cay_khung.py`.
