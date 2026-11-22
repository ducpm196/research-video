# Lab CS115 L33 — Tổng ôn: quy tắc chọn mô hình theo cỡ mẫu và loại tác vụ

Cài hàm chọn mô hình `pick(n, kind)` theo quy tắc ba tầng: nếu tác vụ là giảm chiều vẽ hình (`kind == 'viz'`) thì chọn `'PCA/t-SNE'`; nếu là dữ liệu dạng bảng (`kind == 'tab'`): với cỡ mẫu `n < 1000` chọn `'Linear/Ridge'`, ngược lại (`n >= 1000`) chọn `'Tree/Boosting'`. Kiểm hàm với 3 kịch bản: `(500, 'tab')`, `(100000, 'tab')`, `(5000, 'viz')`.

Định dạng đầu ra (3 dòng):
`s1= <tên>`
`s2= <tên>`
`s3= <tên>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L33 duong_dan/bai_cua_ban.py
```
