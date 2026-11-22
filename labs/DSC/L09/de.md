# Lab DSC L09 — Câu cá dữ liệu: xác suất báo giả toàn họ (FWER) và hiệu chỉnh Bonferroni

Với `15` lần kiểm định ở mức `0.05` khi không có hiệu ứng thật, tính xác suất ít nhất 1 báo động giả toàn họ (`FWER = 1 - (1 - 0.05)^15`) và kết quả sau khi chia đều ngưỡng theo hiệu chỉnh Bonferroni (`0.05/15`).

Định dạng đầu ra:
`raw_fwer=<3 chữ số> bonf_alpha=<4 chữ số> fwer_bonf=<3 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh DSC L09 duong_dan/bai_cua_ban.py
```
