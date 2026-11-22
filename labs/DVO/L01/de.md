# Lab DVO L01 (Mô phỏng nhánh & CI) — Tính xác suất xung đột hợp nhất

Viết chương trình Python tính xác suất ít nhất 1 trong `k = 40` thay đổi ngẫu nhiên chạm vào tập `5` trên `100` tệp theo công thức `1 - (1 - 5/100)^40`, so với nhánh nhỏ `5` thay đổi xen vào, in đúng 3 dòng:
1. `p_conflict_40=87.1%`
2. `p_conflict_5=22.6%`
3. `shorter_branch_safer=1`

Chấm tự động:
```bash
bash labs/cham.sh DVO L01 duong_dan/bai_cua_ban.py
```
