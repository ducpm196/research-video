# Báo cáo hoàn thành loạt video CS112 — Phân tích & Thiết kế Thuật toán (25 bài)

- Thời điểm kiểm cuối: 2026-10-27T03:42Z — verify CS112 25/25 PASS, CS115 44/44 PASS, lint 0 FAIL cả 69 bài, tests 0 FAIL, ASR 0 câu chưa xem xét.
- Trạng thái: **DONE** cho phần máy kiểm được. Các mục ở §5 vẫn NOT_VERIFIED.
- Nhãn: OBSERVED = máy chạy trong phiên này; INFERRED = suy luận; NOT_VERIFIED = chưa kiểm được.

## 1. Từng bài (OBSERVED)

Video: `out/CS112/<id>/<id>.mp4`, phụ đề `<id>.srt`, chương `chapters.txt`, bản duyệt `preview.html`, báo cáo nghe lại `asr_report.md`.

| bài | tiêu đề | thời lượng | verify | ASR: số câu · độ khớp TB · gắn cờ (đã xem xét) |
|---|---|---|---|---|
| L00 | Đếm số bước của thuật toán: số lần so sánh, làm tròn lên/xuống, lôgarit và các tổng Sigma | 12:10 | PASS | 122 · 0.968 · 5 (5) |
| L01 | Ký hiệu tiệm cận O, Ω, Θ (và o, ω): định nghĩa chặt và phương pháp giới hạn | 8:54 | PASS | 83 · 0.952 · 8 (8) |
| L02 | Xếp hạng tốc độ tăng của các hàm: từ log n đến n! và bẫy đổi cơ số mũ | 7:35 | PASS | 67 · 0.935 · 3 (3) |
| L03 | Mảng, mảng động & danh sách liên kết: địa chỉ ô nhớ và chi phí khấu hao | 8:15 | PASS | 77 · 0.952 · 9 (9) |
| L04 | Ngăn xếp & hàng đợi: vào sau ra trước, vào trước ra trước, và ngăn xếp lời gọi hàm | 7:08 | PASS | 75 · 0.951 · 3 (3) |
| L05 | Cây nhị phân, cây tìm kiếm nhị phân & cây AVL tự cân bằng | 7:42 | PASS | 67 · 0.972 · 4 (4) |
| L06 | Bảng băm & đống nhị phân (hàng đợi ưu tiên): vì sao dựng đống chỉ tốn Θ(n) | 8:11 | PASS | 71 · 0.940 · 16 (16) |
| L07 | Đồ thị: ma trận kề, danh sách kề, duyệt theo chiều rộng (BFS) và chiều sâu (DFS) | 6:12 | PASS | 62 · 0.942 · 12 (12) |
| L08 | Hệ thức truy hồi & phương pháp thế ngược: bài toán Tháp Hà Nội | 6:30 | PASS | 60 · 0.968 · 0 (0) |
| L09 | Hàm sinh: giải hệ thức truy hồi bằng chuỗi lũy thừa | 5:26 | PASS | 49 · 0.979 · 1 (1) |
| L10 | Đếm đúng số lời gọi đệ quy & chứng minh quy nạp có phần dư | 8:30 | PASS | 78 · 0.965 · 1 (1) |
| L11 | Đổi biến số: giải T(n) = √n · T(√n) + n | 6:03 | PASS | 50 · 0.968 · 1 (1) |
| L12 | Chia để trị & định lý thợ (Master theorem) | 8:29 | PASS | 73 · 0.948 · 9 (9) |
| L13 | Giảm để trị & biến đổi để trị: sắp xếp chèn, tìm kiếm nhị phân, sắp xếp trước | 6:39 | PASS | 58 · 0.952 · 9 (9) |
| L14 | Quay lui: cây trạng thái và bước trả lại đánh dấu | 5:16 | PASS | 51 · 0.964 · 1 (1) |
| L15 | Nhánh cận: bài toán người du lịch với ma trận rút gọn | 5:38 | PASS | 50 · 0.962 · 1 (1) |
| L16 | Tham lam (1): bài toán cái túi phân số | 5:30 | PASS | 52 · 0.955 · 1 (1) |
| L17 | Tham lam (2): xếp lịch hội trường — chọn hoạt động kết thúc sớm nhất | 5:06 | PASS | 48 · 0.985 · 1 (1) |
| L18 | Bản chất quy hoạch động: bài toán con gối nhau, ghi nhớ từ trên xuống và lập bảng từ dưới lên | 5:24 | PASS | 57 · 0.962 · 2 (2) |
| L19 | Quy hoạch động theo đoạn: đặt dấu ngoặc cho biểu thức và nhân chuỗi ma trận | 6:32 | PASS | 55 · 0.944 · 8 (8) |
| L20 | Quy hoạch động kinh điển: dãy con tăng dài nhất và xâu con chung dài nhất | 5:20 | PASS | 47 · 0.938 · 8 (8) |
| L21 | Quy hoạch tuyến tính hai biến: miền chấp nhận được và nghiệm tại đỉnh | 5:07 | PASS | 45 · 0.968 · 2 (2) |
| L22 | Thuật toán đơn hình: đi từ đỉnh này sang đỉnh tốt hơn | 5:45 | PASS | 51 · 0.962 · 1 (1) |
| L23 | Bài tập lớn: so sánh thuật toán có đo đạc, ghi minh bạch phần việc của AI | 6:57 | PASS | 67 · 0.963 · 1 (1) |
| L24 | Tổng ôn: bản đồ các dạng bài và những bẫy toán học đã gặp | 6:19 | PASS | 62 · 0.931 · 2 (2) |

