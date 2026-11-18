# fix7_ACB_A — L03, L04, L05 (vòng 7, theo R6_ACB)

Bài đã đổi (requeue): L03, L04, L05. Sổ screen_code: chỉ đổi khoá thủ công `ACB L04 example 3 0` thành `example 4 0` và `ACB L05 symbol 0 0` thành `symbol 1 0` (chèn bước làm lệch; sha không đổi). Không chạy gen_sc_acb.py.

## Thay đổi
- L03: nhắc lại "đối soát" (hai bên so sổ giao dịch xem từng khoản có khớp không) ở bước 3 của ví dụ; "luồng máy chủ" giải nghĩa (dòng việc chạy song song trong máy chủ) ở cảnh check; hàng bảng `>=` (lớn hơn hoặc bằng) ở bảng "Đọc trước" mã Python. Cắt lời hook/prereq/quymo/recap để bù.
- L04: bảng "Đọc trước" mới cho mã Go (`:=` và hai giá trị, `nil`/`err != nil`, `c.Status(fiber.StatusConflict)` kèm "Fiber là khung viết dịch vụ", `.JSON(fiber.Map{…})`) đứng trước Bước 4, bước sau có `clear: true`; "đáo hạn" (ngày kết thúc kỳ hạn) ở bảng và lời prereq; "SQL" giải nghĩa ở tiêu đề khối cập nhật; Fiber giải nghĩa ở concept.
- L05: bảng "Đọc trước" mới cho PL/SQL `FOR r IN (...) LOOP … END LOOP;` (4 hàng) đứng trước khối mã; bỏ đoạn ghi chú dài cũ (đã gộp vào bảng); bảng mới cho `so_du = 10`, `dau = []`, `for phat_sinh in …`, `dau.append(so_du)`; "phân vùng" giải nghĩa ở Bước 4; "bắt lỗi" giải nghĩa (nhận ra lỗi báo về); câu nối "mục tiêu 3 phút = 180 giây: tuần tự một triệu lệnh (5 000 giây) vượt xa, chia 100 khối còn 50 giây đạt" (trên màn hình và lời, số lấy từ bảng có sẵn).

## Cổng
| cổng | kết quả |
|---|---|
| lint L03/L04/L05 | 0 FAIL, 0 WARN (28/29/34 PASS) |
| lời đọc | L03 2288 · L04 2296 · L05 2287 |
| render 3 bài | 0 vấn đề; đã xem khung bảng Go (L04 khung 51) và bảng PL/SQL (L05 khung 30) |
| verify_acb.py (đủ cả khoá) | 306/306 PASS |
| tests/test_e52.py | 0 FAIL |
| curriculum acb, screen_code check | chạy nền chưa xong khi nộp (không đổi curriculum); các mục cảnh `code` của L03–L05 lệch tới khi sinh lại sổ |

## Mục chưa giảng ước còn lại
L03 0 · L04 0 · L05 0.

## Lưu ý
- Sự cố đã khắc phục: một lần `setsay` ghi nhầm vào bước bảng Redis của L03 (đã khôi phục từ SRT cũ, lời đọc y nguyên) và một lần mất `af2: true` ở L03 (đã trả lại). `sed -i` làm mất CRLF ở L04/L05, đã chuẩn hoá lại CRLF cho cả hai.
- Câu `say` mới chưa qua ASR; `asr_reviewed` mồ côi đã xoá.
