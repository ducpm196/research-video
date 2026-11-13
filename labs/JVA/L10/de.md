# Lab JVA L10 — Hạn mức rút trong ngày

Trong Git Bash, viết `RutHanMuc` (tệp `RutHanMuc.java`, số liệu là số minh hoạ), gồm ba lớp trong một tệp:

1. `class HetHanMuc extends Exception` có hàm tạo nhận lời nhắn và gọi `super(thongBao)`.
2. `class The` với trường `private long daRut = 0;` và hạn mức **2 000 000**. Hàm `void rut(long tien) throws HetHanMuc`: nếu `daRut + tien > hanMuc` thì **ném** `new HetHanMuc("Vuot han muc, da rut " + daRut + ", xin rut " + tien)`; ngược lại cộng vào `daRut`. Thêm `long laySoDaRut()`.
3. `public class RutHanMuc` có hàm chính: trong khối `try` rút lần lượt **800000**, **900000**, **500000**, sau mỗi lần rút thành công in `Rut … xong`; khối `catch (HetHanMuc e)` in `Tu choi: ` + lời nhắn; khối `finally` in `Da rut hom nay: …`.

Thử thêm: bỏ khối `catch` rồi biên dịch, đọc thông báo lỗi của trình biên dịch.

Chạy: `javac RutHanMuc.java && java RutHanMuc`. Chấm: `bash labs/cham.sh JVA L10 RutHanMuc.java`.
