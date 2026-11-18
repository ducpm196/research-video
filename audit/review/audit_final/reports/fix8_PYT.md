# fix8_PYT: sửa nhỏ vòng 8 theo `R5_PYT.md` (PYT, một tác tử)

Nguồn sửa: `audit/pyt/src/lNN.py` -> `gen.py` (không sửa YAML sinh ra). Nền R5: MUST 0; P1 = 2 chắc+vừa 13/14, cả yếu 6/14; mục vừa L09; SHOULD 6.

## 1. Bài đổi, CẦN DỰNG LẠI
L00, L01, L02, L03, L04, L06, L09, L10, L11, L12, L13 (11 bài). Không đổi: L05, L07, L08. Lab không đổi. Thêm `audit/pyt/src/pyt_b.py` (hàm dùng chung L12/L13: khoảng trắng không ngắt); `audit/pyt/make_fig_l11.py` + `fig_l11.json` thêm khoá `pts1k` (1 000 điểm thật đầu mẫu hexbin).

## 2. Mục chưa giảng
| Bài | Mục | Cách giảng |
|---|---|---|
| L09 (vừa) | `print((so_tien > 1000).sum())` | bảng sym hàng mặt nạ: `(a > 1000).sum()`, `True` = 1, `False` = 0, nên tổng là số phần tử đúng (chữ + câu lời); ví dụ 2: ghi chú ngay dưới phiên + câu lời |
| L10 | `isna().sum()` | bước 4: ghi chú "isna() cho cột đúng/sai, True = 1 nên .sum() đếm số ô thiếu" + câu lời |
| L00 | `print` ở prereq; `float(2 ** 53)` | một vế câu cho `print(…)` (chữ + lời); `float(x)` đổi số nguyên thành số thực (chữ + lời) |
| L01 | `list(range(3))`; `µs` | tiêu đề khung phiên nói `list(...)` xếp dãy thành danh sách (đứng trước/cùng khung), lời đọc đổi thứ tự; tiêu đề cột bảng ghi `µs = phần triệu giây, ms = phần nghìn giây` |
| L02 | `ms`, `s` | tiêu đề cột bảng scale: `ms = phần nghìn giây, s = giây` |
| L03 | `gd.remove(x)` | hộp cảnh báo lỗi 2: `gd.remove(x)` xoá phần tử đầu tiên bằng `x` khỏi danh sách (chữ + lời) |
| L06 | `dang_dung, dinh = tracemalloc.get_traced_memory()` | thêm hàng vào bảng step đứng trước khung mã: hàm trả hai số (đang dùng, đỉnh), gán cho hai tên, chỉ dùng `dang_dung` (chữ + lời); `introduces: pyt_tracemalloc` chuyển lên step bảng |
| L11 | `ax.collections[0].get_offsets()`, `.get_array()` | hàng thứ tư của bảng sym (đọc lại điểm, ô gộp) + lời; `introduces: pyt_get_offsets` chuyển lên step bảng |
| L13 | "mã đã biên dịch" | prereq: ghi chú và lời "thư viện viết sẵn, chạy nhanh hơn vòng lặp Python" |

## 3. SHOULD
| Bài | Việc |
|---|---|
| L04 | "41 ký tự (ngoại suy)": `s30`, `s40` đổi sang `t2` (hai chữ số có nghĩa): 0,82 s × 2^16 ≈ 53 700 s -> "≈ 15 giờ" (lời "khoảng mười lăm giờ"), 31 ký tự "≈ 52 s". Sinh từ `measured.json`, không còn số "10 giờ" ở chỗ nào khác (đã grep) |
| L11 | hình đường + phân tán (ví dụ) có vạch và nhãn trục (số giao dịch 120/140/160, doanh thu 60–90, tiêu đề nêu trục đứng/ngang); hình scale: thay hình giả bằng 1 000 điểm THẬT (đầu mẫu của `hexbin`, từ `fig_l11.json`) trên hệ trục −4..4 có vạch và nhãn; hình bên phải ghi rõ "bầu dục minh hoạ −3..3" |
| L12 | "ngay sau" ngưỡng 11 000 000 thống nhất `11 001 000`: bảng ngưỡng ví dụ, quiz (đáp án + lời + `checks`), SVG đã có; ghi rõ vì sao cách 1 000 (phí = tien // 1000); bộ bảy ca của bài giữ `12 000 000` nên số 18/4/14/12/14 giữ nguyên; step đột biến nêu đúng tập: mỗi `<`/`>` đổi hai cách, dịch bốn hằng 50000, 1100, 11000, 1000 lên/xuống 1 (chữ + lời); hook rút ngắn tiêu đề và ghi chú diff |
| L12, L13 | khoảng trắng không ngắt cho số nhóm ba chữ số và đơn vị (`1 099 999`, `≈ 10 ms`, `≈ 98 KB`), `--tb=short` bọc `nowrap`: hàm `nbsp_spec` (chỉ đổi chữ NGOÀI khối mã nên sổ screen_code không đổi) |

## 4. Độ dài lời đọc
L00 2295, L01 2178, L02 2297, L03 2292, L04 2285, L05 2228, L06 2293, L07 2169, L08 2290, L09 2143, L10 2193, L11 2290, L12 2278, L13 2277 (≤ 2300).

## 5. Cổng thật
- `lv.py lint`: 0 FAIL, 0 WARN ở cả 14 bài. `curriculum curriculum/pyt.yaml`: 14 bài, 0 lỗi. `tests/test_e52.py`: 0 FAIL. `arith_scan`: 259 phép, 0 FAIL.
- `lv.py render` (chạy được): L00 L01 L02 L03 L04 L06 L09 L10 L11 L12 L13: lần đầu 3 bài lỗi do chính các sửa mới: L01 scale (tiêu đề cột dài), L03 pitfalls (hộp cảnh báo 2 dòng), L11 scale (chữ tiêu đề hình vượt mép 52 px). Đã sửa: L01 chú đơn vị đưa vào chính ô (`≈ 93 µs (phần triệu giây)`), L03 rút hộp còn một dòng, L11 rút tiêu đề hình. Chạy lại: **cả 11 bài 0 vấn đề**. Đã xem khung PNG: L12 `00000` (chữ cuối cách thanh phụ đề ~25 px), L11 `00060` (hình có vạch và nhãn trục), `00062`.
- `verify_pyt`: toàn bộ ô tất định PASS (L00 L01 L02 L03 L06 L11 L13 PASS hẳn). Còn đúng 4 ô THỜI GIAN lệch >×8 ở lần chạy lại cuối: L04 `l04_redos`, L09 `l09_sum`, L10 `l10_mem2`, L12 `l12_scale`. Máy đang tải nặng (cùng phép đo chậm ~8 lần so với lúc lưu; lần chạy khác lệch ô khác nhau: nhiễu đo, không phải lỗi bài). CẦN chạy lại `verify_pyt L04 L09 L10 L12` khi máy rảnh. Không đổi `measured.json` ở vòng này.
- `screen_code check --course PYT`: PASS 544 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 (không đổi khoá; không cần `gen-pyt`).
- `lab_gate`: lab không đổi nên không chạy lại (vòng trước 14 PASS).
