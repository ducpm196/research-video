# Lab CSA L03 — Giải mã 3 trường IEEE 754 float32 và so sánh gần đúng

Đọc từ `stdin` 2 số thực `f=-6.5 tol=1e-9`. Giải mã biểu diễn `float` 32 bit bằng `memcpy` sang `uint32_t` lấy bit dấu, số mũ trừ thiên lệch 127 và phần định trị hexa 6 chữ số, cùng kiểm tra `fabs((0.1 + 0.2) - 0.3) < tol`.

In đúng 3 dòng: `sign=<d> exp_unbiased=<d> mant_hex=0x<XXXXXX>`, `close_03=<0|1>`, `hex32=0x<XXXXXXXX>`.
Chấm tự động: `bash labs/cham.sh CSA L03 duong_dan/bai_cua_ban.c`
