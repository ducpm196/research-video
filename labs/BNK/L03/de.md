# Lab BNK L03 — Bốn yêu cầu, hai khoá

Số dư đầu **3 000 000**; mỗi yêu cầu chuyển **trừ 700 000**. Bốn yêu cầu đến theo thứ tự với khoá lũy đẳng `k1`, `k1`, `k2`, `k1` (hai lần thử lại cùng khoá `k1`).

Viết chương trình `XuLyTrung` (tệp `XuLyTrung.java`):
1. Hàm `static long chuyen(String khoa)`: nếu `khoa` chưa xử lý thì trừ 700 000 vào số dư và nhớ **phản hồi** (số dư sau khi trừ); nếu đã xử lý thì **trả lại đúng phản hồi đã nhớ**, không trừ nữa. (Gợi ý: `Map<String, Long>` và `computeIfAbsent`.)
2. Với từng yêu cầu trong dãy (bốn yêu cầu nên in đúng bốn dòng, khoá `k1` xuất hiện ba lần), in một dòng đúng dạng `k1 -> 2300000`.

Chạy: `javac XuLyTrung.java && java XuLyTrung`. Chấm: `bash labs/cham.sh BNK L03 XuLyTrung.java`.

## Phần thêm (không chấm): máy chủ nhỏ và `curl`
Thư mục `may_chu/` có sẵn tệp `MayChu.java` đầy đủ (đúng như trong video) và `thu_curl.sh` (sáu lệnh `curl`). Cần JDK 21 và `curl`.
1. Cửa sổ lệnh thứ nhất: `cd may_chu` rồi `java MayChu.java` (máy chủ chạy nền, lắng nghe cổng 8099; dừng bằng Ctrl+C).
2. Cửa sổ lệnh thứ hai: `cd may_chu` rồi `bash thu_curl.sh`. Kết quả phải giống `may_chu/ket_qua_curl.txt`: ba lần không khoá trừ ba lần, ba lần cùng khoá chỉ trừ một lần.
3. Thử đổi: gửi hai lần tới `/chuyen-co-khoa` với **hai khoá khác nhau** (`Idempotency-Key: x1`, `x2`) và đoán số dư trước khi chạy.
