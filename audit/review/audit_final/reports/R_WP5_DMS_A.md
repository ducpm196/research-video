# WP5 DMS-A (L00–L10): đã đọc 11/11 bài

Người đọc độc lập, 2026-11-14. Chỉ đọc; không sửa tệp nào ngoài báo cáo này. Tiêu chí: BRIEF mẫu F + ADDENDUM + BRIEF_READ_S01, người học mất gốc toán và lập trình, chỉ biết Python cơ bản. Bài chỉ tự đủ trong chính khoá DMS (các bài trước), không có chỗ nào viện "khoá khác".

## 1. Bảng chuẩn xác (chỉ lỗi có bằng chứng)

MUST: 0 (không có kiến thức sai, đáp án sai, số sai, mã sai luật, màn hình lệch lời đọc ở điểm kiến thức).

| Bài:cảnh | Mức | Trích / bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|
| L00:quymo.1; L02:quymo.1; L03:quymo.1; L05:quymo.1; L06:quymo.1; L08:quymo.1; L10:quymo.1 | SHOULD | `say` có số nhóm bằng dấu cách: "1 024 dòng" (L00), "5 149 phép", "1 000 số" (L02), "2 500 cặp", "1 000" (L03), "666 667", "666 666 666 667" (L05), "1 000 ô", "10 000", "100 000" (L06), "40 320", "10 080" (L08), "4 950", "1 000", "499 500" (L10). TTS có thể đọc rời từng cụm. Các bài L01, L04, L07, L09 đã viết số bằng chữ (ví dụ "456 nghìn 976"): đúng cách. | Ghi bằng chữ ("một nghìn hai mươi bốn", "năm nghìn một trăm bốn mươi chín") hoặc số liền không cách; nghe thử bằng tai | CONFIRMED (chưa nghe tiếng) |
| L01:hook.1 → example.1 | SHOULD | Màn hình đầu bài: `if (!(du_tuoi && co_ve)) chan();` dùng `!`, `&&` trước khi cảnh example.1 giảng "! là không, && là và". Quymo.1–2: "số nguyên 32 bit", "2^32 cặp" không giảng "32 bit". | Thêm một câu ở hook: "dấu ! là không, && là và"; thêm "32 bit là số có 2^32 giá trị" ở quymo.1 | CONFIRMED |
| L08:practice.1 (+quymo.1) | SHOULD | "đếm số hàng hợp lệ bằng cách thử mọi hoán vị"; "phần tử tối tiểu, tối đại". "Hoán vị" chỉ được giảng ở L09; "tối đại" chưa giảng (chỉ "tối tiểu" ở cảnh minimal); `from itertools import permutations` không giảng. | Thêm "hoán vị = mỗi cách xếp thứ tự" và "tối đại = không có ai đứng trên"; một câu về `permutations` | CONFIRMED |
| L08:quymo.2 | SHOULD | "chọn từng việc không còn ai đứng dưới: tối đa n lượt chọn, kịp với cả triệu việc". Số lượt là n, nhưng mỗi lượt nếu quét lại mọi việc thì tổng là n² (cách ở `practice` làm đúng như vậy); chỉ tuyến tính khi giữ bộ đếm "còn chờ mấy việc". | Nêu điều kiện (đếm sẵn số việc phải xong trước của từng việc) hoặc bỏ "kịp với cả triệu việc" | CONFIRMED |
| L05:practice.1/2; example.4 | SHOULD | Màn hình: "BCNN của 4 và 6 là 12" (BCNN không giảng); say example.4 "2 và 3 không có ước chung lớn hơn 1" (ước chung không giảng). Dòng mong đợi "…từ 1 đến 1000: 333 333" gồm HAI số, nhưng cả khoá dùng "333 333" kiểu nhóm nghìn ("1 024", "5 149") nên dễ đọc thành 333333. | Viết "bội chung nhỏ nhất (BCNN)" và định nghĩa ước chung; đổi định dạng thành `a=333 b=333` hoặc báo "hai số" trên màn hình | CONFIRMED |
| L06:quymo.1–2 | SHOULD | "chính là cận dưới mà nguyên lý chuồng bồ câu bảo đảm" (cận dưới không giảng; mục tiêu bài cũng dùng); hook "cất 11 khoá" (khoá = key không giảng ngoài "hàm băm chỉ mỗi khoá tới một ô"). | Giảng "cận dưới = mức thấp nhất chắc chắn có"; "khoá = mã định danh của dữ liệu cần cất" | CONFIRMED |
| L10:practice.1/3 | SHOULD | Dùng `C(12,5)`, `C(12,3) − C(7,3)` trong khi cả bài dùng ký hiệu binom; "vét cạn" (cũng ở L07:quymo) không giảng. | Nêu "C(n,k) cũng là tổ hợp chập k của n"; "vét cạn = thử hết mọi trường hợp" | CONFIRMED |
| L02:example.1, quymo.2, practice | SHOULD | `all(x*x >= x for x in range(10000))`, `any(... for y in range(n))`: biểu thức sinh trong ngoặc không giảng; chỉ nói "all là với mọi, any là tồn tại". Có thể Chặng 1 chưa dạy. | Một câu giảng "x*x >= x for x in range(...) nghĩa là thử lần lượt từng x" | PLAUSIBLE |
| L01:practice.1 | SHOULD | "Cặp 1 và cặp 3 là luật bạn vừa học; cặp 2 là mệnh đề đảo" nói trước đáp số 3/5 cặp trước khi người học thử (de.md thì không). | Bỏ vế "Cặp 1 và cặp 3…cặp 2 là…" hoặc chỉ nói "có cả luật đúng và mệnh đề đảo" | CONFIRMED |
| L10:pitfalls.3 | SHOULD | Tiêu đề "Chia k! cả khi các vật đã giống nhau (sai)" nhưng thân bài: "nếu đề đã đếm nhóm rồi thì không chia nữa" (khác ý). | Đổi tiêu đề thành "Chia k! khi đã đếm theo nhóm" | CONFIRMED |
| L03:direct.1; L04:quiz.1–2 | SHOULD | Lời đọc không có ngoặc: "2 nhân a cộng b cộng 1" (= 2(a+b+1)), "n nhân n cộng 1 chia 2" (= n(n+1)/2), "2 nhân 3k cộng 1", "2 nhân 5k cộng 1": mơ hồ khi chỉ nghe. Màn hình có ngoặc. | Đọc "2 nhân, mở ngoặc, a cộng b cộng 1, đóng ngoặc" hoặc "tất cả nhân" | CONFIRMED |
| out/DMS L00–L09 | Ghi chú quy trình | `L0x.mp4/.srt/chapters.txt` (11-02…11-11) cũ hơn YAML (11-14): SRT không có lời đọc cảnh quymo và practice, chapters.txt không liệt kê; `frames/` đã làm mới ngày 14 (có đủ quymo/practice). L10 chưa có thư mục out. Không phải lỗi nội dung. | Dựng lại video trước khi phát hành | CONFIRMED |

