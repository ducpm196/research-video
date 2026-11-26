# Lab CSA L00 — Hệ đếm nhị phân, thập lục phân và phân biệt KB vs KiB

Đọc từ `stdin` 2 số nguyên không dấu `x kib_count` (dạng `x=47 kib_count=1`). Đổi `x` sang hệ 16, in tổng trạng thái và giá trị cực đại `uint8_t`, cùng chênh lệch `(1024 - 1000) * kib_count`.

In đúng 3 dòng: `dec=<u_> hex=0x<XX>`, `u8_states=<d> max=<u>`, `kib_minus_kb=<d>`.
Chấm tự động: `bash labs/cham.sh CSA L00 duong_dan/bai_cua_ban.c`
