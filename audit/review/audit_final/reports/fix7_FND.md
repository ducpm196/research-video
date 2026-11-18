# fix7_FND — sửa khoá FND vòng 7 theo `reports/R5_FND.md` — 2026-11-17

Nguồn sửa: `audit/fnd/src/l00..l10.py`, `audit/fnd/lib.py` (hai thay đổi chung cho FND, xem dưới), `tools/registry/lexicon_vi.FND.yaml` (thêm luật đọc Python), `curriculum/fnd.yaml` (hai chỗ). Chạy `gen.py` cho cả 11 bài; không sửa YAML sinh ra bằng tay. Sổ `audit/review/screen_code/FND.yaml` sinh lại bằng `gen-fnd` (bản cũ ở scratchpad `fnd6/FND_screen_code_before7.yaml`). Không chạy tts/asr/build/docker. `lv.py render` được phép chạy.

## Bài đổi (đều cần dựng lại): L00–L10 (cả 11; L02 và L03 đổi lời/hình thật; L01–L10 cũng đổi vì `lib.py` làm ghi chú đậm hơn và cột 1 không gãy dòng)

## Hai thay đổi chung trong `audit/fnd/lib.py` (không đụng `player.css` dùng chung)
- Ghi chú xám nhạt: `st()` thêm `style='color:#475569'` cho mọi `class='note'` của FND (đậm hơn `--muted` #6b7280; khi khối đã qua còn bị mờ `opacity .62` nên vẫn đọc được).
- Gãy dòng cột 1: `table()` thêm `white-space:nowrap` cho ô cột 1 khi bắt đầu bằng `<code>` và ≤ 28 ký tự chữ (sửa `cp a b`, `mv a b` L02; `set -e`, `A && B`, `A || B` L04; `khoa: gia_tri` L06; `kill $SV` L07).

## 4 mục "vừa" (bắt buộc)
| Bài | Mục | Xử lý |
|---|---|---|
| L00 | `javac` ở caidat step 4 | hàng "kiểm" của bảng JDK giải `java -version` (chương trình chạy Java) và `javac -version` (trình biên dịch: chương trình dịch mã Java sang dạng máy chạy được); lời đọc giảng trình biên dịch tại đó; bỏ lời giảng trùng ở pitfalls |
| L01 | "độ sâu" | step mới ngay trước formula step 3: độ sâu = số thư mục đếm từ gốc `/`; ví dụ `/c` sâu 1 … `/c/Users/ban/hoc/nen` sâu 5 |
| L05 | `"x = " + x` | step bảng thứ hai (4 hàng): `println`, `int x = 5;`, `"x = " + x` (dấu `+` nối chữ với giá trị), dấu `;`; ngay trước các phép đọc lỗi |
| L09 | `sed -i` ở practice | đề thực hành ghi `sed -i 's/cũ/mới/' tệp` (thay chữ ngay trong tệp) + lời đọc "dạng s gạch chéo cũ gạch chéo mới, cờ i sửa ngay trong tệp" |

## Mục yếu
- Quy tắc "một dấu gạch + vài chữ = vài cờ riêng": giảng ở L03 (`sort -rn` = `sort -r -n`, hàng bảng + lời); nhắc ở L07 (`-sf` = `-s -f`) và L09 (`-am` = `-a -m`).
- L00: `"$1"`/`"$2"` nháy kép giữ giá trị là một chữ nguyên vẹn (hàng bảng + lời); gọi tên Python ở lần đầu (hai chỗ).
- L04: `cut -d' ' -f1-2`, `cut -d. -f1` giải ở ghi chú "Nếu kẹt" (cột ngăn bằng dấu cách / dấu chấm, lấy cột 1 tới 2; ví dụ biến đổi) + lời đọc.
- L05: `main(String[] args)` = "khung bắt buộc, `args` là nơi chứa đối số gõ sau tên chương trình"; step Python mới: `loi.py` viết bằng Python, `sodu = 100` gán, `print(...)` in, `python loi.py` chạy tệp (lời đọc gọi tên Python).
- L06: `len(hang)`, `print(a, b)` giải ở ghi chú phép ③; `head -n 1 tệp` giải ở scale; dấu `>` tiếp dòng của `python -c "…` ở quiz (chữ + lời); gọi tên Python trong lời ở hook, phép ②, pitfalls.
- L07: `\n` trong `-w "%{http_code}\n"` (lệnh ở cột 1 nay có `\n`, giải "xuống dòng"); `-sf` như trên.
- L08: step riêng 3 hàng `sqlite3 $DB 'câu SQL;'` (chạy câu trong nháy đơn; dấu `;` kết thúc câu SQL), `CREATE TABLE`, `INSERT`; hàng SELECT giải `SELECT *` (mọi cột) và `COUNT(*)`; hai bảng ≤ 4 hàng, `clear: true`.
- L10: bảng ôn ⑤ liệt kê đủ mệnh đề SQL (`SELECT … FROM … WHERE … GROUP BY … ORDER BY … LIMIT`, `*`, `COUNT(*)`, `AND`) + lời đọc.

## SHOULD
- L02: tiêu đề hook và step 2 "xoá sạch mọi tệp trong thư mục" ("Thư mục không còn tệp thường nào"); `curriculum/fnd.yaml` L02 example cùng chữ.
- L05: bảng khuôn UTF-8 có hàng 4 byte (65 536 .. 1 114 111, `11110xxx 10xxxxxx 10xxxxxx 10xxxxxx`); lời đọc nói số lớn hơn dùng bốn byte, bài không cần tới.
- L08: lời đọc "An Le, không dấu như trên màn hình".
- L04 (cột 1 không gãy), L09 (`git branch`, `git switch`, `git merge` cách nhau dấu phẩy), L02, L06, L07 (nowrap): xem trên.
- Ghi chú xám nhạt: tăng tương phản bằng `lib.py` (xem trên).

## Lexicon
`lexicon_vi.FND.yaml`: thêm `Python` → `Pai-thon` (chép từ BNK/PYT/BNX, đã ASR ở các khoá đó; NOT_VERIFIED bằng tai người ở FND). Chú thích đầu tệp đã sửa (Python là ngoại lệ). Người điều phối nghe lại chữ "Python" khi dựng.

## Lời đọc (từ)
L00 3129 (≤ 3133, ngoại lệ không dài thêm) · L01 2121 · L02 2087 · L03 1995 · L04 2288 · L05 2298 · L06 2053 · L07 2291 · L08 2300 · L09 2196 · L10 2298. Mọi bài ≤ 2300 trừ L00. Lint 11 bài: 0 FAIL, 0 WARN.

## Kết quả cổng (sqlite3 shim; PYTHONIOENCODING=utf-8)
- `lv.py lint` 11 bài: 0 FAIL, 0 WARN (lần đầu gặp: L00 hai câu > 38 từ, L01 thiếu từ lý do ở step "độ sâu", L05 câu dài và `args` không phải âm tiết Việt (đọc "a r g s"), L07 focus 6/7; đã sửa).
- `lv.py render` 11 bài: **0 vấn đề** ở cả 11 (188/146/147/137/141/146/131/144/148/149/142 khung). Chưa xem ảnh khung PNG bằng mắt.
- `verify_fnd.py`: **83/83 PASS**.
- `screen_code.py gen-fnd` (206 khối, chưa khớp 0) rồi `check --course FND`: **PASS 300 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0**.
- `lab_gate.py FND`: 11 PASS · 0 FAIL (196 lab). `arith_scan.py FND`: 0 FAIL. `tests/test_e52.py`: 0 FAIL. `lv.py curriculum curriculum/fnd.yaml`: 0 lỗi. `check_course_refs.py FND`: 0. `check_next_refs.py`: 550 lời hẹn, 0 lệch.
- Chưa chạy lại: `check_curricula_graph.py`, `check_meta.py`, `check_xref.py` (không đổi cấu trúc giáo án; chỉ sửa chữ ở ví dụ).

## Ước số mục chưa giảng còn lại (theo R5): 4 vừa → 0; 15 yếu → 0 ước (mỗi mục đã có một câu/hàng bảng tại chỗ). Chưa có người đọc chấm lại.
