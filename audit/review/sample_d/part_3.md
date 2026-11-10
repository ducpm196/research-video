# Đọc mẫu độc lập đợt D — phần 3 (10 bài, 2026-11-10)

Người đọc: một tác tử AI, chỉ đọc, không mở `audit/review/full_review_c/*`. Đã đọc toàn bộ `show` (kể cả chữ trong SVG), `say`, `checks`, quiz, `title`, `objectives` của từng bài, mục bài trong `curriculum/<khoá>.yaml`, và `audit/<khoá>/sources_*.md` khi có (HCI L12, IRS L08, MLO L14). Mọi con số trên màn hình hoặc trong lời đọc đã tính lại bằng `.venv/Scripts/python` (bộ đếm xen kẽ PAR, khối PIN và bản đồ bit INT, các phép mũ, lôgarit và chia của IRS/LLM/HCI/MLO/OSY/NET, mô phỏng tay số dư JVA). **Không thấy số sai nào**, cũng không thấy lỗi mức MUST. Không thấy chỗ nào nhắc khoá khác bằng mã hay bằng tên trong phần người học thấy hoặc nghe, cũng không có trong giáo án. INT L04 không khẳng định ACB dùng T24 (cảnh hook nói rõ "Tin tuyển dụng ACB không nói ACB dùng hệ lõi nào").

