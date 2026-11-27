# Lab DSY L10 — Kiểm chứng Bloom filter: 0% false negative & FPR lý thuyết

Đọc `stdin` `m=<int> n=<int> k=<int>`. Cài Bloom filter SHA-256 trên mảng `m` bit: chèn từng phần tử `x` từ `0` tới `n - 1` qua `k` chỉ số băm `i` từ `0` tới `k - 1` theo công thức `int(hashlib.sha256(f"{i}:{x}".encode()).hexdigest(), 16) % m`. Sau khi chèn, kiểm lại cả `n` phần tử để xác minh `false_negatives=0` và tính FPR lý thuyết bằng `(1 - math.exp(-k * n / m)) ** k`.

In đúng 3 dòng: `false_negatives=<d>`, `theory_fpr_pct=<.2f>%`, `bits_per_elem=<d>`.
Chấm tự động: `bash labs/cham.sh DSY L10 duong_dan/bai_cua_ban.py`
