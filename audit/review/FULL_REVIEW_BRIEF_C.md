# Đọc kiểm lần ba + làm cho mỗi bài tự đứng được (đợt C, 2026-11-09)

Bối cảnh: người học **mất gốc**, học từ con số 0, sắp bắt đầu học thật. Hai đợt đọc trước (A: 300 bài nền, B: 326 bài còn lại) đã sửa nhiều lỗi, nhưng mẫu đọc độc lập 42 bài sau đó (`audit/review/sample_c/REPORT.md` — **đọc tệp này trước**) vẫn thấy lỗi mức MUST ở 5/42 bài và phát hiện thật ở 16/42 bài. Các cổng máy (lint, bộ kiểm số, ASR) đều qua nhưng **không** bắt được những lỗi đó. Nhiệm vụ của bạn: đọc **toàn bộ** từng bài được giao như một chuyên gia môn học khó tính, sửa ngay mọi lỗi, và làm cho bài **tự đứng được** (mục B).

## A. Tìm lỗi nội dung (như đợt B, nhưng kỹ hơn)
Đọc mọi `show` (HTML màn hình, cả chữ trong SVG), `say` (lời đọc), `checks`, quiz (câu hỏi, phương án, đáp án, giải thích), `title`, `objectives`, và mục của bài trong `curriculum/<khoá>.yaml` (`title`, `objectives`, `example`, `fix`), cùng `audit/<khoá>/sources_*.md` nếu có.
1. **MUST — sai kiến thức**: định nghĩa, định lý, công thức, hành vi hệ thống/thư viện/giao thức, quy chuẩn sai hoặc lỗi thời; ví dụ tự mâu thuẫn giữa các cảnh; màn hình và lời đọc nói khác nhau; đáp án quiz hoặc lời giải từng bước sai; số liệu tính sai; giáo án hứa điều bài không dạy hoặc nói khác bài.
2. **SHOULD — gây hiểu nhầm / làm người mất gốc kẹt**: thuật ngữ, ký hiệu, chữ viết tắt dùng trước khi giải thích (mỗi thuật ngữ mới phải được định nghĩa bằng lời thường ngay lần đầu xuất hiện); bước suy luận bị nhảy cóc; khẳng định tuyệt đối sai ("luôn", "không bao giờ", "100%"); số thực tế không nguồn trình bày như sự thật (thêm "(số minh hoạ)" hoặc dẫn nguồn); sự kiện, năm, tên người/sản phẩm sai hoặc không kiểm được; điều mang tính thời điểm (phiên bản "mới nhất", giá, "tốt nhất") nói như vĩnh viễn; bỏ sót điều kiện quan trọng.
3. **Làm tròn và số hiển thị**: tự tính lại bằng Python **mọi** con số hiện trên màn hình hoặc đọc ra (không chỉ số có trong `checks`), đúng tới số chữ số được ghi. Các lỗi mẫu đã thấy: 0,736 thay vì 0,7354; 19,6 thay vì 19,52; "201 ns" thay vì 200; "4 trạng thái" khi bảng có 5.
4. Bài sự cố/lịch sử có thật (CAS, bài `case: journey`, phần `stage`): mỗi sự kiện, năm, con số phải khớp nguồn ghi trong `audit/<khoá>/sources_*.md` hoặc `source`. Mở nguồn khi có thể; không kiểm được thì viết mềm lại và ghi "chưa kiểm được nguồn" trong báo cáo. Không bao giờ ghi "trích nguyên văn" cho câu bạn không đọc được trong nguồn.
5. An toàn thông tin chỉ ở mức phòng thủ/khái niệm. Không báo chuyện văn phong thuần tuý.

Dẫn nguồn có thẩm quyền cho mỗi sửa (sách chuẩn, RFC, tài liệu chính thức, bài báo gốc, báo cáo sự cố gốc). Không bịa nguồn; trang web không có số phiên bản thì ghi "truy cập 2026-11-09, no revision given".

