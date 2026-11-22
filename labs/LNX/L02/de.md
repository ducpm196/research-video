# Lab LNX L02 — Tính mã thoát POSIX và kiểm chứng dọn dẹp khi nhận SIGTERM

Viết kịch bản Bash tạo subshell có `trap` đón tín hiệu `TERM` in ra `graceful=1` rồi thoát mã `143`, gửi `kill -TERM`, và in đúng 3 dòng:
1. `graceful=1`
2. `term_exit=143`
3. `kill_exit=137`

Chấm tự động:
```bash
bash labs/cham.sh LNX L02 duong_dan/bai_cua_ban.sh
```
