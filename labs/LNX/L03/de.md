# Lab LNX L03 — Tách luồng 1/2 và lọc lỗi 5xx quy mô động qua stdin

Viết kịch bản Bash đọc `<total_lines> <c500> <c503> <msg_out> <msg_err>` từ `stdin`, thực hiện tách stdout (luồng 1) và stderr (luồng 2), tạo nhật ký `total_lines` dòng (`c500` dòng `500`, `c503` dòng `503`, còn lại `200`) rồi đếm `5xx` bằng `grep`.
In 3 dòng: `stdout_ok=<0|1>`, `stderr_ok=<0|1>`, `err_5xx=<số dòng 5xx>`.

Chấm tự động:
```bash
bash labs/cham.sh LNX L03 duong_dan/bai_cua_ban.sh
```
