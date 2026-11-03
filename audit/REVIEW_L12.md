# Bài L12 “Hàm mũ eˣ & lôgarit: tính chất và đạo hàm” — 2026-10-25

Phạm vi (yêu cầu người dùng): “Dựa vào skill và source code và những gì đã có, tiếp tục làm video bài giảng tiếp theo.”
Nhãn: OBSERVED = chạy trong phiên này; CITED = nguồn ngoài có ngày truy cập; INFERRED = suy luận, chưa kiểm.

## 1. Nút thắt hợp đồng

| ID | Chưa xác định / chưa kiểm | Việc phụ thuộc | Bằng chứng | Trạng thái |
|---|---|---|---|---|
| B20 | Cách đọc “logarit” | Lời đọc L12 (39 câu), L14, L17, L20 | Probe §2; ASR toàn bài §3 | **PARTIAL**: ASR-checked 32–33/39; 6 câu cả hai mô hình chép “logatrix” → cần người nghe |
| B40 | Tài liệu viết lẫn log / ln, exp / e^ | L12 và các bài sau | Luật nhất quán mới trong `symbols.yaml` + 3 ca test | CLOSED |
| B26, B32 | Momentum, epsilon; Adagrad, RMSprop | L09–L10 | L12 không đọc các từ này (Lỗi 2 nói “một số rất nhỏ”, không đọc epsilon) | OPEN (không đổi) |

## 2. Phát âm “logarit” (OBSERVED 2026-10-25T00:10:53Z, `scratchpad/l12_probe.py`; 4 ngữ cảnh × small + medium; ngưỡng 7/8)

| Cách viết | Đúng | Ghi chú |
|---|---|---|
| lôgarit | 3/8 | medium 3/4 (“logarithm”, “Logarit”, “logarit”); small 0/4 |
| lo-ga-rít | 2/8 | |
| lô-ga-dít | 0/8 | |
| lốc-ga-rít | 0/8 | |
| Logarithm | 0/8 | |
| đối chứng âm “lô-ga-ních” | 0/8 | |

Lượt probe L00 trước đó (2026-10-24, CITED `audit/REVIEW_L00.md` §3): tốt nhất 4/8.

Quyết định: dùng chính tả SGK “lôgarit”. Nguồn (CITED, WebSearch 2026-10-25, no revision given): giáo án Toán 11 của bộ Chân trời sáng tạo, Cánh diều và Kết nối tri thức trên hoatieu.vn, sách bài tập trên loigiaihay.com. Áp dụng:

- lexicon `logarit → lôgarit`;
- bí danh ASR chỉ cho các cách viết đúng (`logarit`, `logarith`, `logarithm`);
- `foreign_ok` thêm `lôgarit` sau khi có ASR toàn bài.

Quyết định này giống cách đã làm với “Newton” (probe 3/6, sau đó toàn bài 12/12).

## 3. ASR (OBSERVED)

- Lượt 1 (00:3xZ): 102 câu, TB 0,934, **13 cờ**.
  - 5 câu ngắn bị nghe sai thật: “Ôn lại lũy thừa.”, “Một, nó luôn dương.”, “Hai, nó luôn tăng.”, “Gọi p là xác suất ra ngửa.”, “Kiểm bằng bảng số.”. Đã viết lại cả 5 câu cho dài hơn, có ngữ cảnh.
  - Câu “giữ nguyên … chia x” cũng được viết lại.
- Lượt 2 (00:42:12Z): TB 0,951, 8 cờ.
  - 5 cờ có “lôgarit” (B20).
  - 3 cờ do tên chữ cái (p → b; e → em; “mũ x” chép dính thành “mũi”).
  - Cả 8 đã ghi vào `asr_reviewed` kèm lý do. **0 câu chưa xem xét.**
- “lôgarit” trên toàn bài (sau lần dựng lại): 39 câu. small chép đúng 32, medium 33, cả hai cùng sai 6.

## 4. Nguồn và sửa nguồn

- Tài liệu môn học dùng mà không dạy:
  - dòng 300–301: `\exp`;
  - dòng 311, 314, 348: `\log`;
  - dòng 325, 327: `\ln`.
