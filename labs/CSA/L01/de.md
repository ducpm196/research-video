# Lab CSA L01 — Số nguyên không dấu, bù 2 và ranh giới tràn 8 bit

Đọc từ `stdin` 2 giá trị dạng `raw_hex=FF base=127` (giá trị hex 8-bit và số nguyên `uint8_t` cộng thêm 1). Khai báo `<stdint.h>` để dùng kiểu 8 bit không dấu `uint8_t` (0..255), kiểu có dấu bù 2 `int8_t` (-128..127) và hằng `INT8_MIN`, `INT8_MAX`; giải mã `i8` bằng công thức `u8 >= 128 ? (int)u8 - 256 : (int)u8` (hoặc chép 1 byte bằng `memcpy` từ `<string.h>`), và tính kết quả tràn không dấu `(base + 1) mod 256` (chia lấy dư 256).

In đúng 3 dòng: `u8=<u_> i8=<d>`, `i8_min=-128 i8_max=127`, `u8_wrap_127_plus_1=<u_>`.
Chấm tự động: `bash labs/cham.sh CSA L01 duong_dan/bai_cua_ban.c`
