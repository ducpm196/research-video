# Lab DMS L14 — Nghịch đảo mô-đun, Fermat nhỏ và lũy thừa nhanh bằng chương trình

Viết `luythua.py` (Python 3.11 trở lên); chạy: `python luythua.py`.

In đúng năm dòng (không dấu):
1. `nghich dao cua 7 theo mo-dun 40: <số>` — số b trong 1..39 có `(7*b) % 40 == 1` (duyệt từng b)
2. `nghich dao cua 12 theo mo-dun 18: khong co` — nếu không có b nào trong 1..17 thoả `(12*b) % 18 == 1` thì in `khong co` (viết chương trình in `<số>` nếu có, `khong co` nếu không; với 12 và 18 là `khong co` vì ước chung lớn nhất là 6)
3. `6^100 mod 19: <a> <b>` — `a` tính bằng lũy thừa nhanh (bình phương liên tiếp, lấy dư mỗi bước, tự viết vòng `while`); `b` tính bằng Fermat nhỏ: 19 nguyên tố nên `6^18` đồng dư 1, hạ số mũ 100 thành `100 % 18`, rồi tính `6` mũ số đó theo mô-đun 19. Hai số phải bằng nhau.
4. `so phep nhan cua luy thua nhanh voi mu 1000: <số>` — đếm số lần nhân trong vòng `while` của lũy thừa nhanh khi số mũ là 1000 (mỗi vòng có một phép bình phương, và thêm một phép nhân vào kết quả khi bit thấp của số mũ bằng 1)
5. `2^560 mod 561: <số>, uoc nho nhat cua 561: <số>` — tính 2 mũ 560 theo mô-đun 561 bằng lũy thừa nhanh; rồi tìm ước nhỏ nhất lớn hơn 1 của 561 bằng cách thử chia (561 là hợp số nhưng vẫn qua phép thử Fermat với cơ số 2)

Chấm: `bash labs/cham.sh DMS L14 luythua.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
