# Đọc mẫu độc lập đợt E — chuẩn xác + đủ sâu cho người mất gốc (2026-11-10)

Người dùng hỏi: *"rà soát đánh giá chất lượng video và giáo án đủ chuyên sâu cho người mới và người mất gốc không"* và *"đảm bảo đủ chuẩn xác, ít sai sót không"*.

Người học: **mất gốc, học từ con số 0**, chỉ có video (không có sách, không có khoá khác). Mỗi video phải tự đứng được.

Mẫu: mỗi khoá một bài, `random.Random(20261111).choice(...)` trên `sorted(lessons/<khoá>/L*.yaml)`, bỏ các bài của mẫu C (`audit/review/sample_c/REPORT.md`) và mẫu D (`audit/review/sample_d/REPORT.md`).

## Bạn được phép làm gì
- **CHỈ ĐỌC.** Không sửa bất kỳ tệp nào trong kho, ngoài tệp báo cáo của bạn `audit/review/sample_e/part_<N>.md`. Không chạy `build`, `tts`, `asr`, `render`, không chạy lệnh git.
- **Không mở** `audit/review/full_review_*/*`, `audit/review/sample_c/part_*`, `audit/review/sample_d/part_*` (báo cáo của người đã sửa; đọc chúng sẽ làm bạn mất độc lập).
- Tệp tạm (script Python tính lại số): chỉ trong thư mục scratchpad được giao trong lời nhắn.
- Python: `PYTHONIOENCODING=utf-8 .venv/Scripts/python -B ...` (hoặc `python`).

## Đọc gì cho mỗi bài
1. Đặc tả `lessons/<khoá>/<bài>.yaml`: mọi `title`, `objectives`, `show` (HTML màn hình, cả chữ trong SVG), `say` (lời đọc), `checks`, quiz (câu, phương án, đáp án, lời giải).
2. Mục của bài trong `curriculum/<khoá>.yaml` (`title`, `objectives`, `example`, `fix`). Nếu có, đọc thêm `audit/<khoá>/sources_*.md`.
3. **Video đã dựng**: `out/<KHOÁ viết hoa>/<Lxx>/`. Mở `chapters.txt` (mục lục có mốc thời gian) và `<Lxx>.srt` (lời đọc thật). Mở **ít nhất 5 khung hình** trong `frames/*.png` bằng công cụ Read. Chọn: 1 khung phần mở đầu, 2 khung phần ví dụ hoặc hình cơ chế, 1 khung phần quiz, 1 khung phần tổng kết. Muốn biết khung nào ứng với thời điểm nào thì cộng dồn `duration` trong `_frames.txt`. Kiểm tra: chữ có tràn, đè nhau hay bị cắt không; hình có khớp lời đọc không; cỡ chữ có đọc được không.

## Phần A — Chuẩn xác (giữ tiêu chí của mẫu C/D để so được)
- **MUST**: kiến thức sai hoặc lỗi thời (định nghĩa, định lý, công thức, hành vi hệ thống/thư viện/giao thức, quy chuẩn); ví dụ tự mâu thuẫn giữa các cảnh; màn hình nói khác lời đọc ở một điểm kiến thức; đáp án quiz hoặc lời giải sai; số tính sai; giáo án hứa điều bài không dạy; mã trên màn hình không chạy hoặc cho kết quả khác điều bài nói.
- **SHOULD**: khẳng định tuyệt đối sai ("luôn", "100%"); thiếu điều kiện áp dụng; số thực tế không có nguồn; nhãn hình sai; màn hình lệch lời đọc ở chi tiết nhỏ.
- **Tự tính lại bằng Python mọi con số** hiện trên màn hình hoặc được đọc ra, đúng tới số chữ số được ghi. Chạy thử mọi đoạn mã ngắn trên màn hình nếu chạy được (Python, SQL bằng sqlite3; ngôn ngữ khác thì đọc kỹ).
- Bài sự cố có thật (CAS, cảnh có `stage`): năm, con số, sự kiện phải khớp nguồn trong `audit/<khoá>/sources_*.md` hoặc `source`. Không kiểm được thì ghi "chưa kiểm được nguồn", đừng kết luận sai.
- Chỉ báo lỗi bạn chỉ ra được bằng chứng (trích nguyên chữ + lý do + nguồn có thẩm quyền hoặc phép tính). Không báo chuyện văn phong.

