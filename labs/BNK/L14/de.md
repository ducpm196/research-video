# Lab BNK L14 — Ba lần gửi, một lần ghi chuyển mạch

Khách A có số dư đầu **3 000 000**. Sổ ngân hàng ghi **ba** dòng trừ 800 000 (mã `r8`, `r8b`, `r8c`); sổ chuyển mạch chỉ ghi một dòng, mã `r8`.

Viết tệp `sua_sai.sql` (chạy bằng `python labs/sqlrun.py sua_sai.sql`, hoặc `sqlite3 :memory: < sua_sai.sql`):
1. Tạo hai bảng `ngan_hang (ma TEXT, tk TEXT, tien INTEGER)` và `chuyen_mach (ma TEXT, tien INTEGER)`; chèn các dòng nói trên (ngân hàng: `-800000` mỗi dòng, tài khoản `'A'`; chuyển mạch: `('r8', 800000)`).
2. `SELECT` các mã có ở ngân hàng mà không có ở chuyển mạch, `ORDER BY ma`.
3. `SELECT 3000000 + SUM(tien) FROM ngan_hang;` (số dư trước khi sửa).
4. `INSERT INTO ngan_hang SELECT 'dao-' || ma, tk, -tien …` cho **đúng các mã thừa** (dùng lại điều kiện `NOT IN` ở bước 2).
5. Lại `SELECT 3000000 + SUM(tien) FROM ngan_hang;` (số dư sau khi sửa).

Chấm: `bash labs/cham.sh BNK L14 sua_sai.sql`.
