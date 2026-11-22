# Lab CLC L06 — Chi phí GB-giây của hàm theo sự kiện (Serverless)

Tính tổng `GB-giây` cho `2 500 000` lượt gọi hàm theo sự kiện ở hai cấu hình: `0,5 GB` chạy `160 ms/lượt`, và `1,0 GB` giúp giảm thời gian xuống `80 ms/lượt`. Kiểm tra xem tổng `GB-giây` của hai phương án có bằng nhau hay không.

Định dạng đầu ra (3 dòng):
`gb_sec_512mb=<số>`
`gb_sec_1gb=<số>`
`same_gb_sec=<0|1>`

Chấm tự động:
```bash
bash labs/cham.sh CLC L06 duong_dan/bai_cua_ban.py
```
