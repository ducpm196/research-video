# Lab DEN L04 — Tán điểm nóng bằng thêm hậu tố muối (salting)

Mô phỏng `400` sự kiện của một cửa hàng quá tải `'vip'` đổ dồn vào 1 phân vùng nếu giữ khoá thô `'vip'`, so với rải bằng hậu tố `'vip#' + str(i % 5)` qua `5` phân vùng. Tính tải phân vùng lớn nhất trước và sau khi rải muối.

Định dạng đầu ra (2 dòng):
`raw_hot_max=<số nguyên>`
`salted_max=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh DEN L04 duong_dan/bai_cua_ban.py
```
