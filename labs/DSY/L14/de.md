# Lab DSY L14 [Mô phỏng phân tán] — Hộp thư nhận khử trùng lặp idempotent

Viết chương trình Python xử lý luồng sự kiện có bản tin gửi trùng `[('#41', 100), ('#42', 50), ('#42', 50), ('#43', 25)]`: lưu tập `seen_ids` cùng lúc cộng số dư để bảo đảm tổng chuẩn `175`, in đúng 3 dòng:
1. `raw_events=4`
2. `unique_applied=3`
3. `final_balance=175`

Chấm tự động:
```bash
bash labs/cham.sh DSY L14 duong_dan/bai_cua_ban.py
```
