# Lab GFX L04 — Tính toạ độ trọng tâm tam giác trực tiếp từ ba hàm cạnh có hướng

Cho tam giác có ba đỉnh `A = (0, 0), B = (6, 0), C = (0, 6)` và điểm thử `P = (1, 2)`. Viết hàm cạnh có hướng `edge(P, U, V) = (P_x - U_x)*(V_y - U_y) - (P_y - U_y)*(V_x - U_x)`, tính diện tích kép toàn tam giác `edge(C, A, B)` và chia để ra bộ ba trọng tâm `(l0, l1, l2)`.
In đúng 1 dòng `bary=(l0, l1, l2) inside=0/1` (2 chữ số).

Chấm tự động:
```bash
bash labs/cham.sh GFX L04 duong_dan/bai_cua_ban.py
```
