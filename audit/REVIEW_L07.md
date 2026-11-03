# Đánh số lại lộ trình + L07 (tìm cực trị) + sửa lỗi hạ tầng — 2026-10-24

Phạm vi:
1. Đánh số lại lộ trình theo đúng thứ tự học (L00–L29) và áp luật trích dẫn bài khác (luật 17). Chi tiết ở `audit/CURRICULUM_RENUMBER.md`.
2. Làm bài L07 `lessons/L07_cuc_tri.yaml` → `out/L07/`.
3. Sửa các lỗi hạ tầng tìm thấy trong phiên: build treo, chữ hai dấu lệch trong công thức, `curriculum` không bắt được bài bị bỏ sót.

L00 được báo cáo riêng ở `audit/REVIEW_L00.md`.
Nhãn: OBSERVED = chạy trong phiên này; CITED = kết quả phiên trước, kèm ngày; INFERRED = suy luận, chưa kiểm.
Môi trường: Python 3.13.5 (`.venv`), Windows 11, KaTeX 0.16.11, giọng vi-VN-NamMinhNeural.

## 1. Nút thắt hợp đồng (contract bottleneck)

| ID | Chưa xác định / chưa kiểm | Việc phụ thuộc | Bằng chứng đóng | Trạng thái |
|---|---|---|---|---|
| B16 | Câu “bài sau” của L07 và các ghi chú `fix` (A1, A2, A4) | L07 | L07 dạy Δ₁, Δ₂ và Sarrus từ đầu. Phép kiểm T21a–c: 3000 ma trận 2×2 ngẫu nhiên, Sarrus trên 200 ma trận, công thức uᵀHu; tổng 59/59 PASS (12:06:37Z). Đối chứng âm (luật sai) lệch 314/3000 | CLOSED |
| B17 | Số hiệu bài khác thứ tự học: người học nghe “bài 17” mà thực tế học ở vị trí khác | Mọi câu “bài N” | Đánh số lại; `curriculum` kiểm số hiệu tịnh tiến; lint E22 kiểm “bài N” có trong lộ trình | CLOSED |
| B18 | `build` L07 treo ~6,5 giờ, không in gì | Mọi lần build | Nguyên nhân (INFERRED, chưa tái hiện được): `edge_tts…save()` không có thời hạn. Đã thêm `asyncio.wait_for(…, 60)` và `timeout=120` cho ffmpeg. Sau khi sửa, 9 lượt build chạy hết; L00 gặp `NoAudioReceived` ở 7 câu → báo BLOCKED đúng thiết kế, không treo | CLOSED (phần chặn treo) |
| B19 | Chữ hai dấu (ố, ầ, ễ…) trong `\text{}` hiện lệch dấu ở mọi bài | Khung hình L00–L07 | `katex_safe()` + CSS `.katex .text`. Xem phóng to: L00 khung 45 (“số phòng”), L05 khung 16 (“độ dốc”), L06 khung 25, L07 khung 39 đều đúng. Có test | CLOSED |
| B20 | Cách đọc “logarit” | L11 | Probe: tốt nhất “lô-ga-rit” 4/8 < 7/8 | **OPEN** → L11 (đã ghi vào `fix` của L11) |

## 2. L07: kết quả (OBSERVED)

| Hạng mục | Kết quả | checked_at |
|---|---|---|
| lint | 0 FAIL, 0 WARN, 50 PASS; 43 phép kiểm sympy; 15 scene; ký hiệu mới: `star` (x*) | 12:03:39Z |
| Trích dẫn | 3 step nhắc bài sau (đều `forward_ref: true`, ở in_ai/recap); 15 câu nhắc bài trước, không câu nào bị E23 | 12:03:39Z |
| build + verify | `out/L07/L07.mp4` 824,67 s (13,7 phút), 145 khung, verify PASS | 12:06:04Z |
| render | 145 khung, 0 vấn đề (tràn bảng, KaTeX, phụ đề) | 12:04:04Z |
| ASR | 145 câu, độ khớp TB 0,968, gắn cờ 3, **chưa xem xét 0** | 12:28:58Z |

