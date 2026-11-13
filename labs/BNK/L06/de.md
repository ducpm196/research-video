# Lab BNK L06 — Bộ đệm nhỏ, bốn tài khoản

Bộ đệm kiểu **hỏi bộ đệm trước, trượt thì hỏi cơ sở dữ liệu rồi nạp vào bộ đệm**. Trúng bộ đệm tốn **2 ms**; trượt tốn **2 ms** (hỏi bộ đệm) **cộng 30 ms** (hỏi cơ sở dữ liệu). Số liệu là số minh hoạ.

Viết chương trình `BoDemNho` (tệp `BoDemNho.java`), dùng một `Map<Integer, Long>` làm bộ đệm:
1. Hàm `soDu(int tk)`: nếu bộ đệm có `tk` thì tính trúng; nếu không thì tính trượt, đọc `tk * 1000L` làm số dư giả lập và nạp vào bộ đệm.
2. Gọi `soDu(i % 4)` cho `i` từ 0 tới 39 (40 lần hỏi, bốn tài khoản).
3. In một dòng: `trung 36/40, trung binh 5.0 ms` (số trúng, và tổng độ trễ chia 40).

Chạy: `javac BoDemNho.java && java BoDemNho`. Chấm: `bash labs/cham.sh BNK L06 BoDemNho.java`.
