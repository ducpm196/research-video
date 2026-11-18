# Lab ACB L03 — Chọn kênh, hàng đợi ưu tiên và xô thẻ giới hạn tốc độ

Số liệu (số minh hoạ, khác ví dụ trong bài):
- Bốn biến động: (khách có ứng dụng, số tiền) = `(True, 15000)`, `(None, 120000)`, `(False, 49999)`, `(False, 50000)`. Luật: có ứng dụng → `OTT_PUSH`; không thì từ **50 000** trở lên → `SMS_BRANDNAME`; còn lại → `EMAIL`.
- Bốn tin đưa vào hàng đợi ưu tiên (số ưu tiên, nội dung): `(3, "khuyen mai")`, `(1, "otp 9911")`, `(2, "bien dong so du")`, `(1, "otp 7788")`; số nhỏ ra trước.
- Xô thẻ: chứa tối đa **3** thẻ, đầy từ đầu, mỗi giây thêm **1** thẻ (không vượt 3); mỗi tin gửi đi lấy **1** thẻ, hết thẻ thì từ chối. Bảy tin đến ở giây `0, 0, 0, 0, 1, 1, 2`.
- 90 000 tin mỗi phút, **65%** thuộc khách đã cài ứng dụng (đi thông báo đẩy, không cước); phần còn lại tính cước tối đa.

Viết `mau.py` (Python 3) in đúng bốn dòng:

1. `kenh: <bốn kênh cách nhau một dấu cách>`
2. `uu tien: <bốn nội dung theo thứ tự ra, cách nhau " | ">`
3. `xo the: <bảy kết quả cách nhau một dấu cách, mỗi kết quả là gui hoặc tu_choi>`
4. `mien cuoc: <số tin không cước> tin/phut, tinh cuoc toi da: <số tin còn lại>`

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh ACB L03 mau.py`.
