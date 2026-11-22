# Lab BCH L00 — Áp dụng cây câu hỏi quyết định nhu cầu chuỗi khối cho 5 công ty đối thủ

Cho điều kiện dùng chung sổ cái: `need = shared_state and multi_writers and (not trusted_ttp) and (not mutual_trust)`. So sánh chi phí vận hành giữa `1` máy chủ trung tâm tin cậy với ngưỡng đồng thuận quá bán `n // 2 + 1` cho mạng `n = 5` công ty đối thủ, và kiểm tra hai tình huống (có bên tin cậy vs không có bên tin cậy).
In đúng 1 dòng `central_ops=... maj_quorum_5=... school_need=0/1 rivals_need=0/1`.

Chấm tự động:
```bash
bash labs/cham.sh BCH L00 duong_dan/bai_cua_ban.py
```
