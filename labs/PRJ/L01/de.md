# Lab PRJ L01 (100đ theo labs/PRJ/SPEC.md) — Lõi chuyển khoản bút toán kép

Viết chương trình Python cài lõi chuyển khoản SQLite (khoá thứ tự tăng dần, kiểm số dư nguyên tử, ghi bút toán kép) chạy 3 giao dịch: 1) A→B 300; 2) C→B 900 (từ chối thiếu số dư); 3) B→C 150 kèm phí 5, với số dư đầu A=500, B=400, C=150, FEE=0. In đúng 3 dòng:
1. `tx_results=True,False,True`
2. `ledger_sum=0`
3. `balances=A:200,B:545,C:300,FEE:5`

Chấm tự động:
```bash
bash labs/cham.sh PRJ L01 duong_dan/bai_cua_ban.py
```
