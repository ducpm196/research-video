# Lab SEC L04 — Kiểm tra chính sách phân quyền RBAC tối thiểu

Đọc `stdin` `r1=<role:act> r2=<role:act> deny_check=<role:act>`. Dựa trên bảng quyền `accountant: read,create`, `auditor: read`, kiểm tra từng yêu cầu quyền hạn.

In đúng 3 dòng: `accountant_create=<0|1>`, `auditor_read=<0|1>`, `auditor_create_denied=<0|1>`.
Chấm tự động: `bash labs/cham.sh SEC L04 duong_dan/bai_cua_ban.py`
