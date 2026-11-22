# Lab OSY L01 (Mô phỏng tiến trình) — Đếm cây tiến trình fork()

Viết chương trình Python mô phỏng số tiến trình sinh ra sau `3` và `4` lệnh `fork()` (nhân bản tiến trình) liên tiếp (`2^k` kể cả tiến trình gốc) và đếm số không gian địa chỉ dùng chung nếu 4 luồng nằm trong cùng 1 tiến trình `pid=100`, in đúng 3 dòng:
1. `procs_fork3=8`
2. `procs_fork4=16`
3. `shared_spaces_4threads=1`

Chấm tự động:
```bash
bash labs/cham.sh OSY L01 duong_dan/bai_cua_ban.py
```
