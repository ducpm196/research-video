# Dự án PRJ L06 — Sổ nhật ký HMAC-SHA256 & chỉ mục SQLite

Đọc từ luồng chuẩn (`stdin`) 3 dòng dạng `khoá=giá trị`:
- Dòng 1: `key=<khoá_bí_mật>`
- Dòng 2: `msg=<nội_dung_bản_ghi>`
- Dòng 3: `probe=<chuỗi_tấn_công_SQL>`

Yêu cầu chương trình Python:
1. Tạo bảng SQLite trong bộ nhớ `log(id INT PRIMARY KEY, m TEXT, mac TEXT)` và tạo chỉ mục `CREATE INDEX idx_m ON log(m)`.
2. Tính mã xác thực `HMAC-SHA256` ở dạng chuỗi thập lục phân thường (`hexdigest()`) cho `msg` với khoá `key`, rồi chèn `(1, msg, mac)` bằng câu lệnh tham số hoá `?`.
3. Thực thi truy vấn tham số hoá `SELECT * FROM log WHERE m=?` với đối số `probe` để xác minh không bị khớp nhầm (`sqli_blocked=1` khi số dòng trả về bằng 0, ngược lại `0`).
4. Đọc lại `(m, mac)` ở `id=1` và dùng `hmac.compare_digest` kiểm tra toàn vẹn (`hmac_verified=1` khi hợp lệ).

In đúng 3 dòng theo định dạng:
```
mac_len=<độ_dài_chuỗi_hexa>
sqli_blocked=<0_hoặc_1>
hmac_verified=<0_hoặc_1>
```

Chấm tự động:
```bash
bash labs/cham.sh PRJ L06 duong_dan/bai_cua_ban.py
```
