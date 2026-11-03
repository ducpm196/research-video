# Phần mở rộng L34–L39 + bài L09 “Gradient Descent, SGD, Momentum & Adam” — 2026-10-24

Phạm vi (yêu cầu người dùng): “bổ sung đầy đủ thêm các topic đang cân nhắc, hoàn thiện giáo án đầy đủ, chuẩn xác. Sau đó tiếp tục làm video bài giảng tiếp theo.”
Nhãn: OBSERVED = chạy trong phiên này; CITED = nguồn ngoài có ngày truy cập; INFERRED = suy luận, chưa kiểm.

## 1. Nút thắt hợp đồng

| ID | Chưa xác định / chưa kiểm | Việc phụ thuộc | Bằng chứng đóng | Trạng thái |
|---|---|---|---|---|
| B28 | “Các topic đang cân nhắc” = gì | Lộ trình | = các mục `not_included` của bản 3 (CNN, RNN, học tăng cường, UMAP, ICA, autoencoder, boosting) | CLOSED |
| B29 | Thêm bài có làm đánh số lại 10 video đã làm không | L00–L09 | Đặt L34–L39 SAU tổng ôn L33 → không đổi số bài nào; chỉ L00 thêm “bài 34–39: mở rộng tuỳ chọn” | CLOSED |
| B30 | Phát biểu toán trong `fix` L34–L39 có đúng không | Các bài mở rộng sau này | `ext_checks.py` (OBSERVED 14:3xZ): tất cả PASS; 1 câu viết lại cho chính xác (gradient boosting: phần dư chỉ đúng với loss ½(y − ŷ)²) | CLOSED |
| B31 | Trích dẫn ngoài nguồn môn học | L34–L39, L32 (UMAP), L09 (Adam) | WebSearch 2026-10-24: 8/9 xác nhận đủ tạp chí, tập, trang; **ICA (Hyvärinen & Oja 2000): chưa xác nhận số tập/trang** | CLOSED trừ ICA (ghi NOT_VERIFIED trong `source`) |
| B26 | Cách đọc eta, beta, SGD, Adam, Momentum, epsilon | Lời đọc L09 | `l09_probe.py`, `l09_probe2.py` — xem §3 | CLOSED cho eta, beta, SGD, Adam; **OPEN** cho Momentum (đối chứng âm không phân biệt) và epsilon (4/6 < 5/6) |
| B20 | “logarit” | L12 | — | OPEN (không đổi) |

## 2. Lộ trình (OBSERVED: `lv.py curriculum` → 40 bài, 10 đã có đặc tả, 0 lỗi)

L00–L33 như bản 3; thêm **Phần 7 mở rộng tuỳ chọn**: L34 CNN, L35 RNN/LSTM, L36 Boosting, L37 Autoencoder, L38 ICA, L39 Học tăng cường; UMAP gộp vào L32. Chi tiết, nguồn: `audit/SYLLABUS_CS115.md` §7.
Lệnh `curriculum` bắt được L09 `assumes` ký hiệu ŷ và x* mà chưa khai bài tiên quyết → `requires` sửa thành [L00, L06, L08] (bài cũng dùng lại ví dụ của L00 và L08).

## 3. Phát âm (OBSERVED 14:52Z, 14:56Z; 3 ngữ cảnh × small + medium, chấm bỏ dấu, ngưỡng 5/6, có đối chứng âm)

| Từ | Đọc thô | Chọn | Đối chứng âm | Kết luận |
|---|---|---|---|---|
| eta | 1/6 (“y ta”) | ê-ta 6/6 | ê-va 0/6 | CLOSED |
| beta | 6/6 | bê-ta 6/6 | bê-la 0/6 | CLOSED |
| SGD | **0/6 (“đô la Singapore”)** | ét-giê-đê 5/6 | ét gờ bê 0/6 | CLOSED |
| Adam | 6/6 | A-đam 6/6 | A-năm 0/6 | CLOSED |
| Momentum | 6/6 | mô-men-tum 6/6 | **mô-men-tôm 6/6** | OPEN — phép thử không phân biệt |
| epsilon | 0/6 | ép-xi-lôn 4/6 (medium 15/15 mọi cách viết; small chép “FC”) | ép-xi-măng 0/6 | OPEN — cần người nghe |

## 4. L09: kết quả (OBSERVED)

| Hạng mục | Kết quả |
|---|---|
| lint | 0 FAIL, 0 WARN, 47 PASS; 40 phép kiểm sympy; 15 scene; ký hiệu mới: η, β, ε |
| Trích dẫn | 2 step nhắc bài sau (bài 10, 22 — `forward_ref`); 12 câu nhắc bài trước (bài 0, 6, 8), đều nói lại nội dung |
| build + verify | xem §6 |
| ASR lượt 1 | 123 câu, TB 0,952, 9 cờ → viết lại 9 câu (6 do đọc tên chữ cái w/v/g/s → nói bằng lời; 2 câu quá ngắn; 1 câu “SGD” thiếu ngữ cảnh) |

