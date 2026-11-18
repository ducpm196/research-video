# Lab BNX L19 — Khe băm trong cụm 4 nút, khử trùng hạn 90 giây, danh sách đen (không cần Redis)

Viết `mau.py` (Python, chỉ thư viện chuẩn). Số liệu là số minh hoạ. Mọi thứ chạy ngay trong Python, không cần Docker hay Redis: ta mô phỏng đúng công thức của Redis Cluster.

**Phần 1 — khe và nút.** Cụm có **4 nút**, chia 16384 khe thành 4 dải bằng nhau (nút 1: 0–4095, nút 2: 4096–8191, nút 3: 8192–12287, nút 4: 12288–16383).
Khe của một khoá = `CRC16(khoá) mod 16384`, với CRC16 kiểu XMODEM (đa thức 0x1021, giá trị đầu 0). Trong Python có sẵn hàm này: `binascii.crc_hqx(khoa.encode(), 0)`.
Với 4 khoá theo thứ tự `loan:disb:B7`, `dedup:TX9`, `{acc}:5`, `{acc}:6` in mỗi dòng `<khoá> -> khe <k>, nut <n>`. Lưu ý quy tắc thẻ băm: khoá có `{acc}` thì chỉ chữ `acc` được đem băm — hai khoá cuối phải cùng khe.

**Phần 2 — khử trùng.** Viết lớp `Kho` mô phỏng lệnh `SET khoá 1 NX EX hạn` với đồng hồ giả `t`: nếu khoá còn sống (`thời điểm hết hạn > t`) trả `None`; ngược lại ghi `thời điểm hết hạn = t + hạn` và trả `"OK"`.
Gửi mã giao dịch `dedup:TX9` với hạn **90 giây** ở các giây 0, 45, 90, 91 và in `giay <t> <kết quả>`.

**Phần 3 — danh sách đen.** Mã truy cập có hạn dùng đến giây 1000 bị thu hồi ở giây 640. In `han danh sach den: <hạn của mục danh sách đen>` (bằng thời gian còn lại của mã).

In đúng 9 dòng như `mong_doi.txt`. Chấm: `bash labs/cham.sh BNX L19 mau.py`.
