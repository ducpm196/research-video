# Lab CPR L03 — Đếm độ dài chuỗi và sao chép chống tràn qua stdin

Viết chương trình C chuẩn C11 đọc `cap` (số nguyên `1 <= cap <= 64`) và chuỗi không khoảng trắng `src` (tối đa 127 ký tự) từ `stdin`.
Dùng `snprintf(buf, (size_t)cap, "%s", src)` chép an toàn vào vùng đệm và in đúng 2 dòng:
1. `src_len=<strlen(src)> buf_size=<cap>`
2. `cut=<buf> last_byte=<(int)(unsigned char)buf[cap - 1] nếu tràn hoặc (int)(unsigned char)buf[strlen(buf)]>`

Chấm tự động:
```bash
bash labs/cham.sh CPR L03 duong_dan/bai_cua_ban.c
```

> Gợi ý đọc `stdin`: `size_t cap = 0; char src[128] = {0}; if (scanf("%zu %127s", &cap, src) != 2) return 1;` (`%127s` giới hạn tối đa 127 ký tự chừa 1 byte cho `\0`).
