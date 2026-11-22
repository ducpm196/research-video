# Lab CLC L10 — Tính dung lượng dự phòng liên vùng ở tải 1 800 yêu cầu/giây

Hệ thống phục vụ tải bình thường `1 800 yêu cầu/giây (req/s)` và phải sống sót khi mất 1 vùng. Tính tổng công suất cần cấp ở mô hình chủ động–chủ động (`Active-Active`) `2` vùng (mỗi vùng gánh `1 800`), mô hình `3` vùng dự phòng `N+1` (mỗi vùng gánh `900`), và phần trăm dự phòng dư của phương án 2 vùng.

Định dạng đầu ra (3 dòng):
`cap_2region=<số>`
`cap_3region=<số>`
`headroom_2region=<1 chữ số>%`

Chấm tự động:
```bash
bash labs/cham.sh CLC L10 duong_dan/bai_cua_ban.py
```
