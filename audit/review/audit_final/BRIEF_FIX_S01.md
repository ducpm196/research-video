# BRIEF_FIX_S01 — sửa Chặng 1 theo báo cáo người đọc độc lập — 2026-11-13

Mỗi tác tử sửa MỘT khoá (FND, JVA hoặc JV2) theo báo cáo của người đọc: `audit/review/audit_final/reports/S01_<KHOÁ>.md` (đọc TOÀN BỘ báo cáo: bảng chuẩn xác, bảng độ sâu, cột "Cần biết trước", mục "Người học kẹt ở đâu", lab). Chuẩn bài = `BRIEF_AF2.md` (đọc lại mục 1–10) + `.claude/skills/lecture-video/SKILL.md`. Ngưỡng chốt cần đạt sau sửa: **MUST 0; P1 = 2 ở ≥ 90% bài; P8 = 2 ở 100%**.

## Việc phải làm
1. **Sửa mọi MUST** (kiểm lại từng cái bằng cách chạy thật trước khi sửa; nếu báo cáo sai thì ghi lý do vào báo cáo của bạn, không sửa).
2. **Sửa mọi SHOULD** có thể sửa; mục nào không sửa thì ghi lý do cụ thể (không "để sau").
3. **P1 — thuật ngữ tại chỗ**: với mỗi mục "Cần biết trước" của bài: giảng bằng một câu lời thường ở lần đầu xuất hiện TRONG BÀI (kèm ví dụ nhỏ nếu là cú pháp), hoặc bỏ thuật ngữ khỏi bài nếu không cần, hoặc (chỉ khi một bài ĐỨNG TRƯỚC trong dãy học của chính khoá đã giảng) ghi nhắc lại ngắn ở `prereq`. Thuật ngữ nhiều bài cùng dùng: giảng ở bài đầu tiên dùng nó, rồi nhắc lại ngắn ở bài sau.
4. **Mã trên màn hình đầy đủ để gõ lại được**: mọi `import`, khung `class`/`main`, `throws`, dòng in mà người học cần để mã chạy phải HIỆN (khung ≤ 12 dòng: tách khung hoặc `lines=`), và `de.md` của lab ghi rõ những `import`/lệnh cài cần dùng. Ví dụ đo hiện đầu ra thì phải hiện cả mã tạo ra nó (hoặc nói rõ nó nằm ở lab).
5. **Mục tiêu giáo án chép đúng điều video dạy** (E51): mục tiêu thừa xoá khỏi bài và `curriculum/<khoá>.yaml` (sửa giáo án bằng Edit, đồng bộ `covers`); mục tiêu thiếu thì thêm cảnh/step dạy.
6. **Nhất quán**: tiêu đề–bảng–lời đọc cùng một số, cùng một tên (ví dụ "ba/bốn điều"); chính tả thống nhất.
7. Giữ nguyên chuẩn AF2 (cảnh `practice` + lab, quy mô) — chỉ sửa chỗ báo cáo chỉ ra, không viết lại cả bài.

## Quy trình (như BRIEF_AF2)
Sửa **nguồn** (`audit/<khoá>/src/lNN.py` → `gen.py`; không sửa YAML sinh ra bằng tay) → `verify_<khoá>` (thêm kiểm cho điều vừa sửa: số/đầu ra thật) → `gen.py Lxx` → `lv.py lint` (0 FAIL, 0 WARN) → `lv.py render` (0 vấn đề; tràn thì tách step + `clear: true`, chỉnh `focus` theo số câu) → `audit/review/lab_gate.py <KHOÁ>` → xem ≥ 3 khung PNG mỗi bài đã đổi. Cuối khoá: `tools/lv.py curriculum curriculum/<khoá>.yaml`, `audit/check_curricula_graph.py`, `audit/review/check_xref.py`, `check_meta.py`, `check_course_refs.py`, `check_next_refs.py`, `arith_scan.py`, `python tests/test_e52.py`; `audit/review/screen_code.py check --course <KHOÁ>` (sổ cập nhật nếu khối mã đổi: dùng `stub` rồi điền; sổ của FND/JV2: `audit/review/screen_code/<KHOÁ>.yaml`).
**KHÔNG chạy** `build`/`tts`/`asr`/`audit_all`/git/docker (người điều phối dựng lại một lần sau). Chuỗi có `\` qua heredoc bị hỏng → luôn Edit/Write. Lời đọc không từ khoá lập trình tiếng Anh (gen từ chối); câu ≥ 4 từ và ≤ 38 từ; đầu ra chương trình viết không dấu. Mỗi câu `say` mới/đổi là một câu TTS mới → giữ câu đủ dài (≥ 8 từ) để máy nghe không gắn cờ ngắn.

## Cổng mới (bài AF2 phải qua)
- **E52** (thuật ngữ chữ): mục sổ `term:` trong `tools/registry/symbols.<KHOÁ>.yaml` (xem `tests/test_e52.py`). Bạn được **thêm mục sổ** cho các thuật ngữ then chốt của khoá mình (id có tiền tố khoá, `name`, `term: '(?i)regex'`) và đặt `introduces: [id]` đúng step giảng + `assumes: [id]` ở bài sau dùng (bài sau phải có bài tiên quyết giới thiệu: `lv.py curriculum` kiểm). Chỉ thêm thuật ngữ bạn chắc chắn bài giảng đúng chỗ; lint sẽ báo nếu bài khác của khoá dùng trước khi giảng — khi đó sửa bài (đó chính là lỗi P1).
- **E55**: dạng viết chuẩn ở `tools/registry/term_canon.yaml`.

## FND: quyết định môi trường (người điều phối đã chốt)
`sqlite3` dòng lệnh là **bắt buộc** (không dùng Python thay thế): FND L00 dạy cài (tải `sqlite-tools-win-x64` từ sqlite.org, giải nén, đặt thư mục có `sqlite3.exe` vào PATH hoặc bỏ cạnh `bash.exe`… chọn cách đơn giản và kiểm được bằng `sqlite3 --version`); `kiem.sh` kiểm bằng `command -v sqlite3` (không qua mô-đun Python); sửa `labs/check_env.sh` cho khớp. Máy kiểm của kho CHƯA có `sqlite3`; để kiểm bằng CLI thật, dùng bản mượn tạm trong scratchpad (người đọc đã dùng `sqlite3.exe` 3.46.0 trong thư mục Nsight Systems của máy; chỉ chạy trong scratchpad, KHÔNG chép vào kho, KHÔNG tải gì từ mạng). Ghi rõ trong báo cáo bản `sqlite3` bạn dùng; người điều phối sẽ chạy lại bằng bản chính thức. Thông tin về `.import` và dòng tiêu đề (bản 3.46: không có bảng trước thì dòng tiêu đề thành tên cột nên COUNT ra 10, không phải 11) phải được bài dạy đúng.
Git (L09): dạy `git config user.name/user.email` (một lần) và `git init -b main` (hoặc nói rõ nhánh mặc định có thể là `master`); mọi lệnh trên màn hình chạy được trên Git for Windows mới cài.

## Báo cáo
Tin nhắn cuối ≤ 30 dòng: bài đã sửa, MUST/SHOULD đã sửa (số), điểm P1 dự kiến, cổng nào PASS (số thật), mục nào không sửa và vì sao. Báo cáo chi tiết ghi `audit/review/audit_final/reports/fix_S01_<KHOÁ>.md`. Không kể quá trình.
