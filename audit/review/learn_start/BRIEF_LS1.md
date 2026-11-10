# Đọc kỹ trọn bài trước khi người dùng bắt đầu học (đợt LS1, 2026-11-10)

Người dùng sắp **bắt đầu học thật** theo các bài bạn được giao. Họ là người **mất gốc, học từ con số 0**, chỉ có video và giáo án, không có sách hay khoá khác. Mỗi video phải tự đứng được.
Nhiệm vụ của bạn: đọc **trọn từng bài** như một chuyên gia môn học khó tính, tìm mọi lỗi mà người học sẽ vấp phải. Bạn không sửa; người điều phối sẽ kiểm lại và sửa theo đề xuất của bạn.

## Bạn được phép làm gì
- **CHỈ ĐỌC.** Không sửa tệp nào trong kho. Không chạy `build`, `tts`, `asr`, `render`, không chạy git.
- **Không mở** `audit/review/full_review_*/*`, `audit/review/sample_*/part_*`, `audit/review/screen_code/report_*` (báo cáo của người đã sửa; đọc chúng làm bạn mất độc lập).
- Tệp tạm, ví dụ script Python tính lại số: chỉ đặt trong thư mục scratchpad ghi trong lời nhắn.
- Python: `PYTHONIOENCODING=utf-8 .venv/Scripts/python -B <tệp>.py`. **Luôn viết script ra tệp rồi chạy**; đừng dùng heredoc với `< /dev/null`, vì Python sẽ treo.
- Có sẵn trên máy: Python 3.13, sqlite3 (mô-đun Python), JDK 22 (`javac`, `java`), node, go. Không có trình biên dịch C.

## Đọc gì cho mỗi bài
1. **Đặc tả** `lessons/<khoá>/<bài>.yaml`, đọc trọn:
   - mọi `title`, `objectives`;
   - `show` (HTML màn hình, cả chữ trong SVG);
   - `say` (lời đọc);
   - `checks`;
   - quiz (câu, phương án, đáp án, lời giải).
2. **Mục của bài trong giáo án** `curriculum/<khoá>.yaml` (`title`, `objectives`, `example`, `fix`). Nếu có, đọc cả `audit/<khoá>/sources_*.md`.
3. **Video đã dựng** `out/<KHOÁ viết hoa>/<Lxx>/`:
   - `chapters.txt` và `<Lxx>.srt` (lời đọc thật);
   - ít nhất **4 khung hình** trong `frames/*.png`, mở bằng công cụ Read: phần mở đầu, hình cơ chế hoặc ví dụ, quiz, tổng kết. Cộng dồn `duration` trong `_frames.txt` để biết khung nào ứng với thời điểm nào.
   - Xem chữ có tràn, đè nhau hay bị cắt không, và hình có khớp lời đọc không.

## A. Chuẩn xác
- **MUST**:
  - kiến thức sai hoặc lỗi thời: định nghĩa, định lý, công thức, hành vi hệ thống / thư viện / giao thức / quy chuẩn;
  - ví dụ tự mâu thuẫn giữa các cảnh;
  - màn hình nói khác lời đọc ở một điểm kiến thức;
  - đáp án quiz hoặc lời giải sai;
  - số tính sai;
  - giáo án hứa điều bài không dạy, hoặc nói khác bài;
  - mã trên màn hình không chạy, hoặc cho kết quả khác điều bài nói.
- **SHOULD**:
  - khẳng định tuyệt đối sai ("luôn", "100%");
  - thiếu điều kiện áp dụng;
  - số thực tế không nguồn trình bày như sự thật;
  - nhãn hình sai;
  - màn hình lệch lời đọc ở chi tiết nhỏ;
  - chữ trên khung hình bị tràn, đè hoặc cắt.
