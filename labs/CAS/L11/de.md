# Lab CAS L11 — Sự cố Năm 2038: so sánh hạn 32-bit có dấu (2038), không dấu (2106) & hợp đồng 2040

Dùng `datetime(1970, 1, 1, tzinfo=timezone.utc)` tính ngày tràn của mốc `2^31 - 1` (có dấu 32-bit) và `2^32 - 1` (không dấu 32-bit), đồng thời kiểm xem ngày đáo hạn trái phiếu `2040-06-01` có vượt ngưỡng 2038 hay không.

Định dạng đầu ra (1 dòng):
`i32_date=<YYYY-MM-DD> u32_date=<YYYY-MM-DD> bond_2040_fails=<0 hoặc 1>`

Chấm tự động:
```bash
bash labs/cham.sh CAS L11 duong_dan/bai_cua_ban.py
```
