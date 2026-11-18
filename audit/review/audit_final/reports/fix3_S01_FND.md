# fix3_S01_FND — sửa khoá FND vòng 3 theo `reports/S01c_FND.md` — 2026-11-14

Nguồn sửa: `audit/fnd/src/l00..l10.py`, `audit/fnd/shim/sqlite3_shim.py`, `labs/check_env.sh`, `labs/ENV.md` → `gen.py` (không sửa YAML sinh ra bằng tay). Không chạy build/tts/asr/audit_all/git (một lệnh `git diff --stat` chỉ đọc để đếm dòng, không ghi)/docker; không tải gì từ mạng. Cả 11 bài đổi lời đọc hoặc hình nên mọi bài FND đều STALE: người điều phối dựng lại cả khoá một lần.

## Bản `sqlite3` đã dùng để kiểm
`sqlite3.exe` 3.46.0 (2024-05-23, 64-bit) mượn từ thư mục Nsight Systems của máy, đã có sẵn trong scratchpad (`…\scratchpad\sqlbin\`), đặt vào PATH chỉ trong phiên chạy; KHÔNG chép vào kho. Mọi số "thật" dưới đây chạy bằng bản này. Người điều phối chạy lại `verify_fnd.py`, `lab_gate.py FND`, `screen_code.py check --course FND` bằng bản chính thức.

## MUST (1/1 đã sửa)
| Bài | Kiểm lại | Sửa |
|---|---|---|
| L00 `kiem.sh` bị lối tắt Microsoft Store đánh lừa | Đúng như báo cáo: `command -v python` chỉ dò tên trong PATH. Dựng lại ca bằng một `python` giả in "Python was not found; run without arguments to install from the Microsoft Store" rồi thoát mã 49: cách cũ in `✔ python`. (Ngay trong phiên này, `python3` của Git Bash trên máy soạn cũng là lối tắt Store: gõ vào là ra đúng dòng đó.) | `kiem.sh` mới có hàm `dat TÊN MỨC_THẤP_NHẤT`: chạy THẬT `TÊN --version`, lọc số phiên bản đầu tiên, so bằng `sort -V` với mức thấp nhất; lối tắt Store không in số → THIEU. Mức: bash 4.0, git 2.28, javac 21, java 21, python 3.11, sqlite3 3.32 (khớp BRIEF: Java 21, Git ≥ 2.28, sqlite ≥ 3.32). Vẫn đúng sáu dòng `✔ ten` nên `mong_doi.txt` không đổi. Kiểm bằng máy (kịch bản giả): có đủ → 6 dấu tích; Python Store-stub → `THIEU python`; Git 2.25 → `THIEU git`; JDK 8 (không có `--version`) → `THIEU javac`; thiếu sqlite3 → `THIEU sqlite3`; không có gì → 5 THIEU + bash. `verify_fnd` thêm phiên `KiemStub` (stub Python kiểu Store + Git 2.25.1 giả: phải ra `THIEU git` và `THIEU python`). Cảnh `chuanbi` giảng từng phần (hàm, `$1 $2`, biến, `--version`, `2>/dev/null`, `|`, `grep -oE`, `head -1`, `sort -V`, điều kiện, một lần gọi) trong hai bảng; cảnh `practice` ("Nếu kẹt") nói đúng: THIEU python = chưa cài, chưa "Add to PATH", bản < 3.11, hoặc chỉ có lối tắt cửa hàng ứng dụng (gõ `python --version` báo "Python was not found"). `de.md`, `loi_giai.sh` L00 sinh lại từ nguồn (nêu mức thấp nhất); `labs/check_env.sh` chạy thật `--version` rồi so mức thấp nhất, báo lý do ("phiên bản X nhỏ hơn mức tối thiểu Y" / "không chạy được (chưa cài, hoặc chỉ là lối tắt mở cửa hàng ứng dụng)") — đã chạy thử ba kịch bản; `labs/ENV.md` ghi các mức thấp nhất; shim `sqlite3_shim.py` biết `--version` (máy kiểm chưa có sqlite3 vẫn chạy được `kiem.sh`). Đầu ra trên màn hình (`bash kiem.sh` → sáu dòng `✔`) khớp (verify 79/79; `cham.sh FND L00 loi_giai.sh` → ĐÚNG). |

## SHOULD (7/7 đã sửa)
| Bài | Sửa |
|---|---|
| L00 không kiểm phiên bản | Gộp trong MUST (kiem.sh kiểm mức thấp nhất; `check_env.sh` in số phiên bản). |
| L04 `chmod +x` trên Git Bash/NTFS | Cảnh `formula` bước 0 (chữ + lời đọc): "trên máy chủ máy chỉ chạy như một lệnh những tệp có quyền chạy; cửa sổ lệnh trên máy của bạn vẫn chạy được tệp chưa bật, nhưng hãy cứ gõ để giữ thói quen đúng". |
| L04 lab đề thiếu `> /dev/null` | Cảnh `practice` (chữ + lời đọc) và `de.md`: phải giấu cả danh sách do `ls .` in ra (`> /dev/null`) lẫn thông báo lỗi (`2> /dev/null`). Kiểm: tự viết `kiem_tra.sh` theo đề mới → `cham.sh FND L04` ĐÚNG; bản theo đề cũ (không giấu `ls .`) vẫn KHÁC (`_err`, `_out`) như báo cáo, nay đề đã nói rõ. |
| L04 check #19 nhãn "đang có" | Tiêu đề khung: "Đối chiếu danh sách ban đầu (hai thư mục, trước khi thêm)" (khớp 2 dòng `/usr/bin` `/bin` và lời đọc "ban đầu"). |
| L02 `*` và tệp ẩn | Hook, bảng ký hiệu (chữ + lời đọc), formula bước 2 (tiêu đề, chữ, lời đọc): `*` khớp mọi chuỗi trừ tên bắt đầu bằng dấu chấm (tệp ẩn), nên tệp ẩn không bị `rm *` chạm tới. |
| L06 scale "một nghìn lần" | Lời đọc: "Nhân lên một trăm lần rồi mười nghìn lần cũng thế…" (khớp hàng ×100 và ×10 000 của bảng). |
| L06 quiz CSV/JSON | Đề nói rõ bản ghi có danh sách thẻ lồng, dài ngắn khác nhau; quyết định đổi thành JSON mỗi dòng một bản ghi (CSV không lồng được, muốn dùng phải làm phẳng trước: mỗi thẻ một dòng, lặp tên chủ thẻ; giá phải trả ≈ 2,3× dung lượng); CSV chỉ hợp bản ghi phẳng đồng dạng (chữ + lời đọc, nhất quán với "CSV không lồng nhau được" của bài). |
| L08 INSERT 'Dung' hai lần | Nguồn đúng: mỗi phiên dựng lại cơ sở dữ liệu nên chạy được; người học gõ nối tiếp trên một cơ sở dữ liệu sẽ gặp lỗi. Cảnh `check` và `pitfalls` nói rõ: mã 4 là khoá chính, chèn lại báo `UNIQUE constraint failed`, muốn làm lại thì dựng lại cơ sở dữ liệu; cảnh `pitfalls` chỉ còn hiện hai lệnh COUNT (không lặp lệnh INSERT). `verify_fnd`: thêm bước chạy thật chèn lần hai → `UNIQUE constraint failed: tai_khoan.ma`. |
| L10 lab thiếu sqlite3 | Kiểm lại: `PATH=/usr/bin:/bin bash loi_giai.sh` → `thieu sqlite3, cai theo bai L00`, mã thoát 1; có sqlite3 → ĐÚNG. Không đổi. |

## P1 (thuật ngữ tại chỗ) — mọi mục "Cần biết trước" của 11 bài
Mỗi mục giảng bằng một câu lời thường (kèm ví dụ nhỏ) ở LẦN ĐẦU xuất hiện trong bài, cả trên màn hình lẫn lời đọc (đã quét vị trí lần đầu của từng thuật ngữ trong YAML).
- L00: Git (ghi lại các phiên bản của dự án), Java và Python (ngôn ngữ lập trình = cách viết chỉ dẫn cho máy), SQL (ngôn ngữ hỏi dữ liệu trong bảng), "biến" (cái tên mang một giá trị, ví dụ `v=$(…)`, `$v`) — cảnh `chuanbi`.
- L01: hệ tệp (cách hệ điều hành đặt tên và sắp xếp tệp; `HOC` khác `hoc`), máy chủ (máy chạy sẵn để nhiều người hay chương trình hỏi qua mạng), Linux — cảnh `pitfalls` lỗi 3.
- L02: không có mục; thêm "trừ tệp ẩn".
- L03: MB/GB (1 MB = một triệu byte, 1 GB = một nghìn MB; 1 000 000 dòng × 100 byte = 100 MB), "ngoại suy" (từ số đo nhỏ suy ra số lớn bằng phép nhân; chỉ đúng khi tuyến tính, cảnh báo xếp/tìm không tăng đều), "sổ cái" (tệp ghi mọi giao dịch, mỗi dòng một giao dịch) — step mới ở cảnh `scale`.
- L04: xác suất (con số 0 % đến 100 %; tung đồng xu ngửa = 50 %), độc lập — cảnh `scale`.
- L05: lũy thừa (2 nhân với chính nó vài lần; 2³ = 8), Linux/macOS (hệ điều hành hay chạy trên máy chủ) — cảnh `formula`, `sym`.
- L06: cú pháp (luật viết đúng, như chính tả), bộ kiểm, bộ đọc (chương trình đổi chữ trong tệp thành dữ liệu), YAML `[a, b]` (danh sách viết gọn trên một dòng, giống mảng JSON; cả trong bảng ký hiệu YAML và `de.md`).
- L07: HTTP/giao thức (bộ quy ước hai máy nói chuyện: yêu cầu đúng khuôn, phản hồi đúng khuôn; `curl` gửi một yêu cầu và in ra phản hồi), tiêu đề (thông tin phụ dạng `Tên: giá trị`, ví dụ `Content-Length: 7`), cục bộ (ngay trên máy bạn) — cảnh `hook`, `sym`.
- L08: mệnh đề (phần câu lệnh chọn hàng nào) — cảnh `hook`.
- L09: tác dụng phụ của `core.autocrlf false --global` (áp cho mọi kho; cách hoàn lại bằng `--unset`), tách thành step riêng.
- L10: MB/GB và ngoại suy (step mới ở cảnh `scale`, như L03), tệp nhị phân (tệp chứa byte để máy đọc, không phải chữ cho người đọc), `%` trong `sinh.awk` (phép chia lấy dư, `7 % 3` ra 1).
Điểm P1 dự kiến: 2 ở 11/11 bài (≥ 90 %); P8 giữ 2 ở 11/11. NOT_VERIFIED: điểm do người đọc độc lập chấm lại.

## Lời đọc (≤ 2 300 từ)
Số từ lời đọc sau sửa (trước → sau): L00 2676 → 2806 · L01 1969 → 2013 · L02 2047 → 2077 · L03 1860 → 1971 · L04 2014 → 2110 · L05 2251 → 2276 · L06 1784 → 1875 · L07 2108 → 2185 · L08 2285 → 2292 · L09 2047 → 2074 · L10 2267 → 2297. Mười bài ≤ 2 300. **L00 vượt (2 806)**: đã vượt từ trước (2 676 ở vòng 2, trần cũ cũng không giữ được vì ba cảnh nền: cơ chế máy, cách học, cài đặt); phần thêm lần này (+130) là chính điều MUST đòi (giảng tệp kiểm chạy thật phiên bản + ca lối tắt Store) và P1; đã cắt ba câu dư ở L00 và các câu dư ở L08/L10; cắt thêm sẽ phá nội dung mục tiêu 5/6 (`covers` giữ nguyên). Không có câu `say` mới/đổi nào < 8 hay > 38 từ (lint: E-độ dài câu 0 WARN).

## Mục tiêu giáo án
Không đổi (mục tiêu của 11 bài và `covers` giữ nguyên; `curriculum/fnd.yaml` không cần sửa).

## Cổng (số thật, sqlite3 3.46.0)
- `verify_fnd.py`: **79/79 PASS** (78 + `KiemStub`; gồm bước UNIQUE của L08).
- `lv.py lint` cả 11 bài: **0 FAIL, 0 WARN** (lần đầu gặp: L00 E31 focus recap, L04/L03/L10/L06 câu dài hoặc thiếu lý do, từ nước ngoài "Linux/Windows/Python/Git" trong lời đọc → đều sửa). `lv.py render`: **0 vấn đề** ở cả 11 bài (L09 formula bước 0 tràn sau khi thêm đoạn `autocrlf` → tách thành step riêng + `clear`; L00 bảng `kiem.sh` có `$1 $2` bị KaTeX hiểu là công thức → dùng `code()`; đã xem lại khung).
- `audit/review/lab_gate.py FND`: **11 PASS · 0 FAIL** (120 lab được bài tham chiếu).
- `screen_code.py gen-fnd` (202 khối, chưa khớp 0; sổ cũ lưu ở scratchpad `FND_screen_code_before3.yaml`) + `check --course FND`: **PASS 292 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0** (lần chạy đầu có 2 FAIL/6 STALE/3 MISSING/2 ORPHAN do khối mã đổi và do tôi đặt sai PATH sqlite3; sinh lại sổ bằng `gen-fnd` rồi chạy lại sạch).
- `tools/lv.py curriculum curriculum/fnd.yaml`: 11 bài, 0 lỗi · `check_curricula_graph.py`: 46 lộ trình, 731 bài, 0 tham chiếu hỏng, 0 chu trình · `tests/test_e52.py`: 0 FAIL.
- Khung PNG đã xem: L00 (cảnh `chuanbi`: sơ đồ + note, khung tệp `kiem.sh`, hai bảng giải mã), L03 (đơn vị + ngoại suy), L04 (xác suất), L06 (bộ đọc, quyết định), L07 (hook HTTP), L01 (pitfalls 3), L09 (autocrlf), L10 (đơn vị, `sinh.awk`). Không chữ đè/tràn.

## Không sửa / ghi chú
- `labs/cham.sh` (dùng chung) vẫn có nhánh dự phòng `sqlrun.py` cho `.sql`: không đụng.
- Báo cáo ghi "Chưa xem khung cảnh practice": không phải lỗi, không sửa.
- `check_next_refs.py` / `check_course_refs.py` (không đối số): không chạy vì lý do đã ghi ở vòng 1 (PYT chưa vào STAGES); FND không có lời hẹn "Bài sau (bài N)".
- Việc người điều phối: dựng lại 11 bài FND (TTS câu mới/đổi, ASR); chạy lại `verify_fnd`, `lab_gate`, `screen_code check` bằng sqlite3 chính thức; thử `kiem.sh` trên một máy Windows chưa cài Python để xác nhận lối tắt Store thật cho THIEU (máy này chỉ kiểm bằng `python` giả mô phỏng đúng thông báo).
