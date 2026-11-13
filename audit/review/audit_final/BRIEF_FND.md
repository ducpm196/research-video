# BRIEF_FND — soạn khoá FND "Nền thực hành" (11 bài, L00–L10) — 2026-11-13

Đọc trước: `audit/review/audit_final/BRIEF_AF2.md` (chuẩn bài AF2, BẮT BUỘC), `audit/review/audit_final/new_courses.md` (bảng 11 bài + lab từng bài), `labs/ENV.md`, `audit/jva/BRIEF.md` + `audit/jva/lib.py` + `audit/jva/gen.py` + `audit/jva/src/l00.py`, `l04.py` (mẫu cấu trúc 10 cảnh + cảnh practice), `.claude/skills/lecture-video/SKILL.md`.

Người học: **chưa từng mở dòng lệnh, chưa viết dòng mã nào**. FND là khoá ĐẦU TIÊN của toàn bộ lộ trình (Chặng 0, đứng trước JVA); sau FND người học sẽ học Java, rồi backend ngân hàng, rồi toán/thuật toán/AI. Vì vậy mọi thứ FND dạy phải là thứ các khoá sau DÙNG mà KHÔNG giảng lại: Git Bash và đường dẫn, tệp/thư mục, ống và chuyển hướng, `PATH`, mã thoát, JSON/YAML/CSV, HTTP + `curl`, SQL cơ bản, Git tối thiểu.

## Việc phải làm
1. `tools/lv.py new-course FND --title "Nền thực hành: dòng lệnh, tệp, dữ liệu, HTTP, SQL, Git"` (xem `references/new-domain.md`); lộ trình `curriculum/fnd.yaml` (mỗi bài: id, title, spec, requires theo thứ tự L00→L10, objectives đo được, example có số, fix). Đừng sửa `pack.py`/`tracks.yaml`/`STAGES` (người điều phối làm).
2. Bộ sinh `audit/fnd/` theo mẫu `audit/jva/`: `lib.py` (sao từ jva/lib.py: đổi COURSE="FND", SERIES; thay `prog(...)` bằng `cmd(name, script, out, files=None)` — một đoạn script bash **chạy THẬT bằng Git Bash trong thư mục tạm sạch**, đầu ra ghi vào `out`), `gen.py`, `src/l00.py … l10.py`, `verify_fnd.py` (chạy mọi `cmd` đã khai, so từng dòng; bài có SQL chạy qua sqlite/`labs/sqlrun.py`; bài HTTP dùng máy chủ cục bộ). Đầu ra có phần không ổn định (ngày giờ, mã băm, thời gian, đường dẫn tuyệt đối) thì **không hiện trên màn hình**: dùng `--format`, cố định ngày bằng biến môi trường `GIT_AUTHOR_DATE/GIT_COMMITTER_DATE`, hoặc cắt bằng `cut/sed` trong script.
3. Mỗi bài theo mẫu 10 cảnh + cảnh `practice` (Tự làm) + `af2: true` + `covers` (BRIEF_AF2). Lab của bài theo bảng trong `new_courses.md`; với lab chạy script `.sh` thì `loi_giai.sh` là script tự đủ, `mong_doi.txt` là đầu ra thật. Lời giải lab dùng thư mục tạm `$(mktemp -d)`; không ghi ngoài.
4. **Mọi lệnh người học thấy phải chạy được trên Windows 11 + Git Bash** (không dùng `ls --color`, `xdg-open`, `apt`, `sudo`). Nói rõ chỗ Windows khác: dấu `\` của đường dẫn trong Windows Explorer ↔ `/` trong Git Bash; `/c/Users/...` là ổ C.
5. **L00 đặc biệt**: (a) cái máy chạy chương trình thế nào (CPU–bộ nhớ–đĩa–hệ điều hành, hình cơ chế); (b) cách học cả khoá học: xem một bài → dừng làm cảnh Tự làm → chấm bằng `labs/cham.sh` → tick ở trang HOC_TAP; ôn ngắt quãng; vì sao tự làm trước khi xem đáp án; (c) chuẩn bị máy: cài Git for Windows (kèm Git Bash), JDK 21 Temurin, Python 3.11+ (tick Add to PATH), sqlite3 (hoặc dùng `labs/sqlrun.py`), rồi `bash labs/check_env.sh` đối chiếu từng dòng ✔. Không có ảnh chụp trình cài đặt: diễn đạt bằng sơ đồ các bước + địa chỉ chính thức (git-scm.com, adoptium.net, python.org, sqlite.org) và hành vi kiểm bằng lệnh. Đây là cảnh duy nhất được nhắc địa chỉ web.
6. Bài tình huống chuyên gia ở cuối (L10): dự án nhỏ "sổ tay giao dịch" ghép bash + sqlite + git: CSV giao dịch giả → nạp vào bảng → 3 truy vấn báo cáo → commit; có phần "khi dữ liệu lớn gấp 1000 lần" (vì sao đọc cả tệp vào bộ nhớ không ổn, vì sao cần chỉ mục) — P9.
7. Phát âm: dò mọi tên riêng/lệnh bạn định đọc thành lời (Git, Bash, curl, JSON, YAML, HTTP, SQL, sqlite, grep…) bằng ASR (`audit/cs112/probe_terms.py`, ghi `tools/registry/lexicon_vi.FND.yaml` + `symbols.FND.yaml` nếu cần). Không đạt ≥ 7/8 thì lời đọc diễn đạt bằng tiếng Việt, tên gốc chỉ hiện trên màn hình.

## Cổng cho mỗi bài (theo thứ tự; phải sạch)
```
cd /d/research-video
PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/fnd/verify_fnd.py Lxx
PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/fnd/gen.py Lxx
PYTHONIOENCODING=utf-8 .venv/Scripts/python -B tools/lv.py lint lessons/fnd/Lxx_*.yaml      # 0 FAIL, 0 WARN
PYTHONIOENCODING=utf-8 .venv/Scripts/python -B tools/lv.py render lessons/fnd/Lxx_*.yaml    # 0 vấn đề
PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/review/lab_gate.py FND
```
Cuối khoá: `tools/lv.py curriculum curriculum/fnd.yaml`, `audit/check_curricula_graph.py`, `audit/review/check_xref.py`, `check_meta.py`, `check_course_refs.py`, `check_next_refs.py` không báo lỗi do FND; mở 3 khung PNG mỗi bài kiểm bằng mắt. KHÔNG chạy `build`/`tts`/`asr`.
Nhắc khi viết: chuỗi có `\` đi qua heredoc bị hỏng → dùng Edit/Write; tên tệp/đường dẫn trên màn hình không có dấu và không có khoảng trắng; "bài sau" chỉ nhắc ở hook/recap và đánh `forward_ref: true`; không nhắc khoá khác ("bài JVA…") trong màn hình/lời đọc.
