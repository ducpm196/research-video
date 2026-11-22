# Lab MLO L03 — Kiểm thử bất biến hành vi và theo từng lát nhóm thay vì điểm tổng

Viết hàm chấm điểm `pred(s)` trả `1` nếu có `'tot'` ngược lại `0`, kiểm thử bất biến khi thử đủ 3 câu `'Binh is tot'`, `'Chi is tot'`, `'Dung is tot'`, và kiểm ngưỡng `>= 0.80` cho từng nhóm `{'maj': 0.94, 'min': 0.71}`.

Định dạng đầu ra:
`inv_pass=<1 hoặc 0> min_slice_pass=<1 hoặc 0>`

Chấm tự động:
```bash
bash labs/cham.sh MLO L03 duong_dan/bai_cua_ban.py
```
