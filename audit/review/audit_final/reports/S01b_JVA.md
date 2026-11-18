# S01b JVA: đã đọc 13/13 bài

Người đọc độc lập vòng 2, ngày 2026-11-14. Đọc trọn `show` + `say` + `checks` + quiz của 13 YAML `lessons/jva/L00..L12`, mục tương ứng `curriculum/jva.yaml`, đối chiếu `.srt` với `say`, chạy lab như người học (JDK 21.0.13, `labs/cham.sh`), tự biên dịch/chạy lại mã trên màn hình, xem khung hình. Không mở báo cáo/handover/plan cũ; không sửa gì trong kho (chỉ tệp này).

Kiểm toàn vẹn video: `build_report.spec_sha256 == lv.spec_digest(YAML hiện tại)` đúng cả 13 bài; chuỗi `say` khớp `.srt` 100% (SequenceMatcher = 1.0000, số cue = số khung = số câu `say`). Lưu ý: mtime YAML L08, L10 (00:03 14/11) muộn hơn `built_at` nhưng digest vẫn khớp, nên video đúng đặc tả hiện tại.

## 2. Bảng chuẩn xác (chỉ lỗi có bằng chứng)

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L12 | MUST (theo chữ BRIEF: kết quả khác điều bài nói; tác động thấp) | pitfalls[0], [5], [6] | "Gõ lại thành So.java rồi gài lỗi này, dấu vết hiện So.java với đúng các số dòng ấy." Màn hình: `at SoCai.kiem(SoLoi.java:54)`, `…chuyen(SoLoi.java:49)`, `SoLoi.main(SoLoi.java:72)`; `CuoiNgay.java:53/81`; `TuChuyen.java:51/46/66` | Ghép nguyên văn 7 phần ở scene `tep` thành So.java (script `r2_jva/t12/assemble.py`), áp đúng chỉnh sửa bài mô tả, chạy: lỗi 1 ra `So.kiem(So.java:53)`, `So.chuyen(So.java:48)`, `So.main(So.java:70)`; lỗi 3 ra `So.java:52` và `:79`; lỗi 4 ra `So.java:50/45/64`. Số dòng và tên lớp (SoLoi/CuoiNgay/TuChuyen vs So) đều lệch; các phần chiếu không có dòng trống giữa phần nên người học không thể tái tạo 54/49/72. Thêm: "Biến thể CuoiNgay.java: bỏ dòng kiem(); trong chuyen, thêm so.kiem(); ở cuối hàm chính" không nhắc giữ lỗi `a + l.tien()`; áp lên So.java đã sửa thì chạy ra tổng 3000000, không có ngoại lệ (đã chạy, thư mục `cuoi_fixed`), khác màn hình 4900000. | Chiếu thêm dòng trống ở các phần để số dòng khớp, hoặc bỏ cam kết "đúng các số dòng ấy" và nói "số dòng của bạn có thể lệch, hãy đọc tên phương thức"; ghi rõ "giữ lỗi a + l.tien()" ở 2 biến thể | CONFIRMED |
| L04 | SHOULD | pitfalls[1] (khung ~#98) | `while (thang <= 12) { … // quên viết: thang++;` rồi "Kết quả chạy / Da 1000 vong, thang van = 1" | Mã chiếu thiếu `}` đóng vòng `while`; copy chạy sẽ báo `reached end of file while parsing`. Đã chạy bản thêm `}`: ra đúng dòng. | Thêm `}` | CONFIRMED |
| L10 | SHOULD | intuition[2] (khung #34); pitfalls[2] (#106) | `TaiNguyen.java` kết thúc ở `System.out.println("Loi doc: " + e.getMessage());` rồi chiếu "Kết quả chạy A01;500000…"; pitfalls[2] gọi `phiMoiLan(3000, 0)` | Tệp chiếu thiếu 3 dấu `}` (catch, main, class) và không có phần sau; `phiMoiLan` không được định nghĩa ở đâu. Runner báo `reached end of file`. Bản đủ ngoặc chạy ra đúng 2 dòng. | Chiếu đủ tệp (hoặc ghi "phần đầu") và định nghĩa/ghi chú `phiMoiLan` | CONFIRMED |
| L02 | SHOULD | sym[3] | `so sánh: < <= > >= == != → và: && → hoặc: ||` | Bảng ưu tiên gộp `<`/`>` và `==`/`!=` cùng một bậc; JLS §15.20 (quan hệ) cao hơn §15.21 (bằng nhau). Không ảnh hưởng ví dụ trong bài. | Tách hai bậc | PLAUSIBLE (đối chiếu JLS, không có ví dụ trong bài sai) |
| L08 | SHOULD | sym[0] | say: "Chương trình này thử sáu hàm trên tên Nguyễn Văn An." | Màn hình/mã dùng `"Nguyen Van An"` (không dấu), chuỗi có dấu sẽ có độ dài và chỉ số khác tuỳ mã hoá. Lệch lời–hình ở chi tiết nhỏ. | Đọc "Nguyen Van An" | CONFIRMED |
| L11 | SHOULD | check[0] | `GiaoDichThuong x = new GiaoDichThuong("A01", 500000);` | Lớp `GiaoDichThuong` không được định nghĩa trên màn hình (tôi phải tự khai báo lớp thường 2 trường để ra `false`). | Chiếu 3 dòng khai lớp | CONFIRMED |
| L07 | SHOULD (nhỏ) | formula[4] | say: "Hàm đổi ra chuỗi phải có từ khoá công khai, vì mọi đối tượng Java đã có sẵn một hàm cùng tên ở dạng công khai, và bản ta viết lại không được hẹp quyền hơn." | Lý do dựa vào kế thừa/ghi đè, mới dạy ở L11. Người học chỉ cần nhớ "phải public"; không sai kiến thức. | Rút gọn: "phải ghi public, bài 11 sẽ giải thích" | PLAUSIBLE |
| L00, L01, L03, L05, L06, L09 | — | | | không phát hiện lỗi | | |

Không có lỗi kiến thức, số, đáp án quiz hay mã không chạy (xem mục 6). Không có MUST nào ngoài dòng L12 ở trên.

## 3. Bảng độ sâu

sha16 = sha256 16 ký tự đầu của YAML lúc đọc. Phút = `timeline_seconds` trong build_report. Thang 0/1/2.

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 8c665d917859efa9 | 15.7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | Git Bash/VS Code đã cài (FND), cài JDK (bài không có bước cài, dựa FND:L10) | "lô giao dịch" không định nghĩa; `static` hoãn có đánh dấu forward_ref |
| L01 | 873017944dd8f025 | 14.7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | không | — |
| L02 | 56e71132caa9e7a6 | 13.8 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | không | bảng ưu tiên gộp bậc (SHOULD) |
| L03 | 086fc8df2cd3dc7b | 13.3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `echo … \|` ống (giảng 1 câu), `args` (forward từ L00) | — |
| L04 | 607c89eb9ccfab47 | 13.7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | không | mã pitfalls[1] thiếu `}` |
| L05 | fa0fe0aad8902c5b | 11.3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `int[]` ở quiz (bài chỉ dạy `long[]`, suy ra hiển nhiên) | — |
| L06 | e97a625c8dd7523a | 11.5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | không | — |
| L07 | 7e7f52004255de1e | 11.2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | lý do `public` của toString (kế thừa chưa dạy) | một câu hoãn nhỏ |
| L08 | c29006cead3275ba | 13.3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `throws Exception` (tạm giao, hẹn L10); mẫu split (giảng ở cuối cảnh check) | say "Nguyễn" vs mã không dấu |
| L09 | 95fdb496d5957697 | 13.6 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | lambda `->`, Comparator (chỉ đọc hiểu, đã giải thích bằng lời) | — |
| L10 | cd9112d8cc8fafe2 | 14.2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | lambda (từ L09), `Thread` (giảng trong bài) | tệp TaiNguyen và pitfalls[2] chiếu không đủ ngoặc |
| L11 | b828359cd2a248e3 | 13.8 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | tên Spring/JUnit chỉ nêu tên, bài nói không dạy | `GiaoDichThuong` không khai |
| L12 | b345e057fa1d9e48 | 15.7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | gõ lại 7 phần liền nhau | số dòng dấu vết không tái tạo được (MUST nhẹ ở mục 2) |

Tổng thời lượng 13 bài: 175.8 phút (≈ 2 giờ 56). P1 = 2 ở 13/13 bài (100%, ngưỡng 90% đạt); P8 = 2 ở 13/13 (100%, ngưỡng đạt); P9 = 2 ở 13/13. Mục tiêu giáo án: `objectives` trong 13 YAML trùng nguyên văn `curriculum/jva.yaml` (13/13), mỗi mục tiêu có `covers` trỏ đúng cảnh tồn tại (0 thiếu).

Ghi chú chấm P8/P9: cả 13 bài có cảnh `practice` với đề cụ thể, `mong_doi.txt`, lệnh chấm; thêm jshell (L01, L02), thử ở biên (L03, L06), biến thể gài lỗi (L12). P9: mọi bài có bảng số liệu ở ≥ 2–4 mức quy mô (ví dụ L04: 12/120/360 tháng, lệch 5/81/509 đồng; L05: 5/5 000/5 000 000 bước; L08: 19 KB/19 MB/1,9 GB; L12: N×M tới 10^12 phép cộng ≈ 2,8 giờ) kèm đánh đổi. Riêng L09, "bản đồ khoảng 1 bước" được ghi rõ là lấy từ mô tả HashMap, không đo (trung thực, không tính là lỗi).

## 4. Lab

Cách làm: đọc `de.md`, tự viết lời giải vào `scratchpad/r2_jva/lab/Lxx/` (chưa mở `loi_giai.*`), chấm bằng `bash labs/cham.sh JVA Lxx <tệp>`, sau đó chạy `cham.sh` cho cả 13 `loi_giai.java` (13/13 ĐÚNG). Trung thực: tôi không phải người mất gốc; "tự làm được = có" nghĩa là mọi cấu trúc đề đòi đều đã được giảng trong chính bài (tôi đối chiếu từng cấu trúc với cảnh dạy).

| Bài | Tự làm được | Thời gian | Kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L00 | có | ≈2 s mỗi lần chấm; người học ước 15–30 phút (INFERRED) | không; bước 4 (xoá `;`) đã có mẫu lỗi `Thieu.java:3` trong bài, đã chạy lại, khớp | có (5 dòng khớp video) |
| L01 | có | ≈2 s | không | có |
| L02 | có | ≈2 s | không | có |
| L03 | có | ≈2 s; thêm `java BacLai 9999999` và `100000000` ra đúng 29999 và 500000 như đề | không (ternary, `args`, `Long.parseLong` đã dạy ở scene `nhap`) | có |
| L04 | có | ≈2 s | không | có |
| L05 | có | ≈2 s | không | có |
| L06 | có | ≈2 s | không | có |
| L07 | có | ≈2 s | không | có |
| L08 | có | ≈2 s | không (cần `throws Exception` và 3 import, đề nêu sẵn) | có |
| L09 | có | ≈2 s | không | có |
| L10 | có | ≈2 s; "bỏ khối catch rồi biên dịch" ra `unreported exception … must be caught or declared to be thrown` đúng như formula[2] | không | có |
| L11 | có | ≈2 s | không | có |
| L12 | có (đề dài, 3 mốc) | ≈2 s | chỉ có `mong_doi` của bản hoàn chỉnh, mốc 1–2 không có kết quả trung gian để tự đối chiếu (nhẹ) | có |

Thời gian của người học thật không đo được ở đây; con số "≈2 s" là thời gian máy.

## 5. Người học kẹt ở đâu (chỗ đầu tiên không theo được, nếu chỉ xem video này và các bài trước)

- L00: không kẹt nếu đã qua FND; nếu chưa, chậm ở formula[0] "Mở Git Bash… Cài bộ công cụ JDK" (không có bước cài).
- L01: không kẹt.
- L02: không kẹt.
- L03: không kẹt; chậm nhẹ ở nhap[3] `echo "300000 500000" | java RutNhap` (ống được giảng một câu).
- L04: pitfalls[1] nếu gõ lại mã thiếu `}`: lỗi biên dịch không có trong bài.
- L05: không kẹt.
- L06: không kẹt.
- L07: formula[4] "toString phải có từ khoá công khai, vì mọi đối tượng Java đã có sẵn một hàm cùng tên…" (lý do chưa học).
- L08: tep[0] `throws Exception` ("tạm giao cho máy ảo", chấp nhận được, hẹn bài ngoại lệ).
- L09: muiten[0] `gd.sort((a, b) -> Long.compare(b, a))` (cú pháp mũi tên chỉ đọc hiểu, giải thích bằng lời nhanh).
- L10: intuition[2] chiếu `TaiNguyen.java` thiếu 3 dấu `}`; luong[1] `new Thread(() -> { … tong[0] += i; })` (lambda chỉ nhắc "như ở bài danh sách").
- L11: check[0] `GiaoDichThuong` không có định nghĩa trên màn hình.
- L12: pitfalls[0] làm theo "Gõ lại thành So.java rồi gài lỗi này" thì số dòng dấu vết lệch.

## 6. Số đã tính lại / mã đã chạy

- `checks` trong YAML: 284 biểu thức, chạy lại bằng Python: 284/284 đúng (6 biểu thức đầu lỗi do tôi thiếu `import math/Fraction`, sau khi thêm đều đúng).
- Khối "Trình biên dịch báo" (lỗi biên dịch): 16 khối, tự tái tạo bằng `javac` JDK 21: 16/16 khớp thông báo (L00 ×4, L01, L03, L05, L06 ×2, L07, L09, L10 ×2, L11 ×3).
- Khối "Kết quả chạy" (đầu ra): 118 khối. Tôi biên dịch lại gần như toàn bộ chương trình (bằng bộ chạy tự động trích mã từ YAML cho các bài có chương trình đầy đủ, và bằng các tệp tự ghép cho phần còn lại: `t04`…`t12`). Khớp 115/118; 3 khối lệch đều ở L12 pitfalls[0], [5], [6] (số dòng/tên lớp trong dấu vết, mục 2). Các dấu vết khác (L10 `Vet.java` 12 dòng: `:3`, `:6`, `:10`; NPE; CME; ArrayIndexOutOfBounds) khớp.
- jshell: 12 dòng của L01–L02 chạy lại, khớp (`$2 ==> 300`, `s ==> -294967296`, `0.30000000000000004`, `true || 1 / 0 > 1 ==> true`).
- Số liệu quy mô tính lại: L04 12/120/360 tháng cho 106167776/181939592/602257012 so với 106167781/181939673/602257521 (lệch 5/81/509) đúng khi chạy Java; L05 5/5000/5000000 bước; L08 19000 byte cho 1000 dòng; L10 1/100/1000 lệnh bị nuốt; L12 12/10^6/10^8 phép cộng chạy thật, 10^12×10 ns = 10 000 s = 2,8 giờ.
- Kết quả tôi tính tay lại và so với video: tất cả 13 phần quiz đúng.

## 7. Khung hình đã xem (≥ 5 mỗi bài)

Tổng 108 khung (ghép 4 khung/ảnh, đọc ở 960x540 mỗi khung). Chỉ số = số thứ tự `frames/NNNNN.png`.
- L00: 0, 12, 34, 56, 74, 83, 97, 107, 117, 125, 138, 154
- L01: 1, 31, 43, 59, 87, 100, 117, 124
- L02: 1, 42, 54, 87, 102, 115, 121, 137
- L03: 1, 53, 60, 72, 94, 104, 119, 143
- L04: 1, 25, 59, 88, 98, 112, 126, 138
- L05: 1, 24, 36, 46, 61, 75, 82, 95
- L06: 1, 14, 25, 49, 66, 76, 89, 92
- L07: 1, 14, 25, 37, 50, 58, 67, 80
- L08: 1, 21, 50, 53, 77, 90, 99, 112
- L09: 1, 34, 47, 56, 79, 98, 105, 117
- L10: 4, 24, 49, 71, 83, 94, 103, 128; thêm 34, 91, 106, 75
- L11: 1, 18, 46, 56, 78, 92, 102, 114
- L12: 1, 24, 65, 79, 86, 97, 118, 131

Lỗi hiển thị: không có chữ tràn, đè hay cắt ở các khung đã xem; cỡ chữ đọc được; hình cơ chế khớp lời đọc ở mọi bài (đường ống biên dịch L00, vòng số int L01, ngắn mạch L02, rẽ nhánh L03, lưu đồ vòng lặp L04, mảng và tham chiếu L05, sao chép giá trị/mũi tên L06, lớp–đối tượng L07, chỉ số ký tự và hai kiểu so sánh L08, hộp hoá L09, đường đi ngoại lệ L10, giao diện L11, hai bút toán L12). Duy nhất liên quan hiển thị: mã bị cắt không đủ ngoặc ở L04 pitfalls[1] và L10 intuition[2] (mục 2). Quan sát thiết kế (không phải lỗi): khoảng 50–60% diện tích phía dưới mỗi khung để trống vì nội dung chỉ dùng nửa trên.

## 8. Nhận xét chung

- Nội dung kiến thức chính xác: không tìm thấy lỗi kiến thức Java, số hay đáp án quiz nào trong 13 bài; mọi thông báo lỗi biên dịch và dấu vết chính tái tạo được trên JDK 21.0.13.
- Một vấn đề thực sự: L12 hứa người học gõ lại `So.java` sẽ thấy "đúng các số dòng ấy" nhưng không thể tái tạo (53/48/70 so với 54/49/72), cộng một biến thể thiếu chỉ dẫn giữ lỗi. Sửa nhanh bằng chiếu dòng trống hoặc bỏ cam kết.
- Ba chỗ mã chiếu thiếu `}` hoặc thiếu định nghĩa (L04 pitfalls[1], L10 TaiNguyen và phiMoiLan, L11 GiaoDichThuong): người học gõ lại sẽ gặp lỗi biên dịch không được dạy; sửa bằng cách chiếu đủ mã hoặc ghi "phần đầu".
- Cấu trúc sư phạm đồng đều và mạnh: mỗi bài có quy tắc, tính tay từng bước, quiz có dừng và lời giải theo bước, lỗi người mới/người đi làm, bảng quy mô, lab có `mong_doi`.
- Lab chạy sạch: 13/13 `loi_giai` ĐÚNG, 13/13 lời giải tự viết ĐÚNG ngay lần đầu.
- Video khớp đặc tả: digest khớp 13/13; chuỗi đọc khớp `.srt` 100%.
- Ngưỡng chốt: MUST 0 chưa đạt nếu tính dòng L12 (mức thấp, đọc theo chữ BRIEF); P1 = 2 đạt 13/13; P8 = 2 đạt 13/13. Nếu người điều phối xếp mục L12 là SHOULD thì ngưỡng đạt đủ.
- Hạn chế của tôi: tôi biết Java sẵn nên "tự làm được" được suy ra từ việc đối chiếu cấu trúc đề với cảnh dạy chứ không do thử người mất gốc; chưa nghe âm thanh (không kiểm giọng đọc).
