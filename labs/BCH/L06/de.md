# Lab BCH L06 — Xác suất đuổi kịp Nakamoto

Đọc `q1 z1 q2 z2` từ stdin (ví dụ `0.15 6 0.25 4`). Dùng công thức xấp xỉ Nakamoto (2008) `P = 1 - sum_{k=0..z} (e^{-lambda} * lambda^k / k!) * (1 - (q/p)^{z-k})` với `p = 1 - q`, `lambda = z * q / p` để tính xác suất tấn công chi tiêu hai lần (`q < 0.5`) thành công cho 2 kịch bản.
In đúng 1 dòng `p_q15_z6=<5 chữ số sau dấu phẩy> p_q25_z4=<4 chữ số sau dấu phẩy>`.
