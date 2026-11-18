# R8 DMS L00–L10 (lần đọc độc lập đầu tiên sau sửa, P1 chặt): 11/11 bài — ghi lại bởi người điều phối từ tin nhắn của reader (adda4d985f132bf3a)

## 1. Tóm tắt
MUST 0 (11/11). P1=2: 3/11 chắc+vừa (L00, L02, L09); tính cả yếu 0/11. Tổng 39 mục: 0 chắc, 10 vừa, 29 yếu. P8=2 11/11; P9=2 11/11; spec khớp 11/11; SRT khớp `say` 11/11 (kiểm văn bản, chưa nghe audio); lab `cham.sh` ĐÚNG 11/11; 276/276 `checks`; 14/14 chương trình trên màn hình chạy khớp; đáp án lab tính tay khớp. Mất gốc ĐỦ 10/11 (L06 GẦN). Không có số hiệu/điều pháp lý. 60+ khung hình đã xem: không tràn/đè/cắt (kể cả L01 — từng tràn); Hasse L08 đúng 7 cạnh. SHOULD 4.
Nhận định của reader: toàn bộ P1 yếu của DMS đến từ mã Python; bảng cách đọc phủ đủ `for`, `range`, `%`, `==`, `//`, `**`, `print`, `all/any`, `while`, `index`, `max`, `set/len`, các mục chắc+vừa nằm ở: câu lệnh `if` dạng câu lệnh (L03, L05, L07, L08), hàm tự định nghĩa (L04, L10), cú pháp chỉ ở de.md (L01 `repeat=n`; L06 `combinations`, từ điển; L10 `math`/`combinations`/lưới số), "nhị phân" (L06).

## 2. SHOULD (4)
| Bài | Cảnh | Trích | Vấn đề | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L01 | practice.3 | "Ba chỗ cú pháp mới đã giải thích kèm ví dụ trong de.md: import, repeat=n và dấu *" | lời đọc chỉ đọc import và `*`, không đọc `repeat=n` | đọc thêm hoặc bỏ khỏi màn hình | CONFIRMED |
| L03 | quymo.2 | `print(n, 'so: da thu', dem, 'cap, deu chan')` | nhãn 'deu chan' viết cứng; `dem` chỉ đếm cặp tổng chẵn, không so với tổng số cặp | đếm cả cặp tổng lẻ hoặc in `n_le*n_le` cạnh `dem` | PLAUSIBLE |
| L03 | contradiction.1 | "số không thuộc ℚ gọi là số vô tỉ" | thiếu điều kiện số thực, ℝ chưa nhắc | thêm "số thực" | PLAUSIBLE |
| L09 | quymo.3, quymo.4 | màn hình "2 ngay" so với bảng "khoảng 2,5 ngày" và lời đọc "khoảng hai ngày rưỡi" | `62^8 // 10^9 // 86400` cắt xuống 2; giá trị thật 2,527 ngày | đổi chữ trên màn hình/lời đọc thành "hơn hai ngày" hoặc in phần lẻ | CONFIRMED |

## 3. Mục chắc+vừa (10)
| # | Bài | Cảnh/step | Trích | Loại | Lý do vừa | Bảng phủ? |
|---|---|---|---|---|---|---|
| 1 | L01 | practice.3 | `product((True, False), repeat=n)` | M | `repeat=n` chỉ ở de.md | không |
| 2 | L03 | quymo.2 | `if (a + b) % 2 == 0:` | B | giảng ở L02; bảng L03 chỉ có `%`, `==`, `for`, `range` | không |
| 3 | L04 | practice.1, .3 | "viết hàm tong(n) … hàm ct(n)" | B | `def` chỉ ở L01 | không |
| 4 | L05 | quymo.3 | `if x % 2 == 0 or x % 3 == 0:` | B | bảng có `%`, `==`, `or`, không có `if` | một phần |
| 5 | L06 | practice.3 | `{1: 'a', 2: 'b'}.values()`, "từ điển f" | A | ví dụ ở cột cho thấy kết quả | một phần |
| 6 | L06 | practice.3 | `combinations` từ `itertools` | M | chi tiết ở de.md | không |
| 7 | L06 | quymo.2 | "32 chữ số nhị phân" | A | kèm "hơn 4 tỉ", "2 mũ 32" | một phần |
| 8 | L07 | quymo.3 | `if a % 3 == b % 3 and … and a % 3 != c % 3:` | B | bảng giảng `and`, `!=` | một phần |
| 9 | L08 | quymo.4 | `if hang.index(1) < hang.index(2) and …:` | B | bảng có `index`, `<`, `and`, không có `if` | một phần |
| 10 | L10 | practice.1 | "hàm pascal(n)" (tự viết hàm) | B | `def`/`return` chỉ ở L01 | không |
Yếu (29): `for` lồng nhau, "biến" (L00); `break`, `if (!(…)) chan();`, "32 bit", "xác suất 2 phần 2^32" (L01); `#`, `{1, 2, 3}`, `x²`, "hữu hạn/vô hạn", "lồng nhau" (L02); "số hạng", "thừa số", "thương" (L03); "hằng đẳng thức", "lấy n nhỏ nhất", "quy đồng mẫu 2" (L04); `{1, 2} | {2, 3}`, "dùng dãy" (L05); "hằng số lớn chọn sẵn", `f: ℤ → ℤ` (L06); `R(a, b)`, "gom cụm", "đẳng thức" (L07); bộ `(1, 2, 3)` (L08); "chuỗi", `from itertools import …` (L09); "khai triển", `from math import factorial`, `hang = [1]` (L10).

## 4. Người học kẹt ở đâu
L01 practice.3 `repeat=n`; L02 example.1 `all(… for …)` và `#` (nhẹ); L03 quymo.2 `if`; L04 practice.1 viết hàm; L05 quymo.3 `if`; L06 quymo.2 "nhị phân" rồi practice.3 từ điển, `combinations`; L07 quymo.3 `if`; L08 quymo.4 `if`; L10 practice.1 viết hàm, practice.3 cú pháp ở de.md; L00 và L09 không kẹt.
