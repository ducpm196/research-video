# Lab BNK L06 — Bộ đệm nhỏ, bốn tài khoản

Bộ đệm kiểu **hỏi bộ đệm trước, trượt thì hỏi cơ sở dữ liệu rồi nạp vào bộ đệm**. Trúng bộ đệm tốn **2 ms**; trượt tốn **2 ms** (hỏi bộ đệm) **cộng 30 ms** (hỏi cơ sở dữ liệu). Số liệu là số minh hoạ.

Viết chương trình `BoDemNho` (tệp `BoDemNho.java`, đầu tệp có `import java.util.*;`), dùng một `Map<Integer, Long>` làm bộ đệm:
1. Hàm `soDu(int tk)`: nếu bộ đệm có `tk` thì tính trúng; nếu không thì tính trượt, đọc `tk * 1000L` làm số dư giả lập và nạp vào bộ đệm.
2. Gọi `soDu(i % 4)` cho `i` từ 0 tới 39 (40 lần hỏi, bốn tài khoản).
3. In một dòng: `trung 36/40, trung binh 5.0 ms` (số trúng, và tổng độ trễ chia 40).

Chạy: `javac BoDemNho.java && java BoDemNho`. Chấm: `bash labs/cham.sh BNK L06 BoDemNho.java`.

## Phần thêm (không chấm): mã chặn
Thư mục `ma_chan/` có `MaChan.java` đầy đủ (đúng như trong video) và `ket_qua.txt`. Cần JDK 21.
1. `cd ma_chan`, rồi `javac MaChan.java && java MaChan`: B ghi được, A ghi muộn bị từ chối, giá trị cuối là B.
2. **Đoán trước**: đổi mã của B thành 32 (nhỏ hơn mã 33 của A) thì ai ghi được, giá trị cuối là gì? Sửa `main`, chạy lại và so với đoán.
3. Thêm lần ghi thứ ba, người C mang mã 35 ghi "C" sau cùng, và đoán giá trị cuối rồi chạy.
