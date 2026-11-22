# Lab HCI L02 — Định luật Fitts trên khoảng cách D=360 px giữa nút 18 px và nút 72 px

Áp dụng công thức Fitts `T = a + b * log2(D / W + 1)` với `a = 0.1`, `b = 0.15`, `D = 360 px` cho hai bề rộng nút `W = 18 px` và `W = 72 px`, in chỉ số độ khó `ID = log2(D / W + 1)` và thời gian trỏ.

Định dạng đầu ra (1 dòng):
`id_18=<3 chữ số> t_18px=<3 chữ số>s id_72=<3 chữ số> t_72px=<3 chữ số>s`

Chấm tự động:
```bash
bash labs/cham.sh HCI L02 duong_dan/bai_cua_ban.py
```
