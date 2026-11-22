# Lab LNX L09 — Tính ngưỡng healthcheck và chẩn đoán cấu hình Compose

Viết kịch bản Bash kiểm tra cấu hình dịch vụ hợp lệ (nghe `0.0.0.0`, dùng cổng nội bộ `6379`, chờ `service_healthy`) và tính độ trễ tối đa `interval=2, retries=5` để in đúng 3 dòng:
1. `internal_addr=cache:6379`
2. `wait_healthy=1`
3. `max_detect_s=10`

Chấm tự động:
```bash
bash labs/cham.sh LNX L09 duong_dan/bai_cua_ban.sh
```
