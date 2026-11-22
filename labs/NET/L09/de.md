# Lab NET L09 — TCP socket loopback (kết nối cục bộ) + tính số thứ tự bắt tay ba bước

Viết chương trình Python mở một máy chủ ổ cắm TCP (`socket.AF_INET` IPv4, `SOCK_STREAM` TCP) thật trên địa chỉ cục bộ loopback `127.0.0.1`, gửi/nhận thông điệp `PING` ↔ `PONG` và tính `ack` khi client gửi `SYN seq=100`, server gửi `SYN-ACK seq=500`, in đúng 3 dòng:
1. `tcp_echo=PONG`
2. `syn_ack_ack=101`
3. `final_ack=501`

Chấm tự động:
```bash
bash labs/cham.sh NET L09 duong_dan/bai_cua_ban.py
```
