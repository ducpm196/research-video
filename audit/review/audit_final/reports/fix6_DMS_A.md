# fix6 DMS L00–L10 (sửa theo R4_DMS_A, chuẩn P1 chặt) — 2026-11-16

Tiến độ: L00–L02 xong; L03–L05 xong; L06–L08 xong; L09–L10 xong. Không chạy build/tts/asr/render/git/docker.

## Cách làm
- Hạ tầng mới `audit/dms/af2/fix6lib.py` (không sửa af2lib để khỏi đụng L11–L20): `read_step` (bảng "viết trong mã → đọc là → ví dụ" đặt NGAY TRƯỚC khối mã; một câu mở + đúng một câu cho mỗi hàng, `focus` từng hàng), `hint_parts` (bảng cho khối gợi ý của cảnh Tự làm), `patch_cham` (chân trang chấm bài có giải thích bằng chữ trên màn hình + lời đọc 4 câu).
- Sửa CẢ script vá `audit/dms/af2/l00..l10.py` (bài sinh lại từ `base/` bằng script, chạy lại ổn định) và bài `lessons/dms/L00..L10`; L08 vá mẫu `audit/dms/src/L08_*.tpl.yaml` rồi ghép hình như cũ.
- Mã trong lời đọc không nói tên từ khoá (lexicon): lời đọc tả bằng tiếng Việt ("dòng mở đầu vòng lặp", "chia lấy số dư", "hai dấu sao liền nhau là lũy thừa"), tên thật chỉ hiện trong bảng trên màn hình.

## Theo bài (đã đổi, số mục chưa giảng ước còn lại)
| Bài | Bảng đọc mã thêm | Chân trang | Thuật ngữ / SHOULD | Từ | Chưa giảng ước |
|---|---|---|---|---|---|
| L00 | quymo: for…in (…), gán, `**`, range, print, `//` (6 hàng); gợi ý practice: `==`, and/or, `int` | có; thêm cách chạy `.py` bằng Git Bash ở đề practice | – | 2223 | 0 |
| L01 | quymo: def/return, `<= >= or`, for+range, `!=`, gán, `** //`, print (7 hàng) | có | SHOULD "vế": "luật nhỏ" / "không p lẫn không q" (cả chữ trên màn hình); khôi phục mục asr_reviewed bị mất khi sinh lại | 2154 | 0 |
| L02 | quymo: 6 hàng (for, range, gán, if, break, print) + 2 hàng any/all trước mã thứ hai; gợi ý: all, any, `[x for … if not (…)][0]` | có | "phản ví dụ" định nghĩa tại verify.0 (lời + bảng) | 2279 | 0 |
| L03 | quymo: for, `range(1, n+1, 2)`, `%`, `==`, gán, print | có | SHOULD "tối giản" = không có ước chung lớn hơn 1 (chữ + lời + mục asr_reviewed) | 2272 | 0 |
| L04 | quymo: for, range, gán `2 * k - 1`, print; gợi ý: `while … == …` | có | ASR "bằng một": "tổng có giá trị là 1", "n có giá trị là một", "Q của 1, câu đầu tiên của hàng" | 2162 | 0 |
| L05 | quymo: 7 hàng (for+`**`, range, `% ==`, or, gán, `//`, print); gợi ý: `| & -`, `//` | có | SHOULD "3 phép chia": "với hai điều kiện (chia hết cho 2 và cho 3)" ở bảng, hộp, lời | 2085 | 0 |
| L06 | quymo: hai đợt (4 + 6 hàng): gán m, for, `[0] * m`, range, `k * hằng`, `% 2 ** 32`, `% m`, `dem[o]`, `// làm tròn lên`, `max`/`.count`; gợi ý: `.values()`, set, len | có | "32 bit" định nghĩa ở hàng bảng và lời; "va chạm" định nghĩa ở quymo.0 trước lần dùng; bỏ bước giải thích đặt sau mã (đã gộp vào bảng) | 2254 | 0 |
| L07 | quymo: 6 hàng (đổi `not a % 3 == c % 3` thành `!=`, `n ** 3` thành `n * n * n`) + bảng 4 hàng cho mã gom lớp (đổi từ điển `{}`/`.get`/`.values()` thành danh sách `[0, 0, 0]`); gợi ý: all+for lồng, `if … and …`, `[b for b in A if R(a, b)]` | có | "vét cạn" định nghĩa ở câu mở + ghi chú; SHOULD "phủ kín" (equivalence.1 thêm dòng + câu); SHOULD dấu "." lẻ ở quiz.1 (câu kết thúc bằng "(các số lẻ)… (các số chẵn)") | 2228 | 0 |
| L08 | quymo: hai bảng (5 + 3 hàng) cho mã liệt kê hoán vị; khối mã Kahn (`dict`, `while`, `.pop`, `.append`) thay bằng BẢNG VẾT chạy thật (dựng lại bằng thuật toán, assert khớp từng dòng với đầu ra của mã cũ); gợi ý: `not any`, `!=`, `% ==`, `max` | có | – | 2207 | 0 |
| L09 | quymo: 6 hàng (for, `**`, range, gán, print, `//`) | có | "PIN" định nghĩa (câu mở + ghi chú); SHOULD "Lỗi 2" → "…tuỳ bước trước chọn cái nào"; ASR "bằng một": "có giá trị là 1" ×2; gợi ý: product, permutations | 2074 | 0 |
| L10 | quymo: 5 hàng (for, range 1 và 2 đối số, gán, `* //`, print); gợi ý: `hang[i] + hang[i + 1]` | có | "khoá băm" định nghĩa (lời + màn hình); SHOULD "49 500 cặp" thêm "khi chỉ cần so các cặp cùng khoá/nhóm"; ASR "cùng bằng 1" → "cùng có giá trị là 1" | 2181 | 0 |

