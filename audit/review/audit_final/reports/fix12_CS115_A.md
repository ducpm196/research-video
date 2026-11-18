# fix12 CS115 L00–L11 (sửa theo R8_CS115_A) — 2026-11-17

Không chạy build/tts/asr/audit_all/git/docker. `tools/lv.py render` chạy được (không bị từ chối).

## Nguyên tắc: ưu tiên chỉ đổi `show`
Mọi sửa trên màn hình chỉ đổi `show` (giữ bộ nhớ đệm giọng đọc). Lời đọc chỉ đổi ở: (a) mỗi bài L00–L09, L11 thêm 1 step "đọc trước (tiếp)" có đúng 1 câu mới "Còn vài mẩu mã nữa, đọc kỹ ở bảng." (9 từ); (b) cắt vế ở 1–3 câu ở L01, L02, L03, L04, L06, L07, L08, L09 để bù (không đổi số câu, không đổi `focus`); (c) L10 adadelta.0: "dùng D" thành "dùng q".

## Việc đã làm
1. R1 (L00–L11): thêm hai dòng ghi chú dưới bảng R1: "Git Bash là cửa sổ gõ lệnh trên Windows (đi kèm Git for Windows): vào thư mục bài làm, bấm chuột phải vào chỗ trống, chọn Open Git Bash here." và "kho = thư mục chứa mã nguồn khoá học bạn được giao (có thư mục labs); chưa có kho thì chỉ chạy python <tên>.py và so với kết quả mong đợi" (đúng tên tệp từng bài). Khung đã xem (L00): vừa khung, không tràn.
2. Bảng R3 "đọc trước (tiếp)" (≤ 4 hàng, step sau bảng có `clear: true`), mỗi hàng có ví dụ đã tính lại: L00 f-string `f"w={w}"` (khớp đầu ra mong đợi `w=2 P=16 …`) + `if`; ví dụ hàng `print("w =", w)` ghi rõ "có dấu cách"; L01 `sum/zip`, comprehension, `join`+`str`, f-string; L02 `sum` ô tích, `join`+`str`, `if dt == 0`; L03 f-string, `if/elif/else`, comprehension `zip`; L04 `join`+`str`, comprehension, `sum/zip`; L05 f-string, `for`, `if`; L06 `x**2`, f-string, so sánh in True/False; L07 `x**2`, comprehension, `sum`; L08 `for … in ham.items()`, f-string; L09 f-string, `round` comprehension, so sánh; L11 comprehension, f-string, `if … and`. Ký tự "·" trong chữ đổi thành "nhân" (lint notation).
3. B/vừa: L03 link_inverse "định thức ad − bc (bài 2)"; L07 symm "chuyển vị = lật qua đường chéo, đổi hàng thành cột"; `**` ở L06/L07 (hàng R3); `import math` = nạp thư viện toán, `math.sqrt/gcd/isqrt` (hàng R2 của L05, L06, L10 sửa trên màn hình); L11 "xác định dương = mọi trị riêng dương, nhớ từ bài 8" và "BFGS: một cách xấp xỉ Hessian".
4. SHOULD: L02 cỡ `M×N`, `N×P` thành m, n, p chữ thường (màn hình; lời đọc giữ chữ cái, âm không đổi); L05 thêm "nếu (b, λ − a) = (0, 0) thì dùng (λ − d, c); đề này b = 2 ≠ 0" trong hộp "Nếu kẹt" (step thêm `clear: true` vì tràn); L07 ghi chú "đồng nhất với ∂²f/∂x_i∂x_j khi đạo hàm cấp 2 liên tục (H đối xứng)"; L08 Sarrus tô ba đường đi lên màu đỏ (tích, và hai ô không trùng đường xuống), ba đường đi xuống màu lục; L09 "≈ 5.2 (máy ghi 5.199999999999999; dùng round)"; L10 `D_k` → `q_k` (màn hình + một câu lời đọc "nó dùng q"); L00 SVG nhãn "w = 3,4: tổng 0,16" dời sát chấm; L11 alternatives.3 thêm dòng "đạo hàm của ½ dᵀAd theo d là A d khi A đối xứng".
5. Chưa làm (ghi rõ): L11 newton_1d hình parabol đơn giản (cần thêm SVG và có nguy cơ vượt khung; để dành); `hội tụ` (L09, L10), `đường chéo`, `khả nghịch`, `ma trận vuông` và các mục yếu khác của reader.

## Bài đã đổi / đổi `say` / render
- Đổi `show` (cả 12): L00, L01, L02, L03, L04, L05, L06, L07, L08, L09, L10, L11.
- Đổi `say` (cần TTS lại các step này): L00 (step R3 mới), L01 (R3 + verify.1), L02 (R3 + transpose.0), L03 (R3 + rowops.2, verify.0, verify.1), L04 (R3 + pitfalls.1), L05 (R3), L06 (R3 + prereq.2), L07 (R3 + pitfalls.1), L08 (R3 + pitfalls.0, pitfalls.1, quiz.0), L09 (R3 + pitfalls.0, pitfalls.1, recap.1), L10 (adadelta.0), L11 (R3). Các step khác giữ nguyên lời.
- Từ lời đọc: L00 2298, L01 2299, L02 2300, L03 2297, L04 2298, L05 2298, L06 2296, L07 2298, L08 2300, L09 2300, L10 2277, L11 2297 (≤ 2300).
- Render `tools/lv.py render` đủ 12 bài: 0 vấn đề (L05 lần đầu tràn ở step "Nếu kẹt" → thêm `clear: true`, render lại 0). Khung đã xem: L00 R1/R2. Chưa xem tay khung L08 (Sarrus màu), L11 alternatives.3, L10 adadelta (render báo 0 vấn đề).

## Cổng (2026-11-17)
lint L00–L11: 0 FAIL, 0 WARN. `verify_cs115_af2`: 184 PASS · 0 FAIL (một lần chạy song song với render báo 1 FAIL tạm, chạy lại sạch). `screen_code.py check --course CS115`: PASS 59 · FAIL/STALE/MISSING/ORPHAN 0 (sổ đổi khoá bằng Edit: `practice 3 0` → `4 0` ở L00–L09, L11; `practice 2 0` → `3 0` ở L03, L04, L08; L10 giữ). `lab_gate CS115`: 25 PASS · 0 FAIL. curriculum: 0 lỗi; `test_e52`: 0 FAIL; `asr_reviewed`: 0 mục mất.
