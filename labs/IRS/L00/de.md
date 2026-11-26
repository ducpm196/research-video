# Lab IRS L00 — Độ chuẩn xác P@k, độ phủ R@k và MRR

Đọc từ đầu vào chuẩn (`stdin`, dòng tham số dạng `khoá=giá_trị` cách nhau khoảng trắng) `total=<int> ra=<r1,r2,...> rb=<r1,r2,...> first=<f1,f2,...>` (trong đó `<int>` là số nguyên, danh sách cách nhau dấu phẩy). Tính `P@5`, `R@5`, `R@10` cho danh sách A (`ra`), `P@3` cho danh sách B (`rb`) và `MRR` cho danh sách vị trí đầu `first` (`0` nghĩa là không tìm thấy).

In 2 dòng đúng nhãn (`<.1f>` làm tròn 1 chữ số thập phân, `<.4f>` làm tròn 4 chữ số): `A_P5=<.1f> R5=<.1f> R10=<.1f> B_P3=<.1f>`, `MRR_3=<.4f>`.
Chấm tự động: `bash labs/cham.sh IRS L00 duong_dan/bai_cua_ban.py`
