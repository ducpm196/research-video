# Báo cáo Kiểm định Độc lập Stage 11 — Khoá ESY (L00–L07) [AF4 v2]

**Verdict: `NO-GO`**

## 1. Kết quả kiểm tra tự động & Tình trạng bản dựng
- `tools/lv.py lint` (`L00..L07`): **8 / 8 PASS** (0 FAIL, 0 WARN; thời lượng 9,9–13,5 phút).
- `audit/esy/verify_esy.py`: **72 / 72 PASS**.
- `audit/review/screen_code.py check --course ESY`: **35 / 35 PASS**.
- Chạy `loi_giai.py` vs `mong_doi.txt`: **8 / 8 PASS**.
- `audit/layout_ESY.tsv`: **0 dòng lỗi**.
- Bản dựng MP4 (`out/esy/L00..L07`): **PENDING REBUILD** (SVG `L02 example#1` đã gỡ viền trắng trên số `4`).

## 2. Bảng tổng hợp & lỗi cần sửa (L00–L07)
| Bài | Phút | P1 | P8 | P9 | `covers:` | Lỗi chính |
|---|---:|---:|---:|---:|---|---|
| **L00** | 10,7 | 1 | 1 | 2* | Đúng | `assumes:` 7 ký hiệu dù `requires: []`; `practice#2` nhầm `set()`; `sym#0` thiếu chú thích `ADC` trên chữ |
| **L01** | 11,0 | 1 | 1 | 1 | Sai mục 2 (`ops`) | `ops#0 say` lặp 2 lần câu giải thích `;` và `//`; `0x12` chưa giảng ở L00–L01; `practice#2` nhầm `set()`, thiếu `|=,&=,^=,~`; thiếu P9 thân bài |
| **L02** | 11,2 | 0 | 1 | 1 | Sai cả 3 (`sym, isr, example`) | `isr#0`: `sei()` chú thích sai AVR & `say` đảo ngược `volatile` vs `uint16_t` + chưa giải `cli/sei/;/()//`; `practice#2` nhầm `set()`, thiếu `None`/`and`; thiếu P9 thân bài |
| **L03** | 10,0 | 0 | 1 | 2 | Sai mục 1 (`sym`) | `PWM` & `clk` chưa giải thích; `practice#2` nhầm `dict(...)`, thiếu `16_000_000`, `a,b,c,d=...`, `:` |
| **L04** | 10,1 | 1 | 0 | 2 | Sai cả 3 (`sym, sym/snr, example`) | `de.md` trùng y hệt `quiz` (`12-bit, 3.3V, 2048`); `practice#0` ghi thiếu `V` (`V2048=...`); `practice#2` nhầm `dict(...)`, thiếu `:` |
| **L05** | 13,5 | 1 | 1 | 1 | Sai cả 3 (`sampling, filters, example/pitfalls`) | `assumes: [assign, dots]` chưa giảng ở L00–L04; `practice#2` nhầm `dict(...)`, ghi `i` thay `_`; `recap` nêu `N=64` thiếu ở thân bài |
| **L06** | 9,9 | 1 | 1 | 1 | Đúng | `practice#2` nhầm `dict(...)`, thiếu `a, b = ...`, `:`; `sym#0` `show` chưa nêu 1 bit dấu trong 8 bit nguyên; thiếu P9 thân bài |
| **L07** | 10,9 | 2 | 1 | 2* | Sai cả 3 (`sym, speed, example/check`) | `covers:` sai (mục 3 → `practice`); `practice#2` nhầm `dict(...)`, thiếu `baud, bits_per_byte = ...`, `:` |
