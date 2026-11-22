# Lab PAR L05 — Chia sẻ giả (False Sharing): tính số bộ đếm 8 byte/dòng 64 byte và phần đệm

Tính số biến 8 byte vừa khít một dòng bộ nhớ đệm 64 byte (`cache line`), rồi tính tổng bộ nhớ khi tách đệm 4 biến đếm mỗi biến một dòng 64 byte riêng.

Định dạng đầu ra (1 dòng):
`shared_per_64B=<số> count=4 padded_total_B=<số>`

Chấm tự động:
```bash
bash labs/cham.sh PAR L05 duong_dan/bai_cua_ban.py
```
