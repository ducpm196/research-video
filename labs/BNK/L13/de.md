# Lab BNK L13 — Phép kiểm Luhn cho số thẻ thử

Phép kiểm Luhn: đi từ **phải sang trái**, chữ số ở vị trí 0 (cuối) giữ nguyên, chữ số ở vị trí 1, 3, 5, … **nhân đôi** (kết quả quá 9 thì trừ 9); cộng tất cả; **tổng chia hết cho 10** thì hợp lệ.

Viết chương trình `luhn_lab.py` (Python):
1. Hàm `luhn(so)` trả `True` hoặc `False` theo phép kiểm trên.
2. Với thẻ thử `the = "5500005555555559"`: in `luhn(the)`, rồi in `luhn` của số đó khi đổi chữ số cuối thành `8`, rồi in số thẻ đã che (giữ 6 số đầu, 4 số cuối, 6 dấu `*` ở giữa).

Kết quả đúng ba dòng: `True`, `False`, `550000******5559`. Chạy: `python luhn_lab.py`. Chấm: `bash labs/cham.sh BNK L13 luhn_lab.py`.
