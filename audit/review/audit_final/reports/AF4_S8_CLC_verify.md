# Báo cáo kiểm định độc lập WP-AF4-3 Stage 8 — Khóa CLC (`L00–L12`, 13/13 bài)

**Verifier:** `5a907c15` (`WP-AF4-3 Stage 8 CLC Verifier`, read-only)  
**Kết luận:** **`NO-GO`**

---

## 1. Tổng hợp cổng tự động & nhất quán dữ liệu (`L00–L12`)
- `lv.py curriculum curriculum/clc.yaml`: `13 bài, 13 đã có đặc tả, 0 lỗi`; `title` & `objectives` khớp **13/13**.
- `audit/clc/verify_clc.py`: **13/13 PASS**.
- `audit/clc/sources_L12.md`: Khớp nguồn S3 **100%**.
- `lv.lint`: **13/13** `0 errors, 0 warnings`; `checks`: **96/96 PASS**.
- `spec_sha256`: **13/13 khớp**; `L*.srt == say`: **13/13**; `asr_report.md`: **13/13 `chưa xem xét: 0`**.
- `screen_code.py check --course CLC`: `15 khối — PASS 16 · FAIL 0 · STALE 0`.
- `loi_giai.py == mong_doi.txt`: **13/13 khớp stdout** (nhưng `L00, L03, L11` đi đường tắt/mâu thuẫn).

---

## 2. Lý do `NO-GO` (`6` nhóm `MUST`)
1. **`L12` (`MUST` — sai toán học trong `practice#0` / `00124.png`):** Ghi `"gấp ~6 lần ngân sách cả năm 99.99%"` thay vì `4,9 lần` (`257 / 52.56 ≈ 4.9x`).
2. **`L11` (`MUST` — mâu thuẫn kiến thức):** `curriculum` & `L11.yaml` dạy **6 trụ cột**, còn `labs/CLC/L11/de.md` ghi `"5 trụ cột"` và `loi_giai.py` không tính điểm trụ cột.
3. **`L00` & `L03` (`MUST` — `loi_giai.py` đi đường tắt):** `L00` gán cứng `{'IaaS': 3, 'PaaS': 2, 'SaaS': 1}` thay vì mô hình 4 lớp; `L03` viết `def eval_iam(effs):` sai chữ ký `eval_iam(policies, action)`.
4. **`L10` (`MUST` — SVG đè chữ):** `out/CLC/L10/frames/00018.png`, nhãn `"sức chứa 1/2"` (`x=720, y=212`) chạm đè viền trái hộp `"vùng 1"` (`x=830`).
5. **`P9` (`MUST`):** **13/13** thiếu `<p class="note"><b>Hai mức quy mô:</b> ...` trong `recap` (`L00, L03, L07, L11` thiếu cả so sánh 2 quy mô trong thân bài).
6. **`covers:` (`MUST`):** **13/13** gán cứng `[(1, example/stage1), (2, check), (3, practice)]`; `P1` chặt chỉ đạt `1/13` (`12/13` bài còn thuật ngữ tiếng Anh chưa chú thích tại `practice#0`/`de.md`).

*(42 PNG đã xem trực tiếp: `L00–L12` mỗi bài 3–6 khung tiêu biểu.)*
