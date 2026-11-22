# Lab PAR L07 — Mô hình mái nhà (Roofline): đỉnh 20 nghìn tỉ phép/giây (TF/s), 2 TB/s, cường độ 2

Với đỉnh tính toán `20 TF/s` và băng thông bộ nhớ chính `2 TB/s`: tính điểm gãy (tỉ lệ đỉnh chia băng thông) và hiệu năng tối đa đạt được tại cường độ số học `AI = 2.0 FLOP/byte`.

Định dạng đầu ra (1 dòng):
`ridge_intensity=<1 chữ số> ai=<3 chữ số> max_tflops=<3 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh PAR L07 duong_dan/bai_cua_ban.py
```
