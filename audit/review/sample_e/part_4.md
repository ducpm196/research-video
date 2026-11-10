# Mẫu E — phần 4: đã đọc 10/10 bài

Bài: RBM L17, RLN L12, ROB L12, SAR L06, SDP L02, SEC L15, SEP L01, SWF L06, TOC L08, WEB L11.
Đã đọc với mỗi bài: đặc tả yaml (title, objectives, show, say, checks, quiz), mục trong `curriculum/<khoá>.yaml`, `audit/<khoá>/sources_*.md` (RBM, RLN, SEC, SEP), `chapters.txt`, `_frames.txt`, và ít nhất 5 khung hình.

## 1. Chuẩn xác

| Bài | Mức (MUST/SHOULD) | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/nguồn) | Đề xuất sửa | Tin cậy (CONFIRMED/PLAUSIBLE) |
|---|---|---|---|---|---|---|
| SDP L02 | MUST (giáp ranh: hạ SHOULD nếu coi là trích đoạn) | example, step0 (mã) + step1 (bảng, bước 3) | Mã `class TaiKhoan:` chỉ có `__init__`, `so_du`, `rut`; bảng: “3 \| tạo 200, nạp 50 \| … \| cộng \| 250” | Lớp trên màn hình không có phương thức `nap`. Tôi chạy đúng mã đó: `TaiKhoan(200).nap(50)` báo `AttributeError: 'TaiKhoan' object has no attribute 'nap'`. Hình trực giác ghi “chỉ 2 cửa: nap(x), rut(x)”, còn quiz ghi “nạp 30 \| 30 > 0”. Vậy mã cho kết quả khác với điều bài nói | Thêm 2 dòng `def nap(self, x): if x <= 0: raise ValueError(...)` / `self._so_du += x` vào khung mã | CONFIRMED (đã chạy) |
| SEP L01 | SHOULD | recap step0; pitfalls step0 (bảng Lỗi 1) | “$c$ lớn hơn $N$ thì phần lớn người lộ”; “58 400 > 10 000 → phần lớn duy nhất” | Theo công thức của chính bài, khả năng duy nhất là $(1-1/c)^{N-1} \approx e^{-N/c}$. Khi $c = N$: 0,368; khi $c = 1{,}2N$: 0,435, tức vẫn chưa quá nửa. Phải có $c > N/\ln 2 \approx 1{,}44N$ thì mới quá 50%. Như vậy quy tắc tuyệt đối “c > N ⇒ phần lớn” là sai trong khoảng $N < c < 1{,}44N$ (ví dụ của bài, c ≈ 5,8N, thì vẫn đúng) | Sửa thành “c gấp vài lần N thì phần lớn người lộ”, hoặc nêu ngưỡng ≈ 1,5N | CONFIRMED (tính lại) |
| SEC L15 | SHOULD | quiz step1 (bảng câu 1) | “giữ mua chứng chỉ 1 năm \| quen quy trình \| 20 lần làm tay mỗi năm” | Phương án này đã lỗi thời so với ngày dựng bài (11/2026). Theo phiếu SC-081 của CA/Browser Forum, chứng chỉ TLS công khai cấp từ 15/3/2026 chỉ được hiệu lực tối đa 200 ngày, giảm còn 100 ngày từ 3/2027 và 47 ngày từ 3/2029. Do đó không còn mua được chứng chỉ 1 năm. `sources_L15.md` không có nguồn này | Đổi thành “chứng chỉ trả phí tối đa 200 ngày (từ 3/2026)”, kèm một dòng về lịch 200 → 100 → 47 ngày | PLAUSIBLE (theo hiểu biết về SC-081, chưa có nguồn trong kho) |
| RLN L12 | SHOULD | prereq step0 | “Ví dụ 0,5 / 0,5 → 0,6 / 0,4 cho đúng 0,4” | Cả màn hình lẫn lời đọc đều thiếu lợi nhuận của hai hành động (2 và −2), hai số này chỉ có trong `checks`. Người học không thể tự ra 0,4. Phép tính đúng: 0,5·(0,6/0,5)·2 + 0,5·(0,4/0,5)·(−2) = 1,2 − 0,8 = 0,4 | Ghi lợi nhuận 2 và −2 lên màn hình, kèm phép tính từng bước | CONFIRMED |
| WEB L11 | SHOULD | recap step0 | “nhãn, ngữ nghĩa, văn bản thay thế” | Tìm trong toàn bộ yaml thì “ngữ nghĩa” và “văn bản thay thế” chỉ xuất hiện ở phần tổng kết. Phần tổng kết nêu hai điều mà bài không dạy | Bỏ hai cụm này, hoặc thêm một bước về `alt` của ảnh | CONFIRMED (grep) |
| RBM L17 | SHOULD | quiz step0–1 | “vi điều khiển chỉ có số thực 32 bit (24 bit phần định trị)… Tỉ số phương sai… còn dưới $2^{24}$ khoảng 17 lần” | Chặng 3 giải thích quy tắc “so tỉ số với $2^{24}$” bằng số phẩy tĩnh: “một thang chung… 0,01 nhỏ hơn một nấc, thành 0”. Quiz lại áp quy tắc đó cho số thực dấu phẩy động. Số dấu phẩy động có số mũ riêng nên 0,0004 không bị làm tròn về 0. Với số dấu phẩy động, lý do đúng là mất chữ số khi trừ (số điều kiện của **P** so với 1/ε ≈ $2^{24}$). Các con số (10⁶, 16,8) đều đúng, nhưng cơ chế giải thích không áp được, nên thiếu điều kiện áp dụng | Thêm một câu: với số thực dấu phẩy động, lý do là mất chữ số khi trừ, không phải nấc thang | PLAUSIBLE |
| ROB L12 | — | | | không phát hiện lỗi | | |
| SAR L06 | — | | | không phát hiện lỗi | | |
| SWF L06 | — | | | không phát hiện lỗi | | |
| TOC L08 | — | | | không phát hiện lỗi | | |

