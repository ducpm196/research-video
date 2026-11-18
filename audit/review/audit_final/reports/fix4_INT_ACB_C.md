# fix4 ACB L00–L03 (fork C, đợt 1) — 2026-11-15

Bài đổi (CẦN DỰNG LẠI: spec_sha256 đã đổi): ACB L00, L01, L02, L03. Không đụng L04–L08, INT, curriculum (curriculum/acb.yaml không cần sửa: `lv.py curriculum` 0 lỗi).
Tiến độ: 4/4 bài xong.

## Số từ lời đọc (tổng `say`, trước → sau; trần 2300)
L00 2066 → 2227 · L01 1841 → 1917 · L02 2076 → 2225 · L03 1802 → 1947. Mọi câu ≤ 38 từ, ≤ 170 ký tự (lint 0 WARN).

## Từng bài
**L00** — P1 giảng tại chỗ (lời đọc + màn hình): giao diện lập trình/API+REST (hook), hệ thống lõi/core + T24 là phần mềm lõi của Temenos (hook), NAPAS (hook), bản tin (prereq), kết nối TCP (symbol), socket (concept), SLA (vaitro, cột bảng), Spring Boot (vaitro), gọi đồng bộ (quymo, lời + bảng), Python `print`/`if` thụt dòng (code, lời + màn hình). Hook step 0 thêm 3 câu; focus cập nhật; bảng vaitro rút gọn gloss cho khỏi tràn.
**L01** — JMS/JMSCorrelationID (prereq: cột bảng + lời), microservice + consumer (concept: ghi chú dưới sơ đồ + lời "vi dịch vụ", "bên nhận tin"), hàm/từ điển/vòng lặp/pop (code: lời + ghi chú màn hình). Bảng check thành 3 cột "hành động sai | hậu quả | cách xử lý chuẩn" (hàng 3 viết lại hành động sai thật: "Hoàn tiền ngay khi chưa tra soát"). Quiz: cân độ dài (đáp án A không còn dài nhất; nhiễu B/C/D hợp lý hơn).
**L02** — byte (hook), ràng buộc duy nhất/UNIQUE (example, lời + bảng), toán tử `|` và `<<` (code), hệ mười sáu 0111=7, 0010=2 → 72 (symbol, lời + màn hình), THÊM step giải mã (`int(x,16)`, `>>`, `& 1`) cuối cảnh code vì lab đòi giải mã `5030…` (có `checks` mới + sổ mã màn hình sinh lại). Bảng check 3 cột (hành động sai | hậu quả | chuẩn), "hạn mức 1500 mi li giây" → "ngưỡng chờ". Sơ đồ concept vẽ lại đúng thứ tự lời đọc: 1 Digital → 2 Core Banking (giữ tiền) → 3 Gateway → 4 Switch, đường vòng về Core; bỏ câu chú thích "ô vẽ ở cuối hình". Quiz cân độ dài (A là nhiễu-dài-nhất → A ngắn nhất).
**L03** — phân vùng (partition) + tiến trình (quymo: lời + ghi chú), xô thẻ có ví dụ số nhỏ (step mới ở pitfall, bảng 4 hàng, số khác lab), `import`, SELECT/CASE WHEN/ON (symbol), "(số minh hoạ)" gắn ngưỡng 50 nghìn ở hộp sơ đồ ("SMS ≥ 50k (minh hoạ)"), chú dưới sơ đồ, chú dưới SQL, và lời. Nhãn "Email sao kê định kỳ" → "Email (số tiền nhỏ)" khớp SQL. Kafka at-least-once có điều kiện ("ở cấu hình mặc định", gửi tin ra ngoài Kafka không nằm trong cam kết) ở lời + màn hình. Bảng check 3 cột. Quiz cân độ dài (A không còn dài nhất).

## Sổ thuật ngữ (chỉ thêm vào tools/registry/symbols.ACB.yaml; mục cũ và sổ chung không đổi)
Mới: acb_napas, acb_core (hook L00) · acb_tcp (symbol L00) · acb_spring (vaitro L00) · acb_jms (prereq L01) · acb_microservice, acb_consumer (concept L01) · acb_byte (hook L02) · acb_unique (example L02) · acb_partition (quymo L03).
Đã thêm `assumes` ở L01 (acb_core, acb_tcp), L02 (acb_napas, acb_tcp, acb_core), L03 (acb_microservice, acb_core).
**L04–L08 (đợt 2) cần thêm `assumes` (lint hiện FAIL, tôi KHÔNG sửa):**
- L04: acb_core · L05: acb_napas, acb_core, acb_partition · L06: acb_core, acb_napas · L07: acb_napas, acb_core, acb_unique · L08: acb_core, acb_napas, acb_unique.
(Tất cả đều nằm trong bao đóng tiên quyết: L00/L01/L02/L03 đúng như dãy.) Ngoài `assumes`, các bài này vẫn nên giảng ngắn tại chỗ nếu dùng ở chỗ khác (ví dụ L04 "HTTP 409").

## Cổng (số thật, sau khi sửa)
- `lv.py lint` L00–L03: 0 FAIL, 0 WARN (mỗi bài). `lv.py render` L00–L03: 0 vấn đề (113/97/111/100 khung).
- `audit/acb/verify_acb.py`: 262/262 PASS. `lab_gate.py ACB`: 9 PASS · 0 FAIL.
- `screen_code.py check --course ACB`: PASS 83, FAIL 0, STALE 0, MISSING 0, ORPHAN 0 (đã chạy `audit/acb/gen_sc_acb.py` để sinh lại sổ vì L02 thêm khối mã giải mã; sổ ACB.yaml phần GEN-WP4 được ghi lại, L04–L08 kiểm vẫn PASS).
- `tests/test_e52.py`: 0 FAIL. `arith_scan`: 244 phép, 0 FAIL. `lv.py curriculum curriculum/acb.yaml`: 9 bài, 0 lỗi.
- `check_course_refs.py ACB`: 0 vấn đề (chạy không đối số quét mọi khoá, chậm > 3 phút).
- Đã xem khung PNG: L00 (2, 50, 56), L01 (20, 51, 56), L02 (24, 70), L03 (20, 67): không tràn/đè.
- Lint L04–L08: mỗi bài 1–3 FAIL E52 chỉ vì thiếu `assumes` như danh sách trên (không phải lỗi nội dung).

## Mục không sửa / ghi chú
- `asr_reviewed`: đã xoá 2 mục mồ côi ở L02 (câu không còn trong bài); câu mới/đổi chưa có ASR (cần dựng + ASR lại, đúng quy trình).
- Quiz: quiz L00 không có phương án (câu mở), không đổi.
- INT, L04–L08: ngoài phạm vi.
- Không chạy build/tts/asr/git/docker. Tôi có chạy một lần `git diff --stat` (chỉ đọc) trên L02 để kiểm tra ghi tệp.
