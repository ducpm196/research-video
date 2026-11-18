# Lab BNX L11 — Đọc BIC, kiểm IBAN bằng phép chia 97 và tính ba cách chịu phí (không cần mạng)

Viết `mau.py` (Python 3, chỉ thư viện chuẩn), in đúng năm dòng như `mong_doi.txt`. Số liệu là số minh hoạ, không phải tỉ giá hay biểu phí của ngân hàng nào.

1. BIC `ABCDDEFFXXX`: in `BIC ABCDDEFFXXX: to chuc <4 ký tự>, quoc gia <2>, dia diem <2>, chi nhanh <3 ký tự>` (không có chi nhánh thì in `-`).
2. IBAN `GB90BANK98765432101234` và bản đổi chỗ hai ký tự cuối: đưa 4 ký tự đầu ra cuối, đổi mỗi chữ thành số (A = 10, …, Z = 35, chữ số giữ nguyên), chia 97 lấy dư. In `<IBAN>: du <r> -> hop le` nếu r = 1, ngược lại `khong hop le`.
3. Chuyển 2 000 USD, phí ngân hàng gửi 8, phí trung gian 12: in `nguoi nhan: OUR <số> SHA <số> BEN <số>` rồi `nguoi gui tra: OUR <số>`.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L11 mau.py`.
