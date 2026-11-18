# S01b JV2: đã đọc 10/10 bài (đọc độc lập vòng 2, 2026-11-14)

Phạm vi: `lessons/jv2/L00..L09` + `curriculum/jv2.yaml` + `labs/JV2/*` + `out/JV2/*/{chapters.txt,*.srt,frames}`. JDK 21, Git Bash. Không mở báo cáo/handover/plan cũ. L09 đang được dựng lại: chỉ đọc đặc tả YAML (sha16 không đổi từ đầu tới cuối phiên); khung hình L09 xem là bản dựng hiện có lúc đọc.

Kết luận theo ngưỡng chốt:
- MUST = 0 (đạt). SHOULD = 8 (chi tiết bảng 2).
- P8 = 2 ở 10/10 bài = 100% (đạt). Cả 10 lab tự viết lời giải rồi chấm `cham.sh` đều ĐÚNG ngay lần đầu.
- P1 = 2 ở 5/10 bài = 50% (KHÔNG đạt ngưỡng 90%). Nếu coi log₂ là toán phổ thông và bỏ L02, L07 thì vẫn chỉ 7/10 (L03, L08, L09 còn thiếu). Chi tiết ở bảng 3.

## 2. Bảng chuẩn xác (chỉ lỗi có bằng chứng)

