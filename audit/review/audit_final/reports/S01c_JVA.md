# S01c JVA: đã đọc 13/13 bài (vòng 3, độc lập)

Ngày đọc: 2026-11-14. Tiêu chí: `sample_f/BRIEF.md` (A, P1-P7) + `ADDENDUM.md` (P8, P9, "Cần biết trước", "Người học kẹt ở đâu"). Không mở báo cáo cũ, plan, handover.
Cách làm: tôi đọc trọn `title/objectives/show/say/checks/quiz` cả 13 YAML (trích văn bản bằng `lv.load_yaml`), tự viết và chạy lại mã Java trên màn hình (JDK 21.0.13), tính lại số, ghép và chạy cảnh `tep` của L12.
Hai việc tôi giao cho tác tử phụ (đọc kho, không sửa): (a) chạy lab như người học cho 13 bài; (b) so từng câu `say` với `.srt` và xem khung hình (hai tác tử, L00-L06 và L07-L12). Tôi tự kiểm lại hai phát hiện của (b) bằng cách xem trực tiếp `L05/frames/00070.png` và `L06/frames/00066.png` (cả hai đúng). Số khung do tôi tự xem: 2; số khung do tác tử xem: 10-27 mỗi bài.
Giới hạn trung thực: tác tử lab biết Java sẵn nên cột "tự làm được" chưa đo được độ vất vả của người mất gốc thật; thời gian là ước lượng.

**Kết quả so với ngưỡng chốt: MUST = 0 (đạt). P1 = 2 ở 12/13 bài = 92% (đạt, L03 = 1). P8 = 2 ở 13/13 = 100% (đạt).**

## Kiểm bản dựng
`lv.spec_digest(YAML hiện tại)` == `build_report.json:spec_sha256`: 13/13 khớp (L00-L12), `built_at` mới hơn YAML. SRT khớp `say` 100% ở 13 bài (L00 160/160, L01 141/141, L02 140/140, L03 145/145, L04 140/140, L05 106/106, L06 110/110, L07 105/105, L08 125/125, L09 129/129, L10 142/142, L11 130/130, L12 151/151 câu; 0 thiếu, 0 thừa, 0 sai số, 0 đảo).