Tổng thời lượng: 170.7 phút

ASR: mô hình small nghe mọi câu, medium nghe lại mọi câu. Một câu bị gắn cờ khi cả hai mô hình đều khớp dưới 0,8, hoặc có từ rủi ro mà cả hai đều nghe khác. Mọi câu bị gắn cờ đều có lý do trong trường `asr_reviewed` của bài; số câu gắn cờ chưa xem xét là 0 ở cả 25 bài.

## 2. Kiểm tra bằng máy (OBSERVED)

| Kiểm tra | Kết quả |
|---|---|
| `lv.py lint` 25 bài CS112 | 0 FAIL, 0 WARN mỗi bài |
| `lv.py verify` 25 bài CS112 | 25/25 PASS (thời lượng khớp dòng thời gian; có tiếng và hình) |
| `lv.py curriculum curriculum/cs112.yaml` | 25 bài, 25 đặc tả, 0 lỗi |
| `tests/test_lint.py` | 0 FAIL (gồm các test tách khoá CS115/CS112) |
| `audit/cs112/verify_cs112.py` (rà soát bản thảo) | 32 PASS · 15 FIX · 0 FAIL |
| `audit/cs112/mutate_checks.py` (đổi số kỳ vọng thì check phải hỏng) | 0 FAIL trên L00–L24 |
| CS115 sau mọi thay đổi | lint 0 FAIL; verify 44/44 PASS; curriculum 44 bài, 0 lỗi; `spec_sha`/`tts_sha`/số khung giống bản chụp trước thay đổi |

## 3. Xem bằng mắt (SKILL Bước 6)

Danh sách khung theo `audit/cs112/frames_to_check.py`. Đã mở trực tiếp hoặc qua ảnh ghép 2×2 (`audit/cs112/contact_sheet.py`):
L00 (0, 26, 41, 80, 86, 110, 113), L01 (25, 42), L02 (20, 30, 42), L05 (6, 34, 38), L06 (39), L07 (9), L10 (16, 22, 32, 36), L13 (14–17), L15 (0, 8, 15, 19, 22, 36, 39, 49), L16 (0, 2, 11, 16, 24, 38, 51), L17 (1, 9, 14, 18, 22), L18 (0, 12, 17, 19, 25, 28, 42, 49, 56), L21 (3, 10, 14, 16), L22 (9, 19, 22, 37), L23 (0, 23–26, 40, 66), L24 (4, 9, 14, 20), L03 (11, 26, 32, 35, 42, 43, 48, 62), L04 (0, 13, 30, 33, 36, 40, 57, 74), L08 (1, 14, 17, 26), L09 (17, 23, 37, 48), L11 (20, 24, 35, 49), L12 (4, 23, 32, 34, 39, 42, 57, 72), L14 (12, 18, 20, 37), L19 (13, 18, 20, 41), L20 (12, 20, 32, 46).

