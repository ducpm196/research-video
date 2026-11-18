# fix11 BNK (tinh chỉnh sau người kiểm mục) — 2026-11-17

1. L13 `#`: hàng `# chú thích` (Dấu thăng mở đầu một chú thích Python, máy bỏ qua) đưa lên bảng TRƯỚC khối mã đầu tiên (bảng step 0 cảnh chay_that, cùng gán song song và biểu thức sinh); bảng sau chỉ còn hàng `==` (so hai MAC).
2. L02 quy_mo ×100: lời đọc "hộp mười kết nối thiếu, có thể bị kẹt" (khớp màn hình).
3. L12 chay_that.1: `focus` = [4, 4, 4] (khối kết quả chạy thật).
4. L13 formula.0: `focus` = [1, 1, 1, 1, 1, 2] (đoạn có TDES/AES sáng khi đọc TDES/AES; "Làm thử" sáng ở câu cuối).
5. Trên màn hình: L08 "(khoá chính: không cho hai dòng trùng)" ở ô ví dụ `tk TEXT PRIMARY KEY`; L13 "gọi thẳng API (API = cửa cho chương trình khác gọi vào)".

Lời đọc (đếm bằng mã): L02 2298; L08 2287; L12 2217; L13 2298 (≤ 2300). lint 0/0 (4 bài); verify_bnk 48/48; screen_gen rồi screen_code BNK: 107 khối, PASS 156, FAIL 0, STALE 0. `lv.py render` bị từ chối quyền, không đi vòng.

Requeue: L02, L08, L12, L13.