- Bài giảng có hai step `notation_note`: exp(·) = e^(·), và “log không ghi cơ số trong học máy là ln”. `np.log` là ln (INFERRED theo tài liệu numpy; không chạy trong bài).
- Bổ sung so với `fix` của curriculum:
  - ln biến tích thành tổng: có chứng minh bằng quy tắc cộng số mũ, kèm số kiểm.
  - ln chỉ xác định với số dương: có ở cảnh đồ thị và Lỗi 2.
  - Lý do dùng log-likelihood: ví dụ đồng xu và cảnh hook về tràn số dưới.

## 5. Thiết kế và kiểm toán học (OBSERVED, 42 check trong đặc tả)

- Hook:
  - Python cho `0.1**400 == 0.0`.
  - 400·ln 0,1 = −921,03.
  - Số dương nhỏ nhất kiểu float64 là 5·10⁻³²⁴, tức 323 chữ số 0 sau dấu phẩy. **Sửa bản nháp**: bản nháp ghi “cỡ 10⁻³⁰⁸”, nhưng đó là số chuẩn nhỏ nhất. Bản nháp cũng dùng số mũ âm trước khi bài dạy.
- Lãi kép (1 + 1/n)ⁿ: 2; 2,25; 2,6130; 2,7146; 2,71828.
- Đạo hàm:
  - (eʰ − 1)/h: 1,0517 → 1,0005.
  - Cơ số 2: 0,7177 → 0,6934 ≈ ln 2.
  - (ln x)′ = 1/x suy từ e^{ln x} = x bằng quy tắc chuỗi bài 7. Không dùng quy tắc lũy thừa xⁿ, vì bài 6 chỉ dạy hằng số, x, x².
- Đồng xu (3 ngửa, 1 sấp):
  - Đạo hàm của ln L cho p = 3/4 (sympy).
  - Bảng L: 0,1029 / **0,1055** / 0,1024.
  - Bảng ln L: −2,274 / **−2,249** / −2,279.
- Đối chứng âm (OBSERVED): đổi số kỳ vọng ở 5 check (đạo hàm, nghiệm đồng xu, bảng L, quiz, hook) thì cả 5 check thành FAIL.
- Luật mới: `consistency` “Lôgarit tự nhiên” (`\ln` / `\log`) và “Hàm mũ cơ số e” (`e^` / `\exp`). Test kèm theo:
  - bắt lỗi khi chèn `\log` hoặc `\exp` ngoài `notation_note`;
  - không báo lỗi với L12 gốc (`tests/test_lint.py`).
- Xem bằng mắt các khung:
  - khung 2, 4 (hook), 9, 10 (ôn nền), 13 (bảng e), 29 (SVG hai đồ thị), 41 (notation_note), 47 và 52 (đạo hàm), 56 (hàm lồng), 67 (bảng đồng xu), 79 (pitfall), 92 (đáp án quiz).
  - Lỗi bắt bằng mắt đã sửa:
    - quy tắc ② hiện trước câu đọc nó;
    - ô kiểm đạo hàm ln bị lặp hai lần;
    - ký hiệu e^{…} rời rạc.

## 6. Kiểm toàn bộ

Xem bảng chạy cuối của `final_check.sh` (báo cáo trong chat).
L12: `out/L12/L12.mp4` 602,5 s (10,0 phút), verify PASS, lint 0 FAIL / 0 WARN, ASR 0 câu chưa xem xét.

## 7. Còn mở (NOT_VERIFIED)

- Người nghe:
  - “lôgarit” (B20, 6/39 câu cả hai mô hình nghe sai) và 8 câu trong `asr_reviewed`;
  - các mục cũ: “Niu-tơn”, B26, B32, L01 (8), L02 (8), L04 (1), L05 (4).
- Trước L13: tên “Bayes” chưa probe (L12 chỉ ghi trên màn hình, không đọc).
- ICA còn thiếu số tập/trang. L01, L02 dài hơn 15 phút. Hiệu quả sư phạm chưa đo.
