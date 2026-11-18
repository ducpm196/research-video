# S01c FND (vòng 3): đã đọc 11/11 bài

Ngày đọc 2026-11-14. Tiêu chí: `sample_f/BRIEF.md` + `audit_final/ADDENDUM.md` + `BRIEF_READ_S01.md`. Người đọc độc lập; không mở báo cáo/plan/handover nào khác. Ghi chú trung thực: tôi có mở `out/FND/L00/asr_report.md` và `out/FND/L10/asr_report.md` (đầu ra dựng, không thuộc `reports/`) để xem đầu tệp, không dựa vào chúng để chấm.

Máy kiểm: Git Bash (Git 2.53), JDK 21.0.13, Python 3.11.9 (cũng có 3.13), curl 8.18, **không có `sqlite3` CLI**. Mọi tệp tạm nằm ở scratchpad; không ghi gì vào kho ngoài báo cáo này.

## 0. Toàn vẹn video
- `spec_sha256` trong `out/FND/Lxx/build_report.json` so với `lv.spec_digest` của YAML hiện tại: **11/11 khớp** (đầy đủ 64 ký tự).
- Từng câu `say` (ghép theo thứ tự cảnh/bước) so với `Lxx.srt`: **11/11 giống từng chữ**, tổng 1 552 khối phụ đề = 1 552 khung (L00 169, L01 139, L02 148, L03 130, L04 128, L05 141, L06 120, L07 138, L08 147, L09 146, L10 146).
- Thời lượng mp4 (ffprobe) = `timeline_seconds` ở cả 11 bài (L00 1042,3 s … L10 1284,9 s). Giọng duy nhất `vi-VN-NamMinhNeural`. `tts_sources` mỗi bài có 1 khung nhãn `edge?` (không kiểm được nghĩa nhãn; không thấy lỗi nghe/đọc ở SRT).
- Mục `curriculum/fnd.yaml` (title, objectives) = YAML bài: 11/11; `covers` phủ đủ mọi mục tiêu: 11/11.

