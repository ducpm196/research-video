# fix10_PYT: sửa nhỏ chốt PYT theo vòng 7 (một tác tử, không thêm nội dung khác)

Nền vòng 7: MUST 0; P1 = 2 chắc+vừa 13/14; không mục chắc/loại B. Nguồn sửa `audit/pyt/src/lNN.py` -> `gen.py`.

## 1. Bài đổi, CẦN DỰNG LẠI
L00, L03, L05, L10, L11, L12, L13 (7 bài). Không đổi: L01, L02, L04, L06, L07, L08, L09. Không thêm/bớt step; lab không đổi.

## 2. Việc đã làm
| Bài | Mục | Cách sửa |
|---|---|---|
| L03 (vừa) | `for ma in sorted(tong):` | ghi chú ví dụ 2: `sorted(tong)` = danh sách các KHOÁ của từ điển, xếp tăng dần; lời đọc đổi tương ứng |
| L03 | "ns" | ghi chú scale: `ns = phần tỉ giây, µs = phần triệu giây` |
| L05 | "GB" | ghi chú hook: `MB = triệu byte, GB = tỉ byte` |
| L11 | `ax1.plot(du_lieu)` một đối số | ghi chú bước thang lôgarit: trục ngang tự lấy 0, 1, 2, … |
| L11 | `set_ylabel` ở phần tự làm | hàng bảng sym: `set_title`, `set_xlabel`, `set_ylabel` (tiêu đề, nhãn trục ngang, nhãn trục đứng) |
| L00 | lệnh chấm | bước kết quả mong đợi (chỉ L00): "chạy tệp chấm của bài (`bash` chạy một tệp lệnh); in ĐÚNG khi trùng" (chữ + lời); các bài sau đã có câu "in ĐÚNG khi trùng" ở cùng step |
| L10 | `if h["so_tien"]:` | tách khỏi câu chú thích (không còn "::"): "Dòng điều kiện `if h["so_tien"]:` coi chuỗi rỗng `""` (ô trống) là sai…" |
| L11 | `round(100 * dat / tong, 1)` | ghi chú và lời ở bước kết quả gộp: phần trăm đạt, làm tròn một chữ số; hai biến cộng dồn đạt và tổng của cả hai loại |
| L12 | đột biến | nêu hai cách đổi dấu (ví dụ `<` thành `<=`, hoặc `<` thành `>`) rồi 3 × 2 = 6, sáu chỗ hằng × 2 = 12, cộng 18 (chữ + lời); 18/4/14/12/14 không đổi |
| L13 | `10` ở Bước 0 | ghi chú và lời: 10 = 1 tiêu đề + 8 giao dịch + 1 phần rỗng cuối |

## 3. Độ dài lời đọc
L00 2290, L01 2196, L02 2297, L03 2295, L04 2285, L05 2273, L06 2287, L07 2178, L08 2290, L09 2143, L10 2219, L11 2299, L12 2299, L13 2294 (≤ 2300). Cắt để bù: câu mở "Chào bạn", câu giải thích lặp trên màn hình (L00, L11, L12, L13), câu cuối quiz (L11).

## 4. Cổng thật
- `lv.py lint`: 0 FAIL, 0 WARN ở cả 14 bài. `curriculum`: 14 bài, 0 lỗi. `test_e52`: 0 FAIL.
- `lv.py render`: L00 L03 L05 L11 L12 0 vấn đề ngay lần đầu. L10 (bước kiểm) và L13 (Bước 0) lần đầu TRÀN do chính ghi chú mới; đã sửa: L10 tách bước kiểm thành hai step (khung mã + ghi chú đọc; hộp kết quả 1 450 000 / 3 000 000 / 300 000 / 4 750 000), L13 rút ghi chú Bước 0. Chạy lại: **L10 và L13 0 vấn đề**. Không xem lại PNG vòng này (chỉ chữ ghi chú).
- `verify_pyt` L00 L03 L05 L10 L11 L12 L13: **117/117 PASS** (không còn ô thời gian lệch lần này).
- `screen_code check --course PYT`: PASS 544 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 (không thêm khối mã; step mới của L10 nằm cuối cảnh nên khoá không đổi).
- Lời đọc cuối: L10 2219, L13 2294 (cả khoá ≤ 2300).
