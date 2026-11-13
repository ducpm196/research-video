# Lab JVA L02 — Chia hoá đơn và tính phí

Trong Git Bash, viết `ChiaHoaDon` (tệp `ChiaHoaDon.java`), số liệu là số minh hoạ. Dùng biến `long` cho tiền:

1. Hoá đơn **2 500 000** đồng chia đều cho **7** người: in `Moi nguoi: …` (thương) và `Du: …` (số dư).
2. Số tiền **987 654** đồng, phí **0,3%** (tức `* 3 / 1000`): in `Phi dung: …` (nhân trước, chia sau) và `Phi chia truoc: …` (viết `soTien / 1000 * 3`). Hai số khác nhau mấy đồng?
3. Có `soNguoi2 = 0`. Đặt phép kiểm **trước** phép chia bằng `&&` để chương trình không báo lỗi: `chiaDuoc = soNguoi2 != 0 && tong / soNguoi2 > 100000`; in `Chia duoc: …`.

Trước khi viết, thử từng phép trong `jshell`. Chạy: `javac ChiaHoaDon.java && java ChiaHoaDon`. Chấm: `bash labs/cham.sh JVA L02 ChiaHoaDon.java`.
