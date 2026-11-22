# Lab DVO L05 — Đối chiếu Hạ tầng dạng mã khai báo (lũy đẳng) vs mệnh lệnh

Viết hai hàm Python: `declarative_apply(cur, target=5)` (luôn đặt `replicas=5`) và `imperative_add(cur, delta=2)` chạy lặp 2 lần từ trạng thái ban đầu `3`, in đúng 3 dòng:
1. `decl_after_2_runs=5`
2. `imp_after_2_runs=7`
3. `decl_is_idempotent=1`

Chấm tự động:
```bash
bash labs/cham.sh DVO L05 duong_dan/bai_cua_ban.py
```
