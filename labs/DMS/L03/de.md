# Lab DMS L03 — Ví dụ không phải chứng minh: tìm phản ví dụ nhỏ nhất bằng chương trình

Viết `phanvidu.py` (Python 3.11 trở lên); chạy: `python phanvidu.py`.

Ba biểu thức sau cho ra số nguyên tố ở nhiều giá trị n đầu tiên (n = 0, 1, 2, ...), nhưng khẳng định "với mọi n tự nhiên, biểu thức là số nguyên tố" là SAI:

1. `n*n + n + 17`
2. `2*n*n + 29`
3. `n*n - 79*n + 1601`

Với mỗi biểu thức, tìm n nhỏ nhất làm giá trị KHÔNG phải số nguyên tố (giá trị lớn hơn 1 chỉ chia hết cho 1 và chính nó mới là nguyên tố), rồi in một dòng:

`<số thứ tự>: n=<n>, <giá trị> = <ước nhỏ nhất lớn hơn 1> x <thương>`

Ví dụ định dạng: `9: n=3, 45 = 3 x 15`.

Gợi ý: thử chia cho d = 2, 3, 4, ... cho tới khi `giá trị % d == 0`; vòng `for n in range(...)` bên ngoài, `break` khi gặp phản ví dụ đầu tiên.

Chấm: `bash labs/cham.sh DMS L03 phanvidu.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
