# Lab ACB L05 — Sắp thứ tự khoá, kiểm vòng chờ và ghép số dư đầu đoạn

Số liệu (số minh hoạ, khác ví dụ trong bài):
- Hai lệnh chuyển tiền: A cần khoá tài khoản **7 rồi 3**, B cần khoá **3 rồi 7**. Lịch xin khoá xen kẽ cố định: A xin khoá đầu của mình, B xin khoá đầu của mình, A xin khoá thứ hai, B xin khoá thứ hai. Một tiến trình xin khoá đang do người khác giữ thì phải chờ người đó; tiến trình đang chờ không giữ thêm khoá nào.
- Có **vòng chờ** khi A chờ B **và** B chờ A.
- Sao kê chia 5 đoạn, số dư đầu kỳ **20**, tổng phát sinh từng đoạn `4, -6, 3, -2, 5` (triệu).
- Lô **2 500** lệnh chia khối **500** lệnh.

Viết `mau.py` (Python 3) in đúng sáu dòng:

1. `A khoa: <danh sách khoá của A sau khi sắp tăng dần>` (dạng `[3, 7]`), 2. `B khoa: …`
3. `vong cho khi khong sap: co|khong` — chạy lịch với thứ tự khoá gốc.
4. `vong cho khi sap: co|khong` — chạy lịch với thứ tự đã sắp.
5. `dau doan: <danh sách số dư đầu năm đoạn> cuoi: <số dư cuối kỳ>`.
6. `so khoi: <số khối>` (chia làm tròn lên).

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh ACB L05 mau.py`.
