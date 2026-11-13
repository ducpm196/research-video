# Lab JVA L00 — Phiếu số dư đầu tiên

Làm trong **Git Bash**, đứng đúng thư mục (xem bước 1).

1. `mkdir -p ~/hoc/jva`, rồi `cd ~/hoc/jva`; kiểm bằng `pwd`.
2. Dùng trình soạn mã tạo tệp `PhieuSo.java` (chữ hoa chữ đầu) trong thư mục đó, lớp `PhieuSo`. Hàm chính in **đúng năm dòng**:
   - `Xin chao Lan`
   - `So du: 250000 dong`
   - `Phi: 1500 + 500` (chuỗi, in nguyên chữ)
   - `Tong phi: 2000` (chuỗi nối với **phép cộng hai số đặt trong ngoặc**)
   - `Ghep: 1500500` (cùng hai số nhưng **không ngoặc**, để thấy dấu + nối chữ)
3. `javac PhieuSo.java && java PhieuSo`
4. Xoá thử dấu `;` ở dòng cuối, biên dịch lại, đọc dòng đầu thông báo (tệp, số dòng) rồi sửa lại.

Chấm: `bash labs/cham.sh JVA L00 PhieuSo.java`.
