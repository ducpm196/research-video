# Lab BCH L12 — So sánh dung lượng tiêu đề 80 byte/khối với dữ liệu đầy khối ở tốc độ 5 khối/giờ

Xét mạng tạo trung bình `5` khối mỗi giờ trong `1` năm (`5 * 24 * 365 = 43_800` khối). Tính tổng dung lượng 1 năm nếu chỉ tải tiêu đề `80 byte` (tính bằng `MB`, 2 chữ số) so với tải đủ cả khối `1_000_000 byte` (tính bằng `GB`, 2 chữ số), cùng tỉ số thu gọn (`:.0f`).
In đúng 1 dòng `blocks_yr=... header_MB=... full_GB=... ratio=...x`.

Chấm tự động:
```bash
bash labs/cham.sh BCH L12 duong_dan/bai_cua_ban.py
```
