# Lab AIF L02 — Hàm đánh giá cho A*: đếm ô sai chỗ h1 và khoảng cách Manhattan h2

Với trạng thái trò xếp 8 ô số `[0,6,2,1,3,5,7,4,8]` (đích `[0,1,2,3,4,5,6,7,8]`, chi phí thật tối ưu `h* = 10`), tính `h1` (số ô khác 0 sai vị trí), `h2` (tổng khoảng cách Manhattan), và kiểm tra tính chấp nhận được (`h1 <= h2 <= 10`).

Định dạng đầu ra:
`h1=<số> h2=<số> admissible=<1 hoặc 0>`

Chấm tự động:
```bash
bash labs/cham.sh AIF L02 duong_dan/bai_cua_ban.py
```
