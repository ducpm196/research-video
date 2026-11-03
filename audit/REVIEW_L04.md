# Rà soát L01–L03 + làm L04 — 2026-10-23

Phạm vi: chạy lại toàn bộ kiểm tra của L01–L03; làm bài L04 `lessons/L04_tri_rieng_vector_rieng.yaml` → `out/L04/`.
Nhãn: OBSERVED = chạy trong phiên này; CITED = kết quả phiên trước, kèm ngày; INFERRED = suy luận, chưa kiểm bằng máy.
Môi trường: Python 3.13.5 (`.venv`), Windows 11.

## 1. Nút thắt hợp đồng (contract bottleneck)

| ID | Chưa xác định / chưa kiểm | Việc phụ thuộc | Bằng chứng đóng | Trạng thái |
|---|---|---|---|---|
| B8 | Nguồn **dùng** trị riêng/vector riêng (dòng 205, 207, 213, 256–260) mà không định nghĩa; thiếu v ≠ 0; bảng 256–260 ngầm cần trị riêng thực | Nội dung L04 (không được lặp lại thiếu sót) | Audit A21 + T14a–d; `verify_cs115_tex.py` → `TOTAL=40 PASS=40 FAIL=0` (19:29:27Z). Lần chạy đầu T14b FAIL do chính câu lệnh kiểm (`sp.solve` không nhận `domain=`), đổi sang `sp.solveset`, giữ nguyên kỳ vọng. L04 nêu v ≠ 0 (symbol + lỗi 1), ma trận quay (meaning), A1 (in_ai) | CLOSED |
| B9 | Cách đọc “lambda” của giọng vi-VN-NamMinhNeural | Mọi câu có λ (≈ 40 câu) | Đối chứng `lambda_probe.py`: “lambda” và “lam đa” dài bằng nhau (3,264 s); ASR nghe “lam” thành “năm” (l/n). Đối chứng âm “trị chung” vẫn bị nghe ra. Lexicon `lambda → lam-đa`; `vi_text.LETTER_HEARD` (“lam”, “đa”) + `ASR_ALIASES` + 2 test E17 | CLOSED (phần máy); thanh điệu “lam” hay “làm” → mục 4 |

## 2. Lỗi tìm thấy khi làm L04 (đã sửa)

| # | Lỗi | Phát hiện bằng | Sửa |
|---|---|---|---|
| G1 | Bảng có hình ở phần mở đầu tràn (4 khung) | render FAIL | `clear: true` + nhắc lại ma trận A trên bảng có hình |
| G2 | Heredoc Python trong Git Bash biến `\b` thành ký tự 0x08 → YAML lỗi | YAML reader | sửa dòng bằng file `.py` viết qua Write; thêm dòng vào `production.md` |
| G3 | Công thức bước 3 và “phép thử nhanh” bị ngắt dòng giữa chừng | xem khung 59, 85 | chuyển thành công thức dòng riêng |
| G4 | Bảng ý nghĩa λ không kẻ ô, chữ dính nhau (“0 < λ < 1ngắn lại”) | xem khung 44 | `class="t"` |
| G5 | 7 bảng nhắc tới A hoặc B nhưng ma trận không có trên bảng (luật 16) | xem khung 31, 47, 73, 107, 114, 126, 133 | thêm dòng “Đang có: A = …” hoặc ghi ma trận ngay trong bảng |
| G6 | “định thức của nó trừ λI₂” đọc thành det(M) − λI₂ | rà câu chữ | viết rõ det(M − λI₂) = (2 − λ)(2 − λ) − (−1)·(−1) (có `checks`) |
| G7 | Câu 3 từ “Đáp án như sau.”, cụm “then chốt” bị cả hai mô hình nghe sai | ASR | ghép câu; đổi thành “quan trọng nhất” |

## 3. Bằng chứng (OBSERVED, `checked_at` lấy từ đầu ra công cụ)

| Kiểm tra | Lệnh | Kết quả |
|---|---|---|
| Tự kiểm công cụ | `tests/test_lint.py` | 0 FAIL, 46 dòng PASS (thêm 2 ca E17 cho lambda; 19:29:18Z) |
| Lint L04 | `lv.py lint lessons/L04_…yaml` | 0 FAIL, 0 WARN; 45 phép kiểm số học (sympy); 181 công thức KaTeX không lỗi |
| Lint + verify L01–L03 | `lv.py lint`, `lv.py verify` | 0 FAIL, 0 WARN; PASS (1121,73 s; 1114,1 s; 902,9 s) |
| Lộ trình | `lv.py curriculum curriculum/cs115.yaml` | 17 bài, 4 có đặc tả, 0 lỗi (19:29:28Z) |
| Audit nguồn | `audit/verify_cs115_tex.py` | `TOTAL=40 PASS=40 FAIL=0` (19:29:27Z) |
| Video L04 | `lv.py build` → verify | 873,93 s = timeline 873,933 s (14,6 phút, 156 khung); PASS (19:28:20Z) |
| Khớp tiếng–hình L04 | `sync_check.py` (9 điểm trải đều) | 0 lệch (19:29:32Z) |
| ASR L04 | `lv.py asr` (small + medium) | 156 câu, TB 0,963; gắn cờ 13, đã xem xét 9 (đối chứng), **chưa xem xét 4**; tham khảo 36 (19:28:53Z) |
| ASR L01–L03 sau khi đổi `vi_text` | `lv.py asr` | không đổi: chưa xem xét 9 / 8 / 1 |
| Khung đã xem bằng mắt | Read ảnh | 51 khung cuối của mọi bảng (bảng tổng hợp), gồm khung có hình, mọi khung có ký hiệu mới (λ, det), khung cuối formula/example, pitfall, khung cuối; 31, 35, 44, 47, 59, 73, 85, 107, 114, 119, 126, 129, 133 xem lại sau khi sửa |

## 4. Còn mở (NOT_VERIFIED)

- L04 cần người nghe:
  - **01:32** “A trừ 3 I hai cho âm 1, 1, 1, âm 1” và **07:18** “… v hai bằng 1, âm 1”: ASR nghe “một → mục”, cùng loại với L01–L03.
  - **03:45** “Lambda lớn hơn 1 …”: medium nghe “Làm đa” ở cả bản viết “lam-đa” lẫn bản “làm đa”. Cần nghe xem giọng đọc nói “lam-đa” hay “làm-đa”; câu trả lời áp dụng cho **mọi** câu có lambda.
  - **09:42** “… B nhân v …”: ASR nghe “bầy”, còn bản viết “bê” lại nghe ra “b”; máy chưa phân định được.
- L01 (9 câu), L02 (8 câu) ở `audit/REVIEW_L02.md` §4, L03 (13:29) ở `audit/REVIEW_L03.md` §4: vẫn mở.
- Phát biểu “ma trận đối xứng: vector riêng ứng với hai trị riêng khác nhau luôn vuông góc” chỉ kiểm trên ví dụ (T14c, `checks`), chưa chứng minh trong video (hẹn bài 11). Đây là định lý chuẩn: INFERRED về tổng quát.
- Hiệu quả sư phạm với người học thật: chưa đo.
