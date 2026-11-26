# Lab IRS L05 — Học xếp hạng: mất mát theo cặp & độ giảm DCG

Đọc từ đầu vào chuẩn (`stdin`, dạng `khoá=giá_trị`) `sa=<f> sb=<f> rels=<r0,r1,r2,r3>` (với `<f>` là số thực). Tính mất mát thuận và đảo `ln(1 + exp(-(si - sj)))` cho cặp `(sa, sb)` và độ giảm DCG khi tráo cặp `(0,1)` vs `(2,3)`.

In 2 dòng đúng nhãn (`<.3f>` làm tròn 3 chữ số thập phân): `loss_ok=<.3f> loss_swap=<.3f>`, `dcg_drop_12=<.3f> dcg_drop_34=<.3f>`.
Chấm tự động: `bash labs/cham.sh IRS L05 duong_dan/bai_cua_ban.py`