Lỗi thấy bằng mắt và đã sửa:
- L05 khung 34: nhãn hệ số cân bằng đè lên cạnh nối với nút cha. Đã đặt nhãn sang ngang (`treesvg.py`).
- L01: nhãn SVG. L02: chữ trong bảng. L00: phần tổng kết.
- L23: tiêu đề bài dài làm dòng đầu trang xuống hai dòng, đè tiêu đề phân cảnh ở mọi khung. Đã rút gọn tiêu đề và ghi vào `production.md`.
- Khối mã (L04 khung 36): viền nhấn dày 5px, cách chữ 5px, che dấu dưới (“kiện”) của dòng bên trên. `player.css` giờ dùng viền 3px sát dòng cho `.code > div.focus`; CS115 không có khối mã. Đã dựng lại 11 bài có khối mã.
- L08 khung 1: nhãn tên cọc sát đáy SVG bị viền nhấn của dòng dưới che. Đã tăng chiều cao SVG và căn giữa nhãn; quét mọi SVG của 25 bài, không còn chữ nào sát đáy.
- `render` FAIL vì tràn khung ở L04 khung 41, L13 khung 16, L23 khung 25. Đã tách step bằng `clear: true` và nhắc lại ngữ cảnh.

Còn để nguyên: ở L10 khung 16 và L24 khung 4, hai viền nhấn của hai dòng liền nhau chạm nhau. Chỉ là thẩm mỹ, không che chữ.

Mỗi bài đã xem ít nhất một khung `symbol`, các khung SVG/bảng/khối mã, một khung pitfall và khung cuối; xem bằng ảnh ghép thì chữ nhỏ có thể sót. Khung xem sau khi sửa: L04 36, L08 1, L13 14–17, L23 0, 25, 40, 66.

## 4. Phát âm (ASR-checked, không phải “đã nghe”)

- Đã thử bằng probe (`audit/cs112/probes/`): Tê-ta 8/8, Omega 8/8, “O lớn” 8/8, AVL 8/8, Catalan 8/8, Fi-bô-na-chi 8/8, Đan-xích 7/8.
- Không xác nhận được nên không đọc, chỉ để trên màn hình: Euclid, byte, Bland, Python.
- `p4_chen` (2026-10-27): “chèn” được medium nghe đúng 4/4, small nghe sai 4/4, đối chứng “chàng” 0/8. INFERRED: lỗi nằm ở mô hình small, không phải ở giọng đọc.
- Các câu ngắn bị nghe sai đã được viết dài hơn để có ngữ cảnh, ví dụ “Đến lượt bạn.” thành “Bây giờ đến lượt bạn tự làm.”, “Năm bẫy cuối.”, “Ôn hai công cụ.”.
- Các nhóm gắn cờ đã xem xét: Theta chép thành teta/θ; lôgarit chép thành logarith (nút thắt B20 đã biết); “ô” chép thành O; tên chữ cái đọc kiểu Việt; nhầm thanh của ASR (hằng/hàng, bậc/bật, đệ/để, mảng/mạng).

## 5. Còn NOT_VERIFIED

1. Hiệu quả sư phạm với người học thật: chưa có ai học thử.
2. Các câu ghi NOT_VERIFIED trong `asr_reviewed`: “chèn” (L03), “Lỗi thứ nhất, quên đánh dấu đỉnh đã thăm.” (L07), “nhầm dãy con” (L20), “Bẫy mười ba” (L24, bẫy/bảy). Cần người nghe.
3. Không có trên máy nên không đưa vào video: thang điểm, phân bổ thời gian thi, quy định chấm của giảng viên, slide, đề thi (AUDIT §1).
4. Số đo trong bài 23 lấy từ báo cáo bài tập lớn (một máy). Bài 23 nói rõ điều này; chưa đo lại trên máy khác.
5. Giọng đọc edge-tts là dịch vụ trực tuyến của Microsoft; dựng lại về sau có thể cho âm khác nếu dịch vụ đổi.
