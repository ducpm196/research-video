# Lab PAR L09 — Nhân ma trận n=512 chia khối 16×16 cắt giảm 16 lần truy cập bộ nhớ chậm

Với cỡ ma trận vuông `n = 512` và cỡ khối `b = 16`, tính số phần tử phải đọc từ bộ nhớ chậm khi nhân ngây thơ `2 * n^3` và khi chia khối `2 * n^3 // b`.

Định dạng đầu ra (1 dòng):
`naive_reads=<số nguyên> tiled_reads=<số nguyên> reduction=<số nguyên>x`

Chấm tự động:
```bash
bash labs/cham.sh PAR L09 duong_dan/bai_cua_ban.py
```
