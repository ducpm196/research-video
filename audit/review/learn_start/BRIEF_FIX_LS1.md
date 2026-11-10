# Giai đoạn sửa của đợt LS1 (2026-11-10)

Người điều phối đã đọc báo cáo của bạn và **chấp nhận** các phát hiện, trừ những điểm ghi riêng trong lời nhắn. Bây giờ bạn **được sửa** đúng các bài trong phần việc của mình, theo đề xuất trong báo cáo.

## Quy tắc bắt buộc
1. **Chỉ dùng công cụ Edit** để sửa tệp. Không dùng sed, python hay heredoc để thay chuỗi, vì dấu `\` trong LaTeX/regex sẽ hỏng.
   - Trong chuỗi YAML nháy kép, `\t` của `\times`, `\text`, `\to`, `\theta` sẽ thành TAB; dùng `\\` hoặc chuỗi khối `|`.
2. **Sửa đúng nguồn của bài**:
   - **JVA**:
     - sửa `audit/jva/src/lNN.py`, rồi chạy `PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/jva/gen.py LNN` (đọc docstring `gen.py` trước);
     - giáo án JVA sinh từ `audit/jva/gen_curriculum.py` (đọc docstring);
     - xong thì chạy `PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/jva/verify_jva.py` (phải 0 FAIL), rồi `PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/review/screen_code.py gen-jva` và `... screen_code.py check --course JVA` (0 FAIL, 0 STALE).
   - **Bài có mẫu `audit/<khoá>/src/*.tpl.yaml`** (CS112 L05, L06, L07…; DMS L08, L16–L18): sửa bài, rồi chạy `PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/review/sync_tpl_from_lesson.py <KHOÁ> --write` (đọc docstring trước), và kiểm mẫu đã nhận bản sửa.
   - **INT, ACB**: sửa thẳng `lessons/int|acb/*.yaml`. **Không bao giờ** chạy `resources/job/generate_int_*.py` hay `create_acb_lesson*.py`, vì chúng ghi đè.
   - **BNK**: nếu bài sinh từ `audit/bnk/src/lNN.py` thì sửa src rồi chạy `audit/bnk/gen.py LNN` (đọc docstring).
   - **Giáo án** `curriculum/<khoá>.yaml`: sửa thẳng, trừ JVA (xem trên).
3. **Màn hình và lời đọc phải khớp.**
   - Sửa `say` thì sửa `show` tương ứng, và ngược lại.
   - Nếu step có `focus` dạng danh sách mà bạn **thêm câu** vào `say`, thì phải thêm một mục `focus` cho câu đó. Cách an toàn hơn là nối mệnh đề vào câu có sẵn.
   - Câu mới dài hơn 7 từ. Không thêm từ ngoại mới vào `say` ngoài những từ bài đã đọc; xem `tools/registry/lexicon_vi.<KHOÁ>.yaml`.
   - Nếu bạn đổi một câu có trong `asr_reviewed`, hãy **xoá mục asr_reviewed của câu cũ** (máy nghe sẽ chấm lại khi dựng).
4. **Có con số mới thì thêm `checks`** để máy tính lại (xem cách viết checks ở các cảnh lân cận).
5. **Khối mã trên màn hình** (`class="code"` hoặc `<pre>`) mà bạn đổi:
   - chạy `PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/review/screen_code.py check --course <KHOÁ>`;
   - mục nào STALE: `screen_code.py show "<khoá>"` để lấy sha mới, rồi sửa `audit/review/screen_code/<KHOÁ>.yaml` (sha, và khẳng định nếu nội dung đổi);
   - chạy lại tới 0 FAIL / 0 STALE / 0 MISSING / 0 ORPHAN.
6. **Sau khi sửa mỗi bài**:
   - Lint: `PYTHONIOENCODING=utf-8 .venv/Scripts/python -B tools/lv.py lint lessons/<khoá>/<tệp>.yaml`, phải 0 FAIL và 0 WARN mới.
   - Render (không TTS, khoảng 20–60 giây): `PYTHONIOENCODING=utf-8 .venv/Scripts/python -B tools/lv.py render lessons/<khoá>/<tệp>.yaml`, phải không có lỗi tràn khung / layoutIssues.
     - Nếu tràn: tách step, thêm `clear: true`, hoặc rút chữ.
     - Mở bằng Read **khung hình của các step bạn đã đổi** trong `out/<KHOÁ>/<id>/frames/` (cộng dồn `duration` trong `_frames.txt` để tìm khung).
     - Render chạy tuần tự qua khoá `out/_render.lock`; nếu phải chờ thì cứ chờ.
7. **Không** chạy `build`, `tts`, `asr`, không chạy git. Người điều phối sẽ dựng lại video.
8. Cuối cùng chạy bộ kiểm của khoá nếu có: `audit/<khoá>/verify_<khoá>.py` (đọc docstring), cùng `audit/review/check_xref.py --course <KHOÁ>` và `audit/review/check_meta.py`. Không được có lỗi mới.

## Trả lời người điều phối (mọi thứ nằm trong câu trả lời cuối)
- Một bảng, mỗi phát hiện một dòng: `| Bài | Phát hiện (tóm tắt) | ĐÃ SỬA / KHÔNG SỬA (lý do) | Tệp đã đổi |`.
- Danh sách bài đã đổi, cần dựng lại: dạng `KHOÁ Lxx`.
- Kết quả lint, render, verify, screen_code, check_xref của khoá: dán dòng tổng kết.
- Mọi điều bạn phải làm khác đề xuất ban đầu, và vì sao.