Không có MUST: mọi chương trình/lệnh trên màn hình biên dịch và chạy cho đúng đầu ra ghi trên màn hình (mục 6); mọi số tính lại khớp; đáp án quiz đúng (đã chạy riêng quiz L04 câu 1 ra thứ tự A,B,C và 3 đối tượng).

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L06 | SHOULD (nhãn hình sai) | intuition step 1 (trục số, `frames/00022.png`) | nhãn đỏ "biên 2: 10 000 000 / 10 000 001" | SVG: ba chấm đỏ ở cx=400, 780, 1140 (ranh 0\|1, 1M\|1M+1, 10M\|10M+1). Nhãn "biên 2: 10 000 000" đặt ở x=780, tức ngay dưới chấm của biên 1 triệu; nhãn "biên 1: 1 000 000" đặt x=560 (giữa chấm 1 và 2); chấm 1 140 (biên 10 triệu) không nhãn. Lời đọc nói "giữa các bậc là những điểm đỏ" nên người học đối chiếu hình sẽ lệch một biên | dời nhãn biên 1 xuống x=780 và nhãn biên 2 xuống x=1140 | CONFIRMED (toạ độ trong YAML + khung hình) |
| L07 | SHOULD (lệch chi tiết nhỏ) | practice step 3, `de.md` | "Dòng số 15 có vòng for với điều kiện i <= ds.length: đổi dấu." (lời đọc: "Ở dòng mười lăm, điều kiện vòng lặp cho phép đi tới năm") | Trong `labs/JV2/L07/de.md`, dòng 14 là `for (int i = 0; i <= ds.length; i++)`, dòng 15 là `tong += phi(ds[i]);` (nơi nổ, dấu vết ghi `:15`). Đã chạy `javac`+`java`: trace `TongPhi.tongPhi(TongPhi.java:15)`. Người học đếm dòng sẽ không thấy `for` ở dòng 15 | "Dòng 15 nổ; vòng for ở dòng 14 có điều kiện i <= ds.length" | CONFIRMED |
| L09 | SHOULD (giáo án lệch nhỏ; ranh giới MUST "ví dụ tự mâu thuẫn giữa các cảnh") | curriculum L09 objective 1; hook step 2; prereq; intuition | "Dựng dự án nhiều gói gồm bản ghi, bộ đọc…" / hook: "Dự án nhiều gói, đọc tệp từng dòng" / prereq: "gói, javac -d, -cp … ba thư mục, một lệnh biên dịch" / intuition: "Một gói, mười tệp" | Cây dự án trên màn hình chỉ có `src/soc` (một gói) + `TaoSoCai.java` ngoài gói; lệnh `javac -d out src/soc/*.java TaoSoCai.java`; lab L09 chỉ một tệp `SoCaiNho.java`. "Nhiều gói" và "ba thư mục" không có trong ví dụ; nhiều gói chỉ thực hành ở L00 | đổi mục tiêu/hook thành "dự án nhiều tệp trong một gói"; sửa dòng prereq | CONFIRMED |
| L01 | SHOULD (khẳng định tuyệt đối) | hook step 1 | "Một ngân hàng nhận cả triệu giao dịch mỗi ngày thì chỉ có thể đi qua cửa thứ ba." | "ba cửa" (tham số, bàn phím, tệp) bỏ qua mạng, hàng đợi tin nhắn, cơ sở dữ liệu; hệ thống ngân hàng thật nhận phần lớn qua các đường đó | "thường đi qua cửa thứ ba (tệp) hoặc các đường nâng cao hơn như mạng/hàng đợi" | PLAUSIBLE |
| L01 | SHOULD (tuyệt đối trên số ước lượng) | quiz step 3 | lời đọc: "Vậy phương án A chắc chắn hết bộ nhớ" (màn hình: "nhiều khả năng hết bộ nhớ") | Con số 6,4 GB dựa trên ước lượng 64 byte/dòng (màn hình tự ghi "ước lượng"); lời đọc bỏ chữ "nhiều khả năng". Phép tính 10^8×64 = 6,4×10^9 đúng | đọc "nhiều khả năng hết bộ nhớ" | CONFIRMED (so say với show) |
| L06 | SHOULD (thiếu điều kiện) | quiz step 2 câu 1 | "2 999 999 → 0; 3 000 000 → 3 000; 3 000 001 → 3 000" | Đặc tả quiz không nói làm tròn: 0,1% × 3 000 001 = 3 000,001; đáp án 3 000 chỉ đúng nếu cắt phần lẻ (chia nguyên) | thêm "(phí làm tròn xuống đồng)" vào đề | CONFIRMED |
| L08 / L06 | SHOULD (số cắt, không làm tròn) | L08 formula step 4 và example step 5; L06 scale step 1 | "≈ 1 755 616,43"; "≈ 584 năm" | Python: 640 800 000 000 / 365 000 = 1 755 616,438… (làm tròn 2 chữ số: ,44); 2^64 ns = 584,54 năm (làm tròn: 585). Kết quả cuối (1 755 616; ≈584) không ảnh hưởng, chỉ là cắt chứ không làm tròn | ghi "1 755 616,44" và "≈ 585 năm" (hoặc bỏ "≈") | CONFIRMED |
| L01 / L05 | SHOULD (chữ tràn khung) | L01 scale step 3 (`frames/00094.png`); L05 scale step 3 (`frames/00088.png`) | "// giữ MỌI dòng trong bộ nhớ"; "// 400 việc / n luồng, mỗi lượt 50 ms" | Chữ chú thích kéo qua viền phải của khung mã (x≈1845 so với viền ≈1832), vẫn đọc được nhưng sát mép | rút ngắn chú thích | CONFIRMED (xem khung hình) |

## 3. Bảng độ sâu

