# Rà soát L01 + làm L02 — 2026-10-22

Phạm vi: rà lại hiện trạng L01 (công cụ, môi trường, cổng ASR), làm bài L02 `lessons/L02_ma_tran.yaml` → `out/L02/`.
Nhãn: OBSERVED = chạy trong phiên này; INFERRED = suy luận, chưa kiểm bằng máy. Môi trường: Python 3.13.5 (venv mới), Windows 11, Node v25.8.0.

## 1. Nút thắt hợp đồng (contract bottleneck) đã gặp và cách đóng

| ID | Chưa xác định / chưa kiểm | Việc phụ thuộc | Bằng chứng đóng | Trạng thái |
|---|---|---|---|---|
| B1 | `.venv` tạo trên máy khác (`D:\Doan\…`, Python 3.12 của user `ducpm2`) → mọi lệnh `lv.py` lỗi `No Python at …` | Toàn bộ lint/test/build/asr | Đổi tên venv cũ thành `.venv-broken-py312` (giữ lại), tạo venv Python 3.13.5, cài **đúng phiên bản cũ** (đọc từ dist-info). Ghim vào `requirements.txt`. `tests/test_lint.py` 0 FAIL, L01 `verify` PASS (OBSERVED) | CLOSED |
| B2 | Cổng ASR chỉ so cả câu: **một từ đọc sai lọt qua**. Đối chứng dương: “nghịch lý” thay “nghịch đảo” → medium 0,917; “đường ngang” thay “đường chéo” → 0,875 (OBSERVED) | Mọi kết luận “ASR-checked” về phát âm | `asr` cho medium nghe mọi câu, gắn cờ **từ rủi ro** (do lexicon sinh, từ ngoại, chữ cái) mà cả hai mô hình đều nghe khác; từ thuần Việt hai mô hình cùng nghe khác ghi mục tham khảo. Chuẩn hoá phía ASR: dấu kiểu cũ/mới, bí danh từ ngoại, tên chữ cái chỉ ở vị trí gióng hàng, chữ cái viết dính. Test E17 (11 ca) | CLOSED, giới hạn ở §4 |
| B3 | `audit/verify_cs115_tex.py` chết `UnicodeEncodeError` khi stdout bị pipe (cp1252) | Bằng chứng audit nguồn | Thêm `sys.stdout.reconfigure(encoding="utf-8")`; chạy lại `TOTAL=35 PASS=35 FAIL=0` (OBSERVED) | CLOSED |
| B4 | Dấu × vừa là kích thước (2 × 3) vừa là phép nhân (L01 đã chuyển phép nhân sang ·) | Ký hiệu L02 trở đi | Macro `\sz{M}{N}`, ký hiệu `dim` + `sub2` trong registry; lint FAIL khi gõ `\times` trong số mũ (test E18, E19) | CLOSED |

## 2. Lỗi tìm thấy khi làm L02 (đã sửa)

| # | Lỗi | Phát hiện bằng | Sửa | Cổng chặn |
|---|---|---|---|---|
| G1 | Bảng sau `clear` nói “X ở trên”, “M lúc nãy”, “(5 + 5, 1 + 2)” nhưng đối tượng đã bị xoá (4 khung) | Xem khung hình | Hiện lại X, A, B, AB, M ngay trong khối; tô màu phần tử được nhắc | pedagogy luật 16 (xem khung) |
| G2 | “ma trận phục vụ hai bước đầu”, “trường hợp hiếm hoi đổi thứ tự…”, “mỗi ô luôn là một tổng” — phát biểu không chính xác | Rà phát biểu (luật 15) | Viết lại chính xác | — |
| G3 | **y** trong công thức nghiệm hồi quy chưa giải thích; `I_N` dùng lại chữ N với nghĩa khác | Xem khung hình | Thêm “y ∈ ℝ^{N×1}: giá thật”; đổi thành Q⁻¹ = Qᵀ | — |
| G4 | ½, 3/2 trong ma trận nhỏ li ti | Xem khung hình | `\dfrac` | production.md |
| G5 | Chữ **w** đọc thô → ASR nghe “với đúc” | Thử 3 cách viết + ASR | lexicon `w → vê kép` | test E11 |
| G6 | Tràn bảng ở cảnh mở đầu | `render` FAIL | `clear: true` | render |

