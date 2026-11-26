# Lab SDP L07 — SOLID 3: Tiêm phụ thuộc đồng hồ (Clock Injection)

Đọc `stdin` `m1=<int> d1=<int> m2=<int> d2=<int>`. Cài `greet(clock_fn)` trả `'Chuc mung nam moi'` vào mùng 1 tháng 1 và `'Ngay binh thuong'` cho ngày khác; gọi lại lần nữa với cùng đồng hồ `(m1, d1)` để kiểm chứng kết quả không đổi (`deterministic=1`).

In đúng 3 dòng: `jan1=<str>`, `may10=<str>`, `deterministic=<0|1>`.
Chấm tự động: `bash labs/cham.sh SDP L07 duong_dan/bai_cua_ban.py`
