# Lab CSA L08 (Mô phỏng hiệu năng CPU) — Tính CPI trung bình và thời gian chạy

Viết chương trình Python cho chương trình có tổng số lệnh `IC = 1e9` gồm `50%` số học (`CPI = 1`), `30%` tải/lưu (`CPI = 3`), `20%` nhánh (`CPI = 2`) chạy trên CPU `2.0 GHz` (`2e9 Hz`), in đúng 3 dòng:
1. `cpi_avg=1.80`
2. `cpu_time_s=0.900`
3. `speedup_vs_3ghz_cpi3=1.11`

Chấm tự động:
```bash
bash labs/cham.sh CSA L08 duong_dan/bai_cua_ban.py
```
