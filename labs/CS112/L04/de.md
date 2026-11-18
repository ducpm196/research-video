# Lab CS112 L04 — Ngoặc, hàng đợi vòng và biểu thức hậu tố

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Không cần cài thêm thư viện.

Cách tạo tệp: mở một **trình soạn thảo chữ thuần** (Notepad, VS Code; không dùng Word), gõ nội dung, lưu với tên `ngan_xep.py` (đuôi `.py`, mã hoá UTF-8) vào **thư mục gốc của bộ khoá** (thư mục chứa `labs`), rồi mở Git Bash tại đó.

Trong Python, một danh sách (`list`) dùng làm ngăn xếp: `ngan_xep = []`, đẩy vào bằng `ngan_xep.append(x)`, lấy ra ở đỉnh bằng `ngan_xep.pop()`, kiểm rỗng bằng `not ngan_xep`. Phép chia lấy dư viết là `%` (ví dụ `7 % 5` bằng `2`).

**Phần 1 — ngoặc.** Viết `hop_le(s)` kiểm một chuỗi chỉ gồm `(` `)` `[` `]` `{` `}` có hợp lệ không (gặp ngoặc mở thì đẩy vào; gặp ngoặc đóng thì lấy đỉnh ra, phải là ngoặc mở cùng loại, và nếu ngăn xếp rỗng là sai; hết chuỗi, ngăn xếp phải rỗng). Với mỗi chuỗi trong `("{[()]}", "([)]", "((", "())")` in một dòng: `<chuỗi>: hop le` hoặc `<chuỗi>: sai`.

**Phần 2 — hàng đợi vòng.** Viết lớp `HangDoiVong(max_o)`: mảng `o` gồm `max_o` ô (`[None] * max_o`), chỉ số `dau = 0`, `cuoi = max_o - 1`, `dem = 0`. `xep_vao(x)`: `cuoi = (cuoi + 1) % max_o`, ghi `x` vào `o[cuoi]`, tăng `dem`. `lay_ra()`: lấy `o[dau]`, `dau = (dau + 1) % max_o`, giảm `dem`, trả giá trị đã lấy. `noi_dung()`: danh sách các phần tử theo thứ tự từ đầu hàng, `[o[(dau + k) % max_o] for k in range(dem)]`. Dùng hàng 4 ô: xếp vào 10, 20, 30, 40; in `lay ra: <giá trị lấy ra>`; xếp vào 50; rồi in ba dòng `dau hang: <các phần tử cách nhau một dấu cách>`, `chi so cuoi: <cuoi>`, `so phan tu: <dem>`.

**Phần 3 — hậu tố.** Viết `hau_to(bieu_thuc)` tính biểu thức viết ngược: tách bằng `bieu_thuc.split()`; gặp số (`int(k)`) thì đẩy vào; gặp `+`, `-`, `*` thì lấy ra **b rồi a** (số lấy ra trước là toán hạng bên phải), đẩy `a` phép tính `b` vào; cuối cùng trả phần tử còn lại. In `hau to: <kết quả>` cho `"6 2 3 + * 4 -"`.

Chạy: `python ngan_xep.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh CS112 L04 ngan_xep.py`.
