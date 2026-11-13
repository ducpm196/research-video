# Lab FND L09 — Dựng kho Git, chốt ba lần

Tạo `kho.sh` (chạy trong thư mục tạm của lệnh chấm, không ghi ra ngoài):

1. `git init -q -b main repo`, `cd repo`, đặt cục bộ `git config user.name` và `user.email` (giá trị tuỳ ý);
2. chốt **3 lần**, lời nhắn đúng như sau:
   - `tao kho`: `kho.txt` chứa dòng `ao 10`;
   - `them non`: nối dòng `non 5` vào `kho.txt`;
   - `sua so luong ao`: đổi `ao 10` thành `ao 12` bằng `sed -i 's/ao 10/ao 12/' kho.txt`;
3. in lần lượt: `git log --format=%s` (lời nhắn, mới nhất trước), `git branch --show-current`, `git rev-list --count HEAD`.

Chạy `bash kho.sh`; chấm: `bash labs/cham.sh FND L09 kho.sh`. Cần Git 2.28 trở lên. Cảnh báo về xuống dòng (LF/CRLF) nếu có nằm ở luồng lỗi, không ảnh hưởng chấm.
