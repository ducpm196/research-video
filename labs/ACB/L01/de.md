# Lab ACB L01 — Ráp bản tin OFS, ghép trả lời theo mã và định luật Little

Số liệu (số minh hoạ, khác ví dụ trong bài). Chuyển **1 250 000** đồng từ tài khoản `5550001111` sang `6660002222`; người dùng `INPUTTER`, mật khẩu che bằng `******`, mã công ty `VN0010002`; mã giao dịch để trống (hai dấu phẩy liền nhau). Ba yêu cầu đang chờ: `a1` (2tr), `a2` (1tr), `a3` (7tr); ba trả lời đến theo thứ tự `a3 OK`, `a1 OK`, `a2 LOI`. Tải **2 000** lệnh mỗi giây, độ trễ **45** mi li giây.

Viết `mau.py` (Python 3, chỉ `print`, hàm, vòng lặp, từ điển) in đúng các dòng:

1. Hai dòng cho bản tin (một bản tin, in làm hai dòng cho vừa màn hình): `ofs dau: <phần đầu>` và `ofs cap: <phần cặp>`. Bản tin theo khung `FUNDS.TRANSFER,ACTR/I/PROCESS,<người dùng>/<mật khẩu che>/<công ty>,,<cặp tên=giá trị nối bằng dấu phẩy>`; phần đầu là mọi thứ tới và gồm hai dấu phẩy liền nhau, phần cặp là phần còn lại; ba cặp theo thứ tự `DEBIT.ACCT.NO`, `CREDIT.ACCT.NO`, `DEBIT.AMOUNT`.
2. `so truong: <số cặp tên=giá trị trong bản tin>` — đếm từ bản tin vừa ráp.
3. Với mỗi trả lời, theo thứ tự đến: `<mã> <yêu cầu> -> <kết quả>`; rồi `con cho: <số yêu cầu còn chờ>`.
4. `dang cho: <số>` — tải nhân độ trễ (mi li giây) chia nguyên cho 1000.
5. `ket noi tuan tu: <số>` — mỗi kết nối làm `1000 // 45` lệnh mỗi giây; số kết nối làm tròn lên.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh ACB L01 mau.py`.
