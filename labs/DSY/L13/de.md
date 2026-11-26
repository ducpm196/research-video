# Lab DSY L13 — Giao thức Cam kết hai pha (2PC) & trạng thái kẹt

Đọc `stdin` `votes1=<V1,V2> votes2=<V1,V2> state=<STR> coord_up=<0|1>`. Ra quyết định `COMMIT`/`ABORT` theo phiếu pha chuẩn bị và xác định nút có bị khóa chờ hay không.

In đúng 3 dòng: `all_yes_commit=<0|1>`, `one_no_abort=<0|1>`, `prepared_blocked_on_coord_loss=<0|1>`.
Chấm tự động: `bash labs/cham.sh DSY L13 duong_dan/bai_cua_ban.py`
