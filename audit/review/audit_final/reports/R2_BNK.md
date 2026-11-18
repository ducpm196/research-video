# R2 BNK (vòng 2, trên bản đã sửa và dựng lại): đã đọc 15/15 bài (L00–L14), 2026-11-15

Cách làm: 4 người đọc độc lập (L00–03, L04–07, L08–11, L12–14), mỗi người đọc trọn YAML + curriculum/bnk.yaml, xem >= 5 khung hình/bài, so SRT với `say`, tự viết lab rồi chấm bằng labs/cham.sh, chạy lại số/mã. Không sửa kho, không mở báo cáo cũ. Người điều phối đã tính sha16 và spec_digest (lv.spec_digest, bỏ asr_reviewed) cho cả 15 bài.

## 0. Tóm tắt chốt

| Chỉ tiêu | Ngưỡng | Kết quả | Đạt? |
|---|---|---|---|
| MUST | 0 | 1 (L10 chay_that step 5, ở ranh giới MUST/SHOULD, xem dưới) | KHÔNG (nếu tính ranh giới là MUST) |
| SHOULD | — | 20 (L00-03: 7, L04-07: 3, L08-11: 5, L12-14: 5) | — |
| P1 = 2 | >= 90% bài | 0/15 (0%): L00=0, L11=0, L13=0, còn lại 12 bài = 1 | KHÔNG |
| P8 = 2 | 100% bài | 15/15 (100%) | ĐẠT |
| P9 = 2 | — | 15/15 | — |
| Spec khớp video | — | 15/15 SPEC_MATCH (spec_sha256 trong build_report.json == lv.spec_digest hiện tại) | ĐẠT |
| SRT == say | — | 15/15 bài, 0 câu lệch (mỗi bài so từng câu: 148/144/138/141 ..., 131-146 câu/bài); lưu ý SRT sinh từ `say` nên chỉ chứng minh không rơi câu, chưa kiểm âm thanh | ĐẠT |
| Số/mã tính lại | — | khoảng 340 số/kết quả (105 + 71 + 115 + 49) đều khớp màn hình; hai lệch lời-màn hình/chữ-mã nêu ở L10 và L11; khoảng 49 chương trình/đoạn mã đã chạy (14 + 7 + 14 + vài lab D) | — |
| Lab | — | cham.sh chấm ĐÚNG lời giải kho 15/15 và lời giải tự viết 15/15; mong_doi khớp màn hình 15/15; tự làm được trọn (có): 6 bài (L02, L04, L05, L08, L09, L14); "phần": 9 bài (L00, L01, L03, L06, L07, L10, L11, L12, L13); "không": 0 | — |

Lưu ý về P1: người đọc B áp quy ước "mục chưa giảng chỉ là mã chạy-xem hoặc công cụ thì P1=1, thiếu khái niệm then chốt thì 0"; người đọc C tính cả từ chỉ nhắc ở hook rồi mới giảng ở cảnh sau (Outbox L08; hàng đợi, mã tương quan L10). Nếu miễn các từ đó thì L08, L10 lên 2, nhưng vẫn chỉ 2/15 = 13%, xa ngưỡng 90%. Nguyên nhân gốc chung: BNK là khoá Java/SQL/Python dành cho người "mất gốc" nhưng không có bài dạy khung tệp (class/main/for/try/catch/lambda/def/import), cách mở cửa sổ lệnh/cài JDK; mỗi bài dùng cú pháp mà không giảng.

### MUST / SHOULD chính (file:cảnh)

MUST (ranh giới):
- L10_t24_ofs_ibm_mq_tuong_quan.yaml : chay_that step 5, say "Hỏi trạng thái trước thì trong mô hình này cả bốn trường hợp đều đúng một lần." Màn hình ngay trước (phần 2: bốn tình huống, dòng đầu "da hach toan, gui lai ngay: 2") cho 2,1,1,1; người học thấy bốn dòng, một dòng bằng 2, nghe nói "đều đúng một lần". Người điều phối đã đối chiếu YAML: khớp. Cách đọc khoan dung "hỏi trước thì cả bốn tình huống (nếu áp chính sách hỏi trước) đều một lần" tồn tại nhưng mâu thuẫn với bảng 4 dòng trên màn hình, nên giữ MUST. Sửa: "cả hai trường hợp hỏi trước đều đúng một lần".

SHOULD chính:
- L11 formula step 3 và chay_that step 3: chữ/lời nói "duyệt từ trường 2" nhưng mã dùng `range(1, 65)` (gồm bit 1). Sửa `range(2, 65)`.
- L12 hook step 2 (khung 00008): say "kết quả mô phỏng ở cuối bài" nhưng bảng hiện ở phút 06:10, còn 9 phút; L12 formula step 3 "việc sửa sổ luôn qua bước duyệt" (tuyệt đối).
- L13 formula step 1 mã hoá khối PIN định dạng 0 "bằng TDES hay AES" (ISO 9564-1 Amd 1:2015 đòi định dạng 4 khi dùng AES; PLAUSIBLE); formula step 3 chưa có nguồn trong registry (PLAUSIBLE); intuition SVG1 (khung 00033) chữ "(ngân hàng thanh toán, chuyển mạch)" tràn ô, đè mũi tên (CONFIRMED); ngưỡng 10/20 triệu tự ghi CHƯA KIỂM.
- L14 mục tiêu 4 (kể sự cố thật theo STAR): chỉ có khung trống, không có ví dụ mẫu; quiz câu 3 không đáp án mẫu.
- L08 hook step 2: bảng hứa "thấy ở phần chạy thật" hai dòng "tiền mất dấu", "ghi nợ được hoàn lại" nhưng chạy thật không cho thấy; L08 chay_that step 1: Saga.java "phần chính" thiếu `}` đóng vòng for và khung class/main, chép nguyên văn không biên dịch (khung 00052).
- L09 check: cảnh dùng `entry(txn, amt)`, cảnh chạy thật và lab dùng `but_toan(gd, tien)`.
- L11 pitfalls: "tối đa 6 số đầu" theo PCI DSS thiếu điều kiện BIN 8 số cho thẻ >= 16 số (PLAUSIBLE).
- L04 quy_mo: "Byte: đơn vị lưu một ký tự / mười sáu byte, tức mười sáu ký tự" sai với chữ có dấu UTF-8 (CONFIRMED); chay_that: "Máy in thêm ba cột số" chỉ đúng với sqlrun.py, sqlite3 CLI in dạng cây (PLAUSIBLE).
- L05 quy_mo: nhãn "cặp ngược thứ tự kỳ vọng" nhưng lời "bế tắc xảy ra vài chục lần" (ngược thứ tự chỉ là điều kiện cần; PLAUSIBLE).
- L00 prereq step 4 định nghĩa MB = 1 048 576 byte nhưng RoRi.java chia 1_000_000; chú thích G1 thiếu vế >= 2 GB RAM (PLAUSIBLE); quiz câu 2 thiếu số đối tượng rác ở đề.
- L01 CoKhoa.java đặt `sleep` trong `synchronized` ngay trước cảnh Lỗi 2 không nói là giả lập; cơ số 1024 (L00) vs ~1000 (L01/L03).
- L02 hook gộp hai nhãn giao dịch khác nhau; L03 "bảng khoá 64 byte mỗi khoá" chỉ tính khoá, bỏ phần phản hồi.

### Bảng tổng hợp một dòng mỗi bài (P1..P7 | P8 | P9 | Tổng | Mất gốc)

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng | Mất gốc | Spec |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 4771fdfbe14af7e0 | 14.8 | 0 | 2 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 10 | GẦN (có mục 0) | khớp |
| L01 | c1317fea87b99aee | 15.3 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | khớp |
| L02 | 75929da343f77d0e | 14.8 | 1 | 2 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 11 | GẦN | khớp |
| L03 | 6df7bdce8fb33424 | 14.6 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 12 | ĐỦ | khớp |
| L04 | fe6af285924852a1 | 14.3 | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 10 | GẦN | khớp |
| L05 | 31d8962949cbe789 | 15.3 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 12 | ĐỦ | khớp |
| L06 | 94ebbf6255890705 | 15.3 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ | khớp |
| L07 | 6c2101ac92336180 | 15.1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | khớp |
| L08 | 529eebd880d911ba | 15.0 | 1 | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 11 | GẦN | khớp |
| L09 | bc40ae378b945413 | 14.4 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | khớp |
| L10 | fbc24c50afb1ca08 | 15.5 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ | khớp |
| L11 | 4966948d62115414 | 15.6 | 0 | 1 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 10 | GẦN (có mục 0) | khớp |
| L12 | ef115d71d7b8e015 | 15.2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | khớp |
| L13 | 04f28429d76daa40 | 15.5 | 0 | 2 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 10 | GẦN (có mục 0) | khớp |
| L14 | efb970d81af090ba | 15.6 | 1 | 2 | 2 | 2 | 1 | 2 | 1 | 2 | 2 | 11 | GẦN | khớp |

Thống kê: ĐỦ 7/15, GẦN 8/15, CHƯA 0/15. Mô tả chi tiết từng ô ở các phần dưới.

### Nhận xét chung
- Kiến thức chuẩn: không có sai kiến thức nặng; lỗi duy nhất ở mức MUST là một câu nói lệch màn hình (L10).
- Lỗ hổng lớn nhất là nền cú pháp cho người mất gốc (Java class/main/for/try-catch/lambda; Python def/import/comprehension; SQL SELECT/WHERE; mở cửa sổ lệnh, cài JDK): 0/15 bài đạt P1=2. Đây là lý do chính chưa chốt "bắt đầu học".
- Thực nghiệm (P8) và quy mô (P9) đạt trọn 15/15; mọi lab chấm ĐÚNG, mong_doi khớp màn hình.
- Lab nhiều bài chưa luyện đúng kỹ năng cốt lõi của bài (L04 không có EXPLAIN, L05 không có khoá, L06 không có mã chặn, L07 không có thứ tự ghi nhớ, L13 chỉ hàm luhn trong khi mục tiêu là hàm che số thẻ).
- L11 (đầu tiên dùng Python, đọc ngược mã bằng list comprehension) và L13 (def/return/import/join/ljust/XOR dùng trước khi giảng) là hai bài yếu nhất về nền.
- Hiển thị: chỉ lỗi nhẹ (L13 khung 00033 chữ tràn; L06 00034/00046/00064; L08 00028/00052; L10 00027; L01 00069; L03 00014/00035).
- Ngoại lệ lưu ý: tất cả SRT sinh từ `say` nên chưa kiểm được âm thanh thực bằng tai người; PL/SQL L05 và T24/Oracle chỉ đọc, không chạy (không có Oracle).

---
# Chi tiết từng phần (nguyên văn báo cáo của người đọc, lưu ở scratchpad)


## ===== PART A =====
# PART A: đã đọc 4/4 bài (BNK L00, L01, L02, L03)