## 3. Bằng chứng (OBSERVED trong phiên, `checked_at` từ đầu ra công cụ)

| Kiểm tra | Lệnh | Kết quả |
|---|---|---|
| Tự kiểm công cụ | `tests/test_lint.py` | 39 PASS, 0 FAIL (`2026-10-22T18:15Z`) |
| Lint L02 | `lv.py lint lessons/L02_ma_tran.yaml` | 0 FAIL, 0 WARN; 158 công thức KaTeX; 52 phép kiểm số học (sympy) |
| Lint L01 | `lv.py lint lessons/L01_…yaml` | 0 FAIL, 0 WARN |
| Lộ trình | `lv.py curriculum curriculum/cs115.yaml` | 17 bài, 2 có đặc tả, 0 lỗi (mọi `assumes` của L02 đã được L01 giới thiệu) |
| Video L02 | `lv.py build` → verify | 1114,1 s = timeline 1114,1 s; h264 + aac 1920×1080; PASS (`18:14:14Z`) |
| Video L01 | `lv.py verify` | 1121,73 s = timeline; PASS — không STALE sau khi thêm `asr_reviewed` |
| Khớp tiếng–hình L02 | `sync_check.py` (9 điểm trải đều) | 0 lệch; MAE với khung đúng 1,27–1,61 < khung kế 1,94–4,93 |
| ASR L02 | `lv.py asr` (small + medium, mức câu + mức từ) | 210 câu, TB 0,951; gắn cờ 20, đã xem xét 12 (bằng đối chứng), **chưa xem xét 8**, tham khảo 58 |
| ASR L01 (cổng mới) | `lv.py asr` | 239 câu, TB 0,963; gắn cờ 11 + 4 xem xét mới, **chưa xem xét 9** (trùng danh sách chờ người nghe của REVIEW_L01) |
| Audit nguồn | `audit/verify_cs115_tex.py` | `TOTAL=35 PASS=35 FAIL=0` |
| Khung đã xem bằng mắt (L02) | Read ảnh | 0, 5, 24, 32, 37, 40, 48, 55, 62, 75, 85, 92, 103, 117, 125, 134, 146, 157, 165, 170, 173, 176, 190, 200/201, 209 |

Đối chứng phát âm (OBSERVED; audio đối chứng nằm ở thư mục tạm của phiên, không lưu trong dự án — kết quả được ghi vào `asr_reviewed` của từng bài): viết hẳn tên chữ cái (“a dê trừ bê xê”, “bê ích”, “cột gi”, “vê kép”, “tê”) thì ASR nghe sai **y hệt** bản chữ cái thô → TTS đọc đúng tên chữ cái; “S” và “ét”, “T” và “tê” cho audio dài bằng nhau tới mili giây.

## 4. Còn mở (NOT_VERIFIED) — cần người nghe

L02 (`out/L02/asr_report.md`): 04:11 (“âm” trong “2, 1, âm 1” — cả hai mô hình đều mất chữ “âm”, **quan trọng vì đổi dấu số**), 05:38, 05:47, 06:30, 10:20, 11:45, 12:18, 16:31. Đa số là “một → mục”, “cột → cục”: viết hẳn chữ “một” ASR vẫn nghe “mục”, trong khi cùng giọng ở câu khác thì “một” nghe đúng → không phân định được bằng máy.
L01: 07:45, 08:51, 11:19, 12:59, 13:48, 15:10, 16:39, 16:41, 17:18.

Giới hạn của cổng ASR mới (INFERRED): từ thuần Việt bị đọc sai thanh điệu chỉ nằm ở mục tham khảo, không chặn — vì mô hình ASR hiện có nhầm thanh rất nhiều (58 câu tham khảo ở L02) nên không dùng được làm cổng.

Lệch chuẩn đã biết: L02 dài 18,6 phút (L01: 18,7 phút) — vượt khung 10–15 phút của pedagogy.md luật 10. Bài gồm 4 chủ đề (nhân, đơn vị, chuyển vị, nghịch đảo) theo đúng lộ trình; tách đôi là quyết định của người dùng.

Hiệu quả sư phạm với người học thật: chưa đo.