Ghi chú nguồn đã đối chiếu, tất cả khớp: RBM với `sources_L17.md` (8 người, IBM 704, (KH)P, bản ghi nhớ Honeywell 8/7/1964, phép thử 3σ, CV-340 44 000 lb, 3 phép đo / 7 máy kinh vĩ, đàn gia súc ở Pháp). RLN với `sources_L12.md` (“a couple months”, [0,52; 1,74], giá trị lớn thứ năm, 18%, 22 triệu trang / 5 tuần). SEC với `sources_L15.md` (24–55%, 10% / 14%, 55–70% → 72–95%, 178 USD, 20%, 64/19/16%, 2,9%). SEP với `sources_L01.md` (87% = 216/248 triệu, 365 000 / 54 805, Luật 91/2025 Điều 2, 3, 9, 12). Mốc Let's Encrypt 13/5/2026, 10/2/2027, 16/2/2028 khớp thông báo [L25] mà bài trích.

## 2. Độ sâu cho người mất gốc

| Bài | Phút (từ chapters/srt) | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | Mất gốc | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RBM L17 | 18,5 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | P1: dùng mà không giảng “phần dư” (then chốt cho phép thử 3σ và quiz câu 2), “bình phương tối thiểu có trọng số” (stage1), “trị riêng âm” (stage2, stage3), “điều kiện số” (stage4, box kết luận), “hiệp phương sai” (prereq) |
| RLN L12 | 9,9 | 1 | 1 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | P1: “phương sai” (có trong tựa và mục tiêu, không giảng), ký hiệu $\pi(a \mid s)$ (s, “\|” không giảng). P2: prereq step0 thiếu lợi nhuận nên nhảy cóc ra 0,4. P7: mục tiêu 3 “giải thích bằng số… phương sai bùng nổ”, bài chỉ cho 2¹⁰ = 1024 và xác suất 0,62, không có con số độ dao động nào |
| ROB L12 | 9,4 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 12 | ĐỦ | P1: “bộ giám sát”, “bộ lập kế hoạch”, “vùng bảo vệ của cảm biến an toàn” (pitfalls step1) không giảng. P7: mục tiêu 3 “khoảng cách mô phỏng – thực tế” chỉ có một đoạn ở Lỗi 1, không có số, không có ví dụ ngẫu nhiên hoá tham số |
| SAR L06 | 8,7 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | P1: “máy chủ ứng dụng”, “cơ sở dữ liệu”, “bộ nhớ đệm” (pitfalls step3) không giảng |
| SDP L02 | 6,9 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | P1: “trường” (hook, sym), “thuộc tính”/`@property`, `raise ValueError` (example step0), “luồng”, “khoá” (pitfalls step3) không giảng. Thêm lỗi mã thiếu `nap` (bảng 1) |
| SEC L15 | 12,6 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 12 | ĐỦ | P1: “nhịp tim” (stage1), “giữ kết quả xác minh tên miền”, “gợi ý gia hạn của tổ chức cấp” (stage4, quiz) không giảng. P3: không có hình cho cơ chế đọc quá biên của Heartbleed, chỉ có bảng; trục thời gian (00017.png) chỉ minh hoạ |
| SEP L01 | 10,5 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 12 | ĐỦ | P1: “mã hoá”, “khoá” (Lỗi 2) không giảng. P3: lỗi hiển thị nhỏ, dòng “Bước 1” in hai lần (00044.png). Thêm quy tắc “c > N” chưa chính xác (bảng 1) |
| SWF L06 | 6,0 | 1 | 2 | 1 | 2 | 2 | 1 | 1 | 10 | GẦN | P1: “đặc tả”, “phản ví dụ” không giảng. P3: hình “máy sinh → trọng tài” (00017.png) chỉ là các hộp chung chung. P6/P7: tựa bài là “kiểm thử ngẫu nhiên” nhưng ví dụ là duyệt hết 121 danh sách. Không có lần sinh ngẫu nhiên nào, không giảng thu nhỏ phản ví dụ (cốt lõi của mục tiêu “tìm phản ví dụ nhỏ nhất” khi sinh ngẫu nhiên), không có công cụ thật |
| TOC L08 | 7,9 | 0 | 2 | 2 | 2 | 2 | 1 | 2 | 11 | GẦN | P1: “văn phạm phi ngữ cảnh” (khái niệm then chốt của mục tiêu 3), “đơn định / không đơn định”, “bổ đề bơm”, “dựng tập con”, “bộ phân tích cú pháp” không giảng tại chỗ. P6: định lý PDA ⇄ văn phạm chỉ được phát biểu, không có ví dụ $S \to 0S1 \mid \varepsilon$; chuỗi đối xứng chỉ được nêu, không chạy thử |
| WEB L11 | 8,6 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 12 | ĐỦ | P1: “tiêu điểm”, `<label for>`/`id` (pitfalls step1–2) không giảng. P7: mục tiêu 2 “kiểm tra dùng được bằng bàn phím” và chữ “trình đọc màn hình” trong tựa chỉ có một đoạn lỗi mỗi thứ, không có ví dụ làm tay. Phần tổng kết nêu điều chưa dạy |

