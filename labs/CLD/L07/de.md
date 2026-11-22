# Lab CLD L07 — Công thức tự co giãn ngang (HPA) kèm dung sai

Viết hàm `hpa(cur, cpu, tgt=60, tol=0.10)` trả về `cur` nếu `|cpu/tgt - 1| <= tol`, ngược lại trả về `ceil(cur * cpu / tgt)`. Kiểm tra từ `cur = 6` với mức tải cao `cpu = 84%` (cần mở rộng) và tải gần đích `cpu = 64%` (giữ nguyên).

Định dạng đầu ra (2 dòng):
`replicas_at_84=<số nguyên>`
`replicas_at_64=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh CLD L07 duong_dan/bai_cua_ban.py
```