## Phần B — Đủ sâu cho người mất gốc (tiêu chí mới, chấm 0/1/2 từng mục)
Đặt mình vào vị trí một người **chưa học gì về chủ đề**, chỉ xem video này.
| Mã | Tiêu chí | 2 = đạt | 1 = một phần | 0 = không |
|---|---|---|---|---|
| P1 Nền | Mọi khái niệm, thuật ngữ, ký hiệu, chữ viết tắt bài dùng đều được giảng tại chỗ bằng lời thường ở lần đầu xuất hiện | không còn từ nào bị kẹt | 1–2 từ chưa giảng | ≥3 từ, hoặc một khái niệm then chốt chưa giảng |
| P2 Từng bước | Mỗi bước suy luận/biến đổi có lý do ("vì…") và được thử bằng số; không nhảy cóc | đủ | có 1 chỗ nhảy | nhiều chỗ nhảy |
| P3 Trực quan | Hình, bảng, sơ đồ cho thấy **cơ chế** (không chỉ trang trí) và khớp lời đọc; khung hình đọc được, không đè chữ | đạt | hình có nhưng chỉ minh hoạ, hoặc có 1 lỗi hiển thị nhỏ | không có hình cơ chế, hoặc lỗi hiển thị làm khó đọc |
| P4 Làm tay | Có ít nhất một ví dụ trọn vẹn mà người học tự làm lại được bằng giấy bút, có số cụ thể | đạt | ví dụ có nhưng thiếu bước | không có |
| P5 Tự kiểm | Quiz kiểm **hiểu** (không chỉ nhớ chữ), có dừng để nghĩ, lời giải từng bước | đạt | quiz nhớ chữ, hoặc lời giải một dòng | không có |
| P6 Chuyên sâu | Vượt qua định nghĩa: vì sao đúng, giới hạn hoặc điều kiện, lỗi thường gặp, cách người làm nghề làm thật (tình huống có số liệu) | đạt | có một phần | chỉ định nghĩa |
| P7 Giáo án | Mục giáo án khớp bài, mục tiêu đo được, và bài đạt các mục tiêu đó | đạt | lệch nhỏ | lệch lớn |

Kết luận mỗi bài (cột "Mất gốc"): **ĐỦ** (tổng ≥ 12 và không mục nào 0), **GẦN** (tổng 9–11, hoặc ≥12 mà có một mục 0), **CHƯA** (tổng ≤ 8).
Với mỗi điểm 0 hoặc 1, ghi ngắn **chỗ cụ thể** (cảnh/step, trích chữ, hoặc tên tệp khung hình).

## Báo cáo `audit/review/sample_e/part_<N>.md`
1. Dòng đầu: `# Mẫu E — phần <N>: đã đọc K/K bài`.
2. Bảng chuẩn xác, một dòng cho mỗi phát hiện: `| Bài | Mức (MUST/SHOULD) | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/nguồn) | Đề xuất sửa | Tin cậy (CONFIRMED/PLAUSIBLE) |`. Bài không có phát hiện: một dòng `| <Bài> | — | | | không phát hiện lỗi | | |`.
3. Bảng độ sâu, **một dòng cho MỌI bài**: `| Bài | Phút (từ chapters/srt) | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | Mất gốc | Chỗ thiếu chính |`.
4. Mục "Khung hình đã xem" (bài → tên tệp png) và "Mã đã chạy / số đã tính lại" (bao nhiêu số, bao nhiêu khớp).
5. Mục "Nhận xét chung": điểm mạnh, điểm yếu lặp lại giữa các bài (tối đa 8 gạch đầu dòng).

Trả lời người điều phối ≤ 250 từ: số bài, số MUST/SHOULD, phân bố ĐỦ/GẦN/CHƯA, 3 điểm yếu lặp lại nhiều nhất.
