# Lab BNK L02 — Đếm giao dịch của ba lời gọi

`ChuyenKhoanProxy.java`: một dịch vụ có ba hàm `chuyenKhoan`, `tinhPhi`, `thongBao`; **`chuyenKhoan` tự gọi `tinhPhi` và `thongBao` bằng cách gọi thẳng chính nó**. Proxy mở một giao dịch mỗi khi một hàm được gọi **qua proxy**.

Chép khung sau, rồi điền hai chỗ `// TODO`:

```java
import java.lang.reflect.*;
public class ChuyenKhoanProxy {
    interface Dich { void chuyenKhoan(); void tinhPhi(); void thongBao(); }
    static int moGiaoDich = 0;
    static class DichThat implements Dich {
        public void chuyenKhoan() { tinhPhi(); thongBao(); }
        public void tinhPhi() { }
        public void thongBao() { }
    }
    public static void main(String[] args) {
        Dich that = new DichThat();
        Dich proxy = (Dich) Proxy.newProxyInstance(Dich.class.getClassLoader(), new Class<?>[] { Dich.class },
            (p, m, a) -> {
                // TODO 1: đếm một giao dịch (moGiaoDich++)
                return m.invoke(that, a);
            });
        // TODO 2: gọi qua proxy lần lượt chuyenKhoan(), tinhPhi(), thongBao();
        //         sau mỗi lời gọi in "sau <tên hàm>: <số giao dịch>" (tên hàm viết như trong khung)
    }
}
```

Trước khi chạy, **dự đoán** ba con số rồi mới chấm. Chạy: `javac ChuyenKhoanProxy.java && java ChuyenKhoanProxy`. Chấm: `bash labs/cham.sh BNK L02 ChuyenKhoanProxy.java`.
