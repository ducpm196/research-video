# Lab PRJ L02 (Đạt / Chưa đạt theo `labs/PRJ/SPEC.md`) — Cổng bảo mật JWT, khử trùng `Idempotency-Key` & phân trang con trỏ

Mở rộng phần cổng bảo mật, lũy đẳng và truy vấn từ khoá `SPB`. Đọc dữ liệu động từ `stdin`:
- Dòng 1: `NOW=<epoch> SECRET=<khóa_hmac>`
- Các dòng `REQ <idem_key> <amount> <sub.exp.hmac_sha256_hex>`: kiểm tra chữ ký `HMAC-SHA256(SECRET, "sub.exp")` bằng so sánh thời gian hằng `hmac.compare_digest` và kiểm hạn `exp >= NOW`. Nếu sai chữ ký, sai định dạng, hoặc hết hạn → tăng `jwt_invalid`, không ghi giao dịch. Nếu hợp lệ → tăng `jwt_valid` và `INSERT OR IGNORE INTO idem(k, a)` trong SQLite.
- Dòng `IDS <N>`: tạo bảng `tx(id INTEGER PRIMARY KEY)` gồm các mã từ `1` đến `N` trong 1 giao dịch lô (`executemany`).
- Dòng `CURSOR <last_id> <limit>`: truy vấn `SELECT id FROM tx WHERE id > ? ORDER BY id LIMIT ?`.

Xuất đúng 3 dòng ra `stdout` (khớp `mong_doi.txt` với `du_lieu.txt` và toàn bộ các ca kiểm trong `ca_an/`):
1. `jwt_valid=<số_hợp_lệ> jwt_invalid=<số_lỗi>`
2. `executed=<số_giao_dịch_thực_hiện> total_amount=<tổng_tiền>` (lấy `0` nếu `executed=0`)
3. `cursor_page=<danh_sách_id_cách_nhau_dấu_phẩy>` (hoặc `none` nếu trang rỗng)

Mẫu kiểm thử công khai ở `labs/PRJ/L02/du_lieu.txt`. Chấm tự động:
```bash
bash labs/cham.sh PRJ L02 duong_dan/bai_cua_ban.py
```
