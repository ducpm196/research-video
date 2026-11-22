# Lab NET L06 (Mô phỏng bảng định tuyến) — Khớp tiền tố dài nhất (LPM)

Viết chương trình Python tra bảng `{10.1.0.0/20: 'A', 10.1.8.0/21: 'B', 0.0.0.0/0: 'DEFAULT'}` cho hai đích `10.1.10.5` và `8.8.8.8`, và kiểm tra gom 2 mạng `/24` thành `/23`, in đúng 3 dòng:
1. `dst_10_1_10_5=B`
2. `dst_8_8_8_8=DEFAULT`
3. `collapsed_prefix=192.168.0.0/23`

Chấm tự động:
```bash
bash labs/cham.sh NET L06 duong_dan/bai_cua_ban.py
```
