# Lab BNX L04 — Đếm số lần xin mã và giây cuối còn được nhận

Một dịch vụ thanh toán gọi 4 API. Mã truy cập có hạn `TTL = 120` giây (TTL: thời gian sống của mã); dịch vụ lưu mã trong bộ đệm và **xin mã mới khi còn 20 giây** hạn
(tức mỗi mã dùng 100 giây). Máy chủ tài nguyên cho lệch đồng hồ `LECH = 30` giây và từ chối từ đúng giây `TTL + LECH` trở đi (quy tắc của bài).
Số liệu là số minh hoạ.

Viết chương trình Python (`mau.py`) mô phỏng **một giờ (3600 giây)**, mỗi giây là một số nguyên bắt đầu từ 0:
1. Một mã chung cho cả 4 API: xin mã lúc giây 0, rồi xin lại mỗi khi đến lúc; đếm số lần xin trong giờ.
2. Mỗi API một mã riêng: cùng quy tắc, nhân với 4 API.
3. Với mã cấp lúc giây 0: tìm bằng vòng lặp giây cuối cùng (số nguyên) mà máy chủ tài nguyên còn nhận.

In đúng ba dòng:
```
Mot ma chung: <số> lan xin ma
Moi API mot ma: <số> lan xin ma
Giay cuoi cung ma con duoc nhan: <giây>
```
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L04 mau.py`.
