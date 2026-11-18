# S01 JVA: đã đọc 13/13 bài (L00–L12)

Phạm vi: `lessons/jva/*.yaml` (đọc trọn `show`, `say`, `checks`, quiz, lab), mục `curriculum/jva.yaml`, `out/JVA/Lxx/` (`.srt`, `chapters.txt`, `_frames.txt`, ≥ 6 khung hình mỗi bài), `labs/JVA/Lxx/`. Người đọc đóng vai mất gốc, chỉ giả định đã học FND (Git Bash, tệp, ống, PATH, soạn mã, đọc lỗi).
JDK dùng để chạy: Temurin 21.0.13. `curriculum/jva.yaml` sha16 `624338897a040795`. Không đọc `audit/jva/*` (không cần).

## Kết luận ngắn

| Chỉ số | Kết quả | Ngưỡng |
|---|---|---|
| MUST | 0 | 0 |
| SHOULD | 12 (xem mục 2) | — |
| P1 = 2 | 8/13 = 61,5% (L02, L03, L04, L05, L06, L07, L11, L12) | ≥ 90% (KHÔNG đạt) |
| P8 = 2 | 13/13 = 100% | 100% (đạt) |
| P9 = 2 | 13/13 | — |
| Mất gốc | 13/13 ĐỦ (tổng P1–P7 từ 12 đến 14, không mục nào 0) | — |
| Lab | 13/13 tự làm được, chấm `cham.sh` "ĐÚNG" ngay lần đầu | — |
| Bài kẹt thật | không bài nào chặn hẳn; kẹt nhẹ ở L06, L08, L10 (xem mục 5) | — |

Tổng thời lượng 13 video: 10 065 giây = 167,8 phút. `.srt` khớp `say` từng từ ở cả 13 bài (so chuỗi từ, độ khớp 1,0000, 0 chỗ lệch).

## 1. Đọc K/K

13/13 bài, 13/13 mục giáo án, 13/13 `.srt`, 13/13 `chapters.txt`.

| Bài | sha16 YAML lúc đọc (kiểm lại cuối phiên: không đổi) |
|---|---|
| L00 | a6ee88f30e4bb409 |
| L01 | d0cbd68f2e4cd476 |
| L02 | ebacc56670e1deb0 |
| L03 | e859000b03ab3982 |
| L04 | 1fa4c7fc329ef902 |
| L05 | 0aa0b71c4069c645 |
| L06 | 2e2d68bad7466e2a |
| L07 | f563131ce341da9f |
| L08 | 0e5f2670bea98434 |
| L09 | b0de6894ea1e9955 |
| L10 | 937823d27bfe3db8 |
| L11 | 0eec35f38ca616b0 |
| L12 | 418458d962b4c37c |

## 2. Bảng chuẩn xác (chỉ lỗi có bằng chứng)

