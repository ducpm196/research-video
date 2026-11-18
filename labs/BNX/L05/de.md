# Lab BNX L05 — Lịch xoay vòng chứng chỉ

Hôm nay là **15/6/2026**. Ba chứng chỉ dịch vụ (số minh hoạ) cho dưới dạng (tên, ngày cấp, hạn dùng tính bằng ngày):

```python
CHUNG_CHI = [("so_cai", "2026-04-20", 60),
             ("bao_cao", "2026-01-10", 365),
             ("doi_soat", "2026-05-01", 30)]
```
Quy tắc của bài: **ngày hết hạn** = ngày cấp + hạn; **ngày xoay** = ngày cấp + (hạn × 2 // 3) ngày (xoay khi đã dùng 2/3 thời hạn).
Chứng chỉ **đã hết hạn** nếu hôm nay đứng sau ngày hết hạn; **cần xoay** nếu chưa hết hạn nhưng hôm nay đã tới (hoặc qua) ngày xoay, kèm số ngày còn lại tới hết hạn; còn lại là **chưa đến hạn xoay**.

Viết `mau.py` (dùng `datetime.date` và `timedelta` của Python) in mỗi chứng chỉ một dòng, rồi dòng đếm số chứng chỉ phải xử lý (đã hết hạn hoặc cần xoay):
```
<tên>: xoay <ngày>, het han <ngày>: <da het han | can xoay, con N ngay | chua den han xoay>
So chung chi can xu ly: <số>
```
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L05 mau.py`.
