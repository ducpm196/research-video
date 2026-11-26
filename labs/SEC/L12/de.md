# Lab SEC L12 — Mô phỏng bảng luật tường lửa first-match và chặn mặc định

Đọc `stdin` `allow_src=<s1> allow_dst=<d1> allow_port=<p1> q1=<s,d,p> q2=<s,d,p> q3=<s,d,p>`. Dựng bảng luật cho phép đúng cặp quy định rồi chặn mặc định mọi lưu lượng còn lại.

In đúng 3 dòng: `app_db_5432=<ALLOW|DENY>`, `web_db_5432=<ALLOW|DENY>`, `app_db_22=<ALLOW|DENY>`.
Chấm tự động: `bash labs/cham.sh SEC L12 duong_dan/bai_cua_ban.py`
