# Lab JVA L11 — Hai cách tính lãi, một bản ghi, một kiểu liệt kê

Trong Git Bash, viết `LaiSuatLab` (tệp `LaiSuatLab.java`, số liệu là số minh hoạ), nhiều lớp trong một tệp, chỉ `LaiSuatLab` là `public`:

1. `interface LaiSuat { long lai(long goc); }`.
2. `LaiCoDinh implements LaiSuat`: lãi `goc * 4 / 1000`. `LaiBac implements LaiSuat`: dưới **50 000 000** lãi `goc * 3 / 1000`, từ 50 000 000 lãi `goc * 5 / 1000`. Mỗi phương thức ghi đè có nhãn `@Override` và là `public`.
3. `record KyHan(String ten, int thang) {}` và `enum LoaiThe { THUONG, VANG }`; hàm `static long hanMuc(LoaiThe t)` dùng `return switch`: THUONG 20 000 000, VANG 100 000 000.
4. Hàm chính: mảng `LaiSuat[]` chứa hai cách tính, **một** vòng lặp in `l.lai(10000000) + " " + l.lai(80000000)`; rồi `a.equals(b) + " " + (a == b)` cho hai `KyHan("6T", 6)` tạo riêng; rồi `Han muc VANG: …`.

Chạy: `javac LaiSuatLab.java && java LaiSuatLab`. Chấm: `bash labs/cham.sh JVA L11 LaiSuatLab.java`.
