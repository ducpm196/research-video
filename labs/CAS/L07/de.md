# Lab CAS L07 — Cloudflare (2019): bùng nổ bậc ba O(n^3) của mẫu `.*.*=.*` khi quét mọi vị trí đầu

Tính tổng số bước quay lui tích lũy khi bộ khớp không neo thử lại ở mọi vị trí bắt đầu `s = 0..n-1` trên chuỗi `n = 150` ký tự thiếu dấu `'='`: mỗi vị trí `s` xét `m*(m+1)//2` với `m = n - s`, so với `n` bước tuyến tính.

Định dạng đầu ra (1 dòng):
`n=<số nguyên> cubic_steps=<số nguyên> ratio=<số nguyên>x`

Chấm tự động:
```bash
bash labs/cham.sh CAS L07 duong_dan/bai_cua_ban.py
```
