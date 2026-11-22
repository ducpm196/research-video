# Lab IRS L12 — Thiết kế hệ gợi ý hai tầng trong ngân sách 100 ms

Tính độ trễ phân vị 99 khi cắt ứng viên từ `1 200` xuống `500` (biết sinh ứng viên tốn `18 ms`, mạng đọc đặc trưng `22 ms`, và tầng xếp hạng tốn `0.06 ms` mỗi ứng viên ở phân vị 99), rồi tính xác suất một yêu cầu gặp đuôi chậm khi chia `8` mảnh song song mà mỗi mảnh chậm `1.5%`.

Định dạng đầu ra (1 dòng):
`p99_before=<số nguyên>ms p99_after=<số nguyên>ms tail8=<1 chữ số>%`
