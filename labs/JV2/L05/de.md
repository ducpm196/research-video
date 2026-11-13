# Lab JV2 L05 — Đo tranh chấp dữ liệu và sửa cho đúng

Viết `DemSaiDung` (tệp `DemSaiDung.java`). **Bốn luồng**, mỗi luồng lặp **250 000** lần; mỗi vòng làm ba việc:

1. tăng biến `static int thuong` bằng `thuong++` (không bảo vệ);
2. tăng biến `static int dongBo` **bên trong** `synchronized (khoa) { … }`;
3. tăng `AtomicInteger nguyenTu` bằng `incrementAndGet()`.

Tạo bốn `Thread` từ cùng một `Runnable`, `start()` cả bốn rồi `join()` cả bốn. In ba dòng:

```
Khong dong bo: dem < 1000000 -> true
Dong bo: 1000000
Nguyen tu: 1000000
```

(Dòng đầu in `thuong < 1000000` — giá trị thật của `thuong` thay đổi mỗi lần chạy, nên bài chỉ in kết quả so sánh.)

Chạy: `javac DemSaiDung.java && java DemSaiDung`. Chấm: `bash labs/cham.sh JV2 L05 DemSaiDung.java`.