## 2. Bảng chuẩn xác
MUST: không có. Mọi số/mã/kết quả trên màn hình tính lại hoặc chạy lại đều khớp (mục 6).

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L02 | SHOULD | quymo step 0 (say) | "Phí chính xác của một lệnh ở ví dụ trước có phần lẻ tám trăm ba mươi lăm phần nghìn đồng" | Tham chiếu tới ví dụ chưa xem: phí 0,5% của 1 234 567 (6 172,835) chỉ xuất hiện ở cảnh `pitfalls` step 2-3. `chapters.txt`: quymo 07:39, pitfalls 08:31. Không cảnh nào trước đó nhắc 1 234 567 | Đổi thành "ta lấy số tiền 1 234 567, phí 0,5%..." hoặc đưa pitfalls lên trước | CONFIRMED |
| L10 | SHOULD | quymo step 1 (say) | "khối bắt rỗng nuốt lỗi như ở phần lỗi thường gặp" | Khối bắt rỗng chỉ được dạy ở cảnh `pitfalls` (09:24), sau quymo (08:21) | Nêu ngay "khối bắt rỗng là khối catch không làm gì" | CONFIRMED |
| L00 | SHOULD | quymo step 0 (say) vs hình | "chết ở giữa thì gần tám phút công việc đã làm dở" | Hình ghi "499,999 giây ≈ 8,3 phút"; 8,3 > 8 nên "gần tám" lệch hướng (tính lại 499,999/60 = 8,33) | "hơn tám phút" | CONFIRMED |
| L09 | SHOULD | formula step 2 (hình) | bảng "vòng 1..4" | Mảng `loai` có 6 phần tử (NAP,RUT,NAP,CK,NAP,RUT) nhưng bảng chỉ có 4 vòng; kết quả NAP=3, RUT=2 nói ở step sau không suy ra được từ bảng. Cùng step: lời nói "lấy thường sẽ trả giá trị rỗng... báo lỗi" trong khi hình vẫn là `getOrDefault` (khung 00045) | Thêm hai hàng vòng 5-6; thêm dòng `dem.get(t)` có chú thích lỗi | CONFIRMED (YAML + khung) |
| L05 | SHOULD | pitfalls step 0 (hình) | `...ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 5` | Ký tự "5" cuối bị cắt ở mép phải khung (tôi xem `L05/frames/00070.png`) | Xuống dòng hoặc thu cỡ chữ | CONFIRMED |
| L06 | SHOULD | quymo step 1 (focus) | focus `[1,'1.2','1.3']` | Khung `00066`: lời "Mười chỗ chỉ còn khoảng tám mươi hai phần trăm" nhưng ô sáng là hàng "1 / 980"; hàng "10" phải sáng (tôi xem khung). Cùng kiểu: example step 1 và 3 (khung 00047, 00051: sáng ① khi lời nói ②, sáng ④ khi lời nói ⑤) | `[1,'1.3','1.4']` như L05 | CONFIRMED (00066 do tôi xem; 00047/00051 do tác tử) |
| L04 | SHOULD | example step 1 và 3 (focus) | khung 00053, 00059 | Lời nói phép ② (502 500) / ⑤ (tháng 12) nhưng khung cam sáng dòng ① / ④ | Sửa focus cho khớp số câu | CONFIRMED (tác tử) |
| L12 | SHOULD | tep (8 step) | "Đây là toàn bộ tệp, chia thành tám phần để bạn gõ lại" | 8 phần chạy trong 57 s (05:41-06:38), không step nào có `pause`; người học phải tự bấm dừng 8 lần trong khi lời chỉ đọc 1 câu mỗi phần | Thêm `pause` 30-60 s mỗi phần, hoặc dặn "dừng ở mỗi phần" | CONFIRMED |
| L07/L08/L10/L11 | SHOULD (hiển thị) | nhiều khung | xem mục 7 | Số "50 000" ngắt dòng (L11 00112), nút cam đè viền khung mã (L10 00114), mã HaiLuong chia hai màn không có dấu "tiếp" (L10 00072/00074), "this.;" (L07 00092), chuỗi "→" tổng kết ngắt dòng, chữ SVG ~20 px | chỉnh bố cục | CONFIRMED (tác tử) |
| L02/L04 | SHOULD (nhỏ) | hình | "− 7/2" (KaTeX dựng dấu trừ như toán tử hai ngôi); "33 333.333…", "528 197.895" dấu chấm thập phân khi nơi khác dùng dấu phẩy | thống nhất dấu | CONFIRMED (tác tử) |
| L04 | SHOULD (nhỏ) | prereq | "Ta ôn lại bốn điều" | bảng có 5 hàng | sửa thành "năm" | CONFIRMED |
| L00, L01, L05, L08 | SHOULD (nhỏ) | say vs hình | "mã bai", "bốn bai" | Lời đọc "bai" (lexicon) còn màn hình ghi "byte"; ASR cũng chép lệch (`asr_reviewed` của L00). Người mới nghe "bai" rồi thấy "byte" không có chỗ nào nói hai chữ là một | Giảng một lần: "chữ byte, đọc là bai" | CONFIRMED |

Lab (do tác tử chạy, tôi kiểm lại de.md L07, L11): SHOULD, không có MUST.
- S-lab1 (13 bài): đề ghi `bash labs/cham.sh JVA Lxx <tệp>` nhưng người học đang ở `~/hoc/jva`; từ đó lệnh cho `No such file or directory`. Cần nói chạy từ thư mục gốc kho, hoặc đưa đường dẫn tuyệt đối.
- S-lab2 (L07): de.md viết "`toString()` trả ..." thiếu `public`; bỏ `public` thì `error: ... attempting to assign weaker access privileges; was public`. Video có `public` nhưng chỉ hứa giải thích ở bài 11.
- S-lab3 (L09): `ArrayList<Long>` nhận `300000` không đuôi `L` gây `incompatible types: int cannot be converted to Long`; đề không nhắc.
- S-lab4 (L12, mức cao nhất): đề không nêu lời nhắn của `lay()`; mong_doi dòng 4 là `SAI LENH Khong co tai khoan Z`, bỏ lời nhắn cho `SAI LENH null` (cham.sh báo KHÁC). Nên ghi `"Khong co tai khoan " + stk`.
- S-lab5: L10 chưa nêu `getMessage()`; L12 chưa nêu định dạng dòng `P=... Q=... R=...`; L02 dùng lại biến `tong` ở mục 3.

