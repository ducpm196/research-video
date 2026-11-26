# Lab CPR L09 — Mảng động Rec 16 byte tăng dung lượng gấp đôi qua stdin

Viết chương trình C chuẩn C11 đọc `init_cap` (`>= 1`) và `n`, tiếp theo đọc `n` cặp `(type, amt)` từ `stdin`.
Cài mảng động `Rec *` tăng dung lượng gấp đôi bằng `realloc` qua biến tạm mỗi khi đầy, lọc tổng `amt` của các bản ghi có `type == 1`, giải phóng sạch và in đúng 2 dòng:
1. `rec_size=16 cap=<dung lượng cuối> sum_t1=<tổng loại 1>`
2. `clean=<d == NULL ? 1 : 0>`

Chấm tự động:
```bash
bash labs/cham.sh CPR L09 duong_dan/bai_cua_ban.c
```
