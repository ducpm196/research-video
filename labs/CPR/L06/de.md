# Lab CPR L06 — Cấp phát động calloc, mở rộng realloc an toàn và giải phóng

Viết chương trình C chuẩn C11 đọc `n1`, `n1` số nguyên (cấp bằng `calloc`), rồi đọc `n2`, mở rộng mảng bằng `realloc` qua con trỏ tạm lên `n1 + n2` phần tử và đọc tiếp `n2` số nguyên.
Tính tổng toàn mảng, `free(p); p = NULL;`, và in đúng 2 dòng:
1. `len=<n1 + n2> sum=<tổng>`
2. `freed=<p == NULL ? 1 : 0>`

Chấm tự động:
```bash
bash labs/cham.sh CPR L06 duong_dan/bai_cua_ban.c
```
