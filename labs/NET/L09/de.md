# Lab NET L09 — TCP socket loopback và tính số thứ tự bắt tay 3 bước

Đọc `stdin` `msg=<str> reply=<str> syn_seq=<int> srv_seq=<int>`. Mở socket TCP thật loopback gửi `msg` nhận phản hồi `reply`, và tính ACK bắt tay 3 bước.

In đúng 3 dòng: `tcp_echo=<str>`, `syn_ack_ack=<d>`, `final_ack=<d>`.
Chấm tự động: `bash labs/cham.sh NET L09 duong_dan/bai_cua_ban.py`

> Khung `socket` loopback (`PYT:L04` + stdlib): tạo server bằng `s = socket.socket(); s.bind(("127.0.0.1", 0)); s.listen(1)` lấy cổng tự gán `port = s.getsockname()[1]`, chạy `accept()`/`sendall()` trong `threading.Thread(..., daemon=True)`, rồi kết nối bằng `socket.create_connection(("127.0.0.1", port))`.
