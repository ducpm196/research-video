# Lab SAR L10 — Đối chiếu độ trễ ghi đồng bộ liên vùng với ghi bất đồng bộ tại chỗ

Hai vùng cách nhau độ trễ truyền một chiều `36 ms` (lưu ý khứ hồi `RTT` đi và về gồm hai lượt truyền). So sánh độ trễ ghi đồng bộ liên vùng với ghi bất đồng bộ tại chỗ (`3 ms`) và tính tỉ số chênh lệch.

Định dạng đầu ra (3 dòng):
`sync_rtt_ms=<số>`
`local_async_ms=<số>`
`latency_ratio=<số>x`

Chấm tự động:
```bash
bash labs/cham.sh SAR L10 duong_dan/bai_cua_ban.py
```