## B. Yêu cầu mới: mỗi bài, mỗi video, mỗi mục giáo án tự đứng được
Người dùng yêu cầu: *"các video giáo án bài học đều độc lập, không nói ngắn gọn tham chiếu đến khóa học khác, cần giảng giải kỹ càng chuyên sâu."*
1. Trong mọi phần người học thấy hoặc nghe (`title`, `objectives`, `show`, `say`, quiz, chữ trong hình) và trong giáo án (`title`, `objectives`, `example`, `fix`): **không** nhắc khoá khác bằng mã (CS115, DBS, OSY…) hay bằng tên ("ở khoá Toán cho khoa học máy tính", "như khoá Hệ điều hành"), và không dùng "khoá trước", "khoá nền", "các khoá trước", "như đã học ở khoá…". Trường `source`, `checks`, `asr_reviewed`, chú thích YAML và `requires_ext` được giữ (không hiện, không đọc).
2. **Không chỉ xoá tên khoá.** Mỗi khái niệm bài mượn từ ngoài (từ khoá khác hoặc kiến thức nền) phải được **giảng lại trong chính bài này**, đủ để người chưa học khoá kia hiểu: định nghĩa bằng lời thường, trực giác (vì sao), và ít nhất một ví dụ số nhỏ làm từng bước (có `checks`) khi khái niệm có tính toán. Cảnh `prereq` thường đã có phần ôn — viết lại câu mở thành "Trước hết, ta cần hiểu …" / "Nhắc lại từ đầu: …" và kiểm xem phần giảng có đủ không; nếu chỉ một câu thì mở rộng thành một bước giảng hoàn chỉnh (thêm `steps`, có thể thêm cảnh `prereq`). Ví dụ đã thấy: "như ở khoá Toán cho robot, tần số lấy mẫu phải lớn hơn hai lần tần số cao nhất" — phải giải thích vì sao (lấy mẫu thưa thì hai sóng khác nhau cho cùng dãy mẫu) bằng ví dụ số.
3. Câu chỉ đường cuối bài ("muốn học thêm hãy xem khoá X") → bỏ tên khoá; có thể nói chủ đề nên học tiếp ("chủ đề nên tìm hiểu tiếp là …"). Bài bản đồ lộ trình (bài 0 của khoá) được nói về các bài **trong khoá này**.
4. Tham chiếu tới bài **trước trong cùng khoá** vẫn được, nhưng khi dùng lại một khái niệm thì nhắc lại định nghĩa của nó một hai câu ngay tại chỗ, để người học xem lẻ một video vẫn theo được.
5. Cẩn thận chữ "khoá": trong nhiều bài "khoá" còn là khoá chính/ngoại (cơ sở dữ liệu), khoá loại trừ (hệ điều hành), khoá mật mã. Chính sự trùng nghĩa này làm câu "ở khoá Hệ điều hành, khoá loại trừ…" khó nghe — thêm lý do bỏ tên khoá.
6. Công cụ kiểm: `PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/review/check_xref.py --course <KHOÁ>` liệt kê mọi lượt còn lại (bài và giáo án). Mục tiêu 0 lượt. Lượt dương tính giả (ví dụ "SEC" là Uỷ ban Chứng khoán Mỹ, "ACB" là tên ngân hàng) thì giữ và ghi vào báo cáo mục "Dương tính giả của check_xref".

## C. Cách sửa (bắt buộc)
- **Bài sinh từ mã/mẫu** — sửa đúng nguồn, không sửa tay bản sinh:
  - JVA, BNK: sửa `audit/<khoá>/src/lNN.py` rồi chạy `PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/<khoá>/gen.py LNN` (đọc docstring `gen.py` trước); JVA chạy lại `audit/jva/verify_jva.py`.
  - Khoá có `audit/<khoá>/src/*.tpl.yaml` khớp bài: sửa bài xong chạy `PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/review/sync_tpl_from_lesson.py <KHOÁ> --write` (đọc docstring trước) và kiểm mẫu đã nhận sửa.
  - INT, ACB: sửa thẳng `lessons/int|acb/*.yaml`; **không bao giờ** chạy `resources/job/generate_int_*.py`, `create_acb_lesson*.py` (ghi đè bản sửa).
