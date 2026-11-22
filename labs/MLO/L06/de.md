# Lab MLO L06 — Gộp lô phục vụ: đánh đổi độ trễ chờ đợi và thông lượng yêu cầu

Với tốc độ đến `200` yêu cầu mỗi giây (cách nhau `5` mi-li-giây), gộp lô `16` yêu cầu; một yêu cầu đơn xử lý mất `4` mi-li-giây còn cả lô 16 mất `15` mi-li-giây. Tính thời gian chờ tối đa của yêu cầu đầu (`first_wait_ms`), thông lượng chạy đơn và chạy lô.

Định dạng đầu ra:
`first_wait_ms=<số nguyên> single_rps=<số nguyên làm tròn bằng round> batch_rps=<số nguyên làm tròn bằng round>`

Chấm tự động:
```bash
bash labs/cham.sh MLO L06 duong_dan/bai_cua_ban.py
```
