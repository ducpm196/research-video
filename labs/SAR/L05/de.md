# Lab SAR L05 — Dự phòng và ước lượng dung lượng phân mảnh (sharding)

Đọc `stdin` `tb=<int> max_node_gb=<int> rf=<int>` (với `1 TB = 1000 GB`). Tính số mảnh tối thiểu cần có (chia trần `ceil(tb * 1000 / max_node_gb)`), tổng số nút vật lý sau khi nhân hệ số sao chép `rf`, và tổng dung lượng lưu trữ cụm `tb * rf`.

In 3 dòng (giữ nguyên tên khoá cố định kể cả khi `rf` thay đổi): `shards_needed=<d>`, `total_nodes_rf3=<d>`, `total_stored_tb=<d>`.
Chấm tự động: `bash labs/cham.sh SAR L05 duong_dan/bai_cua_ban.py`
