# Lab MLO L02 — Phiên bản hoá dữ liệu bằng mã băm nội dung SHA-256 thay vì đặt tên tệp

Đổi đúng 1 nhãn trong chuỗi bản ghi `"u101,1\nu102,0"` thành `"u101,1\nu102,1"` rồi lấy 12 ký tự đầu mã băm SHA-256 để kiểm tra hai phiên bản khác nhau hoàn toàn.

Định dạng đầu ra:
`h1=<12 ký tự> h2=<12 ký tự> changed=<1 hoặc 0>`

Chấm tự động:
```bash
bash labs/cham.sh MLO L02 duong_dan/bai_cua_ban.py
```
