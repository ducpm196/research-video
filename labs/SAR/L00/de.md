# Lab SAR L00 — Đo P95, P99 và kiểm tra mục tiêu SLO

Đọc `stdin` `base=<int> mod=<int> step=<int> slo=<int>`. Sinh `100` mẫu `base + (i % mod) * step`, sắp xếp tăng, rút `P95` (chỉ số 94), `P99` (chỉ số 98) và kiểm `P95 <= slo`.

In 3 dòng: `p95_ms=<d>`, `p99_ms=<d>`, `slo_pass=<0|1>`.
Chấm tự động: `bash labs/cham.sh SAR L00 duong_dan/bai_cua_ban.py`
