# fix4_S01_FND — sửa khoá FND vòng 4 theo `reports/R_S01d_FND.md` — 2026-11-14

Nguồn sửa: `audit/fnd/src/l00..l10.py` → `gen.py` (không sửa YAML sinh ra bằng tay); `de.md` L01 sinh lại từ nguồn; sổ `audit/review/screen_code/FND.yaml` sinh lại bằng `gen-fnd` (bản cũ ở scratchpad `FND_screen_code_before4.yaml`). Không chạy build/tts/asr/audit_all/git/docker; không tải gì từ mạng. Cả 11 bài đổi lời đọc hoặc hình, nên 11 bài FND đều STALE: người điều phối dựng lại.

## Bản `sqlite3` đã dùng
`sqlite3.exe` 3.46.0 (2024-05-23, 64-bit) mượn trong scratchpad (`…\scratchpad\sqlbin\`), đặt vào PATH chỉ trong phiên chạy, KHÔNG chép vào kho. Người điều phối chạy lại `verify_fnd`, `lab_gate FND`, `screen_code check` bằng bản chính thức.

## MUST: 0 (báo cáo không có MUST). SHOULD: 7/7 đã sửa (đã kiểm lại từng cái bằng chạy thật trước khi sửa)
| Bài | Kiểm lại | Sửa |
|---|---|---|
| L10 pitfalls#3 ↔ quiz | Đúng: dựng chuỗi `so_tay_loi.sh` chạy 2 lần trên `so_tay.db` rồi 2 câu của quiz bằng sqlite3 thật → `20` hàng, `1500000`, `2026-01-02\|7000000` (gấp đôi đáp án trên màn hình). | `so_tay_loi.sh` ghi vào `loi.db` (không đụng `so_tay.db`); khung tệp và lời đọc nói rõ; lệnh đếm hiện `sqlite3 loi.db …` → 20. `verify_fnd` thêm phiên `PhienLapRoiQuiz`: `so_tay.sh`, chạy tệp lỗi 2 lần, `loi.db` = 20 hàng, `so_tay.db` vẫn 10 hàng, quiz vẫn ra `750000` và `2026-01-02\|3500000` (PASS với sqlite3 3.46.0). |
| L09 pitfalls#1→#2 | Đúng: git thật trong thư mục tạm, không add/commit trước thì `git status -s` ra `?? a.txt`; có add+commit rồi sửa thì ` M a.txt`. | Khung lỗi 1 nay hiện từ `echo a > a.txt`, `git add a.txt`, `git commit -q -m 'a'` rồi sửa và chốt lần hai (phiên `PhienLoi` đã chạy thật); lỗi 2 nói rõ dòng `M` là tệp `a.txt` còn dở từ lỗi 1 (chữ + lời đọc). |
| L07 sym#2 | Đúng (lời "vài phần giây", màn hình `sleep 1`). | Lời đọc: "chờ cho máy chủ một giây". |
| L04 example#2 | Đúng. | Phiên `PhienMa` có `echo "xin chao" > a.txt` hiện ở đầu khung; chú thích `grep -q` (tìm im lặng, không in, chỉ để lại mã thoát). |
| L06 scale#0 | Đúng. | Tách hai step: step 1 hiện lệnh sinh `a10k.csv`/`a10k.json` + `wc -c` (đo thật 178894 / 418894), kèm giải `seq` và `sed 's/.*/…&…/'` (`.*` = cả dòng, `&` = chính phần khớp); step 2 hiện hai dòng `head -n 1`. |
| L01 practice#1 | Đúng theo hành vi chuẩn của `ls` khi đầu ra là cửa sổ lệnh (cột). | Đề (chữ + lời đọc) và `de.md`: chạy trực tiếp `ls` xếp cột, viết `ls -1` để mỗi tên một dòng như kết quả mong đợi, máy chấm coi cả hai cách ĐÚNG. Kiểm: `di.sh` dùng `ls -1` → `cham.sh FND L01` ĐÚNG; lời giải dùng `ls` vẫn ĐÚNG (lab_gate). |
| L05 hook#0 | Đúng (cp1252 = Windows Tây Âu). | Lời đọc: "một bảng mã cũ dành cho chữ Tây Âu, còn gặp trên một số máy cũ"; màn hình: "cp1252 của Windows Tây Âu". |
| L06 frame 00092 (tràn viền) | Đúng. | Hai lệnh `python -c` ở quiz chia hai dòng trong nháy kép (`> print(…)`, đúng như cửa sổ lệnh hiện dấu nhắc tiếp); đã chạy thật (30000000, 60000000); render lại, đã xem khung 00098: không tràn. |

## P1 (thuật ngữ tại chỗ)
- L00: `printf '%s\n%s\n'` có hàng riêng trong bảng giải kiem.sh (khuôn chữ, `%s` = một chỗ điền, `\n` = xuống dòng, ví dụ `printf '%s\n%s\n' 2.28 2.53` in hai dòng; ở tệp: mức thấp nhất và số phiên bản thật); khung `kiem.sh` được giữ lâu hơn (thêm câu mời dừng video chép + `pause: 40`); bảng giải tách hai step (3 hàng + 2 hàng) cho khỏi tràn. "Trình biên dịch" (JRE/JDK) giải tại chỗ ("chương trình dịch mã Java sang dạng máy chạy được").
- L02: bỏ `&&` khỏi hình hook (`mkdir bc`, `cd bc` hai lệnh riêng; `&&` vẫn giảng ở L04 bảng sym). Sửa tiêu đề cảnh sym "tám lệnh và ba dấu" → "bảy lệnh và bốn dấu" (đếm đúng bảng: 4+3 lệnh, 4 dấu).
- L04: `grep -q` (giải ở example#2), `$HOME` (ghi chú ở pitfalls#1: biến có sẵn chứa thư mục nhà, ví dụ `/c/Users/ban`).
- L05: `grep -o 'line [0-9]*'` (cờ `-o`, `[0-9]`, dấu `*` lặp), `sed 's/^/INFO dong /'` + `seq` + `^` = đầu dòng, dạng `s/cũ/mới/` (tách step example để khỏi tràn).
- L06: `sed 's/.*/&,…/'` (`.*`, `&`). L08: `sed 's/.*/&,&/'`, nhóm `( … ) > big.csv`, `seq` (tách step: dựng tệp / đếm + tra).
- L10: awk `NR > 1`, `if/else`, `+=`, `-=`, `END` (step mới sau bước 3 của cảnh formula, bảng 3 hàng); `<>` = khác (ghi chú ở quiz đáp án, và gợi ý lab).
Điểm P1 dự kiến: 2 ở 11/11 bài (≥ 90%). NOT_VERIFIED: người đọc độc lập chấm lại. P8 giữ 2 ở 11/11 (không đụng cảnh practice/lab).

## Lời đọc
- `cat`: không còn "cát" trong lời đọc FND (L04 nói "một tệp tên c a t, trùng tên với lệnh in nội dung tệp", "dòng chữ giả"); không cần mục lexicon mới (lexicon FND không đổi).
- 4 câu ≤ 3 từ nối vào câu liền kề: L02 "Ba dấu cuối." (nay "Bốn dấu cuối, trước hết là…"), L02 "Ta được năm." (nay "Ta được năm tệp, và sau khi xoá…"), L09 "Bước ba, chốt." ("Bước ba là chốt, và vì…"), L09 "Chốt ba lần." ("…, rồi chốt ba lần."). Quét lại cả 11 bài: 0 câu ≤ 3 từ. Mọi câu mới ≥ 8 từ, ≤ 38 từ (lint 0 WARN).
- Số từ lời đọc (≈ 2 300 là trần của BRIEF_AF2 mục 10; đã cắt câu dư để bù phần thêm): L00 2 843 (đã vượt trước đó: 2 806 ở vòng 3; phần thêm là printf + trình biên dịch + câu mời chép) · L01 2 049 · L02 2 082 · L03 1 971 · L04 2 192 · L05 2 304 · L06 1 947 · L07 2 184 · L08 2 318 · L09 2 106 · L10 2 311. L00, L08, L10 hơi trên 2 300 (≤ +1% với L08/L10); không cắt tiếp vì sẽ phá giảng P1 vừa thêm.
- Sửa kèm: `check_course_refs` (R4) báo "Hai bài cuối dạy…" ở L00 recap (cur=0 không phải bài cuối) → "Hai bài sau cùng dạy…" (lỗi có từ trước, nay 0).

## Cổng cuối khoá (sqlite3 3.46.0 mượn)
- `verify_fnd.py`: **80/80 PASS** (79 cũ + `PhienLapRoiQuiz`).
- `lv.py lint` 11 bài: **0 FAIL, 0 WARN** (lần đầu gặp: L00 focus recap, L05 câu > 38 từ, L10 focus + câu dài + thiếu lý do → đều sửa).
- `lv.py render` 11 bài: **0 vấn đề** (169/142/147/136/137/145/128/140/149/146/145 khung). Khung đã xem: L00 (khung kiem.sh, bảng printf), L04 (mã thoát), L05 (grep -o, sed), L06 (sinh a10k, quiz python), L08 (dựng big.csv), L09 (pitfalls), L10 (awk, pitfalls loi.db).
- `audit/review/lab_gate.py FND`: **11 PASS · 0 FAIL** (195 lab được bài tham chiếu).
- `screen_code.py gen-fnd` (204 khối, chưa khớp 0) rồi `check --course FND`: **PASS 295 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0** (lần đầu STALE 13/MISSING 5/ORPHAN 3 do khối mã đổi, đúng dự kiến; kết quả cuối chạy lại sau khi sửa L00 xem dòng cuối mục này).
- `tools/lv.py curriculum curriculum/fnd.yaml`: 11 bài, **0 lỗi** · `check_curricula_graph.py`: 46 lộ trình, 732 bài, 0 tham chiếu hỏng, 0 chu trình · `check_meta.py`: 0 vấn đề · `check_course_refs.py FND`: 0 vấn đề · `check_next_refs.py`: 550 lời hẹn, 0 lệch dãy học · `check_xref.py`: chạy xong, 14 lượt tham chiếu sang khoá khác ở 2 tệp (không đổi) · `tests/test_e52.py`: **0 FAIL** · `arith_scan.py FND`: 3 phép tính, **0 FAIL**.

## Không sửa / ghi chú
- Mục tiêu giáo án và `covers`: không đổi (`curriculum/fnd.yaml` không sửa).
- Sổ E52 `symbols.FND.yaml`: không thêm mục (các thuật ngữ thêm là cú pháp lệnh, không phải thuật ngữ then chốt của khoá).
- L00 khung `kiem.sh` giữ trên màn hình bằng `pause: 40` + câu mời dừng; không đổi thành mô tả khác. Giữ nguyên các lệnh sinh dữ liệu (không bỏ khỏi màn hình) vì chính chúng là mã người học gõ lại.
- Việc người điều phối: dựng lại 11 bài FND (TTS câu mới/đổi, ASR); chạy lại `verify_fnd`, `lab_gate`, `screen_code check` bằng sqlite3 chính thức.
