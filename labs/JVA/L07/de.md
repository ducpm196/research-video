# Lab JVA L07 — Lớp Vi (ví tiền)

Trong Git Bash, viết tệp `QuanLyVi.java` (số liệu là số minh hoạ) gồm **hai lớp** trong cùng một tệp: lớp `Vi` (không `public`) và lớp `public class QuanLyVi` có hàm chính.

Lớp `Vi`:
- trường `private String ten;` và `private long tien;` (bất biến: `tien` không bao giờ âm);
- **hàm tạo** `Vi(String ten)`: đặt `ten`, `tien = 0` (dùng `this.`);
- `void them(long soTien)`: chỉ cộng khi `soTien > 0`;
- `boolean chi(long soTien)`: nếu `soTien <= 0` hoặc `soTien > tien` thì in `Tu choi chi <soTien>, con <tien>` và trả `false`; ngược lại trừ và trả `true`;
- `long layTien()` và `toString()` trả `ten + ": " + tien + " dong"`.

Hàm chính: tạo `lan` và `minh`; `lan.them(800000)`, `lan.chi(250000)`, `lan.chi(900000)`; `minh.them(50000)`, `minh.chi(50000)`; in `lan`, in `minh`, rồi `Tong: …` (tổng hai `layTien()`).

Chạy: `javac QuanLyVi.java && java QuanLyVi`. Chấm: `bash labs/cham.sh JVA L07 QuanLyVi.java`.
