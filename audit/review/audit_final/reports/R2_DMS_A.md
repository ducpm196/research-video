# R2 DMS_A: đã đọc 11/11 bài (L00–L10), vòng 2 trên bản đã sửa và dựng lại

Người đọc độc lập. Chỉ đọc, chạy mã ở thư mục tạm; không sửa tệp nào trong kho ngoài báo cáo này. Tệp tạm: `scratchpad/r2dmsA/`.

## 0. Chuẩn chấm và kiểm video mới

**Chuẩn P1 đã dùng.** P1=2 khi mọi khái niệm kỹ thuật, ký hiệu và thuật ngữ trên đường chính được giảng tại chỗ bằng lời, hoặc được định nghĩa ngầm rõ ràng bằng ví dụ ngay tại chỗ dùng lần đầu. Từ phổ thông tiếng Việt (vế, chia hết, tích, thừa số) không tính. P1=1 khi 1–2 thuật ngữ hoặc ký hiệu kỹ thuật dùng mà chưa giảng. P1=0 khi từ 3 thuật ngữ trở lên hoặc thiếu một khái niệm then chốt. Cú pháp Python lấy chuẩn là PYT L00–L03 (curriculum ghi `requires_ext`); phần ngoài chuẩn đó ghi ở cột "Cần biết trước".

**Spec so với video (build_report.json).** Dùng `lv.spec_digest` (bỏ `asr_reviewed`): 11/11 bài khớp `spec_sha256`. Không bài nào là "video cũ". `built_at` từ 2026-11-14T19:24Z đến 19:54Z.

**SRT so với `say`.** So chuỗi từ (bỏ dấu câu, chữ thường) của toàn bộ `say` với toàn bộ `.srt`: 11/11 bài giống 100% (L00 1978/1978 từ, L01 1890, L02 2049, L03 2087, L04 1995, L05 1833, L06 1898, L07 1877, L08 1767, L09 1807, L10 1901; ratio = 1.0, 0 chỗ lệch). Lưu ý: SRT sinh từ chính văn bản gửi TTS nên đây là kiểm tính nhất quán, không phải nghe độc lập. Phần nghe độc lập là `asr_report.md`: chưa xem xét 0 ở cả 11 bài, thiếu audio 0, gắn cờ 6/8/3/1/0/4/0/7/2/0/6 (L00..L10). Tôi không nghe âm thanh.

**Giọng.** Cả 11 bài một giọng `vi-VN-NamMinhNeural`, không trộn giọng.

**sha16 của YAML lúc đọc:** L00 5f814acbce7bb70b, L01 1829657d0b119840, L02 6cb79aa0847b75dd, L03 736f22896b87ee09, L04 aeed027b8ae58d23, L05 0c6bb51c8c9d1873, L06 9160df8366961ef7, L07 dbd03fffaeaa49e6, L08 5c7547a0e898ac80, L09 7a084dec3c43f443, L10 51995d9a9537fe85.