## 3. Bảng độ sâu
sha16 YAML lúc đọc. Phút = `timeline_seconds`/60. Điểm P1-P7 là của tôi.

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1-P7) | Mất gốc | Cần biết trước (dùng, không giảng tại chỗ) | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 8c665d917859efa9 | 15,7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | cài JDK, Git for Windows, trình soạn mã (chỉ có tên, không hướng dẫn cài); "lô", "đối soát", "mili giây" | "gần tám phút" lệch 8,3 |
| L01 | 873017944dd8f025 | 14,7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | "biểu thức" (nói trong jshell, giảng ở L02) | "bai" vs "byte" |
| L02 | 456b8823e75621d6 | 13,9 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "đối soát" (giảng ở L08), "phí 0,5%" | quymo nói "ví dụ trước" trước khi ví dụ đó xuất hiện |
| L03 | 086fc8df2cd3dc7b | 13,3 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "biên" và "kiểm thử" dùng ở hook, chỉ hiểu dần ở formula/quymo | định nghĩa "biên = số nằm đúng ranh giới hai bậc" ngay hook |
| L04 | 50b456559f76a892 | 13,7 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "lãi kép" (giảng tại chỗ), "hạn mức" (giảng) | ô sáng lệch lời ở example (00053, 00059) |
| L05 | fa0fe0aad8902c5b | 11,3 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "cơ sở dữ liệu / chỉ mục" (mới nhắc, có giải thích ngắn) | dòng ngoại lệ bị cắt chữ "5" |
| L06 | e97a625c8dd7523a | 11,5 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "xác suất" (dùng ở quymo) | ô sáng lệch lời ở example và quymo |
| L07 | 04cd7d925a5c035c | 11,2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | lý do `public toString()` (hẹn bài 11) | đề lab thiếu `public` |
| L08 | 0821e7f04fb0f972 | 13,3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | không có đáng kể | chữ ghi chú nhỏ ở hình |
| L09 | 95fdb496d5957697 | 13,6 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "gói/thư viện", "cấu trúc dữ liệu" | bảng đếm thiếu vòng 5-6; hình lệch lời "get ra null" |
| L10 | 3605a67a0382fcc2 | 14,3 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "nhật ký (log)" | quymo nhắc pitfalls trước khi dạy; mã HaiLuong chia hai màn |
| L11 | 145091c852021750 | 13,9 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | "khung phần mềm" (giảng), JUnit/Spring (chỉ nhắc) | số "50 000" ngắt dòng |
| L12 | 605652330f794825 | 16,3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | "giao dịch cơ sở dữ liệu" (chỉ nhắc, hẹn khoá sau) | cảnh `tep` không dừng cho gõ; đề lab thiếu lời nhắn `lay` |

Ghi chú chấm: P1 = 1 chỉ cho L03 (khái niệm then chốt "biên" dùng từ hook mà chưa định nghĩa). P8 = 2 ở cả 13 bài vì mỗi bài có lab với `mong_doi.txt` chạy được bằng `cham.sh`, cộng jshell (L01, L02) và lệnh chạy từ dòng lệnh (L03, L04). P9 = 2 ở cả 13 bài, có số liệu ≥ 2 mức quy mô và đánh đổi: L00 (10/1000/1 000 000 lệnh), L01 (100/2147/2148/10 000 lệnh), L02 (1/1000/1 triệu lệnh/365 ngày: 835 → 304 775 000 đồng), L03 (3/10/100 bậc; 2^n tổ hợp), L04 (12/120/360 tháng: lệch 5/81/509), L05 (5/5000/5 triệu ô), L06 (1/10/100 chỗ chép: 980/817/132 phần nghìn), L07 (1000/100 000/1 triệu dòng), L08 (1000/1 triệu/100 triệu dòng: 19 KB đến 1,9 GB), L09 (1000/1 triệu tài khoản, danh sách và bản đồ), L10 (1000/100 000/1 triệu lệnh), L11 (3/10/50 loại phí), L12 (3/1000/10 000/1 triệu tài khoản).

## 4. Lab (chạy bằng `cham.sh JVA Lxx`, JDK 21)
Cả 13 bài: chấm ĐÚNG ngay lần đầu; `loi_giai.java` mẫu chạy ĐÚNG 13/13; mong_doi khớp đề ở 13/13. Thời gian là ước lượng của tác tử (đã biết Java).

