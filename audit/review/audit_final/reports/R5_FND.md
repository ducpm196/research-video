# R5 FND (vòng 5, đọc độc lập bản dựng sau sửa, P1 chặt): 11/11 bài — ghi lại bởi người điều phối từ tin nhắn của reader (a38281a92370a88cd)

## 1. Tóm tắt (so với vòng 4: P1=2 2/11 → 7/11 chắc+vừa)
MUST 0 (11/11). P1=2: 7/11 chắc+vừa (L02, L03, L04, L06, L07, L08, L10); tính cả yếu 1/11 (L02). Số mục chưa giảng: 19 = 0 chắc + 4 vừa + 15 yếu. P8=2 11/11; P9=2 11/11; spec khớp 11/11; SRT khớp 11/11 (3133, 2066, 2082, 1971, 2270, 2290, 2001, 2266, 2300, 2165, 2296 từ); lab ĐÚNG 11/11 (L00, L08, L10 qua shim sqlite3); `checks` 173/173 và >40 số đo khớp; ~270 lệnh/đoạn mã chạy khớp (4 khác biệt không đổi nghĩa: `%h`/đường dẫn theo máy; `ls` không thêm `/`; lỗi UNIQUE của shim khác CLI; Python 3.11 thêm `^^^^`). Bảng "viết → đọc là" 25/28 đã mở: không tràn/đè/cắt chữ (chỉ gãy dòng cột 1 hẹp: `cp a / b`, `mv a / b` L02; `A && / B`, `A || / B`, `set - / e` L04; `khoa: / gia_tri` L06; `kill / $SV` L07). SHOULD 6 (+1 ghi nhận). Mất gốc ĐỦ 11/11.

## 2. SHOULD
| Bài | Cảnh | Trích | Vấn đề | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L02 | hook tiêu đề + step 2 | "Một dấu cách thừa xoá sạch cả thư mục" / "cả thư mục bị xoá sạch" | `rm * .txt` chỉ xoá tệp thường; chạy lại: thư mục vẫn còn, `ls` trống, tệp ẩn không bị chạm | "xoá sạch mọi tệp trong thư mục" | CONFIRMED |
| L05 | formula step 1 | bảng 3 hàng, hàng cuối "2 048 .. 65 535 / 3 byte" | bảng `sym` nói "1 đến 4 byte" nhưng bảng khuôn thiếu hàng 4 byte (65 536 .. 1 114 111, `11110xxx`; RFC 3629) | thêm hàng 4 byte hoặc nói "chỉ xét tới 3 byte" | CONFIRMED |
| L08 | example step 2 | `SET ten = 'An Le'` / `1|An Le|500000`; lời "đổi tên thành An Lê" | lệch dấu màn hình/lời đọc | đồng bộ | CONFIRMED |
| L04 | sym step 2 khung 00019 | ô cột 1 | cột hẹp làm gãy dòng `set -e` → "set -"/"e"; `A && B`; `A || B` | mở rộng cột 1 hoặc chống gãy | CONFIRMED |
| L09 | sym step 2 khung 00019 | "git branch git switch git merge" | ba lệnh dính liền một ô | tách dòng/thêm "," | CONFIRMED |
| Nhiều bài | L05 khung 00091, L06 00042, L08 00083 | ghi chú xám nhạt khi không focus | tương phản thấp khi lời đọc đang nói tới | tăng tương phản | PLAUSIBLE |
Ghi nhận: `MAX_PATH`=260 (L01) và Little 1961 (L07) NOT_VERIFIED; System Type, "Add python.exe to PATH", "Show more options" (L00) chưa kiểm vì máy không chạy trình cài; mỗi bài có đúng 1 câu cache cũ không ghi nguồn (`edge?`, cùng giọng NamMinh).

## 3. Mục chưa giảng (19): 4 vừa, 15 yếu
Vừa (SỬA BẮT BUỘC):
1. L00 caidat step 4 + kiemsh step 2–3: `java -version rồi javac -version`; `dat javac 21` — `javac` chỉ giảng ở pitfalls step 2, SAU lần xuất hiện đầu (M).
2. L01 formula step 3: "độ sâu chỗ đứng − độ sâu của thư mục chung", "(độ sâu 5)" — chưa nói cách đếm (A).
3. L05 example step 7 + pitfalls step 4: `System.out.println("x = " + x);` — nối chữ bằng `+` (A).
4. L09 practice step 1: `sed -i` đổi `ao 10` thành `ao 12` — L05 giảng, bài này không nhắc cách đọc (B).
Yếu (xử lý hết càng tốt):
- L00 kiemsh step 2 `"$1"`, `"$2"` nháy kép quanh biến.
- L03 example step 4 `sort -rn | head -n 1` cờ gộp (bảng chỉ `-n`, `-r` riêng).
- L04 practice step 3 `cut -d' ' -f1-2`, `cut -d. -f1` (L03 chỉ `-d,` `-f2`).
- L05 example step 1 `public static void main(String[] args)` chỉ bảo "chép nguyên"; example step 5 `sodu = 100`, `print(sodu_moi)`, `python loi.py` (Python chỉ giảng ở L06).
- L06 example step 3 `print(len(hang), tong)`; scale step 2 `head -n 1 a10k.csv` (L03, B); quiz step 2 `python -c "…` xuống dòng với dấu `>` tiếp dòng (chú thích chỉ ở L02, B).
- L07 example step 3 `curl -sf $U/khong_co` (`-s`+`-f`), `-w "%{http_code}\n"` (`\n`; B).
- L08 example step 1 `SELECT * FROM tai_khoan`, `COUNT(*)`; từ hook `sqlite3 $DB 'câu SQL'` (chỉ giảng dạng `< dung.sql`); `;` kết thúc câu SQL (chỉ có chú thích `;` của bash).
- L09 example step 2 `git commit -q -am '…'` (`-a`, `-m` riêng, `-am` gộp).
- L10 quiz step 2 `GROUP BY ngay ORDER BY t DESC LIMIT 1`, `AND`, `COUNT(*)` (L08, B).
Điểm chung: không bài nào dạy quy tắc "một dấu gạch + vài chữ = vài cờ" (`-rn`, `-sf`, `-am`); lời đọc không bao giờ gọi tên Python (chỉ "ngôn ngữ thứ hai").
Đã loại, không tính: `echo`, `sum`, `MAX`; đầu ra thuần; đoạn "khoảng 55 dòng Python, chép đúng, chưa cần hiểu" ở lab L07.

## 4. Người học kẹt ở đâu
L00 caidat step 4 "java -version rồi javac -version" (nhẹ); L01 formula step 3 "độ sâu 5 … lùi 5 − 3" (nhẹ); L02–L03 không kẹt; L04 practice step 3 `cut -d.` (cụt); L05 example step 5 `sodu = 100 / print(sodu_moi)` (nhẹ), step 7 `"x = " + x`; L06 example step 3 `print(len(hang), tong)` (nhẹ); L07 không kẹt; L08 example step 1 `SELECT *` (dấu `*` chưa nói rõ); L09 practice `sed -i` không nhắc; L10 quiz câu 2 cần nhớ L08.
