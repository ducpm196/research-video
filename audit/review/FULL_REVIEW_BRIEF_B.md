# Đọc kiểm + sửa nội dung 23 khoá còn lại (đợt B, 2026-11-08)

Bối cảnh: người học **mất gốc**, học từ con số 0; mọi video trong thư viện phải dùng được để tự học về sau. Đợt A (300 bài nền) cho thấy các cổng tự động (lint, bộ kiểm số, ASR) **không** bắt được lỗi kiến thức: mẫu 50 bài có 9 bài sai kiến thức mức MUST, 42 bài có điểm cần sửa; cuối cùng 180/300 bài phải sửa. Nhiệm vụ: đọc **toàn bộ lời giảng** (`show` = HTML màn hình, `say` = lời đọc tiếng Việt, `checks`, đáp án quiz) của **từng** bài được giao, tìm lỗi và **sửa ngay**.

## Tìm gì
1. **Sai kiến thức** (MUST): định nghĩa, định lý, công thức, hành vi hệ thống/thư viện, quy chuẩn sai hoặc lỗi thời; ví dụ tự mâu thuẫn giữa các cảnh; màn hình và lời đọc nói khác nhau; đáp án quiz hoặc lời giải từng bước sai; số liệu tính sai.
2. **Gây hiểu nhầm** (SHOULD): khẳng định tuyệt đối sai ("luôn", "không bao giờ", "100%"); con số thực tế không nguồn trình bày như sự thật (thêm "(số minh hoạ)" hoặc dẫn nguồn); sự kiện, ngày tháng, tên người, tên sản phẩm có thật mà sai hoặc không kiểm được; điều mang tính thời điểm (phiên bản "mới nhất", mô hình AI "tốt nhất", giá) nói như vĩnh viễn; thuật ngữ dùng trước khi giải thích làm người mất gốc kẹt; bỏ sót điều kiện quan trọng.
3. Không báo chuyện văn phong. Số học đã có `checks` và `audit/<khoá>/verify_<khoá>.py` — vẫn đọc lại, thấy sai thì sửa.
4. Bài về sự cố/lịch sử có thật (CAS, bài `case: journey`, phần "stage"): mỗi sự kiện, năm, con số phải khớp nguồn đã ghi (`audit/<khoá>/sources_*.md` hoặc trường `source`). Mở nguồn để kiểm khi có thể; không kiểm được thì viết mềm lại và ghi "chưa kiểm được nguồn" trong báo cáo.
5. Nội dung an toàn thông tin chỉ ở mức phòng thủ/khái niệm; không thêm hướng dẫn khai thác.

Dẫn nguồn có thẩm quyền cho mỗi sửa (sách giáo khoa chuẩn, RFC, tài liệu chính thức, bài báo gốc, báo cáo sự cố gốc). Không bịa nguồn; trang web không có số phiên bản thì ghi "truy cập 2026-11-08, no revision given".

## Cách sửa (bắt buộc)
- Kiểm bài có sinh từ mẫu không: `ls audit/<khoá>/src/` (tệp `*.tpl.yaml` khớp bài). Có mẫu → sửa bài xong chạy `PYTHONIOENCODING=utf-8 .venv/Scripts/python audit/review/sync_tpl_from_lesson.py <KHOÁ> --write` (đọc docstring trước) và kiểm mẫu đã nhận sửa.
- Sửa bằng công cụ **Edit** (không dùng bash/python/sed thay chuỗi: dấu `\` qua shell bị hỏng; trong chuỗi YAML nháy kép, `\t` của `\times`, `\text`, `\to`, `\theta` thành TAB — dùng nháy đơn hoặc `\\`). Sau khi sửa chạy `.venv/Scripts/python -B audit/review/scan_ctrl.py` và bảo đảm không có lượt mới ở khoá của bạn.
- `say` là tiếng Việt nói được: không thêm từ ngoại mới ngoài những từ bài đã đọc (xem `tools/registry/lexicon_vi.<KHOÁ>.yaml`), số viết như cách tệp đang viết trong `say`. Màn hình và lời đọc phải khớp.
- Đổi số/logic → sửa `checks:` của cảnh và chạy bộ kiểm của khoá; nếu bộ kiểm mã hoá logic cũ thì sửa kèm lý do có nguồn ghi trong chú thích, **không bao giờ sửa kỳ vọng chỉ để qua**.
- **Tệp dùng chung** (`tools/checklib.py`, `tools/lv.py`, `audit/verify_plan_curricula.py`, `audit/dms/asr_review_dms.py`): KHÔNG sửa `lv.py` và `asr_review_dms.py`. Cần hàm mới trong `checklib.py` thì thêm bằng một lệnh Edit nhỏ (chỉ chèn, tiền tố tên khoá, không viết lại cả tệp, không dùng Write), rồi chạy `audit/check_checklib_dupes.py`. Không sửa `verify_plan_curricula.py`; nếu `rec()` của khoá bạn cần đổi vì bài đổi số, ghi vào báo cáo.
- `asr_reviewed`: xoá mục có `sentence` không còn trong `say` nào (lint E30 báo; có thể dùng `audit/review/prune_stale_asr.py`).
- Không nhắc số bài của bài sau giữa bài (lint E22); bài cuối không nói "bài sau" (E37).
- **Giáo án** `curriculum/<khoá>.yaml`: sau khi sửa bài, đọc mục của bài đó (`objectives`, `example`, `fix`) và sửa cho khớp bài nếu lệch; chạy `.venv/Scripts/python -B tools/lv.py curriculum curriculum/<khoá>.yaml` → 0 lỗi.
- Sau mỗi bài sửa: `.venv/Scripts/python -B tools/lv.py lint <tệp>` → 0 FAIL, 0 WARN; `.venv/Scripts/python -B tools/lv.py render <tệp>` → 0 vấn đề (rút gọn hoặc `clear: true` nếu tràn). Cuối cùng chạy bộ kiểm của khoá. **Không chạy `build`/`tts`/`asr`.**
- Tệp tạm: chỉ trong thư mục riêng `C:\Users\AI_WOR~1\AppData\Local\Temp\claude\740fb36319f596fa\7f725234-304e-4978-a40f-fd96917b65c7\scratchpad\review_b\<tên khoá>\`. Không chạm khoá của tác tử khác.

## Báo cáo ghi ra đĩa (bắt buộc — người điều phối sẽ đếm lại bằng công cụ)
Mỗi khoá một tệp `audit/review/full_review_b/<KHOÁ>.md`:
1. Dòng đầu: `# <KHOÁ> — đã đọc N/N bài`.
2. Bảng **một dòng cho MỌI bài** (kể cả bài không lỗi), đúng 5 cột:
   `| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |`
   Cột Kết luận chỉ dùng một trong: `đã sửa`, `không phát hiện lỗi`. Bài đã sửa ghi dòng kết quả lint (`lint: 0 FAIL, 0 WARN, …`) và render (`… (0 vấn đề)`) sau sửa.
3. Mục "Không sửa và vì sao" (điều nghi ngờ nhưng không đủ căn cứ).
4. Dòng kết quả cuối của bộ kiểm khoá và của `lv.py curriculum`.
Trả lời người điều phối ≤ 300 từ: số bài đã đọc/đã sửa, số mục MUST/SHOULD, đường dẫn tệp báo cáo, điều cần người điều phối làm (nếu có).