| Bài | Mức (MUST/SHOULD) | Cảnh/bước | Phát hiện (trích nguyên chữ trong bài) | Bằng chứng (phép tính Python / nguồn / dòng YAML) | Tin cậy (cao/vừa) |
|---|---|---|---|---|---|
| HCI L12 | SHOULD | prereq bước 1 | Màn hình hiện công thức "Thời gian trỏ $T = a + b \cdot \log_2(D/W + 1)$" nhưng không giải nghĩa T, a, b, D, W. Lời đọc không đọc công thức (chỉ nói "nút càng nhỏ thì … càng mất nhiều thời gian") | dòng 46. Brief B.4 yêu cầu nhắc lại định nghĩa khi dùng lại khái niệm của bài trước; bài này không có chỗ nào nói D là khoảng cách, W là bề rộng đích | cao |
| HCI L12 | SHOULD | prereq bước 1, stage2 bước 2, check bước 2 | Ba mức A / AA / AAA dùng mà không định nghĩa: "(mức AA)", "Ở mức AA (tiêu chí 1.4.3)", lời đọc "Ở mức hai chữ A". Ở check còn có câu "Mức AA là mức tối thiểu; mức AAA dễ bấm hơn": đọc tách khỏi ngữ cảnh thì trái với thang mức của chuẩn (A mới là mức thấp nhất; bài 9 cùng khoá ghi "mức A thấp nhất, AA là mức thường được yêu cầu"). "24 × 24 điểm ảnh" cũng không nói đó là đơn vị CSS chứ không phải chấm vật lý (bài 9 có nói, bài 12 không) | dòng 48, 154, 225. `lessons/hci/L09_*.yaml` dòng 85, 89 có định nghĩa; `audit/hci/sources_L12.md`: "Level AA", "24 by 24 CSS pixels" | cao |
| HCI L12 | SHOULD | stage2 bước 2 | "Độ chói tương đối là mức sáng của một màu theo cảm nhận của mắt" là định nghĩa không chính xác. W3C định nghĩa độ chói tương đối là đại lượng tuyến tính chuẩn hoá về 0–1 ("relative brightness … normalized to 0 for darkest black and 1 for lightest white"), không phải độ sáng cảm nhận. Ví dụ: màu xám mà mắt thấy sáng bằng nửa trắng có L ≈ 0,18–0,2, không phải 0,5. Câu này dễ làm người học hiểu sai đề quiz ($L_2 = 0{,}20$) | dòng 151; định nghĩa "relative luminance" của WCAG 2.x | vừa |
| INT L04 | SHOULD | concept (SVG ô 6), pitfall | Thuật ngữ không giải thích: "Khóa Redis 300 giây", "Khóa nguyên tử Redis theo STAN và RRN", "Bỏ qua kiểm tra trùng lặp khóa phân tán", "Cổng CIC B2B Quốc gia". Bài không nói Redis là gì, khoá nguyên tử/khoá phân tán là gì, vì sao 300 giây. Mẫu đợt C đã ghi đúng dạng lỗi này cho ACB L02 | dòng 191 (B2B), SVG ô 6, dòng 417 | cao |
| INT L04 | SHOULD | example bước 1–2 | Ký hiệu độ phức tạp "O(N^2)", "$O(N \log N)$ với thuật toán TimSort", "Hai con trỏ O(N)" dùng mà không giảng O(·) bằng lời thường; TimSort cũng không giải thích. Riêng O(N²) có phép tính số kèm theo, các ký hiệu còn lại thì không | dòng 312, 328 | vừa |
| INT L04 | SHOULD | hook bước 2 (say) | Lời đọc "giao tiếp với ngân hàng lõi qua bản tin đặc tả mở" và "quy chuẩn gói tin chuyển mạch liên ngân hàng quốc tế" lệch với màn hình cùng bước: "Bản tin OFS (chuỗi văn bản)" (OFS là định dạng riêng của Temenos, chữ "Open" chỉ có trong tên) và "Đặc tả riêng của NAPAS, thường mô tả có gốc ISO 8583". NAPAS 247 là chuyển mạch trong nước | dòng 77–78 so với bảng ở cùng bước | vừa |
| JVA L12 | SHOULD | prereq, formula bước 2–3 | Phần ôn chỉ có một bảng 3 dòng ("Ta ghép ba công cụ đã học"). Các khái niệm dùng lại không được nhắc định nghĩa: "Phương thức lấy dùng lớp bọc" (không nói lớp bọc `Long` là gì, vì sao `Long` có thể là `null` còn `long` thì không); `void chuyen(Lenh l) throws KhongDuTien` (không giải thích `throws` và ngoại lệ phải khai báo); `record Lenh(...)` chỉ được tả là "bản ghi để chở một lệnh chuyển" | dòng 56–67, 194, 197. Brief B.4 | vừa |
| JVA L12 | SHOULD | pitfalls bước 4 (Lỗi 2) | Màn hình hiện kết quả "SAI LENH Khong co tai khoan X / A=2500000 B=300000 C=2100000 / Tong 4900000" nhưng không giải thích từng bước vì sao ra số đó, vì sao không có dòng "OK" nào, vì sao không có "TU CHOI". Lời đọc chỉ nói "gần hai triệu tự sinh ra". Tự mô phỏng (lỗi `a + l.tien()` vẫn còn, `kiem()` ném nhưng bị nuốt trước `println("OK")`): lệnh 1 → A 700 000, B 1 300 000; lệnh 2 B→C qua kiểm tra vì B = 1 300 000 → B 300 000, C = 1 300 000 + 1 000 000 = 2 300 000; lệnh 4 C→A → C 2 100 000, A 2 500 000. Tổng 4 900 000 là **đúng**, nhưng người học bị bỏ qua một bước suy luận | dòng 382–394; mô phỏng tay đã khớp số in ra | vừa |
| LLM L06 | SHOULD | prereq bước 3, sym bước 2, check | Chữ N mang hai nghĩa trong cùng một bài mà không có lời cảnh báo: "$PP = P^{-1/N}$" và "xác suất cả chuỗi mũ âm 1 chia N" (N = số từ tố của chuỗi) so với bảng ký hiệu "$N$ — số tham số" và "$C \approx 6 \cdot N \cdot D$" | dòng 66–67, 85, 140, 142 | cao |
| LLM L06 | SHOULD | hook, toàn bài | "khoảng 681 ngày-thẻ nếu mỗi thẻ làm $10^{14}$ phép tính mỗi giây": chữ "thẻ" (thẻ tăng tốc tính toán) không được giải thích. "Từ tố" và "tham số" dùng xuyên bài mà không có câu định nghĩa nào (bài 1 cùng khoá có định nghĩa, bài này không nhắc lại). Phép tính 5,88·10²¹ / (10¹⁴ · 86 400) = 680,56 → 681 vẫn đúng | dòng 34, 37; Python: 680.5555 | vừa |
| MLO L14 | SHOULD | quiz bước 3 | "2 mô hình nhân 2 bước nhân 1 nơi chạy = 4 đường cần kiểm": không nói "2 bước" là bước nào, trong khi cùng ô vừa nêu "một kịch bản cộng **ba** cửa kiểm" | dòng 353 | vừa |
| MLO L14 | SHOULD | prereq, stage3, stage4 | Thuật ngữ không định nghĩa trong bài: "ví dụ các vector nhúng", "một nhóm luồng riêng, chỉ 1 hoặc 2 luồng", "thử nghiệm hai nhóm cho thấy …" (phần quiz mới giải thích cụm này), "bộ điều phối", "cơ sở dữ liệu siêu dữ liệu", "mã băm nội dung" (chỉ tả tính chất, không nói mã băm là gì) | dòng 51, 217, 221, 226, 266 | vừa |
| NET L12 | SHOULD | pitfalls Lỗi 1 | "Nghĩ DNS chỉ dùng UDP … thì chuyển sang TCP": UDP không được định nghĩa trong bài (bài 9 cùng khoá có dạy), bài cũng không nói UDP khác TCP ở chỗ nào. "chép cả vùng tên" cũng chưa giải thích | dòng 177–179. Brief B.4 | vừa |
| PAR L03 | SHOULD | prereq bước 3 (say), Lỗi 4 | Lời đọc "cộng 8 số theo cặp cần 7 phép cộng và đường găng 3 tầng": chữ "đường găng" không được định nghĩa, và màn hình cùng bước ghi khác ("xếp thành cây 3 tầng"). "thư viện đó ghi chúng là không tất định": chữ "tất định" chưa giải thích bằng lời thường | dòng 68, 254–255 | vừa |
| PLC L09 | SHOULD | prereq bước 1 (say), hook | "ôn lại phép gán trong các ngôn ngữ mà bài này dùng … phép gán b bằng a không sao chép danh sách": câu này sai với C/C++, mà bài cũng dùng hai ngôn ngữ đó (ở C/C++ `b = a` sao chép giá trị). Hook và prereq cũng không nói đoạn mã là Python; tên Python chỉ xuất hiện ở bảng ký hiệu | dòng 46; bảng sym "`void f(int x)` trong C" | vừa |

