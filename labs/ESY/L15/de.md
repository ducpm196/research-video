# Lab ESY L15 — Mô phỏng vượt ngân sách chu kỳ do đảo ngược ưu tiên

Cho hệ chạy chu kỳ `10 Hz` (`100 ms`). Bình thường 3 tác vụ tốn `[25, 5, 30]` ms; khi bị đảo ngược ưu tiên bởi tác vụ trung bình `45 ms`, tổng trễ thành `[25, 45, 5, 30]`. Kiểm tra tình trạng vượt hạn trước và sau.
In đúng 1 dòng `period_ms=... normal_ms=... inverted_ms=... overload=0/1`.

Chấm tự động:
```bash
bash labs/cham.sh ESY L15 duong_dan/bai_cua_ban.py
```
