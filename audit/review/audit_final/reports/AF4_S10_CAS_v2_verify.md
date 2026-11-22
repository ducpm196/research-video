# WP-AF4-5 Stage 10 CAS Verifier v2

- **Khoá học**: `CAS` (`L00–L11`, 12 bài)
- **Phán quyết**: **NO-GO**
- **Tóm tắt kiểm tra tự động**:
  - `lv.py lint`: `12/12 PASS` (`13.0–15.2p`)
  - `verify_cas.py`: `93/93 PASS`
  - `loi_giai.py == mong_doi.txt`: `12/12 PASS`
  - `layout_CAS.tsv`: `0` dòng lỗi bố cục
  - Kiểm tra `"càng "`: `0` lỗi
  - `P9`: `12/12`
  - `MP4`: `12/12 STALE` (cần dựng lại sau khi sửa về `GO`)

## Lỗi MUST cần sửa

1. **Sai số học / tính toán — `L01/de.md`**:
   - Đề khẳng định `1 << 24` cho ra `0.3433 s`, nhưng thực tế `1 << 24` cho ra `0.1287 s`; `2^23` mới cho ra `0.3433 s`.
   - Cách sửa: đổi sang `1 << 23` (với số giờ phân biệt, ví dụ `48h/72h`) hoặc bỏ con số `0.3433 s` sai lệch.

2. **Sai công thức & chất lượng đề bài — `L09`**:
   - `L09/loi_giai.py` tính `(1 + 2 + 65535 + 16) - 20 = 65534` do cộng thêm 16 byte padding thay vì `65535 - (20 - 3) = 65518`.
   - `L09/de.md` thiếu định nghĩa rõ ràng, làm lộ công thức ngay trong tiêu đề và lặp nguyên bộ số `(65535, 20)`.

3. **Lặp cụm từ giải thích nội dòng (3x–4x)**:
   - `L00` (`:205`): `(giữ bộ nhớ không trả lại)` lặp 4 lần.
   - `L00` (`:221`): `(bảng tra cứu vị trí)` lặp 4 lần và `(nhóm nhiều máy chủ)` lặp 4 lần.
   - `L08` (`:191`): `($1\text{ GB} = 1000\text{ MB}$)` lặp 3 lần.
   - `L11` (`:184`): `(kiểu cột lưu ngày–giờ)` lặp 3 lần.

4. **`screen_code/cas.yaml` STALE**:
   - `CAS L03 design 0 0` lệch hash (`1787ec543f6f10df` -> `32acf78b6b7cdde4`).

5. **P8 — Lộ công thức / lặp số bài giảng trong `de.md`**:
   - `L06/de.md`: làm lộ `(max_removable = 20)`.
   - `L11/de.md`: tiêu đề làm lộ `(2038), (2106)`.
   - `L07/de.md`: lặp nguyên `n=200` từ thân bài.

6. **P1 — Bảng đọc Python & định dạng HTML**:
   - Nhiều cảnh gặp false positive do `common.py` cũ (nay xử lý qua `ast_p1.py`).
   - `L05 check#0`: bổ sung giải thích dict comprehension.
   - `L00`: bổ sung thuật ngữ `quay lui`.
   - `L07 recap#1`: đổi backtick thô `` `.*.*=.*` `` thành `<code>...</code>`.

7. **`covers:` lệch scene trên `12/12` bài**:
   - Rà soát và khớp lại `check` với `timeline`/`pitfalls`/`quiz`/`design`/`formula`/`intuition`/`inventory`.