- **Tự tính lại bằng Python mọi con số** hiện trên màn hình hoặc được đọc ra, đúng tới số chữ số được ghi. Chạy thử mọi đoạn mã trên màn hình chạy được. Người điều phối đã có một cổng chạy nguyên văn mọi khối mã; bạn vẫn đọc mã, vì cổng không bắt được mã đúng cú pháp nhưng sai ý.
- Chỉ báo lỗi bạn chứng minh được: trích nguyên chữ, lý do, và phép tính hoặc nguồn có thẩm quyền (tài liệu chính thức, RFC, JLS, sách chuẩn, văn bản pháp quy). Không báo chuyện văn phong.

## B. Kẹt với người mất gốc (BLOCK)
Đặt mình vào vị trí người chưa học gì về chủ đề, chỉ xem video này theo đúng thứ tự lộ trình. Lộ trình gồm các bài trước của cùng khoá và các khoá đứng trước trong lời nhắn.
- **BLOCK-TERM**: một thuật ngữ, ký hiệu hay chữ viết tắt được **dùng trước khi được giảng**, hoặc không bao giờ được giảng, trong cả bài này lẫn các bài trước trên lộ trình. Một từ đã giảng ở bài trước của cùng khoá thì không tính, nhưng ghi "nên nhắc lại một câu" nếu bài dùng nó như trung tâm.
  Ghi: từ, chỗ xuất hiện đầu tiên (cảnh, step), và **một câu định nghĩa đề xuất bằng lời thường**, đúng kiến thức.
- **BLOCK-STEP**: một bước suy luận hay biến đổi nhảy cóc, mà người mất gốc không tự nối được. Ghi bước còn thiếu.
- **BLOCK-QUIZ**: quiz dùng điều bài chưa dạy, hoặc đáp án không suy ra được từ bài.
Không báo những từ người Việt phổ thông đều hiểu.

## Cách ghi đề xuất sửa (để người điều phối áp được ngay)
Mỗi phát hiện ghi:
- tệp;
- vị trí: id cảnh, số thứ tự step tính từ 0, và trường (`show`, `say`, quiz…);
- **chuỗi cũ nguyên văn**, đủ dài để chỉ khớp một chỗ trong tệp;
- **chuỗi mới** đề xuất.

Ràng buộc khi đề xuất:
- Khi sửa `say` thì sửa cả `show` tương ứng, và ngược lại, để màn hình và lời đọc khớp.
- `say` phải là tiếng Việt nói được:
  - không thêm từ ngoại mới ngoài những từ bài đã đọc; xem `tools/registry/lexicon_vi.<KHOÁ>.yaml` nếu có;
  - số viết như cách tệp đang viết trong `say`;
  - câu mới dài hơn 7 từ.
- Không đề xuất thêm câu vào giữa một step có `focus` dạng danh sách mà không nói rõ cần thêm một mục `focus`. Cách an toàn nhất là thêm một mệnh đề vào câu đã có.

## Trả lời người điều phối (KHÔNG ghi tệp; mọi thứ nằm trong câu trả lời cuối)
Câu trả lời cuối gồm đủ các phần sau, theo đúng thứ tự:
1. Dòng đầu: `ĐÃ ĐỌC K/K bài: <danh sách id>`.
2. **Bảng phát hiện**, một dòng mỗi phát hiện:
   `| Bài | Mức (MUST/SHOULD/BLOCK-TERM/BLOCK-STEP/BLOCK-QUIZ) | Tệp · cảnh · step · trường | Chuỗi cũ nguyên văn | Vì sao + bằng chứng | Chuỗi mới đề xuất | Tin cậy (CONFIRMED/PLAUSIBLE) |`
   Bài không có phát hiện: một dòng `| <Bài> | — | | | không phát hiện | | |`.
3. **Bảng từng bài**, một dòng cho MỌI bài:
   `| Bài | Phút (từ chapters/srt) | Số đã tính lại / khớp | Mã đã chạy | Khung đã xem (tên png) | Mất gốc theo được? (ĐƯỢC / KẸT ở …) |`
4. Tối đa 6 gạch đầu dòng nhận xét chung.

Không giới hạn độ dài câu trả lời, nhưng đừng chép lại nội dung bài.
