# Lab CLD L06 — Phân mảnh tài nguyên khi xếp Pod lên nút máy

Mỗi nút máy có `6.0 CPU` (`CPU` = đơn vị xử lý), mỗi `Pod` yêu cầu `2.2 CPU`. Tính số `Pod` tối đa xếp được vào một nút và phần trăm tài nguyên bị kẹt không sử dụng.

Định dạng đầu ra (2 dòng):
`pods_per_node=<số nguyên>`
`stranded_pct=<1 chữ số>%`

Chấm tự động:
```bash
bash labs/cham.sh CLD L06 duong_dan/bai_cua_ban.py
```
