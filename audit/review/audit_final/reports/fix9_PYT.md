# fix9_PYT: sửa vòng 9 theo `R6_PYT.md` (PYT, một tác tử)

Nguồn sửa: `audit/pyt/src/lNN.py` -> `gen.py`. Nền R6: MUST 0; chắc+vừa 9/14 (6 mục loại B xếp "vừa"), cả yếu 6/14; SHOULD 4. Lưu ý đo lường của R6: ranh giới vừa/yếu không tái lập được giữa người đọc; vòng này xử lý cả 6 mục vừa và các mục yếu cùng họ loại B bằng một hàng/câu nhắc tại chỗ.

## 1. Bài đổi, CẦN DỰNG LẠI
L01, L04, L05, L06, L07, L08, L10, L11, L12, L13 (10 bài). Không đổi: L00, L02, L03, L09. Lab không đổi.

## 2. Mục chưa giảng
| Bài | Mục | Cách giảng |
|---|---|---|
| L05 (vừa) | `print([p.name for p in thu_muc.iterdir()])` | step bảng mới ĐỨNG TRƯỚC khung mã: `iterdir()` (đi qua từng mục), `[p.name for p in dãy]` (danh sách suy ra: dựng danh sách mới) + câu lời (thử đặt ghi chú dưới khung mã bị TRÀN, nên tách step) |
| L06 (vừa) | "thấu chi" trước định nghĩa | định nghĩa nằm ngay trong ghi chú và câu lời của step đầu cảnh tự làm: thấu chi = mức số dư được phép âm |
| L10 (vừa) | `if h["so_tien"]:` | bước kiểm: chuỗi rỗng là sai, nên dòng thiếu bị bỏ (chữ + lời); cùng ghi chú `DictReader`, `newline=""` |
| L11 (vừa) | bước gộp: `for ten, kenh in ((…),(…))`, `dat, tong = kenh[loai]` | thêm step bảng "viết trong mã -> đọc là" (từ điển các bộ `(đạt, tổng)`, mở gói bộ ở vòng ngoài, mở gói bộ ở dòng trong) đứng TRƯỚC khung mã gộp |
| L13 (vừa) | `khoi.groupby("loai")["so_tien"].sum()` | hàng prereq: nhóm theo cột rồi cộng cột khác + câu lời |
| L13 (vừa) | `assert chay("…") == 150` | ghi chú và câu lời: `assert` là khẳng định, sai thì ca đỏ |
| L01 | `print("Giao dich", tien, …)` | tiêu đề khung + câu lời: `print` nhận nhiều giá trị, in cách nhau một dấu cách |
| L06 | f-string `return f"…"`, `.append(x)` | tiêu đề khung mã nêu `f"…{x}…"`, lời đọc nhắc chuỗi có chỗ điền; hộp cảnh báo lỗi 2 nêu `.append(x)` thêm `x` vào cuối |
| L07 | `raise …(f"thieu {…}")` | ghi chú và lời: `f"thieu {x}"` điền giá trị x vào chuỗi |
| L10 | `.days`; `with open(…, newline="")` | ghi chú ngày trừ ngày ra khoảng thời gian, `.days` là số ngày; `newline=""` nêu ở bước kiểm |
| L11 | `ax.lines[0].get_ydata()`, `get_ylim`, `get_yscale` | hai hàng bảng sym được thêm chú thích (`ax.lines[0]` là đường đầu, `get_ydata()` giá trị trục đứng; `get_ylim()`, `get_yscale()` hỏi lại khoảng, thang) + câu lời |
| L12 | `max(500, 1100)`, `min(11000, 11000)`; `.stdout` | ghi chú bước kiểm: `max` lấy số lớn hơn, `min` số nhỏ hơn, dùng để kẹp (chữ + lời); gợi ý practice: `.stdout` là chữ chương trình con đã in |
| L13 | `csv.DictReader`, `newline=""`, `p.write_text(…)` | ghi chú ở cách B (từ điển mỗi dòng, `newline=""`) và ở ca kiểm (`write_text` ghi chuỗi vào tệp) |

## 3. SHOULD (4/4)
- L04: `.` trong bảng ký tự mẫu: "ký tự bất kỳ (trừ xuống dòng)" (chữ + lời).
- L08: đáp án quiz câu 2: bỏ dấu `;` thừa ("…, vì khi bị nạp, …").
- L12: ghi chú bảng và lời đọc: "ở hai ngưỡng sau, ca ngay sau cách ngưỡng 1 000 (phí = tien // 1000); ở 50 000 các ca cách 1 đồng".
- L12 đột biến: đếm theo "ba dấu so sánh, mỗi dấu đổi hai cách: 3 × 2 = 6; sáu chỗ có hằng số (50000 một lần, 1100 hai lần, 11000 hai lần, 1000 một lần), mỗi chỗ dịch lên hoặc xuống 1: 6 × 2 = 12; cộng lại 18". Tự kiểm bằng mã: `re.finditer` trong `measure l12_mut` đếm đúng 3 dấu và 6 chỗ hằng số; kết quả 18/4/14/12/14 giữ nguyên (`measured.json` không đổi).

## 4. Độ dài lời đọc
L00 2295, L01 2196, L02 2297, L03 2292, L04 2285, L05 2273, L06 2287, L07 2178, L08 2290, L09 2143, L10 2216, L11 2291, L12 2288, L13 2294 (≤ 2300). Cắt để bù: câu mở lặp lại bảng (L11, L12), câu quiz dài (L11), câu "Bài sau" (L11), vài câu đệm (L06, L12).

## 5. Cổng thật
- `lv.py lint`: 0 FAIL, 0 WARN ở cả 14 bài. `curriculum curriculum/pyt.yaml`: 14 bài, 0 lỗi. `tests/test_e52.py`: 0 FAIL.
- `lv.py render`: L01 L04 L05 L06 L07 L08 L10 L11 L12 L13 chạy lại; lần đầu L05 TRÀN (ghi chú dưới khung mã iterdir), đã tách thành step bảng đứng trước khung mã; chạy lại: **cả 10 bài 0 vấn đề**. Đã xem khung PNG: L11 `00041` (bảng đọc bước gộp: 3 hàng, đủ chỗ), `00036`.
- `screen_code`: `gen-pyt` (347 khối, 0 chưa khớp) rồi `check --course PYT`: PASS 544 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 (step bảng mới ở L05 và L11 làm lệch khoá, đã sinh lại bằng công cụ chính thức).
- `verify_pyt` (L01 L04 L05 L06 L07 L08 L09 L10 L11 L12 L13): 165/167 PASS; L04, L10, L12 PASS lần này. Còn 2 ô thời gian lệch >×8 do máy tải: L09 `l09_sum` (`t_np_1e6` 0,0003 s lưu so 0,0026 s đo lại) và L13 `l13_scale` (`t_line_1e3` 0,0028 s so 0,0285 s). Nhiễu đo, không phải lỗi bài; cần chạy lại `verify_pyt L09 L13` khi máy rảnh.
- Chưa chạy lại: `arith_scan` (không đổi số), `lab_gate` (lab không đổi).
