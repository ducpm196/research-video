# S01b FND: đã đọc 11/11 bài

Phương pháp: đọc trọn `title/objectives/show/say/checks/quiz` của 11 YAML (qua bộ trích văn bản bỏ thẻ HTML), đối chiếu `curriculum/fnd.yaml`, so SRT với `say`, xem 66 khung hình (6 mỗi bài), chạy lab như người học (tự viết lời giải trong scratchpad, chấm bằng `labs/cham.sh`, không mở `loi_giai.*`), chạy lại mọi lệnh của bài có thể chạy. Không mở báo cáo/kế hoạch cũ.

Môi trường: Git Bash (git 2.53, bash MSYS), JDK 21.0.13, Python 3.11.9, curl. **Không có `sqlite3` dòng lệnh chính thức** (xem mục Lab).

## 1. Bảng chuẩn xác (chỉ lỗi có bằng chứng)

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L08 | **MUST** | example ② -> ③, ⑤; check step 1 | ② `UPDATE tai_khoan SET ten = 'An Le' WHERE ma = 1;` và `DELETE FROM giao_dich WHERE id = 2;` rồi ③ in `1\|An\|0`, ⑤ in `1\|An\|400000`, check in `1\|300000 ... 1000000` | Các cảnh là một phiên liền (cùng `$DB`), nhưng kết quả ③, ⑤ và check chỉ đúng với CSDL dựng lại từ `dung.sql`. Chạy liền một phiên (Python sqlite3 3.45.1, cùng câu lệnh): ③ ra `1\|An Le\|0`; ⑤ ra `1\|An Le\|400000`; nhóm theo tk ra `1\|350000 ... 1050000` (vì id=2 đã xoá, không rollback). Mã dựng video (`audit/fnd/src/l08.py` dòng 41, 45, 51, 58) chạy lại `DB=...; sqlite3 $DB < dung.sql` giữa các nhóm, nhưng bước dựng lại KHÔNG hiện trên màn hình; khung hình example ③ (L08 frame 63) hiện `An` ngay sau cảnh đổi thành `An Le`. Người học làm theo từng dòng sẽ thấy khác video; chạy lại `sqlite3 $DB < dung.sql` trên DB cũ còn báo lỗi bảng đã tồn tại. Ảnh hưởng tri thức thấp, nhưng đúng điều "ví dụ tự mâu thuẫn giữa các cảnh" của tiêu chí MUST | Thêm vào ③, ⑤ và check một dòng `rm -f ngan_hang.db; sqlite3 $DB < dung.sql` (hoặc đổi ② thành SELECT/ROLLBACK, không để lại dấu vết) và nói rõ "dựng lại CSDL" trong say | CONFIRMED |
| L01, L03 | SHOULD | prereq step 1 | say: "Ta ôn lại bốn điều." | Bảng có 5 hàng ① đến ⑤ và lời đọc cũng kể 5 điều (L01: tệp, thư mục, cây, trình duyệt thư mục, tệp lệnh; L03: tệp văn bản, tệp bảng, in nội dung, chuyển hướng, khối chữ nhúng). Lời đọc lệch màn hình ở chi tiết nhỏ | Đổi "bốn" thành "năm" | CONFIRMED |
| L02 | SHOULD | intuition step 2 (frame `out/FND/L02/frames/00040.png`) | hình so `>` với `>>` | Chữ trong ô xanh bị đè lên viền: dòng "tệp ghi.txt" đè viền trên, "dòng mới" đè viền dưới (ô quá thấp cho 4 dòng); nhãn "echo >> (nối)" bị mũi tên cắt ngang. Đã xem ở độ phân giải đầy đủ | Tăng chiều cao ô, dời nhãn | CONFIRMED |
| L06 | SHOULD | sym step 1 | "bốn kiểu giá trị: chữ (nháy kép), số, đúng/sai viết thường, rỗng" | RFC 8259: giá trị JSON gồm cả đối tượng và mảng (ngay cả bài vừa dạy `{ }` và `[ ]` lồng làm giá trị: `"hang": [ {...} ]`). Nói "bốn kiểu" thiếu hai kiểu cấu trúc | "bốn kiểu đơn giản, cộng đối tượng và mảng" | CONFIRMED (RFC 8259 mục 3) |
| L07 | SHOULD | check step 1; example nhãn ④ | "Cách 2: đọc dòng đầu của -i ở trên / $ curl -s $U/ / xin chao" | Cách 2 không dùng `-i`, không in mã, và hỏi địa chỉ khác (`/`) với Cách 1 (`/khong_co`), nên không so được "hai cách cùng một mã" như lời đọc nói. Ngoài ra example có hai bước cùng nhãn ④ (Phương thức gửi; Sự cố ở máy chủ) và tiêu đề nói "năm phép" trong khi có 6 bước | Cách 2: `curl -s -i $U/khong_co \| head -n 1` ra `HTTP/1.1 404 Not Found`; đánh số lại | CONFIRMED |
| L08 | SHOULD | formula step 1, 3 vs 4; scale step 2 | tai_khoan: An 500000, Binh 1200000, Chi 300000; "số dư của từng tài khoản theo sổ giao dịch": 300000, 400000, 300000 | Hai bảng của cùng bài cho số dư khác nhau (An 500000 vs 300000; Binh 1200000 vs 400000) mà không nói (vd số dư đầu kỳ); người học dễ thắc mắc. Cột "có chỉ mục (tìm nhị phân)" 3/10/17 bước là cận của tìm nhị phân (ceil(log2 n), đã tính lại khớp); chỉ mục thật của SQLite là cây B (số trang đọc còn ít hơn nhiều), và bài không bao giờ hiện `CREATE INDEX` | Nói "số dư ở hai bảng độc lập, chỉ để minh hoạ GROUP BY" hoặc cho khớp số; ghi "cận trên" và thêm một dòng `CREATE INDEX` | CONFIRMED (khác biệt số); PLAUSIBLE (B-tree) |
| L09 | SHOULD | formula step 2-5, example, pitfalls | `git status -s` / `git add` / `git commit` | Trên Windows (git 2.53, `core.autocrlf=true` mặc định của bộ cài) mỗi lần add/diff/commit in `warning: in the working copy of 'so_du.txt', LF will be replaced by CRLF the next time Git touches it` ra màn hình người học; video không có dòng này, bài không nhắc (chỉ `de.md` nhắc ở lab). Đã chạy: dòng cảnh báo xuất hiện 6 lần trong phiên mẫu | Thêm một câu giải thích (nối với L05) hoặc đặt `git config core.autocrlf false` trong bước khai tên | CONFIRMED |
| L04, L05, L06, L10 | SHOULD | L04 formula step 1-3; L05 example step 2-3, check step 2, pitfalls 1; L06 pitfalls 3; L10 hook, formula step 1-3 | các tệp `chao` trong `tien_ich`/`hai`, `loi.py`, `crlf.sh`, `Quote.java`, `kh_ngoac.csv`, `so_tay_loi.sh`; `so_tay.sh` bị chẻ ba cảnh | Ví dụ dùng tệp mà màn hình không hiện nội dung nên người học không dựng lại để tự chạy được (L04: cần `chmod +x`, dòng đầu `#!`; L10: tệp `so_tay.sh` phải tự ghép từ ba cảnh, dòng `EOF` nằm ở đầu cảnh sau). Đã tự ghép và chạy được (khớp 3150000 / 130000000), nhưng người mất gốc dễ kẹt | Hiện nội dung tệp một lần, hoặc đưa vào `de.md` | CONFIRMED |

