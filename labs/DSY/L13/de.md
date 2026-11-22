# Lab DSY L13 [Mô phỏng phân tán] — Giao thức Cam kết hai pha (2PC) & trạng thái kẹt

Viết máy trạng thái 2PC cho 2 bên tham gia `P1, P2`: khi cả hai đều vote `PREPARED` -> điều phối quyết `COMMIT`; khi mất điều phối ngay sau `PREPARED`, các nút phải giữ khoá chờ (`blocked_until_coord_up=1`), in đúng 3 dòng:
1. `all_yes_commit=1`
2. `one_no_abort=1`
3. `prepared_blocked_on_coord_loss=1`

Chấm tự động:
```bash
bash labs/cham.sh DSY L13 duong_dan/bai_cua_ban.py
```