## 1. Bảng chuẩn xác (chỉ lỗi có bằng chứng chạy)
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L00 | **MUST** | `practice` step #36 (và `de.md`, kiem.sh `chuanbi` #25) | "Dòng THIEU python: có thể bạn chưa đánh dấu “Add to PATH”, hoặc máy mở cửa hàng ứng dụng thay cho Python" | `kiem.sh` dùng `command -v python`. Trên Windows 10/11 chưa cài Python, lối tắt Microsoft Store (`WindowsApps\python.exe`) vẫn nằm trong PATH nên `command -v` **thấy** nó và in `✔ python`, không phải `THIEU`. Chạy lại: `env PATH=/usr/bin:/mingw64/bin:<WindowsApps> bash -c 'command -v python; python --version'` → `.../WindowsApps/python` rồi "Python was not found; run without arguments to install from the Microsoft Store"; vòng `for ten in python` in `✔ python`. Máy học sai trạng thái "đủ 6 dấu tích" mà chưa có Python; mục tiêu 5 ("kiểm máy bằng tệp lệnh") không đạt đúng ca phổ biến nhất. (`labs/cham.sh` có chú thích chính về lối tắt này nhưng bài không dạy.) | kiem.sh thử chạy thật: `python --version >/dev/null 2>&1 && echo ✔ python \|\| echo THIEU python` (tương tự javac/sqlite3); sửa câu "kẹt" cho khớp | CONFIRMED |
| L04 | SHOULD | `formula` step #8 (`chmod +x`) | "không có quyền này, tệp chỉ là chữ, máy không chạy nó như một lệnh" | Đúng trên Linux/macOS; **sai trên Git Bash/NTFS của người học**: `ls -l` vẫn `-rw-r--r--` sau `chmod +x`, và tệp `nochmod/chao` (không chmod) vẫn chạy được qua PATH (`chao` → "no chmod", rc=0; `mount`: `ntfs (binary,noacl…)`). | Thêm điều kiện: "trên Linux/macOS bắt buộc; Git Bash trên Windows luôn chạy được nhưng cứ gõ để thói quen đúng" | CONFIRMED |
| L04 | SHOULD | lab `practice` #28–#29 + `labs/FND/L04/de.md` | "in lần lượt (bảy dòng): … mã thoát của ls . và của ls khong_co (giấu thông báo lỗi), dạng ls: 0, ls loi: 2" | Chỉ hướng dẫn giấu lỗi của `ls khong_co`; `ls .` in cả danh sách thư mục ra màn hình. Bản tự viết theo đề: chạy tay in thêm `kiem_tra.sh`; `cham.sh` báo KHÁC (`4,5d3 < _err < _out`). Lời giải mới có `ls . > /dev/null`. | Thêm vào đề/cảnh: `ls . > /dev/null` | CONFIRMED |
| L04 | SHOULD | `check` step #19 | tiêu đề "Đối chiếu danh sách đang có" + đầu ra `/usr/bin` `/bin` (2 dòng) | Sau các bước ②③ PATH đã có 4 thư mục; chạy lại đúng chuỗi lệnh cho 4 dòng (`.../hai`, `.../tien_ich`, `/usr/bin`, `/bin`). Lời đọc nói đúng "ban đầu", màn hình ghi "đang có" (khung 70). | Đổi nhãn thành "danh sách ban đầu" hoặc in 4 dòng | CONFIRMED |
| L02 | SHOULD | `formula` #11, `hook` #2 | "Dấu sao đứng một mình khớp mọi tệp" / "`*` khớp mọi chuỗi" | `*` không khớp tệp ẩn (tên bắt đầu bằng dấu chấm, vừa học ở L01): `touch a.txt b.txt c.png .hid; echo *` → `a.txt b.txt c.png`. | Thêm "trừ tệp ẩn" | CONFIRMED |
| L06 | SHOULD | `scale` step #18 | "Một nghìn lần nhiều hơn cũng thế, JSON luôn to hơn gấp hơn hai lần" | Bảng cùng cảnh có hàng ×100 (100 bản ghi) và ×10 000 (10 000 bản ghi); không có mốc "một nghìn lần". Tỉ lệ đo lại đúng (39/15=2,6; 3992/1592=2,5; 418894/178894=2,3). | Đọc "một trăm rồi mười nghìn lần" | CONFIRMED |
| L06 | SHOULD | `quiz` #25 | "với 10 triệu bản ghi đồng dạng, chọn CSV …" | Đề (#23, `tk.json`) có mảng lồng `cac_the` độ dài thay đổi; chính bài dạy "CSV không lồng nhau được" (#6) và "Chọn JSON khi bản ghi lồng nhau". Lời giải bỏ qua yếu tố quyết định của đề. | Đề đổi bản ghi phẳng, hoặc lời giải nói "phải làm phẳng trước" | PLAUSIBLE |
| L00 | SHOULD | `chuanbi` #22–#27, `practice` | "máy sẵn sàng khi tệp kiểm in sáu dấu tích" | `kiem.sh` chỉ kiểm có/không, không kiểm phiên bản, trong khi lab L04 cần `javac 21`, L09 cần Git ≥ 2.28 (`-b`, `--show-current`), L10 cần `sqlite3` có `.import --skip` (≥ 3.32). JDK 8 hoặc Python 2 vẫn ✔. | kiem.sh in thêm phiên bản (hoặc nhắc `bash labs/check_env.sh`) | PLAUSIBLE |
| L08 | SHOULD (thấp) | `check` #18 và `pitfalls` #24 | `INSERT INTO tai_khoan VALUES (4, 'Dung', NULL);` hai lần | Chạy tuần tự trên cùng DB: lần hai báo `UNIQUE constraint failed: tai_khoan.ma` (đã chạy lại bằng engine SQLite 3.45.1 của Python). Người học gõ theo sẽ gặp lỗi chưa được giảng. | Ghi "đã chèn ở cảnh trước" hoặc dùng mã 5 | CONFIRMED |
| L01,L02,L03,L05,L07,L09,L10 | — | | | không phát hiện lỗi chuẩn xác | | |

MUST = 1 (L00). Các số, mã, lệnh khác khớp (mục 6).

