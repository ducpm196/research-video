# Báo cáo Kiểm định Độc lập WP-AF4-3 Stage 8 — Khóa `SAR` (`L00–L13`, 14 bài)

**Vai trò:** WP-AF4-3 Stage 8 SAR Verifier (read-only)  
**Kết luận tổng thể:** **`NO-GO`**

---

## 1. Tóm tắt chỉ số & cổng tự động (`OBSERVED`)
- `lv.py curriculum curriculum/sar.yaml`: **14/14 PASS** (`0 lỗi`).
- `audit/sar/verify_sar.py`: **15/15 PASS** (`0 FAIL`).
- `lv.py lint`: **14/14 PASS** (`0 errors, 0 warnings`); `lv.py verify`: **14/14 PASS**; `checks`: **208/208 PASS**.
- `build_report.json`: **14/14 khớp**; `L*.srt == say`: **14/14 khớp 100%**; `asr_report.md`: **14/14 `chưa xem xét: 0`**.
- `screen_code.py check --course SAR`: `15 khối — PASS 16 · FAIL 0 · STALE 0`.
- `audit/layout_SAR.tsv`: **0 lỗi**; **31/31 PNG** xem trực tiếp sạch đẹp.
- `loi_giai.py == mong_doi.txt`: **14/14 PASS**.
- **`P1` chặt (gồm `practice#0` & `de.md`):** **4/14 (28,6%)** (thân bài `14/14 = 100%`, `10/14` lọt thuật ngữ tiếng Anh ở `practice#0`/`de.md`).
- **`P8`:** Lab chạy đúng **14/14 (100%)**, nhưng `covers:` gán cứng **0/14**, thiếu `recap Hai mức quy mô` **0/14**.
- **`P9`:** SVG sạch **14/14 (100%)**; thân bài `L03, L09` thiếu đối chiếu 2 quy mô; `14/14` thiếu khối `Hai mức quy mô` ở `recap`.

---

## 2. Việc cần làm để đạt `GO`
1. Bổ sung `<p class="note"><b>Hai mức quy mô:</b> ...` ở `recap` cho `14/14` bài (và bổ sung đối chiếu 2 quy mô định lượng trong thân bài `L03`, `L09`).
2. Sửa `covers:` trong `audit/sar/af2/upgrade_sar.py` khớp cảnh dạy thật (theo quy chuẩn `E51`).
3. Việt hóa / chú thích tại chỗ các thuật ngữ tiếng Anh trong `practice#0` (`de_hint`) và `labs/SAR/L*/de.md` (`P95`, `SLO`, `ADR`, `RDBMS/NoSQL`, `ACID`, `Sharding`, `QPS/DAU`, `UI->App->Data`, `Cache/DB/hit`, `RF/shard`, `Token bucket/burst/cap`, `SQL`, `URL/W/s`, `500M/QPS`).

*(31 PNG đã xem trực tiếp: `L00–L13` mỗi bài 2–4 khung tiêu biểu.)*
