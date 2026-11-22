# Lab EVT L11 — Quy mô luồng tin và giảm vòng gọi mạng nhờ gom lô

Quy đổi tải `864 000 000` tin nhắn mỗi ngày ra tốc độ trung bình mỗi giây, đồng thời tính số lô phải gửi và hệ số giảm số vòng gọi mạng (`RPC`) khi gom `400 000` tin thành từng lô `40` tin.

Định dạng đầu ra (3 dòng):
`msgs_per_sec=<số nguyên>`
`batches=<số nguyên>`
`rpc_cut=<số nguyên>x`

Chấm tự động:
```bash
bash labs/cham.sh EVT L11 duong_dan/bai_cua_ban.py
```