Không có MUST. Mọi chương trình trên màn hình, mọi khối "Kết quả chạy" và mọi thông báo lỗi biên dịch đều chạy thật bằng JDK 21 và khớp (xem mục 6). Các SHOULD dưới đây đều là chi tiết nhỏ: màn hình thiếu dòng mã so với đầu ra, nhãn lệch, thiếu điều kiện.

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L00 | SHOULD | prereq, tiêu đề; `chapters.txt` dòng 2 | "Trước hết: ba điều về máy tính" | Bảng liệt kê ①–④ (bốn mục), lời đọc: "ta cần hiểu bốn điều về máy tính"; tiêu đề và mục lục nói "ba". Lệch nhãn, không lệch kiến thức. | Sửa tiêu đề thành "bốn điều" | CONFIRMED |
| L02 | SHOULD | sym step 0–1; quiz step 0; intuition step 3 | `soNguoi != 0 && tong / soNguoi > 50000`, `a > 10 && a % 2 == 0` | Bài chỉ dạy thứ tự "nhân, chia, dư làm trước cộng trừ". Việc `%` và `/` trước `==`, `>`, và so sánh trước `&&` được dùng ở 3 chỗ nhưng không giảng ở đâu (FND cũng không). Người học phải đoán. | Thêm một dòng bảng thứ tự: số học, rồi so sánh, rồi `&&`, rồi `||` | CONFIRMED |
| L04 | SHOULD | nhap step 0 → 1 | step 0: vòng lặp `tong += Long.parseLong(args[i])`; step 1 in `3 lenh, tong 20000000` | Mã hiện không có dòng in `args.length + " lenh, tong " + tong`; không suy ra đầu ra từ mã. Tôi phải tự thêm dòng in mới chạy ra đúng. | Hiện đủ `System.out.println(...)` | CONFIRMED |
| L05 | SHOULD | example step 0–5 | "Tong: 9700000 / Lon nhat: 4000000 o chi so 2" | Hai lệnh in tạo đầu ra này không hề hiện ở step 0–4; tương tự `KiemMang` dùng `tong` không khai. | Hiện hai lệnh in ở step 1 | CONFIRMED |
| L06 | SHOULD | sym step 0; example step 0; formula | "Tệp Phi.java: hàm tính phí" (chỉ `static long tinhPhi(...) {...}` rồi ba lệnh `System.out.println(tinhPhi(...))`) | Toàn bài không có lần nào hiện một tệp đủ `public class … { hàm; main }`; người học mất gốc không biết hàm tĩnh đặt trong lớp, ngoài `main`. Gõ nguyên màn hình sẽ lỗi biên dịch. (`de.md` có nói "đặt trong lớp RutATM", video thì không.) | Hiện một tệp trọn vẹn một lần ở sym step 0 | CONFIRMED |
| L08 | SHOULD | tep step 0–1; quymo step 0; pitfalls step 1–2; `labs/JVA/L08/de.md` | `Path tep = Path.of(...)`, `Files.writeString(...)`; de.md: "như bài mẫu `DocTep`" | (a) `import java.nio.file.*;` không hiện (chỉ có chú thích `Locale`); (b) `de.md` nhắc "bài mẫu `DocTep`" mà trong video không có chương trình nào tên đó; (c) `Files.size` (quymo), `timTen(...)`, `s`, `n`, `daChep` dùng mà không khai. | Hiện dòng import; sửa `de.md` | CONFIRMED |
| L09 | SHOULD | sym step 1; quymo step 2 | `import java.util.ArrayList;` (bảng) / "khi hàm băm phân tán tốt" | (a) bảng chỉ có import `ArrayList`, không có `HashMap` (de.md có); (b) "hàm băm" xuất hiện trên màn hình mà không giảng; (c) thí nghiệm đếm bước chỉ chạy cho danh sách, cột "bản đồ: khoảng 1" là trích Javadoc, không đo. | Thêm import; bỏ "hàm băm" hoặc giải thích; thêm một lần đo bản đồ | CONFIRMED |
| L10 | SHOULD | luong step 1; example step 0; quymo step 0 | `a.join(); b.join();` ở hàm chính | Không hiện `throws InterruptedException` (chỉ nói trong lời đọc); gõ y màn hình sẽ lỗi biên dịch "unreported exception InterruptedException". `chia(...)`, `rut(...)` dùng nhưng không hiện định nghĩa. | Hiện `throws` và hai hàm | CONFIRMED (đã tự biên dịch bản không có `throws`: lỗi) |
| L11 | SHOULD | giáo án mục tiêu 2; sym step 1; pitfalls | "Dùng kế thừa và chú thích ghi đè đúng cách" | Kế thừa chỉ có một dòng bảng (`class TaiKhoanVip extends TaiKhoan`) và một ví dụ lỗi gõ sai tên. Không có ví dụ chạy được nào dùng trường/hàm tạo của lớp cha, không `super`, và lab không có `extends` nào. Mục tiêu hứa nhiều hơn bài dạy. | Thêm một ví dụ lớp con ghi đè đúng, chạy được; thêm một dòng lab | CONFIRMED |
| L12 | SHOULD | pitfalls step 0, 5 | `at SoCai.kiem(SoLoi.java:51)` / `(CuoiNgay.java:50)` | Dấu vết trỏ vào hai tệp không hiện trên màn hình. Áp đúng chỗ sửa vào `So.java` hiển thị (đổi `b` thành `a` ở dòng cộng bên nhận) cho dấu vết `So.java:50 / 45 / 67`, còn kiểu "đối soát cuối ngày" cho `So.java:49 / 76`. Người học gõ lại sẽ thấy số khác và có thể tưởng gõ sai. Nội dung (loại lỗi, số 3 500 000 / 4 900 000) khớp. | Dùng đúng số dòng của `So.java` hoặc ghi chú "tệp khác" | CONFIRMED (đã dựng lại bằng `So.java` từ 7 phần trên màn hình) |
| L12 | SHOULD | formula step 3; pitfalls | lệnh `chuyen` | Thiếu điều kiện áp dụng: lệnh chuyển tự mình (`tu == den`) qua được mọi phép kiểm tra trước, rồi `put(tu, a − t)`, `put(den, b + t)` làm tiền tự sinh. Tôi chạy `Lenh("A","A",100000)`: `IllegalStateException: Lech tong 3100000 != 3000000` (tổng tăng) và sổ đã bị sửa, không hoàn tác. Bài khẳng định "kiểm tra trước, sửa sau" đủ giữ luật mà không nêu hai điều này. | Thêm điều kiện `tu.equals(den)` và nêu "kiem() ném sau khi đã sửa, cần hoàn tác" | CONFIRMED (chạy thật) |
| L12 | SHOULD (hiển thị) | tep, phần 3 và 4; khung 58–60 | `long tong() {`, `void chuyen(Lenh l) …` | Hai phần nằm trong lớp `SoCai` nhưng thụt lề 0, trong khi phần 2 và phần 5 thụt đúng. Bài mục tiêu "gõ lại được": Java không phạt nhưng người học thấy mã lệch. | Thụt lề 4 | CONFIRMED (khung hình) |

