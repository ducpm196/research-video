# Phụ lục vòng 4 (đọc độc lập trên bản dựng cuối) — đọc SAU `audit/review/sample_f/BRIEF.md` và `ADDENDUM.md`

Đợt này CHỈ ĐO. Giữ nguyên mọi quy định của BRIEF (chỉ đọc; không mở báo cáo nào trong `audit/review/audit_final/reports/`; tự tính lại số;
xem ≥ 5 khung hình; báo cáo trong tin nhắn cuối; tệp tạm chỉ trong scratchpad được giao). Mỗi bài đã được dựng lại; người điều phối đã
kiểm `spec_sha256` của bản dựng khớp đặc tả. Bạn vẫn phải kiểm lại (xem dưới).

## Chuẩn P1 CHẶT (chuẩn chính thức từ giờ — chấm đúng như sau)
"Mục chưa giảng" = một lệnh / ký hiệu / đối số / cú pháp / thuật ngữ / chữ viết tắt xuất hiện trong mã hoặc chữ trên màn hình của đường
chính (không tính khung xem trước ở mở đầu, không tính đầu ra thuần, không tính tên suy ra được từ chính cái tên, ví dụ `sum`) mà
người chưa biết gì KHÔNG suy ra được và KHÔNG được giảng (a) tại lần xuất hiện đầu tiên trong bài, hoặc (b) trong một cảnh đứng trước
nó trong CÙNG bài, hoặc (c) trong bài đứng trước của CÙNG khoá (theo `curriculum/<khoá>.yaml`) VÀ bài này không nhắc lại một dòng cách đọc.
Chấm: 0 mục = P1 2; 1–2 mục = P1 1; ≥ 3 mục = P1 0. Liệt kê TỪNG mục (bài, cảnh/step, trích chữ) — không chỉ ghi số.
Thông tin "đã học ở khoá khác" không được tính là giảng. Bài phải tự đứng được.

## Việc phải làm thêm so với BRIEF
- Kiểm `build_report.json` của mỗi bài: `spec_sha256` của bản dựng so với `python -c "import sys;sys.path.insert(0,'D:/research-video/tools');import lv"` → hàm `lv.spec_digest` trên đặc tả (bỏ `asr_reviewed`). Nếu không tự gọi được thì so `built_at` với thời gian sửa tệp YAML và ghi rõ phương pháp.
- So `<Lxx>.srt` với `say` từng câu (thiếu câu? sai số?).
- Chạy thật mọi lab: `labs/<KHOÁ>/<Lxx>/{de.md,mong_doi.txt,loi_giai.*}` — đọc đề, chạy lời giải bằng đúng lệnh trong `de.md`, đối chiếu `mong_doi.txt` (bài nào cần Docker/mạng/cơ sở dữ liệu ngoài thì ghi "chỉ đọc").
- Mọi đoạn mã/lệnh trên màn hình chạy được: chạy thử và so kết quả với kết quả trên màn hình và lời đọc.
- Chấm P8 (thí nghiệm) và P9 (quy mô/thời gian) như ADDENDUM; cuối báo cáo thêm mục "Người học kẹt ở đâu".
- Báo cáo thêm bảng tóm tắt: số bài MUST=0; số bài P1=2; số bài P8=2; số bài spec khớp; số bài SRT khớp; số bài lab chạy; số SHOULD.
- Nếu cú pháp mã của một ngôn ngữ chưa từng được giảng ở đâu cả trong khoá nhưng bài có bảng "cách đọc"/"viết trong mã → đọc là" thì
  vẫn liệt kê mục đó, thêm cột "bảng cách đọc có phủ không (có/không)" để người điều phối đo riêng.
