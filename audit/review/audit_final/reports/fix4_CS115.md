# fix4_CS115 — sửa CS115 theo R2_CS115_A và R2_CS115_B (xong, 2026-11-15)

## Tiến độ
- Hoàn tất: L11 (MUST), L45 (P8), L05 (P1), toàn bộ SHOULD, mọi bài có lab, cổng cuối (số thật ở mục 4).
- Không chạy build/tts/asr/git/docker. Đã chạy `lv.py render` (khung PNG trong out/CS115/Lxx/frames bị ghi đè bằng khung mới; video/SRT/âm thanh CHƯA dựng lại).

## 1. Bài đổi, CẦN DỰNG LẠI (25 bài)
Có đổi lời đọc hoặc hình: **L01, L05, L06, L08, L11, L16, L17, L18, L19, L20, L45, L46**.
Chỉ thêm một dòng trỏ `de.md` trên màn hình của cảnh Tự làm (lời đọc không đổi, nhưng khung hình đổi nên vẫn phải dựng lại phần hình): **L00, L02, L03, L04, L07, L09, L10, L12, L13, L14, L15, L21, L44**.
Tệp khác đổi: `labs/CS115/L01/de.md`; mới `labs/CS115/L45/{de.md,mong_doi.txt,loi_giai.py}`; `curriculum/cs115.yaml` (mục tiêu 2 của L45); `audit/verify_cs115_af2.py` (thêm kiểm L11.h, L20.q4, L45.a/b/c); `audit/review/screen_code/CS115.yaml` (sinh lại bằng gen_screen_cs115.py: thêm khối kết quả mong đợi L45). Không chạm CS112.
Đã xoá khỏi `asr_reviewed` các câu không còn tồn tại: L05 (1 mục), L08 (1 mục), L45 (cả 5 mục, vì mọi câu đã viết lại) — ASR sẽ cần chạy và người nghe duyệt lại các câu mới.

## 2. Việc đã làm theo từng mục giao
**MUST**
- L11 `convex` step 0: đường w^4 − 2w^2 vẽ lại bằng 6 cung Bezier tính từ đúng f và f' (Hermite, tiếp tuyến ngang tại w = 0, ±1), đối xứng, đáy tại w = ±1, đỉnh tròn tại 0; dây cung đỏ nối hai đáy (y = 200) nằm dưới chỗ nhô (y = 130). Đã render, xem khung 14: trơn, không còn điểm nhọn. (Gợi ý path trong brief có đáy chỉ sâu 54 điểm ảnh và dây cung cũ y = 240 nằm DƯỚI cả đường cong, nên tôi dựng lại đường chính xác thay vì dùng nguyên path gợi ý.)

**P8 (L45)**
- Thêm `af2: true`, `covers` (mục tiêu 1 → intuition, 2 → practice, 3 → stage5), cảnh `practice` (pause 360 s, kết quả mong đợi hiện trên màn hình, lệnh chấm, "Nếu kẹt"), lab `labs/CS115/L45`: ba bước Adam với gradient không đổi (g = 10 và 0,1), căn của s hiệu chỉnh, độ kéo trọng số về 0 của phạt L2 (η·λ·w/√ŝ) so với suy giảm tách rời (η·λ·w), tỉ số B chia A (100 và 1). Tất định, chỉ `import math`, in 10 dòng; `bash labs/cham.sh CS115 L45 labs/CS115/L45/loi_giai.py` → ĐÚNG; chạy cả bằng Python 3.13 (.venv) và 3.11 (labs/.venv-pyt) cho cùng đầu ra.
- Mục tiêu 2 của L45 sửa lại cho đúng điều bài dạy và lab làm (bỏ "bước trung bình của ví dụ không hội tụ" khỏi mục tiêu LÀM; phần đó vẫn dạy ở stage3), đồng bộ `curriculum/cs115.yaml`.
- Lời đọc L45 cắt từ 2877 xuống 2283 từ (≤ 2300): rút gọn mọi cảnh; bỏ bước bảng tên (chuyển thành ghi chú dưới bảng thuật ngữ), gộp hai bước bài học sai thành một (3 bài học, bỏ bài "bật biến thể mặc định" vì đã nêu ở stage5), bỏ hai hàng ở cảnh tự kiểm (0,632 và 0,905; còn 632 ngày và −0,35). Sửa nhất quán: cột "tách rời" của chặng 2 nay là η·λ·w (10⁻⁷) cùng thang với cột phạt L2 (trước đó thiếu η nên hai cột khác thang).

