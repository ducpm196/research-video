# Lab BNX L09 — Thùng ảo của một khoá và ghi có dấu phiên bản CAS (kho mô phỏng bằng Python, không cần Couchbase)

Viết `mau.py` (Python 3, chỉ thư viện chuẩn), in đúng năm dòng như `mong_doi.txt`:

1. Khoá `session::s77`: `r = (zlib.crc32(khoa.encode()) >> 16) & 0x7FFF`. In `thung ao (1024): <r % 1024> | (128): <r % 128>`.
2. Hồ sơ 300 điểm, CAS 4. Hàm `ghi(moi, cas_kem)`: nếu `cas_kem` khác CAS hiện tại thì trả `tu choi`; khớp thì lưu giá trị mới, tăng CAS thêm 1 và trả `ghi duoc, CAS moi = <số>`.
3. P1 (cộng 20) và P2 (trừ 50) cùng đọc (300, CAS 4) trước khi ai ghi. In `P1: <kết quả ghi>`, `P2: <kết quả ghi>`. Rồi P2 đọc lại giá trị và CAS hiện tại, trừ 50 lần nữa và ghi lần hai: in `P2 lan 2: <kết quả ghi>`.
4. In `cuoi: <giá trị> <CAS>`.

Đặt tên biến và hàm không dấu. Gợi ý cú pháp: `import zlib` nạp thư viện băm; `s.encode()` đổi chữ thành byte; `"... %d" % x` chèn số `x` vào chỗ `%d`; từ khoá `global` cho hàm sửa biến ngoài hàm. Số liệu là số minh hoạ, khác ví dụ trong bài. Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L09 mau.py`.
