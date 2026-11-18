# R7 PYT L00–L13 (vòng 7, đọc độc lập sau lần sửa thứ ba, P1 chặt): 14/14 bài — ghi lại bởi người điều phối từ tin nhắn của reader (a773950839c4f9ffa)

## 1. Tóm tắt (P1=2 chắc+vừa: vòng 4 0/14 → 5 13/14 → 6 9/14 → 7 13/14)
MUST 0 (14/14). P1=2: 13/14 chắc+vừa (L03 = 1) — ĐẠT ngưỡng (93%); tính cả yếu 10/14 (L00, L03, L05, L11 = 1). Tổng 5 mục: 0 chắc, 1 vừa (L03), 4 yếu; không có loại B. P8=2 14/14; P9=2 14/14; spec khớp 14/14; SRT khớp `say` 14/14 (kiểm văn bản, chưa nghe audio); lab `cham.sh` ĐÚNG 14/14 (L08 `pip install` cần mạng, chỉ đọc; lời giải vẫn ĐÚNG trên `.venv-pyt`); 263/263 khối `>>>` khớp; 174/174 `checks`; 94 cặp mã↔đầu ra (74 khớp ngay, 20 lệch do cách chạy, đã chạy lại tay khớp); số đo theo máy chậm 5–10 lần (bài ghi "số minh hoạ") nhưng mọi tỉ lệ/hình dạng tái hiện. Mất gốc ĐỦ 14/14. 70 khung hình đã xem: không tràn/đè/cắt.
Sửa gần đây đạt: L05 `iterdir` bảng đọc trước khung mã; L06 "thấu chi" định nghĩa ở practice#1; L10/L13 "chuỗi rỗng tính là sai", `groupby`, `assert` có giải thích; L11 bảng đọc ba dòng mở gói; L12 "18" và 11 001 000 đúng (kiểm thử đột biến: 18 cách, 4 tương đương, 14 sai, 7 ca bắt 12, thêm 1 099 999 và 11 001 000 bắt 14/14).

## 2. SHOULD (4)
| Bài | Cảnh | Trích | Vấn đề | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L10 | check#1 | `if h["so_tien"]::` | chú thích dưới mã in hai dấu hai chấm liền | viết `if h["so_tien"]:` rồi xuống dòng nói nghĩa | CONFIRMED |
| L11 | formula#7 | "Vì vậy ta chạy và đọc kết quả thật ở bước kế." | khối 11 dòng chỉ 1 câu đọc; `round(100 * dat / tong, 1)` và hai biến cộng dồn không được đọc | thêm 1 câu | CONFIRMED |
| L12 | example#5 | "ba dấu so sánh, mỗi dấu đổi hai cách" | không nói hai cách đổi là gì, không tự dựng lại được 18 | ghi rõ ví dụ `<` → `<=` và `<` → `>` | CONFIRMED |
| L13 | formula#1 (Bước 0) | `open("gd.csv", …).read().split("\n")` → "10 True True" | đọc `gd.csv` trước khi tệp được giới thiệu ở formula#4 | chuyển formula#4 lên trước hoặc chú thích 10 = 1 tiêu đề + 8 giao dịch + 1 dòng trống | CONFIRMED |

## 3. Mục chưa giảng (1 vừa, 4 yếu)
Vừa: L03 example#2 `for ma in sorted(tong):` (A; `sorted` trên từ điển trả danh sách khoá đã xếp; manh mối lời "duyệt các mã theo thứ tự"; bảng sym#3 chỉ có `sorted(x, key=f)` cho danh sách). Yếu: L00 practice#2 `bash labs/cham.sh PYT L00 lai_tk.py` (lặp mọi bài, tính một lần); L03 scale#1 `≈ 110 ns` (M; `ns` định nghĩa ở L04 hook#2); L05 hook#1, scale#1 `GB` (M); L11 formula#9, pitfalls#4 `ax1.plot(du_lieu)` một đối số (A); L11 `set_ylabel` chỉ có trong đề lab.

## 4. Người học kẹt ở đâu
Không kẹt cứng. L00 practice#2 lệnh chấm; L03 example#2 `sorted(tong)`; L11 phần tự làm (đề đòi nhãn trục y, màn hình chỉ có `set_xlabel`) và formula#9; L13 formula#1 (đọc `gd.csv` trước khi tệp được hiện).
