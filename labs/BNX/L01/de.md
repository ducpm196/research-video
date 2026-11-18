# Lab BNX L01 — Kiểm một yêu cầu rút tiền theo lược đồ

Một API rút tiền tại máy ATM có lược đồ yêu cầu (số minh hoạ):

| trường | bắt buộc | luật |
|---|---|---|
| `soThe` | có | chuỗi đúng 16 chữ số |
| `soTien` | có | số nguyên, từ 50000 trở lên |

Viết `mau.py` (Python) gồm hàm `kiem(req)` trả về **danh sách lỗi** (rỗng nếu hợp lệ), dùng đúng các chuỗi lỗi sau (không dấu):

- thiếu số thẻ: `soThe: thieu`; sai dạng (không phải chuỗi 16 chữ số): `soThe: sai dang`
- thiếu số tiền: `soTien: thieu`; không phải số nguyên hoặc nhỏ hơn 50000: `soTien: phai la so nguyen >= 50000`

Với số thẻ dùng `re.fullmatch` trên chuỗi, kiểm `type(v) is str` trước. Với số tiền kiểm `type(t) is int` (chuỗi `"200000"` là sai kiểu).

Sau hàm, chép nguyên văn đoạn chạy năm yêu cầu thử:

```python
thu = [
    {"soThe": "1234567890123456", "soTien": 200000},
    {"soThe": "123456", "soTien": 200000},
    {"soThe": "1234567890123456", "soTien": 20000},
    {"soThe": "1234567890123456", "soTien": "200000"},
    {"soTien": 200000},
]
for i, req in enumerate(thu, 1):
    loi = kiem(req)
    print(i, 400 if loi else 201, "; ".join(loi) or "-")
```

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L01 mau.py`.
