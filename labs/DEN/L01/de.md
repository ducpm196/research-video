# Lab DEN L01 — Bộ lọc xác suất Bloom trên cây LSM

Khi tìm một khoá không tồn tại trên `8` tệp dữ liệu đã sắp (`SSTable`), mỗi tệp có bộ lọc xác suất Bloom với tỉ lệ dương tính giả (`FPR`) là `2%` (`0.02`), tính kỳ vọng số tệp phải mở đĩa và phần trăm đọc đĩa được tránh (%).

Định dạng đầu ra (2 dòng):
`expected_disk_reads=<2 chữ số>`
`disk_avoided_pct=<1 chữ số>%`

Chấm tự động:
```bash
bash labs/cham.sh DEN L01 duong_dan/bai_cua_ban.py
```
