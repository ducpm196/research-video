# Lab RBM L15 — Tìm đường ngắn nhất A* trên lưới 4×5 có chướng ngại vật

Cho lưới kích thước `4 hàng × 5 cột` (`0 <= r < 4, 0 <= c < 5`), danh sách tường `{(0, 2), (1, 2), (2, 2)}`, điểm xuất phát `(1, 0)` và đích `(1, 4)` (chỉ đi 4 hướng kề). Chạy thuật toán `A*` với hàm ước lượng Manhattan `|r - r_goal| + |c - c_goal|` và in giá trị `h` tại gốc cùng độ dài đường đi ngắn nhất.
In đúng 1 dòng `astar_steps=... h_start=...`.

Chấm tự động:
```bash
bash labs/cham.sh RBM L15 duong_dan/bai_cua_ban.py
```
