# Báo cáo kiểm định độc lập WP-AF4-5 Stage 9 — Khóa DAN (`L00–L12`, 13 bài)

**Kết luận tổng thể:** **`NO-GO`** (read-only audit 13/13 bài).

---

## 1. Tóm tắt chỉ số & cổng kỹ thuật
- `lv.lint`, `lv.py curriculum curriculum/dan.yaml`, `audit/dan/verify_dan.py`, `arith_scan.py DAN`, `screen_code.py check --course DAN`: **13/13 PASS** (`0` lỗi).
- `build_report.json` (`spec_sha256` & `tts_sha256`), `L*.srt == say`, `asr_report.md` (`0` thiếu audio / `0` chưa xem xét), `check_xref` (`0` lượt): **13/13 sạch**.
- `loi_giai.py == mong_doi.txt`: **13/13 khớp stdout** (nhưng `L05`, `L09` sai với đề/bài).
- Kiểm trực quan **32 PNG**: **32/32 sạch** (`audit/layout_DAN.tsv` đang STALE, cần chạy lại `layout_scan.py DAN`).
- **`P1` (chuẩn chặt gồm `practice`/`de.md`):** **0/13** (thân bài sạch, gãy ở `practice#0/#1/#3` & `de.md`).
- **`P8`:** **10/13** (`3` `MUST`: `L05`, `L09`, `L12`).
- **`P9` (`Hai mức quy mô`):** **2/13** (`L10`, `L12`; thiếu khối chuẩn ở `recap` 13/13).
- **`covers:` khớp cảnh dạy thật:** **0/13** (gán cứng `example/check/practice`).

---

## 2. 3 lỗi `MUST` & việc cần sửa để đạt `GO`
1. **`L05` (`MUST`):** `de.md` hỏi *"ước lượng kết quả nếu bước 2 tăng lên 35%"* nhưng `loi_giai.py`, `mong_doi.txt`, `practice` không tính — bổ sung phép tính/in dòng này vào lời giải hoặc sửa đề đồng bộ. (Khuyến nghị bổ sung tính đúng tỷ lệ mới `40% → 35% → 25% = 3.5%` / `overall_35=3.5%` vào `loi_giai.py` + `mong_doi.txt` + `upgrade_dan.py`).
2. **`L09` (`MUST`):** Thân bài & `curriculum/dan.yaml` dạy độ lệch chuẩn tổng thể (`n=8`, **`z=2.65`**) và chuẩn hoá **`1.4826 * MAD`**, còn `loi_giai.py` & `practice#1/#2/#4` dùng `n-1` (`z_classical=2.47`) và hằng số `0.6745` — sửa `loi_giai.py` + `practice` dùng đúng `n` (`pstdev`, `2.65`) và `1.4826 * MAD`.
3. **`L12` (`MUST`):** `de.md` và `practice#3` gọi nhầm `1 - 0.975^5` / `1 - 0.975^30` là *"5 và 30 lần nhìn trộm"* — sửa thành *"5 phiên bản đồng thời và 6 vòng × 5 phiên bản"* (`[KO13] §5.1`), thay `"A/B"` bằng *"thử nghiệm có đối chứng"* đúng quy ước `curriculum/dan.yaml`.
4. **Đồng bộ `P1`, `P9`, `covers:` trên `L00–L12`:**
   - Bổ sung `<p class="note"><b>Hai mức quy mô:</b> ...` ở `recap` (13/13) + so sánh 2 quy mô ở thân bài (`L00, L02, L03, L05, L06, L07, L08` và `L01, L04, L09, L11`).
   - Sửa `covers:` khớp cảnh dạy thật ở 13/13 bài.
   - Đồng bộ `practice#0/#1/#3` & `de.md` (chú thích tại chỗ `active user`, `vs`, `TB`, `1-N`, `:memory:`, `cohort retention`, `10k`, `Pareto`, `z-score`, `alpha`, bỏ bảng thừa `:.3f`/`math.log` không dùng, sửa `L04 de.md` bổ sung `18/100` tuổi tháng 2).
   - Chạy `layout_scan.py DAN` làm tươi `audit/layout_DAN.tsv`.

*(32 PNG đã xem trực tiếp: `L00/{00020,00064,00067}`, `L01/{00015,00065}`, `L02/{00012,00025,00068}`, `L03/{00010,00016,00072}`, `L04/{00016,00060}`, `L05/{00015,00062}`, `L06/{00016,00067}`, `L07/{00017,00067}`, `L08/{00015,00016,00060}`, `L09/{00019,00065,00066,00068}`, `L10/{00022,00072,00073}`, `L11/{00019,00065,00066}`, `L12/{00020,00023,00032,00124,00127}`.)*