Kiểm riêng theo yêu cầu: ký tự điều khiển (`\t`, `\f`, `\b`...) trong mọi chuỗi YAML đã phân tích: 0 trường hợp ở 11 bài. Ký hiệu toán/LaTeX còn sót trong `say`: 0. Số "(số minh hoạ)" ghi rõ trong mọi bảng/ tiêu đề có tốc độ giả định (L00, L03, L04, L05, L07, L08, L09, L10); L01, L02, L06 không có số thời gian. Tiêu đề và bảng số khớp. Lab de.md không ghi sẵn đáp số.

## 2. Bảng độ sâu

Phút = ước tính từ số từ lời đọc (≈155 từ/phút) cộng thời gian dừng; bản dựng cũ chỉ 8–10 phút vì chưa có quymo/practice.

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | P8 | P9 | Mất gốc | Cần biết trước (dùng mà không giảng tại chỗ) | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 8f390ea820c4c714 | ~17 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | vòng for lồng nhau, range | SHOULD số "1 024" trong say |
| L01 | d2a52e2ac210905a | ~16 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | `!` `&&` `||` ở hook, "32 bit", "biên" (chỉ giảng qua ví dụ), `lambda`/`*dong` ở lab | hook dùng cú pháp chưa giảng |
| L02 | 399b1eac00a2569a | ~17 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | biểu thức sinh `x for x in ...` trong all/any | số "5 149" trong say |
| L03 | 94d8054f1e76a02f | ~18 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | "tối giản" (chỉ giảng bằng ngoặc đơn) | đọc công thức thiếu ngoặc |
| L04 | 3f312441791ef2dd | ~18 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | "hằng đẳng thức" (chữ trên màn hình) | đọc "n nhân n cộng 1 chia 2" |
| L05 | bbc8037ecc9bf1b8 | ~16 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | BCNN, ước chung, "dãy" | dòng mong đợi "333 333" nhập nhằng |
| L06 | 1b41d9b3f912a63a | ~17 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | khoá (key), cận dưới, `[0] * m` | cận dưới/khoá chưa giảng |
| L07 | dbd03fffaeaa49e6 | ~17 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | `lambda` ở de.md (giảng ở L01), "vét cạn", từ điển `.get` | không đáng kể |
| L08 | 165160fcbc556a2a | ~17 | 1 | 2 | 2 | 2 | 2 | 1 | 2 | 12 | 2 | 2 | ĐỦ | hoán vị (L09 mới dạy), tối đại, `itertools.permutations` | khẳng định "kịp cả triệu việc" thiếu điều kiện |
| L09 | 7a084dec3c43f443 | ~17 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | "PIN" (quen thuộc), `product(repeat=k)` ở gợi ý | không đáng kể |
| L10 | cd1df1bfaa97b0e6 | ~18 | 1 | 2 | 2* | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | ký hiệu `C(n,k)`, "vét cạn" | *P3 chấm theo mã SVG, chưa có khung hình (chưa dựng) |

