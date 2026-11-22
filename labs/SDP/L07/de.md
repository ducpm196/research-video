# Lab SDP L07 — SOLID 3: Tiêm phụ thuộc đồng hồ (Clock Injection)

Viết hàm `greet(clock_fn)` trả `'Chuc mung nam moi'` nếu `(month, day) == (1, 1)` ngược lại trả `'Ngay binh thuong'`. Tiêm hai lambda đồng hồ `(1, 1)` và `(5, 10)`, in đúng 3 dòng:
1. `jan1=Chuc mung nam moi`
2. `may10=Ngay binh thuong`
3. `deterministic=1`

Chấm tự động:
```bash
bash labs/cham.sh SDP L07 duong_dan/bai_cua_ban.py
```