Lưu ý không tính là lỗi: thông báo lỗi trên màn hình L00 (`class Chao is public, should be declared in a file named Chao.java`), L05, L06, L08, L09, L11 rút gọn tiền tố tên tệp hoặc bỏ các dòng `at …`; nội dung còn lại khớp trình biên dịch/máy ảo thật. `jshell` L01 bỏ tiền tố `$7 ==>` ở dòng `0.1 + 0.2` (thật: `$7 ==> 0.30000000000000004`).

## 3. Bảng độ sâu (P1…P7: 0/1/2; P8, P9 không tính vào tổng)

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước (bài dùng mà không giảng tại chỗ) | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | a6ee88f30e4bb409 | 15:24 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | cài JDK, PATH, lưu tệp đúng tên/đuôi (FND L00/L04/L05); `int` (L01 giảng) | `int soNguoi = 0` ở pitfalls 3 chưa giải thích kiểu |
| L01 | d0cbd68f2e4cd476 | 13:52 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `import`, `new`, `Integer.MAX_VALUE`/`.add` (dấu chấm gọi hàm) ở BigDecimal và hằng có sẵn | pitfalls step 3 dùng BigDecimal "chỉ cần biết tồn tại" |
| L02 | ebacc56670e1deb0 | 13:05 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | thứ tự ưu tiên của so sánh/`&&` so với số học | không có bảng thứ tự ưu tiên toàn bộ |
| L03 | e859000b03ab3982 | 13:02 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `long phi;` khai chưa gán (gán chắc chắn); `Scanner` chỉ lướt | — |
| L04 | 1fa4c7fc329ef902 | 13:23 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | — (dòng in thiếu ở `TongArgs`, xem SHOULD) | — |
| L05 | 0aa0b71c4069c645 | 10:57 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | — | — |
| L06 | 2e2d68bad7466e2a | 11:17 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | vị trí hàm trong lớp (cạnh `main`) | không hiện tệp đủ lớp + hàm + `main` |
| L07 | f563131ce341da9f | 11:10 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | — | — |
| L08 | 0e5f2670bea98434 | 12:15 | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ | `import java.nio.file.*`, mẫu `split` (regex, chỉ nhắc "mẫu đặc biệt"), KB/MB/GB | import và nhiều dòng phụ (`Files.size`, `timTen`) không hiện |
| L09 | b0de6894ea1e9955 | 12:55 | 1 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 12 | ĐỦ | `import java.util.HashMap`, "hàm băm" | không có cơ chế vì sao tra bản đồ ~1 bước; HashMap không giữ thứ tự thêm |
| L10 | 937823d27bfe3db8 | 13:19 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `System.exit`, `BufferedReader/StringReader/IOException`, `throws InterruptedException` | `chia`, `rut` không hiện định nghĩa |
| L11 | 0eec35f38ca616b0 | 12:25 | 2 | 2 | 2 | 2 | 2 | 1 | 1 | 2 | 2 | 12 | ĐỦ | tên khung Spring/JUnit (bài nói "không dạy chi tiết") | kế thừa (`extends`, `super`, hàm tạo lớp cha) gần như không có ví dụ |
| L12 | 418458d962b4c37c | 14:41 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 13 | ĐỦ | "nano giây", "chỉ mục", "giao dịch cơ sở dữ liệu" (nêu cho khoá sau) | tự chuyển (`tu == den`), không hoàn tác khi `kiem()` ném |