## 1. Chuẩn xác (chỉ lỗi có bằng chứng)

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L05 | MUST | `example` step 3 (SRT 00:04:25, `lessons/dms/L05_tap_hop.yaml` dòng 179, `out/DMS/L05/L05.srt` dòng 175) | “Bước ba, giao gồm số chia hết cho cả 2 và 3, tức là chia hết cho 6, vì không có số nào lớn hơn 1 mà chia hết cho cả 2 lẫn 3.” | Câu lý do sai nghĩa đen: 6, 12, 18 đều lớn hơn 1 và chia hết cho cả 2 và 3 (chạy `[x for x in range(2,100) if x%2==0 and x%3==0]` ra 6, 12, 18). Ý đúng là “2 và 3 không có ước chung nào lớn hơn 1” (nguyên tố cùng nhau), nên chia hết cho cả hai thì chia hết cho tích 6. Chỉ lời đọc sai; chữ trên màn hình chỉ viết “tức chia hết cho 6”, không có lý do. Người học chưa biết ước chung sẽ bị mâu thuẫn ngay với số 6 vừa nêu. | Đổi vế “vì …” thành “vì 2 và 3 không có ước chung nào lớn hơn 1”, hoặc bỏ lý do và nói “các số vừa chia hết cho 2 vừa chia hết cho 3 là 6, 12, 18, …, tức bội của 6”. | CONFIRMED |
| L04 | SHOULD | `hook` step 1 | say: “Hãy nghĩ tới một hàng quân cờ dựng đứng sát nhau”; màn hình: “Hàng domino” | Lời đọc nói “quân cờ”, hình và tên cảnh nói domino. Nhãn lệch ở chi tiết nhỏ. | Đổi lời đọc thành “quân domino”. | CONFIRMED |
| L05 | SHOULD | `intuition` | say: “vùng giữa màu đỏ bị đếm hai lần”; màn hình: “vùng đỏ bị đếm hai lần” | Khung `00033.png`: phần giao tô xám-xanh, chỉ chữ số 7 và nhãn “cả hai” màu đỏ. Hình không khớp cách gọi “vùng đỏ”. | Tô đỏ nhạt phần giao. | CONFIRMED |
| L09 | SHOULD | `rules` step 0 | show: “làm lần lượt nhiều bước, số cách mỗi bước không đổi”; say: “số cách ở mỗi bước không phụ thuộc bước trước đã chọn gì” | Cùng bài sau đó dùng A(10,3)=10×9×8 (số cách giảm dần). Lời đọc đúng (không phụ thuộc vào lựa chọn cụ thể), nhãn màn hình “không đổi” dễ đọc thành bằng nhau mỗi bước. | Sửa chữ màn hình thành “số cách ở mỗi bước không phụ thuộc bước trước chọn gì”. | CONFIRMED |
| L09 | SHOULD (hiển thị) | `quymo` step 0, khung `00053`–`00056` | dòng `print(do_dai, 'ky tu (62 ky tu):', 62 ** do_dai, 'mat khau,', 62 ** do_dai // 10 ** 9 // 86400, 'ngay')` | Dòng mã dài tràn ra ngoài khung mã bên phải (chữ tới x≈1908 trên khung 1920, khung kết thúc ở x≈1833). Quét điểm ảnh toàn bộ 1216 khung của 11 bài: chỉ 4 khung này có mực ở lề phải. Chữ vẫn đọc được, không bị cắt. | Ngắt dòng mã. | CONFIRMED |
| L10 | SHOULD | `binomial` step 1 | say: “Ta được x mũ n trừ k nhân y mũ k khi chọn y ở đúng k trong n ngoặc” | Khi nghe, “x mũ n trừ k” hiểu được là xⁿ − k (sai) thay vì x^(n−k). Màn hình viết rõ nên chỉ người nghe không nhìn bị nhầm. | Nói “x mũ, n trừ k, ngoặc đóng, nhân y mũ k” hoặc “x mũ (n trừ k)”. | PLAUSIBLE |
| L08 | SHOULD | `quymo` step 1 | “Tổng công sức chỉ cỡ n cộng số ràng buộc nếu giữ sẵn bộ đếm số việc phải xong trước của mỗi việc. Nhờ vậy kịp với cả triệu việc.” | Khẳng định đúng (thuật toán Kahn, O(n + số cạnh)), nhưng cả bài không chạy hay minh hoạ bộ đếm: cột “kịp với cả triệu việc” chỉ là lời khẳng định, khác các bài còn lại có chạy cả hai phía. Số tính lại ở phía thử mọi hàng (15! → 21,8 phút; 20! → 77,1 năm) đều khớp. | Thêm một dòng mã hoặc một bảng bộ đếm 6 việc. | CONFIRMED (không có số sai) |
| L10 | SHOULD | `quymo` step 1 | “gom các phần tử cùng nhóm trước (sắp xếp, hoặc dùng khoá băm), rồi chỉ so trong nhóm” | Cách thay thế chỉ nêu lời, không chạy/không đếm. Số phía bình phương (28; 4950; 499500; 49 995 000; 4,99999950×10¹¹; 4,99999995×10¹⁵) đều khớp. | Thêm số cặp còn lại sau khi gom. | CONFIRMED (không có số sai) |
| L02 | SHOULD (P1, nhẹ) | `sym_quant` step 1 | “Cùng một vị từ, đổi miền là đổi chân trị.” | Từ “miền” chỉ được định nghĩa ngầm qua cặp ví dụ ℕ/ℚ ngay trước đó, không có câu giảng thẳng. Đủ hiểu nên giữ P1=2. | Thêm một câu “miền là tập các giá trị x được phép nhận”. | PLAUSIBLE |
| L00, L01, L03, L06, L07 | — | — | — | không phát hiện lỗi | | |