**P1**
- L05: bỏ nhắc "ma trận S" treo; thay bằng ví dụ ngay tại chỗ (ma trận [[1,2],[2,4]] nhân (2, −1) ra vector không; định thức 0) ở `meaning` step 0 và `derive` step 3.
- L45: "động lượng" định nghĩa tại chỗ ở stage2 (bước đi theo trung bình trượt của các gradient trước, như viên bi lăn có đà); dấu nón = đã hiệu chỉnh độ lệch (prereq); đọc ŝ là "s hiệu chỉnh" (không còn "s mũ" lẫn với lũy thừa).
- L11: "dày đặc" giảng ngay (Hessian gần hết ô khác 0); "TB" ghi kèm "8 000 tỉ byte" trên màn hình, lời đọc không đọc chữ viết tắt; gradient liên hợp: thêm công thức độ dài bước t = g·g/(gᵀAg) = 2504/125008 (cho ra đúng 7500/7813, −12/7813) và định nghĩa "liên hợp" (d1ᵀ A d2 = 0), tách thành hai step (clear) để không tràn.
- L17: ŷ/θ̂ "dấu nón = ước lượng" giảng ở mle step 0; đọc "ước lượng của thê ta/muy" thay cho "thê ta mũ/muy mũ".
- L20: ŷ đọc là "xác suất dự đoán", "lũy thừa" cho số mũ ở bce step 0.
- E52 (sổ thuật ngữ): KHÔNG thêm mục `term:`. Lý do cụ thể: CS115 là khoá mặc định, `lv.registry()`/`lv.lexicon()` KHÔNG nạp `symbols.CS115.yaml` (chỉ nạp overlay cho khoá khác DEFAULT_COURSE) nên một tệp riêng sẽ không có tác dụng; thêm vào `symbols.yaml` chung sẽ làm mọi bài af2 của khoá khác dính E52 và STALE. Mọi thuật ngữ được giảng tại chỗ trong bài.

**SHOULD**
- L01: de.md mục 1 nói rõ dùng `Fraction`/`//`, in `3` chứ không phải `3.0`; slide Tự làm cũng ghi. Đã kiểm: lời giải dùng `/` bị cham.sh chấm KHÁC (c = 3.0), lời giải gốc ĐÚNG. Thêm "gốc toạ độ, tức điểm 0, 0" ở sym_vec.
- L11 alternatives: thêm quy tắc chọn độ dài bước (xem trên).
- L08: "vector riêng vuông góc" nay ghi rõ nhãn "bài này nhận không chứng minh" kèm ví dụ (1,1)·(1,−1) = 0 và "chọn được cả khi hai trị riêng bằng nhau" (prereq và eig).
- L05 quymo: "cỡ c·r^k, c là hằng số tuỳ vector xuất phát (lấy c = 1)".
- L06 quymo: ghi rõ bảng đếm là sai phân một phía D(D+1); hai phía như phần Tự làm tốn gấp đôi (cỡ 2D²), vẫn theo D².
- L46: không đổi `requires` mà sửa lời tự đủ: recap nói "sẽ học kỹ ở bài 18" kèm giải thích hồi quy/đặc trưng/trọng số; quymo nói "phạt L2, sẽ học ở bài 19"; `forward_ref: true`; `lv.py curriculum` và check_curricula_graph đều 0 lỗi.
- L19 ridge_formula: nêu rõ X (4 hàng, cột đầu toàn 1, hai cột sau là 1, 2, 3, 4) nên người học tái hiện được det = 105.
- L20: logistic[0] ranh giới "2x − 4 = 0, tức x = 2: một điểm (1 đặc trưng), đường thẳng (2), mặt phẳng"; quymo[0] "tràn số: NumPy trả vô cực, `math.exp` báo lỗi" (đã chạy kiểm cả hai; thêm check `OverflowError`).
- L16 sym_svd: U, V có các cột trực chuẩn; phép xoay/phản chiếu chỉ khi A vuông; ma trận cao 4×2 thì U chỉ có cột trực chuẩn.
- L18 quymo: ghi chú chưa kể giải hệ D×D (cỡ D³; với D = 10⁵ là 10¹⁵ < 10¹⁶) và 100 bước là giả định.
- Mọi bài có lab (L00–L21, L44, L46: 24 bài): slide Tự làm có dòng "Đề đầy đủ và quy tắc định dạng nằm trong tệp labs/CS115/Lxx/de.md — mở tệp đó ra đọc" (chỉ trên màn hình, lời đọc không đổi).
- L45: "lam-đa phẩy" (λ′) đổi ký hiệu thành λ_L2, đọc "lam-đa L hai"; "eta" đọc "ê-ta" (cách viết chữ cái Hy Lạp, lint cho phép). **Giữ "Adam" trong lời đọc/phụ đề**: lint E28 CẤM gõ phiên âm "A-đam" vào `say` (phụ đề phải hiện tên gốc, lexicon tự đổi sang "A-đam" khi gửi TTS, đã probe 6/6); do đó phụ đề vẫn có chữ Latin "Adam" — đúng quy ước, không sửa.

