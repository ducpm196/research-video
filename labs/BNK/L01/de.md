# Lab BNK L01 — Ba luồng cộng chung một tổng

Ba luồng, **mỗi luồng cộng 1 vào biến chung `tong` đúng 200 000 lần**. Tổng đúng phải là 600 000.

Viết chương trình `TongBaLuong` (tệp `TongBaLuong.java`):
1. Biến chung `static long tong = 0;` và một đối tượng khoá `static final Object KHOA = new Object();`.
2. Một việc `Runnable` cộng 200 000 lần, **mỗi lần cộng bọc trong** `synchronized (KHOA) { … }`.
3. Tạo ba luồng cho cùng việc đó, `start()` cả ba rồi `join()` cả ba.
4. In đúng một dòng: `tong = 600000`.

Khung tệp `TongBaLuong.java` (viết bài vào chỗ `...`; `throws Exception` cho phép bỏ qua lỗi bất thường khi chờ luồng):

```java
public class TongBaLuong {
    static long tong = 0;
    static final Object KHOA = new Object();
    public static void main(String[] args) throws Exception {
        // ... Runnable viec = () -> { ... };  rồi ba luồng, start(), join(), in tong
    }
}
```

Thử thêm: bỏ `synchronized`, chạy lại vài lần. `tong` sẽ nhỏ hơn 600000 và đổi mỗi lần: đó là mất cập nhật.

Chạy: `javac TongBaLuong.java && java TongBaLuong`. Chấm: `bash labs/cham.sh BNK L01 TongBaLuong.java`.
