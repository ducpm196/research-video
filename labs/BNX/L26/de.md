# Lab BNX L26 — Phân giải phiên bản phụ thuộc: Maven và Gradle

**MÔ PHỎNG**: bài này không chạy Maven, Gradle hay Jenkins thật; bạn viết bộ phân giải bằng Python thuần, với đồ thị phụ thuộc là số minh hoạ. Luật Maven đã được kiểm bằng Maven thật ở video; luật Gradle theo hướng dẫn chính thức (không chạy Gradle).

Dự án khai hai phụ thuộc trực tiếp theo thứ tự: `A 1.0`, `B 1.0`. Phụ thuộc bắc cầu (số minh hoạ):

- `A 1.0` cần `X 1.0` rồi `Y 2.0`
- `B 1.0` cần `Y 3.0` rồi `Z 1.0`
- `Z 1.0` cần `X 2.0`

Luật Maven: mỗi thư viện lấy phiên bản của khai báo **gần dự án nhất** (độ sâu nhỏ nhất); cùng độ sâu thì **khai báo trước thắng**.
Luật Gradle mặc định: lấy phiên bản **cao nhất** trong mọi yêu cầu.

Viết `mau.py` in kết quả hai luật: trước hết 5 dòng `maven <tên> <bản>` (A, B, X, Y, Z theo thứ tự chữ cái), rồi 3 dòng `gradle <tên> <bản>` cho X, Y, Z.
Gợi ý: duyệt theo độ sâu (hàng đợi), thư viện nào đã chọn thì bỏ yêu cầu sau (Maven); với Gradle thì chỉ giữ khi phiên bản cao hơn.
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L26 mau.py`.