**Không sửa (có lý do)**
- Các ghi chú nhẹ trong cột "Chỗ thiếu chính" không nằm trong danh sách giao (L00 P6 ít "người làm nghề", L02 tính kết hợp một ví dụ, L03 link_inverse cô đọng, L09/L10 ký hiệu từng phần tử, L14 quy tắc diện tích x^k nhận sẵn): bài không có lỗi sai, ngưỡng đã đạt; ghi ở đây để vòng sau cân nhắc.
- L45 `introduces/assumes` bằng sổ `term:`: xem mục E52 ở trên.

## 3. Điểm P1/P8 dự kiến sau sửa
- MUST: 0 (hình L11 đã sửa).
- P1 = 2: L05 lên 2 (S đã bày), L45 lên 2 (động lượng đã giảng), L11 lên 2 chắc (dày đặc, TB, liên hợp đã giảng): 25/25 bài (dự kiến, chờ người đọc).
- P8 = 2: 25/25 (L45 có cảnh Tự làm + lab).

## 4. Số liệu cổng thật (chạy 2026-11-15, sau sửa)
- `lv.py lint` 25 bài đã đổi (L00–L21, L44, L45, L46): 0 FAIL, 0 WARN ở cả 25.
- `lv.py render` 25 bài: 0 vấn đề (L16, L19, L45 từng tràn sau khi thêm nội dung, đã tách bằng `clear: true`).
- Lời đọc (từ, đếm theo khoảng trắng): tất cả ≤ 2300 (L01 2298, L02 2300, L05 2293, L06 2300, L11 2221, L45 2283, L46 1616).
- `audit/verify_cs115_af2.py`: 184 PASS, 0 FAIL (có L11.h, L20.q4, L45.a/b/c; L08.q3 là phép đo thời gian, một lần chạy đầu bị nhiễu 4,9 ms > 3,8 ms, các lần sau PASS — nhận xét: nên nới kiểm này).
- `audit/verify_cs115_l44.py` 16 PASS; `verify_cs115_tex.py` PASS.
- `audit/review/lab_gate.py CS115`: 25 PASS · 0 FAIL (196 lab được bài tham chiếu).
- `screen_code.py check --course CS115`: 34 khối, PASS 59 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 (sau khi sinh lại sổ).
- `lv.py curriculum curriculum/cs115.yaml`: 47 bài, 0 lỗi. `check_curricula_graph.py`: không lỗi. `check_xref.py`: 14 lượt, 0 lỗi. `check_next_refs.py`: 550 lời hẹn, 0 lệch. `check_course_refs.py CS115`: 0 vấn đề.
- `tests/test_e52.py`: 0 FAIL. `arith_scan.py`: 245 phép, 0 FAIL.

## 5. Lưu ý cho người dựng lại
- Dựng lại 25 bài ở mục 1 (build + tts + asr); với L45 cần ASR/duyệt tai các câu mới (asr_reviewed đã xoá).
- Lời đọc L45 vẫn gõ "Adam" (lexicon → "A-đam") và "ê-ta"; "w" đọc "vê kép", "s hiệu chỉnh" thay "s mũ".
- Chưa kiểm được bằng tai người: âm thanh mọi câu mới/đổi.
- Bài học thao tác: đã lỡ chạy `sed` với dấu `\` một lần trên L45 (làm hỏng 3 dòng λ_L2), đã sửa bằng mã đổi trực tiếp chuỗi và lint lại sạch; mọi chỗ khác dùng Edit/Write.
