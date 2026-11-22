# Lab SEP L02 — Bất khả thi đồng thời: tính giá trị dự báo dương (PPV) khi tỉ lệ nền 40% vs 15%

Với mô hình giữ `TPR = 0.90` (tỉ lệ dương thật) và `FPR = 0.15` (tỉ lệ dương giả): tính `PPV = (b * TPR) / (b * TPR + (1 - b) * FPR)` cho nhóm A (`b = 0.40`) và nhóm B (`b = 0.15`).

Định dạng đầu ra (1 dòng):
`ppv_A=<3 chữ số> ppv_B=<3 chữ số> mismatch=<0 hoặc 1>`

Chấm tự động:
```bash
bash labs/cham.sh SEP L02 duong_dan/bai_cua_ban.py
```