Không phát hiện sai kiến thức ở các bài còn lại (L00, L03 phần kiến thức, L05, L06 phần còn lại, L07 phần còn lại, L09, L10). Nguồn trích dẫn "chưa kiểm được nguồn": Roediger & Karpicke 2006 (L00), Little 1961 (L07), MAX_PATH 260 (L01) đều khớp hiểu biết chung, bài đã tự ghi NOT_VERIFIED trong `source`.

## 2. Bảng độ sâu

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1-P7) | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | ae1a0c7115f8b234 | 17,4 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | Git/Java/Python chỉ nêu là "công cụ" (không nói để làm gì); File Explorer, chuột phải | Không có chỉ dẫn các lựa chọn trong trình cài Git/JDK (chỉ "Add to PATH" của Python) |
| L01 | a213bbdc8357e56d | 14,8 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `mkdir -p`, `touch` (bài nói "học sau") | prereq nói "bốn" kể năm |
| L02 | 936327d5567455fb | 16,0 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ | "biến" (dùng ở khối chữ nhúng trước khi giảng ở lỗi 3), dấu nháy trong `echo "..."` | Hình `>`/`>>` đè chữ (frame 00040) |
| L03 | 5a31383a9208a066 | 15,8 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `wc -c` (cờ c không nói là byte), "ngoại suy", `2>` không có ví dụ chạy | prereq nói "bốn" kể năm |
| L04 | 078ada8c83be1ec6 | 16,9 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | quyền chạy tệp (chmod) chỉ nói chức năng; `cut -f1-2`; `2>&1` | Tệp `chao` ở formula không hiện cách tạo |
| L05 | be4d9bf71c662c28 | 18,5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | cú pháp Java (class/main) chỉ để đọc lỗi; `sed -i`; `2>&1` | `loi.py`, `Quote.java`, `crlf.sh` không hiện |
| L06 | cb1427e92d635f22 | 16,3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | cú pháp Python trong `-c` (được giảng từng phần); "nén" | "bốn kiểu giá trị" thiếu đối tượng/mảng |
| L07 | 35d27addd0bba6cc | 17,8 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | "hàng đợi", "giãn dần khoảng cách"; `2>&1` | Check step 1 không so hai cách thật |
| L08 | cb8e55063d4b4c5e | 18,2 | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ | "tìm nhị phân"/log2 chưa giảng (mới giảng ở L09), lệnh chấm của sqlite3 (`.import`) | Mâu thuẫn phiên liền (MUST); "17 bước" không dẫn ra cách tính |
| L09 | 1cb7832bf6a37bdb | 17,9 | 1 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 12 | ĐỦ | "con trỏ", "tua nhanh" (fast-forward) | Không có xung đột gộp, không có kho từ xa; cảnh báo LF/CRLF không giải thích |
| L10 | 17837c848d6a7ad0 | 21,1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | "máy chủ cơ sở dữ liệu" (nêu ở cảnh quy mô, không giảng) | `so_tay.sh` chẻ ba cảnh; `so_tay_loi.sh` không hiện |