Bài không có phát hiện: IRS L08, OSY L03.

## Ghi chú kiểm số (không phải phát hiện)
- PAR L03: duyệt hết C(12,6) = 924 cách xen kẽ ra {2: 702, 3: 216, 4: 6}; C(6,3) = 20 ra {1: 18, 2: 2}; cộng dồn 8 lần 0,1 bằng vòng lặp ra 0,7999999999999999, cộng theo cây ra 0,8; 8000/1003 = 7,976; 160000/10004 = 15,99. (Lưu ý: hàm `sum()` của Python 3.12 trở lên cộng có bù sai số nên ra 0,8. Phải dùng vòng lặp cộng dồn.)
- INT L04: bản đồ bit của các trường 3, 4, 11, 37, 52 = `3020000008001000`; 041234FFFFFFFFFF XOR 0000198765432109 = `04122D789ABCDEF6`; log₂(3·10⁶) = 21,52; 9·10¹²/10⁹/3600 = 2,5 giờ. Đều khớp bài.
- HCI L12: 1936/576 = 3,361; 1,05/0,25 = 4,2; ngưỡng $L_2 \le 0{,}1833$ (bài ghi "≤ 0,18"); 16 + 30 + 19 = 65; 78 − 1 + 9 = 86. Đều khớp nguồn W3C ghi trong `sources_L12.md`.
- IRS L08: 100^0,75 = 31,623; tổng 38,246; các tỉ phần 0,827 / 0,147 / 0,026 và 0,901 / 0,090 / 0,009; tỉ số 2,90; 1/(31,62 + 1) = 0,0307; 1000/1990 = 50,25%; −ln 0,02 = 3,912; ln 25 = 3,219; e^3,4539 = 31,623.
- LLM L06: −ln của 0,25 / 0,5 / 0,8 = 1,3863 / 0,6931 / 0,2231; trung bình 0,7675; e^0,7675 = 2,1544 = 0,1^(−1/3); 2/ln 2 = 2,885; 10¹²/(7·10⁹) = 142,9; e^1,5 = 4,4817.
- MLO L14: 465/45 = 10,33; 10,3·45 = 463,5; 500/75 = 6,67; 0,5/12 = 0,042; các câu trích khớp `sources_L14.md` (SC15, TX17, TH20).
- OSY L03: xoay vòng q = 4 cho [24, 3, 3] ra thời gian chờ 6/4/7, trung bình 5,67; q = 2 cho [5, 3, 8] ra 7/6/8, trung bình 7; 5/10005 = 0,050%, 5/105 = 4,76%, tỉ số 95,3; 127·15/60 = 31,75 giờ.
- NET L12: 22 / 12 / 3 lượt đi về; 80 000 bit / 10⁷ bit/s = 8 ms; 19·100 = 1900 ms; câu tự làm 12 / 7 / 200 ms.

## Đã sửa (2026-11-10)

