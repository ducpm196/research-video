---
name: lecture-video
description: Produces Vietnamese explainer videos that teach step by step to beginners and learners with weak foundations — technical subjects (math, computer science, data, AI, systems, engineering) and, through domain profiles, foreign languages, soft skills, social science and philosophy, film analysis and transparent affiliate product guides — from a source document or a designed curriculum to a narrated 1080p MP4 with subtitles, with machine-checked numbers, notation consistency, ASR-checked pronunciation and expert case lessons built from real incident reports. Use when the user asks to make a lecture/teaching video, turn course material into videos, open a new subject area or course, write the next lesson of a series, fix or audit lesson videos, or keep the course roadmap accurate (for example: tạo video giảng giải, bài giảng cho người mất gốc, mở khoá mới cho chuyên ngành, làm bài tiếp theo L02, sửa phát âm video, rà soát lộ trình).
---

# Lecture Video (video giảng giải cho người mới / mất gốc)

**Hồ sơ chuyên ngành** (`tools/profiles/*.yaml`, references/profiles.md): `stem` (mặc định), `language`, `softskill`, `humanities`, `film`,
`affiliate`. Đường ống, luật đọc được, máy nghe, kiểm bố cục là chung; hồ sơ quyết định phân cảnh, nhãn, chuẩn độ sâu, chính sách bằng
chứng và luật riêng (E41–E50). Kiến trúc mã: `tools/README.md`.

Pipeline: tài liệu nguồn → rà soát toán → lộ trình → đặc tả bài (YAML) → lint → storyboard → giọng đọc → **máy nghe lại (ASR)** → khung hình → MP4 + SRT → verify → xem bằng mắt.
Mọi lệnh chạy từ thư mục gốc dự án bằng `.venv/Scripts/python` (Windows) hoặc `.venv/bin/python`.

## Dependency contract
- Capability ownership: viết đặc tả bài giảng theo khung sư phạm cho người mới, theo hồ sơ chuyên ngành; kiểm chứng toán trong bài; giữ ký hiệu nhất quán; dựng video có giọng đọc tiếng Việt, phụ đề, chương; kiểm phát âm bằng ASR; quản lý lộ trình khoá học.
- Trigger conditions: yêu cầu tạo video giảng giải, chuyển tài liệu môn học thành video, viết bài tiếp theo trong `curriculum/*.yaml`, sửa lỗi phát âm/ký hiệu của một video, rà soát toán của một bài giảng.
- Exclusions: dựng phim/hiệu ứng điện ảnh, hoạt hoạ chuyển động liên tục (Manim), đăng tải lên nền tảng video (là hành động ra bên ngoài — phải hỏi người dùng).
- Required capabilities: `evidence-gated-work` (nhãn OBSERVED/CITED/INFERRED, DONE/PARTIAL/BLOCKED — EGW section 2); Python 3.10+ với `.venv` (numpy, sympy, pyyaml, playwright, edge-tts, imageio-ffmpeg, pillow, faster-whisper); Node.js với `tools/vendor/node_modules/katex`; trình duyệt Microsoft Edge hoặc Chromium của Playwright.
- TTS dự phòng (2026-10-28): (1) edge-tts → Azure Speech REST tự động TỪNG CÂU khi có `AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION` — cùng mô hình giọng vi-VN-NamMinhNeural; (2) giọng khác chỉ chọn cho CẢ bài qua `voice: "vieneu:<giọng>"` (VieNeu-TTS, Apache-2.0, chạy trong `.venv-tts`) hoặc `voice: "piper:<mô hình>#<người đọc>"` — piper 1.8 mất thanh điệu tiếng Việt (OBSERVED), KHÔNG dùng cho bài giảng. Không trộn giọng trong một bài; một khoá nên dùng một giọng. `build_report.json` ghi `tts_sources` và `voices`. Đo giọng mới: `audit/tts_fallback_probe.py` (F0, giây/từ, ASR).
- Optional dependencies: mạng Internet cho edge-tts (giọng đọc trực tuyến của Microsoft) và cho lần tải đầu mô hình ASR (~480 MB). Khi không có mạng: `lint`, `preview`, `render` vẫn chạy; `build` dừng ở bước tts và báo BLOCKED, không tự thay giọng khác; thiếu mô hình ASR thì phát âm là NOT_VERIFIED.
- Canonical standards referenced: references/pedagogy.md (khung bài giảng, luật ký hiệu, luật lý do), references/production.md (lỗi đã gặp & cách xử lý), references/new-domain.md (mở chuyên ngành mới: phạm vi, khung, cổng kiểm), references/case-lessons.md (bài tình huống chuyên gia, bài hành trình theo trục thời gian), references/profiles.md (hồ sơ chuyên ngành: ngoại ngữ, kỹ năng mềm, xã hội–triết học, phim ảnh, tiếp thị liên kết; luật E41–E50).
- Compatible specialist workflows: artifact/HTML để chia sẻ storyboard; không cần skill định dạng file.
- Verification requirements: `lint` 0 FAIL và mọi WARN đã được xử lý hoặc giải thích; `tests/test_lint.py` 0 FAIL; `build` kết thúc bằng `verify … PASS`; `asr` 0 câu gắn cờ chưa xem xét; đã tự mở khung hình theo Bước 6. Kiểm tra bằng máy không thay được việc xem bằng mắt, và ASR không thay được tai người.

