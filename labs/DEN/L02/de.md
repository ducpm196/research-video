# Lab DEN L02 — Khuếch đại ghi cây B so với LSM

Đọc `stdin` `page_b=<int> rec_b=<int> tiers=<int>`. Tính khuếch đại ghi của cây B khi sửa 1 bản ghi trong trang `page_b` và khuếch đại ghi của cây LSM gộp theo bậc theo công thức `1 (nhật ký) + 1 (xả) + tiers`.

In 2 dòng: `btree_wa=<.1f>x`, `lsm_tiered_wa=<.1f>x`.
Chấm tự động: `bash labs/cham.sh DEN L02 duong_dan/bai_cua_ban.py`
