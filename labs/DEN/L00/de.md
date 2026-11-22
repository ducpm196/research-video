# Lab DEN L00 — Lưu trữ theo hàng so với theo cột

Tính tổng dung lượng (`GB`, quy ước `1 GB = 10^9 byte`) phải đọc cho bảng `50 000 000` dòng x `40` cột x `8 byte/ô` khi truy vấn chỉ cần `4` cột, theo hai kiểu lưu: theo hàng (đọc đủ `40` cột) và theo cột (chỉ đọc `4` cột), cùng tỉ lệ tiết kiệm (%).

Định dạng đầu ra (3 dòng):
`row_scan_gb=<1 chữ số>`
`col_scan_gb=<1 chữ số>`
`io_saved_pct=<1 chữ số>%`

Chấm tự động:
```bash
bash labs/cham.sh DEN L00 duong_dan/bai_cua_ban.py
```
