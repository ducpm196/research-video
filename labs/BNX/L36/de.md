# Lab BNX L36 — Ước lượng tải, chọn thành phần và khoá lũy đẳng

Số liệu (số minh hoạ; khác ví dụ trong bài): **50 000 khách**, mỗi khách **4 giao dịch mỗi ngày**, hệ số đỉnh **8**, mỗi nút ghi chịu **500 giao dịch mỗi giây**. Hai cỡ: ×1 và ×1 000.

Viết `mau.py` in năm dòng:
1. Với mỗi cỡ (`x1`, `x1000`): `x<cỡ>: tb <trung bình>/s, dinh <đỉnh>/s, <số nút> nut -> <chọn>`.
   Trung bình = giao dịch mỗi ngày : 86 400 (chỉ làm tròn khi in, 1 chữ số thập phân); đỉnh = trung bình **chưa làm tròn** × hệ số đỉnh (làm tròn số nguyên khi in); số nút = làm tròn LÊN (đỉnh chưa làm tròn : 500).
   Nhân từ trung bình đã làm tròn sẽ ra số khác (ví dụ ×1 cho 18 thay vì 19).
   Chọn: 1 nút → `mot nut`; từ 2 tới 10 nút → `nhom nut`; trên 10 → `chia theo khoa`.
2. Một hàm chuyển tiền có khoá lũy đẳng, số dư ban đầu `A = 500`, `B = 0`. Gửi hai lần cùng khoá `K9`, chuyển 200 từ A sang B: in `lan 1: da chuyen`, `lan 2: trung khoa, bo qua`, rồi `so du: A=300 B=200`.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L36 mau.py`.
