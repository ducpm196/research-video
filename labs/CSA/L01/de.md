# Lab CSA L01 — Số nguyên không dấu, bù 2 và ranh giới tràn 8 bit

Đọc từ `stdin` 2 giá trị dạng `raw_hex=FF base=127` (giá trị hex 8-bit và số nguyên `uint8_t` cộng thêm 1). Giải mã mẫu bit dưới dạng `uint8_t` và `int8_t` bù 2, cùng kết quả tràn không dấu `(base + 1) & 0xFF`.

In đúng 3 dòng: `u8=<u_> i8=<d>`, `i8_min=-128 i8_max=127`, `u8_wrap_127_plus_1=<u_>`.
Chấm tự động: `bash labs/cham.sh CSA L01 duong_dan/bai_cua_ban.c`