Cột Phút = độ dài video dựng (`_frames.txt`). P1: 2 = không từ nào kẹt. "Mất gốc": ĐỦ ≥ 12 và không mục 0.

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước (dùng mà không giảng tại chỗ) | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 8a04707e794d4c10 | 14:21 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | heredoc `cat > … <<'EOF'` (có ở FND L02); `ClassNotFoundException` chỉ xuất hiện trong thông báo | không đáng kể |
| L01 | f57e870c51ff574d | 16:23 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | không đáng kể | khung hình 00094 chú thích tràn khung; hook nói "chỉ có thể đi qua cửa thứ ba" |
| L02 | 41e05d1517a12395 | 15:01 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | lôgarit / log₂ (chỉ có trong JV2 L02 và L07, không có ở FND/JVA); cờ `sort -t, -k2,2 -k3,3nr` | scale step 1: "n nhân lôgarit của n" chưa giảng log là gì |
| L03 | 25872f9d27edd258 | 16:23 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | tham chiếu hàm tạo `TreeMap::new` (không có ở FND/JVA); `groupingBy` ba tham số, `toMap` bốn tham số: tham số giữa không giảng | hook step 2 và pitfalls step 5 |
| L04 | ec6210afa627d37c | 18:30 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | nhãn Spring ở hook (được giải nghĩa cuối bài) | không đáng kể; bảng 8 mục dày |
| L05 | 2da44239959a2c8d | 18:16 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | ký hiệu C(4,2) (đã liệt kê đủ 6 cách nên không chặn); lõi CPU | khung hình 00088 chú thích tràn khung |
| L06 | 18c1a455c2be2e81 | 16:33 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | cờ `execute -cp out -c … --details=summary` của JUnit | nhãn hình trục số lệch (SHOULD ở bảng 2) |
| L07 | b8d91f2d29c87552 | 16:49 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | log₂ n (bảng 4/20/30 minh hoạ nhưng không giảng); `bci=9` trong đầu ra jdb | scale step 7; gợi ý lab nói sai số dòng |
| L08 | 1669dbbbe4c58d32 | 15:38 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | UTC và hậu tố `Z`; ký hiệu ISO `PT23H`, `P3M`; tên múi giờ IANA `Asia/Ho_Chi_Minh` | sym step 1, intuition step 2–3 |
| L09 | 24bf92e00aae3189 | 19:36 (bản dựng cũ) | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 12 | ĐỦ | `Consumer<…>`/`accept`; tham chiếu hàm gắn đối tượng `ds::add`, `t::them` (L03 chỉ giảng dạng `Lop::ham`); khối `static { }`; `String.format("%02d")`; `tail -n +2`; `parallel()`/`groupingByConcurrent` chỉ giải thích bằng chức năng | mục tiêu "nhiều gói" không có trong ví dụ (P7); DocSoCai step 5 |

Đối chiếu giáo án: `objectives` của 10 bài trùng từng chữ với `curriculum/jv2.yaml`; `covers` phủ đủ mục tiêu; số trong mục `example` của giáo án trùng số trên video (L00 6 000/4 994 000, L01 6 200 000, L02 18 640 873/999 999, L04 3/3 000 000, L05 21 000, L07 518 GB/ngày, L08 1 755 616 …).

P9 = 2 ở cả 10 bài: mỗi bài có cảnh quy mô với số liệu ≥ 2 mức và đánh đổi (L00 3/30/300 thư viện và 44 850 cặp trùng tên; L01 1k/1M/1G dòng; L02 n log n; L03 bộ nhớ và thời gian; L04 1k/1M yêu cầu; L05 5/500/50 000 luồng; L06 2^64 và lũy thừa tổ hợp; L07 5,2 GB/518 GB/51,8 TB và 4/20/30 lần kiểm; L08 500/500 000/500 triệu; L09 hết bộ nhớ ở 32 MB và 64 MB).

## 4. Lab (làm như người học: đọc `de.md`, tự viết trong thư mục tạm, chấm bằng `bash labs/cham.sh JV2 Lxx <tệp>`, sau đó mới so `loi_giai.*`; tôi không mở `loi_giai.*` trước khi chấm)

| Bài | Tự làm được | Thời gian máy chấm | Kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L00 | có | 10,8 s (javac + jar) | không; lệnh heredoc cần FND L02 | khớp (khối "Kết quả mong đợi" trong YAML = `mong_doi.txt`, so tự động) |
| L01 | có | 2,5 s | không; `de.md` đã cho dữ liệu và import | khớp |
| L02 | có | 2,6 s | không; `de.md` nhắc sắp xếp ổn định, đủ | khớp |
| L03 | có | 2,8 s | không; cần biết `TreeMap::new` (de.md cho cú pháp) | khớp |
| L04 | có | 2,8 s | không; `de.md` mô tả từng bước của `lay` | khớp |
| L05 | có | 2,9 s (chạy lại 8 lần: 8/8 ĐÚNG) | không | khớp |
| L06 | có | 2,9 s | không; lưu ý: chấm bản chưa sửa ra ĐÚNG, sau khi người học sửa hàm thì `cham.sh` báo KHÁC (đúng như `de.md` dặn: "Chấm bản chưa sửa") | khớp |
| L07 | có (bản chưa sửa báo "LỖI khi biên dịch/chạy" đúng như đề, sửa `<=` thành `<` thì ĐÚNG) | 2,6 s | gợi ý nói "dòng 15 có vòng for" nhưng for ở dòng 14 | khớp |
| L08 | có | 2,8 s | không | khớp |
| L09 | có | 2,8 s | không; dòng đếm bắt đầu từ 1 ở tiêu đề đã được gợi ý | khớp |

