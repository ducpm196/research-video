# Lab LNX L09 — Phân tích cấu hình Compose và tính độ trễ healthcheck theo stdin

Viết kịch bản Bash đọc một dòng `<svc:port>|<cond>|<bind>|<interval>|<retries>` từ `stdin`, tách địa chỉ nội bộ, kiểm `cond == service_healthy` (`1`/`0`), và tính `max_detect_s = interval * retries`.

Chấm tự động:
```bash
bash labs/cham.sh LNX L09 duong_dan/bai_cua_ban.sh
```
