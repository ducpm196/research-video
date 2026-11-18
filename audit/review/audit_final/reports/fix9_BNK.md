# fix9 BNK (vòng 9 theo R6_BNK) — 2026-11-17

Nguồn: `audit/bnk/lib.py` (thêm hàng JROW; `jstep` tách ví dụ khỏi lời giải bằng " — " và " | " thay cho ":" và ";" dính mã), `audit/bnk/src/l00..l11,l13,l14.py`, sinh lại bằng `gen.py`. Mọi bảng cách đọc dùng `jsteps` (tự tách ≤ 3 hàng, ≤ 520 ký tự chữ mỗi step), step sau bảng `clear: true`.

## 1. Bốn mục VỪA (bắt buộc)
- L00: hàng `Runtime rt = Runtime.getRuntime();` / `totalMemory() − freeMemory()` (đối tượng đại diện chương trình đang chạy; hiệu = bộ nhớ đang dùng), đặt trước mã RoRi.
- L01: hàng `try { Thread.sleep(cho); } catch (InterruptedException e) { }` (thử chạy; bị ngắt thì vào catch; để trống vì không cần xử lý), trước MatCapNhat; bỏ câu "dòng bắt lỗi chỉ để Java cho phép ngủ".
- L03 (check): 4 hàng SQL (`CREATE TABLE … PRIMARY KEY`, `INSERT OR IGNORE INTO … VALUES`, `SELECT COUNT(*)`, `SELECT … WHERE khoa = 'abc'`) thay hàng TEXT cũ; lời đọc cảnh check rút phần nói miệng trùng.
- L08: hàng `BEGIN; … COMMIT;`, `UPDATE … SET so_du = so_du - 500000 WHERE tk = 'A'`, `INSERT INTO outbox (su_kien) VALUES (…)`, `ROLLBACK;` (cùng `DEFAULT`, `COUNT`, `TEXT/INTEGER`, `--`), trước khối Outbox; lời đọc khối Outbox rút phần đọc lệnh trùng bảng.

## 2. Mục yếu cùng họ (làm được)
`+` nối chuỗi (hàng `concat`) ở L00, L01, L02, L03, L06, L07, L08, L11; `<= >= == !=` (L00, L07), `/` `%` chia nguyên (L07), `j--`/`>=` (L08), `Object`/`_` trong số: chưa (hết ngân sách chữ); `new HashMap<>()`/`new ArrayList<>()` (hàng `diamond`: L08, L10), `put/get/equals` + mảng khởi tạo `{…}` (L10), `if (duoc) sau.unlock();` (L05), `UNION ALL`/`AS` (L04, đọc trong hàng WITH RECURSIVE), `INSERT INTO … SELECT` (L09), `truong[2]` + `#` + nối chuỗi Python (L11), gán song song `pin, pan = …`, biểu thức sinh trong `join`, `b"k"` (L13); L14: bảng SQL tách ba step ≤ 3 hàng (hết bảng 4 hàng). Chưa làm: B-gộp Java ở bài sau, `static class`, `try/catch/finally` của L05, `Object`/`_` của L00.

## 3. SHOULD
- L06: công thức "kết nối bận = lần hỏi mỗi giây nhân không phẩy không hai" được đọc; bỏ ", ." treo. L08: câu cụt "gửi sang Kafka, ." sửa. L02: lời hook.1 "tóm tắt cảnh ví dụ, còn số giao dịch được chạy thật ở cuối bài". L05: de.md ghi đủ tiền tố đầu ra; quy_mo.0 đọc "một trăm nghìn phiên cùng tranh hai hàng là trường hợp cực đoan". L10: check.0 bỏ dòng "tự đếm tay 3 lệnh" khỏi màn hình (không đọc).
- Ô "ví dụ" tách mã khỏi lời giải (hết `tk = null;;`, `moGiaoDich++;:`). Bỏ hàng `null` ở L08 (đổi thành `diamond`) và `+=` ở L10 (hàng `inc1` chỉ `x++`).

## 4. Lời đọc (≤ 2300, đếm bằng mã)
L00 2295; L01 2294; L02 2295; L03 2295; L04 2208; L05 2300; L06 2297; L07 2286; L08 2286; L09 2217; L10 2298; L11 2297; L12 2217; L13 2299; L14 2296.

## 5. Cổng
lint 15/15: 0 FAIL, 0 WARN; verify_bnk 48/48; `screen_gen.py` rồi `screen_code check` (xem tin nhắn cuối); mọi bảng cách đọc ≤ 3 hàng/≤ 560 ký tự, step sau bảng `clear`. `lv.py render` L08: 134 khung, 0 vấn đề; các bài còn lại bị từ chối quyền ở lần gọi sau, không đi vòng (dựa quy tắc jsteps).

## 6. Requeue
L00, L01, L02, L03, L04, L05, L06, L07, L08, L09, L10, L11, L13, L14. L12 không đổi.