Giải thích điểm P1 = 1: số từ chưa giảng tại chỗ nằm trong cột "Cần biết trước" (1–2 từ mỗi bài). Chúng nằm ở đoạn "chỉ cần biết nó tồn tại" hoặc được giảng đúng hai bài sau (`import`, `new`), nên không ai kẹt hẳn; nhưng theo thang chấm thì không được 2.

P8 (13/13 = 2): mỗi bài có lab với `de.md`, `mong_doi.txt`, `loi_giai.java`, lệnh chấm `cham.sh`; thêm việc tự làm ngay trong bài (jshell ở L01, L02; đổi tham số `args` ở L03, L04; làm hỏng có chủ đích ở L00 bước 4; "Thử thêm: bỏ khối catch" ở L10).
P9 (13/13 = 2): mỗi bài có bảng ≥ 2 mức quy mô hoặc mốc thời gian kèm đánh đổi: L00 (10/1 000/1 000 000 lệnh), L01 (100/2 147/2 148/10 000 lệnh), L02 (1/1 000/10⁶/365 ngày), L03 (3/10/100 bậc; 3/10/20 điều kiện), L04 (12/120/360 tháng), L05 (5/5 000/5 000 000), L06 (1/10/100 chỗ chép), L07 (1 000/100 000/10⁶ dòng), L08 (10³/10⁶/10⁸ dòng), L09 (10³ so với 10⁶ tài khoản, danh sách so với bản đồ), L10 (10³/10⁵/10⁶ lệnh), L11 (3/10/50 loại phí), L12 (3/10³/10⁴/10⁶ tài khoản).

## 4. Lab

Cách làm: đọc `de.md`, tự viết tệp trong thư mục tạm, chạy `bash labs/cham.sh JVA Lxx <tệp>`, rồi mới so với `loi_giai.java`. Thời gian ghi cho người mất gốc là ước lượng (tôi làm trong ~1–2 phút mỗi bài vì đã biết Java). "mong_doi khớp" = đầu ra thật của lời giải so với khối "Kết quả mong đợi" trên màn hình video và với `mong_doi.txt`.

