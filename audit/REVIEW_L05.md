# Rà soát L01–L04 + làm L05 — 2026-10-23

Phạm vi: chạy lại toàn bộ kiểm tra của L01–L04; làm bài L05 `lessons/L05_dao_ham_gradient.yaml` → `out/L05/`.
Nhãn: OBSERVED = chạy trong phiên này; CITED = kết quả phiên trước, kèm ngày; INFERRED = suy luận, chưa kiểm bằng máy.
Môi trường: Python 3.13.5 (`.venv`), Windows 11.

## 1. Nút thắt hợp đồng (contract bottleneck)

| ID | Chưa xác định / chưa kiểm | Việc phụ thuộc | Bằng chứng đóng | Trạng thái |
|---|---|---|---|---|
| B10 | Nguồn dòng 223 định nghĩa ∇f bằng đạo hàm riêng nhưng không định nghĩa đạo hàm; “chỉ hướng tăng nhanh nhất” thiếu điều kiện | Nội dung L05 | Audit A22 + T15a–f; `verify_cs115_tex.py` → `TOTAL=46 PASS=46 FAIL=0` (22:37:06Z). L05 dạy đạo hàm từ độ dốc, suy ra hướng tăng nhanh nhất bằng cái bóng + Pytago (bài 1), nêu 3 điều kiện (derive) và lỗi 4 | CLOSED |
| B11 | Cách đọc “nabla”, “gradient”, “Descent”, “Jacobian”, chữ f, h, “f phẩy” | ~60 câu L05 | Đối chứng `l05_probe*.py`, `grad_probe.py`, `jh_probe.py` (small + medium, có đối chứng âm). Lexicon: nabla → na-bla, gradient → grê-đi-ần (cách cũ “gờ-ra-đi-ần” bị medium nghe “gửi ra điền” 2/3 câu), Descent → đi-xen, Jacobian → Gia-cô-biên; `vi_text`: f, h, `x'`, bí danh neuron/Giacobin; 5 test E17 mới | CLOSED (phần máy) |
| B12 | Cách đọc “Hessian”: đọc thô, “Hét-xi-ần”, “Hét-siên” đều cho ASR nghe không nhất quán | L06 | — (lời L05 không nhắc tên này; ghi vào `fix` của L06 trong curriculum) | OPEN → L06 |

## 2. Lỗi công cụ tìm thấy (đã sửa, có test)

| # | Lỗi | Hậu quả | Sửa |
|---|---|---|---|
| T1 | `verify` chỉ so sha256 file đặc tả; đổi lexicon thì audio cũ lỗi thời mà vẫn PASS | Câu cuối L04 (có “gradient”) vẫn giọng cũ sau khi đổi lexicon | `build_report.json` ghi `tts_sha256` (văn bản đã qua lexicon + giọng + tốc độ); verify FAIL khi khác hoặc khi thiếu. Build lại L01–L04: L01–L03 0 câu đọc lại, L04 đọc lại đúng 1 câu. Test E20 |
| T2 | `tts` nhận audio bị dịch vụ cắt cụt mà không báo | L05 khung 75: 0,72 s cho 16 từ; ASR chỉ nghe “Với hàm...” | Audio < 0,15 s/từ là cắt cụt (923 câu L01–L05: trung vị 0,346; nhanh nhất ngoài câu lỗi 0,256) → đọc lại, vẫn cắt thì FAIL. Test E21 |

## 3. Lỗi tìm thấy khi làm L05 (đã sửa)

