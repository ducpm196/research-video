# Lab LNX L05 — Kiểm tra lắng nghe ổ cắm TCP động và thứ tự phân giải /etc/hosts

Viết kịch bản Bash (có thể gọi `python`/`python3 -c` ở bên trong) đọc hai cặp `<nhãn> <địa_chỉ>` từ `stdin` (dòng 1 và dòng 2), mở ổ cắm TCP bằng `socket.bind((host, 0))` xác nhận từng địa chỉ gắn được, kiểm tra thứ tự `files` trước `dns` trong `/etc/nsswitch.conf` (hoặc loopback `localhost`), rồi in `<nhãn>=<địa chỉ gắn>` cho 2 dòng đầu và `hosts_before_dns=<0|1>`.

Chấm tự động:
```bash
bash labs/cham.sh LNX L05 duong_dan/bai_cua_ban.sh
```
