# Lab DEN L06 — Duyệt đồ thị nhiều bước có lọc đỉnh đã thăm

Cho đồ thị có hướng `g = {'u0': ['u1', 'u2'], 'u1': ['u2', 'u3'], 'u2': ['u3', 'u4'], 'u3': ['u5'], 'u4': [], 'u5': []}`. Bắt đầu từ `'u0'`, thực hiện tìm kiếm theo chiều rộng (`BFS`) trong đúng `2` bước đi (hop <= 2) có giữ tập đã thăm để loại trùng. In danh sách đã sắp xếp các đỉnh chạm tới ở vòng 1–2 (trừ `'u0'`) và tổng số đỉnh riêng biệt tìm được.

Định dạng đầu ra (2 dòng):
`reached_sorted=<danh sách>`
`unique_count=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh DEN L06 duong_dan/bai_cua_ban.py
```
