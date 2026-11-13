# Lab FND L04 — Phiên bản công cụ, mã thoát và PATH

Tạo `kiem_tra.sh` in **bảy dòng**, đúng như `mong_doi.txt`:
1. ba dòng: tên và số phiên bản chính của `git` (`git version`), `javac` (`javac 21`), `python` (`Python 3`). Gợi ý: `git --version | cut -d' ' -f1-2`; `javac -version 2>&1 | cut -d. -f1`; `python --version | cut -d. -f1`.
2. `ls .` rồi in mã thoát dạng `ls: 0`; `ls khong_co` (giấu thông báo lỗi bằng `2> /dev/null`) rồi in `ls loi: 2`.
3. tạo `tep.txt` chỉ có chữ `so du`; `grep -q tien tep.txt` rồi in mã thoát dạng `grep: 1`.
4. tạo thư mục `tien_ich`, trong đó tệp `chao_ban` chứa lệnh `echo 'xin chao tu tien_ich'`; `chmod +x`; thêm `"$PWD/tien_ich"` vào **đầu** `PATH`; gọi `chao_ban`.

Chạy `bash kiem_tra.sh`; chấm: `bash labs/cham.sh FND L04 kiem_tra.sh`. Cần Git, JDK 21 và Python theo bài đầu tiên của khoá.