Thiết kế: công thức theo đúng tài liệu (dòng 283–285: w_{k+1} = w_k − η∇f(w_k); SGD với mẫu i; Momentum v_{k+1} = βv_k + η∇f, w_{k+1} = w_k − v_{k+1}); dạng “α·Δw(n − 1)” của slide NN được nêu là cùng công thức (kiểm sympy: v₂ = η(g₁ + βg₀)). Ví dụ chính f = (w − 3)²: suy ra khoảng cách nhân (1 − 2η) mỗi bước → bảng η = 0,05 / 0,25 / 1 / 1,1 (chậm / nhanh / dao động / phân kỳ), điều kiện 0 < η < 1. Hai chiều: dùng lại hàm của bài 8, khoảng cách tới (−1/3, 1/3) giảm một nửa mỗi bước. SGD: dùng lại hai ngôi nhà của bài 0 (gradient trung bình = trung bình gradient, kiểm sympy). Trung bình trượt dạy trước Adam (fix của lộ trình), hiệu chỉnh độ lệch kiểm bằng số (10, 10, 10). Adam: bước đầu dài ≈ η với mọi độ lớn gradient; quên hiệu chỉnh → √10 ≈ 3,16 lần (kiểm sympy). A18 sửa: “phổ biến nhất” là nhận định. Giá trị mặc định của Adam lấy từ bài báo gốc (CITED).

**Xem bằng mắt** (đọc ảnh PNG): khung 21 (ký hiệu — sửa: tiêu đề hiện “w_k” thô), 39 (bảng η — sửa: thêm giải thích trị tuyệt đối), 44 (hai chiều — sửa: “khoảng cách âm”), 59 (SGD — sửa: công thức gãy dòng, tràn bảng), 69 (Momentum — sửa: dòng gãy), 79 (trung bình trượt), 84 + 87 (Adam — sửa: ghi rõ bỏ qua ε, 10⁻⁸ = 0,00000001), 91 (A18), 105 (lỗi 4 — sửa: thiếu η so với lời đọc), 113 (quiz — sửa: dòng gãy). L00 khung bản đồ khoá học (thêm bài 34–39).

## 5. Lỗi gặp trong phiên và cách xử lý

- Heredoc trong Bash làm hỏng chuỗi có `\` (lần này `assert` chặn, file không bị ghi sai) → dùng script tạo qua công cụ Write (đã có trong production.md; lặp lại vì chủ quan).
- Script sinh bằng `sed` (probe lần 2) được kiểm cú pháp bằng `ast.parse` trước khi tin.
- Thêm luật lexicon có thể đổi giọng đọc các bài cũ → chạy `verify` L00–L08: chỉ L00 FAIL (do đã sửa lời bản đồ khoá học, đúng dự kiến), L01–L08 PASS.

## 6. Kiểm toàn bộ

OBSERVED 15:38:48–15:39:24Z:

| Bài | Thời lượng | verify | ASR chưa xem xét |
|---|---|---|---|
| L00 | 654,1 s | PASS | 0 |
| L01 | 1131,97 s | PASS | 8 |
| L02 | 1123,73 s | PASS | 8 |
| L03 | 703,53 s | PASS | 0 |
| L04 | 897,8 s | PASS | 1 |
| L05 | 895,57 s | PASS | 4 |
| L06 | 878,5 s | PASS | 0 |
| L07 | 891,63 s | PASS | 0 |
| L08 | 825,03 s | PASS | 0 |
| **L09** | **724,33 s (12,1 phút)** | **PASS** | **0** (125 câu, TB 0,963; lượt 2 còn 1 cờ “s mũ” → viết lại; lượt 3: 0) |

`tests/test_lint.py` 0 FAIL · lint 10 bài 0 FAIL 0 WARN · `audit/verify_cs115_tex.py` 59/59 · `curriculum` 40 bài, 10 có đặc tả, 0 lỗi · không còn tiến trình pipeline (`Win32_Process`).

## 7. Còn mở (NOT_VERIFIED)

- Người nghe: “mô-men-tum”, “ép-xi-lôn” (B26), cùng các câu cũ của L01 (8), L02 (8), L04 (1), L05 (4), L07–L08 (“Hết-sen”).
- B20 “logarit” trước L12; ICA: số tập/trang của trích dẫn.
- L01, L02 dài hơn 15 phút (có từ trước). Hiệu quả sư phạm: chưa đo.
