# Lab LNX L00 — Liên kết cứng vs liên kết mềm và đếm link_count theo stdin

Viết kịch bản Bash đọc một dòng `<chuỗi_dữ_liệu> <del_orig>` từ `stdin` (trong đó `del_orig` là `1` hoặc `0`), thực thi trên môi trường Linux POSIX thật (chạy trực tiếp trên Linux hoặc qua `docker run --rm postgres:17-alpine sh -c ...` trên Windows):
- Tạo `orig.txt` chứa `<chuỗi_dữ_liệu>`, tạo `hard.txt` (`ln orig.txt hard.txt`) và `sym.txt` (`ln -s orig.txt sym.txt`)
- Nếu `del_orig == 1`, xoá `orig.txt` rồi kiểm tra lại cả hai liên kết; nếu `del_orig == 0`, giữ nguyên `orig.txt`.
In đúng 3 dòng: `hard_content=...`, `hard_links=...`, `sym_failed=<0|1>`.

Chấm tự động:
```bash
bash labs/cham.sh LNX L00 duong_dan/bai_cua_ban.sh
```
