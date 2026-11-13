# Lab JVA L12 — Dựng sổ chuyển khoản qua ba mốc

Trong Git Bash, thư mục làm việc của bạn, tệp `SoCaiLab.java`. Số liệu là số minh hoạ: ba tài khoản **P = 2 000 000**, **Q = 800 000**, **R = 1 200 000** (tổng gốc 4 000 000).

**Mốc 1 — sổ và tổng.** Lớp `SoCai` giữ `HashMap<String, Long> soDu` và `tongGoc`; hàm `mo(stk, tien)` đặt số dư và cộng `tongGoc`; hàm `tong()` cộng mọi số dư; hàm `lay(stk)` ném `IllegalArgumentException` nếu không có khoá. Hàm chính mở P, Q, R và in `Mo xong: tong 4000000`.

**Mốc 2 — chuyển có kiểm tra trước.** Bản ghi `record Lenh(String tu, String den, long tien) {}` và `class KhongDuTien extends Exception`. Hàm `chuyen(Lenh l) throws KhongDuTien`: lấy số dư hai bên, ném `IllegalArgumentException("So tien phai duong")` nếu tiền không dương, ném `KhongDuTien(tu + " chi co " + a)` nếu tiền lớn hơn số dư bên gửi; **chỉ sau đó** mới trừ bên gửi và cộng bên nhận.

**Mốc 3 — kiểm bất biến sau mỗi lệnh.** Hàm `kiem()` ném `IllegalStateException("Lech tong …")` khi `tong() != tongGoc`; `chuyen` gọi `kiem()` cuối cùng. Hàm chính duyệt bốn lệnh: P→Q 500000, Q→R 2000000, P→Z 10000, R→P 700000; mỗi lệnh trong `try`, bắt `KhongDuTien` (in `TU CHOI …`) và `IllegalArgumentException` (in `SAI LENH …`), thành công in `OK ` + lệnh. Cuối cùng in ba số dư và `Cuoi ngay: tong …`.

Chạy từng mốc để thấy kết quả tăng dần. Chấm bản hoàn chỉnh: `bash labs/cham.sh JVA L12 SoCaiLab.java`.
