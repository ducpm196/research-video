# Lab BNX L31 — Dựng đường đi từ nhật ký và tính tốc độ đốt ngân sách

Dưới đây là sáu dòng nhật ký JSON (số minh hoạ), **theo thứ tự đến kho**, không theo thứ tự thời gian (`t` là mili giây của đồng hồ giả):

```
{"t":500,"dv":"gw","cid":"c9","ev":"nhan"}
{"t":505,"dv":"gw","cid":"d4","ev":"nhan"}
{"t":520,"dv":"pay","cid":"c9","ev":"tru"}
{"t":526,"dv":"pay","cid":"d4","ev":"loi"}
{"t":560,"dv":"gw","cid":"c9","ev":"tra"}
{"t":545,"dv":"led","cid":"c9","ev":"ghi"}
```

Viết `mau.py` (chỉ thư viện chuẩn, dùng `json`):
1. Đọc sáu dòng, lọc những dòng có `cid` là `c9`, **sắp theo `t`**, in `c9: <dv>:<ev> > <dv>:<ev> > …`.
2. In `c9 mat <số> ms` (từ sự kiện đầu tới sự kiện cuối của c9).
3. Đếm số dòng có `ev` là `loi` trong cả sáu dòng, in `so dong loi: <số>`.
4. Mục tiêu độ sẵn sàng (SLO) 99%; trong 200 yêu cầu có 6 yêu cầu lỗi. **Tốc độ đốt** = tỉ lệ lỗi chia ngân sách lỗi (1 − SLO). In `toc do dot: <số>` làm tròn 1 chữ số thập phân.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L31 mau.py`.
