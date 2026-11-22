# Lab DEN L02 — Khuếch đại ghi cây B so với LSM

Sửa một bản ghi `128 byte` nằm trong trang `8 192 byte` của cây B (phải ghi lại cả trang). So sánh khuếch đại ghi của cây B với mô hình gộp theo bậc (LSM) tổng `5` lượt ghi (`lsm_tiered_wa=5.0x`).

Định dạng đầu ra (2 dòng):
`btree_wa=<1 chữ số>x`
`lsm_tiered_wa=<1 chữ số>x`

Chấm tự động:
```bash
bash labs/cham.sh DEN L02 duong_dan/bai_cua_ban.py
```
