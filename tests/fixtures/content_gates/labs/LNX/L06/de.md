# Lab LNX L06 — Bảo mật biến môi trường và tính tần suất cron

Viết kịch bản Bash tạo tệp bí mật với `chmod 600` (hoặc kiểm tra `umask`), đọc nạp biến môi trường không in nguyên văn bí mật, và tính số lượt chạy/ngày của `*/5 * * * *` để in đúng 3 dòng:
1. `env_loaded=1`
2. `cron_per_hour=12`
3. `cron_per_day=288`

Chấm tự động:
```bash
bash labs/cham.sh LNX L06 duong_dan/bai_cua_ban.sh
```
