# fix6 CS115 L00–L11 (sửa theo R4_CS115_A, chuẩn P1 chặt) — 2026-11-16

Tiến độ: L00–L11 xong (12/12). Không chạy build/tts/asr/git/docker. `tools/lv.py render` chạy được (không bị từ chối) cho cả 12 bài: 0 vấn đề.

## Cách làm
- Gốc P1 hệ thống (cảnh `practice` bắt viết `<tên>.py` mà video không dạy): MỖI bài thêm TRƯỚC step "Đề" hai step "đọc trước", step "Đề" có `clear: true`:
  1. Bảng 3 hàng "đọc trước: việc | làm thế nào | gõ trong Git Bash": tạo tệp `.py` (trình soạn văn bản, lưu ở thư mục gốc bộ khoá có `labs`), chạy `python <tên>.py` (Git Bash), chấm `bash labs/cham.sh CS115 Lxx <tên>.py` (in ĐÚNG khi mọi dòng trùng). Lặp lại một dòng ở mỗi bài (tên tệp/mã bài đúng của bài đó).
  2. Bảng ≤ 4 hàng "đọc trước: viết trong mã | đọc là | ví dụ", đúng các mẩu mã/ký hiệu của bài đó: `for…in`, gán, `**`, `print`, `Fraction`, `def`/tham số/`return`, danh sách và danh sách lồng + chỉ số, gán nhiều biến, `//`, `math.gcd`, `math.isqrt`, biệt thức (L05), `zip`, `range`, `round`, `math.sqrt`, `abs`, `1e-8`, f-string, `if … and`, `!=`, danh sách mới từ danh sách cũ… Mỗi hàng có một câu `say` và `focus` (lời đọc không nói tên từ khoá/tên hàm: tả bằng tiếng Việt, tên thật chỉ nằm trên bảng).
  - Chân trang chấm bài: lời đọc rút còn 2 câu (đã giảng ở bước 1).
- Mọi ví dụ trong bảng đã tính lại bằng Python (gcd, isqrt, `//`, Fraction, round, 5.2, [0.2, 0.4]…): khớp.
- Dùng sổ chung (`symbols.yaml`, `lexicon_vi.yaml`) KHÔNG đổi (CS115 dùng sổ mặc định, không có `symbols.CS115.yaml`).
- `asr_reviewed`: kiểm bằng script đọc (so từng câu `say`): 12/12 bài, 0 mục bị mất (đã hoàn nguyên các sửa chạm vào câu có trong `asr_reviewed` ở L04, L05).
- Lời đọc ≤ 2300 từ mỗi bài (cắt ý ít giá trị: bước nhắc lại, câu giảng lặp, câu kết nhẹ; không cắt quiz/quy mô/Tự làm; L00 bỏ 1 lỗi trùng "đổi thứ tự", tiêu đề "3 lỗi").

## Theo bài (đã đổi, số mục chưa giảng ước còn lại)
| Bài | Bảng đọc mã (hàng) | Thuật ngữ / SHOULD / P2/P3/P7 | Từ | Chưa giảng ước |
|---|---|---|---|---|
| L00 | for…in; gán + `**`; print; Fraction | in_ai_map: chú thích "hàm mũ", "lôgarit", "xác suất", "mạng nơ-ron", "nén dữ liệu", "Adam"; check step 3 tách 2 câu (đáy nằm giữa vì dạng bát; lớn hơn 0 vì không có w chung) | 2289 | 0 |
| L01 | def/tham số/return; danh sách + chỉ số; Fraction; `//` và `/` | y thường (một số) khác **y** in đậm (cả danh sách), cả trên màn hình; dời nhãn "bóng" khỏi mũi tên; bỏ step "thứ tự" | 2300 | 0 |
| L02 | def; danh sách lồng; Fraction/str; `!=` | recap: thêm "(XᵀX)⁻¹ chỉ có khi XᵀX khả nghịch" (lời + chip); "byte" định nghĩa trên màn hình ở quymo | 2297 | 0 |
| L03 | danh sách lồng; gán hai biến (đổi chỗ); range; Fraction | "đặc trưng" định nghĩa ở hook; "⟹ = suy ra" ở prereq (gộp "vì sao khác 0"); bỏ step cỡ ma trận mở rộng | 2297 | 0 |
| L04 | gán nhiều biến; def; zip; Fraction | "ℝ², ℝ³" định nghĩa (lời + màn hình); "⟹" nhắc ở prereq | 2298 | 0 |
| L05 | gán nhiều biến; gcd; biệt thức delta; isqrt + `//` | thêm ô quy ước "(a,b)ᵀ = vector cột", "với số thực", "⟹"; quymo: thêm điều kiện "trị riêng trội và vector xuất phát có thành phần theo hướng đó" (lời + màn hình); đổi tiêu đề verify ("…và vector riêng có vuông góc không?" bỏ); giáo án `fix` A1 cần nhắc phân cảnh `in_ai` không có: ý dạy ở L08, xem "lưu ý" | 2289 | 0 |
| L06 | def; số thập phân + `/`; round; sqrt | "trơn (khả vi)" = đường cong không gãy khúc, có đạo hàm (lời + màn hình) | 2296 | 0 |
| L07 | def trả danh sách; danh sách lồng; for/range; round | "mạng nơ-ron", "lớp" định nghĩa ở hook; "⟹" nhắc ở prereq | 2299 | 0 |
| L08 | gán nhiều biến; if/elif; Fraction; print | "⟹" nhắc (step clear riêng); "byte" định nghĩa; **Sylvester 3 biến**: nói rõ là định lý chỉ nêu và kiểm bằng ví dụ, không chứng minh (lời + ghi chú màn hình) | 2297 | 0 |
| L09 | for/append; gán dùng giá trị cũ; abs; `//` | dời nhãn w₁, w₂ khỏi mũi tên (đã xem khung render) | 2294 | 0 |
| L10 | sqrt; `1e-8`; `G = G + g**2`; f-string + round | quymo "m và s" (không phải v); "byte" định nghĩa; "dữ liệu thưa" định nghĩa (lời + màn hình); "tham số" → "con số" ở lỗi 2 | 2277 | 0 |
| L11 | danh sách lồng; danh sách mới từ danh sách cũ; Fraction; gradient A w − b | **P2**: suy ra t = gᵀg/gᵀAg (khai triển f(w − t g), đạo hàm theo t = 0) và Levenberg–Marquardt (r(w+d) ≈ r + J d, đạo hàm nửa tổng bình phương + ½c‖d‖² cho (JᵀJ + cI) d = −Jᵀr), cả lời và màn hình; sửa câu sai "đoạn đi xa nhất" → "làm f thấp nhất dọc hướng đó"; 2 kiểm mới trong `checks:` (sympy: khai triển, nghiệm t = 2504/125008, đạo hàm LM); "phương trình chuẩn" chú thích; "tham số" → "trọng số"; "⟹" chú thích ở newton_1d | 2288 | 0 |

