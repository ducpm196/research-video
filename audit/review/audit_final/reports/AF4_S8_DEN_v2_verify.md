# Báo cáo kiểm định độc lập WP-AF4-5 Stage 8 — Khóa `DEN` (`L00–L14`, v2)

**Phán quyết tổng thể:** **`NO-GO`**

## 1. Tóm tắt kiểm tra tự động
- `audit/den/verify_den.py`: **15/15 PASS**
- `tools/lv.py lint` (`L00–L14`): **15/15 PASS (`0 FAIL, 0 WARN`)**
- `arith_scan.py DEN`: **19/19 PASS**
- `loi_giai.py` vs `mong_doi.txt`: **15/15 MATCH**
- `screen_code/DEN.yaml` SHA: **17/17 khớp**; `layout_DEN.tsv`: **0 lỗi**; SVG `L00..L14`: sạch
- `out/den/L*/build_report.json`: **15/15 `STALE_SPEC`** (dựng cũ `2026-11-20 02:03–02:28`)

## 2. Danh sách MUST fix

1. **Rebuild MP4/ASR `15/15` & thời lượng `>= 9.0p`** (`10/15` bài `< 9.0p` thực tế: `L00, L03, L05, L06, L08, L09, L10, L11, L12, L13` `7.98–8.85m`) + chạy `layout_scan.py DEN`.
2. **`[P8]` `15/15` `de.md` lộ đáp số/công thức + `13/15` trùng số bài giảng + `4` lỗi tự đủ (`L04, L05, L06, L12`)**:
   - Lộ đáp số ngay ở `de.md` (`L00–L14`) và `Kiểm chứng` của `practice#0` trước `pause: 30` (`L00..L03, L05, L06, L08, L09, L11, L13`).
   - Trùng số bài giảng: `L00–L03, L05–L09, L11–L14` (kèm `L04, L10` chỉnh sâu hơn).
   - Tự đủ/khớp thực chất: `L04` nói "băm" nhưng không cho hàm băm; `L05/de.md` thiếu ngưỡng `100 MB`, `1 MB = 10^6 B`, `365 ngày`; `L06` nói "BFS đồ thị" nhưng `loi_giai` chỉ tính `100**k`; `L12` thân bài dùng `[f, t)` còn `loi_giai` dùng `BETWEEN`.
3. **`[P1]` Thiếu bảng đọc mã Python `0/15` bài & thuật ngữ tiếng Anh chưa giảng**:
   - Sinh bảng đọc mã qua `ast_p1.py` (kèm `sqlite3` / SQL ở `L10, L12`) cho cả `15/15` bài trong `audit/den/af2/upgrade_den.py`.
   - Thuật ngữ chưa giảng ở thân bài: `SELECT` (`L00`), `FPR` (`L01`), `B-Tree, 4 KiB` (`L02`), `collection` (`L03`), `partition key, salting` (`L04`), `IoT` (`L05`), `BFS` (`L06`), `docID, TF-IDF, df` (`L07`), `consumer, consumer group` (`L08`), `Checkpoint` (`L09`), `Outbox, SQLite, INSERT INTO, ROLLBACK` (`L10`), `min/max, Row Group, Predicate Pushdown` (`L11`), `SCD, SQLite` (`L12`), `Broadcast/Shuffle Join` (`L13`), `MapReduce, job` (`L14`).
4. **`[P9]` Thiếu `Hai mức quy mô` trong `recap` ở `15/15` bài** (và thân bài `L12` thiếu so sánh 2 quy mô định lượng).
5. **`covers:` gán cứng sai ở `15/15` bài** (do `audit/den/af2/upgrade_den.py:208` gán cứng `[(1, 'example'/'stage1'), (2, 'check'), (3, 'practice')]` — cần gán chính xác theo nội dung từng bài `L00–L14`).

## 3. SHOULD fix
- `L12_kho_du_lieu.yaml:246,249`: đổi `"độ mịn càng mịn càng tốt"` → `"chọn độ mịn đủ chi tiết cần hỏi"`; `L09:220`: đồng bộ `say` theo `show`.
- `L13/de.md:1`, `L07/de.md:3`: giảm ngoặc đơn kề/lồng; `L08:77` SVG nới hộp `width="155"`.
- Chạy `screen_code.py check --course DEN` và `lab_gate.py DEN` ngoài sandbox sau sửa.
