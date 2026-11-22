# Lab PAR L10 — Gộp toàn phần theo vòng trên N=4 máy với lượng dữ liệu D=2.0 GB

Tính tổng dữ liệu gửi qua mạng mỗi máy theo công thức `2 * (N - 1) / N * D` với `N = 4` máy và kích thước mảng `D = 2.0 GB`.

Định dạng đầu ra (1 dòng):
`ring_allreduce_sent_GB=<2 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh PAR L10 duong_dan/bai_cua_ban.py
```
