# Lab SAR L00 — Đo phân vị thứ 95 (P95) và kiểm tra mục tiêu mức dịch vụ (SLO)

Sắp xếp chuỗi `100` mẫu độ trễ `[60 + (i % 25) * 4 for i in range(100)]` (đơn vị ms). Trích giá trị phân vị 95 (`P95` ở chỉ số `94`), phân vị 99 (`P99` ở chỉ số `98`) và kiểm tra mục tiêu mức dịch vụ (`SLO`: `P95 <= 160 ms`).

Định dạng đầu ra (3 dòng):
`p95_ms=<số>`
`p99_ms=<số>`
`slo_pass=<0|1>`

Chấm tự động:
```bash
bash labs/cham.sh SAR L00 duong_dan/bai_cua_ban.py
```
