# fix8_FND — sửa nhỏ vòng 8 theo `reports/R6_FND.md` — 2026-11-17

Nguồn sửa: `audit/fnd/src/l00,l02,l04,l05,l06,l08,l09,l10.py`, `audit/fnd/lib.py`, `curriculum/fnd.yaml` (mục tiêu L00). Chạy `gen.py` cả 11 bài. Sổ `screen_code/FND.yaml` sinh lại bằng `gen-fnd` (bản cũ ở scratchpad `fnd6/FND_screen_code_before8.yaml`).

## Bài đổi (cần dựng lại): L00, L02, L04, L05, L06, L08, L09, L10. Vì `lib.py` đổi (màu ghi chú, cột 1 và tuỳ chọn dài không gãy dòng) nên nên dựng lại cả 11 bài (L01, L03, L07 chỉ đổi hình thức).

## Mục chưa giảng
- L09 pitfalls#0 (vừa): ghi chú + lời đọc "`> /dev/null` chuyển đầu ra thường vào chỗ bỏ đi, chỉ giữ mã thoát".
- L09: `%h` (hàng bảng + lời: trong khuôn `%s` là lời nhắn, `%h` là mã băm rút gọn); `wc -l` (check#0: lệnh đếm dòng có cờ l).
- L04: `type -t`, `which` bỏ khỏi tiêu đề khung (chỉ còn `command -v`).
- L05: `>>` ở scale (ghi chú: nối thêm vào cuối tệp, một dấu `>` thì ghi đè; lời đọc nói "hai dấu lớn hơn").
- L08: nháy kép ngoài / nháy đơn trong ở phép ② (ghi chú + lời đọc).
- L10: prereq nhắc `head -n 7`/`tail -n 7`; `git init -q`, `git status -s` (`??` = chưa theo dõi), `git log --format=%s`; awk: `s` chưa gán thì bắt đầu bằng 0 (hàng bảng + lời đọc).

## SHOULD
- Cột đầu bị gãy dòng: `lib.table()` đặt `white-space:nowrap` cho ô cột 1 bắt đầu bằng `<code>` và ≤ 48 ký tự chữ; `st()` đặt nowrap cho mã chứa tuỳ chọn dài `--…` (≤ 40 ký tự). L08: ô UPDATE/DELETE tách hai dòng bằng `<br>`. Đã xem khung: L00 kiemsh#2 (khung 132), L04 sym#1 (21), L05 example#1 (54), L07 sym#1 (23), L08 sym#2 (22), L09 practice#0 (125): không còn gãy giữa token/tuỳ chọn.
- L00 "bốn bước" vs hoc#0 vẽ năm bước: mục tiêu (L00 + `curriculum/fnd.yaml`) đổi thành "năm bước (xem, tự làm, chấm, đánh dấu, ôn)"; chuỗi recap và lời đọc recap thêm "đánh dấu".
- L02 pitfalls#2: demo `echo "$DIR"/` (ra `/`); ghi chú và lời đọc: `"$DIR"/*` mở ra `/*`, tức mọi mục ngay dưới gốc.
- L06 intuition#0: ba tiêu đề panel thêm "(rút gọn)" và lời đọc "hình vẽ rút gọn vài trường, nhưng ba dạng chứa cùng thông tin".
- Ghi chú xám: `NOTE_STYLE` đổi `#475569` thành `#111827` (tính: sau `.blk.past opacity .62` còn ≈ 5:1 trên #fff7e6; với `#475569` đã đo 3,18:1 ở vòng 6). Không sửa `player.css`.

## Lời đọc (từ)
L00 3131 (≤ 3133) · L01 2121 · L02 2096 · L03 1995 · L04 2288 · L05 2292 · L06 2060 · L07 2291 · L08 2295 · L09 2230 · L10 2297. Mọi bài ≤ 2300 trừ L00.

## Cổng
- `lv.py lint` 11 bài: 0 FAIL, 0 WARN. `lv.py render` 11 bài: 0 vấn đề (188/146/147/137/141/145/131/144/148/150/143 khung).
- `verify_fnd` (shim): 83/83 PASS. `screen_code` FND sau gen-fnd: PASS 300 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0.
- `lab_gate FND`: 11 PASS. `arith_scan`: 0 FAIL. `test_e52`: 0 FAIL. `lv.py curriculum`: 0 lỗi. `check_course_refs`: 0. `check_next_refs`: 550 lời hẹn, 0 lệch.
- Chưa tự chạy lại: `check_curricula_graph`, `check_meta`, `check_xref`.

## Không làm / lưu ý
- Bảng L04 sym#1 vẫn 5 hàng dữ liệu (đã có từ trước, không tràn khi render).
- Độ tương phản ghi chú tính bằng công thức, chưa đo lại điểm ảnh trên bản dựng mới.
