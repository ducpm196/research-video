# Lab SDP L16 — Thiết kế lại giỏ hàng bằng Strategy

Đọc `stdin` `items=<int,...> thr=<int> pct=<float> flat=<int>`. Tính tổng giỏ hàng `subtotal = sum(items)`; chiến lược phần trăm trả `round(subtotal * (1.0 - pct))` nếu `subtotal > thr` (ngược lại giữ nguyên); chiến lược trừ thẳng trả `max(0, subtotal - flat)`.

In đúng 3 dòng: `subtotal=<d>`, `pct10_total=<d>`, `flat50_total=<d>`.
Chấm tự động: `bash labs/cham.sh SDP L16 duong_dan/bai_cua_ban.py`
