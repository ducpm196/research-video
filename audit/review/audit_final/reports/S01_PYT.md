# S01 PYT: đã đọc 14/14 bài (L00–L13)

Ngày 2026-11-14. Cách làm: 4 người đọc độc lập (A: L00–L03, B: L04–L07, C: L08–L10, D: L11–L13), mỗi người đọc trọn YAML (`show`, `say`, quiz, Tự làm), mục giáo án, khung hình, chạy mọi mã trên màn hình bằng Python 3.11.9 (+3.13.5 cho đoạn có traceback/thông báo lỗi), tự đo thời gian/bộ nhớ, tự viết lab rồi chấm bằng `labs/cham.sh PYT <Lxx>`. Tổng hợp bởi người điều phối đọc; tôi đã kiểm lại trực tiếp trên YAML các MUST: L01 hook#1, L02 hook#0 (mã cụt), L03 pitfalls#0, ba chỗ "chục byte" (L06, L10, L13), L13 "sát giới hạn", và L13 "trung vị" (chỉ xuất hiện 6 lần trong L13, 0 lần ở L00–L12). Các phần A–D bên dưới nguyên văn từ từng người đọc (bảng chuẩn xác, độ sâu, lab, kẹt, số đã chạy, khung hình, 5 kiểm đặc biệt).

Chú ý chung: số tuyệt đối đo trên máy kiểm đang tải nặng (nhiều tác tử cùng chạy), chậm 2–10 lần số trong bài; chỉ so bậc và chiều. Video L00–L06, L08, L11, L13 cũ hơn YAML (đang dựng lại) — lỗi nội dung của L01/L02/L03 vẫn có mặt trong khung hình hiện có.

## Kết luận ngưỡng chốt: KHÔNG ĐẠT
| Ngưỡng | Yêu cầu | Thực đo | Kết quả |
|---|---|---|---|
| MUST | 0 | 15 (A 8, B 1, C 3, D 3) | KHÔNG đạt |
| P1 = 2 | ≥ 90% bài | 2/14 (L00, L02) = 14% | KHÔNG đạt |
| P8 = 2 | 100% | 14/14 | ĐẠT |
| P9 = 2 | (tham khảo) | 14/14 | đạt |
| Lab tự làm chấm ĐÚNG | | 13/14 lần đầu; L10 ra `5250000.0` (đề không nhắc `int()`), L13 lần đầu 8/10 (lỗi chuỗi `\n`) rồi ĐÚNG | |

## Danh sách MUST (15) — chi tiết bằng chứng ở phần A–D
| # | Bài | Chỗ | Tóm tắt |
|---|---|---|---|
| 1 | L01 | hook#1 | Mã dừng ở `for tien in giao_dich:` không thân vòng lặp mà có kết quả; chạy 3.11/3.13: `IndentationError` (đã kiểm YAML thô) |
| 2 | L01 | quiz#0/#2 | Đề "như bảng dưới" lúc dừng không có bảng; mã đáp án đổi chiều `>=` chứ không đổi thứ tự (gốc `lon`, đổi chỗ `lon`, mã đáp án `vua`) |
| 3 | L02 | hook#0 | Hai `def`, không `print`, mà hiện 3 dòng kết quả (chạy ra 0 dòng; đã kiểm YAML thô) |
| 4 | L02 | formula#3 | `type(tang)`, `f = tang` không định nghĩa ở đâu: NameError |
| 5 | L02 | scale#1 | Bảng "≈1 s vs ≈900 ms" (1,11×) mâu thuẫn "chậm hơn ≈1,5×"; tự đo 1,5–2,6× |
| 6 | L03 | formula#0/#3/#4 | `gd`, `xs` chưa gán: 7 câu `>>>` NameError (3.11, 3.13) |
| 7 | L03 | pitfalls#0 | Mã 1 `print` nhưng hiện 3 dòng kết quả (đã kiểm) |
| 8 | L03 | objectives[0] | Mục tiêu "sửa danh sách bằng chỉ số": cả bài không có `x[0] = ...` (E51) |
| 9 | L06 | hook#0 SAY + srt | "một trăm chín mươi chục byte mỗi đối tượng, chưa kể phần dữ liệu thật": sai số (1900) và sai ý (190 B đã gồm dữ liệu; tracemalloc 193,4 MB/10^6) (đã kiểm: cùng mẫu "N chục byte" ở L10, L13) |
| 10 | L09 | hook/scale/quiz | "nhanh gấp ≈ 30 lần" mâu thuẫn "hàng trăm lần" (đo 129–183×) |
| 11 | L09 | formula#3 | `x.mean()`, `x.std()` dùng `x` chưa định nghĩa (8 số 2,4,4,4,5,5,7,9 không hiện) |
| 12 | L10 | hook SAY | "một trăm bốn mươi chục byte mỗi dòng" (140 B/dòng, đo 137) (đã kiểm) |
| 13 | L13 | formula#0 SAY + srt | "chín mươi bốn chục byte mỗi dòng" (94,3 B/dòng đo được) (đã kiểm) |
| 14 | L13 | quiz#1 câu 1 | "A cần cỡ 5 GB nên sát giới hạn" (tệp 5 GB, máy 8 GB; bài tự nêu bộ nhớ ≈5× tệp ⇒ ≈25 GB, chắc chắn hết) (đã kiểm chữ) |
| 15 | L13 | objectives[0] | "Đo thời gian và bộ nhớ…": không bài nào L00–L13 dạy `perf_counter/timeit/tracemalloc/getsizeof` (grep 0) |