## Quy trình

### Bước 0 — Môi trường (một lần cho mỗi máy)
```
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt   # phiên bản đã ghim
cd tools/vendor && npm install katex@0.16.11
```
Kiểm tra: `.venv/Scripts/python tests/test_lint.py` phải in `tests: 0 FAIL`.

### Bước 1 — Rà soát tài liệu nguồn TRƯỚC khi dạy
1. Đọc toàn bộ nguồn. Liệt kê mọi ví dụ số, công thức, và mọi phát biểu kiểu “luôn / đảm bảo / chính là”.
2. Viết script kiểm chứng (mẫu: `audit/verify_cs115_tex.py`): mỗi ví dụ số được tính lại bằng sympy; mỗi phát biểu khái niệm đáng ngờ được thử tìm phản ví dụ bằng máy.
3. Ghi `audit/AUDIT_<course>.md` gồm bảng Sai / Thiếu điều kiện / Thuật ngữ; mỗi dòng có số dòng nguồn, bằng chứng và cách viết đúng.
4. Video **không bao giờ lặp lại phát biểu sai** của nguồn; ghi điểm cần sửa vào trường `fix` của bài trong curriculum.

### Bước 2 — Lộ trình (`curriculum/<course>.yaml`)
Mỗi bài có `id, title, source, requires, spec, fix`. Chạy `tools/lv.py curriculum ...` để bắt chu trình, thứ tự sai, và `assumes` mà chưa bài nào dạy.
Khoá mới dùng lại số hiệu L00… của khoá khác: ghi `course: <KHOÁ>` trong mọi bài và trong lộ trình; luật đọc, ký hiệu mới của khoá đặt ở tệp phủ thêm `*.<KHOÁ>.yaml` (không sửa tệp chung — đổi lexicon chung làm video khoá cũ thành STALE); sau khi đổi công cụ, chạy lại lint + verify + so `tts_sha256` của mọi bài khoá cũ.
Giáo án kế hoạch (chưa có bài): đặt `status: planned`. Mỗi bài cần `objectives`, `example` và `fix`. Mọi con số trong `example` phải PASS ở một script kiểm (mẫu: `audit/verify_plan_curricula.py`) TRƯỚC khi ghi vào giáo án. Tiên quyết ở khoá khác ghi `requires_ext: ["CS115:L13"]`; `curriculum` kiểm khoá và bài có thật. Bài liên quan nhưng không bắt buộc ghi `see_also`. Bản đồ các khoá: `curriculum/ROADMAP.md`.
**Khoá mới:** `tools/lv.py new-course <KHOÁ> --title "…"` dựng khung (lộ trình, lớp phủ ký hiệu và phát âm, bộ kiểm độc lập) — làm theo references/new-domain.md. Bài chưa có tệp đặc tả ghi `spec_planned:` (đổi thành `spec:` khi tệp có thật). Bài cuối mỗi khoá là bài tình huống chuyên gia (references/case-lessons.md).
Sau khi thêm hay sửa bất kỳ lộ trình nào, chạy `audit/check_curricula_graph.py`. `curriculum` chỉ kiểm từng khoá; script này kiểm MỌI lộ trình:
- đồ thị tiên quyết toàn cục không có chu trình;
- mọi “VER X:Lyy” trỏ tới một dòng PASS của đúng bài đó;
- liệt kê ví dụ có số mà không dẫn VER. Số đặt ra để minh hoạ thì phải ghi “(số minh hoạ)”.
Bài có hình SVG sinh bằng máy: soạn ở `audit/<khoá>/src/Lxx.tpl.yaml`, ghép bằng `fill_tpl.py`. Mẫu là nguồn duy nhất, nên `asr_reviewed` cũng phải ghi vào mẫu.
Chèn bài vào giữa lộ trình = đánh số lại: đổi tên file/`out/`, ánh xạ mọi “bài N” bằng script in từng dòng đổi, đọc lại từng dòng, sửa tay các khoảng số và các câu “bài sau” KHÔNG có số (phép thay không chạm tới), rồi build lại mọi bài đã làm. `curriculum` báo bài bị bỏ sót; E24 báo “bài sau” trỏ sai bài.

