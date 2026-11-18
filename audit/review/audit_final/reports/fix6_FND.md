# fix6_FND — sửa khoá FND theo `reports/R4_FND.md` (đọc độc lập vòng 4, P1 chặt) — 2026-11-16

Nguồn sửa: `audit/fnd/src/l00..l10.py` → `audit/fnd/gen.py` (không sửa YAML sinh ra); `curriculum/fnd.yaml` (Edit nhỏ); sổ `audit/review/screen_code/FND.yaml` sinh lại bằng `screen_code.py gen-fnd` (bản cũ ở scratchpad `fnd6/FND_screen_code_before6.yaml`). Không chạy build/tts/asr/render/audit_all/docker; không dùng git để ghi. Máy không có sqlite3 chính thức: dùng shim `audit/fnd/shim` (đặt vào PATH trong phiên chạy, `sqlite3 --version` = bản Python sqlite3). Người điều phối chạy lại `verify_fnd`, `lab_gate`, `screen_code check` bằng sqlite3 chính thức.

## Bài đổi (đều STALE, cần dựng lại): L00, L01, L03, L04, L05, L06, L07, L08, L09, L10 (L02 không đổi nội dung; gen.py ghi lại cùng nội dung)

## Mục chưa giảng (mục 3 của báo cáo) → cách xử lý, ước còn lại = 0 ở 11/11 bài
| Bài | Mục | Cách xử lý |
|---|---|---|
| L00 | LTS | bảng caidat: "LTS = bản hỗ trợ dài hạn, được vá lỗi nhiều năm" + lời đọc "L T S, nghĩa là hỗ trợ dài hạn" |
| L00 | x64 | step mới trước bảng JDK (hộp): x64 là chip 64-bit của Intel và AMD; cách biết: Start, `System Information`, dòng `System Type`: `x64-based PC` hay `ARM64-based PC` (chọn bản aarch64). NOT_VERIFIED ghi trong `source`: chữ dòng System Type và việc trang adoptium.net có bản aarch64 cho Windows |
| L00 | regex `[0-9]+\.[0-9.]*[0-9]` | ĐỔI MÃ sang dạng đơn giản `grep -oE '[0-9.]+'` (tệp `kiem.sh`, `de.md`, `loi_giai.sh` sinh lại; kiểm `KiemMay` và `KiemStub` vẫn ra đúng ✔ và THIEU) + hàng bảng giải: `-o`, `[0-9.]` = một ký tự chữ số hoặc dấu chấm, `+` (cần `-E`) = một hay nhiều lần liền nhau, ví dụ `2.53.0` |
| L00 | `;` (có trong `if …; then …; else …; fi`, lần đầu của khoá) | hàng "lệnh điều kiện" giảng `[ "$nho" = "$2" ]` và dấu `;` nối các phần trên cùng một dòng, như một lần xuống dòng. Bảng khối kiem.sh tách lại: grep+printf một step, sort+if+dat git một step |
| L01 | `mkdir 'Tai lieu'` | chú thích tại chỗ: `mkdir` tạo thư mục mới, `cd` đi vào; lời đọc cùng ý |
| L04 | `;` | hàng mới `A ; B` ("rồi", dù A thành công hay thất bại) trong bảng sym; tiêu đề "ba dấu nối lệnh"; chuỗi recap có `;`. Thêm `true` luôn thành công (pitfalls 3) |
| L05 | khung Java | step bảng "viết trong mã Java → đọc là" (5 hàng: `public class`, `public static void main(String[] args)`, `System.out.println`, `int x = 5;`, dấu `;`) trước phép ①; lời đọc không có từ khoá Java |
| L05 | `tr -d '\r' < crlf.sh > lf.sh` | chú thích `tr -d`, `<` (đưa nội dung tệp vào làm chữ vào), `>`; thêm câu về `printf` và `\r\n` ở step trước |
| L06 | `;` trong `python -c` | câu giải tại chỗ ở phép ② (chạy lần lượt từ trái sang phải) |
| L07 | `curl …; echo " ma thoat: $?"` | câu giải `;` + `$?` ở phép ③ (cũng áp cho pitfalls 1, 3 vì cùng dạng) |
| L08 | `sqlite3 $DB < dung.sql` | ghi chú + lời đọc: `DB=` đặt biến; `<` đưa nội dung tệp vào làm chữ vào; thêm lý do "vì các câu hỏi sau cần có bảng" |
| L08 | `rm -f $DB; …`, `(echo id,v; seq …)` | giảng `rm -f`, `;` (hai chỗ); biên: `#` chú thích (pitfalls 3), `AND` (quiz) cũng giảng |
| L09 | `HEAD` ở check | giảng `HEAD` + `git rev-list --count HEAD` ngay ở check 1; biên: `;` (pitfalls 1) và `git rm -q .env` (pitfalls 3) cũng giảng |
| L10 | awk `BEGIN`, `printf %02d %d`, `?:` | CHUYỂN phần nặng sang `de.md`: step quy mô không còn hiện nội dung `sinh.awk`, chỉ giải `seq`, `awk -f ../sinh.awk` và nói bài chỉ cần kết quả; tệp `sinh.awk` nằm ở phụ lục `labs/FND/L10/de.md` (kèm cách chạy lại) |

