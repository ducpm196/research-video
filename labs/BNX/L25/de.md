# Lab BNX L25 — Bảng quyết định hoàn tác của giao dịch

**MÔ PHỎNG**: bài này chỉ mô phỏng luật hoàn tác bằng Python thuần; không chạy Spring và không có cơ sở dữ liệu thật. Luật chép theo hướng dẫn chính thức của Spring (đã chạy thật ở phần ví dụ của video).

Theo quy tắc mặc định của Spring: ngoại lệ **không kiểm tra** (lớp con của `RuntimeException`) và `Error` làm giao dịch **hoàn tác**; ngoại lệ **kiểm tra** (như `IOException`)
thì **chốt**, trừ khi khai `rollbackFor` chứa kiểu đó (hoặc kiểu cha như `Exception`). Không có lỗi thì chốt.

Viết `mau.py` có hàm `hoan_tac(loi, rollback_for)` trả `True` khi giao dịch bị hoàn tác, rồi in đúng 5 dòng cho 5 ca sau (theo thứ tự), mỗi dòng dạng
`<loi> + <khai>: hoan tac` hoặc `...: chot` (không lỗi thì ghi `khong loi`, không khai thì ghi `khong khai`):

1. `IllegalArgumentException`, không khai   2. `IOException`, không khai   3. `IOException`, khai `Exception`   4. `Error`, không khai   5. không có lỗi

Gợi ý: kiểu kiểm tra: `IOException`, `SQLException`, `Exception`; không kiểm tra: `IllegalArgumentException`, `RuntimeException`, `NullPointerException`.
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L25 mau.py`.
