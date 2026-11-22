# Lab SEC L12 — Mô phỏng bảng luật tường lửa khớp đầu tiên (first-match) và chặn mặc định

Viết hàm `decide(src, dst, port)` xét từ trên xuống danh sách luật `[(app, db, 5432, ALLOW (cho)), (*, *, *, DENY (chặn))]` cho 3 lưu lượng `(app->db:5432)`, `(web->db:5432)`, `(app->db:22)`, in đúng 3 dòng:
1. `app_db_5432=ALLOW`
2. `web_db_5432=DENY`
3. `app_db_22=DENY`

Chấm tự động:
```bash
bash labs/cham.sh SEC L12 duong_dan/bai_cua_ban.py
```
