# Lab SEC L04 — Kiểm tra chính sách phân quyền theo vai trò (RBAC) tối thiểu

Viết chương trình Python cài bảng phân quyền theo vai trò `RBAC = {'accountant': {'read', 'create'}, 'auditor': {'read'}}`: kiểm tra kiểm toán viên tạo hoá đơn bị từ chối, còn kế toán viên đọc/tạo hợp lệ, in đúng 3 dòng:
1. `accountant_create=1`
2. `auditor_read=1`
3. `auditor_create_denied=1`

Chấm tự động:
```bash
bash labs/cham.sh SEC L04 duong_dan/bai_cua_ban.py
```
