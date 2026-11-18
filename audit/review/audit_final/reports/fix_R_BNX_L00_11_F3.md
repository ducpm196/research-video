# F3 — sửa BNX L08, L09, L10, L11 (2026-11-14)

Cổng thật (mỗi bài): gen → lint 0 FAIL 0 WARN → render 0 vấn đề → verify_bnx PASS hết (L08 30/30, L09 23/23, L10 30/30 gồm Kafka 3.9.0 thật, L11 34/34) → gen-screen → screen_fast 0 FAIL/STALE/MISSING/ORPHAN → `lab_gate.py BNX`: 39 PASS · 0 FAIL.

Từ lời đọc (trước → sau): L08 2306 → 2284; L09 2314 → 2293; L10 2309 → 2300; L11 2478 → 2296.

## L11 (MUST-1, SHOULD-10, SHOULD-11)
- MUST-1: "thứ mười hai" → "thứ mười" (kiểm lại: 10 000 lần cộng 0,1 lệch 1,588e-10, chữ số khác 0 đầu tiên ở vị trí thập phân thứ 10; 1 000 000 lần: thứ 6). `ver/l11.py` thêm kiểm vị trí bằng vòng lặp thuần trên Fraction + kiểm lời đọc không còn "thứ mười hai".
- OUR: bỏ tuyệt đối. Ví dụ ③, lỗi 1, đáp án quiz 3, `curriculum/bnx.yaml` fix #3: "thường nhận đủ (theo mô hình), ngân hàng trung gian hoặc ngân hàng nhận vẫn có thể trừ phí, đối chiếu số báo có".
- Mục tiêu 2 (nostro) và 4 (MT → ISO 20022): thêm quiz câu 4 (Có nostro ở A, Nợ vostro ở C) và câu 5 (71A SHA ↔ ChrgBr SHAR); `ver` kiểm cả hai.
- Bảng "giải mã sáu từ": lời đọc nay đọc đủ cả sáu dòng (nostro/vostro nói bằng "tài khoản của chúng tôi / của bạn", tên gốc chỉ trên màn hình vì chưa dò ASR).
- Cắt còn ≤ 2 300 từ: bỏ cảnh lỗi 1 "float 0,1 + 0,2 / round 2,675" (FLOAT_PY) và bảng "cách lưu tiền" (một câu kết luận chuyển vào cảnh quy mô); giữ cảnh cộng 0,10 ở 3 cỡ (đo thật) và bảng phí cố định; rút gọn lời đọc nhiều chỗ. Mục tiêu 5 giữ nguyên.

## L08
- Quiz Q2/Q3: xoá câu lặp. Cảnh quy mô: ghi nhãn "đếm theo mô hình (độ dài danh sách trong mô phỏng), không đo thời gian/đọc ghi đĩa, chưa tính công dựng chỉ mục"; đổi "đo thật" → "đếm theo mô hình" ở tiêu đề cảnh, bảng, lời đọc, tiêu đề khung. Hàm băm: "băm minh hoạ (CRC32); hàm băm thật của Elasticsearch là murmur3".

## L09
- n(n+1)/2 ghi rõ "trường hợp xấu nhất: n tiến trình đồng bộ, thử lại ngay, không lùi" (màn hình + lời đọc; nhãn "đếm trong mô phỏng"); thêm hàng "phép tăng liền một bước (counter) của kho" vào bảng chọn cách. Kết luận quiz 3: khoá bi quan chỉ khi phải kiểm điều kiện rồi mới ghi; chỉ cộng dồn một số thì phép tăng liền một bước tốt hơn cả hai. Không dùng chữ "nguyên tử" (E52: `bnx_nguyen_tu` do L20 giảng).

## L10
- "Kafka 3.9.0 thật": hiện LỆNH lặp lại được (3 khối: dựng + tạo chủ đề; ghi 8 bản ghi + bia mộ; đọc lại in offset), ghi ở `KAFKA_*_CMD` trong `src/l10.py`; `ver/l10.py` nay lấy mọi cờ/bản ghi TỪ chính các hằng đó (shlex) rồi chạy Kafka thật và so từng dòng với KAFKA_OUT (PASS, bộ dọn chạy sau ~10 s). Sổ screen: 3 khối `other` có `read_check` (cổng screen_code không chạy Docker).
- `backward_ok`: nhãn "hàm đồ chơi, không phải Schema Registry (kho thật còn kiểm đổi kiểu, xoá trường)". `compact()`: nhãn "mô hình sau thời gian giữ bia mộ; Kafka thật còn giữ bia mộ ngay sau lần nén".

## Không làm / ghi chú
- RabbitMQ (queue/binding/ack cơ bản) không thêm: ngoài danh mục SHOULD, bài đã sát 2 300 từ.
- Không dựng lại video: khung PNG đã xem L08 (quymo), L09 (bảng chọn cách), L10 (3 khung lệnh Kafka), L11 (quiz 3, quymo).
- Lỗi cách dùng `\n` qua heredoc Bash làm hỏng chuỗi khi sửa tệp: mọi sửa có `\` đều làm bằng Edit.