## 2. Bảng độ sâu (P1…P7 0/1/2; P8, P9 tách riêng)
Quy ước P1: từ kỹ thuật không được giảng tại chỗ nhưng nằm ở lời dẫn phụ (ví dụ nhãn công cụ) ghi ở cột "Cần biết trước" và chỉ trừ điểm khi ≥ 3 từ hoặc nằm trên đường dạy chính.
| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | fa0f8f98388db1a2 | 17,4 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 13 | ĐỦ | Git/Java/Python/SQL chỉ là tên công cụ; "biến" trong kiem.sh | kiem.sh sai ca Store-stub (mục tiêu 5), không kiểm phiên bản |
| L01 | 7724fa785a7cfbb9 | 14,8 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | "máy chủ Linux", "hệ tệp" (lỗi 3) | — |
| L02 | 41248acc473ad515 | 16,0 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | — | `*` và tệp ẩn |
| L03 | 91c861cca6709b35 | 15,9 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | MB, GB, "ngoại suy", "sổ cái" (bảng scale) | ba từ trên màn hình chưa giảng |
| L04 | 22b1d9e2f685b5bc | 17,3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | "xác suất", "độc lập" (cảnh scale) | chmod trên Windows; đề lab thiếu `> /dev/null`; nhãn PATH |
| L05 | 6ed5536da7ce4ed9 | 18,7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | "lũy thừa" (giảng gián tiếp), Linux/macOS | — |
| L06 | 73e2ce920a7a6c7c | 16,4 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | "cú pháp", "bộ đọc/bộ kiểm", YAML danh sách dạng `[a, b]` ở lab | lời đọc "một nghìn lần"; quiz CSV/JSON |
| L07 | 37c090e914099364 | 18,0 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | HTTP và "giao thức" (không định nghĩa), "tiêu đề", "cục bộ" | HTTP chưa được định nghĩa như một quy ước giữa hai bên |
| L08 | 59e3e52aaf2e53ec | 19,3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | "mệnh đề" (WHERE) dùng qua ví dụ | lỗi INSERT lặp (thấp) |
| L09 | 166403cf0a0e3668 | 18,5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | — | `core.autocrlf false --global` đổi cấu hình toàn máy mà không nói tác dụng phụ |
| L10 | 0a907a49f1315a5a | 21,4 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "ngoại suy", MB/GB, "tệp nhị phân", phép chia lấy dư `%` trong sinh.awk | ba–bốn từ phụ chưa giảng |

Số liệu ngưỡng: **P1 = 2: 8/11 = 73 %** (cần ≥ 90 %): L03, L07, L10 còn thiếu. **P8 = 2: 11/11 = 100 %** (đạt). **P9 = 2: 11/11**. Tất cả 11 bài "ĐỦ" (tổng 13–14, không mục nào 0).

## 3. Lab (chạy như người học: đọc `de.md`, tự viết, `bash labs/cham.sh FND Lxx <tệp>`, sau đó so `loi_giai.*`)
Thời gian: `cham.sh` mỗi lần chạy 1–3 s (L07 thêm khởi động máy chủ); thời gian người học tự làm là ước tính 5–20 phút/bài (không đo).
| Bài | Tự làm được | Thời gian | Kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L00 | Phần: 5/6 dòng; dòng `sqlite3` THIEU vì máy kiểm thiếu sqlite3 (**không chạy được vì thiếu sqlite3**). Bài có dạy cài (tải sqlite-tools-win-x64, chép vào `~/bin`, mở lại Git Bash — đã xác minh `/etc/profile.d/env.sh` đặt `$HOME/bin` vào PATH) và có kiểm; thiếu ca Store-stub | <1 s | không kẹt trong video | khớp 5/6 (cùng chữ trên video) |
| L01 | Có (giống `loi_giai.sh` từng dòng) | ~1 s | không kẹt | khớp |
| L02 | Có | ~1 s | không kẹt | khớp |
| L03 | Có (giống lời giải) | ~1 s | không kẹt | khớp |
| L04 | Phần: bản theo đề nguyên văn KHÁC (`ls .` in thêm `_err`, `_out`; chạy tay in `kiem_tra.sh`); thêm `> /dev/null` thì ĐÚNG | ~1 s | dòng `ls .` | khớp sau khi sửa |
| L05 | Có | ~3 s (javac) | không kẹt | khớp |
| L06 | Có (phần YAML chỉ cần `echo` số đọc bằng mắt) | ~1 s | không kẹt | khớp |
| L07 | Có (máy chủ cổng 18766 dừng đúng bằng `kill $SV`, cổng trống sau đó) | ~3 s | không kẹt | khớp |
| L08 | SQL đúng; `cham.sh` không có `sqlite3` nên tự chạy `labs/sqlrun.py` (mô-đun sqlite3 của Python) → ĐÚNG. **Không chạy được bằng sqlite3 chính thức vì thiếu sqlite3**; các tính năng CLI (`.import`, `-header`, nháy nhiều dòng) chỉ đọc, chưa chạy | ~1 s | không kẹt | khớp (qua shim) |
| L09 | Có (cấu hình Git cách ly bằng `GIT_CONFIG_GLOBAL`) | ~2 s | không kẹt | khớp |
| L10 | **Không chạy được vì thiếu sqlite3**: `cham.sh` ra "KHÁC … LECH:  13530000" (bài đã cảnh báo trong `de.md`). Với một `sqlite3` giả bằng Python do tôi dựng ở scratchpad: ĐÚNG | ~2 s | — | khớp (qua shim) |

