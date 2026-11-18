# fix12 CS115 L12–L21, L44–L46 (sửa theo R8_CS115_B.md) — 2026-11-17

Nguyên tắc: CHỈ đổi `show` (và một dòng `focus` ở L12) để giữ bộ nhớ đệm giọng đọc. **Không bài nào đổi `say`** (so từng step với bản trước fix12: 13/13 giống hệt; `asr_reviewed` 0 mục mất ở 13/13). Số từ lời đọc không đổi (L12 2299, L13 2300, L45 2300 …). Không chạy build/tts/asr/audit_all/git/docker; có chạy `tools/lv.py render`. Script sửa nằm ở scratchpad; bản sao trước sửa nằm ở `scratchpad/c115b/before_fix12/`.

## Đã làm
| Mục | Bài | Việc (chỉ `show`) |
|---|---|---|
| (1) Git Bash | cả 13 | đoạn "Đọc trước khi làm": "Git Bash là cửa sổ gõ lệnh trên Windows (đi kèm Git for Windows): vào thư mục bài làm, bấm chuột phải vào chỗ trống, chọn Open Git Bash here, gõ python <tên>.py rồi Enter"; chân trang chấm bài thêm "Kho = thư mục chứa mã nguồn khoá học bạn được giao (có thư mục labs); chưa có kho thì chỉ chạy python tệp.py và so với kết quả mong đợi" (cùng chữ như ACB/CS112/CS115 A) |
| (2) L12 | practice.0 | hàng bảng "đạo hàm hai phía: lấy hai điểm cách đều hai bên x một đoạn h" cho `(f(x + h) - f(x - h)) / (2 * h)` (ví dụ x², x = 1, h = 0,1 cho 2); để đủ ≤ 4 hàng, gộp `math.log(0.2)` và `math.exp(s)` thành một hàng (focus: hai câu cùng chỉ hàng đó). Hàng đạo hàm không có câu đọc riêng (không đổi `say`) |
| L14 | practice.0 | hàng `math.erf(...)`: "erf là hàm sai số; Z chuẩn tắc (= N(0, 1), độ lệch chuẩn 1); P(−z ≤ Z ≤ z) = erf(z/√2); chia √2 vì erf ứng với e^(−t²), tức độ lệch chuẩn 1/√2" (đã kiểm: erf(1/√2) = 0,6827); ô mã không gãy dòng (nowrap) |
| L15 | eigen.1, spd.0 | "phương sai theo một hướng = phương sai của hình chiếu dữ liệu lên hướng đó" ngay lần đầu |
| L16 | proof.1 | "hai vector riêng trực chuẩn tạo một cơ sở của mặt phẳng, nên mọi u viết được như sau: u = a·v₁ + b·v₂" |
| L17 | mle_normal.0, categorical.0 | bước trung gian: ln của tích = tổng các ln (công thức từng số hạng); giải hệ: θ₁ = 5/2·θ₃, θ₂ = 3/2·θ₃, thế vào tổng 1 ⇒ θ₃ = 1/5 = 2/10, θ₁ = 5/10, θ₂ = 3/10 |
| L18 | closed_form.1 | "hạng = số cột độc lập; hạng 2 < 3 nên det = 0, không khả nghịch" |
| L19 | lasso.0 | tiêu đề cột "nghiệm w khi phạt L2 (2w²)" và "nghiệm w khi phạt L1 (2\|w\|)" |
| L20 | why_not_mse.4, entropy.0, gradient.0, practice.0 | "lồi = đồ thị cong lên như cái bát (đạo hàm bậc hai ≥ 0 mọi nơi); đạo hàm bậc hai âm ở đâu đó nghĩa là không lồi"; quy ước 0·ln 0 = 0; dòng "∂z/∂w = x (vì z = wᵀx + b) nên ∂BCE/∂w = (ŷ − y)x"; ô mã sigmoid không gãy dòng |
| L21 | quymo.1 | "sai số chuẩn = độ lệch chuẩn của ước lượng, ở đây √(p(1−p)/k) với p = 0,9" |
| L45 | prereq.0, stage1.0, hook.0, stage3.0, stage3.1, stage5.0, paths.0 | ε = hằng số rất nhỏ cộng vào mẫu số để không chia cho 0 (prereq và stage1); "lồi (đồ thị cong lên như cái bát)" ở hook và stage3; stage3.1 có dòng "Tính tay": s_mới = 0,1·s_cũ + 0,9·g²; s₁ = 0,1s₃ + 8,1, s₂ = 0,1s₁ + 0,9, s₃ = 0,1s₂ + 0,9 ⇒ s₁ = 8,199/0,999 ≈ 8,21 (đã kiểm: s₂ ≈ 1,72, s₃ ≈ 1,07); stage5.0 tiêu đề bảng "mã nhánh chính đọc ngày 2026-11-02; số phiên bản chưa ghi" (KHÔNG kiểm được số phiên bản đầu tiên có `decoupled_weight_decay`, không dùng mạng); paths.0 dời nhãn ① sang phải, không còn bị nét đứt cắt (xem khung 00026) |
| (3) nhãn cột "dòng in ra" | L15, L16, L17, L19, L46 | tiêu đề cột đổi thành "viết trong mã / dòng in ra" (cột có `[[5/2, 2], …]`, `[28/29, …]`, `M.w: [9, 13]` là dòng in) |
| L14 sym_int.1 | | "các cột phủ [0; 0,5], chiều cao lấy ở đầu trái mỗi cột" (đã kiểm: 0, 0,25, 0,5, 0,75 nhân 0,125 = 0,1875) |