| # | Lỗi | Phát hiện bằng | Sửa |
|---|---|---|---|
| G1 | Bản đầu dài 17,8 phút (> 15) | `verify` + chương | Đếm từ từng phân cảnh, viết gọn lời, bỏ dòng x³: 14,2 phút |
| G2 | Tên hàm `p(x, y)` bị lint hiểu là xác suất | lint FAIL | đổi thành k |
| G3 | Hình tiếp tuyến: nhãn “dốc 6” đè đường cong, hình nhỏ | xem khung | phóng vùng x ∈ [1,5; 4,6], dời nhãn |
| G4 | Công thức ngắt dòng giữa chừng (gradient D biến, thử quy tắc tổng, lỗi 1) | xem khung | công thức dòng riêng |
| G5 | Phân số li ti trong bảng 5 hướng, điểm dừng, bài tự làm | xem khung | `\dfrac`; bảng cao hơn làm TRÀN → `clear: true` + dòng “Đang có” |
| G6 | Lỗi 3 nói “f của ví dụ” khi f không có trên bảng (luật 16); lỗi 4 viết “∇” không tên hàm; “f(1) = 4” dùng lại chữ f cho hàm khác | rà khung | ghi rõ hàm |
| G7 | 13 câu bị ASR gắn cờ: câu ngắn (“Ôn nhanh vài thứ.”, “Cho h nhỏ dần.”), “luật” → “lục”, “dốc k” → “yoga”, D → “dây”, “Hessian” | `lv.py asr` | ghép câu, đổi “luật” → “quy tắc”, viết lại không dùng chữ cái rủi ro; còn 0 |

## 4. Bằng chứng (OBSERVED, `checked_at` lấy từ đầu ra công cụ)

| Kiểm tra | Lệnh | Kết quả |
|---|---|---|
| Tự kiểm công cụ | `tests/test_lint.py` | 0 FAIL, 53 dòng PASS (22:36:47Z) |
| Lint L01–L05 | `lv.py lint` | 0 FAIL, 0 WARN cả 5 bài; L05: 45 phép kiểm số học (sympy) |
| Verify L01–L05 (có dấu TTS mới) | `lv.py verify` | PASS cả 5 (1121,73 s; 1114,1 s; 902,9 s; 873,9 s; 851,07 s) |
| Audit nguồn | `audit/verify_cs115_tex.py` | `TOTAL=46 PASS=46 FAIL=0` (22:37:06Z) |
| Lộ trình | `lv.py curriculum` | 17 bài, 5 có đặc tả, 0 lỗi (22:40:15Z) |
| Video L05 | `lv.py build` | 851,07 s = 14,2 phút, 158 khung, 15 chương; verify PASS |
| Khớp tiếng–hình L05 | `sync_check.py` (9 điểm) | 0 lệch (22:39:58Z) |
| ASR L05 | `lv.py asr` (small + medium) | 158 câu, TB 0,963, gắn cờ 0 (22:36:36Z); tham khảo 50 câu từ thường |
| ASR L01–L04 sau khi đổi `vi_text`/lexicon | `lv.py asr` | chưa xem xét không đổi: 9 / 8 / 1 / 4 |
| Khung đã xem bằng mắt | Read ảnh | 58 khung cuối của mọi step (lượt 1), 24 khung của 7 phân cảnh đã sửa (lượt 2), khung cuối phân cảnh rules (lượt 3) |

## 5. Còn mở (NOT_VERIFIED)

- L05 không còn câu bị gắn cờ, nhưng nên nghe các câu có “phẩy” (khung 27, 29: “f phẩy”; khung 25 và các câu số thập phân): ASR hay chép “phẩy” thành “phải” (hai từ chỉ khác nguyên âm). Đối chứng: câu viết hẳn “phải” thì medium nghe khác bản “phẩy” ở 1/2 câu thử, nên chỉ ghi là ASR-checked.
- L04 (4 câu), L03 (1), L02 (8), L01 (9): vẫn chờ người nghe như các báo cáo trước.
- Bước 1 của phân cảnh derive (cộng hai xấp xỉ theo từng biến) là lập luận trực giác, đúng khi f khả vi liên tục; video nêu điều kiện “f trơn” nhưng không chứng minh: INFERRED về tổng quát, kiểm bằng số ở T15c và bước “làm thử ngay”.
- Hiệu quả sư phạm với người học thật: chưa đo.
