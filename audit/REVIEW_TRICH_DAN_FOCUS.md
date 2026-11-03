# Rà soát toàn khoá: trích dẫn tự hiểu được + focus theo câu (2026-10-27)

Yêu cầu người dùng: người học CHỈ có video. Câu kiểu “Tài liệu gốc viết giảm dần về 0, cách viết đó chưa chính xác” (L00 phút 6:49) trỏ tới thứ họ không có. Ngoài ra, mỗi câu phải cho người xem biết lời đang nói tới chỗ nào trên bảng.

## 1. Trích dẫn mơ hồ

- **Phát hiện (OBSERVED):** 312 chỗ ở 33 bài, quét `title`/`objectives`/`show`/`say`. Các dạng gặp:
  - “tài liệu (gốc/môn học)”;
  - “tài liệu dòng NNN”;
  - “slide môn học”;
  - “bài giảng của môn học”;
  - “bài báo gốc”;
  - mã nguồn ML24/PR25.
- **Cách sửa:**
  - Lỗi của nguồn → “Hay gặp cách nói … Nói vậy chưa chính xác, vì …”.
  - Khác ký hiệu → “Nhiều sách viết …”.
  - Nguồn cần nêu → gọi đủ tên:
    - Adam: Kingma & Ba, 2015;
    - Adadelta: Zeiler, 2012;
    - NMF: Lee & Seung, 1999.
  - Số dòng nguồn chỉ giữ ở `source:` và `fix`.
- **Kiểm (OBSERVED, 2026-10-26T19:14Z):** quét lại còn 0 chỗ. Lint E29 chặn tái diễn; `tests/test_lint.py` có ca thử.
- **Sửa kéo theo:** 3 câu viết lại thành “bài 17 sẽ…”, “bài 20” nằm giữa phần giảng. Lint E22 bắt, đã nói lại bằng lời thường. 4 câu mới bị ASR gắn cờ; cả 4 là tên chữ cái hoặc tên riêng đã biết, đã ghi `asr_reviewed`.
- **Hướng dẫn sai trong skill:** dòng E27 ở `production.md` từng khuyên ghi “tài liệu dòng …” lên màn hình. Dòng này đã được sửa.

## 2. Focus theo câu

- **Cơ chế mới:**
  - `focus:` của step: mỗi câu một mục.
  - `player.html` viền cam phần đang được nói tới và làm mờ các phần khác trong khối.
  - Cú pháp: `2` là phần 2; `"2.3"` là dòng 3 của bảng ở phần 2; `"B1"` là khối 1.
- **Áp dụng:** 213 step ở 44 bài, tức mọi step có ≥3 câu nói về một khối ≥3 phần. Mỗi mục được chọn sau khi đọc chữ của từng phần và từng câu. Tổng cộng 708 trên 3683 khung có focus.
- **Kiểm:**
  - Lint E31: chỉ số focus và số mục khớp số câu.
  - Lint E32: cảnh báo step dày chữ mà thiếu focus.
  - Render FAIL nếu trình duyệt không tìm thấy phần được trỏ. Kết quả: 0 vấn đề ở 44 bài.
- **Xem bằng mắt:** 77 khung lấy mẫu (contact sheet) cùng các khung L00 #61/#63/#82 và L01 #140/#149. Tìm và sửa 3 lỗi:
  - viền không hiện trên `$$…$$`;
  - viền vỡ trên công thức nội tuyến cao;
  - L14 trỏ vào σ² quá nhỏ.

## 3. Kết quả (OBSERVED)

| Kiểm | Kết quả |
|---|---|
| lint 44 bài | 0 FAIL, 0 WARN |
| `tests/test_lint.py` | 0 FAIL (thêm E29–E32) |
| verify | 44/44 PASS, 0 bài cũ so với spec/tts |
| ASR | 3683 câu, 152 gắn cờ, 0 chưa xem xét |
| curriculum | 44 bài, 0 lỗi |
| thời lượng | 5,78 giờ |

## 4. Còn NOT_VERIFIED

- Cảm nhận thật của người học về độ rõ của focus.
- Phát âm mới chỉ được ASR kiểm, chưa có người nghe. Các nút thắt cũ vẫn mở:
  - softmax;
  - Lagrange;
  - Bayes;
  - Adagrad/RMSprop;
  - Nesterov.
