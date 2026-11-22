# Lab DBS L17 — SQLite thật: tính toán phân lô di chuyển bảng lớn không khoá lâu

Viết tập lệnh SQLite tính số lô và tổng thời gian chép bảng `5 000 000` dòng với kích thước lô `1 000` (`0.5 s`/lô), đồng thời mô phỏng sao chép phân lô 10 dòng đầu vào bảng bóng `Users_New`, in đúng 3 dòng:
1. `batches=5000`
2. `total_seconds=2500`
3. `shadow_copied=10`

Chấm tự động:
```bash
bash labs/cham.sh DBS L17 duong_dan/bai_cua_ban.sql
```