10/10 tự làm được ngay lần đầu, 10/10 ĐÚNG, và 10/10 khối "Kết quả mong đợi" trên video trùng `mong_doi.txt`.

## 5. Người học kẹt ở đâu (chỉ xem đúng video này và các bài trước trong khoá)

- L00: không kẹt (rủi ro nhỏ: lệnh `LC_ALL=C sort` ở ví dụ bước ①, được giải thích bằng lời).
- L01: không kẹt.
- L02: scale step 1: "theo n nhân lôgarit của n" (log chưa được giảng ở đâu trong khoá).
- L03: hook step 2: `groupingBy(GiaoDich::loai, TreeMap::new, Collectors.summingLong(…))`, `TreeMap::new` và vai trò tham số giữa.
- L04: không kẹt cứng; dày nhất là bảng sym 8 mục (nhãn, `@interface`, `@Retention`, `X.class`, `getDeclaredFields`, `isAnnotationPresent`, `newInstance/f.set`, tiêm phụ thuộc).
- L05: không kẹt (intuition step 6: "C(4,2) = 6" chỉ là ký hiệu bổ trợ).
- L06: không kẹt (junit step 5: cờ của JUnit chỉ cần để đọc, lab không dùng).
- L07: scale step 7: "số lần kiểm khi chia đôi ≈ log₂ n" (log₂ chưa giảng).
- L08: sym step 1 và intuition step 2: "tính theo UTC", `2026-03-08T07:30:00Z`, `PT23H`, `P3M` (ký hiệu chưa giảng).
- L09: example step 5 (`DocSoCai.duyet(Path p, Consumer<GiaoDich> khiDoc)`) rồi step 11 `DocSoCai.duyet(Path.of(args[0]), ds::add)`: `Consumer` và tham chiếu hàm gắn đối tượng.

## 6. Số đã tính lại / mã đã chạy

Chạy thật bằng JDK 21 (mọi chương trình trên màn hình tự dựng lại từ chữ trên video, kể cả khung nạp tên): khoảng 98 chương trình/lệnh/lab; 98 khớp từng dòng với đầu ra ghi trên màn hình (kể cả số dòng trong dấu vết ngăn xếp L07, phiên jdb, `javap` ở L04, JUnit pass/fail ở L06, OOM ở 32 MB cho L01/L03/L09, `findDeadlockedThreads` = 2 ở L05, 4/20 lần kiểm ở L07, kết quả 8 dòng sổ cái sạch và lỗi ở L09 với dữ liệu tự dựng khớp mọi số trên màn hình). Phân bố: L00 12, L01 10, L02 8, L03 8, L04 9, L05 11, L06 6, L07 9, L08 14 (một chương trình in 30 dòng), L09 11. Đo thời gian L05 (10 luồng 2 472 ms, 100 luồng 249 ms) khớp lý thuyết 2 000/200 ms; DuaTranh chạy 4 lần đều < 2 000 000.

