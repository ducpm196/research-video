# fix5_FND — sửa khoá FND vòng 5 theo `reports/R5_FND.md` — 2026-11-15

## Tiến độ
- Bài 1–3 (L00, L01, L02): XONG (L00 sửa nặng; L01, L02 chỉ khai `assumes`).
- Bài 4–6 (L03, L04, L05): XONG.
- Bài 7–9 (L06, L07, L08): XONG.
- Bài 10–11 (L09, L10): XONG. Cổng cuối khoá: xem mục "Cổng thật".

Nguồn sửa: `audit/fnd/src/l00..l10.py`, `audit/fnd/lib.py` → `gen.py` (không sửa YAML sinh ra bằng tay); sổ E52 `tools/registry/symbols.FND.yaml` (chỉ mục riêng FND); `curriculum/fnd.yaml` (chỉ dòng chú thích nguồn ở đầu tệp, không đổi mục tiêu/`covers`). Không chạy build/tts/asr/audit_all/git(ghi)/docker. Có dùng WebFetch tới nguồn chính thức (chỉ địa chỉ công khai, không gửi gì của dự án).

## Bản `sqlite3` đã dùng
`sqlite3.exe` 3.46.0 (2024-05-23, 64-bit) mượn từ thư mục Nsight Systems của máy, chép vào scratchpad `…\scratchpad\sqlbin\` và đặt vào PATH chỉ trong phiên chạy; KHÔNG chép vào kho. NOT_VERIFIED với CLI chính thức tải từ sqlite.org: người điều phối chạy lại `verify_fnd`, `lab_gate FND`, `screen_code check` bằng bản chính thức.

## 1. Lỗi kiến thức (xử lý như MUST) — 4/4 đã sửa
| Mục | Kiểm lại | Sửa |
|---|---|---|
| L05 "ă = a có dấu mũ" | Đúng: `python -c "print(hex(ord('ă')))"` = 0x103 (U+0103), dấu trăng; dấu mũ là của â. | Lời đọc hook, intuition, formula step 1, check: "chữ a có dấu trăng"; màn hình sym: "chữ ă, tức a có dấu trăng, là 259". Các chỗ "dấu mũ" còn lại ở L05 là dấu `^` (caret) của `sed 's/^/…/'` và của thông báo lỗi javac: đúng, giữ. Quét toàn kho (`rg` "a có (dấu )?mũ", "chữ ă", "dấu trăng"): chỉ FND L05 có lỗi này; JVA L00 ("dòng thứ ba có dấu mũ" = `^` của javac) và BNX L01 ("dấu mũ" = `^` regex) đúng, không đổi. Không có khoá nào dùng chung ví dụ "ă". |
| L03 sym "chín lệnh" | Đúng: bảng có 7 lệnh (head, tail, wc, grep, cut, sort, uniq) + 3 dấu (ống, `2>`, `/dev/null`). | Tiêu đề "Giải mã bảy lệnh, cờ và ba dấu". |
| L10 sym "năm mảnh" | Đúng: hai bảng 4 + 4 = 8 mục. | Tiêu đề "Giải mã tám mảnh mới của dự án". |
| L08 pitfalls step 0 (3 hàng, sau check có `4\|Dung\|0`) | Đúng (shim đã chạy: 4 hàng, tổng vẫn 2 000 000). | Tách step: khung lỗi + note "chạy trên cơ sở dữ liệu vừa dựng lại sạch từ `dung.sql` (ba hàng); nếu bạn đã chèn Dung ở phép kiểm trước và chạy liền sẽ thấy thêm `4\|Dung\|0` (NULL cũng bị đặt thành 0), tổng vẫn 2 000 000"; lời đọc nói tương ứng. Phiên `PhienQuenWhere` vẫn dựng lại từ `dung.sql` (verify PASS). |

## 2. P1 (3 bài) — thuật ngữ giảng tại chỗ; sổ E52 mới (chỉ `symbols.FND.yaml`)
Ba mục `term:` mới: `fnd_bash` (`git bash|\bbash\b`), `fnd_stderr` (`2>&1`), `fnd_as` (`\bAS\b`). `lib.lesson` tự thêm `assumes` cho bài sau (`fnd_bash` từ L01; `fnd_stderr` từ L05; `fnd_as` từ L09); `lv.py curriculum` kiểm assumes ⊂ bao đóng tiên quyết: 0 lỗi.
- L00 (`fnd_bash`, step đầu cảnh "chuanbi"): bảng 4 hàng: vỏ lệnh (shell) là chương trình nhận chữ gõ rồi bảo máy làm, gõ một dòng, nhấn Enter; bash là một loại vỏ lệnh; Git Bash là cửa sổ gõ lệnh trên Windows đi kèm Git for Windows, bên trong chạy bash; `.sh` là đuôi tệp lệnh, `bash kiem.sh` = nhờ bash chạy các lệnh trong tệp. Step sau: ví dụ chạy thật `echo xin chao` → `xin chao` (phiên mới `DemoEcho`, verify PASS). Lời đọc đánh vần "b a s h" (đúng tiền lệ "c a t", "e x e" của khoá; lexicon FND không đọc "bash" vì ASR 2/8).
- L05 (`fnd_stderr`): step mới trước phép ③: hai đường ra chữ (thường / báo lỗi), ống chỉ chuyển đường thường, `2>&1` gộp; ví dụ chạy thật `ls khong_co | wc -l` (in dòng lỗi rồi `0`) và `ls khong_co 2>&1 | wc -l` (`1`), phiên mới `PhienLuong`. L04 là bài đầu dùng `2>&1` (ở gợi ý lab): giới thiệu một câu ở hàng ④ của bảng ôn ("Mới: `2>&1` gộp thông báo lỗi vào chữ in thường, để ống nhận được cả lỗi", `introduces: [fnd_stderr]`); L05 `assumes` và giảng đầy đủ kèm ví dụ.
- L08 (`fnd_as`): step mới trước câu hỏi nhóm: `AS` đặt bí danh cho cột kết quả; ví dụ chạy thật `sqlite3 -header … 'SELECT SUM(so_tien) FROM giao_dich;'` → đầu cột `SUM(so_tien)`; có `AS tong` → `tong` (phiên mới `PhienAS`, sqlite3 3.46.0). Cờ `-header` nói một câu. L09/L10 `assumes: fnd_as` (L10 dùng `CREATE VIEW … AS`).
Điểm P1 dự kiến: 2 ở 11/11 (L00, L05, L08 được bù chỗ thiếu). NOT_VERIFIED: người đọc độc lập chấm lại.

## 3. L00: hướng dẫn cài từng bước (điểm yếu lớn nhất)
Cấu trúc mới: cảnh "chuanbi" (vỏ lệnh/bash/Git Bash → ví dụ `echo` → bốn công cụ + PATH) · cảnh mới "caidat" (Cài đặt từng bước: Git → mở Git Bash từ Start và `git --version` → JDK 21 → Python → sqlite3) · cảnh mới "kiemsh" (tạo `kiem.sh`, bảng giải từng phần, chạy). Mọi step ghi "(giao diện có thể khác nhẹ theo phiên bản)". Cảnh `caidat` dùng bảng/danh sách xen kẽ để qua cổng E39 (không quá 3 khung liền chỉ có chữ).
Điều xác minh được từ nguồn chính thức (truy cập 2026-11-15; ghi đủ trong `source:` của L00):
- Git for Windows: `git-scm.com/install/windows` (tải bản x64 "Git-x.y.z-64-bit.exe"); tệp cài đặt `install.iss` của git-for-windows/build-extra (GitHub): thành phần "Windows Explorer integration" gồm "Open Git Bash here"; màn hình "Adjusting your PATH environment" có ba mục ("Use Git from Git Bash only" thận trọng nhất; "Git from the command line and also from 3rd-party software" ghi (Recommended) và là mặc định; "Use Git and optional Unix tools from the Command Prompt" cảnh báo ghi đè `find`, `sort` của Windows); terminal mặc định MinTTY; lối tắt Start menu thư mục "Git" → "Git Bash". Bài nói: giữ mặc định, mục giữa; mục đầu cũng đủ cho khoá này (vì chỉ dùng Git trong Git Bash).
- JDK: `adoptium.net/installation/windows` (gói `.msi` chỉ cho Windows x64; màn hình Custom Setup: "Add to PATH" chọn sẵn, "Set JAVA_HOME" không chọn sẵn); API `api.adoptium.net` xác nhận gói `OpenJDK21U-jdk_x64_windows_hotspot_21.0.x.msi` (loại JDK, không phải JRE).
- Python: `docs.python.org/3.13/using/windows.html` ("Install Now" / "Customize installation", "nếu chọn, thư mục cài sẽ được thêm vào PATH"; kiểm bằng `python --version`/`py`); `python.org/downloads/windows`: có "Python install manager" (mới) và vẫn có "Windows installer (64-bit)" cho bản 3.13; bài dặn: nếu trang chỉ đưa install manager thì cài theo trang hướng dẫn, đích vẫn là `python --version` trong Git Bash in từ 3.11.
- NOT_VERIFIED (không có ảnh chụp/không chạy được trình cài ở máy kiểm): chữ chính xác của ô tích "Add python.exe to PATH" ở trình cài 3.13 (docs không nêu tên ô, chỉ nêu hành vi); mục "Show more options" của Windows 11 (giữ từ vòng trước); hành vi `python --version` với install manager trong Git Bash. Bài ghi "giao diện có thể khác nhẹ theo phiên bản". Tai người chưa nghe "b a s h", "x sáu mươi bốn", "m s i".
Số từ lời đọc L00: **3 147** (trước 2 847; trần BRIEF_AF2 là 2 300). Không cắt xuống được mà không mất nội dung: phần cài đặt mới ≈ +500 từ (đã rút hết cỡ, bù bằng cắt 70 từ ở cảnh vật lý, bỏ step kiểm đơn vị thừa, gộp bảng giải `kiem.sh` còn 3 step). ĐỀ XUẤT (không tự làm vì đánh số lại): tách L00 thành hai bài "Máy chạy chương trình thế nào và cách học" (~1 600 từ) và "Cài đặt và kiểm máy" (~1 500 từ); nếu bắt buộc đặt bài mới ở cuối khoá thì không hợp lý vì đây là bài đầu tiên; người điều phối quyết định.

## 4. SHOULD — 9/9 đã sửa
| Bài | Việc | Sửa |
|---|---|---|
| L00 hoc step 1 | Roediger & Karpicke NOT_VERIFIED, thiếu điều kiện | Đối chiếu qua API Crossref (doi 10.1111/j.1467-9280.2006.01693.x, Psychological Science 17(3) 249–255; tóm tắt: sau 5 phút học lại nhỉnh hơn, sau 2 ngày và 1 tuần tự kiểm tra giữ được nhiều hơn). Màn hình và lời đọc nêu đúng điều kiện (sau 5 phút / 2 ngày / 1 tuần). `source` ghi CITED (chỉ đọc tóm tắt, chưa mở bài đầy đủ); `curriculum/fnd.yaml` dòng chú thích đồng bộ. |
| L06 pitfalls step 1 | `co: no` → false chỉ đúng YAML 1.1/PyYAML | Bảng đề "bộ đọc theo YAML 1.1 (như PyYAML) hiểu là"; ô nêu "bản YAML 1.2 coi `no` là chữ"; lời đọc nói rõ bản một chấm một; `source` thêm "bản 1.1 coi yes/no/on/off là đúng/sai, bản 1.2 chỉ true/false". |
| L04 quiz step 1 | `hash -r` không bắt buộc | Ghi chú + lời đọc: không bắt buộc khi chỉ đổi PATH (gán lại đã tự xoá bảng nhớ), không hại, có khi cần (lệnh mới đặt vào thư mục đã có trong danh sách). |
| L07 hook | `$U` dùng trước khi định nghĩa | Tiêu đề khung: "`$U` là biến giữ địa chỉ của nó"; lời đọc: đô la U là biến giữ địa chỉ máy chủ, đặt ở cảnh sau (lần đầu thêm vào đoạn văn bị TRÀN bảng ở render → chuyển lên tiêu đề khung). |
| L10 de.md | "thiếu sqlite3 thì cham.sh báo lỗi" sai | Kiểm lại theo báo cáo: lời giải tự viết không kiểm `command -v` thì chỉ ra KHÁC kèm `LECH: …` (stderr bị nuốt). de.md nay nói đúng, dặn chạy `sqlite3 --version` trước; lời giải mẫu vẫn in `thieu sqlite3, cai theo bai L00`. Không sửa `labs/cham.sh` (dùng chung mọi khoá; đề xuất người điều phối: in `_err` khi KHÁC). |
| L07 lab | chép ~45 dòng Python | Màn hình (đề practice, chữ + lời đọc) và de.md: "khối đầu tiên khoảng 55 dòng, trong đó 45 dòng Python: chép đúng từng ký tự, chưa cần hiểu". |
| L05 lab | nhắc `> /dev/null` | Đề trên màn hình: "**bắt buộc** thêm `> /dev/null` sau mỗi lệnh" (de.md vốn đã có "Bắt buộc có `> /dev/null`"). |
| L03/L10 nhãn, L05 "ă", L08 step | (mục 1) | đã nêu ở mục 1. |

## Lời đọc
Mọi câu mới 8–38 từ, không chữ Latin/Anh trong lời đọc (lint 0 WARN). Số từ: L00 3 147 · L01 2 049 · L02 2 082 · L03 1 971 · L04 2 238 · L05 2 320 · L06 1 972 · L07 2 215 · L08 2 341 (đã cắt 70 từ để bù phần thêm; trước 2 318) · L09 2 106 · L10 2 311. L04 (+46), L05 (+16), L07 (+31), L08 (+27) hơi trên mức vòng trước; L00 (+300) giải trình ở mục 3.

## Bài nào đổi → cần dựng lại (CHÍNH XÁC)
- **Đổi lời đọc + hình (dựng lại đủ: TTS câu mới/đổi, ASR)**: L00, L04, L05, L06, L07, L08.
- **Chỉ đổi hình (nhãn tiêu đề cảnh), lời đọc không đổi**: L03, L10 (cũng đổi `assumes`).
- **Chỉ đổi `assumes` (siêu dữ liệu), nội dung không đổi**: L01, L02, L09 — vẫn đổi `spec_sha256` nên phải dựng lại một lần để build_report khớp (TTS dùng bộ nhớ đệm, không có câu mới).
- Lab đổi: L00, L07, L10 (`de.md`); lời giải/`mong_doi` không đổi.
- Việc người điều phối: chạy lại `verify_fnd`, `lab_gate FND`, `screen_code check` bằng sqlite3 chính thức; xem lại bằng tai các câu mới ("b a s h", "x sáu mươi bốn", "m s i").

## Cổng thật (sqlite3 3.46.0 mượn)
- `verify_fnd.py`: **83/83 PASS** (80 cũ + `DemoEcho` L00, `PhienLuong` L05, `PhienAS` L08).
- `lv.py lint` 11 bài: **0 FAIL, 0 WARN** (lần đầu gặp: L00 hai câu > 38 từ, focus lệch, "Start"/"Windows" trong lời đọc, 6 khung liền chỉ chữ; L03–L10 thiếu `assumes`; L04 focus; L05 thiếu lý do; L07 hook focus → đều sửa).
- `lv.py render`: L00 187 khung, L03 136, L04 139, L05 147, L06 128, L07 141, L08 151, L10 145: **0 vấn đề** (lần đầu L07 hook và L08 pitfalls TRÀN → tách step/đổi chỗ, render lại sạch). L01, L02, L09 không đổi hình, không render lại. Khung đã xem: L00 (bảng vỏ lệnh, bảng cài Git, bảng cài Python), L04 (bảng ôn có `2>&1`), L05 (hook ă, step `2>&1`).
- `audit/review/lab_gate.py FND`: **11 PASS · 0 FAIL** (196 lab được bài tham chiếu).
- `tools/lv.py curriculum curriculum/fnd.yaml`: 11 bài, **0 lỗi** · `tests/test_e52.py`: **0 FAIL** · `check_course_refs.py FND`: 0 vấn đề · `check_next_refs.py`: 550 lời hẹn, 0 lệch dãy học · `arith_scan.py FND`: 3 phép tính, 0 FAIL · `check_curricula_graph.py`: dòng "VER dẫn tới mã không PASS: WEB:L04" là khoá WEB có từ trước, không thuộc FND.
- `screen_code.py`: lần đầu **STALE 7 · MISSING 7 · ORPHAN 4** (đúng dự kiến, khối mã đổi) → `gen-fnd` (207 khối, chưa khớp 0; sổ cũ lưu ở scratchpad `FND_screen_code_before5.yaml`) → kết quả `check --course FND` sau gen: xem dòng cuối mục này.
**Sau gen: `check --course FND` = 207 khối, PASS 301 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0.** Cũng chạy: `check_meta.py` 0 vấn đề; `check_xref.py` 14 lượt tham chiếu sang khoá khác ở 2 tệp (BNX, không đổi).

## Không sửa / ghi chú
- Mục tiêu giáo án và `covers` không đổi (`curriculum/fnd.yaml` chỉ sửa dòng chú thích nguồn).
- `labs/cham.sh`: không sửa (dùng chung); đề xuất ở mục SHOULD.
- Lệnh cài đặt bằng winget/Chocolatey (có trên git-scm.com): không dạy, vì người mất gốc dễ kẹt hơn khi phải cài thêm trình quản lý gói; nguồn ghi rõ gói do cộng đồng, không do dự án Git for Windows bảo trì.
- Các câu "nhanh/tức thì" (L01, L02, L05) vẫn là lời, chưa đo (đã có ở báo cáo R5, không phải MUST/SHOULD).
