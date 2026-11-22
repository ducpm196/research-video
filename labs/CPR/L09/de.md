# Lab CPR L09 — Phân tích mảng động Rec 16 byte sạch bộ nhớ

Viết chương trình C chuẩn C11 dùng `typedef struct { uint64_t ts; uint16_t hdr; uint16_t flag; uint32_t amt; } Rec;`, cài mảng động tăng gấp đôi từ `cap=2` để nạp 5 bản ghi có `amt = {100, 250, 400, 150, 600}` (các mục vị trí chẵn 0,2,4 mang loại 1, vị trí lẻ mang loại 2), rồi tính tổng loại 1 và giải phóng sạch, in đúng 2 dòng:
1. `rec_size=16 cap=8 sum_t1=1100`
2. `clean=1`

Chấm tự động:
```bash
bash labs/cham.sh CPR L09 duong_dan/bai_cua_ban.c
```
