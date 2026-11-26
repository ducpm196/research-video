# Lab CAS L09 — Heartbleed (RFC 6520): kiểm biên 1 + 2 + payload + 16 <= record_len

Đọc `stdin` `p_ok=<int> r_ok=<int> p_bad=<int> r_bad=<int>`. Kiểm tra hai gói Heartbeat theo chuẩn RFC 6520 và tính số byte đọc lố của gói lỗi.

In đúng 1 dòng: `valid_ok=<0|1> hb_ok=<0|1> hb_overread_B=<d>`.
Chấm tự động: `bash labs/cham.sh CAS L09 duong_dan/bai_cua_ban.py`
