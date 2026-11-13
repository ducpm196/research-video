# Lab FND L02 — Dựng cây cửa hàng bằng tệp lệnh

Tạo `dung.sh` (làm trong thư mục hiện tại, tuần tự):
1. `mkdir -p`: tạo `cua_hang/kho` và `cua_hang/bao_cao`.
2. Trong `kho`: tạo ba tệp rỗng `ao.txt`, `quan.txt`, `non.txt`.
3. `cua_hang/bao_cao/tong.txt`: dòng `ao 5` bằng `>`, rồi dòng `quan 3` bằng `>>`.
4. Chép `ao.txt` thành `ao_sao.txt`; đổi tên `non.txt` thành `mu.txt`; xoá `quan.txt`.
5. In `find cua_hang | sort` (sort xếp các dòng theo chữ cái, để kết quả cố định), rồi `cat cua_hang/bao_cao/tong.txt`.

Chạy `bash dung.sh`; chấm: `bash labs/cham.sh FND L02 dung.sh`. Khác bài giảng: tên thư mục, tên tệp, số liệu.
