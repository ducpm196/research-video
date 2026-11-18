# BRIEF_WP4 — nâng BNX L00–L23, INT, ACB lên chuẩn AF2 — 2026-11-14

Mục tiêu: người học mất gốc chỉ xem video + làm lab vẫn đi tới trả lời phỏng vấn backend ngân hàng bằng hiểu biết thật. Mỗi bài được giao phải đạt chuẩn AF2 và qua người đọc độc lập (ngưỡng: **MUST 0; P1 = 2 ở ≥ 90% bài; P8 = 2 ở 100%**).

## Đọc trước (BẮT BUỘC, theo thứ tự)
1. `audit/review/audit_final/BRIEF_AF2.md` (chuẩn bài: `af2: true`, `covers`, cảnh `practice`/"Tự làm" + lab, thuật ngữ tại chỗ, cảnh quy mô/thời gian).
2. `audit/review/audit_final/BRIEF_BNK.md` (cách nâng BNK: mã thật trên màn hình, cảnh practice + lab, P1 tại chỗ, P9 quy mô).
3. `audit/review/audit_final/BRIEF_FIX_S01.md` mục "Việc phải làm" và "Cổng mới" (E52 thuật ngữ chữ qua `tools/registry/symbols.<KHOÁ>.yaml` `term:` + `introduces`/`assumes`; E55 `tools/registry/term_canon.yaml`).
4. `.claude/skills/lecture-video/SKILL.md`; `labs/ENV.md`, `labs/cham.sh`, `audit/labkit.py` (cấu trúc lab: `labs/<KHOÁ>/<Lxx>/{de.md,mong_doi.txt,loi_giai.*}`).
5. Mẫu đã qua người đọc: `audit/bnx/src/l24.py`… (BNX L24–L36), `audit/bnk/src/*.py`, `audit/jva/src/*.py` (hạ tầng `lib.py`).

## Bài học từ 4 vòng đọc độc lập Chặng 1–3 (tránh lặp lại)
- **Mã cụt / kết quả dán nhầm khung / REPL dùng biến chưa gán** là lỗi MUST phổ biến nhất: mọi khối mã trên màn hình phải CHẠY ĐƯỢC khi gõ lại từ trên xuống (đủ `import`, khung `class`/`main`, thân vòng lặp, `print` nếu kết quả hiện ra) và kết quả hiện ra đúng là kết quả của mã hiện ra (≤ 12 dòng/khung: tách step). Thêm kiểm vào bộ `verify_*` ghép nguyên văn khối trên màn hình rồi chạy thật.
- Số trong tiêu đề–bảng–lời đọc–quiz phải cùng một số, cùng một tên ("bốn điều" vs 5 hàng); số đo phải khớp bậc độ lớn khi người học tự đo; không nói tuyệt đối ("mọi", "luôn", "chắc chắn") khi có ngoại lệ.
- Chữ số: trong lời đọc viết "byte" đầy đủ (TTS đọc "N B" thành "N chục byte"); câu `say` ≥ 8 từ (câu ngắn bị máy nghe gắn cờ), ≥ 4 và ≤ 38 từ.
- Mục tiêu giáo án chép đúng điều video dạy (E51: mỗi mục tiêu có cảnh dạy; thừa thì xoá khỏi giáo án + bài, thiếu thì thêm cảnh).
- Sản phẩm không chạy được trên máy (Docker nặng, hệ thống ngân hàng, dịch vụ thật): ghi RÕ "mô phỏng" trên màn hình và trong lời đọc, nhãn đủ lớn; không bịa đầu ra của sản phẩm thật; chạy thật ở chỗ có thể (sqlite, Python, JDK 21, Docker `--rm` ảnh chính thức ghim băm, mỗi lần một ảnh; `bnx-ora`/`bnx-mss` chỉ qua `audit/bnx/dbrun.py`).
- Thuật ngữ nào giảng ở bài sau mà bài này đã dùng thì giảng tại chỗ bằng một câu lời thường + ví dụ nhỏ; bài phải tự đứng được (không "như đã học ở khoá…").
- Không số liệu thiếu nguồn (lương, quy trình tuyển dụng một ngân hàng cụ thể, điểm tín dụng thật); nêu "một số tin tuyển dụng backend ngân hàng nêu…" thay vì tên một ngân hàng làm nguồn sự thật. Pháp lý: chỉ dẫn văn bản có trong `audit/legal/registry.yaml`, ghi đúng tình trạng hiệu lực.
- Độ dài lời đọc ≤ 2 300 từ (≤ 16 phút ước); thêm thì cắt chỗ khác, không bỏ mục tiêu `covers`; không vừa thì ghi đề xuất tách bài vào báo cáo (đừng tự tách/đánh số lại).

## Quy trình mỗi bài
Sửa NGUỒN (BNX: `audit/bnx/src/lNN.py` → `python -B audit/bnx/gen.py Lxx`; INT/ACB: không có bộ sinh — sửa trực tiếp `lessons/int/*.yaml`, `lessons/acb/*.yaml` bằng Edit/Write; nếu khoá không có `verify_*` thì viết `audit/<khoá>/verify_<khoá>.py` kiểm số/mã/đầu ra thật) → verify → `tools/lv.py lint` (0 FAIL 0 WARN) → `tools/lv.py render` (0 vấn đề; tràn thì tách step + `clear: true`) → `audit/review/lab_gate.py <KHOÁ>` → xem ≥ 3 khung PNG mỗi bài đã đổi. Cuối phần: `tools/lv.py curriculum curriculum/<khoá>.yaml`, `audit/check_curricula_graph.py`, `python tests/test_e52.py`, `audit/review/screen_code.py check --course <KHOÁ>` (sổ cập nhật khi khối mã đổi; `stub` rồi điền; BNX: `audit/bnx/lib2.py gen-screen Lxx` + `screen_fast.py Lxx`).
**KHÔNG chạy** `build`/`tts`/`asr`/`audit_all`/git (người điều phối dựng một lần sau). Chuỗi có `\` qua heredoc bị hỏng → luôn Edit/Write. Không sửa tệp ngoài phạm vi của mình (các tác tử khác làm song song các bài khác; `curriculum/*.yaml` và registry chỉ sửa bằng Edit nhỏ).

## Báo cáo
Báo cáo chi tiết ghi `audit/review/audit_final/reports/<tên được giao>`; tin nhắn cuối ≤ 30 dòng: bài đã đổi, số cổng thật, P1 dự kiến, mục không làm + lý do, đề xuất tách bài. Ghi tiến độ vào đầu báo cáo sau mỗi 3 bài. Bị ngắt: người điều phối tiếp bằng SendMessage.
