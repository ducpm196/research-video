# Lab SWF L06 — Kiểm thử dựa trên tính chất (idempotence & bảo toàn phần tử)

Viết chương trình Python duyệt toàn bộ `3^4 = 81` dãy độ dài `4` lấy giá trị trong `{0, 1, 2}` và kiểm hai tính chất của `sorted(xs)`: `sorted(sorted(xs)) == sorted(xs)` và đếm tần suất phần tử không đổi, in đúng 3 dòng:
1. `tested_sequences=81`
2. `idempotent_pass=81`
3. `multiset_preserved=81`

Chấm tự động:
```bash
bash labs/cham.sh SWF L06 duong_dan/bai_cua_ban.py
```