| Bài | tự làm được | thời gian (phút) | kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L00 | có | 15 | không; lệnh chấm mơ hồ về thư mục (S-lab1) | có |
| L01 | có | 15 | không | có (750000, 6600, 743400, -1894967296, 2400000000 tính lại đúng) |
| L02 | có | 15 | `tong` mục 3 dùng lại biến hoá đơn | có (357142 dư 6; 2962; 2961) |
| L03 | có | 15 | không | có (40000; 9999999 và 100000000 cũng khớp) |
| L04 | có | 15 | không | có (6 tháng, tháng 4 vượt 51 triệu) |
| L05 | có | 20 | không | có (7210000; 90000 ở chỉ số 5; 3) |
| L06 | có | 20 | không | có (1100, 3300, 7996700, 10500000) |
| L07 | có, cần chú ý | 25 | đề thiếu `public toString()` (S-lab2) | có |
| L08 | có | 25 | không | có (3 625 000; 2 lệnh trên 1 triệu) |
| L09 | có, cần chú ý | 20 | thiếu hậu tố `L` (S-lab3) | có |
| L10 | có | 25 | không nêu `getMessage()` | có |
| L11 | có | 30 | không | có (40000 320000 / 30000 400000 / 20000 / true false / 100000000) |
| L12 | có, cần chú ý | 45 | lời nhắn `lay()` không có trong đề (S-lab4) | có (P=2200000 Q=1300000 R=500000, tổng 4000000) |

Tôi tự xác nhận de.md L11 nêu đủ hạn mức THUONG 20 000 000, VANG 100 000 000 và L07 nêu đủ định dạng dòng từ chối. Bỏ `catch` ở L10 như đề gợi ý cho `error: unreported exception HetHanMuc; must be caught or declared to be thrown` (khớp ý bài).

## 5. Người học kẹt ở đâu (một dòng mỗi bài)
- L00: không kẹt ở nội dung; có thể kẹt trước khi bắt đầu: cài JDK/Git Bash/trình soạn mã chỉ được nhắc tên ("Mở Git Bash: cửa sổ lệnh đi kèm Git for Windows"), không có bước cài.
- L01: không kẹt (jshell và `Integer.MAX_VALUE` đều được giảng).
- L02: không kẹt ở thao tác; có thể hụt ở quymo step 0 "Phí chính xác của một lệnh ở ví dụ trước" (chưa có ví dụ phí).
- L03: hook "dấu so sánh đặt tại biên của bậc phí" và "kiểm thử ở đúng biên": hai chữ này chưa được định nghĩa, phải đợi tới cảnh formula/quymo.
- L04: không kẹt; ô sáng lệch lời ở example ("Phép tính thứ hai..." sáng dòng ①).
- L05: không kẹt (tham chiếu, thuộc tính, chỉ mục đều được giảng).
- L06: không kẹt về nội dung; ô sáng lệch lời ở quymo ("Mười chỗ..." sáng hàng 1).
- L07: không kẹt khi xem; khi làm lab dễ kẹt ở "toString() thiếu public" vì lý do hẹn tới bài 11.
- L08: không kẹt; "biểu thức chính quy" chỉ cần biết tồn tại, đã giải thích trong cảnh check.
- L09: formula step 2: bảng đếm dừng ở vòng 4 trong khi mảng có 6 phần tử, rồi kết quả "nạp ba, rút hai" xuất hiện mà không thấy vòng 5-6.
- L10: quymo step 1 "như ở phần lỗi thường gặp" (chưa học khối bắt rỗng); mã HaiLuong chia hai màn nên có thể tưởng thiếu mã.
- L11: không kẹt; "khung phần mềm" và nhãn Spring/JUnit chỉ cần nhận ra, bài nói rõ không dạy.
- L12: cảnh `tep` chạy 57 s cho 8 phần, người học phải tự dừng nhiều lần; đề lab không cho chuỗi lời nhắn của `lay()`.

