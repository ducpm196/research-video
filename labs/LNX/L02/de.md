# Lab LNX L02 — Kiểm chứng trap SIGTERM và tính mã thoát POSIX qua stdin

Viết kịch bản Bash đọc `<grace_code> <sig_num>` từ `stdin`, bật subshell nền cài `trap` in `graceful=1` rồi `exit $grace_code`, gửi `kill -TERM`, thu `term_exit=$?` và tính `kill_exit=$((128 + sig_num))`.
In đúng 3 dòng: `graceful=1`, `term_exit=...`, `kill_exit=...`.

Chấm tự động:
```bash
bash labs/cham.sh LNX L02 duong_dan/bai_cua_ban.sh
```
