# Lab SAR L12 — Quy mô QPS đọc/ghi và dung lượng 5 năm cho trình rút gọn đường dẫn (URL)

Dịch vụ rút gọn đường dẫn (`URL Shortener`) tạo `150 triệu` đường dẫn mới mỗi tháng (`30` ngày = `2 592 000` giây), tỉ lệ đọc gấp `200` lần ghi, mỗi bản ghi tốn `400 byte`. Tính tốc độ ghi `QPS`, tốc độ đọc tương ứng và tổng dung lượng lưu trữ `5` năm (`60` tháng).

Định dạng đầu ra (3 dòng):
`write_qps=<1 chữ số>`
`read_qps=<số>`
`storage_5yr_tb=<1 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh SAR L12 duong_dan/bai_cua_ban.py
```
