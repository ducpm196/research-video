# Lab JV2 L01 — Tổng giao dịch theo loại

Viết chương trình `TongTheoLoai` (tệp `TongTheoLoai.java`), **không cần mạng, không cần tệp có sẵn**:

1. Dùng `Files.writeString(Path.of("giao_dich.csv"), …)` ghi ra tệp đúng nội dung dưới đây (dòng đầu là tiêu đề):

```
ma,loai,so_tien
1,chuyen,850000
2,nap,4000000
3,chuyen,150000
4,rut,600000
5,nap,250000
6,chuyen,400000
7,rut,900000
```

2. Đọc lại tệp đó bằng `try (BufferedReader …)`, bỏ dòng tiêu đề, cộng theo từng loại và đếm số giao dịch (kiểu `long` cho tiền).
3. In ba dòng theo thứ tự `nap`, `rut`, `chuyen` đúng dạng `nap: 2 giao dich, tong 4250000`, rồi một dòng `Tong tat ca: <tổng>`.

Chạy: `javac TongTheoLoai.java && java TongTheoLoai`. Chấm: `bash labs/cham.sh JV2 L01 TongTheoLoai.java`.