Python tính lại: 2^64/1e9/86400/365,25 = 584,54 năm; 640 800 000 000/365 000 = 1 755 616,438; 50e6×0,048×40/365 = 263 013,6986; 120e6×0,06×95/365 = 1 873 972,603; n·log₂n (1 000; 100 000; 1 000 000) = 9 966; 1 660 964; 19 931 569; (int)(3e9−1) = −1 294 967 297; tổng 1 triệu dòng L01 3 999 998 000 và chia ba nhóm L03 (1 333 332 000/1 333 334 000/1 333 332 000); tổng sổ cái 1 triệu dòng L09 1 333 334 000; 5^3, 5^6, 5^10, 6^4; log₂ 16/10^6/10^9 = 4/20/30; nhật ký 5 184 000 000 / 518 400 000 000 / 51 840 000 000 000 byte; Little 5/500/50 000. Tất cả khớp, trừ ba chỗ cắt (không làm tròn) ở bảng 2: ",43" (đúng ",44"), "584 năm" (584,54), và quiz L06 thiếu điều kiện làm tròn.

Lời đọc: mọi câu của `say` (1 570 câu, 10 bài) có mặt nguyên văn trong `.srt` (0 câu thiếu). `asr_report.md` L00/L05/L08 chỉ gắn cờ câu có âm thuần Việt (đã ghi "chưa kiểm bằng tai người" trong YAML của L00).

## 7. Khung hình đã xem (≥ 5 mỗi bài, ở `D:/research-video/out/JV2/<Lxx>/frames/`)

- L00: 00003, 00029, 00071, 00108, 00134. Sạch.
- L01: 00047, 00094, 00114, 00127, 00140. Lỗi: 00094 chú thích mã tràn viền khung.
- L02: 00025, 00067, 00085, 00110, 00124. Sạch.
- L03: 00036, 00067, 00114, 00127, 00153. Sạch.
- L04: 00033, 00081, 00090, 00133, 00148. Sạch.
- L05: 00025, 00034, 00088, 00115, 00144. Lỗi: 00088 chú thích tràn viền khung.
- L06: 00022, 00076, 00091, 00117, 00134. Lỗi: 00022 nhãn "biên 2" đặt dưới chấm biên 1 triệu.
- L07: 00022, 00078, 00102, 00129, 00145. Sạch.
- L08: 00023, 00060, 00088, 00111, 00126. Sạch (số ",43" cắt, bảng 2).
- L09 (bản dựng hiện có): 00023, 00061, 00078, 00104, 00132. Sạch.
Nhận xét chung về hiển thị: chữ đọc được, không đè chữ; nội dung chỉ dùng nửa trên khung hình, nửa dưới trống (không phải lỗi).

## 8. Nhận xét chung

- Độ chuẩn xác cao: 0 MUST; toàn bộ mã trên video chạy đúng, toàn bộ số khớp. Còn 8 SHOULD nhỏ, sửa trong vài phút (bảng 2).
- Điểm yếu duy nhất theo ngưỡng chốt là P1 (50%): mỗi chỗ chỉ thiếu 1–3 thuật ngữ, rõ nhất là log₂ (L02, L07), `TreeMap::new` (L03), UTC và ký hiệu `PT23H`/`P3M` (L08), `Consumer`/`ds::add` (L09). Thêm một câu giảng tại chỗ cho từng chỗ là đủ.
- Lab rất tốt: 10/10 làm được ngay, đề cho đủ dữ liệu và danh sách import, kết quả mong đợi khớp màn hình; `cham.sh` chạy 3–11 giây. L06 chấm bản chưa sửa là cố ý và được ghi rõ.
- P9 thật sự có nội dung: mỗi bài có số ở ≥ 2 quy mô, được đo thật (OOM ở 32 MB, đo 10 và 100 luồng, 18 640 873 lần so sánh), kèm đánh đổi; quy mô hơn mức kỳ vọng của một khoá "trung cấp".
- Mỗi bài tự đứng được: phần "Ôn lại" đưa lại đủ nền của bài trước, không bài nào nhắc khoá khác thay cho giảng.
- Rủi ro duy nhất đáng sửa trước khi chốt "bắt đầu học": nhãn hình L06 và gợi ý dòng 15 của L07 (người học sẽ đối chiếu trực tiếp với hình/tệp); và đồng bộ mục tiêu "nhiều gói" của L09.
- L09 chưa kiểm khung hình bản dựng lại (đang dựng); đặc tả YAML đã đọc trọn, mã dự án 10 tệp đã dựng lại và chạy khớp.
