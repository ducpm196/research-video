# Lab CS112 L06 — Bảng băm dò tuyến tính và đống nhị phân

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Không cần cài thêm thư viện.

Cách tạo tệp: mở một **trình soạn thảo chữ thuần** (Notepad, VS Code; không dùng Word), gõ nội dung, lưu với tên `bam_dong.py` (đuôi `.py`, mã hoá UTF-8) vào **thư mục gốc của bộ khoá** (thư mục chứa `labs`), rồi mở Git Bash tại đó.

**Phần 1 — bảng băm dò tuyến tính, 11 ô.** Bảng là danh sách `[None] * 11` (`None` là ô trống). Số liệu minh hoạ, **khác ví dụ trong bài**.
- `chen_bang(bang, k)`: ô gốc là `k % 11`; khi ô đang có khoá thì thử ô kế tiếp `(o + 1) % 11`; ghi `k` vào ô trống đầu tiên gặp.
- `tim_bang(bang, k)`: đi như trên từ ô gốc, đếm số ô đã thử (ô gốc là lần thử 1); gặp `k` thì trả số lần thử; gặp ô trống thì trả **âm** số lần thử đã dùng (kể cả ô trống).
- Chèn lần lượt `18, 41, 22, 44, 59, 32`; in `bang: <11 ô cách nhau một dấu cách, ô trống in dấu chấm .>`; in `tim 44: thu <số> o`; in `tim 99: khong thay sau <số> o`.

**Phần 2 — đống lớn nhất.** Đếm chỉ số từ 0: con của ô `i` là `2*i + 1` và `2*i + 2`.
- `vun_xuong(a, i, n)`: trong mảng `a` có `n` phần tử, đổi ô `i` xuống: chọn con lớn hơn `c` trong hai con còn nằm trong mảng; nếu `a[i] >= a[c]` thì dừng, ngược lại đổi chỗ `a[i]` với `a[c]`, đặt `i = c`, đếm một lần đổi, lặp lại. Trả số lần đổi.
- Với `a = [4, 10, 3, 5, 1, 8, 7]`: dựng đống bằng cách gọi `vun_xuong` cho `i` từ `len(a) // 2 - 1` lùi về 0; in `dong: <mảng>` và `so lan doi cho: <tổng số lần đổi>`.
- Lấy phần tử lớn nhất ba lần (mỗi lần: ghi `a[0]` vào danh sách `ra`, chép phần tử cuối lên `a[0]`, bỏ phần tử cuối bằng `a.pop()`, rồi `vun_xuong(a, 0, len(a))`); in `lay ra 3 lan: <ba số>` và `con lai: <mảng>`.

Mọi danh sách in bằng `" ".join(map(str, danh_sach))`.

Chạy: `python bam_dong.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh CS112 L06 bam_dong.py`.
