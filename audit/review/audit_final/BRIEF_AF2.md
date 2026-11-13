# BRIEF_AF2 — chuẩn "bài final" cho người MẤT GỐC (soạn khoá mới và nâng bài cũ) — 2026-11-13

Người học: **mất gốc, chưa từng lập trình**, chỉ có video + thư mục `labs/`. Đích: năng lực nền của kỹ sư senior CNTT/KHMT/AI. Người dùng yêu cầu: hiểu cốt lõi và vận dụng, **thực nghiệm đi kèm kiến thức**, thấy vấn đề đổi theo thời gian và quy mô — không chỉ nhớ. Bài phải tự đứng được.

## Đọc trước (bắt buộc)
`.claude/skills/lecture-video/SKILL.md` + `references/pedagogy.md` + `references/production.md`; `labs/ENV.md`; `audit/labkit.py`; một bài mẫu đã nâng: `audit/jva/src/l04.py` (cảnh `practice`, `covers`, lab); `audit/review/sample_f/REPORT.md` mục 3–4 (các lỗi đã đo).

## Hợp đồng bài AF2 (lint chặn: bài khai `af2: true`)
1. **E51 `covers`**: mọi mục tiêu trong `objectives` trỏ tới MỘT cảnh dạy nó. Mục tiêu bắt đầu bằng động từ LÀM (viết, tính, dựng, chạy, cài, kiểm, chọn, vẽ, đo, tạo, sửa, gỡ, đọc, so sánh, đếm, xác định, chứng minh, giải, lập…) phải trỏ tới cảnh `example`/`check`/`formula`/`practice`. **Không hứa điều bài không dạy**: mục tiêu viết đúng điều video làm; thừa thì xoá; thiếu thì thêm cảnh.
2. **E53 cảnh `practice` (Tự làm)** đặt trước `recap`: trỏ `lab: labs/<KHOÁ>/<Lxx>` có `de.md`, `mong_doi.txt`, đúng một `loi_giai.<py|java|sql|sh|md>`. Step 1 đề + `pause`; step 2 kết quả mong đợi (MỌI dòng của `mong_doi.txt` hiện nguyên văn trên màn hình) + lệnh chấm; step 3 gợi ý. Dùng `labkit.write_lab` + `practice_steps` + `practice_scene`. **Số liệu của lab KHÁC số của ví dụ trong bài** (không chép lại được). Bài lý thuyết thuần: lab giấy bút (`loi_giai.md`, đáp án số ở `mong_doi.txt`) — vẫn có số cụ thể để đối chiếu. Lời giải code là `prog(...)` → bộ kiểm khoá chạy thật VÀ `audit/review/lab_gate.py` chạy lại qua `labs/cham.sh`.
3. **P1 thuật ngữ tại chỗ**: mọi thuật ngữ, ký hiệu, chữ viết tắt, lệnh, cờ lệnh bài dùng được giảng bằng lời thường ở LẦN ĐẦU xuất hiện TRONG BÀI (một câu là đủ), hoặc đã được giảng ở bài đứng trước TRONG DÃY HỌC của khoá (ghi nhắc lại ngắn ở `prereq`). Không "như đã học ở khoá X" (cổng `check_xref.py` cấm).
4. **P2 từng bước + P4 làm tay**: mỗi biến đổi có lý do ("vì", "nên", "nghĩa là") và thử bằng số; ví dụ trọn vẹn tự làm lại được bằng giấy bút/bàn phím.
5. **P3 trực quan**: mỗi khái niệm cơ chế có hình/bảng/sơ đồ khớp lời; không chữ đè/tràn (chạy `lv.py render`); cỡ chữ đọc được.
6. **P5 tự kiểm**: quiz kiểm HIỂU (có câu quyết định: "chọn A hay B, vì sao"), `pause` rồi đáp án từng bước.
7. **P6 chuyên sâu + P9 quy mô/thời gian**: vì sao đúng, giới hạn/điều kiện áp dụng, lỗi thường gặp; và ít nhất một cảnh cho thấy vấn đề ĐỔI khi hệ thống lớn dần hoặc theo thời gian (số liệu tính được ở ≥ 2 mức: ×1, ×100, ×10 000), giải pháp cũ gãy ở đâu, đánh đổi người làm nghề phải chọn. Số thật phải có nguồn trong `source`; số minh hoạ ghi "(số minh hoạ)".
8. Không khẳng định tuyệt đối ("luôn", "100%") mà thiếu điều kiện. Văn bản pháp lý: chỉ dẫn khi có mục trong `audit/legal/registry.yaml`.
9. Mọi con số trên màn hình có `checks`; ví dụ mã chạy thật bằng công cụ thật (JDK 21, Python, sqlite, bash); đầu ra hiện trên màn hình = đầu ra thật.
10. Dài mỗi bài ≥ 9 phút video, ≤ 16 phút (≈ 1 300–2 300 từ lời đọc); bài hành trình có thể dài hơn.

## Quy trình mỗi bài
Sửa **nguồn** (`audit/<khoá>/src/lNN.py` → `gen.py`; với khoá không có bộ sinh thì sửa YAML bằng Edit/Write) rồi theo thứ tự: verify của khoá → `gen.py Lxx` → `tools/lv.py lint` (0 FAIL, 0 WARN) → `tools/lv.py render` (0 vấn đề; tràn khung thì tách step + `clear: true`) → `audit/review/lab_gate.py <KHOÁ>` → mở 3 khung PNG kiểm bằng mắt. KHÔNG chạy `build`/`tts`/`asr` (người điều phối dựng một lần sau khi mọi sửa xong).
**Bẫy**: chuỗi có dấu gạch ngược (`\n`, LaTeX) đi qua heredoc bash/python bị hỏng → luôn dùng công cụ Edit/Write. Lời đọc không chứa từ khoá tiếng Anh của lập trình (gen từ chối); đọc số bằng chữ; câu ≥ 4 từ, ≤ 38 từ; đầu ra trong chương trình viết không dấu ASCII. Tên riêng/sản phẩm phải dò phát âm bằng ASR trước khi dùng trong lời (`audit/cs112/probe_terms.py`); không đạt thì chỉ hiện trên màn hình, lời đọc diễn đạt bằng tiếng Việt.

## Báo cáo
Trả về gọn: danh sách bài đã xong (cổng nào PASS, số liệu thật), bài chưa xong và vì sao. KHÔNG kể quá trình. Báo cáo dài ghi vào `audit/review/audit_final/reports/<tên>.md` (tác tử ghi được tệp trong thư mục này).
