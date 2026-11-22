# Lab WEB L07 — Node.js thật: so sánh chi phí phân trang OFFSET vs Cursor

Viết tập lệnh Node.js tính số dòng cần đọc và bỏ qua khi lấy trang `1 000` (mỗi trang `20` dòng) bằng `OFFSET` (`19 980` dòng bị bỏ) so với Cursor (`0` dòng bỏ), in đúng 3 dòng:
1. `offset_skipped=19980`
2. `offset_scanned=20000`
3. `cursor_scanned=20`

Chấm tự động:
```bash
bash labs/cham.sh WEB L07 duong_dan/bai_cua_ban.js
```