Ngưỡng: **P1 = 2 ở 8/11 bài (73%), dưới ngưỡng 90%** (ba bài mức biên L02, L08, L09, mỗi bài 1 đến 2 từ; sửa được bằng một câu giảng mỗi bài). **P8 = 2 ở 11/11 (100%)**. P9 = 2 ở 11/11. Mất gốc ĐỦ 11/11 (tổng 12 đến 14, không mục nào 0).
Ghi chú Phút: lấy từ `build_report.json` (`timeline_seconds`), SRT khớp `say` từng chữ ở cả 11 bài (so từ-theo-từ, tỉ lệ khớp 1,0000); không nghe được âm thanh nên không đánh giá giọng.

## 3. Lab (làm như người học)

| Bài | Tự làm được (có/không/phần) | Thời gian (pause trong video; chạy chấm) | Kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L00 | phần | pause 120 s; chấm 1 s | Máy kiểm thiếu sqlite3 nên dòng 6 là `THIEU sqlite3` (5/6 dòng đạt; cham.sh báo KHÁC đúng như thiết kế). Bài dạy cài: trang sqlite.org/download.html có mục "Precompiled Binaries for Windows" và tệp `sqlite-tools-win-x64-*.zip` (WebFetch xác nhận); `/etc/profile.d/env.sh` dòng 2 `export PATH="$HOME/bin:$PATH"` và PATH máy kiểm có `/c/Users/AI_Worker/bin` (khớp lời bài); lần đầu mở Git Bash có tạo `~/.bash_profile` nạp `~/.bashrc`. Kết luận: bài dạy cài và kiểm đủ để người học làm được; không chạy được phần sqlite3 vì thiếu sqlite3 (không phải lỗi bài) | có (6 dòng ✔) |
| L01 | có | 150 s; ĐÚNG | không | có |
| L02 | có | 180 s; ĐÚNG | không | có |
| L03 | có | 240 s; ĐÚNG | không | có |
| L04 | có | 300 s; ĐÚNG | cần JDK 21 chính xác (`javac 21`; máy có thêm JDK 22 ở PATH sau, không ảnh hưởng) | có |
| L05 | có | 300 s; ĐÚNG | không | có |
| L06 | có | 300 s; ĐÚNG | không | có |
| L07 | có | 300 s; ĐÚNG (1,8 s; máy chủ cổng 18766) | không | có |
| L08 | phần | 300 s; ĐÚNG qua đường dự phòng của `cham.sh` (`labs/sqlrun.py`, mô-đun Python sqlite3 3.45.1), không phải `sqlite3` dòng lệnh chính thức | Không chạy được bằng sqlite3 chính thức vì thiếu sqlite3. Lab chỉ cần SQL thường nên đường dự phòng đủ; bài dạy cài ở L00 | có |
| L09 | có | 300 s; ĐÚNG | cảnh báo LF/CRLF ở luồng lỗi (de.md đã nói) | có |
| L10 | phần | 420 s; ĐÚNG chỉ khi đặt `audit/fnd/shim` (sqlite3 giả bằng Python) vào PATH; không có shim thì lệnh `sqlite3` báo not found và kịch bản in `LECH:  13530000` | Không chạy được bằng sqlite3 chính thức vì thiếu sqlite3. Lab dùng `.import --csv --skip 1`, cần sqlite3 CLI thật (de.md đã ghi rõ là bắt buộc) | có (với shim) |

