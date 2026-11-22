# Lab SEP L07 — Tính hạn công bố lỗ hổng theo lịch thật (năm nhuận 2024): hạn 90 ngày, sau vá +30 ngày (khi v<=90), và hạn 7 ngày

Dùng `datetime.date` bắt đầu từ ngày `2024-02-01` (năm nhuận 2024 có 29/02): tính hạn chuẩn 90 ngày, ngày công bố sau khi vá sớm ở ngày `v = 45` (`v <= 90`, công bố ở `min(90, v + 30)` ngày sau ngày báo), và hạn khẩn `7` ngày nếu lỗi đang bị khai thác.

Định dạng đầu ra (1 dòng):
`d90=<YYYY-MM-DD> d_patched=<YYYY-MM-DD> exploit_7d=<YYYY-MM-DD>`

Chấm tự động:
```bash
bash labs/cham.sh SEP L07 duong_dan/bai_cua_ban.py
```
