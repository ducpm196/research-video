# fix9_ACB — vòng r9 cuối (2026-11-17)

## Bài đổi (requeue): L00, L07. L02 KHÔNG đổi (mục tuỳ chọn 3 bỏ vì L02 đang đúng 2300 từ và để khỏi thêm bài vào hàng dựng; ô mã L02 khung 54 giữ nguyên).
- L00 pitfall: thêm câu "Spring bọc dịch vụ trong một lớp trung gian gọi là lớp bọc, lớp này mở giao dịch trước khi chạy hàm. Gọi hàm trong cùng lớp thì đi thẳng, không qua lớp bọc, nên chú thích mở giao dịch bị bỏ qua." (lời) và ô bảng "lớp bọc của Spring (lớp trung gian mở giao dịch trước khi chạy hàm)" (màn hình); bảng vẫn 3 hàng. Cắt lời ở concept (Kafka, cổng API) và vaitro để vừa trần: 2299 từ.
- L07 code: bảng "Đọc trước" mở rộng (vẫn ≤ 4 hàng/step): hàng `def ky(noi_dung)` + `print(...)` (def đặt tên hàm, return trả kết quả, print in ra màn hình; ví dụ `print(2 + 3)` in 5) và hàng `goi.replace("1000000", "9000000")` (thay đoạn chữ thứ nhất bằng đoạn thứ hai; `"a1b1".replace("1", "9")` ra `a9b9`); lời đọc tương ứng, focus theo hàng; ô `import hashlib, hmac` / `hmac.new(…).hexdigest()` / `[:12]` ngắt ở chỗ hợp lý (xem khung 57). Cắt lời bước hai con trỏ, HMAC, webhook để còn 2290 từ.
- verify_acb.py: thêm 2 kiểm (lớp bọc, bảng L07).

## Cổng
lint L00 0/0 (31 PASS), L07 0/0 (34 PASS); `lv.py render` L00 và L07 0 vấn đề (đã xem khung bảng L07); `verify_acb.py` 312/312 PASS; `tests/test_e52.py` 0 FAIL; CRLF nguyên vẹn. screen_code: không động tới khối mã; trạng thái sổ như báo cáo fix8 (STALE/MISSING/ORPHAN của cảnh `code` chờ `gen_sc_acb.py`; L07 có thể lệch thêm do chèn nội dung bảng — chỉ ảnh hưởng chỉ số step nếu step đổi, ở đây không chèn step mới).
