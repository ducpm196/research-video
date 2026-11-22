# Lab SAR L05 — Quy mô phân mảnh (shard) khi nhân bản hệ số RF = 3

Kho dữ liệu logic dung lượng `8 TB` (`8 000 GB`) cần chia mảnh sao cho mỗi nút giữ tối đa `400 GB`. Với hệ số sao chép (`RF`) bằng `3`, tính số phân mảnh tối thiểu, tổng số nút vật lý và tổng dung lượng lưu trên cụm.

Định dạng đầu ra (3 dòng):
`shards_needed=<số>`
`total_nodes_rf3=<số>`
`total_stored_tb=<số>`

Chấm tự động:
```bash
bash labs/cham.sh SAR L05 duong_dan/bai_cua_ban.py
```
