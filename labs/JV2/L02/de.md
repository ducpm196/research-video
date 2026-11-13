# Lab JV2 L02 — Sắp xếp giao dịch theo hai khoá

Tự viết chương trình `SapXepGiaoDich` (tệp `SapXepGiaoDich.java`):

1. Khai báo `record GiaoDich(int ma, String loai, long soTien) {}` bên trong lớp.
2. Tạo danh sách bảy giao dịch theo thứ tự này (`ma`, `loai`, `soTien`):
   `(1, chuyen, 900000)`, `(2, nap, 250000)`, `(3, chuyen, 150000)`, `(4, rut, 600000)`, `(5, nap, 4000000)`, `(6, rut, 900000)`, `(7, chuyen, 900000)`.
3. Viết một lớp `TheoLoaiRoiTien implements Comparator<GiaoDich>`: **khoá 1** là `loai` tăng dần; **khoá 2** là `soTien` **giảm dần**
   (dùng `Long.compare`, **không** dùng phép trừ). Sắp xếp bằng `ds.sort(new TheoLoaiRoiTien())`.
4. In mỗi giao dịch một dòng dạng `1 chuyen 900000` (`ma loai soTien`).

Chú ý hai giao dịch `1` và `7` có cùng loại và cùng số tiền: `List.sort` là sắp xếp **ổn định**, nên chúng giữ nguyên thứ tự ban đầu.

Chạy: `javac SapXepGiaoDich.java && java SapXepGiaoDich`. Chấm: `bash labs/cham.sh JV2 L02 SapXepGiaoDich.java`.
