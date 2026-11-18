# Lab BNX L18 — Ca kiểm tự viết, cổng giả đếm lời gọi, đồng hồ đứng yên (không cần tải thư viện)

Lab chạy được chỉ với JDK, không cần JUnit hay Mockito: ta tự viết phần "khẳng định" và "đối tượng giả" bằng Java thuần. Số liệu là số minh hoạ.

Viết `Lab.java` (một tệp, `public class Lab`, `import java.time.*;`) gồm các phần đề cho sẵn dưới đây (chép nguyên) rồi tự viết hàm `ca` và `main`:

```java
interface Cong { boolean chuyen(String tk, long soTien); }

// Đề: dưới 2 000 000: 0; từ 2 000 000 tới dưới 20 000 000: 3 000; từ 20 000 000: 4 000
static long tinh(long soTien) {
    if (soTien < 2_000_000) return 0;
    if (soTien <= 20_000_000) return 3_000;   // nhầm dấu: phải là <
    return 4_000;
}
static long chuyen(Cong cong, String tk, long soTien) {   // phí rồi gọi cổng với soTien + phí
    long phi = tinh(soTien);
    if (!cong.chuyen(tk, soTien + phi)) throw new IllegalStateException();
    return phi;
}
static boolean kip(Clock dongHo) {   // kịp trước 17 giờ
    return LocalTime.now(dongHo).isBefore(LocalTime.of(17, 0));
}
```
(`Cong` đặt trong lớp `Lab` dưới dạng `interface Cong {…}` lồng.)

**Phần 1 — ca kiểm.** Viết hàm `ca(long vao, long mongDoi)`: gọi `tinh(vao)`, so với `mongDoi` (lấy từ ĐỀ, không từ mã), đếm số ca đạt và trượt, in `ca <vao>: mong doi <m>, nhan <n>, DAT` hoặc `TRUOT`.
Gọi cho 5 số tiền theo thứ tự: 1999999, 2000000, 19999999, 20000000, 30000000 (mong đợi lấy từ đề). Rồi in `tong: <đạt> dat, <trượt> truot`.

**Phần 2 — cổng giả.** Viết đối tượng giả `Cong` bằng một biểu thức lambda, ghi lại số lần gọi và số tiền cuối cùng. Gọi `chuyen(gia, "TK07", 12_000_000)` rồi in `cong goi <số lần> lan, so tien <số tiền>`.

**Phần 3 — đồng hồ.** Với `Clock.fixed` ở `2026-11-11T16:59:00+07:00` (múi giờ +7) rồi sau 60 giây, in kết quả `kip(...)` hai dòng.

In đúng 9 dòng như `mong_doi.txt`. Chấm: `bash labs/cham.sh BNX L18 Lab.java`.