## 6. Số đã tính lại / mã đã chạy
- Mọi `checks` trong YAML (biểu thức Python do bài ghi): 284/284 đúng (L00 19, L01 29, L02 36, L03 27, L04 30, L05 17, L06 13, L07 13, L08 21, L09 18, L10 14, L11 15, L12 32). Đây là kiểm chứng của người viết, không tính là độc lập.
- Tự viết lại bằng Java (độc lập với `checks`) rồi chạy, so với chữ trên màn hình: khoảng 110 giá trị/dòng in, khớp 100%: L00 bảng lô (10/1000/1 000 000), L01 (-1594967296; 2147000000; -2146967296; 1410065408; -2147483648; 0.30000000000000004; -294967296; 2700016500; -1894967296; 9223372036854), L02 (3, 3.5, 1, -3, -1, -33333, -1, 3.0, 0, 6170, 6172, 835, 835, 835000, 304775000, 357142, 6, 2962, 2961), L03 (phí 0/2200/5500; 6/27/297 ca), L04 (LaiThang tháng 1-3, 11, 12 và 12/120/360 tháng: lệch 5/81/509; 0.9999999999999999; lab 6 tháng; 4 lệnh vượt; tổng 19), L05 (5/5000/5 000 000 bước; 9700000/4000000/2; "5 6", "1 3"), L06 (500000 600000; 2997800; 2200 6600; 980/817/132; "5 10", 40), L08 (13 N 6 Nguyen|Van An; 10; 1,234,567; 12345671; "0 2 234"; 13 9; T45; 7; 50005000; 19000 byte), L09 (3 2 1 null 3; true false true; ConcurrentModificationException; [A01, C03, D04]; [1200000, 450000, 300000, -50000]; 1000 và 1 000 000 bước), L10 (1/100/1000 lệnh bị nuốt), L12 (N=3 M=4: 12; 1 000 000; 100 000 000). Phép thời gian L12: 10^12 x 10 ns = 10 000 s = 2,78 giờ đúng.
- **L12, ghép nguyên văn 8 phần cảnh `tep`** (trích từ HTML YAML, dòng trống `<div> </div>` là dòng trống): ra tệp 83 dòng; `javac`+`java` cho đúng 6 dòng như màn hình (OK ..., TU CHOI B chi co 800000, SAI LENH Khong co tai khoan X, OK ..., A=900000 B=800000 C=1300000, Tong 3000000). Gõ lại lỗi theo chữ nhỏ, so số dòng dấu vết:
  - Lỗi 1 (SoLoi.java, `b` thành `a`): `kiem(SoLoi.java:54)`, `chuyen(SoLoi.java:49)`, `main(SoLoi.java:72)`, dòng đầu `Lech tong 3500000 != 3000000`: KHỚP.
  - Lỗi 2 (nuốt ngoại lệ): in `SAI LENH Khong co tai khoan X`, `A=2500000 B=300000 C=2100000`, `Tong 4900000`: KHỚP.
  - Lỗi 3 (CuoiNgay.java, bỏ `kiem();`, thêm `so.kiem();` cuối main): 6 dòng + `Lech tong 4900000 != 3000000`, `kiem(CuoiNgay.java:53)`, `main(CuoiNgay.java:81)`: KHỚP.
  - Lỗi 4 (TuChuyen.java, bỏ 3 dòng chặn, 1 lệnh A->A): `Lech tong 3100000 != 3000000`, `kiem(TuChuyen.java:51)`, `chuyen(TuChuyen.java:46)`, `main(TuChuyen.java:66)`: KHỚP.
  - Cảnh `check` L10: Vet.java đúng 12 dòng, vết `chia:3`, `chiaPhi:6`, `main:10` (đọc từ mã: đúng).
  - Số lần chạy L12: 5 chương trình, 5 khớp.
- Lab: 13 bài, `cham.sh` 13/13 ĐÚNG với `loi_giai.java`; 13/13 ĐÚNG với bài tự viết của tác tử.
- Sai lệch tìm thấy: không có số sai. Chỉ lệch diễn đạt ("gần tám phút").