Ước lượng: 12/12 bài còn 0 mục chưa giảng (tự đánh giá; reader chấm lại sau dựng). SHOULD đã sửa 9/9 (L05 ×3, L02, L10, L00, L01, L09, L00/L01); P2 L08, L11; P3 L01, L09; P7 L02, L05 (L05 `fix` giáo án: xem lưu ý).

## Sổ screen_code (Edit từng mục, không script)
Chèn 2 step trước "Đề" làm lệch chỉ số: đổi khoá `CS115 Lxx practice 1 0` → `practice 3 0` (L00–L02, L05–L07, L09–L11) và `practice 0 0` → `practice 2 0` + `practice 1 0` → `practice 3 0` (L03, L04, L08). sha không đổi (không khối mã nào đổi). Bảng "đọc trước" dùng `<code>` nội dòng trong `<table>` nên không là khối mã.

## Cổng (chạy thật, 2026-11-16)
- `tools/lv.py lint` L00–L11: 0 FAIL, 0 WARN (PASS: L00 48, L01 65, L02 63, L03 55, L04 68, L05 63, L06 64, L07 62, L08 62, L09 61, L10 47, L11 55).
- `tools/lv.py curriculum curriculum/cs115.yaml`: 47 bài, 0 lỗi. `tests/test_e52.py`: 0 FAIL.
- `audit/verify_cs115_af2.py` 184 PASS · 0 FAIL; `verify_cs115_tex.py` 59/59; `verify_cs115_l44.py` 16/0.
- `screen_code.py check --course CS115`: 34 khối, PASS 59 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0.
- `lab_gate.py CS115`: 25 PASS · 0 FAIL. `arith_scan.py`: 258 phép, 0 FAIL. `check_curricula_graph.py`: 0 tham chiếu hỏng, 0 chu trình, "VER của bài khác: 0".
- `tools/lv.py render` L00–L11: 0 vấn đề (L08 lần đầu TRÀN ở prereq.1 sau khi thêm ghi chú "⟹" → thêm `clear: true`, render lại 0). Đã xem khung: L00 (bảng đọc mã + focus hàng), L09 (hình gd_pic: nhãn w₁, w₂ đã tách khỏi mũi tên).

## Lưu ý cho người điều phối
- Bài đã đổi (cần requeue, cả 12): CS115 L00, L01, L02, L03, L04, L05, L06, L07, L08, L09, L10, L11 (đều đã nằm trong `rebuild.queue`, chưa trong `done`). Lab không đổi.
- Chưa nghe/ASR lại lời mới; các câu tả ký hiệu bằng tiếng Việt ("hai dấu sao liền nhau", "chữ e trong số là mười mũ", "hàm căn nguyên") cần ASR/nghe thử. Lời đọc sát trần (L01 2300, L07 2299, L04 2298): sửa tiếp phải cắt chỗ khác.
- L05 giáo án `fix` A1 ("có trị riêng bằng 0 … phân cảnh in_ai") vẫn nhắc một phân cảnh không có trong L05: tôi KHÔNG sửa `curriculum/cs115.yaml` (tránh làm STALE); đề xuất người điều phối sửa dòng đó thành "dạy ở bài 8 (cuctri)".
- Bảng "đọc trước" lặp cùng cấu trúc ở 12 bài (bước 1 gần như giống nhau, chỉ khác tên tệp/mã bài); nếu reader coi là lặp thừa, có thể rút bước 1 thành một dòng ở bài sau L00.
