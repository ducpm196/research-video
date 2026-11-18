# R7 ACB L00–L08 (vòng 7, đọc độc lập sau lần sửa thứ hai, P1 chặt): 9/9 bài — ghi lại bởi người điều phối từ tin nhắn của reader (aa965fa8615a7e117)

## 1. Tóm tắt
MUST 0 (9/9). P1=2: 5/9 chắc+vừa (L01, L03, L04, L05, L06; L00, L02, L07, L08 = 1; vòng 6 là 3/9); tính cả yếu 0/9. Tổng 42 mục: 0 chắc, 5 vừa, 37 yếu. P8=2 9/9; P9=2 9/9; spec khớp 9/9; SRT khớp `say` 9/9 (kiểm văn bản, chưa nghe audio); lab `cham.sh` ĐÚNG 9/9, khung "Kết quả mong đợi" trùng `mong_doi.txt` 9/9; 21/21 chương trình Python trên màn hình khớp; 179/179 `checks`; Go (L04, L08) chạy qua khung giả khớp hành vi bài nói; >40 số tính lại khớp. Mất gốc ĐỦ 9/9 (chắc+vừa); GẦN 9/9 nếu tính cả yếu. SHOULD 6.
`grep -i 'thấu chi lương'` trong `lessons/acb` và `_capture.html` = 0. Tiêu đề SVG L08 "Kiến trúc Tín dụng Thấu chi Cầm cố Sổ tiết kiệm". `requires` L06 = [L00, L01, L02, L03], L07 = [L00, L01, L02, L04] nhất quán với `assumes`; phụ thuộc ngoài `requires`: `==` của L07 (dạy ở L05), "sinh trắc học" của L08 (dạy ở L06). Bảng Go (L04, L08) và PL/SQL (L05) không tràn/đè/cắt; chỉ hai ô gãy dòng.

## 2. SHOULD
| Bài | Cảnh | Trích | Vấn đề | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L00 | concept.0 | "Cổng API là cửa duy nhất để ứng dụng gọi vào hệ thống." | khẳng định tuyệt đối | thêm "trong kiến trúc này" | PLAUSIBLE |
| L00 | chaytep.0 | "chưa có thì tạo thư mục mới và chép thư mục labs vào" | không nói lấy `labs/` ở đâu; bước `bash labs/cham.sh` của L01–L08 không làm được nếu thiếu kho | ghi nguồn `labs/` | CONFIRMED |
| L01 | concept.0 (khung 20) | hộp "Hạch toán: trừ và cộng sổ cái" | chữ chạm hai mép viền | co chữ/nới hộp | CONFIRMED |
| L03 | hook.1, concept, symbol.1, quymo | "cây-x-cu-l-đê-bê" | chữ phiên âm nằm trong `say` nên hiện nguyên trong phụ đề (7 dòng SRT) | để lexicon xử lý | CONFIRMED |
| L04 | example.3 (khung 50), quymo.0 | ô `.JSON(fiber.Map{"code": "409", ...})` gãy; tiêu đề cột "bi quan: người cuối chờ (" rồi `(n − 1) × 0,02 giây)` | dấu "(" lẻ cuối dòng | làm gọn | CONFIRMED |
| L08 | symbol.1 (khung 31) | ô Go `if err != nil {` gãy; say "Biến xê tê ích" | gãy dòng nhẹ + phiên âm trong phụ đề | như trên | CONFIRMED |
Chưa kiểm được nguồn (bài đã tự ghi rào): L06 TT 50/2024, TT 77/2025 (01/03/2026), VBHN 25, QĐ 2345/QĐ-NHNN, Luật 91/2025/QH15, ngưỡng 10/20 triệu; L08 TT 31/2024 Điều 10 (nhóm 2 = quá hạn 10–90 ngày), TT 37/2025; L00 lương tháng 13/thưởng 1–4 tháng khớp `resources/job/JD.md` (không kiểm được trang gốc); L01, L02, L04 cú pháp OFS, đặc tả NAPAS (MTI 0400/0420).

## 3. Mục chưa giảng (5 vừa, 0 chắc, 37 yếu)
Vừa (SỬA): L00 chaytep.0 "mở Git Bash trong thư mục chứa mau.py" (M; có gloss Git Bash, thiếu cách mở tại thư mục); L00 pitfall.0 "lớp bọc của Spring", "@Transactional" (A; lớp và giao dịch CSDL chưa định nghĩa, tới L05 mới có); L02 symbol.1 "0111 = 7, 0010 = 2" (A; giá trị vị trí 8-4-2-1 không giảng); L07 code.1, .6 `print(chu_ky == ky(goi))`, `if a[i] == b[j]:` (B; `==` chỉ dạy ở L05, ngoài `requires` của L07); L08 code.0 `han_muc = tien_so * ty_le // 100` (A; "bỏ phần lẻ" không giảng).
Yếu theo nhóm: Python nền lặp (`print`, `=`, `def`, `==`, `//`, `round`, `.replace`) — sửa một lần ở L00 gỡ nhiều mục; "sổ cái", "nút Redis" dùng từ L00 mà tới L04 mới định nghĩa; MTI; ISO 4217; SQL `TRUE`, chuỗi nháy đơn, `NOW()`; Go `//`, `==`, `{}`; "bản ghi", "bộ máy SQL"; `def ky`, `set()` đọc trước bảng giải; CCCD; chữ ký base64; "sinh trắc học" (L08), "gốc/giải chấp".

## 4. Người học kẹt ở đâu
L00 chaytep.0 (mở Git Bash tại thư mục; chép `labs`) rồi pitfall "lớp bọc của Spring"; L02 symbol.1 (nhị phân → hệ 16); L07 code.1 `==`; L08 code.0 `//`; các bài còn lại không kẹt cứng.
