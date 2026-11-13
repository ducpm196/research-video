# Lab JV2 L06 — Viết năm ca kiểm và bắt một lỗi biên

Hàm cần kiểm (số minh hoạ), **đã có lỗi** — bạn chưa biết ở đâu:

```java
static long phiChuyenKhoan(long soTien, boolean cungNganHang) {
    if (soTien <= 0) {
        throw new IllegalArgumentException("so tien phai duong");
    }
    if (cungNganHang) {
        return 0;
    }
    if (soTien < 500000) {
        return 2000;
    }
    if (soTien <= 5000000) {
        return 7000;
    }
    return 11000;
}
```

**Đặc tả đúng:** số tiền không dương → ném `IllegalArgumentException`; cùng ngân hàng → phí 0; khác ngân hàng: đến **500 000** là 2 000; đến **5 000 000** là 7 000; trên đó là 11 000.

Viết tệp `KiemPhiChuyenKhoan.java` gồm hàm trên, hai hàm trợ giúp tự viết và `main` với **năm ca kiểm** theo bảng:

| tên ca | gọi | mong đợi |
|---|---|---|
| `cung ngan hang` | `phiChuyenKhoan(2000000, true)` | 0 |
| `bien 500000` | `phiChuyenKhoan(500000, false)` | 2000 |
| `sau bien 500001` | `phiChuyenKhoan(500001, false)` | 7000 |
| `bien 5000000` | `phiChuyenKhoan(5000000, false)` | 7000 |
| `so khong` | `phiChuyenKhoan(0, false)` | ném `IllegalArgumentException` |

Hàm trợ giúp `kiem(String ten, long mong, LongSupplier thuc)` in `DAT  <ten>` (hai dấu cách sau chữ DAT) hoặc `HONG <ten>: mong <mong>, thuc <thuc>`; `kiemNgoaiLe(ten, soTien)` in `DAT  <ten>` nếu có ném đúng ngoại lệ, ngược lại `HONG <ten>: khong nem ngoai le`. Cuối cùng in `dat <số>, hong <số>`.

Mong đợi: đúng **một** ca `HONG` — đó là lỗi trong hàm. Chấm bản **chưa sửa**: `bash labs/cham.sh JV2 L06 KiemPhiChuyenKhoan.java`. Sau đó tự sửa hàm và chạy lại để thấy năm dòng `DAT`.
