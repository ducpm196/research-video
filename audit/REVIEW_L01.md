# Rà soát L01 (v1 → v2) — 2026-10-22

Phạm vi: `lessons/L01_vector_tich_vo_huong_phep_chieu.yaml`, `out/L01/L01.mp4`, cùng các công cụ trong `tools/` liên quan.

## 1. Lỗi người dùng báo — nguyên nhân gốc — cách chặn vĩnh viễn

| # | Lỗi | Nguyên nhân gốc (OBSERVED) | Sửa | Cổng chặn tái diễn |
|---|---|---|---|---|
| U1 | “hai” đọc thành “hây ai”, “sai” thành “sây ai” | Luật lexicon `AI→ây ai` chạy với `re.I` và không có ranh giới từ, làm hỏng 32/194 câu | Engine bọc ranh giới từ Unicode; mặc định phân biệt hoa thường | `must_not_change` tự kiểm mỗi lần lint; test E11; `lv.py asr` |
| U2 | “Mẹo then chốt” hiện ‖u‖₂² — “dư 2 số 2”, lặp lại ở các phần sau | Bài viết lẫn ‖·‖₂ (độ dài, công thức) với ‖·‖ (lỗi thường gặp, kiểm tra, tổng kết); chỉ số dưới 2 chưa bao giờ được giải thích | Cả bài chỉ dùng ‖x‖; một step `notation_note` giải thích ‖x‖₂ = chuẩn L2; một step riêng giải thích mũ 2 = bình phương | Luật `consistency` (test E12) |
| U3 | Chưa nói rõ vì sao z = y − c·u | Bài chưa dạy cộng/trừ vector, nhân vector với số, chuyển vế; các bước suy luận không nêu lý do | Thêm cảnh “Nhân vector với một số, cộng và trừ vector” có hình nối đuôi; viết lại phần công thức thành 5 bước, mỗi bước có lý do; thêm “làm thử ngay bằng số” (10 − 5c = 0 ⇒ c = 2, khớp với công thức) | Luật pedagogy 11–12; lint WARN khi thiếu từ chỉ lý do (test E13) |

## 2. Lỗi tìm thêm trong lúc rà soát (người dùng chưa báo)

| # | Lỗi | Phát hiện bằng | Sửa | Cổng chặn |
|---|---|---|---|---|
| F1 | Dấu `·` dùng làm phép nhân mà chưa giải thích | Luật mới: `cdot` không còn là kiến thức mặc định | Giải thích trong phần ôn nền | registry `cdot` |
| F2 | “⇒” (ký tự trong chữ) và “⟹” (công thức) cùng nghĩa “suy ra” nhưng khác hình dạng; tương tự ⇔/⟺, “·” dùng làm dấu ngăn cách | Xem khung hình bằng mắt, sau đó máy hoá | Đưa ký hiệu vào công thức; bỏ “·” khỏi vai trò ngăn cách | Luật glyph chữ-vs-công-thức (test E14) |
| F3 | Ký hiệu u′ chưa giải thích | Xem khung hình | Dùng 2u (ký hiệu đã học) | registry `prime` (test E15) |
| F4 | Ký tự ✗ hiển thị giống chữ X, dễ nhầm với biến x | Xem khung hình | Thay bằng chữ “(sai)” màu đỏ | lint (test E16) |
| F5 | “gần cùng hướng” không chính xác | Rà phát biểu | Đổi thành “góc nhọn (< 90°)”, thêm điều kiện hai vector khác vector không; có `checks` bằng arccos | — |
| F6 | `proj`, `logic`, `Vector`, `AI` đọc sai | Thử nhiều cách viết và cho ASR nghe lại (proj → “phô dì”, logic → “lo triển”, Vector → “vết to”, AI → “EA”) | Chọn cách viết ASR nghe đúng: prô-giéc, lô-gíc, véc tơ, ây ai | lint WARN cho mọi từ không phải âm tiết tiếng Việt |
| F7 | Câu 1–2 từ (“Khớp.”, “Đáp án.”) bị nghe sai (“cỡp”, “đập ảnh”) | ASR | Ghép vào câu bên cạnh | lint WARN cho câu ≤ 2 từ |
| F8 | Vector viết ngang (6, 2, 4)ᵀ chưa giải thích | Rà ký hiệu | Thêm step trong cảnh chuyển vị | — |

## 3. Bằng chứng (OBSERVED trong phiên)

| Kiểm tra | Lệnh | Kết quả |
|---|---|---|
| Lint L01 | `lv.py lint lessons/L01_…yaml` | 0 FAIL, 0 WARN; 123 công thức KaTeX; 45 phép kiểm số học |
| Tự kiểm công cụ | `tests/test_lint.py` | 24/24 PASS (E1–E16, phát âm, đổi số → chữ, template) |
| Video | `lv.py build` → verify | 1121,73 s = timeline 1121,733 s; h264 + aac, 1920×1080; PASS |
| Khớp tiếng–hình | trích 7 khung từ mp4 | 0 khung lệch (MAE ≈ 1,1 so với khung đúng) |
| Đối chứng dương ASR | câu cố tình đọc “hây ai” | small 0,609 và medium 0,609 → gắn cờ; câu đúng 1,000 |
| ASR toàn bài | `lv.py asr` (small + kiểm lại bằng medium) | 239 câu, độ khớp TB 0,914; còn 16 câu bị gắn cờ, 4 câu đã xem xét (tên chữ cái), **12 câu chờ người nghe** |
| Cấu trúc skill | `check_skills.py` (bản sao cùng skill gốc) | 28 PASS, 0 FAIL, 2 N/A |

## 4. Còn mở (NOT_VERIFIED)

- 12 câu ASR không phân định được: xem `out/L01/asr_report.md`, mốc thời gian 05:45, 07:45, 08:51, 11:06, 11:19, 12:59, 13:48, 14:54, 15:10, 16:39, 16:41, 17:18. Đa số thuộc cặp âm dễ lẫn (vuông/vùng, một/mục, bạn/bản). Cần người nghe xác nhận.
- Hiệu quả sư phạm với người học thật chưa được đo.
