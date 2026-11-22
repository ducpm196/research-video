# Dự án PRJ L10 — Tổng hợp Chặng 11: PID, lập lịch RMS & cây Merkle

Viết chương trình Python: (1) tính hệ số CPU `U = 3/10 + 5/20 = 0.55` và kiểm dưới biên Liu-Layland 2 tác vụ `0.828`; (2) chạy 5 bước điều khiển tỉ lệ `Kp=0.5` từ `x=0` hướng tới `target=10`; (3) xây gốc Merkle SHA-256 từ 4 lá `'tx0'..'tx3'` và chứng minh sửa `'tx2'` thành `'tx2*'` làm đổi gốc, in đúng 3 dòng:
1. `rms_u=0.55 schedulable=1`
2. `pid_step5=9.688`
3. `merkle_tamper_detected=1`

Chấm tự động:
```bash
bash labs/cham.sh PRJ L10 duong_dan/bai_cua_ban.py
```