MUST: **1** (L05:example step 3). SHOULD: 8 mục ở trên (4 lệch chữ/hình, 2 khẳng định không minh hoạ, 1 nhập nhằng khi nghe, 1 P1 nhẹ).

## 2. Bảng độ sâu

Phút = độ dài video theo `timeline_seconds` (đã gồm 4–6 phút khoảng dừng cho cảnh Tự làm). P1…P7 theo BRIEF mẫu F, P8/P9 theo Phụ lục. Tổng = P1…P7.

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng | Mất gốc | Cần biết trước (dùng mà không giảng tại chỗ) | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 5f814acbce7bb70b | 15,7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | Python for/range/print/`**`/`//` (PYT L01–L02); câu lệnh `if` ở hook | không đáng kể |
| L01 | 1829657d0b119840 | 14,6 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `from itertools import product`, `product(..., repeat=n)`, `f(*dong)` (chỉ có gợi ý trong de.md); “số nguyên 32 bit” (chỉ gloss “2 mũ 32 giá trị”) | lab cần `import` và dấu `*` mở gói chưa dạy |
| L02 | 6cb79aa0847b75dd | 15,5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `all(...)`/`any(...)` với biểu thức sinh (có giảng ngắn ở `example`); từ “miền” | “miền” chưa giảng thẳng |
| L03 | 736f22896b87ee09 | 16,4 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `while`, `%`, `//`; từ “tối giản” (màn hình chú thích một nửa, lời đọc không giảng) | không đáng kể |
| L04 | aeed027b8ae58d23 | 16,7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `while`, `str(...)`, `//` (de.md gợi ý) | hook “quân cờ”/domino |
| L05 | 0c6bb51c8c9d1873 | 15,2 | 2 | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ (sát ngưỡng) | toán tử tập `\|`, `&`, `-`, `sorted`, `' '.join` (gợi ý de.md); từ “dãy” ở lỗi 4 | P2: lý do sai ở `example` step 3; P3: “vùng đỏ” không đỏ |
| L06 | 9160df8366961ef7 | 15,9 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `from itertools import combinations`, `dict.values()`, `[0] * m`, `.count`; hằng 2654435761 (nói “công thức cố định”) | hằng số băm không giải thích |
| L07 | dbd03fffaeaa49e6 | 15,7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `lambda` (de.md giải), `all` lồng ba `for ... if`, `abs`, `dict.get`; từ “lập phương” | không đáng kể |
| L08 | 5c7547a0e898ac80 | 16,2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `from itertools import permutations`, `.index`, `max`; “bộ đếm số việc phải xong trước” (gloss trong câu, không minh hoạ) | phía “chọn từng phần tử” chỉ nêu lời |
| L09 | 7a084dec3c43f443 | 15,5 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `itertools.product/permutations`, `//` chồng hai lần (có giảng một dấu `//`) | P3: dòng mã tràn khung ở `quymo` |
| L10 | 51995d9a9537fe85 | 16,9 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `math.factorial`, `combinations`, danh sách lồng `d[r][c]`; từ “nhị thức” | “x mũ n trừ k” khi nghe |

Tỉ lệ: **P1=2: 11/11 (100%)**. **P8=2: 11/11 (100%)**. **P9=2: 11/11 (100%)**. Mất gốc ĐỦ 11/11 (thấp nhất L05 = 12). Mục nào cũng chưa có điểm 0.

Cảnh P9 (quy mô) mỗi bài: L00 `quymo` (10/20/30/60 mệnh đề; 1024 → 1,15×10¹⁸ dòng; 36,5 năm), L01 (101 số so với 2³² số, ba cách kiểm), L02 (64 / 5149 / 501499 phép so sánh), L03 (25 / 2500 / 250000 cặp; 4 phút → 8 năm), L04 (n phép cộng so với 1 phép nhân, 10⁹ → 10¹⁸), L05 (n=100 đến 10¹⁵: 17 phút → 11,6 ngày so với 3 phép chia), L06 (1000 / 10⁴ / 10⁵ khoá vào 1000 ô: 2 → 11 → 102 khoá/ô), L07 (n³ bộ ba so với n lần chia), L08 (n! : 8!, 15!, 20!), L09 (PIN 4/6 số, 62⁸, 62¹²: 10 µs → 102 000 năm), L10 (C(n,2) từ 8 tới 10⁸: 58 ngày). Cảnh Tự làm (P8) mỗi bài có `lab: labs/DMS/Lxx`, `pause` 240–360 giây, màn hình có "Kết quả mong đợi" và lệnh `bash labs/cham.sh`, lời đọc dặn “dừng video và tự làm, đừng chép lại ví dụ”.

