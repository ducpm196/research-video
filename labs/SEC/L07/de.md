# Lab SEC L07 — Phát hiện lộ mẫu trên chế độ ECB vs mã khối CTR (chế độ bộ đếm) dùng số dùng một lần (IV/nonce)

Viết chương trình Python mô phỏng mã hoá từng khối 8 byte giả lập chế độ khối đơn ECB (cố định) so với chế độ bộ đếm CTR (XOR thêm khoá + bộ đếm/số dùng một lần IV/nonce) trên bản rõ 16 byte lặp 2 khối giống nhau `b'BLOCK_A_' * 2`, cắt `msg[:8]` và `msg[8:]` rồi kiểm tra trực tiếp hai khối mã ECB có trùng nhau làm lộ mẫu không, in đúng 3 dòng:
1. `ecb_blocks_identical=1`
2. `ctr_blocks_identical=0`
3. `ecb_leaks_pattern=1`

Chấm tự động:
```bash
bash labs/cham.sh SEC L07 duong_dan/bai_cua_ban.py
```
