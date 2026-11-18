# fix8_ACB_X — vòng 8, L03 L04 L07 L08 (2026-11-17)

Bài đổi (requeue): L03, L04, L07, L08. Không đụng curriculum, sổ screen_code, lexicon.

- L03: bỏ phiên âm "cây-x-cu-l-đê-bê" khỏi mọi `say` (13 chỗ, gồm asr_reviewed) và viết "ksqlDB"; lexicon_vi.ACB.yaml đã có luật `ksqlDB` nên lời đọc vẫn đúng, SRT hiện "ksqlDB". Lời đọc 2288. lint 0/0, render 0 vấn đề.
- L04: ô `.JSON(fiber.Map{…})` nowrap (không gãy); tiêu đề cột "bi quan: người cuối chờ" bỏ phần công thức (công thức vẫn ở ghi chú dưới bảng) nên hết gãy ở "(". Lời đọc 2296. lint 0/0, render 0, đã xem khung.
- L07: thêm bước bảng "Đọc trước: hai chỗ nữa trong mã HMAC" (JSON + `chu_ky == ky(goi)`: "dấu hai bằng liền nhau (==) so hai giá trị có bằng nhau không, trả Đúng hoặc Sai; khác dấu = đơn là gán"), bảng HMAC còn 3 hàng; bảng hai con trỏ thêm hàng `if a[i] == b[j]:` (gộp `i, j = …` với `a[i:]` để còn 4 hàng). Cắt lời ở ví dụ/sai lầm/code. Lời đọc 2297, lint 0/0, render 0.
- L08: thêm bảng "Đọc trước" 4 hàng trước mã tính hạn mức (gán nhiều giá trị, `//` chia lấy phần nguyên bỏ phần lẻ, `/` và `round`, `print`); bỏ phiên âm "xê tê ích" (lời: "Biến đầu tiên truyền vào mỗi lời gọi là gói thông tin đi kèm lời gọi đó"); ô `if err != nil {…}` nowrap, hết gãy (đã xem khung). Cắt lời để vừa 2299. lint 0/0, render 0. verify_acb.py: sửa một kiểm L08 (cụm "giờ cao điểm còn nhiều hơn" đã cắt khỏi lời; kiểm theo "trung bình có hàng trăm lượt tra CIC").

Cổng: `verify_acb.py` đủ khoá 309/310, FAIL còn lại duy nhất là "L00 có cảnh dạy … chaytep … mở Git Bash" — do L00 (ngoài phạm vi, do người chính sửa đồng thời; kiểm cần cập nhật theo câu mới của L00). `tests/test_e52.py` 0 FAIL.
Không chạy gen_sc_acb.py; screen_code cảnh `code` L07/L08 lệch thêm do chèn step (người điều phối sinh lại).
Mục chưa giảng ước còn lại: L03 0, L04 0, L07 0, L08 0.
