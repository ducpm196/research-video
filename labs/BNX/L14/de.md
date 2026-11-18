# Lab BNX L14 — Thùng token của cổng API khi nhiều bên cùng gọi

Số liệu là số minh hoạ. Viết `mau.py` (chỉ dùng Python có sẵn). **Thùng token**: thùng chứa tối đa `cap` thẻ, đầy lúc đầu, mỗi giây thêm `rate` thẻ (không quá `cap`); mỗi yêu cầu cần 1 thẻ, không đủ thì bị từ chối. Dùng `Fraction` (`from fractions import Fraction as F`) để một phần mười giây không bị lệch như số thực.

Cổng cho mỗi bên `rate = 4` thẻ/giây, `cap = 6`. Viết hàm `nhan(rate, cap, times)` nhận danh sách thời điểm (giây) của các yêu cầu theo thứ tự và trả về số yêu cầu được nhận. Rồi:

1. **20 yêu cầu đến cùng lúc** (thời điểm 0): in `dong 20 yeu cau: nhan <a> tu choi <b>`.
2. **20 yêu cầu rải đều**, cách nhau 1/10 giây (thời điểm `0, 1/10, …, 19/10`): in `rai deu: nhan <số> can tren <số>`, trong đó cận trên là phần nguyên của `cap + rate × T` với `T = 19/10` (thời điểm yêu cầu cuối).
3. **50 bên giống hệt nhau** cùng gửi 20 yêu cầu cùng lúc, mỗi bên có thùng riêng: in `50 ben dong: <tổng nhận> qua cong, <tổng từ chối> tu choi`.
4. Nếu hậu phương chỉ xử lý được 120 yêu cầu/giây, số yêu cầu qua cổng ở bước 3 cần bao nhiêu giây để xử lý hết? In `hang cho <giây> giay neu hau phuong chiu 120 yeu cau/giay` (chia số yêu cầu qua cổng cho 120, in thẳng kết quả của phép chia `/`).

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L14 mau.py`. Đầu ra viết không dấu.
