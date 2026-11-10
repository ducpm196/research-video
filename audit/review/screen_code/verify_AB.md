# Kiểm độc lập SC1: phần A và phần B (2026-11-10), kèm việc người điều phối đã làm

Hai tác tử mới, chỉ đọc, làm theo `BRIEF_VERIFY_SC1.md`. Họ không dùng báo cáo của nhóm điền sổ làm bằng chứng; mọi mục đều tự đọc bài, đọc sổ, tự chạy.
- **Phần A**: SDP, WEB, SEC, DEN, CLD, CLC, SAR, DSY, PLC, SWF, DMS, CAS, TOC, MLO, CVI, GFX L12, JVA (L00/L11 + mẫu 15 khối + so toàn bộ 306 khối/110 nguồn bằng kịch bản riêng). Đã xét 184 mục sổ, 17 bài đổi.
- **Phần B**: DBS, INT, ACB, DAN, BNK, CS112, CSA, OSY, NET, BCH, ESY. Đã xét 120 mục sổ, 3 bài đổi.

**Kết luận chung của cả hai: không có MUST, không có mục NÉ** (không khối mã thật nào bị khai pseudo/other để né). Mọi bài đã đổi được xác nhận sửa đúng: mã chạy đúng, `say` khớp màn hình, `focus` không lệch, `checks` có số mới.

## Phát hiện và xử lý
| Phần | Khối/bài | Loại | Phát hiện (tóm tắt) | Xử lý |
|---|---|---|---|---|
| A | screen_code.py, kind output | LỎNG (cổng) | `_wild_in` so chuỗi con: màn hình "5" khớp nhầm máy in "50000" | **Đã sửa**: `_line_match` so cả dòng, "…" là đoạn lược, bỏ tiền tố `Tệp.java:N:`. `expect_stderr_contains` nhiều dòng hoặc có "…" cũng so cả dòng. Thêm 5 ca lỗi cấy → negative_controls 30/30 |
| A | JVA L08 pitfalls 1 1 | SHOULD (bài) | dòng NullPointerException bị cắt giữa chừng mà không có "…" (cắt cố ý vì 141 ký tự tràn khung) | **Đã sửa** `audit/jva/src/l08.py`: thêm " …"; verify_jva so cả dòng có "…" (`screen_lines_ok`) → 110/110; gen.py, lint 0/0, render 0, dựng lại |
| A | DBS L10 example 4 1 | (do cổng siết lộ ra) | màn hình hiện cột chi tiết của EXPLAIN QUERY PLAN; cổng so cả hàng "id\|parent\|…" | **Đã sửa sổ**: tuỳ chọn `field: -1`; `expect_stdout` của 4 0 vẫn kiểm đủ hai chuỗi chi tiết |
| A | SDP L02 example 0 0 | THIẾU | hai nhánh `raise` mới (hàm tạo âm, nạp ≤ 0) chưa được khẳng định | **Đã sửa sổ**: post kiểm `TaiKhoan(-1)`, `nap(0)`, `nap(-5)` báo đúng thông báo; `TaiKhoan().so_du == 0` |
| A | SDP L08 example 0 0 | CHE (nhẹ) | prelude tự dựng `Vuong(a)` khác bài rồi kiểm điều bài không nói | **Đã sửa sổ**: bỏ ca vuông; Vuong để trống |
| A | PLC L02 code 0 0 | CHE | con số quiz phụ thuộc term/atom do người điền sổ viết (màn hình chỉ tả bằng lời) | **Đã sửa sổ**: các số này thêm vào `unverified_claims` (độ trung thực INFERRED); `expr()` vẫn chạy nguyên văn |
| A | PLC L05 / src:PLC:L05_doi_tuong_minh | LỎNG | nguồn chép tay dòng 2, không gắn sha | **Đã sửa sổ**: `files:` đọc nguyên văn dòng 2 rồi exec |
| A | WEB L04 example 0 0 / 0 1 | LỎNG | trần 1500 ms rộng hơn "vài chục ms" | **Đã sửa sổ**: < 900 và < 500 ms, ghi lý do dung sai (máy bận, đo được 636 ms) |
| A | SDP L12 example | SHOULD (bài) | lời đọc "thêm một dòng ghi nhớ"; màn hình nay có thêm dòng `import functools` | **Mở** (SHOULD, không sai kiến thức; dòng ghi nhớ vẫn là một dòng decorator) |
| B | NET L07 / src:NET:L07_ls | LỎNG | bước 5 "B gửi tiếp qua A rồi C", nhưng nguồn chỉ đọc cây của S | **Đã sửa sổ**: chạy Dijkstra từ B, khẳng định đường B→A→C→D, độ dài 6 |
| B | BCH L08 sym / src:BCH:L08_escrow | THIẾU | điều kiện "đúng số tiền" và việc chuyển tiền không được mô hình | **Đã sửa sổ**: ghi vào `unverified_claims` |
| B | INT L02 example 1 0 / 2 0 | CHE | hai khối dùng hai stub khác nhau cho cùng biến `redis`; không kiểu Spring Data Redis thật nào có đủ setIfAbsent + set + delete | **Đã sửa sổ**: một stub chung `RedisBoc`; ghi `unverified_claims` rằng `redis` phải là lớp bọc của ứng dụng (SHOULD bài, **mở**) |
| B | CS112 / OSY nguồn twin | truy vết | `twin_of` chỉ ghi một khối trong khi nguồn kiểm nhiều khối | **Đã sửa sổ**: `twin_of` dạng danh sách (6 nguồn); cổng kiểm mỗi khối có thật |
| B | CSA L16 stage5 1 0 | SHOULD (bài) | "Mitigation: Enhanced IBRS"; nhân Linux hiện nay in "Mitigation: Enhanced / Automatic IBRS" (bugs.c) | **Mở** (bài đã ghi "một ví dụ kết quả") |
| B | ACB L04 symbol | SHOULD (PLAUSIBLE) | mốc mili giây với `NOW()` mà không nêu hệ quản trị (MySQL `NOW()` mặc định theo giây) | **Mở** |