## 7. Khung hình đã xem (tên png trong `out/JVA/Lxx/frames/`) và lỗi hiển thị
Do tác tử xem (số khung ≥ 5 mỗi bài, đa số ≥ 10) và kiểm tra chữ tràn/đè/cắt, hình-lời, cỡ chữ; tôi xem lại 2 khung (đánh dấu *).
- L00: 00000, 00024, 00043, 00067, 00077, 00081, 00096, 00113, 00122, 00154. Lỗi: chú thích dính `;` ở Tong.java dòng 4 (00067); chữ SVG ~20 px (00043).
- L01: 00000, 00025, 00029, 00045, 00059, 00065, 00087, 00100, 00115, 00137. Lỗi nhẹ: `tong` không còn trên màn hình ở 00059 (do `clear`).
- L02: 00000, 00014, 00019, 00026, 00033, 00055, 00064, 00070, 00088, 00118, 00139. Lỗi: dấu trừ KaTeX tách ("− 7") ở 00064; dấu thập phân không thống nhất.
- L03: 00000, 00016, 00031, 00044, 00050, 00061, 00070, 00080, 00091, 00105, 00117, 00119, 00143. Lỗi nhẹ: chữ SVG nhỏ (00031).
- L04: 00000, 00020, 00025, 00036, 00044, 00053, 00059, 00072, 00086, 00098, 00111, 00139. Lỗi: ô sáng lệch lời 00053, 00059.
- L05: 00000, 00011, 00021, 00025, 00034, 00045, 00062, 00070*, 00083, 00105. Lỗi: dòng ngoại lệ cắt chữ "5" (00070, tôi xác nhận); sơ đồ tham chiếu 3 ô khác mảng 5 ô (00025).
- L06: 00000, 00009, 00021, 00042, 00047, 00051, 00066*, 00079, 00087, 00109. Lỗi: focus lệch lời 00047, 00051, 00066 (tôi xác nhận 00066).
- L07: 00000, 00015, 00024, 00033, 00045, 00048, 00070, 00077, 00080, 00085, 00092, 00096, 00103. Lỗi: chữ nhỏ xanh trên nền nhạt (00024); mũi tên tổng kết ngắt dòng (00103); "this.;" (00092).
- L08: 00000, 00012, 00022, 00035, 00046, 00057, 00060, 00078, 00090, 00095, 00098, 00102, 00110, 00122. Lỗi nhẹ: ghi chú xám nhỏ (00022).
- L09: 00000, 00020, 00034, 00041, 00045, 00047, 00055, 00063, 00068, 00080, 00091, 00093, 00103, 00107, 00115, 00126. Lỗi: bảng thiếu vòng 5-6 (00047); hình lệch lời (00045).
- L10: 00000, 00018, 00030, 00045, 00058, 00064, 00072, 00074, 00076, 00077, 00081, 00082, 00084, 00103, 00114, 00118, 00125, 00128, 00139. Lỗi: nút cam đè viền khung mã (00114); mã HaiLuong chia hai màn (00072/00074).
- L11: 00000, 00012, 00020, 00022, 00025, 00033, 00038, 00044, 00054, 00057, 00062, 00072, 00090, 00098, 00100, 00104, 00112, 00126. Lỗi: "50 000" ngắt dòng (00112).
- L12: 27 khung gồm cả cảnh `tep` (00060, 00062-00069, đủ 8 phần) và `pitfalls` (00089, 00091, 00098, 00100, 00113, 00115): không tràn, không cắt; khung 00100 viền cả bảng trong khi lời chỉ nói hàng 1; 00146 mũi tên "→" ngắt dòng.
Không thấy ô vuông, TeX hỏng, chữ đè chữ ở khung nào đã xem.

## 8. Nhận xét chung
- Chặn MUST đạt: không kiến thức sai, không số sai, không mã không chạy; mọi mã trên màn hình (kể cả toàn bộ So.java và bốn kịch bản lỗi của L12 với số dòng dấu vết) chạy ra đúng chữ trên hình.
- Khoá đủ cho người mất gốc ở cả 13 bài theo thang BRIEF (tổng 13-14/14, không mục nào 0); yếu tố còn thiếu là thiết lập môi trường ở L00 (cài JDK, Git Bash, trình soạn mã) và "biên"/"kiểm thử" ở hook L03.
- Hai lỗi thứ tự (L02 quymo và L10 quymo nhắc điều dạy ở cảnh sau): cùng một kiểu, sửa bằng một câu mỗi bài hoặc đổi thứ tự cảnh.
- Cụm lỗi lặp lại duy nhất ở phần hình: `focus` lệch một ô ở L04, L06 (số phần con tính cả hàng tiêu đề); sửa theo quy ước L05 đã đúng.
- Lab: đề dùng lệnh `bash labs/cham.sh ...` không chạy được từ thư mục người học đang đứng ở cả 13 bài; lỗi chung này có thể sửa một chỗ (nói rõ chạy từ thư mục gốc kho). Đề L12 cần ghi chuỗi lời nhắn của `lay()`; đề L07 cần `public` ở `toString()`; đề L09 cần nhắc hậu tố `L`.
- L12 cảnh `tep`: nội dung đúng, nhưng chưa có `pause` nên "gõ lại từng phần" phụ thuộc người học tự dừng.
- P9 làm tốt và nhất quán (số liệu 2-4 mức quy mô mỗi bài); P8 đạt 100% nhờ lab có mong_doi tự chấm.
- Chưa kiểm được: tai người (ASR chỉ so chữ), người học mất gốc thật trước các lab (tác tử lab đã biết Java).
