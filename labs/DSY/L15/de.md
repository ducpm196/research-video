# Lab DSY L15 [Mô phỏng phân tán] — Tính dung lượng định địa chỉ của cây chỉ mục Bigtable 3 tầng

Viết chương trình Python tính số con trỏ mỗi bảng Metadata `128 MiB / 1 KiB = 2^17`, tổng số mảnh tablet định địa chỉ qua 2 tầng trỏ `2^17 * 2^17 = 2^34` và dung lượng tối đa khi mỗi mảnh `100 MiB`, in đúng 3 dòng:
1. `entries_per_table=131072`
2. `max_tablets_pow2=34`
3. `entries_sq_exact=17179869184`

Chấm tự động:
```bash
bash labs/cham.sh DSY L15 duong_dan/bai_cua_ban.py
```
