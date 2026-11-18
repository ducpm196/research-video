# Lab DMS L20 — Tính lại các con số của hành trình hàm băm bằng chương trình

Viết `hambam.py` (Python 3.11 trở lên); chạy: `python hambam.py`.

Giả định máy thử một tỉ (10^9) lần mỗi giây (số minh hoạ). In đúng sáu dòng (không dấu):
1. `2^80 = <số nguyên đầy đủ>` — số lần thử vét cạn kiểu ngày sinh cho hàm băm 160 bit (`2 ** 80`)
2. `2^64 lan thu o 1e9 lan moi giay: <số> nam` — số năm (một năm = 31 536 000 giây), làm tròn số nguyên (`round`)
3. `nhanh hon vet can (2^80 / 2^61): <số> lan` — tỉ số `2 ** 80 // 2 ** 61`, cho một tấn công giả định cần `2^61` phép tính
4. `1000000 tep, ma 32 bit: ky vong cap trung gia <số>` — kỳ vọng số cặp tệp trùng mã băm do ngẫu nhiên: `C(1000000, 2) / 2**32`, làm tròn 1 chữ số thập phân
5. `1000000 tep, ma 64 bit: ky vong cap trung gia <số>` — như trên với 64 bit, in bằng định dạng khoa học một chữ số thập phân: `'%.1e' % giá_trị`
6. `ma bang bit can de vet can ngay sinh >= 2^100: <số>` — số bit n nhỏ nhất sao cho `2 ** (n / 2)` đạt ít nhất `2 ** 100` (duyệt n = 1, 2, 3, ...)

Chấm: `bash labs/cham.sh DMS L20 hambam.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
