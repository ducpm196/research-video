# Báo cáo xác minh độc lập (read-only) — WP-AF4-5 Stage 9 CS115 L22–L43 (Verifier v2)

**Phán quyết tổng thể: NO-GO**

## 1. Tóm tắt kiểm tra tự động
- `labs/CS115/L22..L43/loi_giai.py` vs `mong_doi.txt`: **22/22 PASS** (`rc=0`, stdout khớp 100%)
- `tools/lv.py lint` (`L22..L43`): **PASS=592, FAIL=0, WARN=0**; `checks:` **350/350 PASS**
- `tools/lv.py curriculum curriculum/cs115.yaml`: **47/47, 0 lỗi**
- `audit/verify_cs115_tex.py`: **59/59 PASS**
- `check_meta`, `E55`, `E38`, cân thẻ `<div>`, `preview.html`: **0 lỗi**
- **ĐÃ ĐẠT** trên 22/22: ẩn code trước `pause: 30`, `covers:` E51, P1 thuật ngữ thân bài, P9 (`Hai mức quy mô` + `recap`), `"càng "` & `<svg>`.
- `audit/layout_CS115.tsv`: đang trống (cần chạy ngoài sandbox với browser).

## 2. Danh sách MUST fix

### M1. `[P1]` Bảng đọc mã `practice` (`22/22` bài `L22–L43`) vẫn dùng `_legacy_build_read_rows`
- Báo giả `dict` (`20/22` bài `L22–32, L35–43`), `set` (`L34`), `for/lambda` (`L24`), `elif/else` (`L33`); thiếu token thật (`L24 set/==/int/for a,b`, `L25 *w/tuple`, `L31 M[i][j]`, `L33 < / ==`, `L43 += / *=`, `22/22` thiếu `= / + / - / * / /`). Cần chạy lại với `ast_p1.py` và đồng bộ `screen_code/CS115.yaml`.

### M2. `[P8]` Mâu thuẫn công thức MSE trong `labs/CS115/L37/de.md` vs `loi_giai.py` & `mong_doi.txt`
- `L37/de.md:3` viết *"MSE theo từng toạ độ"* (8 giá trị -> `3.1250`), nhưng `L37/loi_giai.py:4` chia `len(pts) = 4` -> `6.2500`. Cần đồng nhất `de.md` (hoặc sửa `loi_giai.py`).

### M3. `[P8]` Lộ đáp số và công thức trong `labs/CS115/L42/de.md`
- Tiêu đề `L42/de.md:1` lộ `(-ln 4)`; thân đề `L42/de.md:3` lộ `D* = 0.5` và `-ln(4)`; khuôn đầu ra `L42/de.md:7` gán cứng `gan_nash_d=0.50` (cần đổi thành `gan_nash_d=<2 chữ số>` và đồng bộ `L42_vae_gan.yaml:315`).

## 3. SHOULD fix
- `lessons/cs115/L27_knn.yaml`: `1.204` từ (`8,03–8,60p < 9,0p`) -> bổ sung ~100 từ trực giác/số đo vào `hook` & thân bài; bổ sung số đo vào `hook` (`L28–L39`, `L27/28/33` `intuition`).
- `labs/CS115/L24/de.md`: bỏ `p_k = c_k / sum(c)`, ghi rõ `round(x, 1)` (`<1 chữ số>`).
- `labs/CS115/L34/de.md`: bỏ 2 công thức khỏi tiêu đề & đề; `L36/de.md`: đổi `eps=0.1` trùng quiz → `0.15/0.2`; `L31/de.md`: làm rõ tổng bình phương sai lệch.
- Chạy `layout_scan.py CS115` ngoài sandbox.
