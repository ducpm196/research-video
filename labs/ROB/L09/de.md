# Lab ROB L09 — Mô phỏng lăn mẫu quỹ đạo và chấm điểm cửa sổ động DWA

Cho ba cặp vận tốc `(v, w)` ứng viên: `(0.6, 0.0)`, `(0.4, 0.5)`, `(0.2, -0.6)` lăn `dt = 1.0 s` từ gốc theo quy tắc `x, y, th = v*cos(w), v*sin(w), w`, hướng về đích `(2.0, 0.5)` và né vật cản `(1.2, 0.0)`. Tính điểm từng ứng viên gồm: căn hướng `head = max(0, 1 - |atan2(0.5 - y, 2.0 - x) - th| / pi)`, độ thoáng vật cản `clr = min(1.0, hypot(x - 1.2, y))`, tốc độ chuẩn hoá `v / 0.6`, tổng hợp `tot = round(0.4*head + 0.4*clr + 0.2*(v/0.6), 3)` và chọn cặp `(tot, (v, w))` lớn nhất.
In đúng 1 dòng `scores=[...] best=(score, (v, w))`.

Chấm tự động:
```bash
bash labs/cham.sh ROB L09 duong_dan/bai_cua_ban.py
```
