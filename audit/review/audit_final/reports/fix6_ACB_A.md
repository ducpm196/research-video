# fix6_ACB_A — ACB L03, L04, L05 (fork A, 2026-11-16)

Bài đã đổi (cần requeue): L03, L04, L05. Không đụng L00–L02, L06–L08. Không chạy build/tts/asr/git/docker, không chạy gen_sc_acb.py.

## Thay đổi theo bài
**L03** (lời đọc 2297 từ): symbol: thêm step "Đọc trước" 4 hàng (SELECT…FROM, CASE WHEN…ELSE…END, AS target_channel, CREATE STREAM … AS), step ksqlDB có `clear: true`. example: step "Đọc trước" 4 hàng cho `SET noti:sent:{event_id} 1 EX 86400 NX` (SET, chỗ giữ chỗ `{event_id}`, EX, NX) trước Bước 3. code: 2 step "Đọc trước" (def/return, if + None, `for co_app, tien in […]`, print; rồi import heapq, `[]`, heappush/heappop, `while hang:`), bỏ giải thích `import` rải rác. SVG concept: "Ưu tiên mã OTP" (hết đè khung 22; render 0 vấn đề). Quiz: đáp án đúng chuyển A→D (show + say). Practice: nhắc "lưu thành tệp, chạy bằng python mau.py" + chú thích chân trang cham.sh (bash / labs/cham.sh / ACB L03 mau.py / ĐÚNG khi mọi dòng trùng) cả màn hình lẫn lời.
**L04** (2233 từ): code: 3 step "Đọc trước" (import sqlite3 + ":memory:", CREATE TABLE, INSERT INTO, SELECT + fetchone()[0]; `?`/(7,)/.rowcount/for/print; CANH = {…} (tập các cặp), def/return, `A if c else B`, print) — thay step "Cách đọc hai chỗ lạ" cũ. check: định nghĩa "đối soát" (ghi chú + một câu say) và HOLD. practice: "kỳ hạn 12 tháng" trên màn hình và trong lời; chân trang cham.sh như L03; nhắc chạy tệp. Quiz đúng A→C.
**L05** (2296 từ): code: "Đọc trước" cho mã bảng khoá (`{}`/`khoa[tk] = ai`, def/return/`+`, `if … in … and … !=`, `for ai, tk in …`), cho vòng chờ bằng từ điển (`cho["A"]`, `cho.get(…)`, `==`), cho mã sắp thứ tự (`sorted`, gán hai tên một lúc, chỉ số `[0]`, `return "duoc"`); bỏ step "Cách đọc điều kiện" và khối `cho.get` rời. symbol: `AS acc` giải thích (màn hình + lời "cột được đặt tên gọn"). P3: hình SVG vòng chờ khoá ở example Bước 1 (A giữ khoá 1 / xin khoá 2, B giữ khoá 2 / xin khoá 1, mũi tên thật `markerUnits=userSpaceOnUse`, khớp lời đọc). P2: FORALL "45 giây xuống 1 giây" thành phép tính có giả định ghi rõ "phải đo": 10 000 × 4,5 ms = 45 giây, 10 000 × 0,1 ms = 1 giây (thêm `checks`; lời đọc dùng "phẩy"). Cắt step concept bảng "ba thách thức" (trùng bảng ở hook/pitfall) và rút một số câu lời đọc để giữ ≤ 2300. Quiz đúng A→B. Practice + chân trang như trên. Xoá 5 mục asr_reviewed mồ côi (các câu đã đổi).

## Cổng thật (L03/L04/L05)
- `lv.py lint` 3/3: 0 FAIL, 0 WARN (L03 28 PASS, L04 29, L05 34).
- `lv.py render` 3/3: 0 vấn đề (L03 119 khung, L04 117, L05 123). Đã xem khung L03 22 (hết đè), 29 (bảng symbol); L04 55, 70 (bảng sqlite, bảng CANH); L05 36 (SVG vòng chờ), 42 (phép tính FORALL), 58 (bảng bảng khoá).
- `audit/acb/verify_acb.py L03 L04 L05`: 21 + 18 + 28 PASS, 0 FAIL (không cần sửa chỉ số step).
- `tests/test_e52.py`: 0 FAIL. `lv.py curriculum curriculum/acb.yaml`: 9 bài, 0 lỗi (không phải sửa curriculum: mục tiêu/`fix` của L03–L05 không đổi). `arith_scan.py`: 257 phép, 0 FAIL.
- `screen_code.py check --course ACB` (trạng thái hiện tại, toàn khoá): PASS 53, FAIL 0, STALE 10, MISSING 20, ORPHAN 20 — mọi dòng lỗi của L03–L05 đều là mục cảnh `code` do gen_sc_acb.py sinh (chỉ số step dịch: L03 code 1→3, L04 code 2→4, L05 code 0→1, 3→4…); cần chạy gen_sc_acb.py một lần. Mục thủ công: đã Edit khoá `ACB L03 symbol 0 0` → `symbol 1 0` và `twin_of: ACB L03 symbol 0 0` → `symbol 1 0` (sha không đổi, PASS); L04 symbol 0 0, L04 example 3 0, L05 symbol 0 0 không đổi khoá, PASS.
- Chưa chạy: `lab_gate.py ACB` (lab L03–L05 không đổi), check_legal, check_curricula_graph (không đổi nội dung pháp lý/đồ thị).

## Mục chưa giảng ước còn lại
L03: 0 · L04: 0 · L05: 0 (chân trang cham.sh, while, for a, b in …, CREATE TABLE/INSERT, fetchone, `a if c else b`, `.get`, sorted, return, AS, FROM, ELSE…END, `{event_id}` đều có hàng bảng hoặc câu ngay trước; "đối soát" L04 định nghĩa tại check).

## Việc còn mở
- Cần gen_sc_acb.py + check lại screen_code sau khi cả ba nhóm xong (người điều phối).
- Lời đọc mới chưa qua ASR/tai người; mục asr_reviewed của câu đã đổi bị xoá.
- L05: nhãn "B xin, phải chờ" trong SVG chạm nhẹ đường nét đứt (đọc được); nếu muốn sạch hơn dời nhãn lên 10 px.
