# Lab BNX L03 — Ký và kiểm một JWT HS256

Viết `mau.py` (Python) gồm bốn việc, số liệu là số minh hoạ:

1. Khoá bí mật `KHOA = b"khoa-lab-l03"`.
2. Hàm `b64u(b)`: base64url của các byte, **bỏ dấu `=` ở cuối** (dùng `base64.urlsafe_b64encode` rồi `.rstrip(b"=")`, rồi `.decode()`).
3. Hàm `ky(dau, than)` nhận hai chuỗi byte: ghép `b64u(dau) + "." + b64u(than)` làm chuỗi vào, tính HMAC-SHA256 của chuỗi vào bằng `KHOA` (`hmac.new(KHOA, vao.encode(), hashlib.sha256).digest()`), trả `vao + "." + b64u(mac)`.
4. Hàm `kiem(ma, aud, bay_gio)` tách ba phần, **tính lại chữ ký** và so bằng `hmac.compare_digest`; rồi đọc phần thân (thêm lại `=` cho đủ bội số 4 trước khi giải mã, rồi `json.loads`). Trả đúng một trong các chữ, theo thứ tự kiểm:
   - `chu ky sai`; nếu chữ ký đúng thì
   - `het han` khi `bay_gio >= exp`; nếu chưa hết hạn thì
   - `sai nguoi nhan` khi `aud` của phần thân khác `aud` truyền vào; còn lại là
   - `nhan`.

Sau các hàm, chép nguyên văn đoạn thử (in năm dòng):

```python
dau = b'{"alg":"HS256","typ":"JWT"}'
than = b'{"sub":"u42","aud":"app-b","exp":2000}'
ma = ky(dau, than)
print(ma.split(".")[2])
print(kiem(ma, "app-b", 1999))
print(kiem(ma, "app-b", 2000))
d, t, s = ma.split(".")
sua = b64u(than.replace(b"u42", b"u43"))
print(kiem(d + "." + sua + "." + s, "app-b", 1000))
print(kiem(ma, "app-c", 1000))
```

Đầu vào chữ `import` đầu tệp: `import base64, hmac, hashlib, json`. Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L03 mau.py`.
