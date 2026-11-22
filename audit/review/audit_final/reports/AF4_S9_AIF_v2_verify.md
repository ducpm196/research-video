# Báo cáo kiểm định độc lập WP-AF4-5 Stage 9 — Khóa AIF (L00–L14, v2)

**Phán quyết tổng thể: `NO-GO`**

## 1. Tóm tắt kiểm tra tự động
- `audit/aif/verify_aif.py`: `26/26 PASS`
- `tools/lv.py curriculum curriculum/aif.yaml`: `15 bài, 0 lỗi`
- `tools/lv.py lint lessons/aif/L*.yaml`: `15/15 PASS` (`0 FAIL, 0 WARN`)
- `audit/review/screen_code.py check --course AIF`: `30/30 PASS`
- `loi_giai.py` vs `mong_doi.txt`: `15/15 khớp stdout`
- `L14` vs `audit/aif/sources_L14.md`: `100% khớp`
- Thời lượng `< 9,0p`: **8/15 bài < 9,0p** (`L01, L03, L05, L06, L08, L09, L10, L13` ở 150 từ/phút; cần bổ sung nội dung giảng giải)
- `audit/layout_AIF.tsv`: trống (chờ chạy `layout_scan`) & `15/15` MP4 STALE

## 2. Danh sách MUST fix

### M1. `[P8]` Sai lệch / thiếu dữ liệu `de.md` & mâu thuẫn đề ↔ lời giải
- `labs/aif/L01/de.md:4` vs `loi_giai.py`: `de.md` gợi ý `S, A, B` (3 nút) nhưng `loi_giai.py` kiểm đích khi pop nên ra `expanded=4`. Cần thống nhất rõ (sửa `loi_giai.py` kiểm khi sinh = 3, hoặc sửa `de.md` nêu kiểm khi lấy ra).
- `labs/aif/L05/de.md:3`: thiếu 9 cạnh kề của 7 vùng nước Úc & lộ `3^7 = 2187`.
- `labs/aif/L00/de.md:1,3`, `L03/de.md:1,3`, `L13/de.md:1,3`: lộ đáp số/công thức ở tiêu đề và nội dung (`8 trạng thái`, `N=52, d=5`, `log10(35^80 / 35^4)`).
- `lessons/aif/L14`: `practice#0` in `sim_rate=...s` mất `/` (cần thêm `"/s"` vào `units` trong `common.py` để giữ `sim_rate=.../s`).
- `labs/aif/L04/loi_giai.py:5-8` vs `de.md` & `L04_tim_kiem_cuc_bo.yaml:314`: code dùng `for _ in range(10)` không dừng sớm khi kẹt cực tiểu như đề bài nêu.

### M2. `[P8]` Lặp nguyên bộ số bài giảng ở 11/14 bài thường (`L00, L02, L03, L05, L06, L07, L08, L09, L10, L11, L13`)
- Đổi sang bộ dữ liệu đầu vào độc lập trong `de.md` + `loi_giai.py` + `mong_doi.txt`.

### M3. `[P1]` Bảng đọc mã `practice` lỗi 15/15 bài & mở rộng `ast_p1.py`
- Sửa 15/15 qua `ast_p1.py` (loại bỏ `{...}` dict/set/`%` giả), đồng thời trong `ast_p1.py` xử lý chuẩn `**{...}` dict unpacking (`L10`) vs `**` lũy thừa, `|` hợp tập hợp vs bitwise OR (`L10`), bổ sung token thực tế thiếu (`L00..L12, L14`), đồng bộ `L04`.

### M4. `covers:` trỏ sai cảnh dạy thật (`7/15` bài)
- `L02` obj 1 → `sym`
- `L03` obj 1 → `sym` / `intuition`
- `L04` obj 1 → `sym` / `intuition`
- `L09` obj 2 → `example`/`quiz`, obj 3 → `pitfalls`
- `L12` obj 1 → `sym`
- `L13` obj 1 → `sym`/`intuition`/`quiz`
- `L14` obj 3 → `quiz`, obj 1 → `stage1..stage5`

### M5. 3 lỗi SVG chưa sửa
- `L04`: `<text x="330" y="205">cực tiểu địa phương: h = 1</text>` cắt ngang đường cong.
- `L08`: `<text y="336">` trong `height="340"` chạm viền dưới.
- `L13`: `<text x="1230" y="270">` dài 28 ký tự chạm mép hộp `width="320"`.

### M6. `layout_scan` + Rebuild 15/15 MP4 + ASR

## 3. Danh sách SHOULD fix
- Bổ sung lời giảng để `L01, L03, L05, L06, L08, L09, L10, L13` đều đạt `>= 9,2p` ở 150 từ/phút.
- Bọc KaTeX `$...$` các số mũ `^` trong `Hai mức quy mô` (`L02, L04, L05, L08, L09, L10, L11, L12, L13`); tránh viết tắt/tên chưa giảng (`8/15-puzzle`, `O(N)`, `O(|S|^2|A|)`, `BFS`, `TPU`).
- Sửa lệch nhỏ: `L02` (`1 481 nút` thay vì `vài trăm nút`, `"ít hơn trên 100 lần"`), `L04` (bỏ *"4 hậu (8 bước)"*), `L12` (*"12 ô"* thay *"12 trạng thái"*), `L13` (*"2 449 lá"* thay *"2 449 nút"*).
- Làm rõ `L11/de.md`, `L12/de.md`, `L07/de.md`, và `L11` obj 1 → `sym`, `L14` obj 1..2 → `stage*`.
