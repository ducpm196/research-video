# Lab CS112 L17 — Xếp lịch hội trường: ba tiêu chí và vét cạn

Cần: Python 3.11 trở lên. Tạo `lich.py` (số liệu minh hoạ, khác ví dụ trong bài). Chín sự kiện đánh số từ 1, mỗi sự kiện là `(s, f)` = (giờ bắt đầu, giờ kết thúc); hai sự kiện không chồng giờ khi `f` của cái trước `<= s` của cái sau:

`(6, 8), (4, 9), (1, 3), (10, 12), (3, 6), (0, 5), (6, 13), (6, 11), (1, 7)`

Viết hàm `chon(ds, khoa)`: sắp chỉ số các sự kiện bằng `sorted(range(len(ds)), key=khoa)` (sắp ổn định: hai sự kiện cùng khoá giữ thứ tự ban đầu), rồi duyệt, chọn sự kiện nếu `s >= last` (`last` ban đầu `-1`), trả về danh sách số hiệu (từ 1) đã chọn theo thứ tự duyệt. Rồi in:

1. `Chon theo ket thuc som nhat: ` và danh sách số hiệu, cách nhau một dấu cách (khoá: giờ kết thúc);
2. `So su kien: ` số sự kiện đã chọn;
3. `Bat dau som nhat: <số>, ngan nhat: <số>, vet can: <số>`: số sự kiện chọn được theo khoá giờ bắt đầu, theo khoá độ dài `f - s`, và số lớn nhất tìm bằng vét cạn (thử mọi tập con bằng `itertools.combinations`, giảm dần kích thước tới khi có tập không chồng giờ);
4. `Tham lam = vet can: CO` nếu kết thúc sớm nhất bằng số của vét cạn, ngược lại `KHONG`.

Cú pháp cần dùng (nếu chưa gặp): `key=` là hàm cho mỗi phần tử một "khoá" để sắp; `lambda i: ds[i][1]` là hàm nhỏ trả về giờ kết thúc của sự kiện số `i`. Ví dụ `sorted([0, 1, 2], key=lambda i: [5, 9, 7][i])` ra `[0, 2, 1]` (các khoá 5, 7, 9 tăng dần). `from itertools import combinations` rồi `list(combinations([1, 2, 3], 2))` ra `[(1, 2), (1, 3), (2, 3)]`.

Chạy: `python lich.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L17 lich.py`.