## Chưa làm (ghi rõ)
- (4) Hàng nhắc cú pháp lab chưa có trên màn hình (`sum`, `len`, `max`, `zip`, f-string, `round`; L12 vòng lặp nhân và định dạng `1.126e-35` trong de.md): KHÔNG thêm vì mỗi bảng đã đủ 3–4 hàng và thêm hàng có câu đọc nghĩa là đổi `say`; chỉ L12 có hàng đọc `1.126e-35` (đã có). Đề xuất nếu cần: một step riêng "Cú pháp trong lời giải" ở mỗi bài (cần câu đọc mới, phải dựng lại giọng).
- Hiển thị: L17/L20 quiz (tử số phân số chạm viền hộp) và L18 resid_pic (đoạn đỏ ±0,1 nhỏ): chưa chỉnh (cần đổi cỡ công thức/hình; để reader xem lại sau); L46 practice.1 nút "Dừng video…" chồng viền dưới: là lớp phủ của bộ dựng, không nằm trong `show`, chưa làm.
- Hàng đạo hàm hai phía của L12 và đoạn định nghĩa mới nằm trên màn hình nhưng KHÔNG được đọc thành lời (không đổi `say`).

## Cổng (chạy thật, 2026-11-17)
- `tools/lv.py lint` 13/13 bài: 0 FAIL, 0 WARN. `tests/test_e52.py`: 0 FAIL. `audit/verify_cs115_af2.py`: 184 PASS · 0 FAIL.
- `tools/lv.py render` cả 13 bài (đều thuộc hàng đã dựng nên bắt buộc): lượt đầu TRÀN ở L12 (đoạn đọc trước), L13, L15, L16, L21 (bước "Nếu kẹt" nằm dưới kết quả + chân trang dài hơn); đã thêm `clear: true` cho "Nếu kẹt" (L13, L16, L21), thu cỡ chữ chân trang (L13, L15, L16, L21) và đoạn mở L12 (0,85em); lượt cuối **0 vấn đề ở 13/13 bài**. Khung đã xem: L12 00115, L14 00089, L45 00058 và 00026.
- `screen_code check --course CS115` và `lab_gate CS115`: screen_code: 34 khối — PASS 59 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0; lab_gate: 25 PASS · 0 FAIL (196 lab). Không đổi khối mã, không đổi lab.

## Bài đổi (để requeue) và loại đổi
Cả 13 bài chỉ đổi `show` (L12 thêm đổi `focus`, L45 thêm đổi SVG ở paths): L12, L13, L14, L15, L16, L17, L18, L19, L20, L21, L44, L45, L46. KHÔNG bài nào đổi `say`. Chưa kiểm render: không (13/13 đã render 0 vấn đề).