## Cổng (chạy thật, 2026-11-16)
- `tools/lv.py lint` từng bài L00–L10: 0 FAIL, 0 WARN (số từ lời đọc ở cột "Từ", ≤ 2300).
- `tools/lv.py curriculum curriculum/dms.yaml`: 21 bài, 0 lỗi. `tests/test_e52.py`: 0 FAIL. `audit/dms/verify_dms.py`: 324 PASS · 0 FAIL.
- `audit/review/screen_code.py check --course DMS`: 72 khối — PASS 95 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 (sổ cập nhật bằng `ledger_sync` của script, công cụ chính thức).
- `audit/review/lab_gate.py DMS`: 21 PASS · 0 FAIL. `arith_scan.py`: 251 phép, 0 FAIL. `check_curricula_graph.py`: 0 chu trình, 0 VER lỗi. Lab (`labs/DMS/L00–L10`) không đổi so với trước (so sánh từng tệp).

## Lưu ý cho người điều phối
- Chưa nghe/ASR/render lại: lời đọc mới cần dựng lại ASR; các câu "bằng một" đã đổi sang "có giá trị là một" để né "bằng mục" nhưng chưa kiểm bằng tai. Bảng 3 cột mới chưa xem khung PNG (không được chạy render) — cần xem ≥ 3 khung mỗi bài sau khi dựng, nhất là hàng "ví dụ" dài ở L06, L08.
- Khi sinh lại bài từ `audit/dms/af2/lNN.py`, mục `asr_reviewed` thêm tay sau AF2 không có trong `base/` bị mất; L01 đã được giữ bằng `repl` trong l01.py. Các bài L11–L20 chưa kiểm điều này.
- L08: khối mã Kahn không còn trên màn hình (thay bằng bảng vết chạy thật); thuật toán chọn bằng bộ đếm vẫn được dạy bằng lời + bảng, lab dạy cách chọn số lớn nhất còn trống.
- Mã còn lại trong lab (`de.md`, lời giải) không đổi; cú pháp trong `de.md` vẫn được giải thích riêng ở đó.