Gốc chung đề xuất: (i) quy tắc đọc số của TTS biến "94 B" thành "chín mươi bốn chục byte" — sửa cách ghi "94 byte" trong `say` (L06, L10, L13); (ii) nhiều khung hiện mã CỤT hoặc kết quả sao chép sang khung khác, và REPL dùng biến chưa gán (L01 hook, L02 hook/formula, L03 formula, L09 formula#3, L11 formula, L12 không hiện `phi_chuyen`, L13 không hiện `gd.csv`): thêm dòng gán/`print`/`import` vào khung; (iii) P1 thấp đồng loạt vì các từ: `in`/tập hợp, phương thức dấu chấm, `is`, `isinstance`, `pass`, `.loc`, "biên dịch", "ngoại suy", `datetime64`, `idxmax`, "trung vị", `tempfile`, pip/site-packages/`cut`.

## Bảng độ sâu tổng (14 bài)
Bài | sha16 | Phút | P1 P2 P3 P4 P5 P6 P7 | P8 | P9 | Tổng | Mất gốc
--- | --- | --- | --- | --- | --- | --- | ---
L00 | aaa073885b40d252 | 19,1 | 2 2 2 2 2 2 2 | 2 | 2 | 14 | ĐỦ
L01 | dd04e1dab0cd703f | 18,1 | 1 2 1 2 1 2 2 | 2 | 2 | 11 | GẦN
L02 | f040456f2ba0173b | 17,0 | 2 1 2 2 2 2 2 | 2 | 2 | 13 | ĐỦ (3 MUST)
L03 | 269cf4e7552a232f | 17,6 | 1 1 1 2 2 2 1 | 2 | 2 | 10 | GẦN
L04 | c26668f807e20fa2 | xem phần B | 1 2 1 2 2 2 2 | 2 | 2 | 12 | ĐỦ
L05 | 2d036ca84b71c352 | xem phần B | 1 2 2 2 2 2 2 | 2 | 2 | 13 | ĐỦ
L06 | 517568c66bd10c87 | xem phần B | 1 1 1 2 2 2 1 | 2 | 2 | 10 | GẦN (1 MUST)
L07 | 0fe508b424eeb1d3 | xem phần B | 1 2 2 2 2 2 2 | 2 | 2 | 13 | ĐỦ
L08 | 3c5500c4c814f96a | xem phần C | 1 1 1 1 1 2 2 | 2 | 2 | 9 | GẦN
L09 | 0a24443129857a91 | xem phần C | 1 1 1 2 2 2 2 | 2 | 2 | 11 | GẦN (2 MUST)
L10 | 65297603828a7a1c | xem phần C | 1 1 2 2 1 2 2 | 2 | 2 | 11 | GẦN (1 MUST)
L11 | 92948f46e6cb9c53 | xem phần D | 1 2 1 2 2 2 1 | 2 | 2 | 11 | GẦN
L12 | 9cce8b5914eb1bea | xem phần D | 1 1 1 2 2 2 2 | 2 | 2 | 11 | GẦN
L13 | 7e509027d5e4a219 | xem phần D | 0 1 2 1 1 2 1 | 2 | 2 | 8 | CHƯA (3 MUST)
Tất cả sha16 khớp danh sách giao. ĐỦ 4, GẦN 9, CHƯA 1.

## Năm kiểm đặc biệt (tổng hợp)
1. P1 (thuật ngữ giảng tại chỗ): chỉ L00 và L02 đạt 2; 12 bài còn lại có 1–2 từ (L13: 0, "trung vị" + `tempfile`). Không có khái niệm then chốt thiếu, trừ L13.
2. Cảnh Tự làm đủ để làm: 14/14 lab tự làm được; kẹt nhỏ ở L10 (`int()`), L13 (chuỗi `\n` trong `de.md`/hàm chấm chỉ in "CHUA (0/2)"), L08 trên macOS/Linux (`cham.sh PYT L08` cần thư mục `pyt`; thư mục thật là `labs/pyt`, có cả `labs/PYT`).
3. Cảnh quy mô: tự đo đúng bậc và chiều ở hầu hết (L00, L03 40/66 MB, L04 `(a+)+b` gấp đôi mỗi ký tự, L05 97 MB/26 KB, L06 193/153/161 MB, L10 137 B/dòng, L11 SVG 0,12/10,8/107,8 MB, L13 bộ nhớ ±3%). Sai: L02 (1 s/900 ms vs 1,5×), L09 (30× vs 129–183×), L07 hàng 1% (isdigit 1000 ms > 800 ms ở 0% trái cơ chế), L10 tỉ lệ category "2×→6×" (đo 7,5×, 7,6×), L08 cột "số gói 2/5/17" (đo 1/4/12, cộng pytest 17) và "thời gian tăng theo số thư viện" (không cộng dồn).
4. Python 3.11 vs 3.13: đầu ra mã chạy giống nhau, nhưng traceback khác dạng (3.13 chen `~^~`, thông báo csv dài hơn ở L08). L00 prereq#1 "dòng ngay trên" chỉ đúng 3.11; L04 step ghi chú 3.13 mới "chạy tệp .py thì giống video" sai (tệp cũng in dòng mã + `~^^^`); L07 `breakpoint()` dừng khác dòng giữa 3.11 và 3.13, không nói; L07 không có ghi chú 3.13 cho traceback `<stdin>`.
5. Giáo án ↔ video (E51): lệch ở L03 (mục tiêu "sửa bằng chỉ số"), L13 (mục tiêu "đo"), L06 (`example` giáo án "gấp nhiều lần bộ ba giá trị" nhưng đo 1,2×), L00 ("năm phép toán" vs 7 toán tử), L08/L11 (`covers` trỏ sai cảnh), L10 ("bốn cột" vs bảng 5 cột); còn lại mục tiêu có cảnh dạy.

## Nhận xét chung
- Chất lượng cơ chế và quy mô tốt, lab đều tự làm được và khớp `mong_doi.txt`; P8/P9 = 2 ở mọi bài.
- Lỗi lặp lại nhất: màn hình mã cụt, biến chưa gán trong cửa sổ gõ từng câu, kết quả dán nhầm khung (nhiều chỗ ở ít nhất 10 bài) — sửa theo mẫu một lần, chạy lại bằng REPL sạch.
- Lỗi đọc số ("N chục byte") ở L06/L10/L13 là lỗi hệ thống của cách viết `say`/TTS, nên quét toàn khoá và các khoá khác dùng "B" liền số.
- Ngưỡng MUST 0 và P1 ≥ 90% chưa đạt; L13 (CHƯA) cần sửa trước khi phát hành, cùng L09.
- Cần dựng lại video sau khi sửa YAML vì video hiện cũ hơn YAML ở ít nhất 9 bài.

---
# Phần A — L00–L03 (người đọc A)

Cách làm: đọc trọn YAML (qua bản rút gọn + dump HTML thô khi nghi ngờ), curriculum/pyt.yaml, covers; chạy mọi đoạn mã trên màn hình bằng Python 3.11.9 và 3.13.5 (script `partA/repl.py` chạy từng câu `>>>`, `partA/files.py` chạy từng chương trình); tự đo thời gian/bộ nhớ (`partA/m01.py`, `m02.py`, `extra.py`); tự viết lab, chấm bằng `cham.sh PYT <Lxx>`; mở khung hình. Máy đo đang tải nặng (nhiều tác tử chạy cùng lúc) nên số tuyệt đối chậm hơn 2-10 lần số bài nêu; chỉ so bậc và chiều.

Video so với YAML: mp4 dựng 2026-11-14 00:59-01:24, YAML sửa lúc 03:28-03:35 (video cũ hơn YAML về mốc giờ). Đối chiếu srt với `say`: 594/598 câu có mặt nguyên văn trong srt (4 câu chỉ khác vì srt cắt cụm sau dấu phẩy: L01 example#2, L02 example#0, L03 example#1, L03 quiz#2). Các lỗi MUST bên dưới có mặt TRONG khung hình video (đã xem), không chỉ trong YAML. `_frames.txt` L03 nhắc `00133.png`, `00134.png` nhưng thư mục `frames` chỉ có tới 00132 (L00/L01/L02 cũng nhắc khung cuối thêm 1 số; đây là cách ghép concat nên chỉ L03 có thể thiếu thật).

## (a) Bảng chuẩn xác

### L00
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Bằng chứng đã chạy | Đề xuất sửa |
|---|---|---|---|---|---|
| L00 | SHOULD | sym#2 (SAY), objectives[3], covers | Cảnh tên "Giải mã dấu nhắc, dấu bằng, dấu thăng và **bảy** phép toán"; SAY "Bảng cuối là **năm** phép toán số học"; mục tiêu "Tính bằng **năm** phép toán số học" | Bảng sym#2 liệt kê `+ - * / // % **` = 7 toán tử (đếm từ chính SHOW). Tên cảnh nói 7, lời + mục tiêu nói 5. Khung 00030 (sym) hiện tiêu đề "bảy phép toán". | Thống nhất một con số (7 toán tử, hoặc "năm nhóm phép toán"); sửa luôn mục tiêu giáo án |
| L00 | SHOULD | prereq#1 | SHOW `$ python -c "1/0" 2> loi.txt` ... "dòng cuối của thông báo nói lỗi gì"; SAY "máy in một thông báo nhiều dòng ... dòng ngay trên cho biết lỗi xảy ra ở dòng nào" | Dòng lệnh chuyển lỗi vào `loi.txt` nên màn hình không in thông báo nào (khung 00019: chỉ có `1`). Chạy `python -c "1/0"`: 3.11.9 dòng ngay trên cuối là `File "<string>", line 1, in <module>`; 3.13.5 dòng ngay trên cuối là `~^~` (trước đó `1/0`), dòng `File ... line 1` nằm cách 3 dòng. Với tệp chạy `python x.py` cả 3.11 và 3.13 cũng có dòng mã + `~^~` chen giữa. | Cho hiện thông báo thật (bỏ `2> loi.txt`, hoặc `cat loi.txt`) và nói "tìm dòng bắt đầu bằng File ..., line N" thay cho "dòng ngay trên" |
| L00 | SHOULD | pitfalls#2, scale#2, quiz#3, recap | "Làm tròn có quy tắc rõ ràng"; "tính rồi làm tròn một lần, với quy tắc rõ ràng" (lệnh `round`) | `round` của Python làm tròn về số chẵn khi đúng giữa: `round(0.5)=0`, `round(1.5)=2`, `round(2.5)=2`, `round(1050000.5)=1050000` (3.11 và 3.13 như nhau); `round(2.675, 2)=2.67`. Bài khuyên dùng `round` cho tiền mà không nói quy tắc này. | Thêm một câu: `round` làm tròn về chẵn ở điểm giữa; nếu nghiệp vụ cần "làm tròn lên từ .5" phải tự viết (tính toàn số nguyên như `(x*2+1)//2`) |
Các mục khác của L00: không phát hiện lỗi (54/54 câu `>>>` khớp trên 3.11 và 3.13; `lai.py`, `nhap.py`, `nhap_sai.py` khớp; mọi số trong hook/scale/pitfalls khớp).

### L01
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Bằng chứng đã chạy | Đề xuất sửa |
|---|---|---|---|---|---|
| L01 | MUST | hook#1 (khung 00004) | Mã trên màn hình dừng ở `for tien in giao_dich:` (không có thân vòng lặp), dưới là "Kết quả chạy Tong: 45750000 / So giao dich lon: 1"; SAY "Chương trình này đi qua năm giao dịch, cộng dồn tổng tiền và đếm số giao dịch lớn" | Chép đúng 4 dòng trên màn hình vào tệp, chạy 3.11 và 3.13: `IndentationError: expected an indented block after 'for' statement on line 4`, không in gì. Đúng loại lỗi bài dạy ở example#2. Kết quả hiện ra không thể do mã hiện ra sinh ra. | Hiện đủ thân vòng lặp (5 dòng như `tong.py` ở example#0) hoặc ghi "(rút gọn)" kèm đủ mã trong khung |
| L01 | MUST | quiz#0 (đề, khung 00116) và quiz#2 (đáp án) | Đề: "Đổi thứ tự hai nhánh đầu **như bảng dưới**: với `tien = 25000000` nhánh nào chạy?" (khung đề không có bảng/mã nào); mã chỉ hiện ở lúc chữa (quiz#2): `if tien >= 1000000: vua / elif tien >= 20000000: lon / else: nho` | (1) Trong lúc dừng 60 s người học không có mã để trả lời. (2) Mã ở quiz#2 không phải "đổi thứ tự hai nhánh đầu" của mã gốc: đổi chỗ hai nhánh gốc (`if tien<20000000: vua / elif tien<1000000: nho / else: lon`) cho `25000000 -> lon` và `500000 -> vua`; mã đáp án đổi chiều so sánh (`>=`) thay vì đổi thứ tự, cho `25000000 -> vua`. Chạy cả ba biến thể: gốc `lon`, đổi chỗ `lon`, mã đáp án `vua`. Kết luận "thứ tự nhánh quan trọng" đúng nhưng đề + mã tự mâu thuẫn. | Hiện mã đã đổi ngay trong đề (quiz#0) và gọi đúng tên: "đổi `<` thành `>=` và đảo thứ tự"; hoặc dùng mã đổi chỗ thật |
| L01 | SHOULD | scale#1 | "×1 000: 1 000 000 ≈ 100 ms", "×10 000: 10 000 000 ≈ 2 s"; kết "số lượt lặp tăng bao nhiêu lần thì thời gian tăng chừng đó" | Hai hàng liền nhau tăng ×10 số lượt nhưng ×20 thời gian (100 ms -> 2 s). Tự đo (script cấp mô-đun, máy tải): 1e6 = 0.21-0.57 s, 1e7 = 2.7-6.0 s (tỉ lệ 7-13 lần); 1e3 = 59 µs-2.3 ms. Chiều và bậc đúng, nhưng hàng 1e7 làm lệch đường thẳng. | Đo lại 1e7 (≈1 s nếu 1e6 = 100 ms) hoặc ghi "xấp xỉ" rõ hơn |
Các mục khác của L01: không phát hiện lỗi (18/18 câu `>>>` khớp; 12/13 chương trình khớp, 1 là hook#1 ở trên; 139 tháng khớp; bảng chạy tay khớp; 3 phút ngoại suy khớp 1e9×200 ns).

### L02
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Bằng chứng đã chạy | Đề xuất sửa |
|---|---|---|---|---|---|
| L02 | MUST | hook#0 (khung 00002) | Mã chỉ có hai `def` (không có dòng `print` nào); dưới "Kết quả chạy VAT: 200000 / Tong: 2200000 / Tong (8%): 2160000" | Chạy đúng mã hiện: không in gì (0 dòng). Ba dòng kết quả cần ba lệnh `print` có trong `ham.py` (example#0) nhưng không có ở hook. | Thêm ba dòng `print(...)` vào khung hook |
| L02 | MUST | formula#3 (khung 00051) | `>>> type(tang)` / `<class 'function'>`; SAY "Ta dán thêm nhãn f lên hàm tăng, và gọi qua nhãn mới vẫn cho sáu" | `tang` không được định nghĩa ở bất kỳ đâu trong bài (grep YAML), cũng không có `f = tang` hay `f(5)` trên màn hình. REPL mới: `NameError: name 'tang' is not defined` (3.11, 3.13). Lời nói mô tả hai bước màn hình không có. | Hiện `def tang(x): return x + 1`, `f = tang`, `f(5)`, rồi `type(tang)` |
| L02 | MUST | scale#1 (khung 00080) và SAY | Bảng: "×10 000 000: 10⁷  gọi qua hàm ≈ 1 s  viết thẳng ≈ 900 ms"; ô đánh đổi và SAY "hàm chậm hơn ≈ 1,5 lần ở 10⁷ lần gọi" | 1 s / 0,9 s = 1,11 lần, mâu thuẫn "1,5 lần" ngay trên cùng khung. Tự đo 1e7 lần: gọi hàm / viết thẳng = 1,46-2,2 lần (3.11: 6,49/2,93 s, 4,3/2,87 s trên 3.13; trong hàm 5,1/2,8 s). Hàng "viết thẳng ≈ 900 ms" sai chiều (sát với gọi hàm quá). Ngoài ra "10⁷ lần gọi hàm ≈ 1 s" nhanh hơn "10⁷ lượt cộng ≈ 2 s" của L01 trong khi gọi hàm luôn tốn hơn phép cộng thẳng. | Sửa hàng viết thẳng thành ≈ 650 ms (nếu giữ 1 s và 1,5×) hoặc đo lại cả hai cột và đồng bộ với L01 |
| L02 | SHOULD | formula#1 (và formula#0) | `>>> tong_tien(2000000)` ... `2200000` | Trong REPL mới: `NameError: name 'tong_tien' is not defined` (3 câu). Hàm chỉ có ở tệp `ham.py` của hook/example, bài không nói đã nhập sẵn hay `from ham import *`. | Thêm một dòng "Trong cửa sổ gõ từng câu, ta dán lại hai `def` rồi gọi" hoặc hiện `>>> from ham import tong_tien` |
| L02 | SHOULD | check#0 SAY / SHOW | "Hai cách khớp nhau, nên hàm đúng." | Khớp trên một giá trị (3) không chứng minh hàm đúng; khẳng định quá mức (hàm sai `x*2` vs `x+x` vẫn khớp...). | "nên ta tin hơn (chưa chứng minh)" |
Các mục khác của L02: không phát hiện lỗi (UnboundLocalError đúng văn bản 3.11+ ở cả 3.11 và 3.13; NameError, None, `18,3%`/`86,7%` khớp; lab khớp).

### L03
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Bằng chứng đã chạy | Đề xuất sửa |
|---|---|---|---|---|---|
| L03 | MUST | formula#0, formula#3, formula#4 (khung 00038) | `>>> gd[0]` `450000`; `>>> sorted(gd, key=lambda g: g[1])` `[('A02', 150000), ...]`; `>>> [x // 1000 for x in xs]` `[450, 12000, 800, 30000]` | `gd` và `xs` không được gán ở đâu trong bài (hiện ra chỉ qua chữ "450000, 12000000, 800000" trong lời giải thích; ở step 4 `gd` lại là danh sách bộ, `xs` chưa có giá trị). REPL mới 3.11 và 3.13: `NameError: name 'gd' is not defined` (3 câu step 1 + 2 câu step 4), `NameError: name 'xs' is not defined` (2 câu step 5) = 7 câu không chạy. | Mỗi step đầu thêm dòng gán: `>>> gd = [450000, 12000000, 800000]`, `>>> gd = [("A01", 500000), ("A02", 150000), ("A03", 900000)]`, `>>> xs = [450000, 12000000, 800000, 30000000]` |
| L03 | MUST | pitfalls#0 (khung 00087) | Mã 4 dòng ... `print(goc)`; kết quả hiện 3 dòng: `[100000, 200000, 300000]` / `[100000, 200000, 300000]` / `[100000, 200000, 300000, 400000]` | Chạy đúng 4 dòng trên màn hình: in **1** dòng `[100000, 200000, 300000]`. Hai dòng sau là kết quả của hai `print` ở formula#2 chép nhầm sang. | Chỉ hiện một dòng kết quả, hoặc thêm hai lệnh `print` thật |
| L03 | MUST | objectives[0], covers (obj 1 -> formula) | "Tạo, đọc và **sửa** danh sách bằng chỉ số, chỉ số âm, cắt lát và thêm phần tử" | Toàn bài không có một câu nào gán qua chỉ số (`x[0] = ...`); grep `\] =` chỉ ra duy nhất `dem[l] = ...` của từ điển. Chỉ có đọc (`gd[0]`), cắt lát, `append`. Giáo án hứa điều bài không dạy. | Thêm một ví dụ `x[0] = 999` ở formula (và nói "danh sách sửa được, bộ thì không") hoặc bỏ chữ "sửa ... bằng chỉ số" khỏi mục tiêu |
| L03 | SHOULD | formula#1 SAY (khung 00043 có phụ đề) | "Vì thế số phần tử của một lát **luôn** bằng chỉ số cuối trừ chỉ số đầu." | Sai khi chỉ số cuối vượt độ dài: `len([10,20,30,40,50][3:10]) = 2`, không phải 7. (Đúng khi 0 ≤ đầu ≤ cuối ≤ len.) | "bằng chỉ số cuối trừ chỉ số đầu, khi chỉ số cuối không vượt quá độ dài" |
| L03 | SHOULD | scale#0 (khung 00077) và SAY | Cột chênh "×1: 1 000 ... ≈ 50"; SAY "Nhân một nghìn lần hỏi, đó là khoảng mười phút" | 6 µs / 100 ns = 60, không phải 50. 700 ms × 1000 = 700 s = 11,7 phút. Tự đo 1000 phần tử: list/set = 62-189 lần; 1 triệu phần tử: 1,1-1,6·10⁵ lần (bài 7·10⁴): bậc và chiều đúng. | Ghi ≈ 60 và "khoảng mười hai phút" |
| L03 | SHOULD | intuition#0 SVG, SAY | "các khoá phải là giá trị không sửa được (chuỗi, số, **bộ được**; danh sách thì không)" | Bộ chứa danh sách không làm khoá được: `{(1,[2]):1}` -> `TypeError: unhashable type: 'list'` (3.11, 3.13). | "bộ chỉ được khi các phần tử bên trong cũng không sửa được" |
Các mục khác của L03: số bộ nhớ khớp (list 1 triệu số nguyên ≈ 40,0 MB, `set(range(10**6))` ≈ 65,5 MB bằng tracemalloc: trùng "40 MB / 66 MB"); 7/9 câu `>>>` còn lại khớp, các chương trình example/pitfalls#1/#2/formula#2 khớp.

## (b) Bảng độ sâu
Bài | sha16 | Phút | P1 P2 P3 P4 P5 P6 P7 | P8 | P9 | Tổng | Mất gốc | Cần biết trước | Chỗ thiếu chính
--- | --- | --- | --- | --- | --- | --- | --- | --- | ---
L00 | aaa073885b40d252 | 19,1 | 2 2 2 2 2 2 2 | 2 | 2 | 14 | ĐỦ | FND (cửa sổ lệnh, PATH, mã thoát, `2>`, trình soạn thảo); `type(x).__name__` (dấu chấm thuộc tính) ở gợi ý lab | prereq#1 không hiện lỗi; "năm"/"bảy" phép toán; `round` làm tròn về chẵn
L01 | dd04e1dab0cd703f | 18,1 | 1 2 1 2 1 2 2 | 2 | 2 | 11 | GẦN | toán tử `in` và bộ `("rut", "chuyen")` (pitfalls#1: SAY không nhắc `in`, chỉ màn hình) | hook#1 mã cụt; quiz câu 2 thiếu mã trong đề + mã không phải "đổi thứ tự"
L02 | f040456f2ba0173b | 17,0 | 2 1 2 2 2 2 2 | 2 | 2 | 13 | ĐỦ về điểm (nhưng có 3 MUST) | `VAT` (viết tắt hiện trên màn hình, lời chỉ nói "thuế giá trị gia tăng"); trạng thái REPL (`tong_tien`, `tang` chưa gán) | hook#0 thiếu `print`; formula#3 `tang`/`f` không hiện; scale#1 số 1 s vs 900 ms vs 1,5×
L03 | 269cf4e7552a232f | 17,6 | 1 1 1 2 2 2 1 | 2 | 2 | 10 | GẦN | cú pháp `x in tập_hợp` / `set(...)` (cả bài nói "hỏi có trong đó không" nhưng không có dòng mã nào); phương thức bằng dấu chấm (`.count`, `.remove`, `.get`, `.append`); `is` / "đối tượng" (pitfalls#0) | gd/xs chưa gán; "sửa bằng chỉ số" không dạy; tập hợp không có mã chạy thật; SVG khung 00032 chữ "12 000 000" sát mép ô

Ghi chú điểm: L01 P1=1 (`in`+bộ), P3=1 (hook cụt), P5=1 (đề câu 2 không có dữ liệu). L02 P2=1 (hai chỗ nhảy: REPL không gán, `tang`). L03 P1=1, P2=1, P3=1 (chữ SVG sát mép), P7=1 (mục tiêu 1 thiếu "sửa", mục tiêu 2 "bộ" chỉ định nghĩa suông). Chốt P1=2 ở 2/4 bài (L00, L02): dưới ngưỡng 90%. P8=2 ở 4/4. P9=2 ở 4/4.

## (c) Lab
Bài | tự làm được | thời gian | kẹt ở đâu | mong_doi khớp
--- | --- | --- | --- | ---
L00 | có (lần chạy đầu `ĐÚNG` bằng `cham.sh PYT L00`) | ước tính người học 8-12 phút (đề + gợi ý đủ; viết lại mất <2 phút) | không; chỉ phải tự đoán `type(lai).__name__` (có gợi ý trong đề, `__name__` chưa giảng) | khớp từng dòng
L01 | có (`ĐÚNG`) | 10-15 phút | không (đủ: `for`, `if/elif/else`, biến đếm đều dạy) | khớp
L02 | có (`ĐÚNG`) | 10-15 phút | không (`lambda` đã dạy, gợi ý "viết tên không ngoặc" cứu được lỗi hay gặp) | khớp
L03 | có (`ĐÚNG`) | 12-18 phút | không (đủ `dict.get`, `sorted(key=lambda)`, mở gói bộ); nếu chưa thấy mẫu `d[k] = d.get(k, 0) + v` thì kẹt, nhưng example#0 và gợi ý có | khớp
Sau khi mở `loi_giai.py`: lời giải gần như trùng bản tự lập (L00 thêm biến `lai_tron`; L01 đặt tên `dem_nho...`). Đề không mơ hồ khiến lời giải hợp lý khác bị chấm sai: đã thử cả hai kiểu ghi `So du goc` (`f"{so_du:,}"`) và đếm; không phát hiện lời giải hợp lý bị chấm sai. `labs/PYT` (viết hoa) tồn tại đúng như video nói.

## (d) Người học kẹt ở đâu
- L00: không kẹt cứng; kẹt nhẹ ở prereq#1 ("máy in một thông báo nhiều dòng" nhưng `2> loi.txt` làm màn hình trống) và gợi ý lab `type(lai).__name__`.
- L01: hook#1 ("for tien in giao_dich:" không có thân vòng lặp mà đã có kết quả) rồi quiz#0 câu 2 ("như bảng dưới" nhưng không có bảng khi dừng 60 s).
- L02: hook#0 (kết quả `VAT: 200000 ...` mà mã không có dòng in nào), rồi formula#3 ("type(tang)" `tang` chưa từng được định nghĩa) và formula#1 (`tong_tien(2000000)` trong cửa sổ gõ từng câu mới).
- L03: formula#0 (`>>> gd[0]` mà `gd` chưa gán), rồi pitfalls#0 (mã in 1 dòng, màn hình hiện 3 dòng); lỗi tập hợp: cả bài nói "tìm có/không" mà không có `in`.

## (e) Số đã tính lại / mã đã chạy / khung hình
- Câu `>>>` chạy trên cả 3.11.9 và 3.13.5: L00 54/54 khớp; L01 18/18; L02 9/13 (4 NameError: 3 `tong_tien` phụ thuộc hook, 1 `tang` hỏng thật); L03 7/16 theo script (còn 9 NameError: 7 `gd`/`xs` hỏng thật + 2 `loai` đã gán ở prereq#0 dạng khối không-REPL nên chấp nhận). Chương trình/tệp chạy: L00 3/3 (kể cả `lai.py` mã thoát 0, `python -c "1/0"` mã thoát 1); L01 12/13; L02 6/7; L03 6/7. Thông báo lỗi `IndentationError`, `NameError`, `UnboundLocalError`, `KeyError` đúng cả 3.11 và 3.13.
- Số tự tính lại: ~60 số/giá trị (lãi, chia dư, 2^53, 0,125, bảng chạy tay 450000..45750000, 139 tháng, 18,3 %/86,7 %, 2.160.000, 1.050.000, các số bài chuẩn lab); sai: 2 (scale#1 L02 1 s vs 900 ms vs 1,5×; L03 "≈ 50" vs 60 và "mười phút" vs 11,7 phút, hai cái sau chỉ lệch nhỏ). Đo thực nghiệm: tất cả đúng chiều; bậc độ lớn khớp (hệ số máy tải 2-10×); riêng L02 sai chiều tương đối như trên.
- Khung hình đã xem: L00: 00001, 00019, 00030, 00042, 00113, 00123, 00143, 00160 (không lỗi hiển thị; bảng, SVG, nút "Dừng video" đều đọc được). L01: 00004, 00009, 00039, 00049, 00054, 00100, 00116, 00120 (lỗi nội dung hook#1 và quiz#0 như trên; không có lỗi tràn chữ). L02: 00002, 00034, 00051, 00055, 00080, 00112, 00135 (lỗi nội dung hook#0 và formula#3; bảng scale đọc được). L03: 00004, 00032, 00038, 00043, 00077, 00081, 00087, 00090 (khung 00032: chữ "12 000 000" sát/chạm mép hai ô kề bên; khung 00087 lỗi nội dung pitfalls#0).

## (f) Kiểm đặc biệt
### L00
(1) Thuật ngữ: giảng tại chỗ đủ (dấu nhắc, gán, so sánh, chú thích, chuỗi, kiểu, hệ nhị phân, f-string). Từ kẹt: `__name__` ở gợi ý lab; `2>`, PATH, mã thoát, trình soạn thảo thuộc FND (cho phép).
(2) Cảnh Tự làm: đủ để làm (đề + công thức + gợi ý + `cham.sh`); tự giải 1 lần `ĐÚNG`.
(3) Cảnh quy mô: 3 mức (×1, ×10⁶, ×10¹⁵) tự đo đúng: `1+0.1-1=0.10000000000000009`, `1e6: 0.09999999997671694`, `1e15: 0.125`; đánh đổi nêu rõ.
(4) 3.11 vs 3.13: chỉ có prereq#1 (dòng ngay trên cuối) khác nhau, bài không nói (SHOULD trên).
(5) Mục tiêu giáo án ↔ video: 9/9 mục tiêu được dạy; chỉ lệch chữ "năm phép toán" (7 toán tử).
### L01
(1) Từ kẹt: `in` + bộ `("rut","chuyen")` (pitfalls#1); `list(...)` đã giải thích; "chuỗi không rỗng được coi là đúng" giải thích tại chỗ.
(2) Tự làm: đủ; tự giải 1 lần `ĐÚNG`. Quiz câu 2 thì thiếu mã trong đề (MUST).
(3) Quy mô: 3 mức + ngoại suy; tự đo cùng chiều và bậc (xem SHOULD về hàng 1e7).
(4) 3.11 vs 3.13: IndentationError cùng văn bản (3.10 trở xuống khác, bài nói "3.11 trở lên" ở lab); không khác.
(5) Mục tiêu ↔ video: 9/9 có cảnh dạy; mục tiêu 6 qua quiz#3.
### L02
(1) Từ kẹt: `VAT` (viết tắt) và trạng thái REPL; còn lại (đối số/tham số, None, toàn cục/cục bộ, lambda) giảng đủ.
(2) Tự làm: đủ; tự giải 1 lần `ĐÚNG`.
(3) Quy mô: bảng 3 mức bảo trì (18,3 %, 86,7 % tính lại đúng) + chi phí gọi hàm (số 1 s/900 ms/1,5× mâu thuẫn; tự đo tỉ lệ 1,5-2,6×).
(4) 3.11 vs 3.13: `UnboundLocalError: cannot access local variable ...` đúng cả hai (là văn bản 3.11+; 3.10 khác).
(5) Mục tiêu ↔ video: 8/8 có cảnh dạy.
### L03
(1) Từ kẹt: cú pháp `x in tập_hợp`/`set(...)`; phương thức dấu chấm (`.count`, `.remove`); `is`/"đối tượng"; "sao chép nông" nói qua loa; khoá không sửa được/băm.
(2) Tự làm: đủ; tự giải 1 lần `ĐÚNG`.
(3) Quy mô: 3 mức (1e3, 1e6, 1e8 ngoại suy) + bộ nhớ: tự đo trùng 40 MB / 66 MB, ratio 60-190 và 10⁵; bậc đúng.
(4) 3.11 vs 3.13: không khác (KeyError, danh sách suy ra, chuỗi lát).
(5) Mục tiêu ↔ video: 7/8 dạy được; mục tiêu 1 thiếu "sửa bằng chỉ số"; mục tiêu 2 "bộ" chỉ có định nghĩa, covers trỏ vào quiz (chỉ có quyết định danh sách-hay-tập hợp).

## Tóm tắt MUST/SHOULD
MUST (8): L01 hook#1 (mã cụt); L01 quiz#0/#2 (đề không có bảng + mã không phải "đổi thứ tự"); L02 hook#0 (kết quả không có `print`); L02 formula#3 (`tang`/`f`); L02 scale#1 (1 s/900 ms vs 1,5×); L03 formula#0/#3/#4 (`gd`, `xs` chưa gán); L03 pitfalls#0 (3 dòng kết quả cho 1 `print`); L03 mục tiêu "sửa bằng chỉ số" không dạy.
SHOULD (10): L00 "năm/bảy phép toán"; L00 prereq#1 che lỗi + "dòng ngay trên" 3.13; L00 `round` làm tròn về chẵn; L01 scale#1 hàng 1e7; L02 formula#1 REPL chưa định nghĩa; L02 check "nên hàm đúng"; L03 "luôn bằng chỉ số cuối trừ đầu"; L03 ≈50/≈10 phút; L03 "bộ được" làm khoá; L03 SVG chữ sát mép.
Ngưỡng: MUST 0 (không đạt: 8); P1=2 ở 2/4 bài (không đạt 90%); P8=2 ở 4/4 (đạt); P9=2 ở 4/4.

---
# Phần B (người đọc B)

Ghi chú chung. sha16 cả 4 YAML đúng giá trị mong đợi (L04 c26668f807e20fa2, L05 2d036ca84b71c352, L06 517568c66bd10c87, L07 0fe508b424eeb1d3).
Video so với YAML: L04, L05, L06 video CŨ HƠN YAML (video dựng 01:28–01:42 ngày 2026-11-14, YAML sửa 03:44–04:09). Video L04 không có step ghi chú traceback 3.13 (srt không có "mười ba"). L07 video mới hơn YAML. Các khung đã xem khớp chữ YAML ở mọi chỗ so được.
Cách chạy: Python 3.11.9 và 3.13.5, `PYTHONIOENCODING=utf-8`, thư mục tạm trong `partB/` (code: l04a.py, l04b.py, w05/t05.py, l05m.py, w06/t06.py, w06/m06.py, w07/t07.py, w07/m07.py, lab/*).

## L04 — Chuỗi và biểu thức chính quy

### (a) Bảng chuẩn xác
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Bằng chứng đã chạy | Đề xuất sửa |
|---|---|---|---|---|---|
| L04 | SHOULD | scale#0 (bảng + SAY), recap | "Mẫu tương đương không lồng lặp, a+b, tăng tuyến tính." | `re.compile(r"a+b").search("a"*n+"c")` (3.11.9, min của 5 lần): n=1000 → 2,3 ms; 2000 → 11 ms; 4000 → 78 ms; 8000 → 382 ms: tăng nhanh hơn tuyến tính (bậc hai trên chuỗi không khớp, vì `search` thử từng vị trí đầu). Ở 25–41 ký tự vẫn ~7 µs nên câu "vẫn gần như tức thì" đúng. | Đổi thành "không bùng nổ gấp đôi mỗi ký tự; ở chuỗi ngắn vẫn gần như tức thì" hoặc bỏ chữ "tuyến tính". |
| L04 | SHOULD | formula#1 (step ghi chú 3.13; chỉ có trong YAML) | "khi chạy tệp .py thì giống video. Nội dung lỗi giống nhau." | Chạy tệp `f4.py` (`s="chuyen"; s[0]="C"`) trên 3.11.9 VÀ 3.13.5: đều in `File "C:\...\f4.py", line 2, in <module>` + dòng mã `s[0] = "C"` + `~^^^`; video chỉ có `File "<stdin>", line 1, in <module>` không dòng mã. REPL 3.11 (`python -i`) giống video; REPL 3.13 giả lập `<python-input-1>` có dòng mã + `~^^^`. Dòng cuối `TypeError: 'str' object does not support item assignment` giống ở cả hai bản (phần "nội dung lỗi giống nhau" đúng). | Sửa: "Chạy tệp .py: thêm đường dẫn tệp, dòng mã và dấu ~^ ở mỗi tầng; dòng cuối giống video". |
| L04 | SHOULD | formula#0, #2, #3, #4 | `>>> s.upper()` / `>>> phan = dong.split(",")` / `>>> len(s)` / `>>> re.findall(r"\d+", dong)` | Gõ đúng chữ trên màn hình vào REPL sạch: `NameError: name 's' is not defined`. Màn hình không có `s = "chuyen"` (bước 1), `dong = "A01,chuyen,500000"` (bước 2), `s = "tiền"` (bước 3), `dong = "10:15 GD#A0731 chuyen 1250000 VND"` và `import re` (bước 4). Khi tự thêm các dòng này, mọi đầu ra khớp (chạy 3.11 và 3.13, giống hệt). | Thêm dòng gán biến/`import re` vào đầu mỗi khối. |

Đáp án quiz, lời giải, con số: không phát hiện lỗi (xem (e)).

### (b) Độ sâu
`L04 | c26668f807e20fa2 | 17,9 | P1=1 P2=2 P3=1 P4=2 P5=2 P6=2 P7=2 | P8=2 | P9=2 | Tổng 12 | ĐỦ | ký hiệu hex byte (`\xe1`, `e1 bb 81`), `.encode()/.decode()` (chỉ nói trong lời), `.group()` không đối số, biến `s`/`dong` chưa gán, `ms/ns` | P1: hex byte; P3: cơ chế "thử mọi cách chia chuỗi" của (a+)+b chỉ có chữ, không có hình; ô bảng `[\d.], ( … )` bị ngắt dòng xấu`

### (c) Lab
`L04 | có | ước 5 phút (viết 1 lần, chấm lần đầu) | không kẹt; dùng một mẫu `GD#(\w+) .*?([\d.]+) VND` gộp, đề cho mẫu `[\d.]+ VND` nên không mơ hồ | ĐÚNG (cham.sh pyt và PYT đều chạy; thư mục thật là labs/PYT)`. Đề đủ để tự làm. loi_giai.py dùng hai mẫu riêng, kết quả cùng; không có chỗ đề mơ hồ khiến lời giải hợp lý bị chấm sai.

### (d) Người học kẹt ở đâu
intuition#0 ("e1 bb 81 / 74 69 e1 bb 81 6e": byte viết dạng thập lục phân chưa giảng) rồi formula#0 `>>> s.upper()` (biến `s` chưa gán trên màn hình).

### (e) Đã tính lại / chạy
Mã: ~22 đoạn (hook 2, prereq 3, f-string 4, step 1–4, ví dụ nhat_ky.py, check, pitfalls 3, quiz 3, lab), 22/22 khớp bài nói/hiện, 3.11.9 và 3.13.5 cho đầu ra giống hệt (chỉ khác dòng phiên bản). Số: 2^6=64, 2^16=65536, 1250000×0,0725=90625.00, 1+1+3+1=6, 2+3+1+1=7, 500000+2000000=2500000, 1.250→1,25/1250 (7/7 khớp).
Số đo (3.11.9): `(a+)+b` trên "a"*n+"c": 17 ký tự 20 ms, 21 ký tự 264 ms, 25 ký tự 4,7 s (bài: 3 ms, 50 ms, 1 s). Máy này chậm hơn ~5–7 lần bài nêu, nhưng tỉ lệ 17→25 ký tự = 235 lần (bài: 333; 2^8=256) và gấp đôi mỗi ký tự: ĐÚNG bậc và chiều. 26 ký tự 12 s, 27 ký tự 41 s (3.13: 17 ký tự 42 ms, 25 ký tự 14,9 s, chậm hơn 3.11 ~3 lần, vẫn cùng quy luật). Mẫu tốt a+b 25 ký tự: 6,4–8 µs trên máy này (bài 800 ns; bậc khác do máy chậm, tỉ lệ xấu/tốt cùng ~10^6). Ngoại suy: 1 s × 2^6 = 64 s (≈1 phút), × 2^16 = 18,2 giờ (≈20 giờ): khớp.
Khung đã xem: frames/00000, 00033, 00038, 00044, 00047, 00088, 00097, 00115, 00143. Lỗi hiển thị: ô bảng `[\d.], ( … )` (00033) xuống dòng làm `)` rơi một mình; ngoài ra không chữ tràn/đè/cắt.

### (f) Kiểm đặc biệt
1. P1: kẹt ở hex byte (intuition#0, formula#3 `b'ti\xe1\xbb\x81n'`), `.encode/.decode` chỉ giải bằng lời, `.group()` không đối số; còn lại (import, nhóm, chuỗi thô, \d \w + * ? [], tham lam) giảng tại chỗ.
2. Tự làm: đủ (hai mẫu, 5 dòng, đáp án in sẵn, gợi ý "nếu kẹt").
3. Cảnh quy mô: đúng bậc và chiều (xem (e)); số đã gắn "đo trên máy kiểm, số minh hoạ"; riêng câu "a+b tăng tuyến tính" là SHOULD ở (a).
4. 3.11 vs 3.13: ghi chú YAML đúng về REPL (`<python-input-N>` + dòng mã) và đúng "nội dung lỗi giống nhau", nhưng sai ở "chạy tệp .py thì giống video" (SHOULD ở (a)). Video chưa có step này (video cũ).
5. Giáo án ↔ video: 7/7 mục tiêu có cảnh dạy; mục tiêu 1 "cắt, tìm, thay, tách, ghép": tách/ghép/thay/cắt lát có chạy; `find`, `startswith`, `strip` chỉ nằm trong bảng, không chạy lần nào (không tính lỗi). Ví dụ giáo án (17, 21, 25 ký tự; len('tiền')=4/6) khớp bài.

## L05 — Tệp: văn bản, CSV, JSON

### (a) Bảng chuẩn xác
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Bằng chứng đã chạy | Đề xuất sửa |
|---|---|---|---|---|---|
| L05 | SHOULD | hook SAY + tiêu đề; scale#0 SAY | "đọc cả tệp cần khoảng mười một tỉ byte, nhiều hơn bộ nhớ của hầu hết các máy" / tiêu đề "tệp 2,3 GB thì máy hết bộ nhớ" | Đo `read().split("\n")` 1 triệu dòng: đỉnh 97 MB (×100 ≈ 9,7 GB, cùng bậc với 11 GB). Nhưng máy cá nhân 16 GB (và máy chủ) đủ chỗ cho 11 GB; câu "hầu hết" thiếu điều kiện. | "nhiều hơn bộ nhớ của nhiều máy cá nhân (8 GB, 16 GB)"; tiêu đề: "có thể hết bộ nhớ". |
| L05 | SHOULD | formula#0 | "tệp có $24$ ký tự nhưng $31$ byte" | Trên Windows (máy này) `Path("ghi_chu.txt").stat().st_size` = 33 (xuống dòng ghi thành 2 byte `\r\n`); 31 chỉ là `len(noi_dung.encode("utf-8"))` của chuỗi đã đọc lại (text mode đổi `\r\n` về `\n`). Linux/macOS: 31. Lời nói bài cũng gọi "ba mươi mốt byte" của nội dung (đúng), nhưng màn hình nói "tệp có … 31 byte". | Đổi thành "nội dung có 31 byte (trên Windows tệp trên đĩa 33 byte vì xuống dòng là 2 byte)". |
| L05 | SHOULD | formula#2, example#3, check#0 | `with open("gd.csv", encoding="utf-8", newline="") as f:` | Chạy trong thư mục trống: `FileNotFoundError: [Errno 2] No such file or directory: 'gd.csv'`. Không step nào tạo hay hiện nội dung `gd.csv` (3 dòng A01 chuyen 500000 / A02 nap 2000000 / A03 rut 300000 phải suy từ đầu ra). Khi tự tạo đúng nội dung: đầu ra 3 chuỗi `str` + `Tong: 2800000` + `3 2800000` khớp. | Thêm một step hiện (hoặc ghi bằng `write_text`) nội dung gd.csv trước formula#2. |
| L05 | SHOULD | hook#0 bảng, scale#0 | "bộ nhớ khi đọc cả tệp một lần (đỉnh)" ≈ 110 MB | Nhãn không nói "rồi tách thành dòng": `f.read()` thuần ở 1 triệu dòng chỉ đỉnh 41 MB (2× tệp); 97 MB là `read().split("\n")`. Đúng bậc (đo 97 MB, bài 110 MB) nhưng nhãn mơ hồ. | Thêm "rồi tách thành danh sách dòng". |

### (b) Độ sâu
`L05 | 2d036ca84b71c352 | 16,9 | P1=1 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 | P8=2 | P9=2 | Tổng 13 | ĐỦ | `newline=""` (không nói lý do), `.stat().st_size`, `type(x).__name__`, `-c` và `2> tệp`/`$?` (FND), "đỉnh bộ nhớ" | P1: các chi tiết công cụ kể trên; step có `gd.csv` không hiện dữ liệu`

### (c) Lab
`L05 | có | ước 7 phút | không kẹt (de.md chép sẵn nội dung gd.csv, dùng write_text) | ĐÚNG`. Đề đủ; thiếu kiến thức đáng kể: chuỗi nhiều dòng để `write_text` (de.md cho sẵn, người học dùng `"\n"` được; bài chưa dạy ba nháy). Lời giải mẫu dùng `json.loads(read_text())`, của tôi dùng `json.load(f)`; cùng đầu ra, đề không mơ hồ.

### (d) Người học kẹt ở đâu
formula#2 (Bước 3 CSV): `open("gd.csv", ...)` chạy trên tệp chưa từng được tạo hay hiện nội dung trên màn hình.

### (e) Đã tính lại / chạy
Mã: ~24 đoạn (bước 1–4, ví dụ 1–4, check, pitfalls 3 (cả lệnh shell `PYTHONIOENCODING=cp1252 python -c ...` → mã thoát 1 + `UnicodeEncodeError`, trên 3.11 và 3.13), quiz, lab), 24/24 khớp; 3.13 giống hệt 3.11. Số: 24 ký tự/31 byte nội dung, 500000+2000000+300000=2800000, 6→2→`xyz`, 2000000+1=2000001: khớp.
Số đo bộ nhớ (tracemalloc, tệp 1 triệu dòng, 20,5 MB): đỉnh `read()+split` 97 MB (bài ≈110 MB); đọc từng dòng 26 KB (bài ≈26 KB, đúng cả hai quy mô: 10 000 dòng 0,97 MB / 26,8 KB so với bài 1,1 MB / 26 KB). Thời gian đọc cả tệp 1,33 s so với từng dòng 1,41 s (bài ≈800 ms cho cả hai): cùng cỡ, đúng chiều. Ngoại suy ×100: 9,7 GB (bài 11 GB) khớp bậc; tỉ số 110 MB/26 KB ≈ 4 200 lần ("hàng nghìn lần" ở giáo án: đúng).
Khung đã xem: 00000, 00022, 00028, 00054, 00070, 00084, 00131. Lỗi hiển thị: không.

### (f) Kiểm đặc biệt
1. P1: kẹt ở `newline=""` (chỉ ghi "mở tệp với newline=''"), `.stat().st_size` (SAY chỉ nói "kích thước"), `type(...).__name__`, các lệnh shell trong pitfalls#2 (`-c`, `2>`, `$?`, `tail | cut`; coi là kiến thức FND).
2. Tự làm: đủ (đề, kết quả mong đợi, gợi ý, lệnh chấm).
3. Cảnh quy mô: đúng bậc và chiều ở cả bộ nhớ và thời gian (xem (e)); chỉ có SHOULD về nhãn và "hầu hết các máy".
4. 3.11 vs 3.13: không có traceback trong bài; mọi đầu ra giống hệt hai bản. Không có điều gì cần ghi chú.
5. Giáo án ↔ video: 8/8 mục tiêu có cảnh dạy; ví dụ giáo án (24 ký tự/31 byte, 2 800 000, "gấp hàng nghìn lần") khớp.

## L06 — Lớp và đối tượng

### (a) Bảng chuẩn xác
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Bằng chứng đã chạy | Đề xuất sửa |
|---|---|---|---|---|---|
| L06 | MUST | hook#0 SAY (và L06.srt dòng 7) | "một trăm chín mươi triệu byte, tức khoảng một trăm chín mươi chục byte mỗi đối tượng, chưa kể phần dữ liệu thật" | (1) "một trăm chín mươi chục" = 1 900 byte, sai số (190 triệu / 1 triệu = 190 byte). (2) "chưa kể phần dữ liệu thật" sai và tự mâu thuẫn với scale#0 ("Đo bằng công cụ theo dõi bộ nhớ … (kể cả chuỗi và số bên trong)"). Đo tracemalloc, 3 thuộc tính (str, int, int dùng chung): 1 triệu đối tượng lớp thường = 193,4 MB (3.13: 185,4 MB) và phần str+int+ô danh sách riêng ≈ 105 B/đối tượng, tức 190 B ĐÃ gồm dữ liệu, riêng bộ khung ≈ 85–90 B. | "khoảng một trăm chín mươi byte mỗi đối tượng, đã tính cả chuỗi và số bên trong". |
| L06 | SHOULD | formula#0, example#0, example#2 (rồi `__repr__`) | `>>> a = TaiKhoan("A01", 100)` / `print(a.rut(2000000), a)` → `False TaiKhoan(A01, 1500000)` | Khai báo đầy đủ `class TaiKhoan` (có `__init__`, `nap`, `__repr__`) KHÔNG xuất hiện ở cảnh nào: sym chỉ có tiêu đề bảng, formula#2 chỉ có `rut`, pitfalls chỉ có bản rút gọn không có `__repr__`. Dòng in `TaiKhoan(A01, 1500000)` của example#0 đến từ `__repr__` mà mã chỉ xuất hiện trong gợi ý của practice#2. Tự dựng lại lớp từ mảnh: mọi đầu ra khớp. | Thêm một step hiện trọn `class TaiKhoan` (init, nap, rut, `__repr__`) trước formula#0. |
| L06 | SHOULD | formula#2 SAY; recap#0/#1 | "Nhờ vậy dữ liệu của đối tượng luôn hợp lệ, vì mọi thay đổi đều đi qua cửa này." / "không ai sửa số dư từ bên ngoài mà bỏ qua kiểm tra" | Python không cấm: `a = TK("A",100); a.so_du = -999; print(a.so_du)` → `-999`, không lỗi. | "…miễn là mọi người chỉ đổi qua phương thức (Python không ép; đây là quy ước)". |
| L06 | SHOULD | formula#1 | "Đối tượng thực chất là một từ điển thuộc tính" | Chính bài ở scale#0 dạy `__slots__`; `class S: __slots__=("a",)` rồi `S().__dict__` → `AttributeError: 'S' object has no attribute '__dict__'`. | "…thường là một từ điển thuộc tính (trừ lớp khai báo `__slots__`)". |
| L06 | SHOULD | giáo án `curriculum/pyt.yaml` L06 `example` ↔ scale#0 | "10^6 đối tượng chiếm bộ nhớ gấp nhiều lần bộ ba giá trị" | Bài (và đo): 190 MB so với 160 MB bộ ba = 1,2 lần (đo 193,4 vs 161,4 MB). "gấp nhiều lần" không đúng. | Sửa giáo án thành "hơn bộ ba giá trị khoảng 20% (190 MB so với 160 MB)". |

Đáp án quiz, lời giải lab, các số nạp/rút/lãi: không phát hiện lỗi.

### (b) Độ sâu
`L06 | 517568c66bd10c87 | 17,4 | P1=1 P2=1 P3=1 P4=2 P5=2 P6=2 P7=1 | P8=2 | P9=2 | Tổng 10 | GẦN | `isinstance` (formula#1, example#5), `pass` (pitfalls#0, #2; không giảng ở đâu trong khoá L00–L07), "thấu chi" (lab), cột "khai báo trước chỗ chứa" và "bộ ba" ở hook trước khi giảng | P2: không bao giờ hiện trọn lớp TaiKhoan; P3: nhãn "dựng" ở mũi tên dưới của hình bản vẽ bị gạch đè; P7: ví dụ giáo án "gấp nhiều lần" lệch bài`

### (c) Lab
`L06 | có | ước 6 phút | không kẹt (đề mô tả đủ nap/rut/__repr__ và cho sẵn đoạn thử; "thấu chi" tra được từ công thức `-thau_chi`) | ĐÚNG`. Lời giải mẫu trùng của tôi từng dòng; đề không mơ hồ. Thiếu kiến thức: không có (bài dạy đủ `__init__`, self, return, f-string), trừ việc phải tự ghép lớp đầy đủ từ mảnh.

### (d) Người học kẹt ở đâu
formula#0 `a = TaiKhoan("A01", 100)` / `a.nap(50)`: lớp `TaiKhoan` chưa từng hiện trọn trên màn hình; kế đó formula#1 `isinstance(a, TaiKhoan)` chưa giảng.

### (e) Đã tính lại / chạy
Mã: ~25 đoạn (formula 1–4, ví dụ 0–5, pitfalls 0–5, quiz, check, lab), 25/25 khớp bài hiện (3.11 và 3.13 giống hệt, kể cả thông báo `TaiKhoan.nap() takes 1 positional argument but 2 were given`). Số: 100+50+50=200, 1000000+500000−300000=1200000, 2000000×5//1000=10000 → 2010000: khớp.
Số đo bộ nhớ (tracemalloc, thuộc tính ma=str, so_du=int, han_muc=int): 100 000 đối tượng: lớp thường 19,3 MB / `__slots__` 15,3 MB / bộ ba 16,1 MB (bài 19/15/16); 1 000 000: 193,4 / 153,4 / 161,4 MB (bài 190/150/160). 3.13: 18,5/14,5/15,3 và 185,4/145,4/153,4 MB. Tức khớp bậc và chiều (slots < bộ ba < lớp thường). Ngoại suy ×100: 19 GB / 15 GB (khớp với 193/153 MB × 100).
Khung đã xem: 00000, 00026, 00031, 00034, 00044, 00076, 00092, 00133. Lỗi hiển thị: 00031 nhãn "dựng" của mũi tên thứ hai bị đường mũi tên cắt ngang (nhỏ); bảng hook trùng bảng scale#0 (lặp chủ ý).

### (f) Kiểm đặc biệt
1. P1: `isinstance`, `pass`, "thấu chi", hai tiêu đề cột ở hook trước khi giảng ("khai báo trước chỗ chứa", "bộ ba"). `super()`, `@dataclass`, `__repr__`, `self`, `==` vs `is`, kế thừa/hợp thành được giảng tại chỗ.
2. Tự làm: đủ (lab tự làm được, đề + mong đợi + gợi ý).
3. Cảnh quy mô: số đo đúng bậc và chiều (xem (e)); sai ở lời hook (MUST) và ở giáo án (SHOULD).
4. 3.11 vs 3.13: không có traceback `>>>`; thông báo `TypeError` 3.11 và 3.13 giống; `getsizeof` đối tượng khác nhau nhưng bài không dùng. Không cần ghi chú.
5. Giáo án ↔ video: 9/9 mục tiêu có cảnh; riêng ví dụ giáo án "gấp nhiều lần bộ ba" lệch 1,2 lần; `fix` thứ hai nhắc `__eq__` nhưng bài chỉ nói "viết thêm hàm so sánh" không nêu tên (không tính lỗi).

## L07 — Ngoại lệ và gỡ lỗi

### (a) Bảng chuẩn xác
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Bằng chứng đã chạy | Đề xuất sửa |
|---|---|---|---|---|---|
| L07 | SHOULD | scale#0 bảng dòng 1% | `1%: ≈ 600 ms (bắt lỗi), ≈ 1000 ms (kiểm tra trước)` và `0%: ≈ 800 ms (isdigit)` | `isdigit` làm ít việc hơn khi nhiều chuỗi hỏng (không gọi `int`), nên không thể tăng 800→1000 ms. Đo lại 1 triệu chuỗi (3.11.9): 0%: try 301 ms / isdigit 509 ms; 1%: try 454 / isdigit 393; 50%: try 1290 / isdigit 226 (3.13.5: 220/288; 176/238; 1114/648). Ở 0% và 50% chiều và bậc khớp bài (try rẻ khi hiếm, ~4–5× chậm hơn khi 50%; isdigit nhanh hơn ở 50%). Ở 1% chiều đảo theo bản Python. | Bỏ hàng 1% hoặc ghi "xấp xỉ nhau"; chỉ giữ hai đầu 0% và 50%. |
| L07 | SHOULD | check#0 SAY, scale#0 chú thích | "Hai cách phải phân loại giống nhau trên cùng dữ liệu … tổng hai cách luôn bằng nhau." / "hai cách luôn cho cùng tổng" | Chỉ đúng với chuỗi toàn chữ số: `"1.250.000".isdigit()` → `False` trong khi `doc_tien("1.250.000")` (formula#0) → 1250000; `"²".isdigit()` → `True` nhưng `int("²")` → ValueError. Dữ liệu đo 1 triệu chuỗi toàn số hoặc "abc": tổng bằng nhau (đã kiểm). | Thêm điều kiện "với chuỗi chỉ gồm chữ số 0–9 hoặc chữ cái". |
| L07 | SHOULD | sym#1 bảng breakpoint | "dừng chương trình tại dòng đó" | `x=5; breakpoint(); y=x*2; print(y)` với đầu vào `p x`, `n`, `p y`, `c`: 3.11.9 dừng ở dòng KẾ (`y = x * 2`, `p y` ngay lập tức báo lỗi nếu chưa chạy dòng đó), 3.13.5 dừng ở chính dòng `breakpoint()` (`p y` → `NameError` đến khi `n`). Khác biệt hai bản không được nói. (Bài không chạy `breakpoint()` lần nào.) | "dừng ngay sau/quanh dòng đó (bản 3.11 dừng ở dòng kế, 3.13 dừng ở chính dòng)", hoặc thêm một step chạy thử. |
| L07 | SHOULD | example#2, example#3 (traceback `>>>`) | `File "<stdin>", line 1, in <module>` | Không có ghi chú 3.13 như L04: trên 3.13 REPL gõ tay hiện `<python-input-N>` và dòng mã + `~^^^`. Ngoài ra traceback chính (hook, example#0) viết `File "…"` bỏ dòng mã và dấu `^`, trong khi chạy thật 3.11.9 và 3.13.5 đều in đường dẫn đầy đủ, dòng mã và dấu `~^^` (3.13 bỏ dấu ở tầng `trung_binh`). Số dòng 8, 5, 2 đúng với mã có dòng trống (đã chạy: line 8 `<module>`, line 5 `trung_binh`, line 2 `chia`). | Thêm một câu "bản của bạn còn in thêm dòng mã bên dưới mỗi `File …`; đọc từ dưới lên như cũ". |

Không có MUST ở L07: đáp án quiz, lời giải lab, mọi con số (150000, 300000, 20, −1, 3575000…) đã chạy khớp. `ZeroDivisionError: integer division or modulo by zero` ĐÚNG cho `//` ở cả 3.11.9 và 3.13.5.

### (b) Độ sâu
`L07 | 0fe508b424eeb1d3 | 17,2 | P1=1 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 | P8=2 | P9=2 | Tổng 13 | ĐỦ | `pass` (formula#2, pitfalls#1), tham số `logging.basicConfig(stream=sys.stdout, format="%(levelname)s %(message)s")` và `import sys`, pdb `p n c q` chỉ nằm trong bảng không chạy | P1: `pass`, định dạng log; điểm dừng chỉ nêu, không demo`

### (c) Lab
`L07 | có | ước 6 phút | không kẹt (đề cho sẵn tên lớp, thông báo in và hàm repr) | ĐÚNG`. Lời giải mẫu trùng của tôi; đề rõ về `repr` và thứ tự except; không mơ hồ.

### (d) Người học kẹt ở đâu
formula#2: `class SoDuKhongDu(Exception):` rồi dòng `pass` (chưa giảng); sớm hơn nhẹ là example#4 `logging.basicConfig(stream=sys.stdout, format="%(levelname)s %(message)s", …)` (tham số không giảng).

### (e) Đã tính lại / chạy
Mã: ~20 đoạn (hook, bước 1–4, ví dụ 0–4, check, pitfalls 0–2, quiz, lab, 6 thông báo lỗi `int('abc')`, `10 // 0`, `{'a':1}['b']`, `[1,2][5]`…), 20/20 khớp bài hiện; 3.13 giống hệt 3.11 ở mọi đầu ra chương trình và thông báo (khác chỉ ở dấu `^` trong traceback thật và breakpoint, đã ghi ở (a)). Số: 250000−100000=150000, 500000−200000=300000, 100//5=20, 3575000 = 2500000+75000+1000000 (lab): khớp.
Số đo (1 triệu chuỗi) xem hàng 1 ở (a): 0%: 301/509 ms (bài 600/800), 50%: 1290/226 ms (bài 3000/600). Chiều và bậc đúng ở 0% và 50%.
Khung đã xem: 00000, 00026, 00072, 00079, 00082, 00084, 00094, 00100. Lỗi hiển thị: không (hình 00026: các mũi tên của sơ đồ lỗi trồi lên hơi khó theo nhưng đọc được).

### (f) Kiểm đặc biệt
1. P1: `pass`; tham số `basicConfig`; `breakpoint()` và lệnh pdb chỉ nêu trong bảng. `try/except/finally/raise`, traceback, `isdigit`, `repr` được giảng tại chỗ.
2. Tự làm: đủ.
3. Cảnh quy mô: đúng chiều và bậc ở hai đầu 0% và 50% (xem (a) hàng 1 cho hàng 1%).
4. 3.11 vs 3.13: thông báo `ValueError`, `ZeroDivisionError`, `KeyError`, `IndexError` giống hệt hai bản (đã chạy). Khác ở dấu `^` của traceback thật, REPL 3.13, và vị trí dừng của `breakpoint()`: bài không nói (SHOULD ở (a)).
5. Giáo án ↔ video: 8/8 mục tiêu có cảnh dạy (điểm dừng chỉ ở mức nêu trong bảng, không chạy); ví dụ giáo án ('thieu 150000', "dong giao dich" hai lần, try đắt ở 50%) khớp.

---
## Tóm tắt phần B
- MUST: 1 (L06 hook#0: "một trăm chín mươi chục byte … chưa kể phần dữ liệu thật").
- P1 = 2 ở 0/4 bài (cả bốn đạt 1). P8 = 2 ở 4/4. P9 = 2 ở 4/4.
- Mất gốc: L04 ĐỦ (12), L05 ĐỦ (13), L06 GẦN (10), L07 ĐỦ (13).
- Video L04, L05, L06 cũ hơn YAML; L04 video chưa có step 3.13.

---
# Phần C (người đọc C)

Môi trường tự đo: Windows, Python 3.11.9 (hệ thống), 3.13.5 (py -3.13), numpy 2.4.6, pandas 3.1.1 (labs/.venv-pyt). Máy đo CHẬM và đang tải (python -c pass = 200-320 ms, nhiều tác tử chạy chung), nên số tuyệt đối khác, chỉ so bậc độ lớn và chiều.
sha16 lúc đọc đúng giá trị mong đợi cả ba bài: L08 3c5500c4c814f96a, L09 0a24443129857a91, L10 65297603828a7a1c. SRT khớp 100% câu `say` (135/135, 134/134, 129/129 câu, script sayvssrt.py). Video L09/L10 dựng sau lần sửa YAML cuối; mp4 L08 dựng 01:56, YAML L08 sửa lại 03:50 cùng ngày (cũ hơn YAML ~2 giờ nhưng lời đọc vẫn khớp, màn hình các khung đã xem khớp YAML).
Ghi chú kỹ thuật không phải lỗi: trong `_frames.txt`, khung giữ "pause" (L08 00103.png 62,9 s và 00117.png 422,9 s; L09 00102/00117; L10 00097/00111) xuất PNG nội dung của bước KẾ TIẾP (đáp án / kết quả mong đợi). Đã trích khung thật từ mp4 L08 (ffmpeg, t=560 s và t=800 s): trong lúc dừng màn hình hiển thị ĐỀ, không lộ đáp án. L09/L10 chưa trích mp4, cùng cơ chế.

## L08 — Mô-đun, gói và môi trường ảo

### (a) Chuẩn xác
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Bằng chứng đã chạy | Đề xuất sửa |
|---|---|---|---|---|---|
| L08 | SHOULD | scale#0 | "+ thư viện tính trên mảng \| 2 (kể cả thư viện nền)"; "+ thư viện bảng dữ liệu \| 5"; "+ thư viện vẽ biểu đồ \| 17 (bốn chính, mười ba kéo theo)" | importlib.metadata trong labs/.venv-pyt: numpy = 1 gói; numpy+pandas = 4 (numpy, pandas, python-dateutil, tzdata); thêm matplotlib = 12; thêm pytest = 17. Venv mới cài `pip install -r labs/requirements-py.txt` rồi `pip freeze` = đúng 17 dòng. Không có quy tắc đếm nào cho ra đồng thời 2/5/17 (kể cả pip thì 2/5/13/18). Dòng "vẽ biểu đồ = 17" thực ra gồm cả pytest. | Đổi 2→1, 5→4, dòng vẽ biểu đồ = 12 và thêm dòng "+ thư viện kiểm thử = 17" (hoặc đổi nhãn cột) |
| L08 | SHOULD | scale#0 + objective 6 | cột thời gian "≈ 100 ms, ≈ 400 ms, ≈ 1 s, ≈ 800 ms" dưới nhãn "+ ..." và tiêu đề cảnh "thời gian khởi động tăng theo" | Đo import một mình (subprocess, min của 5): pass 317 ms; numpy 1,6 s; pandas 5,7 s; matplotlib.pyplot 5,4 s; pytest 1,2 s; cả bốn một lượt 5,25 s (< pandas một mình vì pandas đã nạp numpy). Bậc/chiều từng thư viện khớp bảng (máy chậm 3-6 lần) nhưng số là thời gian TỪNG thư viện, không cộng dồn; dòng cuối (17 gói) nhanh hơn dòng trước (5 gói) nên không minh hoạ "tăng theo số thư viện". | Ghi rõ "mỗi thư viện nạp riêng" và bỏ dấu "+", hoặc đo cộng dồn; sửa tiêu đề cảnh (cũng đang cụt: "...tăng theo") |
| L08 | SHOULD | formula#1, sym#0 | "Vì ngan_hang có __init__.py, Python coi nó là gói và cho nạp ngan_hang.phi" | Xoá __init__.py, chạy `from ngan_hang2.phi import f` trên 3.11.9 và 3.13.5: vẫn chạy, in 1100 (gói không gian tên, PEP 420). Quan hệ "vì có __init__.py mới nạp được" sai; người học quên tệp này sẽ không gặp lỗi như bài ngầm báo. | Nói "__init__.py đánh dấu gói quy ước và chạy mã khởi tạo; từ Python 3.3 thiếu nó vẫn nạp được nhưng nên có" |
| L08 | SHOULD | recap#0, intuition#0 | "tên trùng thì che"; "tệp của bạn nằm ở mục đầu nên che mất bộ có sẵn" | Tạo sys.py, time.py, math.py cùng thư mục: `python -c "import sys,time,math"` vẫn cho mô-đun thật (sys.builtin_module_names chứa math, time, sys). Chỉ mô-đun viết bằng Python (csv, json, random...) bị che. | Thêm điều kiện "với các mô-đun thư viện chuẩn viết bằng Python" |
| L08 | SHOULD | pitfalls#0, example#3 | `... \| tail -n 1 \| cut -c1-58` rồi "Đọc dòng cuối" | Python 3.13.5: dòng cuối dài hơn: "AttributeError: module 'csv' has no attribute 'DictReader' (consider renaming '...\csv.py' since it has the same name as the standard library module named 'csv' and prevents importing that standard library module)"; `cut -c1-58` che mất gợi ý này. 3.11.9 đúng như bài. Bài không nói khác biệt. | Một câu: "từ Python 3.13 thông báo còn gợi ý đổi tên tệp"; giảng `cut` |
| L08 | SHOULD | formula#0-1, example#0, objective 1 | `$ python giao_dich.py` → "tu kiem: 300"; `$ python chay_goi.py` → "1100 5000 / 2000" | Mã của giao_dich.py, chay.py, ngan_hang/phi.py, chay_goi.py KHÔNG hiện ở đâu trong video/bài. Tôi phải tự dựng lại (ra đúng đầu ra, 13/13 lệnh khớp) nhưng người học không thể viết/nạp được mô-đun của chính mình từ cái họ thấy; dòng `from ngan_hang.phi import ...` cũng không hiện. `covers` gán mục tiêu 1 (chia mô-đun/gói và nạp bằng import) cho cảnh `example`, nơi không dạy điều đó. | Hiện nội dung 4 tệp (3-5 dòng mỗi tệp) trong formula#0-1; sửa covers 1 → formula |
| L08 | SHOULD (hiển thị) | intuition#0 | "1. thư mục của tệp đang chạy", "3. thư viện đã cài (site-packages)" | Khung 00026.png: chữ chạm/tràn viền ô (mục 3 vượt lề phải ô ~11 px) | Nới ô hoặc giảm chữ |

### (b) Độ sâu
`L08 | 3c5500c4c814f96a | 19,2 (trong đó 7 phút là thời gian dừng làm lab; 12,2 phút lời đọc) | P1=1 P2=1 P3=1 P4=1 P5=1 P6=2 P7=2 | P8=2 | P9=2 | Tổng 9 | GẦN | pip là gì/tải từ đâu (PyPI), site-packages, python -c và sys.prefix/sys.base_prefix (dùng ở formula#2 nhưng chỉ giải thích ở cảnh check sau đó), cut -c | Mã nguồn các mô-đun mẫu không hiện (P2/P4); thuật ngữ pip/site-packages; đáp án quiz một dòng`

### (c) Lab
`L08 | có (phần tạo venv + in_phien_ban.py) | ~2 phút viết + 3 phút 32 giây pip install thật (python -m venv .venv-hoc, pip install -r labs/requirements-py.txt: 17 gói, thư mục venv 248 MB) | không kẹt; de.md đủ; chỉ pip cần mạng | khớp: cham.sh pyt L08 in_phien_ban.py → ĐÚNG; chạy trong venv mới cho đúng 4 dòng matplotlib 3/numpy 2/pandas 3/pytest 9; pip freeze trong venv mới = 17 dòng == requirements-py.txt (sai lệch duy nhất là CRLF). loi_giai.py giống hệt cách tôi làm. Đề không mơ hồ.` (Lưu ý: de.md gọi `bash labs/cham.sh PYT L08` nhưng thư mục thật là labs/pyt; trên Windows không phân biệt hoa thường nên chạy được, trên macOS/Linux `PYT` sẽ báo "không có .../mong_doi.txt".)

### (d) Người học kẹt ở đâu
formula#0 (Bước 1) "$ python giao_dich.py → tu kiem: 300": họ không thấy tệp giao_dich.py viết gì nên không biết `__name__` được in từ dòng nào và 300/750000 từ đâu; kế đó sym#1/formula#2 `python -c "import sys; print(sys.prefix != sys.base_prefix)"` dùng trước khi giảng.

### (e) Số/mã đã tính lại
- Số: 17-4=13 ✓; 500000//1000=500<1100, 5000000//1000=5000, 2000000//1000=2000 ✓; 100 lần × ~1 s ≈ 100 s ≈ "2 phút" ✓ (theo chính số bảng); đếm gói 1/4/12/17 vs bài 2/5/17 ✗ (xem a); ghim numpy==2.4.6, pandas==3.1.1, 17 dòng ✓.
- Mã/lệnh chạy: 13 khối (giao_dich 2 lệnh, find, chay_goi, venv 3 lệnh, activate, khong_guard, csv.py 3 lệnh, pip install thật, in_phien_ban) → 13/13 khớp trên 3.11.9; 3.13.5: csv-shadow, __name__, venv, namespace → khớp trừ thông báo dài hơn (SHOULD ở trên). PS1 sau activate = "(.venv) " ✓.
- Khung đã xem: L08/frames 00000, 00026, 00038, 00052, 00077, 00102, 00103, 00104, 00116, 00117, 00118, 00130 + mp4 L08 t=560 s, t=800 s. Lỗi hiển thị: 00026 chữ chạm viền ô; 00077 tiêu đề cảnh cụt "...tăng theo".

### (f) 5 kiểm đặc biệt
1. P1: kẹt: pip (là gì, tải từ đâu), site-packages, sys.prefix/base_prefix & `-c` (giảng sau), `cut -c1-58`; `2>&1` đã có ở FND L04/L05. Tên bốn thư viện chính (matplotlib, pytest) chỉ lộ ra ở bài lab.
2. Practice/Tự làm đủ để làm: có (đề 4 bước + kết quả + hint); thiếu giải thích pip/PyPI nhưng lệnh chép được.
3. Cảnh quy mô: số/bậc xem (a): thời gian từng thư viện đúng bậc & chiều trên máy chậm gấp 3-6; số đếm gói lệch 1; đánh đổi (dung lượng "vài trăm MB" khớp: venv 248 MB) đúng.
4. 3.11 vs 3.13: đã chạy cả hai; khác biệt duy nhất: thông báo csv 3.13 dài hơn (chưa nói trong bài); venv/activate/__name__ giống nhau.
5. Mục tiêu giáo án ↔ video: 8/8 mục tiêu có dạy; lệch: covers 1 → `example` (thực tế dạy ở sym#0, formula#0-1); mục tiêu 4 "vai trò pip freeze" chỉ qua 1 dòng bảng + câu ở pitfalls#2, không chạy `pip freeze` trên màn hình.

## L09 — Thư viện mảng

### (a) Chuẩn xác
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Bằng chứng đã chạy | Đề xuất sửa |
|---|---|---|---|---|---|
| L09 | MUST | hook#0, scale#0, quiz#2 vs hook title, quiz#2, recap#0, curriculum | hook: "nhanh gấp ≈ 30 lần", "một lệnh trên mảng ≈ 6 ms"; scale#0 "×100: 1 000 000 ≈ 200 ms ≈ 6 ms ≈ 30"; trong khi tiêu đề hook "cả trăm lần", quiz#2 "nhanh hơn khoảng hàng trăm lần", recap "nhanh hàng trăm lần", curriculum "hàng trăm lần" | Tự đo (timeit, min, labs/.venv-pyt, tổng bằng vòng for trên list vs arr.sum() trên mảng đã có): 10^4: 1,38 ms vs 0,011 ms = 129x; 10^6: 153 ms vs 0,87 ms = 176x; 10^7: 2,08 s vs 11,3 ms = 183x. Thời gian vòng lặp khớp bậc (153 vs 200 ms; 2,1 vs 2 s) nhưng mảng nhanh hơn 6-7 lần so với bảng bài (0,87 vs 6 ms) nên tỉ số bài ghi (30) sai bậc và tự mâu thuẫn với "hàng trăm" ở 4 chỗ khác; dòng 10^4 ghi 100, hai dòng sau ghi 30. | Sửa cột mảng thành ≈ 1 ms/≈ 10 ms/≈ 100 ms (10^6/10^7/10^8 ngoại suy ≈ 0,1-0,7 s tuỳ băng thông) và "nhanh gấp ≈ 100-200"; hoặc đổi các câu "hàng trăm" thành "hàng chục đến trăm" |
| L09 | MUST | formula#3 (Bước 4) | `>>> print(x.mean())` ... `>>> print(x.std())` rồi "Tám số có trung bình năm" | Biến `x` không được định nghĩa ở bất kỳ đâu trong bài (grep YAML: không có "x =" / "[2, 4, 4, 4, 5, 5, 7, 9]"; khung 00049.png). Gõ lại ra NameError: name 'x' is not defined. Tám số (2,4,4,4,5,5,7,9) chỉ có trong curriculum. Người học không làm tay lại được ví dụ độ lệch chuẩn. Tôi tự dựng x thì đầu ra khớp: 5.0 / [9. 1. 1. 1. 0. 0. 4. 16.] / 4.0 / 2.0 / 2.0. | Thêm `>>> x = np.array([2, 4, 4, 4, 5, 5, 7, 9])` ở đầu Bước 4 và đọc tám số |
| L09 | SHOULD | formula#0-2 | `>>> print(so_tien * 2)`, `so_tien.sum(axis=0)`, `so_tien + np.array([1, 2, 3])` | `so_tien = np.array([[500, 1200, ...` chỉ xuất hiện ở example#0, SAU ba bước dùng nó; trước đó chỉ có hình intuition#0 gắn nhãn "so_tien". Chạy đủ khớp nhưng thứ tự dạy làm người học không gõ được theo. | Đưa dòng tạo so_tien lên đầu formula#0 |
| L09 | SHOULD | intuition#1 (SVG) | "mảng (3, 4)" vẽ ba hàng giống hệt nhau 500 1200 300 800 | Khung 00031.png: ba hàng giống nhau, trong khi so_tien của bài là 500/1200/300/800, 200/900/450/100, 1500/700/600/2000 (hình intuition#0 và code đúng). Nhãn hình lệch dữ liệu bài. | Thay bằng ba hàng thật hoặc ghi "hàng ví dụ" |
| L09 | SHOULD | scale#1 | "phép tính chạy bằng mã đã biên dịch, không qua từng lệnh của Python" | "biên dịch" không được giảng ở PYT L00-L09 (chỉ FND nói biên dịch Java). Số bộ nhớ khớp: list 1e6 = 36-40 MB (tracemalloc 39,99 MB) ✓, mảng 8,0 MB ✓, 10^8: 800 MB / ~3,6-4 GB ✓. | Thêm một câu giải thích "mã viết sẵn bằng C, chạy cả mảng một lượt" |

### (b) Độ sâu
`L09 | 0a24443129857a91 | 17,1 (5 phút là dừng làm lab; 12,1 phút lời đọc) | P1=1 P2=1 P3=1 P4=2 P5=2 P6=2 P7=2 | P8=2 | P9=2 | Tổng 11 | GẦN | "biên dịch", "ngoại suy", "(3,)" (bộ một phần tử), vì sao 2^31−1 (số nguyên 4 byte = 32 bit), ms/µs, np.allclose/np.sqrt (np.allclose chỉ xuất hiện ở lab) | Biến x không định nghĩa (P2); hình broadcast sai dữ liệu (P3); số tốc độ mâu thuẫn "hàng trăm"`

### (c) Lab
`L09 | có | ~3 phút | không kẹt | khớp: lời giải tự lập chạy cham.sh pyt L09 chuan_hoa.py → ĐÚNG ngay lần đầu; giống hệt loi_giai.py (chỉ khác tên biến). Đề rõ (std mặc định chia n được nêu trong de.md; làm tròn từng dòng nêu rõ). Một cách hợp lý khác (f-string) có thể bị chấm KHÁC do cách in mảng, nhưng đề đã chỉ định "dùng np.round".`

### (d) Người học kẹt ở đâu
formula#3 (Bước 4) `>>> print(x.mean())`: không biết x là gì (chưa bao giờ được định nghĩa), nên không làm lại được ví dụ độ lệch chuẩn.

### (e) Số/mã đã tính lại
- Số: 2200/2800/1350/2900, 9250, [700. 412.5 1200.], 770,8333, 3 giao dịch > 1000, std=2, chuẩn hoá ±1,22474487, [5 7 9]/[6 15], int32 2e9+2e9 = -294967296, 2^31−1 = 2147483647, 10^9×8 B = 8 GB → tất cả khớp. Tốc độ/bộ nhớ ở 3 quy mô: tự đo, xem (a): tốc độ ✗ (30 vs 130-180), bộ nhớ ✓.
- Mã chạy: 45 đầu ra trong 20 khối (s1.py, labs/.venv-pyt, 3.11.9) → 45/45 khớp (x được tôi tự định nghĩa; so_tien dựng lại). Traceback broadcast: "operands could not be broadcast together with shapes (3,4) (3,) " ✓ (có dấu cách cuối). `<stdin>` đúng cho 3.11; 3.13 REPL tương tác in `<python-input-N>`, bài L04 đã có ghi chú, L09 không lặp lại.
- Khung đã xem: L09/frames 00002, 00027, 00031, 00044, 00049, 00072, 00077, 00101, 00130. Lỗi hiển thị: không có chữ tràn; lỗi nội dung ở 00031 (hình) và 00049 (x lạ), 00002/00077 (bảng 30 lần cạnh tiêu đề "cả trăm lần").

### (f) 5 kiểm đặc biệt
1. P1: kẹt: biên dịch, ngoại suy, (3,) , 2^31−1 (không giải thích vì sao), ms/µs, np.allclose (lab). Còn lại (mảng, shape/dtype/ndim, trục, lan truyền, mặt nạ) đều giảng tại chỗ.
2. Practice: đủ để làm (đề có dữ liệu trong de.md, kết quả mong đợi, hint đúng công thức); quiz Q1/Q2 mới, tính được bằng tay.
3. Cảnh quy mô: bộ nhớ đúng bậc; thời gian: vòng lặp đúng bậc, mảng chậm hơn thực tế 6-7 lần → tỉ số 30 sai bậc so với đo 130-180 (MUST ở a); "ngoại suy 10^8: mảng ≈ 700 ms" cũng cao hơn (~0,1-0,3 s).
4. 3.11 vs 3.13: xem ghi chú traceback; mã numpy chạy giống nhau (kiểm cả 3.13 nếu venv 3.13 cài xong: xem cuối tệp).
5. Mục tiêu ↔ video: 9/9 mục tiêu có cảnh; mục tiêu 7 "tốc độ và bộ nhớ ở ba quy mô" dạy bằng số sai tỉ số; curriculum (example) nói "hàng trăm lần" khớp đo nhưng bài ghi 30.

## L10 — Thư viện bảng dữ liệu

### (a) Chuẩn xác
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Bằng chứng đã chạy | Đề xuất sửa |
|---|---|---|---|---|---|
| L10 | MUST | hook#0 (say, có trong SRT 00:00-00:54) | "Trên máy kiểm nó chiếm khoảng một trăm bốn mươi triệu byte bộ nhớ, tức cỡ một trăm bốn mươi chục byte mỗi dòng." | 140 MB / 10^6 dòng = 140 byte/dòng (tôi đo 137 B/dòng với 4 cột, memory_usage(deep=True)). "một trăm bốn mươi chục byte" = 1 400 byte, sai 10 lần. | Đổi thành "một trăm bốn mươi byte mỗi dòng" |
| L10 | SHOULD | formula#3-4 (SRT 04:01-04:11) | lời: "Hai giao dịch nạp cộng ba triệu. Một giao dịch rút cộng ba trăm nghìn, chú ý giao dịch rút thứ hai thiếu số tiền..." | Khung 00048.png (t=04:01): màn hình là bảng groupby("tai_khoan") (A01 1800000, A02 2800000, A03 150000); bảng theo loại với nạp/rút đã qua ở khung 00046. Ba tổng theo tài khoản không được đọc/giải thích (A01 = 500 000 + 300 000 + 1 000 000 không hiện), và chữ "Vì mỗi nhóm cộng riêng: chuyen 500 000 + ..." nằm dưới bảng tài khoản. | Tách lời cho đúng bảng; thêm câu giải thích tổng A01/A02 |
| L10 | SHOULD | hook#0, scale#1 | "nhóm theo loại: vòng lặp Python ≈ 20 ms / ≈ 2 s ; một lệnh trên bảng ≈ 2 ms / ≈ 200 ms" | Tự đo groupby("loai")["so_tien"].sum() (3 loại, 1 cột số): pandas 2,5-3,8 ms (10^4) và 180-250 ms (10^6) ✓ khớp bài. Vòng lặp Python: duyệt list dict 4,7 ms / 350-537 ms; duyệt zip 3,6 ms / 284 ms; csv.DictReader + float 44 ms / 4,5-11,4 s. Tỉ số pandas nhanh hơn: 1,3-1,9x (10^4) và 1,4-2,9x (10^6) nếu chỉ tính nhóm; chỉ khi vòng lặp gồm cả đọc/parse CSV mới ≈ 10-25-45x. Bài không nói vòng lặp gồm những gì; chiều đúng nhưng bậc "10x" chỉ đúng với một định nghĩa ngầm, và ở 10^4 gần như bằng nhau (pandas có chi phí cố định vài ms). | Nêu rõ "vòng lặp đọc CSV rồi cộng" hoặc đổi số 2 s thành ≈ 0,3-0,5 s và thêm câu "bảng nhỏ thì pandas không nhanh hơn" |
| L10 | SHOULD | scale#0 | "×1: 10 000 ≈ 1,4 MB ≈ 820 KB ≈ 2 lần"; "×100: 1 000 000 ≈ 140 MB ≈ 24 MB ≈ 6 lần" | Tự đo memory_usage(deep=True): 10^4: 1,37 MB ✓; 10^6: 137 MB ✓. Kiểu category cho cùng dữ liệu: cả hai cột chữ → 0,18 MB / 18,0 MB = 7,5x và 7,6x (tỉ lệ KHÔNG đổi theo số dòng); chỉ cột loai → 0,77 MB / 77 MB = 1,8x ở cả hai quy mô. Không cấu hình nào cho 2x ở 10^4 rồi 6x ở 10^6; cột "tiết kiệm" gợi ý tỉ lệ tăng theo quy mô là sai. Hướng (category tiết kiệm) và bậc (vài lần) đúng. | Cùng một cấu hình cho hai dòng; ghi "tiết kiệm không đổi theo số dòng, phụ thuộc số giá trị khác nhau" |
| L10 | SHOULD | hook#0, scale#0 | "một triệu dòng, bốn cột" | Bảng gd dùng cả bài có 5 cột (ma, ngay, loai, tai_khoan, so_tien); 4 cột mới ra 137 MB, 5 cột (thêm ngay dạng chữ) ra 204 MB. Số 140 MB ứng với bảng 4 cột không được nêu là cột nào. | Liệt kê 4 cột |
| L10 | SHOULD | toàn bài (formula, example, quiz) | `gd = pd.read_csv("gd.csv")`, `tk = pd.read_csv("tk.csv")`, quiz "Bảng giao dịch ở trên (7 dòng)" | Nội dung gd.csv (7 dòng) và tk.csv không hiện ở khung nào (chỉ head(3) và hình 3 dòng). Tôi phải suy ra dữ liệu từ đầu ra mới dựng lại được (đầu ra khớp 100% sau khi dựng). Người học gõ code trong bài sẽ gặp FileNotFoundError. Quiz Q1/Q2 ("nạp có bao nhiêu dòng, tổng?", "ba nhóm bằng bao nhiêu?") đã có sẵn đáp án trên màn hình ở formula#2-3 nên không còn là tính mới. Hình "bảng gốc" ở intuition#1 chỉ có 6 dòng (thiếu dòng rút thứ 7 không có tiền) dù gọi là "bảng gốc". | Hiện nội dung gd.csv/tk.csv (hoặc ghi vào lab); đổi số liệu quiz |
| L10 | SHOULD | formula#2 | `print(gd.loc[gd["loai"] == "nap", "so_tien"].sum())` | `.loc` dùng không giảng ở bất kỳ đâu trong PYT. | Một câu: ".loc[điều kiện, cột] chọn dòng rồi lấy cột" |

### (b) Độ sâu
`L10 | 65297603828a7a1c | 17,7 (6 phút dừng làm lab; 11,7 phút lời đọc) | P1=1 P2=1 P3=2 P4=2 P5=1 P6=2 P7=2 | P8=2 | P9=2 | Tổng 11 | GẦN | .loc, "biên dịch", "ngoại suy", kiểu hiển thị `str`/`datetime64[us]`, idxmax (chỉ ở hint lab), đọc theo khối (chunksize) chỉ nói tên | gd.csv/tk.csv không hiện (P2); quiz Q1/Q2 lặp lại đáp án đã hiện (P5); lời lệch màn hình ở formula#3-4`

### (c) Lab
`L10 | có | ~5 phút | de.md nói "tổng nguyên" nhưng cảnh video (practice#0) chỉ ghi "<ngày> <tổng>"; tôi in theo_ngay.max() ra 5250000.0 | lần 1 cham.sh pyt L10 thong_ke.py → KHÁC (dòng "Ngay nhieu nhat: 2 5250000.0" vs "2 5250000"); sửa int(...) → ĐÚNG. Người chỉ xem video (không đọc de.md) bị chấm KHÁC mà gợi ý "Nếu kẹt" cũng không có int(). loi_giai.py khác tôi chỉ ở int(theo_ngay.max()). Đề khác (8 dòng, cột kenh) với ví dụ nên không chép được.`

### (d) Người học kẹt ở đâu
formula#0 `gd = pd.read_csv("gd.csv")`: tệp gd.csv không có/không hiện, chạy báo FileNotFoundError; kế đó formula#2 `gd.loc[gd["loai"] == "nap", "so_tien"]` (`.loc` chưa giảng).

### (e) Số/mã đã tính lại
- Số: 500000+150000+800000=1450000; nạp 3000000; rút 300000; tổng 4750000 ✓; 4750000/6=791666,67 ✓, /7=678571,43 ✓; hai ngày: ngày 1 = 2 500 000, ngày 2 = 450 000, ngày 3 = 1 000 000, ngày 4 = 800 000 ✓; max−min = 3 ngày ✓; A01 1 800 000, A02 2 800 000, A03 150 000 ✓; 14 GB = 137 B × 10^8 ✓, 3 phút = 2 s × 100 ≈ 200 s ✓; "140 chục byte" ✗; tỉ lệ 2x→6x ✗ (xem a).
- Mã chạy: 37 đầu ra trong 22 khối (s1.py + chk.py, pandas 3.1.1, gd.csv/tk.csv dựng lại từ đầu ra) → 37/37 khớp, kể cả `str`, `datetime64[us]`, `dtype: object`, ValueError "The truth value of a Series is ambiguous. Use a.empty, a.item(), a.any() or a.all()." (bài rút gọn bằng "…"), `(== nan).sum()` = 0 vs isna = 1 ✓, DictReader cho {'chuyen': 1450000, 'nap': 3000000, 'rut': 300000} ✓.
- Khung đã xem: L10/frames 00002, 00030, 00034, 00044, 00046, 00048, 00053, 00075, 00122. Lỗi hiển thị: không chữ tràn; 00048 màn hình lệch lời; 00034 hình "bảng gốc" 6 dòng.

### (f) 5 kiểm đặc biệt
1. P1: kẹt: `.loc`, "biên dịch", "ngoại suy", `str`/`datetime64[us]` (chỉ nói "kiểu ngày giờ"), idxmax ở hint, "đọc theo khối" (chỉ tên). DataFrame, Series, NaN, mặt nạ, groupby, merge/left, category, parse_dates/.dt.day đều giảng tại chỗ.
2. Practice: đủ để làm (de.md có CSV 8 dòng và kết quả); thiếu `int()` trong cảnh video.
3. Cảnh quy mô: bộ nhớ 137 B/dòng ✓ đúng bậc, 10^8 ≈ 14 GB ✓; thời gian pandas ✓, vòng lặp tuỳ định nghĩa (xem a); tỉ lệ category sai quy luật.
4. 3.11 vs 3.13: pandas 3.1.1 trên 3.11 (đã chạy); 3.13 xem cuối tệp; không có `<stdin>` traceback trong L10, ValueError của pandas giống nhau.
5. Mục tiêu ↔ video: 8/8 mục tiêu có dạy; mục tiêu 6 ("bộ nhớ thay đổi thế nào theo số dòng và kiểu cột") dạy bằng tỉ lệ 2x→6x sai quy luật; example giáo án (7 giao dịch, 1 450 000/3 000 000/300 000, 4 750 000 của 6, chia 6/7, category) khớp.

## Bổ sung: chạy lại trên Python 3.13.5
Dựng venv 3.13.5 (numpy 2.4.6, pandas 3.1.1), chạy lại toàn bộ s1.py của L09 (45 đầu ra) và L10 (37 đầu ra): đầu ra GIỐNG HỆT bản 3.11.9 (diff rỗng, kể cả thông báo ValueError của numpy/pandas, `str`, `datetime64[us]`). Khác biệt 3.11/3.13 chỉ nằm ở (i) tiêu đề traceback của REPL tương tác `<stdin>` vs `<python-input-N>` (L09 dùng `<stdin>`, L04 đã có ghi chú), (ii) thông báo csv bị che ở L08 (đã ghi trong bảng a của L08).
Tệp phụ: partC/l08, l08lab, l08_313, l09, l10, l10lab, v313, mp4 trong cùng thư mục scratchpad.

---
# Phần D (người đọc D)

Môi trường: Python 3.11.9 (labs/.venv-pyt: matplotlib 3.11.2, pandas 3.1.1, numpy 2.4.6, pytest 9.2.0); 3.13.5 hệ thống chỉ có matplotlib 3.11.2/pandas 3.0.6 (không có pytest). Máy đo chậm hơn máy kiểm của bài khoảng 5-7 lần (bị tranh CPU với người đọc khác), nên chỉ so BẬC và CHIỀU.
sha16 lúc đọc: L11 92948f46e6cb9c53, L12 9cce8b5914eb1bea, L13 7e509027d5e4a219 (đều khớp giá trị mong đợi).
Video vs YAML: L11 và L13 YAML sửa sau khi dựng video (YAML 04:05 và 03:59 ngày 14/11; mp4 02:25 và 02:37) — srt lệch 1 câu mỗi bài (L11 "Bước bốn, gộp." thay câu dài; L13 thiếu "Ngoài ra, thêm một tệp thư viện…"); L12 khớp (130/130 câu). Phần còn lại srt khớp YAML 100%.

## (a) Bảng chuẩn xác

### L11
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Bằng chứng đã chạy | Đề xuất sửa |
|---|---|---|---|---|---|
| L11 | SHOULD | formula#0, #2, #3 (hiện mã) | say formula#0: "Ba dòng đầu nạp thư viện và chọn chế độ vẽ ra tệp." (màn hình bắt đầu ở `loai = ["chuyen", "nap", "rut"]`; formula#2 dùng `ax1.bar(ten, tong)` mà `ax1`, `ten`, `tong` chưa dựng) | Chạy nguyên đoạn hiện trên màn hình: `NameError: name 'plt' is not defined`. Người học gõ lại theo màn hình sẽ lỗi; ba dòng import chỉ nằm rải ở prereq/sym#0, không có dòng `import matplotlib` nào hiện. | Thêm 3 dòng import vào đầu formula#0; formula#2 thêm `ten, tong = ..., fig1, ax1 = plt.subplots()`. |
| L11 | SHOULD | pitfalls#0 (frame 00102.png) | `<div class="code"><div> </div></div>` rồi chỉ có đầu ra `[0.0, 110.0] [99.0, 104.0]` | Frame 00102: ô mã rỗng phía trên đầu ra; đầu ra không có mã sinh ra nó. | Dán lại đoạn mã bước 2 vào ô, hoặc bỏ ô rỗng. |
| L11 | SHOULD | intuition, example#1, hook (00033, 00075, 00000) | nhãn trục x "1 2 … 7" chạm/đè dòng chú thích bên dưới; nhãn "103" chạm viền khung biểu đồ A | Xem frame. | Chừa khoảng cách giữa trục và chú thích. |
| L11 | SHOULD | covers / intuition#0 | covers: `objective 3 → formula`; mục tiêu 3 "Đọc một biểu đồ theo thứ tự tiêu đề, đơn vị, trục, thang, rồi mới đến hình" | Thứ tự đọc chỉ có ở intuition#0 (một câu) và recap; formula không dạy thứ tự đọc; không có bài tập đọc một biểu đồ cho sẵn (tiêu đề bài hứa "đọc biểu đồ"). | Sửa covers → intuition, thêm một cảnh/câu hỏi đọc biểu đồ cho sẵn. |
| L11 | SHOULD | sym#1, intuition | "cột nhóm (histogram)" cho `ax.hist` | "Biểu đồ cột nhóm" trong tiếng Việt thường là grouped bar; hist là biểu đồ tần suất/histogram. Tin cậy thấp. | Gọi là "histogram (cột đếm theo khoảng)". |
| L11 | SHOULD | scale#0 | "vẽ gộp thành ô lục giác ≈ 100 ms" | Không có mã `hexbin` hay hình ô lục giác trong cả bài. Tự đo: hexbin PNG 1e3/1e5/1e6 = 457/351/879 ms (phẳng, đúng chiều) nhưng người học không thể tự lặp. | Thêm một dòng `ax.hexbin(x, y, gridsize=30)` và hình. |

Số trong scale đã tự đo: SVG scatter 1e3 = 0,12 MB (bài 120 KB), 1e5 = 10,8 MB (11 MB), 1e6 = 107,8 MB (110 MB; bài ghi "ngoại suy" nhưng thực ra đo được) ✓; PNG 29 KB/23 KB/20 KB (bài "vài chục nghìn byte", "gần cố định") ✓; thời gian PNG 192 ms/1,2 s/8,0 s (bài 90 ms/200 ms/1 s: cùng chiều tăng, máy tôi chậm ~6x) ✓ bậc; hexbin phẳng ✓. SVG mỗi điểm một dòng: 1000 điểm → 1440 dòng, 1039 thẻ `<use>` ✓.

### L12
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Bằng chứng đã chạy | Đề xuất sửa |
|---|---|---|---|---|---|
| L12 | SHOULD | intuition#0 + quiz#1 | "phí = tiền ÷ 1000"; đáp án quiz "10 999 999 → 10 999" (cũng bảng example#1) | Đặc tả hiển thị là phép chia (10 999 999 ÷ 1000 = 10 999,999); chỉ khi làm tròn xuống (`//`) mới ra 10 999 (chạy: `10999999 // 1000 == 10999`). Không cảnh nào nói "làm tròn xuống" (grep YAML L12: không có). Người học tính tay từ đặc tả như bài dặn sẽ ra khác đáp án. | Ghi "phí = tiền chia 1000, lấy phần nguyên (làm tròn xuống)". |
| L12 | SHOULD | scale#0 + say | "Quy mô càng lớn, chạy tay càng không thể, còn máy gần như không đổi." | Bảng của chính bài: máy 800 ms → 2 s → 10 s → 2 phút (×150); tự đo pytest: 100 ca 0,65 s, 1000 ca 4,65 s, 10000 ca 74 s (tăng gần tuyến tính, không "không đổi"). Cảnh scale#1 "trong vài giây" chỉ đúng tới ~1000 ca. Số tay: 10 000×30 s = 83,3 giờ = 3,47 ngày (bài "≈ 3 ngày"; giáo án ghi 83 giờ), 100 000×30 s = 34,7 ngày (bài "≈ 30 ngày"). | Sửa "máy tăng chậm hơn nhiều so với tay (vài giây → vài phút)"; ghi 3,5 ngày. |
| L12 | SHOULD | hook, formula#0-#6, check, example | `phi_chuyen` và bản mã sai | Mã hàm `phi_chuyen` (cả bản `<` và `<=`) không hiện ở cảnh nào của L12 (grep: chỉ có trong `checks`); bài khẳng định "mã sai chỉ khác ở dấu <= so với <" mà người học không thấy hai dòng mã. Tự dựng phi.py theo đặc tả và chạy đúng: bản đúng `7 passed`, bản `<=` `..F....` / `1 failed, 6 passed` / `FAILED test_phi.py::test_bien[50000-1100] - assert 0 == 1100` khớp màn hình. | Hiện 4 dòng `phi_chuyen` ở formula#0 và dòng `<=` ở bước 3. |
| L12 | SHOULD | intuition#0 (00024.png) | trục số "50 000 / 1 100 000 / 11 000 000"; lời: "Mỗi chỗ đổi nhánh là một ngưỡng" | Hình chỉ có hai vạch đỏ (50 000 và 11 000 000), 1 100 000 là chữ xám không vạch, trong khi example#1 có ba ngưỡng; vạch thứ hai lệch khỏi nhãn "11 000 000" ~140 px. | Thêm vạch 1 100 000 và căn nhãn. |

Đã chạy (pytest 9.2.0, 3.11.9): hook/formula#2/#4, example#0 (`1 failed, 1 passed`, `assert (0.1 + 0.2) == 0.3`), pitfalls#2/#3 (`1 passed`), check (`[0, 500, 1100, 1101, 11000, 12000]`, `[0, 1100, 1100, 1101, 11000, 11000]`, 7) — đều khớp.

### L13
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Bằng chứng đã chạy | Đề xuất sửa |
|---|---|---|---|---|---|
| L13 | MUST | formula#0 (say) | say: "tức cỡ chín mươi bốn chục byte mỗi dòng" (srt dòng 127 của video cũng đọc như vậy); màn hình: "tức cỡ 94 byte mỗi dòng" | "chín mươi bốn chục" = 940 byte. Tự đo: tệp 1e6 dòng 18 890 060 B, tracemalloc peak cách A 92 045 KiB = 94,3 MB → 94,3 byte/dòng (màn hình đúng, lời đọc sai ×10). | Sửa lời: "cỡ chín mươi bốn byte mỗi dòng". |
| L13 | MUST | quiz#1 câu 1 | "A cần cỡ 5 GB nên sát giới hạn và dễ hết bộ nhớ khi có thêm việc khác" (tệp 5 GB, máy 8 GB) | Mâu thuẫn số của chính bài: hook/formula#0 nói tệp 19 MB cần 94 MB bộ nhớ (×5; tự đo 18 890 060 B → 94,3 MB = 4,99×). Tệp 5 GB cần ≈ 25 GB (tính: 5e9×94,3/18,89 = 2,5e10 B) > 8 GB: A chắc chắn hết bộ nhớ, không phải "sát giới hạn". | Sửa: "A cần cỡ 25 GB (gấp ~5 lần tệp) nên chắc chắn hết 8 GB". |
| L13 | MUST | covers obj 1 / formula, pitfalls#1 | mục tiêu: "Đo thời gian và bộ nhớ của ba cách đọc tệp ở hai quy mô và ngoại suy lên quy mô lớn"; pitfalls#1: "Phép thử: đo ở hai quy mô rồi ngoại suy bộ nhớ" | Bài chỉ trình bày số đã đo; không có dòng mã đo nào ở L13, và cả L00-L13 không có công cụ đo (Grep `perf_counter|time\.time|timeit|tracemalloc|getsizeof|resource` trên 14 bản rút gọn: 0 kết quả). Người học không biết đo bằng gì; giáo án hứa kỹ năng "đo" mà bài không dạy. | Thêm một cảnh nhỏ dạy `time.perf_counter()` và `tracemalloc` trên 10^3 dòng, hoặc đổi mục tiêu thành "Đọc số đo ... và ngoại suy". |
| L13 | SHOULD | formula#1, scale#0 | "108 dòng (ngoại suy) … B ≈ 4 phút" | Chính bài: B 2 s ở 10^6, tuyến tính ×100 → 200 s = 3,3 phút (C: 300 ms×100 = 30 s ✓). | "≈ 3 phút". |
| L13 | SHOULD | scale#0 (frame 00062.png) | "Đo bằng verify_pyt trên máy kiểm" | Tên công cụ nội bộ hiện cho người học, không ở đâu giảng; người học không có `verify_pyt`. | Bỏ tên, ghi "đo bằng timeit/tracemalloc trên máy kiểm". |
| L13 | SHOULD | example#0-2, check, formula#2 | "Với tệp tám dòng, máy in …" | Tệp `gd.csv` 8 dòng không hiện ở đâu, nên người học không chạy lại được. Tôi dựng lại từ `checks` (500000,2000000,300000,150000,1000000,800000,400000,250000 cho chuyen,nap,rut,chuyen,nap,chuyen,nap,rut): chạy đủ 5 đoạn → `{'nap': 400000, 'rut': 250000}`, `{'chuyen': 1450000, 'nap': 3400000, 'rut': 550000}` ×2, tổng chung `5400000`, ba khối `500000/950000/—`… khớp 100% — nhưng chỉ khi biết đúng dữ liệu. | Hiện 8 dòng CSV ở đầu formula#2. |
| L13 | SHOULD | pitfalls#2, quiz#1 câu 2, scale#1 | "trung vị của các trung vị khối khác trung vị cả tệp" | "Trung vị" chưa từng được giảng (Grep L00-L12: 0 kết quả), và khẳng định không kèm số. Phản ví dụ chạy được: khối [1,2,9] và [3,4,5]: trung vị các trung vị = 3,0, trung vị thật = 3,5. | Một câu định nghĩa trung vị + ví dụ số này. |
| L13 | SHOULD | scale#0/formula#1 (bảng 10^3) | "10^3 dòng: A ≈ 10 ms, B ≈ 3 ms, C ≈ 3 ms" | Tự đo 10^3: A (split) 1,6 ms, A (DictReader trên danh sách) 5,1 ms, B 4,7 ms, C 3,3 ms; thứ tự A>B không lặp lại và mã "duyệt" của A không hiện. Ở 10^6 thứ tự C < A < B lặp lại (1,46 s < 2,47 s < 15,5 s trên máy chậm) ✓. Ghi chú: chênh vài ms ở 10^3 không có ý nghĩa. | Hiện mã A; nói "ở 10^3 cả ba đều vài ms". |
| L13 | SHOULD | practice#1-2 (lab) | "chuỗi MODULE, TESTS do bạn viết" / gợi ý "Ca kiểm tự ghi tệp CSV nhỏ bằng tempfile" | Chuỗi mã nhúng chuỗi có `"\n"`: nếu viết `'''…\n…'''` thường (không raw) thì tệp kiểm bị lỗi cú pháp; hàm chấm dùng `--tb=no` nên chỉ in `4. Ba ca kiem qua: CHUA (0/2)` và `8/10`, không lý do. Tôi mắc đúng lỗi này (lần 1: 8/10; sửa `r'''` → ĐÚNG). `tempfile` chưa được dạy ở bất kỳ bài nào (Grep: 0). `loi_giai.py` dùng `\\n`. | Gợi ý: "trong chuỗi mã, viết \\n (hai gạch) hoặc dùng r'''"; chỉ ra cách xem lỗi (`--tb=short`). |

Số đã chạy lại ở L13 (khớp): bộ nhớ A/B/C ở 10^3: 95,6/41,3/289,9 KiB (bài 98/42/300 KB ✓); ở 10^6: 92 045/42,2/9 099 KiB (bài 94 MB/43 KB/9,3 MB ✓); tệp 15 887 B và 18 890 060 B (bài 16 KB, 19 MB ✓); 94,3 B/dòng; ngoại suy ×100 (9,4 GB, 1,9 GB) ✓.

## (b) Độ sâu
Bài | sha16 | Phút | P1 P2 P3 P4 P5 P6 P7 | P8 | P9 | Tổng | Mất gốc | Cần biết trước | Chỗ thiếu chính
- L11 | 92948f46e6cb9c53 | 19,2 | 1 2 1 2 2 2 1 | 2 | 2 | 11 | GẦN | `ngoại suy`; `điểm ảnh` (vector có giảng, điểm ảnh không); `ô lục giác`; `get_offsets/collections/marker`; 3 dòng import không hiện ở formula | Mã trên màn hình không tự chạy được (thiếu import/biến); hexbin không có mã/hình; mục tiêu "đọc biểu đồ" mỏng; lỗi hiển thị nhỏ (nhãn trục đè chú thích, ô mã rỗng)
- L12 | 9cce8b5914eb1bea | 18,9 | 1 1 1 2 2 2 2 | 2 | 2 | 11 | GẦN | `ngoại suy`; `hàm thuần`; ký hiệu `@` (decorator); `subprocess`/`sys.executable`/`capture_output` (chỉ trong gợi ý lab); `assert` (prereq nói "đã biết" nhưng L00-L11 không có, tuy sym#0 có giảng) | Mã `phi_chuyen` (đúng và sai) không hiện; quy tắc làm tròn xuống không nêu; câu "máy gần như không đổi" lệch số
- L13 | 7e509027d5e4a219 | 22,0 | 0 1 2 1 1 2 1 | 2 | 2 | 8 | CHƯA | `trung vị` (then chốt, chưa giảng); `ngoại suy`; `xếp trên đĩa`; `tempfile`; `verify_pyt` hiện trên màn hình; cách ĐO (perf_counter/tracemalloc) | Không dạy cách đo dù mục tiêu 1 là "Đo"; `gd.csv` không hiện; trung vị không có ví dụ số; đáp án quiz 1 và lời đọc "chục byte" sai

Ghi chú chấm: L13 P1=0 vì khái niệm then chốt (trung vị) + ≥3 từ; P2=1 (số đo xuất hiện không thấy cách đo; "trung vị không gộp được" không thử bằng số); P4=1 (ví dụ tay thiếu dữ liệu dòng); P5=1 (đáp án câu 1 sai chi tiết, lời giải một dòng). Tổng 8 là CHƯA chủ yếu do P1 và các MUST; sửa 3 MUST + định nghĩa trung vị + hiện gd.csv sẽ đưa lên ~11-12. L12 P1=1 là mức biên (4 mục ngoại vi chưa giảng, không mục nào then chốt).

## (c) Lab
Bài | tự làm được | thời gian | kẹt ở đâu | mong_doi khớp
- L11 | có | ~10 phút (tôi) / ước 15-20 phút người mới | không kẹt; cần nhớ `ax.patches`, `get_ylim` (có hình trong "Nếu kẹt"); tính "gấp 4,1" bằng chỉ số của max/min cần `index` (đã học L03) | khớp: `bash cham.sh pyt L11 ve_bieu_do.py` → ĐÚNG
- L12 | có (phần: cần công thức đọc dòng cuối) | ~15 phút / ước 25-35 phút người mới | `subprocess.run([...], capture_output=True, text=True)` và lấy dòng cuối, cắt " in …s" chưa từng dạy (có chép sẵn lệnh trên màn hình, nên làm được) | khớp: `Ban loi: 5 failed, 1 passed` / `Ban sua: 6 passed` → ĐÚNG (cham.sh với đường dẫn tương đối OK)
- L13 | phần → có sau khi sửa | lần 1 ~15 phút ra 8/10; sửa lỗi thoát chuỗi thêm ~10 phút (tôi); ước 45-60 phút người mới | chuỗi MODULE/TESTS chứa `\n` (cần `\\n` hoặc `r'''`), `--tb=no` che nguyên nhân (`4. … CHUA`), `tempfile` chưa dạy | khớp sau sửa: ĐÚNG (10/10)

Đề rõ, không mơ hồ khiến lời giải hợp lý khác bị chấm sai: L11 (mọi cách `set_ylabel` hay không đều qua), L12 (đã so `loi_giai.py`: cùng cấu trúc), L13 (chỉ phụ thuộc `\n`). So `loi_giai.py` sau khi tự làm: cùng ý; L11 dùng `tong.index` thay `chieu_cao.index` (tương đương).

## (d) Người học kẹt ở đâu
- L11: formula#0 "Ba dòng đầu nạp thư viện và chọn chế độ vẽ ra tệp" — mã hiện không có ba dòng ấy, gõ lại gặp `NameError: plt`; kế đó formula#2 `ax1.bar(ten, tong)` (ax1/ten/tong chưa dựng).
- L12: hook/formula#0 "assert phi_chuyen(49999) == 0" — chưa hề thấy hàm `phi_chuyen`; và quiz#1 "10 999 999 → 10 999" cần "làm tròn xuống" chưa nói.
- L13: pitfalls#2 / quiz#1 "trung vị không gộp được" — chưa biết trung vị là gì; trước đó scale#0 "Đo bằng verify_pyt" và mục tiêu "Đo" không có cách đo; lab: chuỗi mã có `\n`.

## (e) Số đã tính lại / mã đã chạy; khung hình
- L11: 21 điểm số/mã chạy lại (formula#0,2,3,5,7, example#0,2, check, quiz, tỉ lệ 4,0/1,03, 90,0/33,3/39,0/88,9/20,0/82,0, hist [5,5,0,0,1], ylim [0,3150]/[117,45;173,55], 7 điểm, 42,5%, 4750, ×10): 21/21 khớp; 3.11.9 và 3.13.5 cho đầu ra y hệt (`diff` rỗng). Quy mô: tự đo SVG/PNG/hexbin (xem trên) ✓ bậc.
- L12: 14 (7 ca, 1 failed/6 passed, `0 == 1100`, float ==/approx, xanh giả ×2, 6 giá trị tay, 7 ca, 5 ngưỡng-bảng 7 dòng, 50 phút/8,3 giờ/3,47 ngày/34,7 ngày, lab 0..150): 14/14 khớp (2 ghi chú SHOULD: làm tròn xuống, "3 ngày"). Quy mô máy: 0,65 s/4,65 s/74 s (100/1000/10000 ca) so bài 0,8/2/10 s: cùng chiều, tăng ~tuyến tính (bài nói "gần như không đổi" là SHOULD).
- L13: 18 số/mã (5 đoạn mã, 6 tổng, 2×3 bảng bộ nhớ, 3 bảng thời gian, 1,9/9,4 GB): 17/18 khớp; sai: "chục byte" (MUST); quiz "5 GB" (MUST); "4 phút" (SHOULD).
- Khung hình đã xem: L11: 00000, 00018, 00033, 00042, 00060, 00075, 00090, 00092, 00095, 00102, 00120, 00126, 00138; L12: 00000, 00024, 00040, 00064, 00076, 00080, 00096, 00112, 00128; L13: 00000, 00026, 00032, 00041, 00048, 00062, 00064, 00088, 00098, 00120. Lỗi hiển thị: L11 nhãn trục x đè chú thích (00033, 00075), nhãn "103" chạm viền (00000), ô mã rỗng (00102), hình 1 000 điểm chỉ vẽ ~45 điểm (00092, minh hoạ); L12 vạch/nhãn trục số lệch và thiếu vạch 1 100 000 (00024); L13 "verify_pyt" lộ trên màn hình (00062). Cỡ chữ đọc được ở mọi khung; không tràn/cắt.

## (f) 5 kiểm đặc biệt
L11:
1. Thuật ngữ: kẹt `ngoại suy`, `điểm ảnh`, `ô lục giác`, `get_offsets`, `marker` (cùng thiếu import ở formula) → P1=1.
2. Tự làm: đủ để làm (đề + kết quả mong đợi + gợi ý); không cần thêm.
3. Quy mô: tự đo đúng bậc/chiều (SVG 0,12/10,8/107,8 MB; PNG phẳng ~20-30 KB; thời gian tăng; hexbin phẳng).
4. 3.11 vs 3.13: không có traceback; chạy trên cả hai, đầu ra giống hệt.
5. Giáo án↔video: mục tiêu 1,2,4,5,6,7,8 được dạy; mục tiêu 3 (thứ tự đọc) mỏng và covers chỉ sai cảnh.
L12:
1. Kẹt: `@` decorator, `hàm thuần`, `ngoại suy`, `subprocess`/`sys.executable`; `assert` ghi "đã biết" nhưng chưa từng dạy trước L12 (sym#0 có giảng tại chỗ).
2. Tự làm: đủ nhờ lệnh chép sẵn; thiếu cách lấy dòng cuối/cắt thời gian (người mới ~25-35 phút).
3. Quy mô: tự đo 100/1000/10000 ca = 0,65/4,65/74 s: cùng chiều và bậc ở ca ít; bậc lệch khi lớn do máy chậm; "máy gần như không đổi" lệch (SHOULD).
4. 3.11 vs 3.13: không có khác biệt liên quan (đầu ra pytest cố định); 3.13 hệ thống không có pytest nên chỉ chạy được trên 3.11.9; ghi rõ.
5. Giáo án↔video: cả 8 mục tiêu được dạy trong cảnh covers (obj 4 → example; obj 5 → check ✓).
L13:
1. Kẹt: `trung vị` (then chốt), `ngoại suy`, `xếp trên đĩa`, `tempfile`, `verify_pyt`, cách đo; `chunksize` được prereq nhắc là "đã học" nhưng chỉ L10 nói khái niệm "đọc theo khối", chưa có tham số.
2. Tự làm: đủ khung nhưng có bẫy thoát chuỗi `\n` không được nói; người mới ~45-60 phút.
3. Quy mô: bộ nhớ khớp ±3% (94,3 B/dòng); thời gian cùng thứ tự C<A<B ở 10^6; chiều/bậc đúng; quiz 5 GB sai (MUST).
4. 3.11 vs 3.13: không có traceback; mã pandas/csv chạy cùng đầu ra trên 3.11.9 (pandas 3.1.1) và 3.13.5 (pandas 3.0.6).
5. Giáo án↔video: mục tiêu 1 ("Đo") KHÔNG được dạy (MUST); các mục tiêu 2-7 được dạy.

Ngưỡng chốt cho phần D: MUST = 3 (cả ba ở L13) → chưa đạt; P1=2 ở 0/3 bài; P8=2 ở 3/3 bài; P9=2 ở 3/3.
