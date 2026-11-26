# Lab OSY L14 — Đổi chuỗi phân quyền rwx 9 ký tự sang bát phân

Đọc `stdin` `p1=<9chars> p2=<9chars>`. Chuyển hai chuỗi quyền thành 3 chữ số bát phân và kiểm tra trên `p1` xem nhóm có bit vào thư mục (`& 1`) và người ngoài bị từ chối hoàn toàn (`== '0'`).

In đúng 3 dòng (giữ nguyên tên khoá cố định `octal_rwxr_x___` cho `p1` và `octal_rw_r__r__` cho `p2`): `octal_rwxr_x___=<str>`, `octal_rw_r__r__=<str>`, `group_can_enter=<0|1> other_denied=<0|1>`.
Chấm tự động: `bash labs/cham.sh OSY L14 duong_dan/bai_cua_ban.py`
