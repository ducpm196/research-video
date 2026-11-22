# Đọc mẫu độc lập Mẫu G — kiểm toán chốt toàn kho 777 bài (hạt giống `20261201`)

Mục đích: Kiểm chứng độc lập bản đặc tả + video đã dựng (`out/<KHOÁ>/<Lxx>/`) trên **50 bài đại diện (mỗi khoá 1 bài, loại trừ 164 bài đã vào Mẫu C–F)**, chia cho 4 tác tử chỉ đọc (~12–13 bài/tác tử).

## Quy định bắt buộc (CHỈ ĐỌC)
- **KHÔNG sửa, KHÔNG tạo tệp nào trong `D:\research-video`** (tệp tính toán tạm nếu cần chỉ viết trong `/tmp` hoặc chạy inline `python -c ...`).
- **TUYỆT ĐỐI KHÔNG chạy**: `lab_gate.py`, `bash.exe`, `audit/layout_scan.py`, `build`, `tts`, `asr`, `render`, `gen.py`, `git`, `docker`, `audit_all.py`.
- Đọc trực tiếp từng bài:
  1. Đặc tả `lessons/<khoá>/<bài>.yaml` (kiểm tra `sha16` khớp danh sách giao việc), mọi `title`, `objectives`, `show` (HTML + SVG), `say`, `checks`, `quiz` (câu, phương án, đáp án, lời giải) và mục `practice`.
  2. Mục tương ứng trong `curriculum/<khoá>.yaml` và `audit/<khoá>/sources*.md` (nếu có).
  3. Sản phẩm video đã dựng trong `out/<KHOÁ>/<Lxx>/`:
     - `asr_report.md` (xác nhận `chưa xem xét 0`), `<Lxx>.srt`, `chapters.txt`
     - Mở bằng `read_file` **ít nhất 5 khung hình** `frames/*.png` (mở đầu, cơ chế/ví dụ, bảng đọc mã/`practice`, quiz, tổng kết) để kiểm lỗi hiển thị/tràn/đè chữ và độ khớp màn hình với lời đọc.
- Tự tính lại bằng Python (`D:/research-video/.venv/Scripts/python.exe -B -c ...`) mọi con số trên màn hình và trong lời đọc; kiểm tra xem có câu diễn đạt khó hiểu kiểu so sánh mập mờ (`"càng ... càng ..."`, thiếu vế nguyên nhân/so sánh).

## Tiêu chí chấm
- **Chuẩn xác (`MUST` / `SHOULD`)**:
  - **MUST**: kiến thức sai/lỗi thời; ví dụ tự mâu thuẫn; màn hình nói khác lời đọc ở điểm kiến thức; quiz/đáp án/số tính sai; mục tiêu giáo án hứa điều bài không dạy; mã trên màn hình sai cú pháp/sai kết quả; bài nhắc khoá khác thay vì giảng tại chỗ. Mục tiêu Mẫu G: **`MUST = 0`**.
  - **SHOULD**: khẳng định tuyệt đối thiếu điều kiện, chi tiết lệch nhỏ, câu nói mập mờ khó hiểu.
- **Độ sâu sư phạm (`0/1/2` điểm)**:
  - **P1 Nền** (`mục tiêu ≥ 80% đạt điểm 2`): mọi khái niệm, thuật ngữ, ký hiệu, chữ viết tắt được giảng tại chỗ bằng lời thường ở lần đầu xuất hiện (kể cả trong lỗi hay gặp/quiz).
  - **P2–P7** (chấm như chuẩn AF2: từng bước số, trực quan cơ chế & khung hình sạch, ví dụ làm tay, quiz hiểu, chuyên sâu vì sao/giới hạn, giáo án khớp bài). Kết luận Mất gốc: `ĐỦ` / `GẦN` / `CHƯA`.
  - **P8 Thực nghiệm** (`mục tiêu = 100% đạt điểm 2`): có bài Tự làm (`practice` + `labs/<KHOÁ>/<Lxx>/`) với lệnh/việc cụ thể + kết quả mong đợi để tự đối chiếu.
  - **P9 Quy mô/thời gian** (`mục tiêu ≥ 80% đạt điểm 2`): có số liệu ở ≥ 2 mức quy mô hoặc mốc thời gian + đánh đổi.

## Định dạng báo cáo trả về trong tin nhắn cuối (KHÔNG ghi tệp vào repo)
1. Dòng đầu: `# Mẫu G — phần <N>: đã đọc K/K bài`
2. Bảng chuẩn xác: `| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy (CONFIRMED/PLAUSIBLE) |` (bài sạch ghi `— | | | không phát hiện lỗi | | |`).
3. Bảng độ sâu (1 dòng/bài): `| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | Mất gốc | P8 | P9 | Cần biết trước / Chỗ kẹt |`
4. Tóm tắt thống kê phần `<N>`: số bài `MUST=0`, đếm `P1=2`, `P8=2`, `P9=2`, `ĐỦ/GẦN/CHƯA`, số khung hình đã mở, số phép tính/mã đã kiểm lại.
