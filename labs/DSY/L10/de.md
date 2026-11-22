# Lab DSY L10 [Mô phỏng phân tán] — Kiểm chứng Bloom filter: 0% false negative & FPR lý thuyết

Viết chương trình Python cài Bloom filter `m = 1000` bit, `k = 7` hàm băm, chèn `n = 100` chuỗi `'k0'..'k99'`: kiểm tra tất cả `100` chuỗi đã chèn đều trả `True` (0 âm tính giả) và tính FPR lý thuyết `(1 - exp(-k*n/m))^k`, in đúng 3 dòng:
1. `false_negatives=0`
2. `theory_fpr_pct=0.82%`
3. `bits_per_elem=10`

Chấm tự động:
```bash
bash labs/cham.sh DSY L10 duong_dan/bai_cua_ban.py
```
