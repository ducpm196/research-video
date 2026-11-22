# Lab NET L10 (Mô phỏng cửa sổ trượt) — So sánh dừng–chờ và cửa sổ phủ BDP (tích băng thông–trễ)

Viết chương trình Python tính hiệu suất dừng–chờ với gói `8 000 bit`, tốc độ `1 Gbps`, `RTT = 30 ms`, tính số gói BDP (tích băng thông–trễ = `3 750` gói, lưu ý để đạt 100% cần `W >= 3 750`, bài kiểm chứng dùng `W = 3 750`) và hiệu suất khi cửa sổ `W = 1 000` gói, in đúng 3 dòng:
1. `stop_wait_eff=0.00027`
2. `bdp_packets=3750`
3. `w1000_eff=26.7%`

Chấm tự động:
```bash
bash labs/cham.sh NET L10 duong_dan/bai_cua_ban.py
```
