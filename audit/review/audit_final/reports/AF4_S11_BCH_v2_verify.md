# Báo cáo kiểm định ĐỘC LẬP AF4 v2 — Khoá Stage 11 BCH (`L00–L12`, 13 bài)

## 1. Kết luận: **NO-GO** (phần lõi sư phạm & lab đã tiến bộ rất mạnh; chỉ còn 3 nhóm nhỏ)

- **0/13 bài lộ `loi_giai.py` hay `mong_doi.txt` trước `pause: 30`**.
- **13/13 `labs/bch/L*/de.md` tự đứng được**, tiêu đề không lộ đáp án (`L09` có callback `Vault`+`Attacker` thật, `L12` tính đủ `full_GB` và `ratio`).
- **13/13 đạt ≥ 9 phút**, **13/13 `recap` có `Hai mức quy mô:`**, **`0/13` `"càng "` trong `say`**, **`lv.py lint` 13/13 PASS**, **`verify_bch.py` 13/13 PASS**, **`screen_code` 34 khối PASS**, **`layout_BCH.tsv` 0 lỗi**, **13/13 `loi_giai.py` khớp `mong_doi.txt`**.

Còn 3 nhóm vấn đề chặn phát hành:
1. **MP4/SRT/ASR chưa dựng lại** (`0/13` khớp `spec_digest`).
2. **E51 `covers:` trỏ sai cảnh ở 5/13 bài (`L03, L04, L06, L07, L12`)**:
   - `L03` obj#3 → `sym`/`quiz`; `L04` obj#3 → `sym`/`pitfalls`; `L06` obj#3 → `pitfalls` (obj#1 → `sym`); `L07` obj#3 → `pitfalls`/`prereq`; `L12` obj#3 → `quiz`.
3. **P1 & lỗi nhỏ `de.md`/`show`**:
   - `L09`: thiếu `class / __init__ / self / or / <` ở bảng `practice`; `L09/de.md:3` viết `receive(vault)` trong khi `loi_giai.py` dùng `recv(self, v)`.
   - `L05/de.md:3`: viết `b'khoi-99:' + str(nonce)` (sẽ lỗi `TypeError`, sửa thành `f"khoi-99:{nonce}".encode()`).
   - `common.py` bảng `practice`: nhận nhầm `{...}` trong f-string thành `dict`/`set` trên nhiều bài; thiếu `and/not/True/False` (`L00`), `int(s, 16)` (`L03`), `2_000_000` (`L10`), `1_000_000` & `1e9` (`L12`); một số thuật ngữ chưa mở nghĩa trên chữ màn hình (`ms` L00, `SHA` L01, `UTXO` L04, `PoW` L05, `BFT`/`validator` L07, `Layer-1`/`TPS` L10, `RAM`/`GB`/`TWh` L12).
   - `L08:126` (`example.3` `show`): còn câu `"mã càng ghi ít, phí càng thấp."` (dù `say` đã sửa). `L08/de.md` trùng `50_000 gas, 30 gwei` với `quiz` câu 1.
   - (Khuyến nghị P9 thân bài): thêm đối chiếu 2 mức quy mô ở thân bài cho `L03, L05, L06, L07, L10`.

---

## 2. Bảng chi tiết 13 bài (`L00–L12`)

| Bài | Phút | `covers:` | P1 | P8 | P9 | Lỗi chính |
|---|---|---:|---:|---:|---:|---|
| **L00** | 10.6 | PASS | 1 | 2* | 2 | thiếu `and/not/True/False`, thừa `set()`, `ms` màn hình |
| **L01** | 10.1 | PASS | 2* | 2 | 2 | thừa `set()`, `SHA` màn hình |
| **L02** | 10.2 | PASS | 2* | 2 | 2 | thừa `set()` |
| **L03** | 10.6 | **FAIL** (obj#3) | 1 | 2 | 1 | `covers` obj#3; thiếu `int(s, 16)`, `RSA`; thiếu P9 thân bài |
| **L04** | 10.1 | **FAIL** (obj#3) | 1 | 2 | 2 | `covers` obj#3; mở nghĩa `UTXO`; thừa `dict` |
| **L05** | 11.0 | PASS | 1 | 1 | 1 | `de.md:3` `TypeError` bytes+str; `PoW`; thừa `dict`; P9 thân bài |
| **L06** | 14.0 | **FAIL** (obj#3) | 2* | 2 | 1* | `covers` obj#1/#3; thừa `dict`; P9 thân bài |
| **L07** | 10.9 | **FAIL** (obj#3) | 1 | 2 | 1 | `covers` obj#3; mở nghĩa `BFT`/`validator`; thừa `set()`; P9 thân bài |
| **L08** | 10.7 | PASS | 2* | 1 | 2 | `L08:126` `"càng "` ở `show`; `de.md` trùng `50_000/30` |
| **L09** | 11.4 | PASS | **0** | 1 | 2 | thiếu OOP (`class/__init__/self/or/<`); `recv` vs `receive` |
| **L10** | 10.3 | PASS | 1 | 2 | 1* | thiếu `2_000_000`; `Layer-1`/`TPS`; P9 thân bài |
| **L11** | 10.4 | PASS | 2* | 2 | 2 | thừa `set()` |
| **L12** | 20.1 | **FAIL** (obj#3) | 1 | 1 | 2 | `covers` obj#3 (`quiz`); thiếu `1_000_000`/`1e9`; `de.md` dùng lại `52_560` |
