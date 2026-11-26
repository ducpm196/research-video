# Lab LNX L06 — Bảo mật tệp .env chmod 600 và tính tần suất cron theo stdin

Viết kịch bản Bash đọc `<key_name> <key_val> <cron_step_min>` từ `stdin`, tạo tệp bí mật trong thư mục tạm với `chmod 600`, nạp bằng `source` (không in bí mật thô ra stdout), kiểm độ dài > 0 (`env_loaded`) và tính `cron_per_hour = 60 / step`, `cron_per_day = cron_per_hour * 24`.

Chấm tự động:
```bash
bash labs/cham.sh LNX L06 duong_dan/bai_cua_ban.sh
```