Kiểm lại từng phát hiện trên tệp thật trước khi sửa: cả 15 phát hiện đều đúng, nên sửa hết, không bỏ mục nào. Các sửa đều dùng công cụ Edit; JVA sửa ở nguồn `audit/jva/src/l12.py` rồi chạy `gen.py L12`. Không chạy build, render, tts, asr; không ghi git.

| Bài | Phát hiện | Đã sửa thế nào |
|---|---|---|
| HCI L12 | Công thức thời gian trỏ có T, a, b, D, W chưa giải nghĩa | prereq: màn hình ghi rõ D là khoảng cách từ con trỏ tới nút, W là bề rộng nút, a và b là hai hằng số đo cho từng thiết bị; lời đọc thêm hai câu đọc công thức và giải nghĩa từng chữ (focus 4 → 8 mục) |
| HCI L12 | Ba mức A/AA/AAA chưa định nghĩa; “Mức AA là mức tối thiểu” dễ hiểu sai; điểm ảnh CSS | prereq: thêm ghi chú “A thấp nhất, AA thường được yêu cầu, AAA cao nhất” và “điểm ảnh CSS, không phải chấm vật lý”, có cả màn hình và lời đọc. Câu ở phần tự kiểm đổi thành “Đích 24 × 24 ở mức AA (tiêu chí 2.5.8) là kích thước tối thiểu thường được yêu cầu; đích 44 × 44 ở mức AAA (tiêu chí 2.5.5) …”. Thêm check `round(576 / 1936, 2) == 0.3` cho cụm “khoảng một phần ba” |
| HCI L12 | Định nghĩa độ chói tương đối | stage2: “lượng ánh sáng một màu phát ra, tính theo độ nhạy của mắt với từng màu, quy về thang 0–1; không phải độ sáng mắt cảm nhận: xám trông sáng bằng nửa trắng chỉ có độ chói khoảng 0,18”. Thêm check `round(((50 + 16) / 116) ** 3, 2) == 0.18`; ghi nguồn CIE 1976 L* vào `source` |
| INT L04 | Redis, khoá 300 giây, B2B, khoá nguyên tử, khoá phân tán chưa giải thích | concept bước 2: thêm dòng bảng “B2B; Redis, khóa 300 giây (số minh hoạ)” và hai câu lời đọc. pitfall: thêm đoạn định nghĩa khoá nguyên tử và khoá phân tán, cùng định nghĩa “hàm băm thường”, và hai câu lời đọc. Không có số mới ngoài 300 giây, đã ghi “(số minh hoạ)” |
| INT L04 | O(·), TimSort chưa giảng | example bước 1: thêm dòng định nghĩa O(N), O(N log N), O(N^2) và một câu lời đọc. Bước 2: thêm ghi chú TimSort (cách sắp xếp có sẵn trong thư viện Python, Java; N log N là mức thấp nhất của sắp xếp dựa vào phép so sánh). Lời đọc thay “độ phức tạp tối ưu” bằng câu đó |
| INT L04 | Lời đọc “đặc tả mở”, “quy chuẩn … quốc tế” lệch màn hình | hook bước 2: “ra lệnh cho hệ lõi T24 bằng bản tin OFS, một định dạng chữ riêng của hãng Temenos” và “bản tin chuyển mạch theo đặc tả riêng của NAPAS, thường được mô tả có gốc từ chuẩn quốc tế ISO 8583”. Không câu nào nói ACB dùng T24 |
| JVA L12 | Phần ôn mỏng; lớp bọc, `throws`, `record` chưa nhắc định nghĩa | `audit/jva/src/l12.py` prereq: thêm bước thứ hai, bảng 3 khái niệm (bản ghi; lớp bọc `Long` khác `long` và phải kiểm `null` trước khi lấy số; `throws` của ngoại lệ phải khai báo, khác `IllegalArgumentException`/`IllegalStateException` là lỗi lúc chạy) và 6 câu lời đọc |
| JVA L12 | Lỗi 2 ra 4 900 000 không có bước suy | pitfalls: thêm bước bảng lần theo 4 lệnh (lỗi gài còn, kiểm ném bị nuốt) và công thức 2 500 000 + 300 000 + 2 100 000 = 4 900 000, kèm 8 câu lời đọc. Thêm 4 check số học |
| LLM L06 | Chữ N hai nghĩa | Độ dài chuỗi đổi thành T: $PP = P^{-1/T}$ ở prereq và check (“ở đây T = 3”); thêm ghi chú “Bài này gọi độ dài chuỗi là T, vì chữ N sẽ dành cho số tham số”, có cả màn hình và lời đọc; prereq bước 3 thêm focus |
| LLM L06 | “thẻ”, “từ tố”, “tham số” chưa định nghĩa | hook: thêm ghi chú định nghĩa ba từ và ba câu lời đọc (focus 3 → 6 mục) |
| MLO L14 | “2 bước” không rõ | quiz: “2 bước (huấn luyện, phục vụ)”; lời đọc “mỗi mô hình 2 bước là huấn luyện và phục vụ” |
| MLO L14 | vector nhúng, luồng, thử nghiệm hai nhóm, bộ điều phối, siêu dữ liệu, mã băm chưa định nghĩa | Thêm định nghĩa trong ngoặc trên màn hình, mỗi khái niệm một câu lời đọc (prereq, stage3 bước 3 và 4, stage4 bước 2); sửa focus tương ứng |
| NET L12 | UDP, “chép cả vùng tên” chưa định nghĩa | pitfalls Lỗi 1: thêm ghi chú UDP khác TCP và nghĩa của “chép cả vùng tên”, cùng hai câu lời đọc. Chạy `sync_tpl_from_lesson.py NET --write`: mẫu `L12_dns_http.tpl.yaml` đã nhận sửa (chạy lại báo khớp) |
| PAR L03 | “đường găng” chỉ có ở lời đọc; “tất định” chưa định nghĩa | prereq: lời đọc và màn hình cùng nói “cây 3 tầng (4 → 2 → 1 phép), các phép cùng tầng làm song song nên chỉ chờ 3 lượt nối tiếp”; thêm check `4 + 2 + 1 == 7`. Lỗi 4: thêm định nghĩa “tất định” ở cả màn hình và lời đọc |
| PLC L09 | Câu phép gán sai với C/C++; không nói mã là Python | prereq: lời đọc đổi thành “ôn lại phép gán trong ngôn ngữ của đoạn mã này”; thêm ghi chú “Mã ở đây là Python. Trong C hay C++, `b = a` giữa hai biến thường lại sao chép giá trị” và câu lời đọc tương ứng. Hook: “Trong Python, gọi `them(a)` …”. Lời đọc không đọc chữ Python (từ này không có trong từ vựng đọc của khoá PLC) |