Ngưỡng: MUST = 0: ĐẠT. P1 = 2 ở 5/11 bài (45%, cần ≥ 90%): KHÔNG ĐẠT (L00, L03, L04, L07, L09 đạt; sáu bài còn lại thiếu 1–2 từ dễ vá). P8 = 2 ở 11/11 (100%): ĐẠT. P9 = 2 ở 11/11. Mọi bài tổng P1–P7 ≥ 12, không mục nào 0.

## 3. Lab

Tự viết từ de.md (không nhìn loi_giai), chấm bằng `bash labs/cham.sh DMS Lxx <tệp>`; sau đó chạy cả `loi_giai.py`. Thời gian: tôi viết mỗi bài dưới 3 phút vì đã biết đáp số; với người học mất gốc ước 20–45 phút mỗi bài.

| Bài | tự làm được | kẹt tiềm năng | mong_doi khớp màn hình |
|---|---|---|---|
| L00 | có | `int(True)`; ba vòng for lồng nhau (đã có gợi ý) | khớp (ĐÚNG; màn hình = mong_doi.txt) |
| L01 | có | `product(..., repeat=n)`, `f(*dong)` (dấu `*` chưa dạy; de.md có gợi ý); lambda | khớp |
| L02 | có | all/any với biểu thức sinh | khớp |
| L03 | có | hàm tìm ước nhỏ nhất bằng while | khớp |
| L04 | có | ghép chuỗi bằng str(...) (có gợi ý), vòng while | khớp |
| L05 | có | `' '.join(str(x) ...)`; hiểu "333 333" là hai số | khớp |
| L06 | có | `dict.values()`, `combinations`, so sánh `set` | khớp |
| L07 | có | gọi hàm lambda `R(a, b)`; gom lớp không trùng | khớp |
| L08 | có (phần) | tự nghĩ thuật toán "chọn số lớn nhất còn trống"; hoán vị chưa dạy | khớp |
| L09 | có | `product`/`permutations`; số chẵn hai quy tắc | khớp |
| L10 | có | dựng hàng Pascal bằng quy tắc cộng; chiều hàng/cột `d[r][c]` | khớp |

Kết quả: 11/11 bài của tôi ĐÚNG, 11/11 `loi_giai.py` ĐÚNG, 11/11 khối "Kết quả mong đợi" trên màn hình trùng `mong_doi.txt`.

## 4. Người học kẹt ở đâu (chỗ đầu tiên)

- L00: không kẹt.
- L01: hook.1, `if (!(du_tuoi && co_ve)) chan();` (ký hiệu `!`, `&&` giảng ở cảnh example.1).
- L02: example.1, `all(x*x >= x for x in range(10000))` (cú pháp for trong ngoặc).
- L03: không kẹt (contradiction.2 "phân số tối giản" chỉ giảng bằng ngoặc đơn).
- L04: không kẹt.
- L05: practice.1, "BCNN của 4 và 6 là 12"; example.4 "ước chung lớn hơn 1".
- L06: quymo.1, "cận dưới mà nguyên lý chuồng bồ câu bảo đảm".
- L07: không kẹt (de.md dùng `lambda`, đã giảng ở L01).
- L08: practice.1, "thử mọi hoán vị", "phần tử tối đại".
- L09: không kẹt.
- L10: practice.1, "C(12,5) hai cách" và "vét cạn".

