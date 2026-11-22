# Lab WEB L12 — Node.js thật: ngân sách thời gian khung hình giao diện 60Hz và 120Hz

Viết tập lệnh Node.js tính ngân sách mỗi khung hình (`1000 / Hz`) cho `60 Hz` và `120 Hz`, và kiểm tra một tác vụ chạy trên luồng giao diện mất `12 ms` có làm rớt khung ở từng tần số không, in đúng 3 dòng:
1. `budget_60hz_ms=16.7`
2. `budget_120hz_ms=8.3`
3. `task12ms_jank_at_60_120=0,1`

Chấm tự động:
```bash
bash labs/cham.sh WEB L12 duong_dan/bai_cua_ban.js
```
