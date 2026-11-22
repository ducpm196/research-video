# Lab PAR L08 — Nhóm 32 luồng GPU (Warp): phân kỳ thành 3 nhánh tốn 3 lượt chạy

Một nhóm 32 luồng phân kỳ thành 3 nhánh (10 luồng vào nhánh A, 12 vào B, 10 vào C) nên phần cứng phải chạy tuần tự 3 lượt cho mỗi nhóm 32 luồng. Tính hiệu suất trung bình `(10 + 12 + 10) / (3 * 32) * 100`.

Định dạng đầu ra (1 dòng):
`warp_eff_diverged=<số nguyên>%`

Chấm tự động:
```bash
bash labs/cham.sh PAR L08 duong_dan/bai_cua_ban.py
```