| Bài | Tự làm được | Thời gian (người mất gốc, ước) | Kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L00 | có | 10–15 phút | không (cần JDK + PATH từ FND) | khớp 5/5 dòng |
| L01 | có | 15–20 | không | khớp 5/5 |
| L02 | có | 15–20 | de.md cho sẵn công thức `soTien * 3 / 1000` và phép kiểm; tự nghĩ ra thì cần thứ tự `&&` (SHOULD L02) | khớp 5/5 |
| L03 | có | 20–25 | `cham.sh` chỉ chấm lần chạy không đối số; hai số ở biên phải tự đối chiếu bằng mắt (de.md có kết quả) | khớp 1/1 (và 2 dòng ở biên khớp de.md) |
| L04 | có | 20–25 | không | khớp 7/7 |
| L05 | có | 20–25 | không | khớp 5/5 |
| L06 | có | 20–25 | video không chỉ hàm đặt ở đâu trong lớp (de.md có nói) | khớp 4/4 |
| L07 | có | 25–30 | không | khớp 4/4 |
| L08 | có | 30–35 | thiếu `import java.nio.file.Files/Path`: phải đọc lỗi `cannot find symbol` rồi tự thêm; de.md nhắc "bài mẫu `DocTep`" không có | khớp 7/7 |
| L09 | có | 25–30 | không (de.md nhắc cả hai import) | khớp 5/5 |
| L10 | có | 25–30 | không | khớp 4/4 |
| L11 | có | 30–35 | de.md cho sẵn mọi số (20 000 000, 100 000 000); lab không chạm `extends` | khớp 4/4 |
| L12 | có (phần lớn là gõ lại `So.java` đã hiện trọn ở scene "tep" rồi đổi tên/số; de.md cho sẵn từng thông báo) | 60–90 | không kẹt; nhưng dựng "từ không" thì cần xem lại scene "tep" | khớp 7/7 |

Cả 13 lab đều chấm "ĐÚNG" ngay lần chạy đầu. `loi_giai.java` giống bản tự viết ở L00 (diff rỗng); các bài còn lại khác về văn phong nhưng cho đầu ra giống.

## 5. Người học kẹt ở đâu

Giả định: đã học FND; chỉ xem video JVA từ L00 đến bài đang xét.

| Bài | Chỗ đầu tiên không theo được |
|---|---|
| L00 | không kẹt nếu FND đã cài JDK; chỉ có rủi ro formula step 0 "javac -version" gặp `command not found` mà video không nói cách xử lý (PATH ở FND L04). |
| L01 | không kẹt; pitfalls step 3 `new BigDecimal("0.1")`, `a.add(b)`, "cần dòng import" là phần nói thẳng "chỉ cần biết nó tồn tại". |
| L02 | intuition step 3 / quiz step 0: `soNguoi != 0 && tong / soNguoi > 50000` — thứ tự `/`, `>`, `&&` chưa giảng; đoán theo trực giác vẫn ra đúng. |
| L03 | không kẹt; nhap step 2 `new Scanner(System.in)` chỉ nói "tạo mới công cụ đọc", chép nguyên. |
| L04 | nhap step 1: đầu ra "3 lenh, tong 20000000" không suy ra được từ mã ở step 0 (thiếu dòng in). |
| L05 | không kẹt; example step 5 in "Tong: …", "Lon nhat: …" dùng lệnh in không hiện trên màn hình. |
| L06 | sym step 0 ("Tệp Phi.java: hàm tính phí"): hàm và lời gọi không có lớp/`main` bao quanh; người học không biết đặt vào đâu. |
| L07 | không kẹt. |
| L08 | tep step 0: `Path tep = Path.of("doi_soat.txt"); Files.writeString(…)` — chưa có dòng import, javac báo `cannot find symbol`. |
| L09 | sym step 1: bảng chỉ có `import java.util.ArrayList;`, lúc viết `HashMap` sẽ báo thiếu; sau đó vẫn tự sửa được nhờ gợi ý "gói java.util". |
| L10 | luong step 1: `a.join(); b.join();` ở hàm chính không có `throws InterruptedException` trên màn hình (chỉ đọc miệng) → lỗi biên dịch. |
| L11 | không kẹt khi làm lab; sym step 1 "class TaiKhoanVip extends TaiKhoan" mô tả một dòng, không dạy thêm. |
| L12 | không kẹt; pitfalls step 0 dấu vết `SoLoi.java:51` khác số dòng khi tự gài lỗi vào `So.java`. |

