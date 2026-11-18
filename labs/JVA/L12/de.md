# Lab JVA L12 — Dựng sổ chuyển khoản qua ba mốc

Trong Git Bash, thư mục làm việc của bạn, tệp `SoCaiLab.java`. Số liệu là số minh hoạ: ba tài khoản **P = 2 000 000**, **Q = 800 000**, **R = 1 200 000** (tổng gốc 4 000 000).

**Mốc 1 — sổ và tổng.** Lớp `SoCai` giữ `HashMap<String, Long> soDu` và `tongGoc`; hàm `mo(stk, tien)` đặt số dư và cộng `tongGoc`; hàm `tong()` cộng mọi số dư; hàm `lay(stk)` ném `IllegalArgumentException` nếu không có khoá. Hàm chính mở P, Q, R và in `Mo xong: tong 4000000`.

**Mốc 2 — chuyển có kiểm tra trước.** Bản ghi `record Lenh(String tu, String den, long tien) {}` và `class KhongDuTien extends Exception`. Hàm `chuyen(Lenh l) throws KhongDuTien`: lấy số dư hai bên, ném `IllegalArgumentException("So tien phai duong")` nếu tiền không dương, ném `IllegalArgumentException("Khong chuyen cho chinh minh")` nếu bên gửi và bên nhận là một (`l.tu().equals(l.den())`), ném `KhongDuTien(tu + " chi co " + a)` nếu tiền lớn hơn số dư bên gửi; **chỉ sau đó** mới trừ bên gửi và cộng bên nhận.

**Mốc 3 — kiểm bất biến sau mỗi lệnh.** Hàm `kiem()` ném `IllegalStateException("Lech tong …")` khi `tong() != tongGoc`; `chuyen` gọi `kiem()` cuối cùng. Hàm chính duyệt bốn lệnh: P→Q 500000, Q→R 2000000, P→Z 10000, R→P 700000; mỗi lệnh trong `try`, bắt `KhongDuTien` (in `TU CHOI …`) và `IllegalArgumentException` (in `SAI LENH …`), thành công in `OK ` + lệnh. Cuối cùng in ba số dư và `Cuoi ngay: tong …`.

**Kết quả trung gian để tự đối chiếu** (chạy từng mốc, đừng đợi tới cuối):

- Sau mốc 1, hàm chính chỉ có bước mở ba tài khoản, in đúng một dòng: `Mo xong: tong 4000000`.
- Sau mốc 2, hàm chính khai `throws Exception`, thêm hai thử nghiệm: gọi `chuyen` với lệnh P → Q 500000 rồi in `"P=" + so.lay("P") + " Q=" + so.lay("Q")`; kế đó gọi `chuyen` với lệnh Q → R 2000000 trong `try`, bắt `KhongDuTien` và in `"TU CHOI " + e.getMessage()`. Ra đúng ba dòng:

```
Mo xong: tong 4000000
P=1500000 Q=1300000
TU CHOI Q chi co 1300000
```

- Sau mốc 3, bạn bỏ hai thử nghiệm của mốc 2 và có đầu ra hoàn chỉnh trong `mong_doi.txt`.

Chấm bản hoàn chỉnh: `bash labs/cham.sh JVA L12 SoCaiLab.java`.