## SHOULD (4) và giáo án
- L06 intuition: "mọi ngôn ngữ đều có sẵn bộ đọc" (hình + lời) → "hầu hết ngôn ngữ phổ biến có thư viện đọc, có ngôn ngữ dùng sẵn, có ngôn ngữ phải thêm".
- L07: bảng mã nhóm bốn "thường không (trừ 408, 429: chờ rồi thử lại)"; lời đọc formula 3 "thường vô ích … trừ vài mã như 429"; pitfalls 2 và đáp án quiz 2 "thường".
- L07: "ký tự" → "byte" ở `Content-Length` (hook, phép ②, lời đọc).
- L05 phép ③: "số dòng nằm ở dòng bắt đầu bằng chữ File, phía trên" (+ ghi chú màn hình có dòng `File "loi.py", line 2, in <module>`).
- `curriculum/fnd.yaml` L05 example: "ể (7 875)" → "ễ (7 877) 3 byte e1 bb 85".
- L00 scale: bỏ câu cuối ("Cách cũ…") nên viền focus không còn dừng ở dòng chú thích "Số minh hoạ" khi nói kết luận; focus kết thúc ở hàng ×10 000.
- L03 scale: khung nay hiện cả lệnh `seq … > t12.txt`, `seq 1 1200 > t1200.txt`, `seq 1 120000 > t120k.txt` (term_block từ bước 0/3/6); lời đọc "byte, tức dung lượng tệp" thay "số ký tự".

## Lời đọc (từ)
L00 3133 (CB-L00, trước 3147: giảm dù thêm LTS, x64, regex, `;`) · L01 2066 · L02 2082 · L03 1971 · L04 2270 · L05 2290 (trước 2320) · L06 2001 · L07 2266 · L08 2300 (trước 2341) · L09 2165 · L10 2296 (trước 2311). Mọi bài ≤ 2300 trừ L00. Không câu mới nào ngoài 4–38 từ (lint 0 WARN).

## Cổng (sqlite3 shim)
- `gen.py`: 11 bài, 0 từ chối. `verify_fnd.py`: **83/83 PASS** (trước 80; thêm các phiên của khối mới, `KiemStub` kiểm regex mới).
- `lv.py lint` từng bài 00–10: **0 FAIL, 0 WARN** (lần đầu gặp: L00 focus 8/7, câu dài, `Windows` trong lời; L05 câu 39 từ; L07 câu 39 từ; L08 thiếu lý do; đã sửa).
- `lv.py curriculum curriculum/fnd.yaml`: 11 bài, 0 lỗi. `tests/test_e52.py`: 0 FAIL.
- `screen_code.py check --course FND`: lần đầu FAIL 2 (do máy không có sqlite3 trên PATH), STALE 11, MISSING 3, ORPHAN 4 → với shim FAIL 0; sau `gen-fnd` (206 khối, chưa khớp 0) và sửa cuối L05 (2290 từ): **PASS 300 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0**; `test_e52` 0 FAIL; `curriculum` 0 lỗi (chạy lại sau sửa cuối).
- `lab_gate.py FND`: **11 PASS · 0 FAIL** (196 lab). `arith_scan.py FND`: 3 phép tính, 0 FAIL. `check_curricula_graph.py`, `check_course_refs.py FND`, `check_next_refs.py` (550 lời hẹn, 0 lệch), `check_meta.py`, `check_xref.py`: 0 vấn đề mới (xref 14 lượt không đổi).
- KHÔNG chạy `lv.py render`: các khối bảng mới (L00 x64, L05 khung Java, L08 `<`) có thể cần người điều phối xem tràn khung khi dựng; các step mới đã đặt `clear` riêng để khỏi chồng khung.

## Không làm / lưu ý
- `check_env.sh` (công cụ riêng, không phải `kiem.sh`) giữ regex cũ.
- Không sửa lexicon/symbols (không thuật ngữ then chốt mới). Không đổi số bài/id/thứ tự, `requires_ext`.
- Chưa nghe âm thanh; câu đọc "a r m", "L T S", "m s i" theo cách đánh vần đã dùng trong khoá.