ASR xử lý (lượt 11:42Z có 4 câu gắn cờ):
- **Khung 101**: “con số tài liệu không ghi” bị nghe thành “còn số … không ký” (độ khớp 0,769). Đã viết lại câu; lượt sau không còn bị gắn cờ.
- **Khung 49, 69, 138**: “Hết-sen” bị nghe thành “hết sang / sành / xe”. Cùng cách viết này được nghe đúng 17/21 lần (small) và 18/21 lần (medium) trong L07, 20/23 và 19/23 trong L06, 8/8 trong probe riêng (`hess_count.py`). Vì vậy đã ghi `asr_reviewed`, kết luận nhiều khả năng do ASR nghe nhầm theo ngữ cảnh. Kết luận này là **INFERRED**, cần người nghe.

Xem bằng mắt trong phiên này: khung 39 (L07, công thức có chữ tiếng Việt). Các khung khác của L07 đã được xem ở phiên trước (CITED 2026-10-24, phần trước khi tóm tắt hội thoại).

## 3. Lỗi tìm thấy và đã sửa trong phiên

| Lỗi | Bằng chứng | Sửa | Chặn tái phát |
|---|---|---|---|
| Build treo nhiều giờ | `build37.log` dừng ở `== lessons/L07_cuc_tri.yaml`; không còn tiến trình con (`Win32_Process`, 11:11Z) | Thời hạn tts/ffmpeg; chạy nền bằng `python -u` + `timeout` | Có trong `lv.py` |
| Chữ hai dấu lệch trong công thức | Khung L05#16 trước khi sửa: dấu sắc của “dốc” chồng lên dấu mũ | `katex_safe()` + CSS | `tests/test_lint.py` (katex_safe) |
| `curriculum` không bắt được bài bị bỏ sót (L00) | Trước khi sửa: `30 bài, 7 đã có đặc tả, 0 lỗi` | Kiểm khoảng trống, file spec tồn tại, `id` khớp | test + đối chứng dương (11:22:33Z) |
| Heredoc ghi byte null vào `lv.py` | `SyntaxError: source code string cannot contain null bytes` | Viết lại bằng script tạo qua công cụ Write; kiểm `b"\x00"` = 0 | production.md |

## 4. Kiểm toàn bộ (OBSERVED)

| Kiểm | Kết quả | checked_at |
|---|---|---|
| `tests/test_lint.py` | 0 FAIL (gồm 2 ca mới: katex_safe, bài bị bỏ sót) | 12:43:45Z |
| `audit/verify_cs115_tex.py` | TOTAL=59 PASS=59 FAIL=0 | 12:44:06Z |
| `lv.py curriculum` | 30 bài, 8 đã có đặc tả, 0 lỗi | 12:44:05Z |
| build lại L00–L07 (CSS mới) | 8/8 verify PASS: L00 646,4 s · L01 1131,8 s · L02 1121,43 s · L03 894,33 s (rút gọn 39 từ, đếm bằng máy từ l03_trim2–4.py, để ≤ 15 phút) · L04 895,03 s · L05 877,77 s · L06 888,8 s · L07 824,67 s; L00 xem REVIEW_L00 | verify lại 12:43–12:44Z |

## 5. Còn mở (NOT_VERIFIED)

- Người nghe: L01 (8 câu), L02 (8), L03 (1), L04 (4), L06 (3 + độ tự nhiên của “Hết-sen”), L07 (3 câu “Hết-sen”).
- L01 (18,9 phút) và L02 (18,7 phút) dài hơn khung 10–15 phút. Đây là vấn đề có từ trước, chưa xử lý trong phiên này.
- Cách đọc “logarit” (B20) → phải giải quyết trước khi làm L11.
- NMF (chỉ có ở slide GT24): người dùng quyết định có thêm hay không. L22 (Lagrange/KKT, ngoài đề cương): người dùng có thể bỏ.
- Hiệu quả sư phạm với người học thật: chưa đo.
- Luật đồng âm miền Bắc (gi/d, s/x) dùng khi so ASR: INFERRED.
