# Lab DMS L15 — RSA trên số nhỏ bằng chương trình

Viết `rsa.py` (Python 3.11 trở lên); chạy: `python rsa.py`.

Chọn `p = 7`, `q = 13`, `e = 5`. In đúng sáu dòng (không dấu):
1. `n = <n>, L = <L>` — `n = p*q`, `L = (p-1)*(q-1)`
2. `khoa bi mat d = <d>` — `d` là số trong 1..L-1 có `(e*d) % L == 1` (duyệt từng d)
3. `ma hoa 10: <số>` — bản mã của bản tin 10: `10**e % n` (dùng `pow(10, e, n)`)
4. `giai ma <bản mã vừa tính>: <số>` — giải mã bản mã đó bằng `pow(bản_mã, d, n)`; phải ra lại 10
5. `ma hoa roi giai ma moi ban tin 0..90: <số bản tin ra đúng> / 91 dung` — thử MỌI bản tin x từ 0 đến 90 (mã hoá rồi giải mã) và đếm số bản tin được trả lại đúng
6. `phan tich n: <n> = <p nhỏ> x <q>` — tìm ước nhỏ nhất lớn hơn 1 của n bằng cách chia thử, rồi in n, ước đó và thương

Chấm: `bash labs/cham.sh DMS L15 rsa.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
