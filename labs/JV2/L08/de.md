# Lab JV2 L08 — Lãi theo ngày, đúng đến từng đồng

Gửi **120 000 000 đồng** ngày **2026-01-15**, đáo hạn ngày **2026-04-20**, lãi **6% một năm** (số minh hoạ). Lãi tính theo công thức
`lãi = gốc × lãi suất × số ngày / 365`, **làm tròn HALF_UP về đồng**.

Viết `LaiTheoNgay` (tệp `LaiTheoNgay.java`):
1. Đếm số ngày bằng `ChronoUnit.DAYS.between` (không tự cộng tay).
2. Tính lãi bằng `BigDecimal` **tạo từ chuỗi** (`new BigDecimal("0.06")`), chia bằng `divide(…, 0, RoundingMode.HALF_UP)`.
3. In bốn dòng đúng dạng:

```
So ngay: 95
Lai: 1873973
Tong: 121873973
Dao han la: MONDAY
```

(`Dao han la` là `getDayOfWeek()` của ngày đáo hạn.) Tự tính tay trước: số ngày từ 15 tháng 1 tới 15 tháng 4 là 31 + 28 + 31 = 90, cộng 5 ngày nữa.

Chạy: `javac LaiTheoNgay.java && java LaiTheoNgay`. Chấm: `bash labs/cham.sh JV2 L08 LaiTheoNgay.java`.