Không sửa: IRS L08, OSY L03 (không có phát hiện). Mục giáo án `curriculum/<khoá>.yaml` của 8 bài không cần đổi: tiêu đề, mục tiêu và ví dụ vẫn khớp bài sau sửa. Tài liệu `interview/04_banking_domain_t24_napas.md` không có các câu đã sửa (“đặc tả mở”, “quy chuẩn quốc tế”), nên không thấy lệch cần ghi.

### Tệp đã đổi
- `lessons/hci/L12_hanh_trinh_wcag.yaml`
- `lessons/int/L04_banking_domain_t24_napas.yaml`
- `audit/jva/src/l12.py` → sinh lại `lessons/jva/L12_so_chuyen_khoan.yaml` (`gen.py L12`)
- `lessons/llm/L06_huan_luyen_truoc.yaml`
- `lessons/mlo/L14_hanh_trinh_no_ky_thuat.yaml`
- `lessons/net/L12_dns_http.yaml`, `audit/net/src/L12_dns_http.tpl.yaml` (sync; bản cũ ở `out/_tpl_backup/net/`)
- `lessons/par/L03_tranh_chap_rut_gon.yaml`
- `lessons/plc/L09_truyen_tham_so.yaml`

### Kết quả kiểm sau sửa
- `lv.py lint`: cả 8 bài 0 FAIL, 0 WARN (HCI 33 PASS, INT 33, JVA 32, LLM 22, MLO 32, NET 25, PAR 32, PLC 21).
- Bộ kiểm khoá: verify_hci 27/27 PASS; verify_jva 110/110 PASS; verify_llm 18 PASS · 0 FAIL; verify_mlo 20 PASS · 0 FAIL; verify_net 89/89 PASS; verify_par 96/96 PASS; verify_plc 72/72 PASS. INT không có bộ kiểm.
- `sync_tpl_from_lesson.py`: NET và PLC 0 mẫu lệch.
- `scan_ctrl.py`: 8 lượt, đều là `\tat` cố ý của JVA L12 (vị trí bước dời từ steps[4] sang steps[5] vì có bước mới chèn trước).
- `check_xref.py --course` HCI, INT, JVA, LLM, MLO, NET, PAR, PLC: mỗi khoá 0 lượt.
- `lv.py curriculum` của 8 khoá trên: 0 lỗi.
