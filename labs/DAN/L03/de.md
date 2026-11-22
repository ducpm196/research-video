# Lab DAN L03 — Hàm cửa sổ trong bảng dữ liệu: tổng lũy kế, chênh lệch và xếp hạng 4 ngày

Dùng thư viện `sqlite3` chạy hàm cửa sổ tính tổng lũy kế (`SUM`), hiệu so với dòng trước (`LAG`) và xếp hạng giảm dần (`RANK`) trên doanh thu 4 ngày `[(1,20), (2,50), (3,30), (4,60)]`.

Định dạng đầu ra (4 dòng, theo ngày d=1..4):
`d=<ngày> cum=<tổng lũy kế> diff=<chênh hôm trước hoặc None> rk=<hạng>`

Chấm tự động:
```bash
bash labs/cham.sh DAN L03 duong_dan/bai_cua_ban.py
```