P7 (giáo án): `objectives` mỗi bài trùng `curriculum/dms.yaml` (11/11 `==`), `covers` khớp cảnh có thật (không thiếu cảnh), mỗi mục tiêu có đúng một cảnh bao phủ.

## 3. Lab

Cách làm: đọc `de.md`, tự viết lời giải (không mở `loi_giai.py`) ở `scratchpad/r2dmsA/lab/Lxx.py`, chấm bằng `bash labs/cham.sh DMS Lxx <tệp>`. Thời gian là ước lượng cho người học (tôi viết nhanh hơn nhiều). Sau đó chạy lại `loi_giai.py` bằng `cham.sh`: 11/11 ĐÚNG. So văn bản “Kết quả mong đợi” trên màn hình (phần `show` của practice step 1, bỏ dòng tiêu đề và dòng lệnh chấm) với `mong_doi.txt`: 11/11 giống từng dòng.

| Bài | Tự làm được | Thời gian (ước) | Kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L00 | có, lần chạy đầu ĐÚNG | 10 phút | không; `int(True)` đã có trong de.md | khớp (10 dòng) |
| L01 | có, ĐÚNG | 20 phút | `product(..., repeat=n)` và `f(*dong)`: video và PYT L00–L03 chưa dạy; làm được nhờ gợi ý de.md | khớp (5) |
| L02 | có, ĐÚNG | 20 phút | không; `all/any` đã giảng ở `example`; chỗ nhỏ: lấy phản ví dụ nhỏ nhất `[... ][0]` | khớp (5) |
| L03 | có, ĐÚNG | 20 phút | viết hàm ước nhỏ nhất (gợi ý trong de.md đủ) | khớp (3) |
| L04 | có, ĐÚNG | 25 phút | định dạng 7 dòng dài, dễ sai dấu cách; phải đọc kỹ de.md | khớp (7) |
| L05 | có, ĐÚNG | 15 phút | không; phép `\|`, `&`, `-` cho tập có trong gợi ý | khớp (6) |
| L06 | có, ĐÚNG | 25 phút | `itertools.combinations` (chỉ gợi ý); đếm “cặp tổng 13” trên 924 tổ hợp | khớp (7) |
| L07 | có, ĐÚNG | 25 phút | phản đối xứng (PDX) dễ viết ngược; định dạng danh sách lớp `print(sorted(lop))` | khớp (4) |
| L08 | có, ĐÚNG | 40 phút | nặng nhất: luật “chọn số lớn nhất còn trống” cùng 7 dòng và đếm 8! hoán vị (40320) | khớp (7) |
| L09 | có, ĐÚNG | 20 phút | dòng 6 (số chẵn) cần hai quy tắc, đã có gợi ý | khớp (6) |
| L10 | có, ĐÚNG | 30 phút | viết `pascal(n)` bằng quy tắc cộng và lưới điền số `d[r][c]` | khớp (5) |

Kết luận lab: đề đủ để tự làm ở 11/11 bài, số liệu khác ví dụ trong bài (L00 biểu thức khác, L03 ba đa thức khác, L05 tập khác, L08 ước của 24 thay cho 12 …). Thiếu kiến thức duy nhất đáng ghi: `import`/`itertools` và dấu `*` mở gói dùng từ L01 mà PYT L00–L03 chưa dạy (kiểm bằng `grep -F` trên `lessons/pyt/L00..L03`: không có `import`, `all(`, `any(`, `itertools`); de.md luôn ghi sẵn dòng `from itertools import ...` nên vẫn làm được bằng cách chép.

## 4. Người học kẹt ở đâu (chỗ đầu tiên không theo được)