### Bước 3 — Viết đặc tả bài (theo **references/pedagogy.md**)
`tools/lv.py new lessons/<khoá>/<id>_<slug>.yaml --id <id> --title "..."` (thêm `--kind case` cho bài tình huống sự cố, `--kind journey` cho bài hành trình theo trục thời gian); mẫu tự điền `course` từ thư mục và `series` từ bài đã có. Bài mới khai `depth: full` (chuẩn độ sâu cho người mất gốc, lint E39 — pedagogy.md luật 22); bài hành trình khai thêm `case: journey` (E40 — case-lessons.md mục 5). Luật cứng (lint chặn):
- Phân cảnh bắt buộc: `hook, symbol, example, pitfall, quiz, recap`.
- **Ký hiệu trước khi dùng:** mọi ký hiệu (kể cả `·`, `⇒`, `‖ ‖`) phải được `introduces` ở step giải thích nó. Ký hiệu mới của khoá thêm vào `tools/registry/symbols.<KHOÁ>.yaml`. Ký hiệu mang nghĩa KHÁC sổ chung thì khai `replaces: <id chung>`; ví dụ ở TOC, `\Sigma` là bảng chữ cái chứ không phải ma trận hiệp phương sai, còn `\varepsilon` là chuỗi rỗng chứ không phải số rất nhỏ. Khi đó lint không đòi người học biết nghĩa cũ. Sửa sổ xong thì kiểm mọi mẫu `re.compile` được.
- **Nhất quán ký hiệu:** mỗi khái niệm chỉ viết một kiểu trong bài (ví dụ ‖x‖ hay ‖x‖₂). Muốn nói về kiểu viết khác thì làm trong một step `notation_note: true`. Ghi quy ước ký hiệu ở đầu file.
- **Phép toán nền phải được dạy trước khi suy luận dựa trên nó.** Ví dụ: trước khi viết `z = y − c·u` phải dạy cộng/trừ vector, nhân vector với số và chuyển vế.
- **Lý do cho mọi bước biến đổi:** trong `formula`/`check`, mỗi step có dấu `=` hoặc `⇒` phải nói *vì sao* (vì / nên / theo / thay / chuyển vế…). Sau công thức tổng quát phải có “làm thử ngay bằng số” cho cùng bước đó.
- Mỗi con số trên màn hình có `checks` (biểu thức Python trả về `True`). Mô phỏng thì gọi `alg.*` (tools/checklib.py: run_asm, cache_hits, sched_waits, rr_waits, race_run/race_finals, prodcons, philosophers, banker, fit, page_faults, inode_max/inode_reads, disk_fcfs/sstf/scan, fork_loop; TOC: strings, dfa_run/dfa_complete, nfa_run, subset_construct, minimize, regex_lang, pump_survivors, cfg_lang, balanced, bracket_values, pda_0n1n, tm_run, collatz, subset_sums) — không gõ sẵn kết quả (E35). Mã chương trình hiện trên màn hình phải được chép nguyên văn vào script kiểm và chạy ra cùng kết quả (lỗi thật TOC L10: băng dạng `list` sai khi đầu đọc đi trái quá ô 0). Thuật ngữ trùng mẫu chặn E29 (“dòng” của bộ nhớ đệm) khai `domain_terms: [dòng]`.
- `say` là lời nói: không có `$ \ _ ^ { }`; số âm đọc là “âm 2”; câu ≤ 38 từ và ≤ 170 ký tự.
- **Người học chỉ có video:** không nhắc “tài liệu (gốc)”, “dòng N”, “slide môn học”, “bài báo gốc” (E29); nêu thẳng điều đúng hoặc gọi tên nguồn (tác giả, năm).
- **Câu nói chỗ nào thì chỉ chỗ đó:** bước ≥3 câu trên khối ≥3 phần cần `focus:` (mỗi câu một mục, E31/E32) — xem pedagogy.md luật 19.
- **Công thức và khoá step**: tên lệnh LaTeX thiếu `\` (`$equiv$`) bị FAIL (E33). Khoá step lạ, ví dụ dòng thừa, bị FAIL (E34). Khoá YAML trùng là lỗi nạp tệp, không còn bị lấy lặng lẽ giá trị sau.
- **Không sửa đặc tả bằng chuỗi thay thế lồng trong shell** (sed, `python -c` trong ngoặc kép): `\b`, `\n`, `\l` (trong `\neg`, `\lt`) bị shell hoặc Python đổi thành ký tự điều khiển và làm hỏng tệp — lỗi thật ở DMS L01, L15, và chính dòng này lần đầu. Dùng Edit, hoặc một tệp `.py` với chuỗi raw; sau khi sửa, lint lại. Heredoc của Bash tool cũng đổi `\\` thành `\` (lỗi thật ở luật nhóm đơn vị của `asr_review_dms.py`): viết script bằng Write rồi chạy, và sau khi sửa thì grep tìm byte `\x08`.
- **Trích dẫn bài khác** (luật 17 của pedagogy.md, lint E22–E24): “bài N” là số thứ tự trong lộ trình. Nhắc bài trước thì nói lại nội dung đó. Nhắc bài sau chỉ ở hook/in_ai/recap, giải thích bằng lời thường, và đánh dấu `forward_ref: true`.
- **Bản đồ khoá học và bài cuối** (E37): khoảng “bài a–b” phải trỏ tới bài có thật; một cảnh nhắc ≥ 60% số bài là bản đồ khoá và phải phủ ĐỦ mọi bài (lỗi thật CS115 L00 bỏ sót L44 sau khi thêm bài); bài số lớn nhất không được hẹn “bài sau”.
- **Một từ, một cách viết** (E38): dạng chuẩn ở `SPELL_CANON` trong `tools/lv.py` (lũy, tuỳ, huỷ, khoẻ, lôgarit, tỉ, vector — dạng đa số của kho). Thay chữ hàng loạt thì đối chiếu lại `reason` trích nguyên văn ASR.

### Bước 4 — Phát âm
- `tools/registry/lexicon_vi.yaml`: luật chỉ khớp **nguyên từ** và mặc định phân biệt hoa thường. Lint tự kiểm danh sách `must_not_change` (hai, sai, …) mỗi lần chạy.
- Lint cảnh báo mọi từ không phải âm tiết tiếng Việt. Với mỗi từ như vậy:
  1. Thử 2–3 cách viết, mỗi cách tổng hợp một câu ngắn.
  2. Cho ASR nghe lại và chọn cách viết mà ASR nghe ra gần đúng nhất.
  3. Thêm luật đọc vào lexicon, hoặc thêm vào `foreign_ok` kèm ghi chú bằng chứng.
- **Không tự bịa cách phiên âm mà chưa thử bằng ASR.**

### Bước 5 — Kiểm và dựng
```
.venv/Scripts/python tools/lv.py lint     lessons/<file>.yaml   # 0 FAIL; đọc từng WARN
.venv/Scripts/python tools/lv.py preview  lessons/<file>.yaml   # out/<khoá>/<id>/preview.html, duyệt bằng ←/→
.venv/Scripts/python tools/lv.py build    lessons/<file>.yaml   # lint → tts → render → mp4/srt/chapters → verify
.venv/Scripts/python tools/lv.py asr      lessons/<file>.yaml   # small nghe mọi câu; câu bị gắn cờ được medium nghe lại
```
`asr` mặc định có `--recheck medium`: mô hình thứ hai nghe **mọi** câu. Một câu bị gắn cờ khi (a) cả hai mô hình đều khớp < 0,8, hoặc (b) có **từ** mà cả hai mô hình đều nghe khác. Mức câu (a) không đủ: một từ đọc sai trong câu 10 từ vẫn cho độ khớp ≥ 0,8 (đối chứng dương L02), nên cần (b).
Các câu còn lại thường rơi vào ba nhóm:
- tên chữ cái đọc kiểu Việt (x → “ích”, z → “dét”), không phải lỗi;
- cặp âm dễ lẫn (hai/hay, vuông/vùng), cần người nghe;
- câu cực ngắn, phải sửa. Lint đã cảnh báo câu ≤ 2 từ.
- `render` FAIL khi nội dung tràn bảng, phụ đề tràn, hoặc KaTeX lỗi. Sửa đặc tả, không giảm cỡ chữ toàn cục để lách.
- `render` cũng FAIL khi có lỗi bố cục (`layoutIssues` trong `player.html`): hai phần của khối chồng nhau, công thức thò ra ngoài phần chứa nó, hoặc viền nhấn chạm chữ của phần khác. Tiêu đề xuống hai dòng cũng FAIL.
- Quét cả khoá mà không cần dựng video: `audit/layout_scan.py <KHOÁ>`. Khung tràn thì tách bước bằng `audit/add_clear.py`.
- Nhịp dọc của mẫu là hợp đồng, không được sửa riêng từng bài:
  - khoảng giữa các phần .4em > viền chờm 8px (viền 4px + cách 4px);
  - mục danh sách cách .28em;
  - dòng bảng và dòng mã: viền vẽ vào trong.
- `asr` gắn cờ câu có độ khớp < 0,8. Với mỗi câu bị gắn cờ:
  - lỗi do TTS thì sửa lexicon hoặc lời đọc, rồi build lại;
  - lỗi do ASR nghe nhầm (ví dụ d/gi, ch/tr) thì ghi vào `asr_reviewed: [{sentence, reason}]` của bài.
- Trước khi tin kết quả ASR trên một giọng hay mô hình mới, chạy **đối chứng dương**: một câu cố tình đọc sai phải bị gắn cờ.

**Dựng hàng loạt và tốc độ** (đo 2026-10-30; số đo trong chú thích ở `tools/lv.py` và `audit/perf/`):
- Một khoá: `bash audit/.build_queue_run.sh <KHOÁ> L00 L01 …`. Sửa `audit/build_queue.sh`, rồi cập nhật bản chạy bằng `cp … x && mv -f x .build_queue_run.sh`. Không ghi đè tại chỗ khi hàng đang chạy.
- ASR chạy trên GPU nếu có (CUDA, int8_float16), không thì CPU int8. Ép thiết bị bằng `LV_ASR_DEVICE=cpu|cuda`.
  - Trên RTX 2060, medium chạy nhanh gấp khoảng 9 lần CPU.
  - Đối chứng dương 12/12. Cờ trên GPU nằm trong tập cờ của CPU (CS115 L02: 14 ⊂ 17).
  - Cache giữ khoá cũ (mô hình + băm wav), nên bản chép đã có không đổi. Bản chép mới có thêm tệp `.dev` ghi thiết bị đã nghe; `asr_report.md` ghi dòng “máy nghe”.
- Khi edge-tts lỗi `NoAudioReceived` (lỗi phía dịch vụ, khoảng 50% số lần gọi ngày 2026-10-30), `lv.py tts` tự đọc lại các câu hỏng thêm 3 lượt, nghỉ 30/60/120 giây, rồi mới báo BLOCKED.
  - Sau đó hàng đợi chờ 3 phút rồi 10 phút. Nếu vẫn bị chặn thì chuyển giọng dự phòng cho CẢ bài.
  - Dòng `tts:` ghi thời gian, số lần thử lại và loại lỗi. Đặt `LV_TTS_CONCURRENCY` / `LV_TTS_ROUNDS` để chỉnh.
- Theo dõi: `audit/review/production_log.tsv` ghi một dòng mỗi bài; xem tổng hợp bằng `.venv/Scripts/python audit/review/prod_watch.py`.
  - Log dựng không còn bị đệm, nên đọc được ngay khi bài đang dựng.
  - Các lần dựng bị chặn được giữ lại thành `<id>.try<N>.log`.
- Nguồn cùng giọng, miễn phí: Azure Speech gói F0 (cùng giọng vi-VN-NamMinhNeural). Đặt `AZURE_SPEECH_KEY` và `AZURE_SPEECH_REGION`, khi đó câu nào edge-tts lỗi sẽ tự chuyển sang Azure; người dùng phải tự tạo khoá.

### Bước 6 — Kiểm tra trực quan (bắt buộc)
- Mở bằng công cụ đọc ảnh ít nhất các khung: khung đầu, 1 khung `symbol`, mọi khung có SVG, mọi khung có ký hiệu mới, khung cuối của `formula` và `example`, 1 khung `pitfall`, khung cuối.
- Tìm các lỗi: nhãn đè hình, mũi tên sai kích thước, ký hiệu viết hai kiểu, chỉ số/số mũ chưa được giải thích, ký hiệu xuất hiện trước lời giải thích.
- Lỗi nào thấy bằng mắt mà máy hoá được thì thêm luật vào lint và thêm ca thử vào `tests/fixtures/bad_lesson.yaml`.

### Bước 7 — Rà toàn kho và cập nhật hiện trạng (sau mỗi đợt dựng hay sửa)
```
.venv/Scripts/python audit/review/audit_all.py          # lint + STALE theo dấu băm + giọng + ASR chưa xem xét + asr_report cũ, mọi bài
.venv/Scripts/python audit/review/asr_flags.py <KHOÁ>   # câu gắn cờ chưa xem xét của một khoá; ⚠ NGẮN = viết lại rồi dựng lại
.venv/Scripts/python audit/review/asr_hand_gen.py <KHOÁ> "<nhãn>" <tệp>  # nháp lý do HAND theo bằng chứng probe — ĐỌC LẠI từng dòng
.venv/Scripts/python audit/review/asr_hand_insert.py <tệp> "<nhãn>"   # chèn khối vào asr_review_dms.py (trước dấu mốc)
.venv/Scripts/python audit/review/tts_speed_scan.py [0.22]  # câu nghi âm thanh cụt (giây/từ thấp) kèm bản chép ASR
.venv/Scripts/python audit/review/pedagogy_scan.py --stats # độ sâu sư phạm mỗi bài: hình, ví dụ số, ôn nền, tự kiểm, khung chữ liền
.venv/Scripts/python audit/review/check_course_refs.py  # “bài N”, bản đồ khoá, “bài cuối”
.venv/Scripts/python audit/review/check_meta.py         # “Bài N —”, series/voice/rate, tên bài = lộ trình
.venv/Scripts/python audit/review/status_report.py      # sinh curriculum/STATUS.md (không sửa tay)
```
- Bài STALE thì dựng lại; câu ASR mới gắn cờ thì xem xét. `curriculum/ROADMAP.md` dẫn STATUS.md cho số liệu, không chép số tay.

### Bước 8 — Báo cáo (theo evidence-gated-work)
- Báo các thứ sau:
  - đường dẫn mp4, srt, chapters; thời lượng;
  - kết quả lint, test, verify, asr kèm `checked_at`;
  - các khung đã xem bằng mắt;
  - các điểm còn NOT_VERIFIED: hiệu quả sư phạm với người học thật, và các câu ASR không phân định được.
- Phát âm chỉ được ghi là **ASR-checked**, không ghi là “đã nghe”. Người dùng nghe thử là bằng chứng mạnh nhất.

## Tệp trong dự án
| Đường dẫn | Vai trò |
|---|---|
| `tools/lv_profile.py`, `tools/profiles/*.yaml` | Hồ sơ chuyên ngành: phân cảnh, nhãn, độ sâu, bằng chứng, luật E41–E50 (references/profiles.md) |
| `examples/profiles/` | Một bài mẫu có nguồn cho mỗi hồ sơ (lint 0 FAIL; mẫu ngoại ngữ đã dựng) |
| `tools/lv.py` | CLI: new (`--kind case|journey`, `--profile`), new-course (`--profile`), lint, preview, tts, render, build, verify, asr, curriculum |
| `tools/vi_text.py` | Chuẩn hoá tiếng Việt, đổi số → chữ, dùng để so ASR |
| `tools/templates/` | `lesson_template.yaml`, `case_lesson_template.yaml`, `journey_lesson_template.yaml` (bài), `curriculum_template.yaml`, `symbols_overlay.yaml`, `lexicon_overlay.yaml`, `verify_template.py` (khoá mới) |
| `audit/review/` | `audit_all.py`, `asr_flags.py`, `check_course_refs.py`, `check_meta.py`, `status_report.py` (rà toàn kho), `sync_tpl_asr.py`, `pedagogy_scan.py` (độ sâu sư phạm) |
| `curriculum/ROADMAP.md`, `curriculum/STATUS.md` | lộ trình chương trình (viết tay, có tầm nhìn) và hiện trạng (sinh tự động) |
| `tools/templates/player.html`, `player.css` | Giao diện khung hình 1920×1080, cũng là storyboard |
| `tools/registry/symbols.yaml` | Sổ ký hiệu (pattern, unicode, cách đọc), lệnh chỉ để trình bày, luật nhất quán |
| `tools/registry/lexicon_vi.yaml` | Luật phát âm theo nguyên từ, `must_not_change`, `foreign_ok` |
| `tools/katex_macros.json` | Macro tô màu `\hl \hlb \hlg \hlo`, `\proj` |
| `tests/test_lint.py` + `tests/fixtures/bad_lesson.yaml` | Chứng minh lint bắt được từng loại lỗi (E1–E40) |
| `out/<khoá>/<id>/` | `<id>.mp4`, `<id>.srt`, `chapters.txt`, `preview.html`, `build_report.json`, `asr_report.md` (khoá = trường `course` của bài, mặc định CS115) |
| `lessons/<khoá thường>/`, `curriculum/<khoá>.yaml` | Đặc tả và lộ trình mỗi khoá; luật đọc / ký hiệu riêng của khoá: `tools/registry/lexicon_vi.<KHOÁ>.yaml`, `symbols.<KHOÁ>.yaml` |
| `out/_cache/tts/`, `out/_cache/asr/` | Cache theo hash: sửa 1 câu thì chỉ đọc lại và nghe lại câu đó |
