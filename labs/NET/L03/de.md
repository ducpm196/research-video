# Lab NET L03 — Kiểm tra lỗi bằng chia đa thức XOR tính CRC

Đọc `stdin` `data=<bits> gen=<bits>`. Tính phần dư CRC của `data + '0'*(len(gen)-1)`, ghép khung truyền và kiểm chứng phía nhận chia hết.

In đúng 3 dòng: `crc_rem=<bits>`, `tx_frame_len=<d>`, `rx_ok=<0|1>`.
Chấm tự động: `bash labs/cham.sh NET L03 duong_dan/bai_cua_ban.py`
