# Đọc kiểm + sửa nội dung toàn bộ khoá nền tảng (2026-11-08)

Bối cảnh: người học mất gốc, học từ con số 0 hướng tới backend ngân hàng. Mẫu 50/300 bài đã đọc: 9 bài sai kiến thức, 42 bài có điểm cần sửa — các cổng tự động (lint, bộ kiểm số, ASR) không bắt được loại lỗi này. Nhiệm vụ: đọc **lời giảng** (`show` = HTML màn hình, `say` = lời đọc tiếng Việt) của từng bài được giao, tìm và **sửa ngay**.

## Tìm gì
1. **Sai kiến thức** (MUST): định nghĩa, định lý, hành vi hệ thống, quy chuẩn sai hoặc lỗi thời; ví dụ tự mâu thuẫn giữa các cảnh; màn hình và lời đọc nói khác nhau; đáp án quiz sai.
2. **Gây hiểu nhầm** (SHOULD): khẳng định tuyệt đối sai ("luôn", "không bao giờ", "100%"); con số thực tế không nguồn trình bày như sự thật (thêm "(số minh hoạ)"); thuật ngữ dùng trước khi giải thích trong bài làm người mất gốc kẹt; bỏ sót điều kiện quan trọng.
3. Không báo chuyện văn phong. Đã kiểm số học bằng `checks` và `audit/<khoá>/verify_<khoá>.py` — tập trung vào lời giảng, nhưng nếu thấy số sai thì vẫn sửa.
Dẫn nguồn có thẩm quyền cho mỗi sửa (sách giáo khoa chuẩn, RFC, tài liệu chính thức, bài báo gốc).

## Cách sửa (bắt buộc)
- Kiểm bài có sinh từ mẫu không: `ls audit/<khoá>/src/` (tệp `*.tpl.yaml` khớp bài). Có mẫu → sửa bài xong chạy `PYTHONIOENCODING=utf-8 .venv/Scripts/python audit/review/sync_tpl_from_lesson.py <KHOÁ> --write` (đọc docstring trước). Khoá BNK/JVA sinh từ `audit/<khoá>/src/lNN.py` (không thuộc phạm vi đợt này).
- Sửa bằng công cụ Edit (không dùng bash/python thay chuỗi: dấu `\` qua shell bị hỏng). `say` là tiếng Việt nói được: không thêm từ ngoại mới ngoài những từ bài đã đọc (xem `tools/registry/lexicon_vi.<KHOÁ>.yaml`), số viết như cách tệp đang viết trong `say`. Màn hình và lời đọc phải khớp.
- Đổi số/logic → sửa `checks:` của cảnh và chạy bộ kiểm của khoá; nếu bộ kiểm mã hoá logic cũ thì sửa kèm lý do có nguồn ghi trong chú thích, không bao giờ sửa chỉ để qua. Hàm mới trong `tools/checklib.py` mang tiền tố khoá, chạy `audit/check_checklib_dupes.py`.
- `asr_reviewed`: xoá mục có `sentence` không còn trong `say` nào (lint E30 báo).
- Không nhắc số bài của bài sau giữa bài (lint E22).
- Sau mỗi bài sửa: `.venv/Scripts/python tools/lv.py lint <tệp>` → 0 FAIL, 0 WARN (ghi kết quả trước khi sửa); `.venv/Scripts/python tools/lv.py render <tệp>` → 0 vấn đề (rút gọn hoặc `clear: true` nếu tràn). Cuối cùng chạy bộ kiểm của khoá. **Không chạy `build`/`tts`.**
- Tệp tạm: đặt trong thư mục riêng `C:\Users\AI_WOR~1\AppData\Local\Temp\claude\740fb36319f596fa\7f725234-304e-4978-a40f-fd96917b65c7\scratchpad\<tên khoá của bạn>\` (không ghi đè tệp người khác).

## Báo cáo (≤ 600 từ)
Theo khoá: số bài đã đọc; bảng ngắn các mục đã sửa (bài, cảnh, MUST/SHOULD, một dòng lý do + nguồn); mục không sửa và vì sao; danh sách bài "không phát hiện lỗi"; dòng kết quả lint/render cuối của mỗi bài đã sửa; dòng kết quả bộ kiểm khoá.
