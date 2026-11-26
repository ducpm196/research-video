# Lab TOC L10 — Cài bộ mô phỏng máy Turing vạn năng U hỗ trợ đọc, ghi và dịch đầu đọc

Cài bộ mô phỏng máy Turing vạn năng U nhận bảng luật `(trạng_thái, ký_tự_đọc) -> (trạng_thái_mới, ký_tự_ghi, hướng_dịch)` (hướng `'R'` sang phải, `'L'` sang trái, `'S'` đứng yên). Chạy máy đảo mọi bit trên băng `'10110'` cho tới khi gặp ô trống `'_'` thì dừng ở `'H'`.

Định dạng đầu ra (1 dòng):
`tape_out=<chuỗi> steps=<số nguyên> final_state=<tên trạng thái>`

Chấm tự động:
```bash
bash labs/cham.sh TOC L10 duong_dan/bai_cua_ban.py
```
