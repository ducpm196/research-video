# Lab CSA L07 (Mô phỏng ISA nhỏ) — Đếm tổng số lệnh thực thi của vòng lặp

Viết chương trình Python mô phỏng đoạn hợp ngữ khởi tạo `R1=0, R2=1` (1 lệnh nạp mỗi thanh ghi → 2 lệnh đầu) rồi chạy vòng lặp `while R2 <= 10` (`N=10` lượt, mỗi lượt gồm `ADD` cộng, `ADDI` tăng 1, `BLE` nhảy nếu ≤ = 3 lệnh), in đúng 3 dòng:
1. `sum_1_to_10=55`
2. `loop_iters=10`
3. `total_dynamic_insts=32`

Chấm tự động:
```bash
bash labs/cham.sh CSA L07 duong_dan/bai_cua_ban.py
```
