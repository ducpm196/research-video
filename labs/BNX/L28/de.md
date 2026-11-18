# Lab BNX L28 — Rút tiền có điều kiện so với đọc rồi ghi

Tài khoản có số dư **700** (số minh hoạ). Trong cơ sở dữ liệu lưu bản ghi JSON, lệnh cập nhật có điều kiện kiểu `{so_du: {$gte: số rút}}` chỉ trừ khi còn đủ tiền, **kiểm và trừ trong một bước**.

Viết `mau.py`:
1. Hàm `rut_co_dieu_kien(tk, so)` (tk là từ điển `{"so_du": …}`): nếu `so_du >= so` thì trừ và trả `1`, ngược lại không đổi và trả `0`. Gọi lần lượt rút 500, 500, 200 rồi in `co dieu kien: <ba số> con <số dư>`, trong đó ba số (mỗi số là 1 hoặc 0, theo thứ tự ba lần rút) cách nhau bằng MỘT dấu cách.
2. Mô phỏng sai lầm đọc-rồi-ghi: A và B cùng đọc số dư 700; A ghi `700 − 500`, rồi B ghi đè `700 − 500`. In
   `doc roi ghi: A doc 700, B doc 700, ghi 200 va 200, con 200 (mat 500)` — số mất = tổng đã chi (500 + 500) trừ số thật bị trừ.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L28 mau.py`.