Đề đủ để tự làm? Có ở cả 11 bài; kiến thức thiếu mà đề tự bù bằng gợi ý: L04 (`cut -d' ' -f1-2`, `2>&1` chỉ có ở gợi ý), L10 (hai cách nạp CSV). Cả 11 lab đều có số khác ví dụ (đúng quy ước ENV.md).

## 4. Người học kẹt ở đâu

- L00: chuanbi step 1-2, cài Git/JDK/Python không có chỉ dẫn lựa chọn trong trình cài (chỉ "Add to PATH" của Python); sau đó có "Nếu kẹt" cho THIEU python/javac/sqlite3 (chưa kiểm được nguồn: JDK Temurin có tự thêm PATH hay không tuỳ tuỳ chọn khi cài).
- L01: không kẹt.
- L02: example step 6 "Nháy quanh EOF: máy không thay biến bên trong" (biến chưa giảng, giảng ở pitfalls 3).
- L03: không kẹt (chỉ `wc -c` ở scale step 1 chưa nói c là byte).
- L04: formula step 1 `$ chao` / `ban tien ich`: người học không thấy tệp `chao` và thư mục `tien_ich`, `hai` được tạo thế nào (cần dòng đầu `#!` hoặc chmod).
- L05: example step 2 `python loi.py 2>&1 | tail -n 1`: tệp `loi.py` chưa từng hiện nội dung.
- L06: không kẹt (pitfalls 3 `kh_ngoac.csv` không hiện nội dung, không chặn).
- L07: không kẹt (check step 1 Cách 2 lệch nhẹ).
- L08: example ③ `1|An|0`: chạy liền ra `1|An Le|0`, người học nghĩ mình sai.
- L09: formula step 2 `git status -s` / step 3 `git add`: dòng `warning: ... LF will be replaced by CRLF` không có trong video, không giải thích.
- L10: formula step 1-3: phải tự ghép `so_tay.sh` từ ba cảnh (dòng `EOF` đầu cảnh 2 và 3 là dấu kết khối của cảnh trước).

## 5. Số đã tính lại / mã đã chạy

- 173/173 biểu thức `checks` trong 11 YAML tính lại bằng Python: 173 đúng.
- Số tự tính thêm ngoài `checks`: thời gian L00 (27 giờ 46 phút 40 giây; 115,7 ngày; 16,7 phút; 27,8 giờ), chiều dài đường dẫn L01 (38/254/263), dung lượng L03 (27/4893/728895 byte), xác suất L04 (1,0/9,5/63,2%), nhị phân/UTF-8 L05 (259=100000011, c4 83, e1 bb 85, Nguyễn 8 byte), dung lượng CSV/JSON L06 (15/39; 1592/3992; 178894/418894), người phục vụ L07 (1/100/10000), tổng/nhóm L08, số lần thử chia đôi L09 (3/10/17), dung lượng và tổng L10 (292; 248221; 130000000; 3150000; 6300000): tất cả khớp (ngoài MUST L08 là mâu thuẫn phiên, không phải số sai).
- Lệnh trên màn hình đã chạy thật (Git Bash/JDK 21/Python 3.11/curl/git 2.53): khoảng 90 đầu ra so với màn hình, khớp, trừ các ghi chú: Python 3.11 thêm gợi ý "Did you mean" ở lỗi NameError (dòng cuối vẫn là NameError, lệnh `tail -n 1` của bài vẫn đúng ý); `curl -w "%{http_code}\n"` in thêm ký tự CR trên Windows (vô hình); cảnh báo CRLF của git (xem SHOULD L09); mô phỏng L08 bằng Python sqlite3 (không có sqlite3 CLI); L10 bằng shim.
- Không chạy: `rm * .txt` ở hook L02 (bộ kiểm an toàn chặn lệnh rm có glob; chỉ đọc), `git bisect` (bài chỉ nêu), kịch bản `so_tay_loi.sh` (không có nội dung; đã mô phỏng bằng nhân đôi nạp).
- Lab: 11/11 tệp lời giải của tôi được `cham.sh` chấm ĐÚNG, riêng L00 5/6 dòng (thiếu sqlite3), L08 qua `sqlrun.py`, L10 qua shim.

