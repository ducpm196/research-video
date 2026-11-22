# Báo cáo Kiểm định Độc lập WP-AF4-5 Stage 8 — Khoá `DSC` (`L00–L15`, v2)

**Phán quyết tổng thể: `NO-GO`**

## 1. Tóm tắt kiểm tra tự động
- `audit/dsc/verify_dsc.py`: **30/30 PASS**
- `tools/lv.py curriculum curriculum/dsc.yaml`: **16 bài, 0 lỗi**
- `tools/lv.py lint lessons/dsc/L*.yaml`: **16/16 PASS** (`0 FAIL, 0 WARN`)
- `loi_giai.py` vs `mong_doi.txt`: **16/16 khớp stdout** (nhưng `L04` sai toán học)
- `audit/review/screen_code.py check --course DSC`: **32/32 PASS**
- `audit/layout_DSC.tsv` & `19 <svg>`: **0 lỗi bố cục**; `"càng "` & lặp ngoặc đơn: **0 lỗi**
- Thời lượng `< 9.0p`: **3 bài < 9.0p nói (`L05` 8.42m, `L07` 8.98m, `L13` 8.65m)**; 8 bài `< 9.0m` theo `build_report` cũ (`L01, L02, L04, L05, L07, L09, L10, L13`)
- MP4/SRT/ASR: **16/16 STALE**

## 2. Danh sách MUST fix

### M1. `[P8 / Toán học]` Lỗi tính tứ phân vị & ngoại lai ở `L04` lab (`outlier=0` mâu thuẫn với thân bài)
- `labs/dsc/L04/loi_giai.py:5-7` dùng nửa tách bỏ trung vị làm `fence = 127.8` → `outlier=0`, trái ngược hoàn toàn với bài giảng (`Q1=2, Q3=4, fence=7.0 -> 100 là ngoại lai`). Đổi bộ số mới (ví dụ 6–8 số) hoặc quy ước khớp thân bài, cập nhật đồng bộ.

### M2. `[P8]` `de.md` lặp nguyên bộ số bài giảng (13/16 bài) & lộ đáp số/công thức
- Lặp số bài giảng: `L01, L03..L12, L14, L15` (cùng `L00` nêu cứng `needs_randomization=1`, `L05` tiêu đề `2%`, `L08/L09/L11/L12/L15` lộ công thức). Đổi sang bộ số mới độc lập cho `L01, L03..L12, L14`, tinh gọn `L15` và tính điều kiện thật ở `L00`.

### M3. `[P1]` Bảng đọc mã `practice` lệch 16/16 bài & sót thuật ngữ chưa giảng
- Tái sinh `practice` qua `ast_p1.py` (bỏ `dict`/`set`/`%` thừa trên 14+2+2 bài; bổ sung `a, b = ...`, `< / ==`, `and`, `(a, b)`, `;`, `_`, `2_817_131`, `.values()`, `int(x)`, slicing `[a:b]`, `:.2f`).
- Thuật ngữ chưa giảng: `vs` (`L00, L01, L04, L10`), `nhiều–nhiều N–M` & `tích Đề-các` (`L02`), `O(N log N)/O(N)` (`L04, L13`), `Pearson` (`L06`), `FWER` (`L09`), `Train/Test` (`L10`), `PPV` & `quy tắc Bayes` (`L11`), `r^2` (`L12`).

### M4. `[E51]` `covers:` trỏ sai cảnh thực tế (`10/16` bài)
- `L01` obj2→`sym`; `L02` obj3→`example/pitfalls`; `L03` obj3→`pitfalls/example`; `L04` obj1→`hook/sym/intuition`; `L06` obj1→`sym`, obj2→`hook/intuition`; `L09` obj2→`example`, obj3→`sym`; `L11` obj3→`cost`; `L12` obj1→`sym/prereq`; `L13` obj3→`pitfalls` (+ chỉnh `L00, L11, L14, L15`).

### M5. Thời lượng `>= 9.0p` (`L05, L07, L13` và kiểm `timeline_seconds >= 540s` cho 16/16)

### M6. `[P9 / Toán học]` Lỗi số liệu chưa kiểm chứng trong `recap` (`L08`, `L15`)
- `L15 recap#1`: trộn `0,9525` (tập kín) vs `0,8554` (công khai `0,9514`), và `0,06%` không có trong bài/nguồn (thực tế `~2,6%` so với `0,88`).
- `L08 recap#1`: `~370 000` (tính đúng `356 335`), `"ở 500 khách"` (thân bài dùng `1000` khách cho `18,9%`).

### M7. Rebuild MP4 + `layout_scan` + SRT + ASR cho 16/16 bài

## 3. SHOULD fix
- `L03, L13`: bỏ `Hai mức quy mô` lặp ở `check` (đã có ở `recap#1`); `L03` đổi `(< 1 giây)` → `(&lt; 1 giây)`.
- `L10 recap#1`: `"~80%+"` → `88,9%`; `L11 recap#1`: `68,75%` & bỏ `PPV`.
- `L15/de.md`: tách tham số khỏi biểu thức Python; `L00/loi_giai.py`: tính thật thay hardcode; `audit/legal/registry.yaml`: bổ sung bản gốc `356/2025/NĐ-CP`.
