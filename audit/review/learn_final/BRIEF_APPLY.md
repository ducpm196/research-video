# Áp phát hiện của chính bạn vào bài (đợt LF2)

Bạn vừa đọc một lô và trả bảng phát hiện. Bây giờ bạn **được phép sửa** các tệp bài trong lô của mình để áp những phát hiện ấy. Người điều phối sẽ kiểm diff rồi dựng lại video.

## Áp cái gì
- **Áp**: mọi MUST; mọi BLOCK và SHOULD có tin cậy CONFIRMED.
- **PLAUSIBLE**: chỉ áp khi ngay bây giờ bạn kiểm lại được bằng phép tính, chạy mã, hoặc tệp nguồn có sẵn trong kho (`audit/<khoá>/sources_*.md`). Dữ kiện cần nguồn ngoài mà kho chưa có: **không áp**, ghi vào danh sách "để lại".
- Không thêm phát hiện mới, không trau chuốt câu chữ khác.

## Áp thế nào
1. Dùng công cụ Edit trên `lessons/<khoá>/<bài>.yaml` (chuỗi có dấu `\` đi qua bash dễ hỏng: không dùng sed/python để thay). Mỗi chuỗi cũ phải khớp đúng một chỗ; nếu câu `say` cũ còn xuất hiện trong mục `asr_reviewed` của tệp thì sửa cả ở đó cho giống hệt câu mới (mục ấy chép nguyên câu đọc).
2. Giữ nguyên **số câu** của mỗi step (`focus` dạng danh sách đếm theo câu). Sửa `say` thì sửa `show` tương ứng và ngược lại.
3. Lời đọc mới: tiếng Việt nói được, không thêm từ ngoại mới, số viết như tệp đang viết, không có `$ \ _ ^ { }`, không viện khoá khác.
4. Nếu bài thuộc khoá sinh từ mã nguồn thì sửa ở nguồn rồi sinh lại, không sửa YAML: JVA (`audit/jva/src` → `audit/jva/gen.py`), BNK (`audit/bnk/src` → `audit/bnk/gen.py`), BNX (`audit/bnx/src` → `audit/bnx/gen.py`). Các khoá khác sửa thẳng YAML.
5. Nếu mục giáo án `curriculum/<khoá>.yaml` nói khác bài sau khi sửa (tiêu đề, mục tiêu, example), sửa cho khớp và ghi vào báo cáo.
6. Sau khi sửa mỗi tệp: `PYTHONIOENCODING=utf-8 .venv/Scripts/python tools/lv.py lint <tệp>` phải **0 FAIL, 0 WARN**. Lint báo lỗi do chỗ bạn sửa thì sửa tiếp; lỗi không do bạn thì báo lại.
7. **Không chạy** `render`, `build`, `tts`, `asr`, git. Không sửa tệp ngoài lô của bạn, không sửa `audit/review/screen_code/*.yaml` (nếu bạn đổi một khối mã trên màn hình, ghi rõ trong báo cáo để người điều phối cập nhật sổ).

## Trả lời cuối (ngắn, không quá 20 dòng)
- `ĐÃ SỬA: <danh sách bài>` kèm mỗi bài một dòng: số chỗ sửa · chỉ show hay có đổi say · kết quả lint.
- `ĐỂ LẠI: <phát hiện> — lý do` cho mỗi mục không áp.
- `CẦN NGƯỜI ĐIỀU PHỐI:` khối mã đã đổi (sổ screen_code), mục giáo án đã đổi, bài có mẫu `.tpl` nếu bạn biết.
