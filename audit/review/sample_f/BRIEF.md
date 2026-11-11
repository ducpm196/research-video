# Đọc mẫu độc lập đợt F — video giáo án đã đủ chuẩn xác để học chưa (2026-11-11)

Người dùng hỏi: *"Đánh giá chất lượng video giáo án hiện tại đã đầy đủ chuẩn xác để học chưa"*.
Người học: **mất gốc, học từ con số 0**, chỉ có video. Mỗi video phải tự đứng được (không dựa vào khoá khác).

Mẫu: `audit/review/sample_f/sample_f.py` (hạt giống 20261112) — mỗi khoá một bài, chỉ lấy trong **448 bài chưa từng được đọc mẫu** (bỏ mẫu C/D/E và 119 bài đợt LS1 đã đọc trọn), cộng thêm một bài BNX thứ hai (khoá mới dựng 2026-11-11). Tiêu chí giữ nguyên mẫu E để so được.

## Bạn được phép làm gì
- **CHỈ ĐỌC.** Không sửa, không tạo tệp nào trong kho `D:\research-video`. Không chạy `build`, `tts`, `asr`, `render`, `gen.py`, lệnh git, docker.
- Có một phiên khác đang làm việc trên kho (khoá BNX). Ghi **sha256 16 ký tự đầu** của mỗi tệp YAML lúc bạn đọc (`python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()[:16])" <tệp>`); nếu khác giá trị trong danh sách giao việc, ghi rõ.
- **Không mở** `audit/review/full_review_*/*`, `audit/review/sample_*/part_*`, `audit/review/sample_*/REPORT.md`, `audit/review/learn_start/findings_*`, `audit/bnx/logs/*`, `audit/review/sample_f/*` ngoài BRIEF này (báo cáo của người đã sửa; đọc chúng làm bạn mất độc lập).
- Tệp tạm (script tính lại số): chỉ trong thư mục scratchpad được giao.
- Python: `PYTHONIOENCODING=utf-8 D:/research-video/.venv/Scripts/python -B ...`.

## Đọc gì cho mỗi bài
1. Đặc tả `lessons/<khoá>/<bài>.yaml`: mọi `title`, `objectives`, `show` (HTML màn hình, cả chữ trong SVG), `say` (lời đọc), `checks`, quiz (câu, phương án, đáp án, lời giải).
2. Mục của bài trong `curriculum/<khoá>.yaml` (`title`, `objectives`, `example`, `fix`). Nếu có, đọc thêm `audit/<khoá>/sources*.md`.
3. **Video đã dựng** `out/<KHOÁ>/<Lxx>/`: `chapters.txt`, `<Lxx>.srt` (lời đọc thật — so với `say`: thiếu câu, sai số?). Mở **ít nhất 5 khung hình** `frames/*.png` bằng công cụ Read: 1 mở đầu, 2 ví dụ/hình cơ chế, 1 quiz, 1 tổng kết (thời điểm: cộng dồn `duration` trong `_frames.txt`). Kiểm: chữ tràn, đè, bị cắt; hình khớp lời đọc; cỡ chữ đọc được.

## Phần A — Chuẩn xác
- **MUST**: kiến thức sai hoặc lỗi thời (định nghĩa, định lý, công thức, hành vi hệ thống/thư viện/giao thức, quy chuẩn, văn bản pháp lý); ví dụ tự mâu thuẫn giữa các cảnh; màn hình nói khác lời đọc ở một điểm kiến thức; đáp án quiz hoặc lời giải sai; số tính sai; giáo án hứa điều bài không dạy; mã trên màn hình không chạy hoặc cho kết quả khác điều bài nói; bài nhắc khoá khác thay vì giảng lại.
- **SHOULD**: khẳng định tuyệt đối sai ("luôn", "100%"); thiếu điều kiện áp dụng; số thực tế không có nguồn; nhãn hình sai; màn hình lệch lời đọc ở chi tiết nhỏ.
- **Tự tính lại bằng Python mọi con số** hiện trên màn hình hoặc được đọc ra, đúng tới số chữ số được ghi. Chạy thử mọi đoạn mã ngắn trên màn hình nếu chạy được (Python; SQL bằng sqlite3 nếu cú pháp hợp; ngôn ngữ khác thì đọc kỹ và ghi "chỉ đọc, không chạy").
- Bài có sự kiện/văn bản có thật: năm, số, sự kiện phải khớp nguồn trong `audit/<khoá>/sources*.md` hoặc trường `source`. Không kiểm được thì ghi "chưa kiểm được nguồn", đừng kết luận sai.
- Chỉ báo lỗi bạn chỉ ra được bằng chứng (trích nguyên chữ + lý do + nguồn có thẩm quyền hoặc phép tính). Không báo chuyện văn phong.

## Phần B — Đủ sâu cho người mất gốc (chấm 0/1/2)
| Mã | Tiêu chí | 2 = đạt | 1 = một phần | 0 = không |
|---|---|---|---|---|
| P1 Nền | Mọi khái niệm, thuật ngữ, ký hiệu, chữ viết tắt bài dùng đều được giảng tại chỗ bằng lời thường ở lần đầu xuất hiện | không còn từ nào bị kẹt | 1–2 từ chưa giảng | ≥3 từ, hoặc một khái niệm then chốt chưa giảng |
| P2 Từng bước | Mỗi bước suy luận/biến đổi có lý do và được thử bằng số; không nhảy cóc | đủ | 1 chỗ nhảy | nhiều chỗ nhảy |
| P3 Trực quan | Hình/bảng/sơ đồ cho thấy **cơ chế** và khớp lời đọc; khung hình đọc được, không đè chữ | đạt | chỉ minh hoạ, hoặc 1 lỗi hiển thị nhỏ | không có hình cơ chế, hoặc lỗi hiển thị làm khó đọc |
| P4 Làm tay | Ít nhất một ví dụ trọn vẹn tự làm lại được bằng giấy bút, có số cụ thể | đạt | thiếu bước | không có |
| P5 Tự kiểm | Quiz kiểm **hiểu**, có dừng để nghĩ, lời giải từng bước | đạt | nhớ chữ, hoặc lời giải một dòng | không có |
| P6 Chuyên sâu | Vì sao đúng, giới hạn/điều kiện, lỗi thường gặp, người làm nghề làm thật | đạt | một phần | chỉ định nghĩa |
| P7 Giáo án | Mục giáo án khớp bài, mục tiêu đo được, bài đạt mục tiêu | đạt | lệch nhỏ | lệch lớn |

Kết luận "Mất gốc": **ĐỦ** (tổng ≥ 12 và không mục nào 0), **GẦN** (9–11, hoặc ≥12 có một mục 0), **CHƯA** (≤ 8). Với mỗi điểm 0/1, ghi **chỗ cụ thể**.

## Báo cáo — trả về trong TIN NHẮN CUỐI (người điều phối sẽ ghi ra tệp; bạn không ghi tệp)
1. Dòng đầu: `# Mẫu F — phần <N>: đã đọc K/K bài`.
2. Bảng chuẩn xác: `| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy (CONFIRMED/PLAUSIBLE) |`. Bài không có phát hiện: `| <Bài> | — | | | không phát hiện lỗi | | |`.
3. Bảng độ sâu, một dòng cho MỌI bài: `| Bài | sha16 lúc đọc | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | Mất gốc | Chỗ thiếu chính |`.
4. "Khung hình đã xem" (bài → tên png) và "Mã đã chạy / số đã tính lại" (bao nhiêu, bao nhiêu khớp).
5. "Nhận xét chung" (≤ 8 gạch).
