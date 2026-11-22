# Lab PAR L00 — Định luật Amdahl: phần song song p=0.80 trên N=8 lõi và trần giới hạn

Tính hệ số tăng tốc theo Amdahl `1 / ((1 - p) + p / N)` với `p = 0.80` trên `N = 8` lõi cùng giới hạn khi `N` tiến ra vô cực (`1 / (1 - p)`).

Định dạng đầu ra (1 dòng):
`amdahl_8=<2 chữ số>x max_limit=<1 chữ số>x`

Chấm tự động:
```bash
bash labs/cham.sh PAR L00 duong_dan/bai_cua_ban.py
```