## 6. Khung hình đã xem (6 mỗi bài, chọn theo khung câu cuối của bước: mở đầu, hình cơ chế, ví dụ, quy mô, quiz, Tự làm hoặc tổng kết) và lỗi hiển thị

| Bài | Khung (số thứ tự, = số câu SRT) |
|---|---|
| L00 | 00004, 00026, 00055, 00079, 00141, 00168 |
| L01 | 00004, 00035, 00060, 00077, 00109, 00125 |
| L02 | 00008, 00040 (và cắt đầy đủ), 00081, 00098, 00122, 00134 |
| L03 | 00004, 00034, 00062, 00079, 00098, 00113 |
| L04 | 00003, 00030, 00057, 00077, 00099, 00112 |
| L05 | 00006, 00036, 00050, 00091, 00112, 00125 |
| L06 | 00003, 00027, 00053, 00070, 00095, 00105 |
| L07 | 00003, 00033, 00058, 00083, 00106, 00122 |
| L08 | 00003, 00030, 00063, 00089, 00110, 00122 |
| L09 | 00003, 00036, 00067, 00088, 00111, 00126 |
| L10 | 00004, 00033, 00057, 00092, 00112, 00125 |

Lỗi hiển thị: (1) L02 frame 00040 chữ đè viền hộp và nhãn bị mũi tên cắt (SHOULD ở mục 1). (2) Nhận xét chung: nhãn trong hình SVG (L00, L04, L06, L09, L10) cao khoảng 20 px trên khung 1080p, đọc được nhưng nhỏ; mọi khung nội dung chiếm nửa trên, nửa dưới trống (không lỗi, chỉ lãng phí chỗ). (3) L09 hình nhánh vẽ gộp thật (main có chốt 3) trong khi ví dụ là tua nhanh (nhãn ghi "hoặc tua nhanh"), không lệch tri thức. Không thấy chữ tràn/cắt ở 65 khung còn lại; không có cách tự động kiểm hết 3 071 khung (thử quét viền nhưng thanh chú thích tối làm quét vô nghĩa, bỏ).

## 7. Nhận xét chung

- Kết luận so ngưỡng: MUST = 1 (L08, mâu thuẫn phiên liền), nên chưa đạt MUST 0; P1 = 2 ở 73% (dưới 90%); P8 = 2 ở 100% (đạt).
- Chất lượng kiến thức rất tốt: 173/173 phép kiểm, ~90 đầu ra khớp, lời đọc khớp `say` từng chữ ở cả 11 bài, mục giáo án khớp 11/11 (mục tiêu = curriculum, covers đủ).
- Điểm mạnh lặp lại: mỗi bài có hook tình huống, "ôn lại", quiz có dừng và lời giải từng bước, lab có số khác ví dụ, đo quy mô ở 2 đến 3 mức và đánh đổi (L00 đến L10 đều có).
- Lỗi lặp lại duy nhất đáng sửa: ví dụ dựa vào tệp không hiện nội dung (L04, L05, L06, L10) và lời "ôn lại bốn điều" lệch số (L01, L03).
- Phụ thuộc môi trường: L08, L10 cần sqlite3 CLI thật; bài L00 dạy cài đủ (đã đối chiếu trang tải sqlite.org và cơ chế `$HOME/bin`), nhưng không có kiểm tra tự động nào ở L08/L10 báo "thiếu sqlite3" thân thiện (L10 khi thiếu in `LECH:` gây hiểu nhầm là sai số, trong khi nguyên nhân là lệnh không tồn tại).
- Khoảng trống chuyên sâu (không phải lỗi): L09 chỉ tua nhanh, không xung đột gộp, không kho từ xa; không có bài nào trong FND đụng đến quyền tệp/biến môi trường cho Windows PowerShell (đúng phạm vi: chỉ Git Bash).
- Dư địa cải thiện nhanh (không đụng nội dung dạy): thêm một dòng dựng lại CSDL ở L08, sửa "bốn thành năm", hiện nội dung tệp còn thiếu, tăng ô hình L02.
