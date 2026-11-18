# Lab DMS L19 — Xác suất rời rạc: ngày sinh, va chạm băm, kỳ vọng bằng chương trình

Viết `xacsuat.py` (Python 3.11 trở lên); chạy: `python xacsuat.py`.

In đúng năm dòng (không dấu):
1. `P(trung ngay sinh) voi 30 nguoi: <số>` — xác suất có ít nhất hai người trùng ngày sinh trong 30 người, 365 ngày rải đều (tính `1 − tích` các tỉ số `(365 − i) / 365`, `i` từ 0 đến 29), làm tròn 4 chữ số thập phân (`round(x, 4)`)
2. `so nguoi nho nhat de P >= 0.5 voi 1000 ngay: <số>` — số người n nhỏ nhất để xác suất trùng đạt ít nhất 0,5 khi có 1000 "ngày" (vòng lặp nhân dần tỉ số không trùng, dừng khi tích không trùng ≤ 0,5)
3. `ky vong so cap va cham 200 khoa vao 10000 o: <số>` — `C(200, 2) / 10000` (mỗi cặp va chạm với xác suất 1/10000, kỳ vọng của tổng bằng tổng kỳ vọng), in bằng `print(..)` của số thực
4. `so diem co dinh trung binh cua 7 vat: <số>` — trung bình số vật ở đúng chỗ cũ trên MỌI hoán vị của 7 vật (`itertools.permutations(range(7))`: 5040 hoán vị), in số thực
5. `P(khong trung) 5 nguoi, 10 ngay (liet ke het): <số>` — liệt kê mọi bộ 5 giá trị từ 10 "ngày" (`product(range(10), repeat=5)`, 100000 bộ), đếm các bộ đôi một khác nhau, chia cho 100000

Chấm: `bash labs/cham.sh DMS L19 xacsuat.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
