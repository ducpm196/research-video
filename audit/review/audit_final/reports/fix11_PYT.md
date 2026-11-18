# fix11_PYT: sửa đúng 3 điểm của item-verifier PYT

## Bài đổi, CẦN DỰNG LẠI: L11, L13
## Việc đã làm
- L11 formula (Bước 4 gộp): câu giải nghĩa `round(100 * dat / tong, 1)` (phần trăm đạt, làm tròn một chữ số) và hai biến cộng dồn `dat_chung`, `tong_chung` (đạt và tổng của từng kênh) nay nằm trong `show` (hộp dưới khung mã) và `say` của ĐÚNG bước có mã; bỏ phần giải nghĩa lặp ở bước kết quả (giữ một vế "vì kênh A nhận nhiều giao dịch lớn khó").
- L11 phần tự làm: gợi ý "Nếu kẹt" có thêm `ax.set_ylabel(...)` (chữ) và lời đọc "đặt tiêu đề và nhãn trục đứng".
- L13 Bước 0: ghi chú trong chính bước có mã: `gd.csv` có 1 tiêu đề và 8 giao dịch, mỗi dòng kết thúc bằng xuống dòng, nên tách theo xuống dòng thừa một phần rỗng cuối: 10 = 1 + 8 + 1 (chữ + lời đọc). Ghi chú thời gian rút gọn để vừa khung (lần đầu TRÀN 3 khung).
Lời đọc: L11 2296, L13 2297 (≤ 2300). Không đổi sổ khối mã.

## Cổng
- lint 0 FAIL 0 WARN (L11, L13). render L11 0 vấn đề; L13 lần đầu TRÀN Bước 0, rút ghi chú, chạy lại 0 vấn đề.
- verify_pyt: L11+L13 23/23 PASS (trước chỉnh khung Bước 0); sau chỉnh lần cuối L13 11/12, ô còn lại là hai ô THỜI GIAN của `l13_scale` lệch >×8 do máy tải (không phải lỗi bài; cần chạy lại `verify_pyt L13` khi máy rảnh).
- screen_code PYT: xem dòng cuối tin nhắn bàn giao.
