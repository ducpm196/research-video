# Lab CLD L02 — Tận dụng bộ nhớ đệm các lớp khi dựng ảnh

Cho chuỗi 4 lớp dựng ảnh `['FROM py', 'COPY req.txt', 'RUN pip install', 'COPY src']` (dựng lại một lớp buộc dựng lại toàn bộ lớp phía sau). Đếm số lớp vẫn dùng lại được từ bộ đệm (`cache hits`) khi thay đổi chỉ ở bước `'COPY src'` so với thay đổi ở `'COPY req.txt'`.

Định dạng đầu ra (2 dòng):
`hits_src_change=<số nguyên>`
`hits_req_change=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh CLD L02 duong_dan/bai_cua_ban.py
```