## 6. Số đã tính lại / mã đã chạy

- Chương trình hoàn chỉnh tự dựng từ màn hình, biên dịch và chạy bằng JDK 21.0.13: khoảng 60 tệp nguồn (phần lớn gom nhiều đoạn mỗi tệp) + 13 lab; `jshell` 15 dòng (L01 8 dòng, L02 5 dòng, hai dòng kiểm định dạng ở L08).
- Khối đầu ra trên màn hình đối chiếu với kết quả chạy thật: 132 (114 khối "Kết quả chạy"/"Chạy lại" + 18 khối "Trình biên dịch báo"). 130/132 khớp nguyên văn hoặc chỉ khác phần rút gọn rõ ràng (tiền tố tên tệp, bỏ dòng `at …`, `$n ==>`). 2/132 (L12, hai dấu vết ngăn xếp dòng 51/46/69 và 50/78) chỉ tái tạo được loại lỗi, số, thông báo; số dòng khác vì hai tệp `SoLoi.java` và `CuoiNgay.java` không có trên màn hình.
- Số trên màn hình tính lại bằng Python (độc lập với `checks` của YAML): 30/30 nhóm số khớp (bảng quy mô L00, L01, L02, L03, L04, L05, L06, L07, L08, L10, L11, L12; lãi 12/120/360 tháng; 6 tháng của lab L04; thời gian 10 ns × N × M ở L12; xác suất 0,98ⁿ ở L06).
- Mã nguồn lỗi cố ý ở phần "Lỗi hay gặp": đã gõ lại các lỗi trong L00, L01, L03, L05, L06, L07, L09, L10, L11, L12 và nhận đúng thông báo/hậu quả như bài nói (kể cả `ConcurrentModificationException` ở L09, tràn `int` 1410065408 ở L01, tổng 3 500 000 và 4 900 000 ở L12).
- Điều bài khẳng định bằng chữ mà tôi kiểm lại bằng chạy thật: `Integer` 127 so bằng `==` true, 128 false (L09); `HashMap`/`String.format("%,d")` theo vùng `vi-VN` ra `1.234.567`, vùng `US` ra `1,234,567` (L08); `@FunctionalInterface` trên giao diện hai hàm bị chặn đúng thông báo (L11); `finally` chạy sau `catch` đúng thứ tự (L10).

## 7. Khung hình đã xem (≥ 5 mỗi bài; tên tệp ở `out/JVA/Lxx/frames/`)

Mỗi bài xem 6 khung (mở đầu, bảng giải mã/mã chính, hình cơ chế, ví dụ từng phép, bảng quy mô hoặc mã quy mô, kết quả mong đợi của lab). Số hiệu là `NNNNN.png`:

