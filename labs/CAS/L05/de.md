# Lab CAS L05 — Knight Capital (2012): tốc độ lỗ trên 460 triệu / 45 phút và xác suất sót triển khai 8 máy

Dùng số liệu sự cố năm 2012 (`460 triệu đô` trong `45 phút`) tính tốc độ lỗ mỗi phút, đồng thời tính xác suất có ít nhất 1 trên `8` máy chủ bị bỏ sót nếu mỗi máy có xác suất thao tác tay sai `p = 0.05` (`1 - (1 - p)^8`).

Định dạng đầu ra (1 dòng):
`loss_per_min_M=<1 chữ số> prob_any_miss=<4 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CAS L05 duong_dan/bai_cua_ban.py
```
