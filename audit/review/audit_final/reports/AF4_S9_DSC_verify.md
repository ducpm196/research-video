# Báo cáo Kiểm định Độc lập Stage 9 — Khóa `DSC` (`L00–L15`)

**Vai trò:** WP-AF4-5 Stage 9 DSC Verifier (read-only)  
**Kết luận tổng thể:** **`NO-GO`**

---

## 1. Tóm tắt cổng kỹ thuật & chỉ số
- `audit/dsc/verify_dsc.py` (`30/30 PASS`), `lv.py curriculum`, `lv.py lint` (`16/16`), `lv.py verify` (`16/16`), `build_report.json` (`16/16`), `L*.srt == say` (`16/16`), `asr_report.md` (`16/16 chưa xem xét=0`), `audit/layout_DSC.tsv` (`0`), `screen_code` (`48/48`, lưu ý toàn bộ ghi `kind: other`): ĐẠT.
- **Thân bài `say` (`càng ...` 5 câu):** Sạch, đúng toán học `16/16`.
- **`P1` (bao gồm `practice#0/#3` & `de.md`):** Strict FAIL (`<= 18.75%`), phần lớn do `practice#0` sinh khuôn mẫu (`:.3f`, `math.log/exp`) lệch mã thật + `de.md`/`p3` lọt `vs`, `N-M`, `Cartesian`, `Pearson`, `FWER`, `Bonferroni`, `Train/Test`, `PPV/Bayes`, `zip_3/age_band`, `Netflix Prize`.
- **`P8` & `P9`:** `L00`, `L08`, `L15` có lỗi `MUST`; `0/16` có `recap Hai mức quy mô` & `covers:` khớp cảnh dạy thật; `47/47 PNG` sạch đẹp.

---

## 2. Lỗi `MUST` & việc cần sửa để đạt `GO`
1. **`L00` (`MUST`):** `labs/DSC/L00/de.md` thiếu dữ liệu đầu vào (trong khi `loi_giai.py` có `import random`/`random.seed(42)` thừa và gán cứng `seen_buy = 60/100; unseen_buy = 20/100`) — viết lại đề/lab gắn với bảng 4 cửa hàng trong bài hoặc cung cấp đầy đủ dữ liệu đầu vào & tính từ dữ liệu thật.
2. **`L08` (`MUST`):** Đồng bộ 1 giá trị duy nhất (`14751` theo `alg.ab_sample_size` trong `curriculum/dsc.yaml` + thân bài + `verify_dsc.py`, hoặc giải thích công thức xấp xỉ + đồng bộ tham số `1.96, 0.84` vs `1.959964, 0.841621` khớp `de.md ↔ loi_giai.py ↔ mong_doi.txt ↔ practice`). Khuyến nghị dùng công thức chính xác cho `n_per_group=14751` khớp 100% bài giảng!
3. **`L15` (`MUST`):** Sửa `loi_giai.py`, `mong_doi.txt`, `practice` từ `goal=0.8573` → **`goal=0.8572`** (cắt 4 chữ số thập phân theo luật cuộc thi vừa dạy trong bài) và `blend_opt=0.00066` → **`0.00067`** khớp `stage4`/`sources_L15.md`/`verify_dsc.py`.
4. **Sửa `L04 loi_giai.py`** không hardcode `med_x = xs[2]`, `q1, q3 = 2.0, 4.0` (tính từ danh sách).
5. **Toàn khóa `L00–L15`:** Bổ sung `Hai mức quy mô` trong `recap` (16/16) và thân bài `L13` (cùng `L03`); sửa `covers:` khớp cảnh dạy thật; sửa bảng `practice#0` khớp đúng cú pháp code thật + chú thích tiếng Việt tại `practice#3`/`de.md`.

*(47 PNG đã xem trực tiếp: `L00..L15`, mỗi bài 2–5 khung SVG + `practice`.)*
