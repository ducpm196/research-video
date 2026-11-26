# Lab BNK L05 — Thứ tự khoá cho bốn lệnh chuyển

Quy tắc chống bế tắc: **luôn khoá hàng có mã nhỏ hơn trước**, dù lệnh chuyển đi từ đâu tới đâu.

Viết chương trình `ThuTuKhoa` (tệp `ThuTuKhoa.java`). Có bốn lệnh chuyển `(từ, tới)`: `(4, 9) (9, 4) (7, 4) (4, 7)`. Với mỗi lệnh, tính mã khoá trước (nhỏ hơn) và mã khoá sau (lớn hơn) bằng `Math.min` và `Math.max`, rồi in một dòng đúng dạng:

`4 -> 9: khoa 4 roi 9`

Chạy: `javac ThuTuKhoa.java && java ThuTuKhoa`. Chấm: `bash labs/cham.sh BNK L05 ThuTuKhoa.java`.

## Phần thêm (không chấm): thấy bế tắc rồi phá nó
Thư mục `be_tac/` có sẵn `BeTac.java` đầy đủ (đúng như trong video) và `ket_qua.txt`. Cần JDK 21.
1. Chạy `cd be_tac`, rồi `javac BeTac.java && java BeTac`: dòng đầu phải ra `A roi B  va  B roi A: be tac`, dòng sau `A roi B  va  A roi B: xong`.
2. Coi `a` là hàng mã 4, `b` là hàng mã 9; lệnh 4 → 9 và lệnh 9 → 4 đi ngược chiều. **Đoán trước**: nếu cả hai lệnh áp quy tắc "khoá mã nhỏ trước" thì mỗi lệnh khoá cặp nào, và kết quả là `xong` hay `be tac`?
3. Thêm vào `main` một dòng `System.out.println("hai chieu nguoc, khoa ma nho truoc: " + thu(...));` với đúng thứ tự khoá mà bạn đoán (bốn tham số: khoá đầu và khoá sau của luồng 1, rồi của luồng 2), chạy lại và so với đoán.

## Phần thêm trên Oracle thật (tuỳ chọn — không chấm tự động bởi `cham.sh`)
Khi có container `bnx-ora` (`gvenzl/oracle-free:23-slim`), chạy `bash labs/BNK/L05/oracle/chay.sh` (tệp `labs/BNK/L05/oracle/thu.sql`) để thử `SELECT ... FOR UPDATE` khoá hàng theo thứ tự id tăng dần trực tiếp trên Oracle. Lab Java ở trên vẫn là bài bắt buộc mặc định.
