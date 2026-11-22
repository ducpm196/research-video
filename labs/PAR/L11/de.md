# Lab PAR L11 — Chồng truyền gradient với tính toán bước tiếp (C=120 ms, G=40 ms, chồng 25 ms)

So sánh hiệu suất mở rộng của cách chạy nối tiếp `C / (C + G)` với cách chồng được `25 ms` truyền thông vào tính toán `C / (C + G - overlap)` khi `C = 120`, `G = 40`, `overlap = 25`.

Định dạng đầu ra (1 dòng):
`seq_eff=<1 chữ số>% overlap_eff=<1 chữ số>%`

Chấm tự động:
```bash
bash labs/cham.sh PAR L11 duong_dan/bai_cua_ban.py
```
