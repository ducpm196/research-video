# Lab CLD L04 — Khuếch đại thử lại và thời gian chờ lùi lũy thừa

Một yêu cầu đi qua chuỗi `4` tầng, mỗi tầng gửi tối đa `2` lần (`1` lần đầu + `1` lần thử lại, hệ số khuếch đại `2^4`). Đồng thời với dãy chờ lùi lũy thừa cơ bản `50, 100, 200 ms`, tính tổng độ trễ chờ đợi cộng dồn qua 3 lần thử lại.

Định dạng đầu ra (2 dòng):
`amplified_reqs=<số nguyên>`
`backoff_sum_ms=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh CLD L04 duong_dan/bai_cua_ban.py
```
