# Lab LNX L00 — Liên kết cứng vs liên kết mềm và đếm link_count

Viết kịch bản Bash tạo `orig.txt` chứa `SAFE_DATA` trong môi trường Linux thật (chạy trực tiếp nếu là Linux, hoặc qua `docker run --rm postgres:17-alpine` trên Windows để giữ chuẩn liên kết mềm POSIX), tạo:
- `hard.txt` bằng `ln orig.txt hard.txt`
- `sym.txt` bằng `ln -s orig.txt sym.txt`
Sau đó `rm orig.txt` và in đúng 3 dòng:
1. `hard_content=SAFE_DATA`
2. `hard_links=1`
3. `sym_failed=1` (bằng 1 vì đọc `sym.txt` thất bại sau khi xoá `orig.txt`)

Chấm tự động:
```bash
bash labs/cham.sh LNX L00 duong_dan/bai_cua_ban.sh
```