| Bài | Chỗ kẹt |
|---|---|
| L00 | không kẹt |
| L01 | không kẹt trên đường video; chỉ kẹt ở lab: `f(*dong)` và `product` (practice step 2), chỉ làm được theo gợi ý |
| L02 | không kẹt |
| L03 | không kẹt thực sự; `example/contradiction` step 1 ①: “phân số tối giản” không được giảng bằng lời |
| L04 | không kẹt (hook nói “quân cờ”, hình là domino) |
| L05 | `example` step 3: “vì không có số nào lớn hơn 1 mà chia hết cho cả 2 lẫn 3” (6 là số lớn hơn 1 chia hết cho cả hai) |
| L06 | `quymo` step 0: `(k * 2654435761) % 2 ** 32 % m` (hằng số và hai `%` chồng, chỉ nói “công thức cố định”); đọc kết quả được, không tự viết lại được |
| L07 | không kẹt |
| L08 | `quymo` step 1: “giữ sẵn bộ đếm số việc phải xong trước của mỗi việc … kịp với cả triệu việc” (không có ví dụ minh hoạ); hasse step 0 “mang tên một nhà toán học ghi trên màn hình” là câu lạ |
| L09 | không kẹt |
| L10 | `binomial` step 1: nghe “x mũ n trừ k” dễ hiểu thành xⁿ − k (nhìn màn hình thì rõ) |

## 5. Số đã tính lại / mã đã chạy

- **Chương trình trên màn hình (cảnh `quymo`) chạy lại:** L00 (1), L01 (1), L02 (2: đếm 64/5149/501499 và `all(any(...))`), L03 (1), L04 (1), L05 (1), L06 (1), L07 (2), L08 (1), L09 (1), L10 (1) = 13 chương trình; **13/13 in đúng từng dòng** như phần “Kết quả chạy thật” trên màn hình (kể cả 271 ô trống ở L06, 10080 hàng hợp lệ ở L08, 3226266762397899821056 ở L09).
- **Lab:** tự viết 11/11 đạt ĐÚNG; `loi_giai` 11/11 ĐÚNG; mong_doi so màn hình 11/11.
- **Số suy ra (thời gian, tỉ lệ, đếm) tính lại bằng Python hoặc tay, khoảng 55 số, 55/55 khớp:** 2⁶⁰/10⁹ = 36,5 năm; 2⁶⁴; 2³²/2; 50+33−16 = 67 (và 666 666 666 667 ở n=10¹²); 10¹²/10⁹ = 16,7 phút; 10¹⁵/10⁹ = 11,57 ngày; 250 000 cặp; (10⁶/2)²/10⁹/60 = 4,17 phút; (10⁹/2)²/10⁹ = 7,92 năm; 10¹⁸/10⁹ = 31,7 năm; 26⁸ = 208 827 064 576 (209 s); 36⁸ (47 phút); A(26,8) = 62 990 928 000 (tỉ số 3,32); 62⁸ (2,53 ngày); 62¹² (102 234 năm, 37 341 050 ngày); 15!/10⁹ = 21,8 phút; 20!/10⁹ = 77,1 năm; 8!/6! = 56; C(10,6) = 210; C(12,7) = 792 và C(12,6) − 2⁶ = 860; C(10⁸,2)/10⁹ = 57,9 ngày; C(12,3) − C(7,3) = 185; n²+n+41 tại n=38,39,40 = 1523, 1601, 1681 = 41²; ba đa thức lab L03 (n=16, 29, 80); số hàng tô pô của {1,2,3,4,6,12} = 5 và của ước 24 = 14; số cạnh Hasse 7 và 10; cạnh/cặp 12 = 5+3+2+1+1.
- **Không chạy được/không cần:** C-style `if (!(du_tuoi && co_ve)) chan();` ở L01 chỉ đọc (đã suy bằng tay: người đủ tuổi, không vé → bị chặn bởi bản đầu, lọt bởi bản gọn).
- **Số có nguồn ngoài:** không có khẳng định thực tế cần nguồn; “36,5 năm”, “8 năm”… đều dán nhãn “số minh hoạ ở một tỉ phép mỗi giây”. Không có mục nào ở trạng thái "chưa kiểm được nguồn". Câu chuyện “Euler n²+n+41 (1772)” ở L03 chỉ nằm trong trường `source`, lời đọc không nêu năm.

## 6. Khung hình đã xem (≥ 5 mỗi bài) và lỗi hiển thị

Xem riêng từng khung bằng công cụ Read; cộng một ảnh ghép thu nhỏ (4×3) của khung đáp án quiz và một của khung tổng kết cho cả 11 bài (kiểm tràn/đè ở mức thô), cộng quét điểm ảnh lề trái/phải của toàn bộ 1216 khung.

