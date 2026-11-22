# Lab OSY L14 (Mô phỏng phân quyền) — Đổi chuỗi rwx 9 ký tự sang bát phân

Viết chương trình Python chuyển chuỗi quyền `'rwxr-x---'` sang bát phân và kiểm tra `750` có cho nhóm đọc/vào thư mục nhưng chặn người ngoài hoàn toàn không, in đúng 3 dòng:
1. `octal_rwxr_x___=750`
2. `octal_rw_r__r__=644`
3. `group_can_enter=1 other_denied=1`

Chấm tự động:
```bash
bash labs/cham.sh OSY L14 duong_dan/bai_cua_ban.py
```
