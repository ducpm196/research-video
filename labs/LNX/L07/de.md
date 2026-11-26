# Lab LNX L07 — Tính tầng ảnh dùng chung và nhận diện mã thoát OOMKill theo stdin

Viết kịch bản Bash đọc 4 số nguyên `<base_mb> <n_containers> <rw_mb> <sig>` từ `stdin`, tính tổng dung lượng dùng chung `shared_mb = base + n * rw`, dung lượng tiết kiệm `saved_mb = n * base - shared_mb` và mã thoát tín hiệu `oom_exit = 128 + sig`.

Chấm tự động:
```bash
bash labs/cham.sh LNX L07 duong_dan/bai_cua_ban.sh
```