| Bài | Khung đã xem |
|---|---|
| L00 | 00001, 00013, 00034, 00067, 00091, 00148 (+ 00116, 00151) |
| L01 | 00001, 00012, 00027, 00050, 00081, 00123 (+ 00106, 00126) |
| L02 | 00001, 00011, 00026, 00053, 00078, 00121 (+ 00103, 00124) |
| L03 | 00001, 00014, 00029, 00049, 00087, 00132 (+ 00051, 00054) |
| L04 | 00001, 00012, 00023, 00050, 00082, 00126 |
| L05 | 00001, 00010, 00019, 00040, 00057, 00094 |
| L06 | 00001, 00010, 00018, 00043, 00061, 00099 |
| L07 | 00001, 00011, 00020, 00042, 00058, 00095 |
| L08 | 00001, 00009, 00016, 00042, 00067, 00106 |
| L09 | 00001, 00012, 00026, 00049, 00072, 00113 |
| L10 | 00001, 00013, 00021, 00052, 00082, 00121 |
| L11 | 00001, 00010, 00017, 00042, 00069, 00107 (+ 00062, 00064) |
| L12 | 00001, 00017, 00022, 00046, 00058, 00060, 00070, 00090, 00098, 00125 |

(Khung xem dưới dạng ghép hai ảnh 1000×562; chữ mã khoảng 13–15 px ở khung gốc 1920×1080 vẫn đọc được.)

Lỗi hiển thị: không thấy chữ tràn, đè, hay bị cắt ở bất kỳ khung nào; công thức (`$$…$$`) hiển thị đúng kể cả dấu `<` trong L03 ("499 999 < 500 000") và L11 ("500 < 1000 ⇒ 1000"); hình khớp lời đọc. Ghi nhận:
- Mọi khung dùng khoảng nửa trên màn hình, nửa dưới trống (phụ đề ở đáy), nên mã dài như L05 quymo và L10 quymo sát phụ đề nhưng còn vừa.
- L12 "tep" phần 3, 4: thụt lề lệch (đã nêu ở SHOULD).
- L10 quymo (khung 00082): khối mã thụt lề dư 8 ô và đóng ngoặc không khớp, do trích từ giữa `main`; không ảnh hưởng đọc.
- Khối mã ở L06 quymo/L10 quymo là đoạn cắt, không có `class`/`main` bao.

## 8. Nhận xét chung

- Chất lượng nội dung rất đều: 13 bài đều có giải mã ký hiệu, hình cơ chế, ví dụ làm tay từng phép, đường kiểm khác, bảng quy mô, lỗi hay gặp "người mới / người đi làm", quiz có dừng + lời giải từng bước, lab có `mong_doi`. Không phát hiện kiến thức sai; mọi chương trình và mọi con số khớp khi chạy thật.
- Điểm yếu lớn nhất so với ngưỡng P1: nhiều mã trên màn hình là đoạn cắt (thiếu `import`, thiếu `class`/`main`, thiếu dòng in, thiếu `throws`). Người học gõ y màn hình sẽ gặp lỗi biên dịch ở L06, L08, L09, L10 và phải tự vá; nên hiện thêm đúng các dòng này. Sửa 5–6 chỗ là đưa P1 lên ≥ 90%.
- Kế thừa (L11) là chỗ giáo án hứa nhiều hơn bài dạy: không ví dụ chạy được, lab không có `extends`; khoá JV2 nếu tiếp nối có thể cần dạy lại.
- Chỗ chuyên sâu còn mỏng: cơ chế bản đồ (vì sao ~1 bước), tự chuyển `tu == den` và hoàn tác khi kiểm bất biến vỡ (L12), thứ tự ưu tiên toán tử (L02).
- Thang lab và "Kết quả mong đợi" khớp tuyệt đối; `cham.sh` chạy được cho 13/13 bài trên Git Bash Windows với JDK 21 (không cần sửa).
- `.srt` là chính văn bản `say` (không phải ASR thật); các câu `asr_reviewed` trong YAML ghi rõ "NOT_VERIFIED bằng tai người": chưa kiểm tai người, chỉ kiểm văn bản.
- Tổng thời lượng 168 phút cho 13 bài là hợp lý với lượng kiến thức; lab chiếm thêm khoảng 5–6 giờ cho người mất gốc (L12 nặng nhất).
- Không có đoạn nào phụ thuộc khoá khác ngoài FND; các lời nhắc "bài trước/bài đầu" đều trỏ vào bài JVA đứng trước.
