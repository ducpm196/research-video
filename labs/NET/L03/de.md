# Lab NET L03 (Mô phỏng phát hiện lỗi) — Chia đa thức XOR tính CRC 3 bit

Viết chương trình Python cài phép chia XOR CRC với chuỗi `11010011101100` và đa thức sinh `1011`: tính phần dư bên gửi, khung `17` bit gửi đi và kiểm tra bên nhận chia lại ra `000`, in đúng 3 dòng:
1. `crc_rem=100`
2. `tx_frame_len=17`
3. `rx_ok=1`

Chấm tự động:
```bash
bash labs/cham.sh NET L03 duong_dan/bai_cua_ban.py
```
