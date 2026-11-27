# Lab CAS L11 — Sự cố Năm 2038: 32-bit có dấu vs không dấu & ngày đáo hạn

Đọc `stdin` `epoch_year=<int> bond_date=<YYYY-MM-DD>`. Dùng mô đun `datetime` (giờ UTC): từ mốc `t0 = datetime(epoch_year, 1, 1, tzinfo=timezone.utc)`, cộng `timedelta(seconds=2**31 - 1)` để lấy ngày tràn 32-bit có dấu `i32_date`, cộng `timedelta(seconds=2**32 - 1)` để lấy ngày tràn không dấu `u32_date`, và kiểm tra `date.fromisoformat(bond_date) > i32_date`.

In đúng 1 dòng: `i32_date=<YYYY-MM-DD> u32_date=<YYYY-MM-DD> bond_2040_fails=<0|1>`.
Gợi ý Python: `import sys; kv = dict(t.split('=') for t in sys.stdin.read().split())`; dùng `from datetime import date, datetime, timedelta, timezone`.
Chấm tự động: `bash labs/cham.sh CAS L11 duong_dan/bai_cua_ban.py`