Phân bố: ĐỦ 5 (ROB, SAR, SEC, SEP, WEB), GẦN 5 (RBM, RLN, SDP, SWF, TOC), CHƯA 0.

## 3. Khung hình đã xem
- RBM L17: 00003 (mở đầu), 00026 (cơ chế), 00087 (chặng 3, bảng 24 bit), 00127 + 00137 (quiz), 00145 (tổng kết)
- RLN L12: 00001, 00023 (hình cột trọng số), 00033 (2¹⁰), 00070 (đáp án quiz), 00077 (tổng kết)
- ROB L12: 00001, 00019 (đường cong quãng dừng; vị trí các điểm khớp 1,425 / 5,1 / 2,26), 00030, 00066 (quiz), 00072 (tổng kết)
- SAR L06: 00001, 00021 (sơ đồ ba tầng), 00032, 00070 (quiz), 00076 (tổng kết)
- SDP L02: 00001, 00023 (khung mã, thiếu `nap`), 00031, 00053 (quiz), 00063 (tổng kết)
- SEC L15: 00001, 00017 (trục thời gian), 00026 (64 KB / 754 ngày), 00083 (quiz), 00098 (tổng kết)
- SEP L01: 00001, 00031 (nối hai bảng), 00044 (dòng “Bước 1” lặp), 00073 (quiz), 00087 (tổng kết, “c lớn hơn N…”)
- SWF L06: 00001, 00017 (sơ đồ), 00024 (bảng duyệt), 00047 (quiz, có nhãn dừng video), 00054 (tổng kết)
- TOC L08: 00001, 00024 (ngăn xếp cao / thấp), 00030 (vết), 00062 (quiz), 00071 (tổng kết)
- WEB L11: 00001, 00021 (trục tương phản, màu thật), 00029 (độ chói), 00056 (quiz), 00068 (tổng kết)

Không thấy chữ tràn, đè nhau hay bị cắt. Cỡ chữ đọc được ở mọi khung đã xem.

