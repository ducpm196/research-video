# Lab CVI L00 — Ảnh số, đơn vị MiB và độ sáng tuyến tính

Cho một khung ảnh màu `1280 × 720`, 3 kênh, mỗi kênh 1 byte: tính tổng số byte và đổi sang `MiB` (biết `1 MiB = 1024^2 byte`). Sau đó chuẩn hoá giá trị `sRGB = 96` về `[0, 1]` (`u = s / 255`) và đổi sang độ sáng tuyến tính theo quy tắc sRGB chuẩn (`u / 12.92` nếu `u <= 0.04045`, ngược lại dùng phần hiệu chỉnh gamma `((u + 0.055)/1.055)^2.4`).

Định dạng đầu ra (1 dòng):
`bytes=<số nguyên> MiB=<2 chữ số> linear_96=<3 chữ số>`
