# Lab JVA L05 — Sáu tài khoản

Trong Git Bash, viết `SauTaiKhoan` (tệp `SauTaiKhoan.java`, số liệu là số minh hoạ). Mảng `long[] soDu = {820000, 150000, 2400000, 150000, 3600000, 90000};` (nhớ `import java.util.Arrays;`).

1. Một vòng lặp duyệt mảng: cộng `tong`; tìm **chỉ số** của số dư **nhỏ nhất** (so với `soDu[nhoNhat]`); đếm số tài khoản có số dư **dưới 200000**. In `Tong: …`, `Nho nhat: … o chi so …`, `So tai khoan duoi 200000: …`.
2. Chép mảng bằng `Arrays.copyOf`, sắp **bản sao** tăng dần, in bằng `Arrays.toString`.
3. In mảng gốc dạng `Goc: [...]` để chứng tỏ nó **không đổi**.

Chạy: `javac SauTaiKhoan.java && java SauTaiKhoan`. Chấm: `bash labs/cham.sh JVA L05 SauTaiKhoan.java`.