- L00: `00000, 00046, 00054, 00087, 00096, 00108` (hook, cây chân trị, bảng cột trung gian, quiz, mã quy mô, đề Tự làm)
- L01: `00000, 00033, 00038, 00058, 00089` (mã hook, lưới 4 ô, De Morgan trong mã, mã quy mô, đề Tự làm)
- L02: `00002, 00036, 00069, 00076, 00100` (hook, hàng đèn, mã đếm, `all(any)`, đề Tự làm)
- L03: `00000, 00038, 00046, 00073, 00101` (hook 40 ví dụ, chứng minh √2, ba con đường, mã quy mô, đề Tự làm)
- L04: `00022, 00028, 00047, 00060, 00093` (domino Q(n), chứng minh quy nạp, tự kiểm, mã quy mô, đề Tự làm)
- L05: `00020, 00033, 00041, 00065, 00096` (∪∩∖, Venn, các bước bao hàm–loại trừ, mã quy mô, đề Tự làm)
- L06: `00023, 00037, 00060, 00063, 00088` (đơn/toàn/song ánh, chuồng–bồ câu, mã bảng băm, bảng tổng, đề Tự làm)
- L07: `00019, 00032, 00038, 00067, 00093` (ba tính chất, cụm khép kín, kiểm 3 bước, bảng n³, đề Tự làm)
- L08: `00020, 00031, 00056, 00066, 00086` (Hasse, thuật toán tô pô, mã hoán vị, lỗi thừa cạnh, đề Tự làm)
- L09: `00000, 00033, 00056, 00061, 00084` (bảng mật khẩu, cây lựa chọn, mã quy mô, lỗi 1, đề Tự làm)
- L10: `00018, 00023, 00035, 00062, 00088` (Pascal, nhị thức, lưới đường đi, mã bắt tay, đề Tự làm)
- Ảnh ghép: `mont_quiz.png` (đáp án quiz L00–L10), `mont_recap.png` (tổng kết L00–L10) trong `scratchpad/r2dmsA/`.

Lỗi hiển thị: L09 `quymo` (khung 00053–00056) dòng `print(...)` tràn khung mã (chữ vẫn nằm trong khung hình, không cắt). L05 `intuition`: phần giao không đỏ. Còn lại: không thấy chữ tràn, đè hay cắt; cỡ chữ đọc được; hình sơ đồ (cây chân trị, domino, chuồng bồ câu, Hasse, lưới Pascal, quan hệ) khớp lời đọc. Hình Hasse L08 (7 cạnh) và hình lỗi 1 (hai nét đứt 1–4, 1–12) đúng theo phép tính.

## 7. Nhận xét chung

- Cấu trúc 11 bài đồng nhất và chắc: hook → ôn nền có số → giải mã ký hiệu → ví dụ từng bước có “Thử” bằng số → hai “đường khác” kiểm lại → cảnh quy mô có mã chạy thật → 4 lỗi hay mắc → quiz có lời giải từng bước → Tự làm với lab. Mọi con số trên màn hình mà tôi chạy lại đều khớp.
- Chỉ một lỗi kiến thức thật (L05 step 3, lời đọc), sửa một câu. Các SHOULD còn lại là chi tiết nhãn/hiển thị hoặc khẳng định chưa minh hoạ (L08/L10 phía “giải pháp thay thế” chỉ bằng lời).
- Mục tiêu chốt: MUST 0 chưa đạt (còn 1, dễ sửa); P1=2 đạt 11/11 theo chuẩn nêu ở đầu; P8=2 đạt 11/11; P9=2 đạt 11/11.
- Tự đủ trong DMS: không bài nào gọi khoá khác; chỉ nhắc “bài k” của chính DMS, và L00 nhắc câu lệnh `if` như một ví dụ động cơ, không cần kiến thức đó để theo bài.
- Rủi ro cho người “mất gốc, chỉ có Python cơ bản”: từ L01 lab dùng `import itertools` và `*` mở gói, từ L06 `combinations`/`permutations`; các bài này chỉ dạy qua gợi ý trong de.md, không dạy trong video hay trong PYT L00–L03. Làm được bằng cách chép, nhưng chưa hiểu. Đề nghị: thêm một câu về `import` ở lần đầu (L01) hoặc thêm PYT L08 vào `requires_ext`.
- Kiểm âm thanh độc lập chưa làm (không được chạy asr/tts); độ tin ở phần lời đọc dựa vào SRT = `say` và `asr_report.md` của máy (gắn cờ đều đã xem xét).
- Ghi chú phương pháp: tôi đã ghi đè một tệp cũ `scratchpad/chk.py` của phiên trước trong thư mục tạm dùng chung; không ảnh hưởng kho.
