# Lab FND L04 — Phiên bản công cụ, mã thoát và PATH

Tạo `kiem_tra.sh` in **bảy dòng**, đúng định dạng sau:
1. ba dòng: tên hoặc tên kèm số phiên bản chính của `git`, `javac`, `python` theo đúng định dạng `cut` bên dưới (dạng `<tên> <nhãn/phiên bản>`). Gợi ý: `git --version | cut -d' ' -f1-2`; `javac -version 2>&1 | cut -d. -f1`; `python --version | cut -d. -f1`.
2. `ls .` rồi in mã thoát dạng `ls: <mã>`, nhưng **giấu danh sách thư mục do `ls .` in ra** (`ls . > /dev/null`, nếu không màn hình có dòng thừa và chấm KHÁC); `ls khong_co` (giấu thông báo lỗi bằng `2> /dev/null`) rồi in `ls loi: <mã>`.
3. tạo `tep.txt` chỉ có chữ `so du`; `grep -q tien tep.txt` rồi in mã thoát dạng `grep: <mã>`.
4. tạo thư mục `tien_ich`, trong đó tệp `chao_ban` chứa lệnh `echo 'xin chao tu tien_ich'`; `chmod +x`; thêm `"$PWD/tien_ich"` vào **đầu** `PATH`; gọi `chao_ban`.

Chạy `bash kiem_tra.sh`; chấm: `bash labs/cham.sh FND L04 kiem_tra.sh`. Cần Git, JDK 21 và Python theo bài đầu tiên của khoá.