- Sửa bằng công cụ **Edit** (không dùng bash/python/sed thay chuỗi: dấu `\` qua shell bị hỏng; trong chuỗi YAML nháy kép, `\t` của `\times`, `\text`, `\to`, `\theta` thành TAB — dùng nháy đơn hoặc `\\`). Sau khi sửa chạy `.venv/Scripts/python -B audit/review/scan_ctrl.py`; không được có lượt mới ở khoá của bạn (8 lượt `\tat` của JVA là cố ý).
- `say` là tiếng Việt nói được: không thêm từ ngoại mới ngoài những từ bài/khoá đã đọc (xem `tools/registry/lexicon_vi.<KHOÁ>.yaml`); số viết như cách tệp đang viết trong `say` (ví dụ "0 phẩy 775"). Màn hình và lời đọc phải khớp. Câu ≤ 7 từ dễ bị TTS/ASR đọc hỏng — tránh câu mới quá ngắn.
- Mỗi bước `show` có `focus` khớp số câu của `say` (lint kiểm) — thêm/bớt câu thì sửa `focus`.
- Đổi số/logic → sửa `checks:` của cảnh và chạy bộ kiểm của khoá (`audit/<khoá>/verify_<khoá>.py` hoặc `verify_parts/`); nếu bộ kiểm mã hoá logic cũ thì sửa kèm chú thích có nguồn, **không bao giờ sửa kỳ vọng chỉ để qua**. Thêm ví dụ số mới → thêm `checks` cho nó.
- **Tệp dùng chung**: KHÔNG sửa `tools/lv.py`, `audit/dms/asr_review_dms.py`, `audit/verify_plan_curricula.py`, `audit/review/check_xref.py`. Cần hàm mới trong `tools/checklib.py` thì chèn bằng một lệnh Edit nhỏ (tiền tố tên khoá, không viết lại tệp), rồi chạy `.venv/Scripts/python -B audit/check_checklib_dupes.py`. Nếu `rec()` của khoá trong `verify_plan_curricula.py` cần đổi vì bài đổi số, ghi vào báo cáo cho người điều phối.
- `asr_reviewed`: xoá mục có `sentence` không còn trong `say` nào (lint E30 báo; có thể dùng `audit/review/prune_stale_asr.py`, đọc docstring trước).
- Không nhắc số bài của bài **sau** giữa bài (lint E22); bài cuối không nói "bài sau" (E37); không viết "<mã khoá> bài N" (E22 đọc nhầm).
- **Giáo án** `curriculum/<khoá>.yaml`: mục của mỗi bài phải khớp bài sau khi sửa (`title` = tiêu đề bài bỏ tiền tố "Bài N —" như các mục khác đang làm, `objectives`, `example`, `fix`), và không nhắc khoá khác (B.1). Sau đó chạy `.venv/Scripts/python -B tools/lv.py curriculum curriculum/<khoá>.yaml` → 0 lỗi.
- Sau mỗi bài sửa: `.venv/Scripts/python -B tools/lv.py lint <tệp>` → 0 FAIL, 0 WARN; `.venv/Scripts/python -B tools/lv.py render <tệp>` → 0 vấn đề (rút gọn chữ hoặc `clear: true` ở step nếu tràn khung). **Không chạy `build`, `tts`, `asr`** (người điều phối dựng lại tuần tự). Chạy `render` tuần tự, không song song.
- Cuối cùng chạy bộ kiểm của khoá, `check_xref.py --course <KHOÁ>`, `lv.py curriculum`.
- Tệp tạm: chỉ trong `C:\Users\AI_WOR~1\AppData\Local\Temp\claude\740fb36319f596fa\861253fe-19f6-4644-af8e-fb72e5360827\scratchpad\review_c\<KHOÁ>\`. Chỉ chạm tệp của khoá được giao (và mục giáo án của nó). Không chạm khoá của tác tử khác, không chạy lệnh git đổi index.

## D. Báo cáo ghi ra đĩa (bắt buộc — người điều phối đếm lại bằng công cụ so với ảnh chụp trước đợt)
Mỗi khoá một tệp `audit/review/full_review_c/<KHOÁ>.md` (nếu bạn chỉ được giao một phần khoá, tệp `<KHOÁ>_<từ>-<đến>.md`, ví dụ `CS115_L00-L15.md`):
1. Dòng đầu: `# <KHOÁ> — đã đọc N/N bài`.
2. Bảng **một dòng cho MỌI bài** (kể cả bài không lỗi), đúng 6 cột:
   `| Bài | Kết luận | Lỗi nội dung đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Độc lập (tham chiếu khoá khác đã thay bằng gì) | Nguồn | lint / render |`
   Cột Kết luận chỉ dùng một trong: `đã sửa`, `không phát hiện lỗi`. Bài đã sửa ghi kết quả lint (`lint: 0 FAIL, 0 WARN, …`) và render (`… (0 vấn đề)`) sau sửa.
3. Mục "Không sửa và vì sao" (điều nghi ngờ nhưng không đủ căn cứ), mục "Dương tính giả của check_xref".
4. Dòng kết quả cuối của bộ kiểm khoá, của `check_xref.py --course`, và của `lv.py curriculum`.
Trả lời người điều phối ≤ 300 từ: số bài đã đọc/đã sửa, số mục MUST/SHOULD, số lượt check_xref trước → sau, đường dẫn báo cáo, điều cần người điều phối làm (nếu có).
