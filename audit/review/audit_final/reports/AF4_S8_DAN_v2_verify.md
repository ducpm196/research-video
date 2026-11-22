# Báo cáo kiểm định độc lập WP-AF4-5 Stage 8 — Khóa DAN v2 (`L00–L12`, 13 bài)

**Phán quyết tổng thể:** **`NO-GO`**

## 1. Tóm tắt kiểm tra tự động
- `tools/lv.py lint` (`L00–L12`): **13/13 PASS** (`0 FAIL, 0 WARN`)
- `tools/lv.py curriculum curriculum/dan.yaml`: **PASS** (`13 bài, 0 lỗi`)
- `audit/dan/verify_dan.py`: **13/13 PASS**
- `audit/review/arith_scan.py DAN`: **PASS** (`40 phép tính, 0 FAIL`)
- `audit/review/screen_code.py check --course DAN`: **29/29 PASS**
- `audit/review/check_xref.py --course DAN`: **PASS** (`0 lượt`)
- `loi_giai.py` vs `mong_doi.txt`: **13/13 PASS**
- `audit/layout_DAN.tsv`: `0` dòng lỗi (`preview.html` hiện tại sạch; `build_report.json` STALE `13/13`)

## 2. Danh sách MUST fix

### M1. MP4/ASR STALE `13/13` và thời lượng thực tế `< 9.0` phút (`L08` 8.33p @140wpm; `11/13` < 9.0p theo `timeline_seconds` cũ `L00–L09, L11`)
- Bổ sung lời giảng/phân tích các bài ngắn đạt `>= 9.0p` thực tế, rồi rebuild `L00–L12`.

### M2. `[P8]` 12/13 lab (`L00–L05, L07–L12`) lặp bộ số bài giảng & lộ công thức/đáp số
- Lộ công thức/đáp số: `L01` (`(mA+mB)/2`), `L03` (công thức SQL), `L05` (`30%`), `L09` (`(1.4826×MAD)`).
- Trùng số bài giảng: `L00–L05, L07–L12`; `L06` cần ghi rõ quy ước `d = 0..13`.

### M3. `L07` sai số liệu & thuật ngữ chưa dạy (`recap#1`)
- `lessons/dan/L07_du_bao_co_so.yaml:262`: viết sai `MAE = 1,5` (bộ số thực cho `1,25`) và dùng `WMAPE` chưa từng giảng ở toàn khoá DAN.

### M4. `[P1]` Bảng đọc mã `practice` & thuật ngữ chưa giảng
- `L02`, `L03`: thiếu bảng đọc mã SQLite/Python trong `practice`.
- Thiếu token thực tế: `L00` (`_`, `for l, _`), `L05` (`s[-1]`, `[... for i in range(3)]`), `L06` (`ds[a:b]`, `range(6, 14)`), `L07` (`int(dieu_kien)`), `L10` (`z=1.96`, `;`, `return ..., ...`).
- Thừa boilerplate: `{k: v} / dict(...)` trên 9 bài (`L01, L04..L09, L11, L12`), `%` giả trên 4 bài (`L04, L05, L11, L12`), `set/all` (`L00, L06`).
- Thuật ngữ chưa giảng: `O(1), vs` (`L01`), `:memory:, RAM, 1–N` (`L02`), `cohort retention, T1/T2` (`L04`), `quy luật Pareto` (`L08`), `vs` (`L09`), `O(N)` (`L10`), `10k/11k` (`L11`), `sai số loại 1, alpha` (`L12`).

### M5. `covers:` sai cảnh dạy thật (`5/13` bài + chỉnh `L08, L12`)
- `L00` obj2 → `sym`/`quiz`; `L02` obj3 → `example`/`pitfalls`; `L03` obj3 → `pitfalls`; `L06` obj2 → `example`; `L07` obj2 → `pitfalls`/`quiz`; `L11` obj2 → `pitfalls`, obj3 → `pitfalls`/`quiz`; `L08` obj3 → `sym`; `L12` obj3 → `quiz`.

## 3. SHOULD fix
- `P9` thân bài bổ sung cho 9 bài (`L00, L02, L03, L05..L08, L10, L12`); `L05 recap#1` `"lượt xem"` vs `"người"`.
- Chuẩn hoá `"mili giây"` theo `tools/lv.py:75` (`L01, L03, L05, L06, L09`); bỏ/giản lược ngoặc lồng; đồng bộ `63,6` → `63,64` và `show`/`say` ở `L01, L03, L06, L07, L10`.
