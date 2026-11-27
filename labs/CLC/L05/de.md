# Lab CLC L05 — Tính điểm hoà vốn gói trả theo giờ và đặt trước

Đọc `stdin` `hourly=<float> reserved=<float>`. Tính số giờ hòa vốn, phần trăm trên cả năm (`8760` giờ) và số USD tiết kiệm khi chạy đủ năm.

In 3 dòng: `breakeven_hours=<d>`, `breakeven_pct_year=<.1f>%`, `full_year_saved_usd=<d>`.
Chấm tự động: `bash labs/cham.sh CLC L05 duong_dan/bai_cua_ban.py`
Gợi ý Python: `import sys; kv = dict(t.split('=') for t in sys.stdin.read().split())`; ép `float(...)`, dùng `round(reserved / hourly)`, `round(8760 * hourly - reserved)` và `f"{pct:.1f}%"`.
