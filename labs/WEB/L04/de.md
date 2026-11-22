# Lab WEB L04 — Node.js thật: đo thời gian chờ tuần tự vs Promise.all

Viết hàm `async` mô phỏng 3 tác vụ `100, 200, 300 ms`: tính tổng thời gian lý thuyết khi `await` tuần tự (`600`) vs chạy đồng thời `Promise.all` (`300`) và mức tăng tốc, in đúng 3 dòng:
1. `seq_ms=600`
2. `parallel_ms=300`
3. `speedup=2.0x`

Chấm tự động:
```bash
bash labs/cham.sh WEB L04 duong_dan/bai_cua_ban.js
```
