# Lab NET L11 (Mô phỏng tắc nghẽn TCP) — Quỹ đạo cửa sổ tắc nghẽn cwnd qua khởi động chậm và AIMD

Viết chương trình Python mô phỏng cửa sổ tắc nghẽn `cwnd` bắt đầu từ `1`, ngưỡng chuyển pha `ssthresh = 16`: mô phỏng `6` RTT đầu theo cơ chế AIMD (tăng cộng – giảm nhân: tăng gấp đôi đến ngưỡng 16 rồi tăng cộng lên 17), sau đó gặp mất gói hết giờ chờ `timeout` (đặt `ssthresh = cwnd // 2`, `cwnd = 1`), in đúng 3 dòng:
1. `slowstart_trace=1,2,4,8,16`
2. `aimd_step1=17`
3. `after_timeout_ssthresh=8 cwnd=1`

Chấm tự động:
```bash
bash labs/cham.sh NET L11 duong_dan/bai_cua_ban.py
```
