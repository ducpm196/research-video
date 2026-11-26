# Lab DSY L10 — Kiểm chứng Bloom filter: 0% false negative & FPR lý thuyết

Đọc `stdin` `m=<int> n=<int> k=<int>`. Cài Bloom filter SHA-256 chèn `n` phần tử, xác minh không có âm tính giả và tính FPR lý thuyết `(1 - exp(-k*n/m))^k`.

In đúng 3 dòng: `false_negatives=<d>`, `theory_fpr_pct=<.2f>%`, `bits_per_elem=<d>`.
Chấm tự động: `bash labs/cham.sh DSY L10 duong_dan/bai_cua_ban.py`