## 4. Mã đã chạy / số đã tính lại
- Đã tính lại bằng Python khoảng 175 con số hiện trên màn hình hoặc được đọc ra; tất cả khớp tới đúng số chữ số được ghi. Gồm: RBM ~45 (K = 0,6 / 0,75; 0,0099; điểm dừng 0,370 / 0,27; Joseph 0,85; 252 / 72 phép nhân; 5050; 8,96; √0,8 = 0,894; 2²⁴; 0,0596; 5,96·10⁻⁵; > 1600 nấc; 44 000 lb ≈ 20 t; 10⁶ / 10⁸; 16,8; ngưỡng 12 / 6), RLN ~20 (số mẫu hiệu dụng 1,07 / 1,23 / 3,03; 0,111; 0,9¹⁰ = 0,35; 1−(1−1/1024)¹⁰⁰⁰ = 0,62; 1,5⁶ = 11,39), ROB ~20 (1,425; 5,1; 3,58; 2,26; 1,81; 2,55; 1,875; quiz 2,0 / 3 / 1,81 / 2,05), SAR ~20 (517,5; 90,7; 95%; 99,49%; 99,9998%; 0,086 phút), SEC ~20 (65 536; 754 ngày; 8,6%; 2,41; 11,6/s; 42,7; 3560), SEP ~15 (0,8426; 8426; 0,0055; 0,918; e^(−0,171); 0,892; 417; 0,366), WEB ~12 (7 tỉ số tương phản bằng hàm WCAG tôi tự viết: 4,48 / 4,54 / 2,14 / 5,57 / 4,12 / 6,58 / 9,81; L = 0,1845 / 0,1812; ngưỡng 0,1833), SWF/TOC ~10.
- Mã đã chạy:
  - SDP: chạy lớp `TaiKhoan` đúng như trên màn hình. `rut(150)` báo lỗi và số dư giữ 100 (khớp). `nap` không tồn tại (lỗi ở bảng 1). Tự duyệt độc lập 81 dãy 4 thao tác: 61/81 dãy âm với lớp lộ trường, số dư nhỏ nhất 0 với lớp đóng gói (khớp).
  - SWF: tự duyệt 121 danh sách. Phản ví dụ [0, 0], [1], [0] khớp bài.
  - TOC: tự viết máy đẩy xuống, chạy 8191 chuỗi: nhận đúng 0ⁿ1ⁿ. `00111` dừng ở ký hiệu thứ 5, `0101` dừng ở ký hiệu thứ 3 (khớp).
  - SEC: đếm ngày bằng `datetime` cho kết quả 754 ngày.

## 5. Nhận xét chung
- Mạnh: số liệu rất sạch. Khoảng 175 số tính lại không lệch số nào. Mỗi bài đều có cảnh “tự kiểm theo đường khác” (ghép cặp, liệt kê trạng thái, tính ngược) và quiz có dừng 12–20 giây, lời giải từng bước, thường là câu quyết định có đánh đổi.
- Mạnh: các bài tình huống (RBM, RLN, SEC, SEP) đối chiếu nguồn cẩn thận. Số được dán nhãn “số minh hoạ”, câu trích khớp `sources_*.md`.
- Yếu lặp lại 1, cũng là nặng nhất: P1. Các bài cuối khoá và bài giữa chuỗi dùng thuật ngữ của bài trước mà không giảng lại tại chỗ (RBM “phần dư”, “trị riêng”; TOC “văn phạm phi ngữ cảnh”, “không đơn định”; SDP “luồng”, “khoá”, “trường”; RLN “phương sai”). 3/10 bài bị 0 ở P1, 7/10 bị 1.
- Yếu lặp lại 2: mục tiêu hoặc tựa bài rộng hơn phần được dạy kỹ. Mục tiêu phụ chỉ có một đoạn ở phần “lỗi hay gặp”, không có ví dụ làm tay: ROB (mô phỏng – thực tế), WEB (bàn phím, trình đọc màn hình), SWF (sinh ngẫu nhiên, thu nhỏ), RLN (phương sai).
- Yếu lặp lại 3: phần tổng kết hoặc quy tắc rút gọn phát biểu mạnh hơn điều bài chứng minh (SEP “c > N thì phần lớn lộ”; WEB tổng kết nêu “ngữ nghĩa, văn bản thay thế” chưa dạy).
- Yếu nhỏ: hình cơ chế đôi khi chỉ là sơ đồ hộp chung chung hoặc trục thời gian (SWF, SEC). Nơi cần nhất, như Heartbleed đọc quá biên, lại không có hình.
- Mã trên màn hình cần được chạy nguyên văn, không chỉ kiểm qua `alg.*`: SDP qua mọi `checks` vì hàm kiểm tra dùng `alg.Account`, trong khi lớp hiển thị thiếu `nap`.
