# Lab JV2 L03 — Thống kê bằng Stream, đối chiếu với vòng lặp

Viết chương trình `ThongKeStream` (tệp `ThongKeStream.java`) với `record GiaoDich(int ma, String loai, long soTien) {}` và tám giao dịch
(`ma`, `loai`, `soTien`): `(1, nap, 3000000)`, `(2, rut, 450000)`, `(3, chuyen, 800000)`, `(4, rut, 1200000)`, `(5, nap, 200000)`, `(6, chuyen, 1500000)`, `(7, rut, 500000)`, `(8, nap, 650000)`.

1. Bằng **Stream** (`filter`, `mapToLong`, `sum`): tổng tiền các giao dịch loại `rut` có `soTien >= 500000`.
2. Bằng `Collectors.groupingBy(..., TreeMap::new, Collectors.counting())`: số giao dịch theo loại.
3. Bằng `groupingBy` với `Collectors.summingLong`: tổng tiền theo loại.
4. Bằng **vòng lặp** `for` và `TreeMap.merge(khoá, số, Long::sum)`: tổng tiền theo loại; in `true` nếu bản đồ này `equals` bản đồ ở bước 3.

In bốn dòng đúng dạng:
```
Rut tu 500000: <số>
Dem: {…}
Tong: {…}
Khop vong lap: true
```

Chạy: `javac ThongKeStream.java && java ThongKeStream`. Chấm: `bash labs/cham.sh JV2 L03 ThongKeStream.java`.
