# Lab DSY L06 — Băm modulo vs Băm nhất quán khi mở rộng cụm

Đọc `stdin` `keys=<int> n_old=<int> n_new=<int>` (xét các khoá `k` từ `0` tới `keys - 1`, tên chuỗi `f"k{k}"`). Tính tỉ lệ khoá dịch chuyển với phép chia dư `k % n` và với băm nhất quán SHA-256 dùng 100 nút ảo mỗi nút (`i` từ `0` tới `n - 1`, `v` từ `0` tới `99`, tên nút ảo `f"n{i}#{v}"`). Hàm băm 32-bit dùng thư viện chuẩn: `h32 = lambda s: int(hashlib.sha256(s.encode()).hexdigest()[:8], 16)`; tìm nút kế tiếp theo chiều kim đồng hồ bằng `bisect.bisect(ring, (h32(f"k{k}"), 99)) % len(ring)`.

In đúng 3 dòng: `mod_moved_pct=<.1f>%`, `ch_moved_lt_30pct=<0|1>`, `ideal_moved_pct=<.1f>%`.
Chấm tự động: `bash labs/cham.sh DSY L06 duong_dan/bai_cua_ban.py`