## 5. Số đã tính lại / mã đã chạy

- Mã trên màn hình (13 khối "Chạy thật" ở cảnh quymo, L00–L10 trừ nơi không có): 13/13 chạy và đầu ra trùng chữ "Kết quả chạy thật" (numpy không cần). L10 mã quymo cũng chạy khớp.
- Số trong bảng/lời đọc tính lại bằng Python: 25 nhóm kiểm (thời gian ở 10^9 phép/giây: L00 36,5 năm; L03 4,2 phút và 7,9 năm; L04 32 năm; L05 17 phút và 11,6 ngày; L07 11,6 ngày; L08 22 phút và 77 năm; L09 209 s, 47 phút, 62^8 = 2,5 ngày, 62^12 = 37 341 050 ngày ≈ 102 000 năm; L10 8 phút, 58 ngày, 0,05 s; số cách C(12,k), 14 hàng tô pô của ước 24, 5 hàng của ước 12, 185, 35, 792, 860…): 25/25 khớp. Thêm kiểm số nguyên tố: 3 biểu thức L03 đúng 16, 29, 80 là n nhỏ nhất; 1523, 1601 nguyên tố; 1681 = 41².
- Luật toán/thuật toán trên màn hình: bảng chân trị, De Morgan, phản đảo, quy nạp, quy nạp mạnh (12–15 cơ sở, n−4 ≥ 12), nguyên lý chuồng bồ câu (6 số/5 cặp bù), bắc cầu, cạnh phủ (7 cạnh của ước 12), tô pô, quy tắc nhân/chỉnh hợp, hệ số nhị thức: đều đúng luật; ghi chú: L07 quymo.1 kiểm bắc cầu cho quan hệ được định nghĩa bằng chính số dư nên số vi phạm luôn 0 (minh hoạ chi phí n^3, không phải kiểm độc lập), không sai.
- Lab: 11 lời giải tự viết + 11 `loi_giai.py` = 22/22 ĐÚNG.
- Chưa nghe bằng tai người; không kiểm được nguồn ngoài (bài không có trích dẫn số liệu thực tế).

## 6. Khung hình đã xem

Dùng ghép 12 khung mỗi bài (frames/ đã làm mới 14/11): L00 #0,#44,#48,#100,#103,#106,#109,#112,#115,#118,#121,#124 (cả quymo, bảng, practice); L01 #0,#32,#36,#58 (quymo), #67,#79; L02 #0,#35,#40,#91…#115; L03 #0,#45,#49,#92…#116; L04 #0,#22,#26,#84…#108; L05 #0,#33,#37,#86…#110; L06 #1,#36,#40,#77…#101; L07 #0,#32,#37,#81…#105; L08 #1,#19,#29,#72…#96; L09 #1,#33,#34,#74…#98. L10 chưa có khung (chưa dựng). Lỗi hiển thị: không thấy chữ tràn, đè, cắt, hay công thức hỏng; cỡ chữ đọc được. Khung quymo chỉ xem rõ ở L00 và L01 (các bài khác xem hook, hình cơ chế, quiz, practice, recap).

## 7. Nhận xét chung

- Nội dung đúng: không MUST, mọi số và mã kiểm lại khớp; chất lượng thực nghiệm (P8) và quy mô (P9) đều tốt: mỗi bài có lab chấm tự động và bảng số ở 2–4 mức quy mô kèm đánh đổi.
- Điểm yếu duy nhất theo ngưỡng là P1: mỗi bài thiếu 1–2 từ/ký hiệu (BCNN, cận dưới, hoán vị, tối đại, C(n,k), cú pháp all/any, `!`/`&&`); sửa bằng một câu mỗi chỗ, không phải viết lại cảnh.
- Mẫu lỗi lặp lại: số nhóm bằng dấu cách trong `say` ở 7/11 bài (quymo): sửa hàng loạt một lần; đọc công thức thiếu ngoặc ở L03, L04.
- Video chưa dựng lại (SRT/TTS cũ không có quymo, practice; L10 chưa dựng): cần dựng lại rồi nghe thử các số lớn.
- Lab đủ để tự làm cho cả 11 bài; L08 nặng nhất vì thuật toán tô pô tự nghĩ và hoán vị chưa dạy.
