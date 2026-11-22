# WP-AF4-3 Stage 8 Independent Verification Report — `DEN` (`L00–L14`, 15 bài)

**Verifier:** `147e0202` (`WP-AF4-3 Stage 8 DEN Verifier`, strictly read-only)  
**Verdict:** **`NO-GO`**

> **Tóm tắt chỉ số:**
> - **MUST:** **`2`** (`L07` `loi_giai.py` không cài BM25 như `de.md`/`practice#0` yêu cầu; `L13` mâu thuẫn số liệu/công thức `990,99 ≈ 991 GB` / `90,0%` trong `curriculum/den.yaml` + `example`/`check` so với `shuffle_gb=1001` / `90.1%` trong `practice` + `labs/DEN/L13/de.md` + `loi_giai.py` + `mong_doi.txt`)
> - **P1:** Core `hook..recap` = **`15/15 (100%)`**; Strict (gồm `practice#0` trên màn hình) = **`5/15 (33.3%) < 80%`** (10/15 bài để lọt thuật ngữ/tiếng Anh chưa chú thích tại `practice#0`: `L02, L05, L06, L07, L08, L09, L10, L11, L12, L14`; kèm `de.md` ở `L04, L13`)
> - **P8:** Cấu trúc AF2/AF4 (`hook`, `recap`, `practice`, `E39/E40/E51/E53`) = **`15/15 (100%)`**; Khớp thực chất `practice`/`lab` với bài giảng = **`13/15 (86.7%) < 100%`** (gãy ở `L07`, `L13`; lệch mô tả phụ ở `L06`, `L12`)
> - **P9:** **`15/15 (100%)`** (`36/36` PNGs `1920x1080` sạch đẹp, 0 tràn/đè chữ; `audit/layout_DEN.tsv` = 0 lỗi)

---

## 1. Cổng tự động & Kiểm tra chéo (`L00–L14`)
- `audit/den/verify_den.py`: **`15/15 PASS`** (`L00..L14`).
- `lv.lint`: **`15/15 PASS` (`0` errors, `0` warnings)**.
- `spec_sha256` & `tts_sha256` & `frames_match`: **`15/15 match`**.
- `SRT == say`: **`15/15 exact match`**.
- `asr_report.md`: **`15/15` (`thiếu audio: 0`, `chưa xem xét: 0`)**.
- `audit/layout_DEN.tsv`: Trống (`0` lỗi).
- `audit/review/screen_code/DEN.yaml`: `17/17` khối khớp SHA (`missing=0, orphan=0, stale=0`).
- `labs/DEN/L00..L14/loi_giai.py == mong_doi.txt`: **`15/15` khớp stdout** (nhưng `L07` đi đường tắt `.count()` và `L13` dùng `1001` sai với bài giảng).

---

## 2. Đánh giá chi tiết từng bài (`L00–L14`)
- **`L00`**: Sạch kỹ thuật (`SHOULD`: `SELECT *` ở `pitfalls` Lỗi 3 nên chú thích `* = mọi cột`).
- **`L01`**: Sạch 100%.
- **`L02`**: Sạch kỹ thuật (`SHOULD` P1: `B-Tree` / `4 KiB` ở `practice#0`/`de.md`, chú thích `40,96 ≈ 41,0`).
- **`L03`**: Sạch kỹ thuật (`SHOULD`: `collection riêng` → `tập (collection) riêng` ở `de.md`).
- **`L04`**: Sạch kỹ thuật (`SHOULD`: `partition key (salting 0..9)` → chú thích `khoá phân vùng (chia muối)` ở `de.md`).
- **`L05`**: Sạch kỹ thuật (`SHOULD` P1: `sensor` → `cảm biến` ở `practice#0`).
- **`L06`**: `SHOULD` P1+P8: `practice#0` ghi `"dùng BFS SQLite tìm nhanh đồ thị thực"` không khớp lab tính `100^k`; Việt hóa `BFS` (`duyệt theo chiều rộng`).
- **`L07`**: **MUST-1**: `labs/DEN/L07/loi_giai.py` dùng `.count('meo')` thay vì tính BM25 thật (`k1=1.2, b=0.75`, `idf`, `avgdl`) như `de.md` yêu cầu. `SHOULD` P1: chú thích `TF-IDF`, `docID`.
- **`L08`**: Sạch kỹ thuật (`SHOULD` P1: `consumer`; `pitfalls` Lỗi 4 bổ sung đối chiếu 2 quy mô cạnh 2 công thức).
- **`L09`**: Sạch kỹ thuật (`SHOULD` P1: `Checkpoint`).
- **`L10`**: Sạch kỹ thuật (`SHOULD` P1: `Outbox`, `SQLite`).
- **`L11`**: Sạch kỹ thuật (`SHOULD` P1: `Row Group`, `min/max`, `Predicate Pushdown`).
- **`L12`**: `SHOULD` P1+P8: `practice#0` nhắc `SCD`, `valid_to`, `is_current=1` nhưng `de.md`/`loi_giai.py` dùng bảng `scd(city, f, t)`.
- **`L13`**: **MUST-2**: `practice#0`, `practice#1`, `de.md`, `loi_giai.py`, `mong_doi.txt` ghi `shuffle_gb=1001`, `network_saved_pct=90.1%`, mâu thuẫn với bài giảng & `curriculum/den.yaml` (`(1000+1)*99/100 = 990.99 ≈ 991 GB`, tiết kiệm `90.0%`). `SHOULD` P1: chú thích `Broadcast Join`, `Shuffle Join` ở `de.md`.
- **`L14`**: Sạch kỹ thuật (`SHOULD` P1: `MapReduce`, `job` ở `practice#0`/`de.md`).

*(Danh sách 36 PNG đã xem trực tiếp: `L00/{00020,00024,00065,00066,00070}`, `L01/{00034,00085}`, `L02/{00026,00073}`, `L03/{00016,00021}`, `L04/{00021,00057}`, `L05/{00015,00020}`, `L06/{00019,00066}`, `L07/{00023,00062,00077}`, `L08/{00015,00063}`, `L09/{00021,00072}`, `L10/{00022,00071}`, `L11/{00018,00070}`, `L12/{00019,00052,00067}`, `L13/{00020,00053,00067}`, `L14/{00025,00029,00142}`.)*
