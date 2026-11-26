# Lab JV2 L04 — Bộ chứa tiêm phụ thuộc cỡ nhỏ

Viết `MiniDiKho` (tệp `MiniDiKho.java`) gồm **ba phần do bạn tự viết**:

1. Hai nhãn `@ThanhPhan` và `@Tiem` (`@interface`, giữ đến lúc chạy: `@Retention(RetentionPolicy.RUNTIME)`).
2. Bộ chứa: `static Map<Class<?>, Object> hop` và hàm `static Object lay(Class<?> loai) throws Exception`: nếu `hop` đã có thì trả lại; nếu chưa thì
   tạo bằng `loai.getDeclaredConstructor().newInstance()`, **bỏ vào `hop` trước**, rồi với mỗi trường có nhãn `@Tiem` thì `setAccessible(true)` và gán `lay(kiểu của trường)`.
3. `main`: lấy `DonHang` từ bộ chứa rồi in ba dòng (bên dưới).

Dòng `import` cần dùng (đặt trên đầu tệp): `java.lang.annotation.Retention`, `java.lang.annotation.RetentionPolicy`, `java.lang.reflect.Field`, `java.util.HashMap`, `java.util.Map`. `Class<?>` là kiểu "mô tả của một lớp nào đó" (dấu `?` nghĩa là chưa biết lớp cụ thể).

Ba lớp có sẵn (chép nguyên vào tệp, ngay trong `MiniDiKho`):

```java
@ThanhPhan static class KhoHang { int soLuong() { return 12; } }
@ThanhPhan static class BangGia { long gia() { return 45000; } }
@ThanhPhan static class DonHang {
    @Tiem KhoHang kho;
    @Tiem BangGia bang;
    long tong() { return kho.soLuong() * bang.gia(); }
}
```

In đúng ba dòng theo dạng:
```
Tong gia tri kho: <tổng tiền từ d.tong()>
Cung mot BangGia: <true|false khi so d.bang == lay(BangGia.class)>
So thanh phan: <hop.size()>
```
(`Cung mot BangGia` là `d.bang == lay(BangGia.class)`; `So thanh phan` là `hop.size()`.)

Chạy: `javac MiniDiKho.java && java MiniDiKho`. Chấm: `bash labs/cham.sh JV2 L04 MiniDiKho.java`.
