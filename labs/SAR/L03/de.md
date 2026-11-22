# Lab SAR L03 — Máy quét ranh giới phụ thuộc 3 lớp kiến trúc

Xếp hạng 3 lớp `RANK = {'UI': 0, 'App': 1, 'Data': 2}`. Một cạnh gọi `(caller, callee)` chỉ hợp lệ khi `RANK[caller] < RANK[callee]`. Kiểm tra danh sách `[('UI', 'App'), ('App', 'Data'), ('UI', 'Data'), ('Data', 'App')]` để đếm cạnh hợp lệ và số vi phạm.

Định dạng đầu ra (3 dòng):
`valid_edges=<số>`
`violations=<số>`
`arch_clean=<0|1>`

Chấm tự động:
```bash
bash labs/cham.sh SAR L03 duong_dan/bai_cua_ban.py
```
