# Lab JV2 L09 — Sổ cái nhỏ: bỏ qua dòng lỗi, in số dư, kiểm bất biến

Viết một tệp `SoCaiNho.java` (một lớp, có thể lồng một `record`). Chương trình tự ghi ra `so_cai.csv` đúng nội dung sau rồi đọc lại:

```
ma,ngay,tai_khoan,loai,so_tien
1,2026-03-02,B01,nap,4000000
2,2026-03-04,B02,nap,2500000
3,2026-03-09,B01,rut,900000
4,2026-03-11,B02,rut,abc
5,2026-04-01,B03,nap,1500000
6,2026-04-05,B01,gui,100000
7,2026-04-12,B02,rut,700000
```

Yêu cầu:
1. Đọc bằng `try (BufferedReader …)`, bỏ dòng tiêu đề, đếm **số dòng của tệp** (tiêu đề là dòng 1).
2. Một hàm `phanTich(dong)` ném `IllegalArgumentException("so tien khong hop le")` khi số tiền không phải số, và `IllegalArgumentException("loai khong hop le")` khi loại không phải `nap` hay `rut`.
3. Dòng lỗi **không làm dừng chương trình**: in `Bo qua dong <số dòng>: <thông điệp>` rồi đọc tiếp.
4. Dòng hợp lệ: số dư theo tài khoản bằng `TreeMap` (`nap` cộng, `rut` trừ); đồng thời cộng riêng tổng nạp và tổng rút.
5. In số dư mỗi tài khoản dạng `B01 3100000`, rồi `Tong <tổng số dư> khop <true/false>` với `khop` là `tổng số dư == tổng nạp − tổng rút`.

Kết quả mong đợi (sáu dòng): hai dòng `Bo qua`, ba dòng số dư, một dòng `Tong`. Tự tính tay trước: B01 = 4 000 000 − 900 000.

Chạy: `javac SoCaiNho.java && java SoCaiNho`. Chấm: `bash labs/cham.sh JV2 L09 SoCaiNho.java`.
