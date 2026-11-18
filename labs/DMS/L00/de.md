# Lab DMS L00 — Lập bảng chân trị bằng chương trình

Viết `bang.py` (Python 3.11 trở lên) rồi chạy trong Git Bash bằng `python bang.py`.

Biểu thức cần lập bảng: **(p và không q) hoặc r**. Trong Python viết `(p and not q) or r`.

In đúng ba phần, giá trị đúng viết **1**, sai viết **0**, các số cách nhau một dấu cách:
1. Dòng đầu: `p q r kq`
2. Tám dòng, mỗi dòng là giá trị của p, q, r rồi kết quả `kq`. Thứ tự dòng: p đổi chậm nhất, r đổi nhanh nhất; dòng đầu là `1 1 1 ...`, dòng cuối là `0 0 0 ...`.
3. Dòng cuối: `so dong dung: N` với N là số dòng có `kq` bằng 1.

Gợi ý: ba vòng `for` lồng nhau, mỗi vòng chạy trên `(1, 0)`; `int(True)` bằng 1 và `int(False)` bằng 0.

Chấm: `bash labs/cham.sh DMS L00 bang.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
