# Lab DSY L00 [Mô phỏng phân tán] — Chi phí RPC nội bộ datacenter vs xuyên châu lục

Viết chương trình Python mô phỏng một yêu cầu gọi tuần tự `20` lần RPC (mỗi lần `0.5 ms` trong cùng DC hoặc `150 ms` xuyên lục địa), in đúng 3 dòng:
1. `local_20_rpcs_ms=10.0`
2. `cross_continent_20_rpcs_ms=3000.0`
3. `slowdown_factor=300x`

Chấm tự động:
```bash
bash labs/cham.sh DSY L00 duong_dan/bai_cua_ban.py
```