## 4. Người học kẹt ở đâu (một dòng mỗi bài, người chỉ xem video + các bài trước)
- L00: không kẹt ở video; kẹt ngầm trên máy chưa có Python (Store-stub): `kiem.sh` vẫn in `✔ python` (practice #36).
- L01: không kẹt.
- L02: không kẹt (brace `t{1..300}` đã giảng là "dải số").
- L03: scale #21 "ngoại suy … ≈ 3,5 GB" (MB/GB, ngoại suy chưa giảng; không ảnh hưởng đường chính).
- L04: lab #28–#29 "mã thoát của ls . … dạng ls: 0" (đề không bảo giấu đầu ra của `ls .`, ra dòng thừa, chấm KHÁC); check #19 nhãn "đang có" lệch lời đọc.
- L05: không kẹt (cảnh formula #9–#11 dày nhưng giảng từng bước).
- L06: lab bước 3 `ten_mien: [a.vn, b.vn]` (YAML dạng ngoặc vuông chưa dạy; đoán được từ mảng JSON).
- L07: sym #4 "giao thức + địa chỉ máy + cổng" (giao thức/HTTP chưa định nghĩa).
- L08: hook #1 dùng `$DB`, `BEGIN … ROLLBACK` trước khi giảng (chấp nhận được ở cảnh mở đầu); gõ theo `INSERT … (4,'Dung',NULL)` hai lần sẽ gặp UNIQUE.
- L09: không kẹt.
- L10: scale #22/#23 "ngoại suy", "tệp nhị phân", `%` trong sinh.awk (bài nói "không cần hiểu từng dấu").

## 5. Cài đặt và kiểm môi trường: bài dạy đủ chưa?
L00 dạy cài Git for Windows (Git Bash), JDK 21 Temurin, Python 3.11+ (tick Add to PATH), sqlite3 (bắt buộc; ba bước không cần quyền quản trị), VS Code, và `kiem.sh` kiểm 6 công cụ; có hướng dẫn "Open Git Bash here". Thiếu: (a) ca Store-stub (MUST), (b) không kiểm phiên bản (SHOULD). curl/awk/sed/od/iconv có sẵn trong Git Bash, đã dùng thật không lỗi.

## 6. Số đã tính lại / mã đã chạy
- 173/173 biểu thức `checks` trong YAML tự đánh giá lại bằng Python: đúng 173 (L00 24, L01 13, L02 12, L03 16, L04 8, L05 20, L06 14, L07 17, L08 20, L09 14, L10 15).
- Chạy lại đầu ra ghi trên màn hình (Git Bash thật, thư mục tạm): L01 ~14 lệnh, L02 ~40, L03 ~25 (kể cả 12 và 15 dòng giao dịch, 27/4893/728 895 byte), L04 ~25, L05 ~20 (javac JDK 21: `';' expected`, `reached end of file`, `illegal character '“'` ×2 + `not a statement` = 3 errors, `cannot find symbol`; UTF-8 c4 83, e1 bb 85; 1201/120001), L06 ~20 (json.tool đúng 2 thông báo, 15/39, 1592/3992, 178 894/418 894 byte), L07 ~14 curl với `may_chu.py` thật (200/201/404/405/500, mã thoát 22/28, Content-Length 7/12/13), L09 ~25 git (cả hai mã blob `7de0592`/`ad79274`), L08 ~25 SQL (qua engine SQLite 3.45.1 của Python), L10 ~15 (qua `sqlite3` giả). Tổng khoảng 215 đầu ra: **toàn bộ khớp màn hình về số/chữ**; sai lệch chỉ ở các mục trong bảng chuẩn xác (một ca hành vi, còn lại là lời giải thích hoặc nhãn).
- Số tự tính độc lập bằng Python: 2^8, 259 → `100000011` → `c4 83`, Nguyễn = 8 byte, 1−0,999^n = 1,0/9,5/63,2 %, ⌈log2 n⌉ = 3/10/17 (n = 7/700/70 000), Little 50 × 0,02, 500 000 × 0,02 = 10 000, 100 000 s = 27 g 46 ph 40 s, 115,7 ngày, 130 000 000 (sinh.awk 10 000 dòng), 3 150 000 (sổ tay): đều khớp.

## 7. Khung hình đã xem (≥ 5/bài; thực tế 6/bài = 66 khung, 0 lỗi hiển thị)
Khung ở mỗi bài (chỉ số `frames/*.png`): hook, intuition, example đầu, scale đầu, quiz (câu hỏi), recap cuối.
L00 0,21,46,70,133,168 · L01 0,29,48,73,98,138 · L02 0,32,55,90,111,147 · L03 0,28,48,70,92,129 · L04 0,24,48,73,90,127 (+70) · L05 0,27,60,85,108,140 · L06 0,23,36,62,84,119 · L07 0,29,49,73,96,137 · L08 0,26,54,82,113,146 · L09 0,25,55,79,105,145 · L10 0,26,44,77,105,145.
Không thấy chữ tràn/đè/cắt; hình sơ đồ khớp lời đọc (đường đi chương trình, cây thư mục, cp/mv/rm, đường ống, dò PATH, UTF-8, ba dạng đơn hàng, vòng yêu cầu–phản hồi, hai bảng + GROUP BY, ba vùng Git, quy trình năm bước). Chữ SVG nhỏ nhất (L06 intuition, khung JSON) vẫn đọc được ở 1920×1080 (~22 px). Hơn nửa dưới khung để trống (bố cục chung, không lỗi). Chưa xem các khung của cảnh `practice` (nội dung đối chiếu bằng văn bản với `mong_doi.txt`: khớp).

## 8. Nhận xét chung
- Chuẩn xác cao: 0 sai số, 0 lệnh cho kết quả khác màn hình; video dựng lại đồng bộ tuyệt đối với YAML và SRT.
- MUST còn 1 (L00, `command -v python` bị Store-stub đánh lừa); sửa trong một dòng của `kiem.sh` + đề + cảnh "kẹt".
- P1 chưa đạt 90 %: ba cụm lặp lại (MB/GB + "ngoại suy" ở L03, L10; HTTP/giao thức ở L07) là đủ để kéo lên 11/11 nếu giảng một câu.
- P8/P9 mạnh: cả 11 bài có việc cụ thể với đầu ra đối chiếu và số liệu ở ≥ 2–3 mức quy mô kèm đánh đổi.
- Lab chạy được và chấm đúng ở 9/11; L00 (5/6), L10 (và L08 chính thức) cần `sqlite3` mà máy kiểm không có; bài dạy cài sqlite3 đầy đủ, không lỗi lớn.
- Đề lab L04 thiếu `> /dev/null` cho `ls .`: người học làm đúng đề vẫn bị KHÁC (nên sửa trước khi mở học).
- Quan hệ bài nền với Windows: `chmod +x` (L04) và `core.autocrlf false --global` (L09) cần một câu điều kiện, không phải lỗi nặng.
- Bản dựng và quiz giữ nhất quán 11 bài; ngưỡng chốt: MUST 0 → **chưa đạt (1)**; P1 = 2 ≥ 90 % → **chưa đạt (73 %)**; P8 = 2 100 % → **đạt**.