sha16 tính lại lúc đọc: L00 4771fdfbe14af7e0, L01 c1317fea87b99aee, L02 75929da343f77d0e, L03 6df7bdce8fb33424 (khớp danh sách giao). Tệp tạm: `...\scratchpad\r2bnk\agA\` (L00..L03, frameat.py, srtcmp.py). Không sửa/tạo gì trong D:\research-video.

## A. Chuẩn xác
MUST: 0. SHOULD: 7 (đều nhẹ, không làm sai kết luận bài).

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L00 | SHOULD | prereq step 4 vs chay_that step 3 | prereq: "$1\,\text{MB} = 1024 \cdot 1024 = 1\,048\,576$ byte"; chay_that (RoRi.java): "(rt.totalMemory() - rt.freeMemory()) / 1_000_000;   // MB đang dùng (1 MB = 10^6 byte)" | Cùng một bài định nghĩa MB hai cách (1 048 576 rồi 10^6). Người học mất gốc vừa được dạy MB=1024², rồi thấy mã chia 10^6 và so `>= 5`. Python: 5 mảng × 1 000 000 B = 5 000 000 B = 4,77 MiB < 5 (theo định nghĩa của chính bài), nhưng mã vẫn in `true` (đã chạy java: true/false khớp màn hình) vì cộng thêm heap nền. Bài không nói vì sao đổi cơ số. | Một câu ở chay_that: "ở mã này ta dùng 1 MB = 1 triệu byte cho dễ" hoặc đổi mã sang 1_048_576. | CONFIRMED |
| L00 | SHOULD | chay_that step 4 (note) + say | "Đúng với bộ dọn mặc định (G1) trên máy nhiều bộ xử lý; máy chỉ một bộ xử lý có thể ra khác." / say: "chọn khi máy có nhiều bộ xử lý" | Điều kiện chọn G1 mặc định thiếu một vế: HotSpot GC Tuning Guide định nghĩa máy "server-class" là ≥ 2 bộ xử lý VÀ ≥ 2 GB RAM vật lý; thiếu RAM cũng rơi về Serial GC. (Chưa kiểm được nguồn trực tuyến trong phiên này, dựa vào hiểu biết về tài liệu JDK; đã chạy: G1 trên máy này cho true/false đúng.) | Thêm "và đủ RAM (từ 2 GB)". | PLAUSIBLE |
| L00 | SHOULD | quiz step 1 (đề câu 2) vs step 3 (đáp án) | đề: "Mỗi đối tượng 50 byte. Dọn được bao nhiêu byte?" đáp án: "Hai đối tượng rác nhân năm mươi byte, bằng một trăm byte." | Đề câu 2 không nêu số đối tượng rác; số "hai" chỉ có từ đáp án câu 1 (4 − 2 = 2). Đề thiếu dữ kiện, người học không thể tự tính nếu không ngầm hiểu "cùng đề câu 1". 2·50=100 đúng. | Ghi "Cùng đề câu 1; mỗi đối tượng 50 byte. Dọn được bao nhiêu byte?" | CONFIRMED |
| L01 | SHOULD | chay_that step 3 (CoKhoa.java) vs pitfalls step 2 (Lỗi 2) | CoKhoa: "synchronized (KHOA) { int doc = soDu; try { Thread.sleep(cho); } ... soDu = doc + tien; }" ; Lỗi 2: "Giữ khoá khi gọi mạng. ... mọi luồng khác chờ 300 ms theo. Khoá chỉ nên bao đoạn đọc rồi ghi ngắn." | Mã mẫu đặt `Thread.sleep` (giả việc chậm) BÊN TRONG khoá, đúng kiểu sai mà cảnh pitfalls cảnh báo 1 phút sau; bài không nói câu nào rằng sleep trong khoá ở đây chỉ để mô phỏng. Người học có thể mang mẫu này đi dùng. (Chạy: CoKhoa → so du = 180, đúng; nên lời bài không sai, chỉ dễ hiểu lầm.) | Thêm lời: "sleep trong khoá chỉ để giả lập; mã thật không làm vậy". | PLAUSIBLE |
| L01 | SHOULD | prereq step 3 (⑧), quy_mo | "1 GB ≈ một tỉ byte"; "1 000 000 MB ≈ 1 TB"; so với L00: "1 GB bằng 1024 MB" | Cơ số đơn vị đổi giữa các bài: L00 dạy nhị phân (KB=1024), L01 và L03 ("64 000 MB = 64 GB", 6 400 000 B = "6,4 MB") dùng thập phân. Phép tính vẫn đúng ở mức "≈" (Python: 10^6 MB = 0,95 TiB), nhưng người học mất gốc có hai quy ước mà không được báo. | Một dòng ở L01 ⑧: "từ bài này ta làm tròn: 1 KB ≈ 1000 byte". | CONFIRMED (văn bản), tác động thấp |
| L02 | SHOULD | hook step 1 | "Lập trình viên gắn @Transactional lên hàm chuyển tiền, và nhãn giao dịch luôn mở giao dịch mới lên hàm ghi vết" | Câu gộp hai nhãn khác nhau (nhãn ngoài trên chuyenTien; nhãn chế độ REQUIRES_NEW trên ghiVet). Đọc lần đầu dễ hiểu một nhãn làm cả hai việc; bảng ở step 2 mới làm rõ ("nhãn luôn mở giao dịch mới" ở hàm ghi vết). Kiến thức đúng. | Tách: "hàm ghi vết mang nhãn riêng, chế độ luôn mở giao dịch mới". | PLAUSIBLE |
| L03 | SHOULD | quy_mo step 1 | "bảng khoá (64 byte mỗi khoá)" → "6,4 MB / 640 MB / 64 GB" | Bảng ở cảnh check/DDL lưu cả `phan_hoi TEXT` ("so du 1500000") bên cạnh khoá; con số chỉ tính 64 B của khoá nên dung lượng thấp hơn thực tế (chưa tính phản hồi, chỉ mục, chi phí dòng). Đã ghi "(số minh hoạ)" nên chỉ SHOULD. Python: 10^9 × 64 = 64 GB khớp. | Ghi "64 byte cho cả dòng (khoá + phản hồi)" hoặc nói "chỉ phần khoá". | PLAUSIBLE |

Bài không còn lỗi kiến thức khác: L00 | L01 | L02 | L03 — không phát hiện lỗi MUST (đáp án quiz, số, mã chạy, JEP 444/491, HikariCP, RFC 9110 đều khớp).

## B. Độ sâu
| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 4771fdfbe14af7e0 | 14.8 | 0 | 2 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 10 | GẦN | cài JDK 21 và chạy `javac/java`; khung `public class X { public static void main(String[] args) {…} }`; vòng lặp `for`/`i++`; chuỗi (String), nối chuỗi bằng `+`, `System.out.println`; `null`; "hàm"; "dịch vụ/yêu cầu/tải"; "bộ xử lý" | P1=0: ≥5 từ dùng mà chưa giảng: "chuỗi" (prereq step 2: "hỏi chuỗi s có cùng nội dung với chuỗi t không"), "hàm" (say intuition step 1 "mỗi lần gọi hàm"), "dịch vụ" và "yêu cầu" (hook step 2 "Một dịch vụ khác chạy tốt vài ngày"; quy_mo "mỗi yêu cầu bỏ lại một ki lô byte" — chỉ được định nghĩa ở L01 ④), "bộ xử lý" (chay_that step 4 note), khung class/main/for ở mã (RoRi.java: `for (int i = 1; i <= 5; i++)`) và ở lab. P3=1: cảnh formula (steps 1–3) và example step 5 nói "ở hình trước", "xoá mũi tên từ A sang B" nhưng màn hình chỉ có chữ (frame 00047: không có sơ đồ); đồ thị A–F chỉ xuất hiện ở intuition. P5=1: câu 2 đề thiếu dữ kiện (xem A); pause 20 s cho 3 câu; câu 2 lời giải một dòng. |
| L01 | c1317fea87b99aee | 15.3 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `throws Exception` (chỉ giảng ở L02 ④); `Runnable`; vòng lặp `for`; mili giây (đơn vị); khung class/main | P1=1: `throws Exception` trong `main` (chay_that step 1), đơn vị "mili giây/ms" dùng từ prereq ⑤ mà chưa nói 1 ms = 1/1000 giây; (Runnable, "lô" được gloss bằng ngữ cảnh). Lab chỉ cho mảnh `for (…)` có dấu chấm lửng, không cho khung. Nhỏ: mã CoKhoa có chú thích tràn mép khung (frame 00069). Lab không bảo người học thử bỏ khoá để thấy lỗi (mình thử: không khoá → tong = 311366 và 313055 thay vì 600000). |
| L02 | 75929da343f77d0e | 14.8 | 1 | 2 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 11 | GẦN | `Class<?>[]`, `getClassLoader()`, `Dich.class` (chuỗi mã tạo proxy); "hàng đợi"; chép khung từ `de.md` (không có trong video); JDK | P1=1: dòng `Proxy.newProxyInstance(Dich.class.getClassLoader(), new Class<?>[] { Dich.class }, (p, m, a) -> …)` chỉ được nói chung chung ("ba tham số") nên ClassLoader/`Class<?>[]` không hiểu; "hàng đợi" (quy_mo step 2 đánh đổi). P3=1: không có hình cho REQUIRES_NEW (hai giao dịch, một commit, một rollback) và không có hình cho cạn hộp kết nối (quy_mo chỉ bảng + chữ); hình chỉ có cho proxy và this. P5=1: câu 1–2 lời giải một câu ("số dòng = 1/0"), gần như lặp lại ví dụ B/A, không có biến thể mới. Phần chay_that step 3 chỉ hiện đuôi chương trình (frame 00075, không thấy `main`/class), clear xoá phần 2, nên người học không thấy chương trình trọn một màn hình. |
| L03 | 6df7bdce8fb33424 | 14.6 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 12 | ĐỦ | `WHERE` (SQL); Map/`HashMap` và lambda `->` (từ L00/L01); `import`, `HttpExchange`; mở hai cửa sổ lệnh và `java MayChu.java` (chế độ chạy thẳng tệp nguồn, khác `javac`+`java`); curl có sẵn trong Git Bash | P1=1: `WHERE khoa = 'abc'` (check step 2) chưa giảng (các lệnh còn lại đều có gloss trong say). P7=1: mục tiêu 5 "Chạy một máy chủ nhỏ và gọi bằng công cụ dòng lệnh" chỉ được trình chiếu, phần video "Tự làm" chỉ bảo viết XuLyTrung (phần máy chủ+curl nằm ở "Phần thêm (không chấm)" của de.md, video không nhắc); mục tiêu 3 "Thiết kế bảng khoá" nhưng video đưa sẵn DDL, không có bài tập tự thiết kế. Hình lần 2: mũi tên "tra" đi từ ô "lần 2" vào bảng khoá (hướng giống "ghi") và "lần 3" không nối với bảng (frame 00035) dù lời nói "lần hai và lần ba … thấy khoá đã có". |

Quy tắc P1 áp dụng thống nhất: coi từ đã được giảng tại chỗ hoặc ở bài đứng trước cùng khoá, hoặc được gloss rõ trong `say`/chú thích; khung `public class/main` chỉ tính ở lần đầu (L00). Hệ quả cần ghi: không bài nào trong L00–L03 dạy cài JDK hoặc khung tệp `.java`; chỉ `de.md` L02 có khung, L00/L01/L03 không có.

## C. Lab
| Bài | tự làm được (có/không/phần) | thời gian | kẹt ở đâu | mong_doi khớp màn hình | cham.sh lời giải kho |
|---|---|---|---|---|---|
| L00 | phần | 10–15 phút nếu đã có JDK; 30–40 phút nếu phải tự cài JDK và học khung `.java`/`for` | đề (de.md) chỉ nêu tên chương trình và dòng in; không có `public class PhiLech { public static void main(...) }`, không nói cài JDK 21; "Nếu kẹt" chỉ cho 2 dòng khai biến và vòng lặp; mình tự viết đúng ở lần chạy đầu (nhưng đã biết Java) | khớp: "double: 5.999999999999998 / so nguyen: 60 phan muoi / bang 6? false" trùng slide và mong_doi.txt; Python: 20 lần += 0.3 = 5.999999999999998 | ĐÚNG |
| L01 | phần | 15–25 phút (+20 nếu thiếu `for`, `Thread[]`, `throws`) | de.md nhắc `Runnable`, `synchronized`, `start()`/`join()` nhưng chỉ cho mảnh `for (…)`; không có khung; không hướng dẫn thử bỏ khoá để thấy mất cập nhật (không khoá: 311366, 313055) | khớp: "tong = 600000" (3 × 200 000) | ĐÚNG |
| L02 | có (nhờ khung đầy đủ trong de.md) | 10–15 phút | không kẹt kỹ thuật vì chỉ điền 2 TODO; điền `moGiaoDich++` đã được ghi sẵn ngay trong đề; phần suy nghĩ thật nằm ở "dự đoán ba số". Kẹt nhẹ: video bảo "chép khung trong de.md" nhưng không hiện khung | khớp: 1, 2, 3 (chuyenKhoan gọi thẳng tinhPhi/thongBao nên không tăng) | ĐÚNG |
| L03 | phần (phần chấm: có nếu biết Map; phần máy chủ: có nếu theo de.md) | XuLyTrung 10–20 phút; phần thêm máy chủ+curl 15–20 phút (mình chạy đủ: 6 dòng khớp ket_qua_curl.txt; thử x1,x2 → 1000000, 500000) | de.md không có khung; "Nếu kẹt" gần như cho đáp án một dòng (`computeIfAbsent`); video không chỉ cách mở hai cửa sổ lệnh/`java MayChu.java`; PowerShell 5.1 có alias `curl` (chưa kiểm được; PowerShell 7.6.9 trên máy này không có alias) | khớp: 4 dòng "k1 -> 2300000 / k1 -> 2300000 / k2 -> 1600000 / k1 -> 2300000"; curl 6 dòng khớp slide | ĐÚNG |

## D. Người học kẹt ở đâu
- L00: sớm nhất ở hook step 2 ("Một dịch vụ khác chạy tốt vài ngày, rồi báo hết bộ nhớ và sập") vì "dịch vụ/yêu cầu" chưa giảng; kẹt thực hành ở practice step 1 ("Viết PhiLech.java: biến double cộng 0.3 hai mươi lần…") vì khung class/main, `for`, `System.out.println`, cài JDK chưa từng được dạy.
- L01: chay_that step 1 (`public static void main(String[] args) throws Exception {`) với `throws Exception` chưa giảng; lab (practice step 3) "`for (…) { synchronized (KHOA) { tong++; } }`, `Thread[] ds = { … }`" là mảnh có dấu chấm lửng, không phải khung.
- L02: chay_that step 2 ("Proxy.newProxyInstance(Dich.class.getClassLoader(), new Class<?>[] { Dich.class }, (p, m, a) -> …"): say chỉ nói "ba tham số là chính proxy, hàm được gọi và các đối số"; phần 3 chỉ hiện đuôi chương trình nên không ráp được chương trình hoàn chỉnh trên màn hình.
- L03: khái niệm theo kịp; kẹt nhẹ ở check step 2 (`WHERE khoa = 'abc'`) và ở practice (chép khung từ đâu, không có khung trong de.md/video); "Phần thêm" máy chủ+curl không được video nhắc nên người xem video có thể bỏ qua.

## E. Số đã tính lại / mã đã chạy
- L00: 24 số/biểu thức tính lại bằng Python (1024², 4·1024³/(r·1024) ở 3 tải → 419 430 s=4,85 ngày / 4 194 s=69,9 phút / 42 s, 10 240 000 B, 600/300/300/500/2/100, 0.9999999999999999 và 5.999999999999998 (16 chữ số thập phân)): 24/24 khớp. Chạy 4 chương trình Java 21 (GiuThamChieu, RoRi, CongTien + so sánh chuỗi, PhiLech): 10/10 dòng in khớp màn hình. SRT vs say: 151 câu, 0 thiếu/0 đổi số; 6 cảnh báo của script chỉ là câu bị gộp ở dấu hai chấm (SRT 148 khối).
- L01: 31 số/biểu thức (6 cách xen kẽ: 180×2, 130×2, 150×2 bằng liệt kê mô phỏng; 90 = 6!/8 và = 3 luồng liệt kê trực tiếp; 8 s; 5 s; 2000/s; 3 hàng quy_mo: 5 s/500 s=8,3 phút/50 000 s=13,9 giờ; 10 GB/1 TB/100 TB; 10 MB/1 GB/100 GB; 600 000): 31/31 khớp. Chạy MatCapNhat (130), CoKhoa (180), LuongAo (xong 10000, 231 ms < 2 s; thêm đối chứng 200 luồng nền = 5640 ms ≈ 5 s), TongBaLuong (600000); thí nghiệm bỏ khoá: 311366. SRT vs say: 146 câu, 0 lệch (2 câu bị tách dấu hai chấm).
- L02: 20 số (6/501/50 001; 5/500/50 000; bảng đếm giao dịch 1,0,2,1,2 bằng mô phỏng riêng; 500 000−500 000=0): 20/20 khớp. Chạy ProxyGiaoDich (6 dòng in khớp slide: số giao dịch 1 rồi 2) và ChuyenKhoanProxy (1,2,3). SRT vs say: 138/138 câu khớp. Giá trị HikariCP (10, 30 s), PostgreSQL 100, "chỉ RuntimeException/Error rollback": theo nguồn đã ghi trong YAML, chưa tra trực tuyến.
- L03: 30 số (1 500 000/500 000/1 000 000; 0 và 800 000; 3 hàng quy_mo × 4 cột: 100/10 000/1 000 000 lệnh trùng, 50 triệu/5 tỉ/500 tỉ đồng, 6,4 MB/640 MB/64 GB; 4 dòng lab): 30/30 khớp. Chạy MayChu.java thật + 6 lệnh curl (khớp slide và ket_qua_curl.txt), SQL sqlite (qua cham.sh/sqlrun: "1", "so du 1500000" khớp slide), XuLyTrung (4 dòng). SRT vs say: 144 câu, 0 lệch (3 câu tách dấu hai chấm).
- Tổng bốn bài: ≈105 số/biểu thức, 105/105 khớp; 14 chương trình/đoạn mã chạy (Java 21, curl, sqlite), 14/14 cho kết quả đúng như bài nói.

## F. Khung hình đã xem
- L00 (14): 00000 (hook), 00016 (prereq ⑦–⑨ + đơn vị), 00028 (stack/heap), 00036 (đồ thị xanh/xám), 00047 (formula, kiểm chứng không có sơ đồ), 00057 (code GiuThamChieu), 00061 (kết quả), 00085 (bảng 3 cách lưu tiền), 00102 (lỗi 2), 00118 (đáp án câu 3), 00123 (bảng quy mô), 00127 (giải pháp cũ gãy), 00136 (đề tự làm), 00147 (tổng kết). Lỗi hiển thị: không có chữ tràn/đè; frame 00028 nhãn "tham chiếu" nằm đè lên biên khung heap (đọc được); hình đồ thị chỉ ở intuition, không ở formula/example (xem B).
- L01 (14): 00014 (prereq ④–⑥), 00021 (bảng 8 thuật ngữ), 00029 (xen kẽ xấu), 00034, 00037 (khoá), 00041 (200 luồng nền vs luồng ảo), 00057 (ví dụ), 00066 (kết quả 130), 00069 (CoKhoa), 00073 (LuongAo), 00086 (kiểm đường khác), 00101 (quiz), 00115 (bảng quy mô), 00129 (đề tự làm). Lỗi: frame 00069 chú thích "// mỗi lúc chỉ một luồng vào khối này" tràn ra ngoài mép khung mã khoảng 10 px (vẫn đọc được); còn lại không lỗi.
- L02 (12): 00000, 00014 (ngoại lệ), 00033 (bảng bean/IoC/proxy), 00040 (proxy ba việc), 00046 (this không qua proxy), 00057 (ví dụ trường hợp A), 00075 (phần 3 mã), 00079 (kết quả), 00106 (bảng lựa chọn quiz), 00111 (công thức hộp kết nối), 00116 (vì sao kẹt), 00124 (đề tự làm). Lỗi: frame 00075 chỉ hiện nửa dưới chương trình (không thấy `main`/phần 2 do clear), không có chữ tràn.
- L03 (11): 00000, 00014 (curl/tiêu đề/cổng), 00031 (phản hồi mất), 00035 (khoá chặn trùng), 00057 (MayChu phần 1), 00061 (phần 2 hàm main), 00066 (kết quả 6 dòng), 00070 và 00073 (check UNIQUE), 00111 (bảng quy mô), 00127 (đề tự làm). Lỗi: frame 00014 cờ `-s` bị tách dòng ("cờ -" xuống dòng "s im lặng") đọc thành "- s"; frame 00035 mũi tên "tra" hướng vào bảng khoá và "lần 3" không có mũi tên (xem B).

## G. Nhận xét ngắn
- Kiến thức L00–L03 chuẩn xác: MUST 0, mọi số và mã đều tái lập; điểm yếu là sư phạm cho người chưa từng viết mã, chứ không phải sai kiến thức.
- Lỗ hổng chung lớn nhất: không bài nào trong L00–L03 dạy cài JDK 21, khung tệp `.java` (`public class`/`main`), `for`, `String`, nên lab L00/L01/L03 (de.md không có khung) chỉ tự làm được một phần với người mất gốc thật; L02 làm tốt hơn nhờ de.md có khung đầy đủ. Đề xuất: thêm khung chạy được vào de.md của L00/L01/L03, hoặc một cảnh "khung tệp Java" ở L00.
- L00 là bài yếu nhất về P1 (từ "dịch vụ/yêu cầu/chuỗi/hàm/bộ xử lý" dùng trước khi giảng) và P3 (cảnh formula/example nhắc "hình trước" mà màn hình không còn hình); sửa bằng cách đặt lại sơ đồ đồ thị A–F vào formula và example.
- L02 thiếu hình cho REQUIRES_NEW và cho cạn hộp kết nối; L03 hình khoá có mũi tên "tra" hướng ngược và lệch lời nói về lần 3; L03 nên nhắc rõ phần máy chủ+curl trong cảnh "Tự làm" vì đó là mục tiêu 5.
- P8 và P9 đạt 2 ở cả 4 bài (có việc cụ thể + kết quả mong đợi khớp màn hình; mỗi bài có bảng ×1/×100/×10 000 kèm giải pháp cũ gãy và đánh đổi); cham.sh chấm ĐÚNG cả bốn lời giải kho và cả bốn lời giải độc lập của mình.

## ===== PART B =====
# PART B (BNK L04, L05, L06, L07): đã đọc 4/4 bài

Quy ước chấm của tôi (để người điều phối quy đổi): P1 = 2 chỉ khi KHÔNG còn từ/ký hiệu/khái niệm nào dùng mà chưa giảng (tính cả trong show/code). P1 = 1 khi các mục chưa giảng chỉ là chi tiết mã "chạy-xem" hoặc công cụ ngoài, không chặn dòng lập luận chính. P1 = 0 chỉ khi thiếu một khái niệm then chốt của chính mục tiêu bài. Không bài nào trong 4 bài bị P1 = 0, nhưng không bài nào đạt P1 = 2.
sha16 tính lại lúc đọc: L04 fe6af285924852a1, L05 31d8962949cbe789, L06 94ebbf6255890705, L07 6c2101ac92336180 (khớp danh sách giao việc).

## A. Chuẩn xác
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L04 | SHOULD | quy_mo step 0 (ghi chú trên màn hình + lời đọc) | "Byte: đơn vị lưu một ký tự" và lời đọc "mỗi dòng chỉ mục chiếm mười sáu byte, tức mười sáu ký tự" | Một byte chỉ bằng một ký tự với chữ ASCII; ký tự tiếng Việt có dấu dùng 2–3 byte trong UTF-8 (ví dụ "ế" = 3 byte: `len("ế".encode())` = 3). Khẳng định thiếu điều kiện áp dụng; con số 16 B/dòng vẫn là số minh hoạ nên không ảnh hưởng phép tính | Đổi thành "một byte đủ lưu một chữ cái không dấu; chữ có dấu tốn 2–3 byte" hoặc bỏ vế "tức mười sáu ký tự" | CONFIRMED |
| L04 | SHOULD | chay_that step 3 (ghi chú) và prereq step 1 | "Máy in thêm ba cột số đứng trước, ta chỉ đọc cột cuối." cùng "chạy tệp SQL bằng python labs/sqlrun.py tệp.sql hoặc sqlite3" | Dòng "2\|0\|216\|SCAN tx" là dạng thô của Python/sqlrun.py (tôi chạy lại bằng sqlite3 của Python 3.49.1: ra đúng (2, 0, 216, 'SCAN tx')). Chương trình dòng lệnh `sqlite3` in dạng cây ("QUERY PLAN" rồi "`--SCAN tx") nên người học dùng `sqlite3` sẽ thấy khác màn hình (không có sqlite3 CLI trên máy kiểm: dựa trên hành vi đã biết của shell, chưa chạy được) | Nói rõ "nếu dùng `sqlite3` thì thấy dạng cây, chữ SCAN/SEARCH vẫn như trên" | PLAUSIBLE |
| L05 | SHOULD | quy_mo step 0 (đầu bảng và lời đọc) | cột "cặp ngược thứ tự kỳ vọng", đối chiếu câu "số cặp gây bế tắc kỳ vọng là số cặp nhân 0,0001" và ở step 1 "ở ×100 xảy ra vài chục lần mỗi lượt" | Nhãn cột nói "cặp ngược thứ tự" nhưng câu dẫn và kết luận nói "bế tắc xảy ra". Chính bài (formula Bước 2) nói ngược thứ tự chỉ là điều kiện cần, "xảy ra thật khi cả hai kịp giữ khoá đầu". Con số 50 (= 499 500 × 0,0001 = 49,95) là số cặp giả định, không phải số lần bế tắc thật; đã có chữ "số minh hoạ" nên chỉ là lệch nhãn | Đổi tên cột thành "cặp gây bế tắc kỳ vọng (giả định)", hoặc nêu xác suất 0,0001 đã gồm cả khả năng chồng thời gian | PLAUSIBLE |
| L06 | — | | | không phát hiện lỗi (mọi số, mã Java và đáp án quiz đều tính lại/chạy lại khớp) | | |
| L07 | — | | | không phát hiện lỗi (crc32 TK-1001 % 6 = 1 và murmur2 của Kafka cho phân vùng 2 đều tính lại khớp lời bài) | | |

Không có MUST ở 4 bài. Tổng: MUST 0, SHOULD 3 (L04 ×2, L05 ×1). Chưa kiểm được: Oracle 26ai Free thật (không có Oracle, không chạy docker), khối PL/SQL chỉ đọc (cú pháp `SELECT … INTO … FOR UPDATE`, `DBMS_OUTPUT.PUT_LINE`, `||` đều hợp lệ theo hiểu biết của tôi).

## B. Độ sâu
| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L04 | fe6af285924852a1 | 14.3 | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 10 | GẦN | Git Bash/cửa sổ lệnh và cách chạy `python labs/sqlrun.py` hoặc `bash labs/cham.sh` (chỉ nhắc tên, không dạy cài/mở); từ "hàm" (function) ở Lỗi 2 và bảng check (abs(...)); `SELECT *`; cú pháp WITH RECURSIVE/UNION ALL (chỉ giải thích bằng lời đọc, không có trên màn hình); "tải" | P1: Git Bash/cửa sổ lệnh (prereq step 1, practice step 1), "hàm" (pitfalls step 1, check step 1), "tầng"/"cây" dùng ở hook trước khi định nghĩa ở intuition. P2: (a) prereq ④ dạy tìm nhị phân + 2^10 + "11 lần so" rồi cả bài KHÔNG nối nó với cây chỉ mục (người học không biết vì sao học nhị phân; f=2 chính là nhị phân); (b) check step 0–1 đổi sang bảng `account_id/created` 5000 dòng và chỉ mục `(account_id, created)` mà không hiện câu CREATE nào, tên cột đổi từ `tk` sang `account_id` nên người học không dựng lại được bảng kết quả. P3: intuition step 0 nhãn nút ghi "100 lối rẽ" nhưng chỉ vẽ 2 mũi tên (chú thích đính chính nằm ở dòng nhỏ cuối hình); hình không thể hiện khoá đã sắp thứ tự trong nút dù lời đọc nói "đã sắp thứ tự". P7: mục tiêu 6 (viết CREATE TABLE/INSERT/GROUP BY/COUNT/tạo chỉ mục) chỉ có một hàng bảng prereq ⑤ và gợi ý "Nếu kẹt"; GROUP BY/SUM/ORDER BY không có ví dụ chạy nào; lab không có EXPLAIN nên kỹ năng chính (đọc kế hoạch) không được tự luyện |
| L05 | 31d8962949cbe789 | 15.3 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 12 | ĐỦ | Java: try/catch/finally, InterruptedException, lambda `() -> …`, mảng boolean[], ReentrantLock/Lock/tryLock (lời đọc chỉ giải thích lock/tryLock; try/catch/finally không được dạy ở L00–L03: grep "finally" = 0); SQL/PLSQL: dấu `/` kết thúc khối, toán tử `||`, kiểu NUMBER; Docker (chỉ có trong lời đọc); Git Bash; "luồng" (thread) ở prereq ① | P1: các mục kể ở cột "Cần biết trước" (prereq ① dùng "luồng chương trình" khi chưa định nghĩa; chay_that step 2 `/` và `\|\|` trên màn hình không giải thích). P7: mục tiêu 4 "Xử lý đúng khi gặp ORA-00060" chỉ có chữ ở pitfalls 3 và recap, không có mã EXCEPTION nào, không có câu quiz/lab kiểm; mục tiêu 5 "chạy PL/SQL trên Oracle" người học không thể làm (cần Oracle trong Docker, lab chỉ là Java Math.min/max không đụng khoá). Ghi chú P3: hình thứ ba trong cảnh "Hình dung: vòng tròn chờ" là sơ đồ khối DECLARE/BEGIN/EXCEPTION/END (đúng nội dung, lệch tiêu đề cảnh) |
| L06 | 94ebbf6255890705 | 15.3 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ | Java: generics `Map<Integer, Long>`/`HashMap<>`, `static`, `long`/`int`, hậu tố `1000L`, `%`; "mili giây/ms" (tiền tố mili không được giảng); "nhóm kết nối" (connection pool) ở quy_mo step 1; "định luật Little" (chỉ nêu tên, công thức có ví dụ 100 × 0,02 = 2); "luồng" ở Lỗi 2; ký hiệu tđệm/tcsdl (bài dùng c/d ở formula nhưng tđệm/tcsdl ở hook, quiz, recap); Git Bash | P1: generics và "mili giây" (hook step 0), "nhóm kết nối" (quy_mo step 1). P3: intuition step 0 hình kiểu hỏi bộ đệm trước KHÔNG vẽ bước "nạp vào bộ đệm" dù đó là điều làm tỉ lệ trúng tăng (chỉ nói ở mã chay_that); intuition step 0 nhãn "2. trượt → hỏi tiếp" và step 2 nhãn "1 < 2 → từ chối" bị mũi tên cắt ngang chữ (khung 00034, 00046); chay_that step 0 dòng chú thích "// trượt: hỏi bộ đệm 1 ms rồi cơ sở dữ liệu 20 ms" tràn ra ngoài khung mã (khung 00064). Lab: hint "Nếu kẹt" gần như là lời giải của hàm soDu |
| L07 | 6c2101ac92336180 | 15.1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | Java: `while`, `continue`, `&&`, `!`, StringBuilder, Arrays.toString (lời đọc có nhắc "bộ ghép chữ", "hàm biến mảng thành chữ"); "luồng" (thread) ở lỗi 2 vì bài dùng "luồng" cả nghĩa "luồng thông điệp" lẫn "luồng riêng của nhịp báo"; "khoá lũy đẳng" (từ L03; check step 1 có dạy cách khử trùng bằng tập mã đã xử lý nên đủ dùng); `poll()`, tham số `max.poll.*` (có chú thích trong ngoặc); Git Bash | P1: các mục ở cột "Cần biết trước" (nhỏ, đều là mã chạy-xem). P3 ghi chú: bài không có hình cho bước băm khoá → phân vùng (chỉ có chữ và phép chia dư 13 = 2×6+1), nhưng 3 hình còn lại (chia việc, chia lại, hai thứ tự ghi nhớ) khớp lời đọc, không lỗi hiển thị. Khó hiểu nhất ở mã: chay_that step 3 dùng `continue` + `while (viTri < 5)` để mô phỏng "khởi động lại" mà lời đọc chỉ nói kết quả, không nói vì sao `continue` = khởi động lại |

## C. Lab
| Bài | tự làm được (có/không/phần) | thời gian | kẹt ở đâu | mong_doi khớp màn hình | cham.sh lời giải kho |
|---|---|---|---|---|---|
| L04 | có (ghi chú: người học phải biết INSERT nhiều bộ giá trị `VALUES (…),(…)` hoặc gõ 7 câu INSERT; cả hai đều đúng) | tôi viết trong ~2 phút (ước tính người mất gốc 15–25 phút, kể cả cài/mở Git Bash và python) | không kẹt ở đề; có thể kẹt ở bước chạy `bash labs/cham.sh` / `python labs/sqlrun.py` vì bài không dạy mở cửa sổ lệnh, và phải đứng đúng thư mục chứa `labs/` | khớp: 7 dòng "1\|900000 … 13\|300000" trong mong_doi.txt trùng chữ với màn hình "Kết quả mong đợi" | ĐÚNG; tệp tôi tự viết cũng ĐÚNG |
| L05 | có (đề gợi sẵn Math.min/Math.max; cần biết mảng 2 chiều và vòng for-each, bài chỉ cho ở khối "Nếu kẹt") | ~3 phút (người mất gốc 10–20 phút) | không kẹt ở đề; kẹt tiềm năng ở `int[][]` và `for (int[] l : lenh)` nếu chưa học L00–L01. Lab không đụng khoá/bế tắc: chỉ luyện "sắp min–max", người học không tự thấy bế tắc | khớp: 4 dòng "4 -> 9: khoa 4 roi 9 …" trùng màn hình | ĐÚNG; tệp tôi tự viết ĐÚNG |
| L06 | phần (đề đủ để hiểu việc; viết `Map<Integer, Long>`, `containsKey`, `put` cần prereq ④ và "Nếu kẹt"; người mất gốc khó tự viết hàm soDu nếu không nhìn ví dụ BoDem trong bài) | ~5 phút (người mất gốc 20–30 phút) | kẹt tiềm năng ở khai báo generics và kiểu `long` + `1000L`; vòng gọi `soDu(i % 4)` | khớp: "trung 36/40, trung binh 5.0 ms" trùng màn hình; tôi tính tay (4×32 + 36×2)/40 = 5,0 | ĐÚNG; tệp tôi tự viết ĐÚNG |
| L07 | phần (công thức `phanVung / bo + (b < phanVung % bo ? 1 : 0)` phải lấy từ de.md hoặc khối "Nếu kẹt"; phần còn lại mô theo ChiaPhanVung) | ~5 phút (người mất gốc 20–30 phút) | kẹt ở toán tử `? :` và `StringBuilder.append` nếu chưa học; khoảng trắng đầu chuỗi " ngoi khong" và " P" quyết định ĐÚNG/KHÁC (đề nêu rõ trong de.md; màn hình không nêu) | khớp: 7 dòng P0…P6, 2 dòng "ngoi khong", "so nguoi ngoi khong: 2" trùng màn hình | ĐÚNG; tệp tôi tự viết ĐÚNG |

## D. Người học kẹt ở đâu
- L04: không kẹt ở khái niệm chính; kẹt đầu tiên ở prereq step 1: "chạy tệp SQL bằng python labs/sqlrun.py tệp.sql hoặc sqlite3" (không dạy cài Python/mở cửa sổ lệnh), rồi check step 1: bảng điều kiện WHERE dùng cột account_id/created và "chỉ mục (account_id, created)" mà không có câu CREATE nào để tự dựng lại.
- L05: kẹt đầu tiên ở chay_that step 4–5 (khối Java): "} catch (InterruptedException e) {" / "} finally { dau.unlock(); }" và "new Thread(() -> ok[0] = lam(x1, y1))" không được giảng; phần lập luận chính (vòng chờ, khoá theo id tăng) không kẹt. Cũng không thể tự chạy "chạy thật trên Oracle" (cần Docker, chỉ xem).
- L06: kẹt đầu tiên ở chay_that step 0: "static Map<Integer, Long> boDem = new HashMap<>();" và "long v = tk * 1000L;" (generics, hậu tố L); phần công thức và mã chặn không kẹt.
- L07: không kẹt ở khái niệm; kẹt đầu tiên ở chay_that step 3: "if (m == 2 && !daSap) { daSap = true; continue; }" (không giải thích `continue` trong `while` chính là "khởi động lại và đọc từ viTri"), trong khi kết quả [1,1,0,1,1] / [1,1,2,1,1] được nêu rõ.

## E. Số đã tính lại / mã đã chạy
- L04: 30 mục tính lại/chạy lại, 30 khớp (2^10; tìm nhị phân 1024 phần tử tối đa 11 lần so; 100^1…100^4; số tầng 10^5 → 3, 10^6 → 3, 10^7 → 4, 10^9 → 5; 4+1; quy_mo: 0,1 s / 10 s / 1000 s ≈ 16,7 phút, 1,6 MB / 160 MB / 16 GB; quiz 3 tầng + 1 = 4; SQL: bảng 5000 dòng, 3 kế hoạch EXPLAIN QUERY PLAN trên sqlite 3.49.1 đúng chữ màn hình "2|0|216|SCAN tx", "2|0|56|SEARCH tx USING COVERING INDEX i_tk (tk=?)", "2|0|216|SCAN tx"; bảng 5 điều kiện × 2 cột = 10 kết quả SCAN/SEARCH đúng như bảng; lab). SRT vs say: 131 câu so, 131 khớp (chuẩn hoá dấu câu/chữ hoa), 0 câu thiếu, 0 câu thừa. Tên script: agB\l04_plan.py, agB\srtcmp.py.
- L05: 10 số khớp 10/10 (T(T−1)/2 = 45, 499 500, 4 999 950 000; ×0,0001 = 0,0045 / 49,95 / 499 995; 3! = 6; 1 000 000 − 300 000 = 700 000 và 500 000 + 300 000 = 800 000, tổng 1 500 000; 4 cặp thứ tự với 2 cặp ngược). Mã: BeTac.java ghép từ 3 khung màn hình, biên dịch và chạy trên JDK 21 cho đúng "A roi B  va  B roi A: be tac" / "A roi B  va  A roi B: xong"; ThuTuKhoa (lab) ĐÚNG; PL/SQL chỉ đọc, không chạy (không có Oracle). SRT vs say: 145 câu, 145 khớp, 0 lệch.
- L06: 21 số khớp 21/21 (T = 3 / 11 / 20 ms; 20/3 = 6,7; 1,2 ms và 16,7 lần; 20/11 = 1,8; (90×1 + 10×21)/100 = 3; quiz 8 ms và 3,75 lần; Little 100/10 000/1 000 000 × 0,02 = 2 / 200 / 20 000 và nhân 0,1, 0,01 cho cột 90%, 99%; 20 000 × 0,0005 = 10; 12 − 10 = 2; lab 5,0 ms). Mã: BoDem.java in "trung 90/100, trung binh 3.0 ms" và MaChan.java in "B ghi (ma 34): true / A tinh day ghi (ma 33): false / gia tri cuoi: B", cả hai đúng như màn hình; BoDemNho (lab) ĐÚNG. SRT vs say: 140/140 khớp, 0 lệch.
- L07: 10 mục khớp 10/10 (13 = 2×6+1; chia 10 phân vùng cho 4 bộ = [3,3,2,2]; 6/3 = 2, 6/2 = 3, 8−6 = 2, 12−10 = 2; 7 phân vùng cho 9 bộ = 7 bộ nhận 1 và 2 ngồi không; 5000/1000 = 5, 500 000/1000 = 500, 50 000 000/1000 = 50 000; tồn đọng (5000−4000)×3600 = 3 600 000, (500 000−4000)×3600 = 1 785 600 000 ≈ 1,79 tỉ, (50 000 000−4000)×3600 = 179 985 600 000 ≈ 180 tỉ; crc32("TK-1001") % 6 = 1; tự cài lại murmur2 của Kafka: partition = 2 đúng như bài nói). Mã: ChiaPhanVung.java và GhiNho.java ghép từ khung màn hình, chạy cho đúng từng dòng màn hình ("bo doc 0: P0 P1 P2 …", "ghi nho truoc: [1, 1, 0, 1, 1]", "xu ly truoc:   [1, 1, 2, 1, 1]"); NguoiNgoiKhong (lab) ĐÚNG. SRT vs say: 140/140 khớp, 0 lệch.
- Tổng L05–L07 trong nums.py: 41/41. Tổng 4 bài: khoảng 71 số/đoạn tính lại, 71 khớp; 7 chương trình Java/SQL chạy lại (BeTac, BoDem, MaChan, ChiaPhanVung, GhiNho, script SQL L04, các lab); 3 lab tự viết + 4 lời giải kho đều ĐÚNG.
- Giới hạn: SRT trùng chữ với `say` nên chỉ chứng minh phụ đề không lệch lời viết, không kiểm tiếng thật bằng tai.

## F. Khung hình đã xem
- L04 (14 khung): frames/00002, 00012, 00033, 00060, 00063, 00069, 00072, 00075, 00084, 00088, 00099, 00105, 00115, 00129. Lỗi hiển thị: 00033 nhãn nút "tầng 2: 100 lối rẽ" nhưng chỉ vẽ 2 mũi tên (chú thích 2 nhánh nằm ở dòng nhỏ cuối hình); 00069 chỉ có dòng mở đầu của cảnh check (bảng ở khung 00072), khung trống phía dưới là bình thường; còn lại không tràn, không đè.
- L05 (12 khung): 00004, 00010, 00026, 00033, 00060, 00067, 00070, 00081, 00104, 00114, 00132, 00144. Lỗi hiển thị: không có. Ghi chú: 00033 là sơ đồ khối DECLARE/BEGIN/EXCEPTION/END dưới tiêu đề cảnh "Hình dung: vòng tròn chờ"; 00104, 00132 có nút "Dừng video…" đúng thiết kế (pause 25 s và 120 s).
- L06 (11 khung): 00004, 00020, 00034, 00040, 00046, 00064, 00100, 00112, 00118, 00127, 00139. Lỗi hiển thị: 00034 chữ "2. trượt → hỏi tiếp" bị mũi tên cắt ngang; 00046 chữ "1 < 2 → từ chối" bị mũi tên đỏ cắt ngang; 00064 dòng chú thích mã "… cơ sở dữ liệu 20 ms" tràn ra ngoài viền khung mã (kết thúc ở x≈1892/1920, gần mép màn hình).
- L07 (12 khung): 00005, 00014, 00028, 00031, 00034, 00038, 00060, 00068, 00112, 00117, 00128, 00139. Lỗi hiển thị: không có (chữ trong khung đọc được, không tràn).

## G. Nhận xét ngắn
- Kiến thức của cả 4 bài đúng theo mọi phép tính tôi chạy lại (kể cả murmur2 và crc32 của L07); không có MUST, 3 SHOULD đều là phát biểu đơn giản hoá thiếu điều kiện hoặc lệch nhãn, không đổi kết luận bài.
- Điểm yếu chung là P1 ở phần mã Java/SQL "chạy-xem" (try/catch/finally, lambda, generics, `continue`) và công cụ (Git Bash, cửa sổ lệnh): bài chỉ nhắc tên lệnh chấm, không dạy mở/cài; vì vậy không bài nào đạt P1 = 2 (mốc ≥ 90% sẽ không đạt nếu giữ chuẩn này).
- Lab đều tự làm được và cham.sh ĐÚNG, nhưng lab không luyện kỹ năng cốt lõi của bài: L04 không có EXPLAIN, L05 không có khoá/bế tắc, L06 không có mã chặn, L07 không có thứ tự ghi nhớ; chúng luyện phần số học phụ (min/max, chia dư, bộ đệm). P8 = 2 theo đúng rubric (việc cụ thể + kết quả mong đợi) nhưng không phải "thí nghiệm đổi tham số" cho phần chính.
- L04 là bài yếu nhất của phần này (tổng P1–P7 = 10, GẦN): tìm nhị phân dạy rồi không dùng, bảng check không dựng lại được, hình cây ghi 100 lối rẽ mà vẽ 2.
- P9 = 2 ở cả 4 bài (có bảng 3 mức quy mô, "giải pháp cũ gãy ở đâu" và đánh đổi), là điểm mạnh nhất của phần này.

## ===== PART C =====
# PART C: đã đọc 4/4 bài (BNK L08, L09, L10, L11)

sha16 tính lại lúc đọc: L08 529eebd880d911ba, L09 bc40ae378b945413, L10 fbc24c50afb1ca08, L11 4966948d62115414 (đều khớp danh sách giao).
Quy ước chấm P1 (nêu rõ để người điều phối tính lại được): một thuật ngữ/ký hiệu xuất hiện ở cảnh `hook` hoặc trong mã mà chưa được giảng tại chỗ, dù cảnh sau mới giảng, vẫn tính là "chưa giảng tại chỗ".

## A. Chuẩn xác
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L08 | SHOULD | hook, step 2 (bảng) | "kết quả (thấy ở phần chạy thật cuối bài)" cạnh hai dòng "ghi có lỗi, không bù → tiền mất dấu" và "ghi có lỗi, chạy bước bù → ghi nợ được hoàn lại" | Phần "chạy thật" chỉ in nhật ký bước (Saga: `[giu han muc, ghi no, loi ghi co, bu ghi no, bu giu han muc]`) và số dư/outbox của SQL. Không có lần chạy nào cho thấy "tiền mất dấu" hay số dư được hoàn lại; "bỏ các dòng bù ... tiền đã trừ" chỉ được nói bằng lời. Hai trong bốn dòng của bảng hứa điều bài không cho xem. | Sửa chú thích thành "(hai dòng đầu thấy qua nhật ký bước bù; hai dòng sau thấy ở cơ sở dữ liệu)" hoặc thêm số dư vào mô phỏng. | PLAUSIBLE |
| L08 | SHOULD | chay_that, step 1 | `Saga.java (phần chính)` — đoạn mã kết thúc ở dòng `System.out.println("loi o buoc " + loi + ": " + nhatKy);` | Đoạn hiển thị thiếu `}` đóng vòng `for` ngoài và thiếu `class`/`main`; chép nguyên văn không biên dịch được (tôi phải thêm khung `public class Saga { main { ... } }` và `}` mới chạy; sau đó cho đúng 3 dòng như màn hình). Tiêu đề có ghi "phần chính", và bài không yêu cầu người học chạy Saga, nên chỉ SHOULD. | Hiện cả khung class/main/dấu `}`, hoặc ghi rõ "lược bớt khung". | PLAUSIBLE |
| L09 | SHOULD | check, step 1 | `SELECT txn FROM entry GROUP BY txn HAVING SUM(amt) <> 0;` ("Bảng entry (bút toán) có cột txn ... và amt") | Cảnh chạy thật và lab dùng bảng `but_toan(gd, tk, tien)`; cảnh này đổi sang `entry(txn, amt)`. Câu truy vấn trên màn hình không chạy được trên bảng người học vừa dựng (tôi chạy với bảng `entry` tự tạo thì ra `1`; với `but_toan` phải đổi tên 3 chỗ). Người mất gốc dễ tưởng là hai thứ khác nhau. | Dùng đúng `but_toan`, `gd`, `tien` ở cảnh check. | CONFIRMED |
| L10 | MUST (ranh giới MUST/SHOULD) | chay_that, step 5 (HetGio, kết quả chạy) | say: "Hỏi trạng thái trước thì trong mô hình này cả bốn trường hợp đều đúng một lần." | Màn hình ngay trước đó in 4 dòng `2, 1, 1, 1`, dòng đầu (đã hạch toán, gửi lại ngay) là 2; bảng cảnh check cũng ghi A = 2. Chỉ có 2 trường hợp "hỏi trước" (đều ra 1). Câu nói sai số đếm và mâu thuẫn với dòng đầu trên màn hình, ở đúng điểm kiến thức của cảnh. Tôi chạy `HetGio.java` chép từ màn hình: 2,1,1,1 (khớp màn hình, lệch lời đọc). | Đổi "cả bốn trường hợp" thành "cả hai trường hợp hỏi trước" (hoặc "ba trong bốn trường hợp còn lại"). | CONFIRMED |
| L11 | SHOULD | formula step 3 và chay_that step 3 | show: "duyệt trường $2..64$"; say: "duyệt các trường từ trường hai"; mã: `print([k for k in range(1, 65) if bando >> (64 - k) & 1])` | Lời và chữ nói bắt đầu từ trường 2 (vì bit 1 chỉ báo bản đồ thứ hai) nhưng mã duyệt `range(1, 65)` tức gồm cả bit 1. Với ví dụ bit 1 tắt nên ra `[2, 3, 4, 11]` đúng, nhưng mã không đúng như điều bài vừa dạy (bản tin có bản đồ thứ hai sẽ in thêm `1`). Chạy: `[2, 3, 4, 11]`. | Đổi thành `range(2, 65)`. | CONFIRMED |
| L11 | SHOULD | pitfalls, step 2; quy_mo, step 2; quiz Q3 | "PCI DSS yêu cầu che khi hiển thị, chỉ giữ tối đa 6 số đầu và 4 số cuối" | (a) Theo hướng dẫn của PCI SSC, với PAN từ 16 số trở lên phần BIN được hiển thị có thể tới 8 số, nên "tối đa 6" thiếu điều kiện. (b) Yêu cầu 3.4.1 là về hiển thị; chỗ lưu trong nhật ký thuộc yêu cầu làm PAN không đọc được ở nơi lưu (3.5.1). Chưa kiểm được nguồn trực tiếp (không có tài liệu PCI trong kho), ghi theo kiến thức của tôi. | Ghi "6 số đầu (hoặc BIN, có thể 8 số với thẻ 16 số trở lên) và 4 số cuối" và nêu yêu cầu cho nhật ký lưu trữ. | PLAUSIBLE |
| L09 | — | | | không phát hiện lỗi MUST (SHOULD duy nhất ở trên) | | |

Ghi chú đã kiểm không lỗi: ISO 4217 VND có 0 chữ số thập phân; USD 2 (L09, L11); MTI 0200/0210, DE 2/3/4/11/37/39, LLVAR, bit 1 = bản đồ thứ hai (L11); OFS = Open Financial Service, MessageID/CorrelationID (L10); SAGA không có tính cô lập, bù ngược thứ tự, Outbox cùng giao dịch (L08); Pacioli 1494 (L09). Mọi con số trên màn hình đã tính lại khớp (mục E).

Số MUST: 1 (ranh giới), SHOULD: 5.

## B. Độ sâu
| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L08 | 529eebd880d911ba | 15.0 | 1 | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 11 | GẦN | Java vòng `for`/`List`/`ArrayList`/`break` (L00–L01); SQL `CREATE/INSERT/UPDATE/PRIMARY KEY/DEFAULT` (L04); MB/GB không giảng | P1: "Outbox" dùng ở bảng hook (00:22) trước khi giảng (01:35, cảnh sym); "hộp thư đi" = Outbox không bao giờ nói thẳng. P2: bảng quy_mo cho "≈ 1,2", "≈ 116", "12 bộ chuyển tiếp" mà không hiện phép chia 86 400 giây/ngày và làm tròn lên (11 574 / 1 000 → 12). P3: nhãn "đọc sau" đè đầu mũi tên ở hình Outbox; hình Outbox dùng nguyên tiêu đề "chuỗi bước và bước bù ngược chiều" của hình trước |
| L09 | bc40ae378b945413 | 14.4 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `UPDATE ... SET` (L08/L04); "khoá hàng" (L05) | P1: pitfalls step 1 dùng "khoá hàng" và `UPDATE … SET so_du = so_du - x` khi chưa giảng (khoá hàng chỉ được nhắc ở quy_mo, "như ở bài 5"); mô hình "số dư của A = −505 500" (âm) dễ bị hiểu là khách nợ, chỉ có chú thích nhỏ "sổ bắt đầu trống" |
| L10 | fbc24c50afb1ca08 | 15.5 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ | Java `Map/HashMap`, toán tử ba ngôi `?:`, `substring`, `equals` (L00–L07); "xác suất"; "xử lý song song" (L01) | P1: hook (00:00–00:40) dùng "hàng đợi", "mã tương quan" trước khi giảng (prereq 00:40, sym 01:30); mã `int n = daHachToan ? 1 : 0;` không giảng `?:`. P3: nhãn "tương quan = M7" và "M7" nằm đè lên mũi tên ở hình hai hàng đợi (vẫn đọc được) |
| L11 | 4966948d62115414 | 15.6 | 0 | 1 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 10 | GẦN (có một mục 0) | Python: list comprehension `[k for k in range(...) if ...]`, `range`, `|=`, thứ tự ưu tiên `>>` trước `&`, `sorted`/`"".join` (gợi ý lab); "băng thông", "lấy mẫu", "đặc tả" | P1=0: Python mới xuất hiện từ bài này, prereq ⑤–⑦ chỉ giảng `<<`, `>>`, `|`, `&`, từ điển, cắt chuỗi, `%016X`; mã đọc ngược dùng list comprehension + `range` + `|=` chưa giảng; "băng thông" và "lấy mẫu" chỉ xuất hiện ở bài này, không giảng. P2: cột "nhật ký mỗi ngày" (933 MB, 93,3 GB, 9,33 TB) cần ×86 400 mà bài không nói. P7: mục tiêu 4 "Che số thẻ khi ghi nhật ký" chỉ được xem ví dụ `411111******1111`, không có việc người học tự che, lab không đụng tới |

## C. Lab
| Bài | tự làm được (có/không/phần) | thời gian | kẹt ở đâu | mong_doi khớp màn hình | cham.sh lời giải kho |
|---|---|---|---|---|---|
| L08 | có | khoảng 8 phút | không kẹt; đề đưa sẵn tên bảng/cột và nhắc `BEGIN;` cho mọi giao dịch; lời giải của tôi (`L08_outbox.sql`) chấm ĐÚNG ngay lần đầu | khớp (màn hình "2300000 / lenh 77 da tru 700000\|0" = mong_doi.txt) | ĐÚNG |
| L09 | có | khoảng 8 phút | không kẹt; `de.md` còn cho nguyên câu `GROUP BY gd HAVING SUM(tien) <> 0` nên phần tìm giao dịch lệch gần như chép (bài chỉ dạy `HAVING` ở prereq ⑤ và check) | khớp ("2 / C\|-1256600 / D\|1240000 / phi\|6600") | ĐÚNG |
| L10 | phần/có (có nếu đã theo Java L00–L07) | khoảng 20 phút với người mới Java | cú pháp `Map<String,String>`, `put/get`, `equals` chỉ được cho qua mã mẫu của bài, không giảng; lời giải của tôi chấm ĐÚNG ngay | khớp (7 dòng, "dung neu ghep theo thu tu: 1/6") | ĐÚNG |
| L11 | phần/có | khoảng 15 phút | người học cần tự ghép `for so in truong: bit \|= 1 << (64 - so)` (mô theo ví dụ) rồi nối chuỗi theo `sorted`; `sorted`/`join` chỉ có trong khung "Nếu kẹt"; không giảng `\|=`. Lời giải của tôi chấm ĐÚNG | khớp ("3020000002000000 / 46") | ĐÚNG |

## D. Người học kẹt ở đâu
- L08: hook step 2 (00:22): "có Outbox → 1 sự kiện được phát" — "Outbox" chưa giảng đến cảnh sym (01:35). Kẹt nhẹ thứ hai ở cảnh intuition (02:05): "Bước không giữ hạn mức đã xong" nghe như phủ định (bước 0), và ở quy_mo (09:42) bảng "≈ 1,2 / 12" không có phép tính.
- L09: pitfalls step 1 (06:56): "câu `UPDATE … SET so_du = so_du - x` thì được khoá hàng nên không ghi đè" — chưa giảng `UPDATE` và "khoá hàng" ngay chỗ này; cảnh check (06:15) đổi tên bảng `entry/txn/amt` khác bảng vừa dựng.
- L10: hook step 1 (00:00): "qua hàng đợi ... Phải ghép theo mã tương quan" chưa giảng (có trực giác nhưng chưa có định nghĩa); kẹt thật ở chay_that step 4 (05:54, `int n = daHachToan ? 1 : 0;`) toán tử `?:` chưa giảng, và lời đọc step 5 (06:10) "cả bốn trường hợp đều đúng một lần" mâu thuẫn với dòng "2" trên màn hình.
- L11: chay_that step 3 (06:48, "Bây giờ đọc ngược"): `print([k for k in range(1, 65) if bando >> (64 - k) & 1])` — danh sách rút gọn, `range`, thứ tự `>>` rồi `&` đều chưa giảng; người mới Python đứng lại ở dòng này.

## E. Số đã tính lại / mã đã chạy
- L08: mã đã chạy 4/4 (Saga.java bọc khung → 3 dòng khớp; SQL Outbox chốt `1500000` và `lenh 42 da tru 500000|0`; ghi kép `1500000`, `0`; huỷ `2000000`, `0`; tất cả khớp màn hình) + lab. Số: 2i+1 cho i=0,1,2 (1, 3, 5) và quiz i=3 (7); bảng quy_mo 15 ô (100/10 000/1 000 000 lệnh bù; 20 MB/2 GB/200 GB; 1,2/116/11 574; 12 bộ) khớp 15/15. SRT vs say: 133/133 câu (số từ 2 180 = 2 180), không lệch (SRT dựng từ chính `say`).
- L09: SQL đã chạy 3 khối/3 khớp (1|0; khach_A −505500, khach_B 500000, thu_phi 5500; sau đảo 0,0,0 và 6 dòng; `entry` cho `1`) + lab. Số: 505 500, 2 011 000, tổng 0; bảng quy_mo 15 ô (300 000/30 M/3 tỉ; 36,5 M/3,65 tỉ/365 tỉ dòng; 36,5 giây/≈1 giờ (1,01 giờ)/≈4,2 ngày (4,22)) khớp 15/15. SRT: 136/136 câu, 2 032 từ = 2 032, không lệch.
- L10: mã đã chạy 2/2 khớp (TuongQuan: `0/5`, `5/5`; HetGio: 2,1,1,1) + lab. Số: 5!=120, mất vị trí 44 (vét cạn bằng Python), 44/120=36,67% ≈ 37%, 3 lệnh: (1,2,0),(2,0,1)=2/6, quiz 3/5, kỳ vọng số điểm cố định = 1 với n=5,6,7 (vét cạn), bảng quy_mo 12 ô (n−1 = 4, 499, 49 999; 100/10 000/1 000 000) khớp 12/12. Lệch lời–màn hình: 1 câu (xem mục A). SRT: 146/146 câu, 2 198 từ = 2 198.
- L11: mã đã chạy 5/5 khớp (bản đồ `7020000000000000`, bản tin 62 ký tự, đọc ngược `[2, 3, 4, 11]` và `4111111111111111`) + lab (`3020000002000000`, 46). Số: 2^62+2^61+2^60+2^53 = 0x7020000000000000; 4+16+18+6+12+6 = 62; quiz `3020000000000000` và 44; 0210 `3020000002000000` và 46; che thẻ `411111******1111`; 500000/100 = 5000; bảng quy_mo 15 ô (10,8 KB, 5,4 KB, 933 MB, 1,08/0,54 MB, 93,3 GB, 108/54 MB, 9,33 TB) khớp 15/15. SRT: 141/141 câu, 2 239 từ = 2 239.
- Tổng cộng: khoảng 115 số/kết quả và 14 đoạn mã/lab đã chạy; mọi số khớp màn hình; 1 lệch lời đọc–màn hình (L10), 1 lệch chữ–mã (L11).

## F. Khung hình đã xem
- L08 (10 khung): 00000 (hook), 00022 và 00026 (hình SAGA), 00028 (hình Outbox), 00052 (mã Saga.java), 00062 (SQL Outbox), 00094 (quiz, nút dừng), 00103 và 00106 (bảng quy_mo), 00132 (tổng kết). Lỗi hiển thị: 00028 nhãn "đọc sau" chồng đầu mũi tên (đọc được); 00052 đoạn mã bị cắt ở dòng println (thiếu `}`); tiêu đề cảnh "Hình dung: chuỗi bước và bước bù ngược chiều" giữ nguyên cho hình Outbox.
- L09 (7 khung): 00007 (prereq), 00028 và 00034 (hình giao dịch, hình sổ cái), 00058 (SQL), 00071 (check), 00102 (bảng quy_mo), 00121 (đề thực hành, nút dừng). Không có chữ tràn/đè/cắt; cỡ chữ đọc được.
- L10 (7 khung): 00001 (hook), 00027 (hình hai hàng đợi), 00033 (hình thứ tự), 00065 (mã TuongQuan phần 3 và kết quả), 00081 (cảnh check vét cạn), 00101 (quiz), 00114 (quy_mo). Lỗi: 00027 nhãn "tương quan = M7" và "M7" nằm đè lên mũi tên (viền trắng giúp vẫn đọc được).
- L11 (8 khung): 00000 (hook), 00030 (hình các khúc), 00034 (hình bản đồ bit hai hàng), 00070 (ghép bản tin), 00100 (quiz), 00113 (bảng quy_mo), 00140 (tổng kết). Không lỗi hiển thị; cỡ chữ DE 4 trong hình khúc hơi nhỏ (18 px trong SVG 1500) nhưng đọc được.

## G. Nhận xét ngắn
- Lab cả bốn bài tự làm được và cham.sh chấm ĐÚNG cả lời giải của tôi lẫn lời giải kho; mong_doi khớp màn hình 4/4. Đề lab đưa nhiều gợi ý trực tiếp (L09 chép nguyên câu HAVING) nên thực nghiệm hơi nhẹ.
- Lỗi chuẩn xác đáng sửa trước: L10 câu "cả bốn trường hợp đều đúng một lần" (mâu thuẫn màn hình); L11 `range(1, 65)` trái với "từ trường hai"; L09 đổi tên bảng ở cảnh check.
- P1=2 không bài nào đạt theo quy ước nghiêm (kể cả từ dùng ở hook trước khi giảng). Nếu người điều phối miễn trừ các từ chỉ xuất hiện ở hook rồi được giảng ở prereq/sym, L08 và L10 lên 2; L09 (khoá hàng, UPDATE) vẫn 1; L11 vẫn thấp vì Python.
- L11 là bài yếu nhất cho người mất gốc: Python mới xuất hiện, mã đọc ngược dùng cú pháp chưa dạy, và hai thuật ngữ (băng thông, lấy mẫu) không giảng; mục tiêu "che số thẻ" không có việc để làm.
- Bảng quy mô cả bốn bài có số liệu 3 mức tải và phần "giải pháp cũ gãy ở đâu / đánh đổi" (P9 đạt), nhưng L08 và L11 bỏ qua phép ×86 400 giây/ngày nên người học không tự dựng lại được cột "mỗi giây/mỗi ngày".

## ===== PART D =====
# PART D (BNK L12, L13, L14): đã đọc 3/3 bài

sha16 tính lại lúc đọc: L12 ef115d71d7b8e015, L13 04f28429d76daa40, L14 efb970d81af090ba (khớp danh sách giao việc).

## A. Chuẩn xác
MUST: 0. SHOULD: 5 (L12 x2, L13 x3 nếu tính cả lỗi hiển thị) + 1 ghi chú chưa kiểm được nguồn (L13).

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L12 | SHOULD | hook, step 2 (khung 00008, 00:20) | say: "Bảng này là kết quả mô phỏng ở cuối bài, với số liệu minh hoạ." | Bảng 3/1/1/1 là kết quả của scene chay_that, hiện ở 06:10 (chapters.txt), bài còn 9 phút nữa mới hết (15:15). Lời đọc nói "cuối bài" lệch vị trí thật. | Đổi thành "ở phần chạy thật" | CONFIRMED (chi tiết nhỏ) |
| L12 | SHOULD | formula step 3 (04:06+) | show/say: "Việc sửa sổ luôn qua bước duyệt" | Khẳng định tuyệt đối "luôn", không nêu điều kiện (thực tế khoản nhỏ/tự động có ngưỡng; chính L14 quy_mo nói "tự động hoá ... đặt ngưỡng, bước duyệt"). | "Quy trình điển hình: sửa sổ phải qua bước duyệt" | PLAUSIBLE |
| L13 | SHOULD | formula step 1 (khung ~00041-00046) | show: "thiết bị còn phải mã hoá khối này bằng khoá (thuật toán chuẩn như TDES hay AES)" | Khối PIN định dạng 0 là khối 64 bit, dùng với TDES. ISO 9564-1 (Amd 1:2015) quy định khi mã hoá bằng mật mã khối 128 bit như AES thì phải dùng định dạng khối PIN 4. Nêu "AES" ngay sau khối định dạng 0 dễ hiểu sai là ghép được. Nguồn: iteh.eu ISO 9564-1:2011/Amd 1:2015 (trích đoạn, nguồn thứ cấp). | Ghi "TDES (khối định dạng 0); AES đi với định dạng 4" | PLAUSIBLE |
| L13 | SHOULD | formula step 3 (khung 00055, 00057; 05:00-05:19) | show: "Tổng cộng dồn tính lại từ 0 đầu ngày và sau mỗi lần đã xác thực mạnh." | Chi tiết "tính lại sau mỗi lần xác thực mạnh" không có trong audit/legal/registry.yaml (mục 50/2024, 77/2025 chỉ nêu ngưỡng, ngày hiệu lực); quiz câu 2 và ví dụ ⑤ dựa vào quy tắc cộng dồn này. Chưa kiểm được nguồn. | Gắn "theo nguồn thứ cấp, chưa kiểm" cho chi tiết này, hoặc bỏ | PLAUSIBLE |
| L13 | NOTE (chưa kiểm được nguồn) | formula step 3 | "trên 10 triệu đồng một giao dịch, hoặc khi tổng trong ngày vượt 20 triệu đồng" | Bài đã tự ghi CHƯA KIỂM bản Công báo (đúng như registry). Tìm web: thông cáo SBV về TT 50 nêu mốc 50 triệu/100 triệu (có thể thuộc nhóm khác, ví dụ tổ chức), một nguồn khác nêu 10 triệu cho doanh nghiệp từ 1/7; không tìm được xác nhận trực tiếp cho cặp 10/20 triệu của cá nhân. Không kết luận sai; cần người đọc bản gốc/bản hợp nhất 25/VBHN-NHNN. | Kiểm bản hợp nhất trước khi coi là chốt | chưa kiểm được |
| L13 | SHOULD | intuition SVG 1 (khung 00033, 02:33-03:35) | SVG: ô "HSM chặng giữa / (ngân hàng thanh toán, chuyển mạch) / dịch TPK/ZPK → ZPK" | Dòng chữ giữa dài hơn bề rộng ô (300 px trong viewBox), tràn ra hai bên và đè lên đầu mũi tên vào/ra (thấy rõ ở "(ngân hàng thanh toán, chuyển mạch)"). Lỗi hiển thị, nhãn bị đè. | Rút ngắn chữ hoặc nới ô lên ≥ 380 | CONFIRMED (thấy trên khung hình) |
| L14 | SHOULD | pitfalls / mục tiêu 4 (08:16, 09:01-10:33) | objectives: "Kể một sự cố thật theo khung STAR, trung thực và có số liệu có nguồn" (covers: scene pitfalls) | Bài chỉ cho khung S-T-A-R (sym) và ô trống để điền (quiz câu 3); không có một ví dụ STAR kể xong làm mẫu, và scene "pitfalls" là danh sách lỗi, không dạy cách kể. Mục tiêu "kể" chỉ được hướng dẫn, chưa được dạy trọn. | Thêm một ví dụ STAR 4 câu (gắn nhãn minh hoạ) từ chính tình huống r7/r7b | PLAUSIBLE |

Các phép tính, mã, SQL, đáp án quiz của cả ba bài: không phát hiện sai (xem mục E).

## B. Độ sâu
| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L12 | ef115d71d7b8e015 | 15.2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | Python: `for ... if`, `and`, `not in`, `!=`, `==`, `print(a, b, ...)` (bảng prereq chỉ giảng từ điển, danh sách lọc, len/sum); từ "tải" (×100 nghĩa là gì), byte/MB/GB, "song song", "tuần tự" | P1 = 1 (sát 0): chưa giảng tại chỗ "tải ×100", đơn vị byte/MB/GB (06:10 và 10:06), "song song", và cú pháp `and`, `not in`, `!=` trong khối mã chay_that (06:10). Khung in kết quả của bài tự làm ("khop 3 - lech tien 1 - ...") cần `print` nhiều đối số, chưa dạy. |
| L13 | 04f28429d76daa40 | 15.5 | 0 | 2 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 10 | GẦN | Python: `def`, `return`, `import`, `"".join(...)`, `.ljust`, `%d %s` định dạng, `.encode()`, `.hexdigest()`, `reversed`, vòng `for ... in`, `if`; TDES, AES; "mã dùng một lần" (OTP); XOR (được giảng ở bảng thứ 3, sau khi bảng thứ 2 đã dùng ở mục ⑦) | P1 = 0: ≥ 3 từ chưa giảng tại chỗ, kể cả khái niệm then chốt cho bài tự làm (hàm, vòng lặp, nhánh `if`) và `"".join(... for ...)` ở chay_that (06:27); XOR dùng ở mục ⑦ (01:2x) trước khi định nghĩa ở mục ④ (bảng sau). P3 = 1: SVG1 chữ tràn đè mũi tên (khung 00033). P7 = 1: mục tiêu 7 "Viết hàm kiểm Luhn và hàm che số thẻ", bài tự làm chỉ yêu cầu hàm `luhn`; che số thẻ viết thẳng, không phải hàm. Bài mã hoá khối PIN (TDES/AES) chỉ nêu một câu. |
| L14 | efb970d81af090ba | 15.6 | 1 | 2 | 2 | 2 | 1 | 2 | 1 | 2 | 2 | 11 | GẦN | SQL: `SELECT ... FROM ... WHERE`, `ORDER BY`, kiểu `INTEGER`/`TEXT` (prereq chỉ giảng `CREATE TABLE`, `INSERT ... VALUES`, `NOT IN`, `INSERT ... SELECT`, `||`, `SUM`); "tài khoản đối ứng", "sqlite", "ngưỡng", "sao kê" | P1 = 1: `SELECT/FROM/WHERE/ORDER BY` và "tài khoản đối ứng" (07:10) chưa giảng tại chỗ (có thể dựa vào L04, nhưng bài không nhắc). P5 = 1: câu 1 và 2 chỉ là tính số, lời giải một dòng ("(3 − 1) · 400 000"); không câu nào hỏi "vì sao khoá lũy đẳng ngăn được"; câu 3 không có đáp án mẫu. P7 = 1: mục tiêu "kể sự cố theo STAR" chỉ có khung trống, không ví dụ kể (xem A). |

## C. Lab
| Bài | tự làm được (có/không/phần) | thời gian | kẹt ở đâu | mong_doi khớp màn hình | cham.sh lời giải kho |
|---|---|---|---|---|---|
| L12 | phần (người mất gốc): tôi làm đúng ngay lần 1 nhưng đã xem bài; đề đủ về số liệu và tiêu chuẩn đầu ra, thiếu kiến thức in nhiều đối số | ước tính 15–25 phút; thực tế khoảng 3 phút | Cú pháp in hai dòng đúng chữ "khop 3 - lech tien 1 - chi ngan hang 2 - chi chuyen mach 2": bài chưa dạy `print(a, "-", b, ...)` hay f-string; khung kết quả mong đợi chỉ hiện SAU lúc dừng 150 giây; không có ở prereq. de.md đủ (có cả hai dòng mẫu) | khớp (hai dòng giống hệt màn hình 00136) | ĐÚNG; lời giải của tôi cũng ĐÚNG |
| L13 | phần: thuật toán Luhn có trong bài (scene check, bước cộng 8+14+8) và "Nếu kẹt" cho `enumerate(reversed(so))`, `i % 2 == 1`, `tong % 10 == 0`; nhưng bài không dạy `def`, `for`, `if`, `return` | ước tính 25–40 phút; thực tế khoảng 3 phút | Viết hàm có vòng lặp và nhánh: cú pháp chưa dạy trong bài; đề trên màn hình nói "vị trí 1, 3, 5" chưa nói đếm từ 0 (de.md nói rõ "vị trí 0 giữ nguyên"), người đếm từ 1 sẽ nhân đôi nhầm chữ số cuối | khớp (True / False / 550000******5559, khung 00132) | ĐÚNG; lời giải của tôi ĐÚNG |
| L14 | có (với người đã xem bài L04 hoặc chép khung từ ví dụ): chay_that cho đủ bốn câu, "Nếu kẹt" cho `NOT IN` và `INSERT ... SELECT` | ước tính 15–20 phút; thực tế khoảng 2 phút | Phải dựng bảng và dữ liệu từ lời đọc; màn hình tự làm không in tên cột `ma, tk, tien`, chỉ nói "chi tiết ở de.md", nhưng các cột có trong ví dụ chay_that. Cần nhớ `ORDER BY ma` (chỉ ở de.md, màn hình chỉ nói "sắp theo mã"). Khoản STAR câu 3: người mất gốc không có "sự cố thật" để viết | khớp (r8b, r8c, 600000, 2200000, khung 00134) | ĐÚNG; lời giải của tôi ĐÚNG |

Lời giải tôi viết giống lời giải kho gần như từng dòng vì bài đã trao toàn bộ khuôn (đổi số).

## D. Người học kẹt ở đâu
- L12: kẹt đầu tiên ở bài tự làm (12:xx-13:xx, step "Viết doi_soat.py"): đề "in số lượng từng loại, rồi chênh tiền" nhưng chưa dạy cách in nhiều giá trị trên một dòng với dấu "-"; kẹt nhẹ trước đó ở quy_mo (10:06) "một trăm nghìn mê ga byte" vì byte/MB/GB, "tải ×100" chưa giảng.
- L13: kẹt đầu tiên ở chay_that 06:27 (step 1): "khoi = "".join("%X" % (int(x, 16) ^ int(y, 16)) for x, y in zip(a, b))" và "a = ("0%d%s" % (len(pin), pin)).ljust(16, "F")": `join`, `ljust`, `%d%s` chưa dạy; kẹt chắc chắn ở bài tự làm 12:04 (viết hàm với vòng lặp). Kẹt nhẹ ở prereq 01:xx: bảng "thêm ba điều" dùng XOR (mục ⑦) trước khi mục ④ giảng XOR.
- L14: kẹt đầu tiên ở quiz câu 3 (09:01-10:33): "viết bốn câu STAR cho một sự cố THẬT của bạn": người mất gốc chưa đi làm không có sự cố thật, bài cấm bịa, không có ví dụ mẫu để bắt chước; kẹt nhẹ ở chay_that 05:59: `SELECT ... FROM ... WHERE` chưa giảng.

## E. Số đã tính lại / mã đã chạy
- Script calc.py (Python 3.13, sqlite3 chuẩn): tổng 49 kiểm tra, 49 khớp, 0 lệch. Chia theo bài: L12 16 (3-1-1-1, 150, 1500, 1650, 5+5-4=6, 50+600-500, 100 s, 11,6 ngày, 317 năm (cả 365 và 365,25 ngày), 0,01/1/100 s, 10 MB/1 GB/100 GB, 100 000 MB = 100 GB, quiz 1+2, bài tự làm 3-1-2-2/-500); L13 20 (khối PIN 041225EEEEEEEEEE, XOR lại 041234FFFFFFFFFF, PAN đệm, 0x34^0x11=0x25, 0111^0101, MAC 7625fd27947ee367 / 7958d294fb89b6dc, che số thẻ, Luhn tổng 30, Luhn lab 5500005555555559 True / ...8 False, che 550000******5559, quy tắc 15 triệu / 8-8-8 / quiz 12 / quiz 6-7-9, HSM 1/20/2000, 200/20000/2000000); L14 13 (SQL r7b / 1000000 / 1500000 chạy trong sqlite3, câu tìm sau đảo liệt kê cả dao-r7b, bẫy NULL của NOT IN trả rỗng đúng như bài nói, 2·500000, −500000−500000+500000, quiz 800 000 và 1, bảng 10/1 000/100 000 vụ, 167 giờ / 16 667 giờ, 0,2 / 21 / 2 083 người, sổ 6 dòng, bài tự làm r8b r8c 600000 2200000).
- Mã chạy: L12 khối chay_that (Python), L13 khối PIN + che số thẻ + MAC (Python), L14 khối SQL (sqlite3). Cả ba chạy đúng kết quả in trên màn hình.
- SRT vs say: L12 145 câu so / 145 cue, 0 lệch; L13 145 / 145, 0 lệch; L14 146 / 146, 0 lệch (so sánh sau khi bỏ dấu câu, hoa thường). Lưu ý: SRT được tạo từ say nên phép so này chỉ chứng tỏ không rơi/đổi câu; chưa kiểm được audio (asr_reviewed đều ghi NOT_VERIFIED bằng tai người).
- Số trong mong_doi.txt đối với màn hình/lời đọc: L12 khớp (-500, 3/1/2/2), L13 khớp, L14 khớp.

## F. Khung hình đã xem
- L12: 00008, 00019, 00040, 00045, 00071, 00076, 00086, 00102, 00121, 00124, 00128, 00133, 00136, 00144 (14 khung). Lỗi hiển thị: không. Ghi chú: SVG1 (00040) chữ ≈ 24 px, đọc được nhưng nhỏ và để trống nhiều.
- L13: 00009, 00016, 00033, 00036, 00040, 00055, 00057, 00063, 00071, 00076, 00078, 00082, 00103, 00117, 00124, 00132, 00144 (17 khung). Lỗi: 00033 (SVG1, ô "HSM chặng giữa") chữ "(ngân hàng thanh toán, chuyển mạch)" tràn ô, đè đầu mũi tên hai bên. Bước 3 (00055, 00057) là đoạn văn dày, nhưng không tràn.
- L14: 00009, 00021, 00031, 00036, 00040, 00045, 00057, 00069, 00078, 00084, 00090, 00093, 00110, 00115, 00122, 00134, 00145 (17 khung). Lỗi hiển thị: không.
(Mỗi khung chọn từ chapters.txt và _frames.txt; khung mỗi câu một khung nên 00040 của L14 là SVG thứ hai, không phải SVG đầu.)

## G. Nhận xét ngắn
- MUST = 0 ở cả ba bài; phép tính, đoạn mã, đáp án quiz, bảng quy mô đều khớp khi tính lại (49/49); SRT khớp say 100%.
- Điểm yếu chung của cụm L12–L14 là P1: bài giả định người học đã biết cú pháp Python/SQL cơ bản (`for`, `if`, `def`, `print` nhiều đối số, `SELECT/WHERE`); L13 rõ nhất (P1 = 0) vì có `def`, `return`, `import`, `"".join(...)`, `.ljust` mà không giảng, và bài tự làm đòi viết hàm có vòng lặp.
- Lab ổn: mỗi bài có de.md, mong_doi khớp màn hình, cham.sh ĐÚNG cho cả lời giải kho và lời giải tự viết; nhưng lời giải gần như là ví dụ đổi số (L12) hoặc có sẵn thuật toán và gợi ý chi tiết (L13), nên chỉ kiểm khả năng chép khuôn.
- P9 tốt cả ba (bảng 3 mức ×1/×100/×10 000 với số tính lại đúng, "giải pháp cũ gãy ở đâu", đánh đổi); P8 = 2 cả ba.
- L14 mục tiêu "kể sự cố thật theo STAR" chỉ dừng ở khung trống; người mất gốc không có sự cố thật. L13 điều khoản pháp lý (ngưỡng 10/20 triệu, cộng dồn "tính lại sau mỗi lần xác thực mạnh") đã tự gắn CHƯA KIỂM; chi tiết cộng dồn không có trong registry.
