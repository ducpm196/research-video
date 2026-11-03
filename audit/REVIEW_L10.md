# L40–L43 (làm trống `not_included`) + bài L10 “Tối ưu thích nghi” — 2026-10-24

Phạm vi (yêu cầu người dùng): “bổ sung đầy đủ thêm các topic not_included đang cân nhắc, hoàn thiện giáo án đầy đủ, chuẩn xác. Sau đó tiếp tục làm video bài giảng tiếp theo.”
Nhãn: OBSERVED = chạy trong phiên này; CITED = nguồn ngoài có ngày truy cập; INFERRED = suy luận, chưa kiểm.

## 1. Nút thắt hợp đồng

| ID | Chưa xác định / chưa kiểm | Việc phụ thuộc | Bằng chứng đóng | Trạng thái |
|---|---|---|---|---|
| B35 | `not_included` còn gì | Lộ trình | Còn UMAP (đang gộp L32) và Transformer/attention, mô hình sinh → thành L40–L43; `not_included: []` | CLOSED |
| B36 | Phát biểu toán trong `fix` L40–L43 | Các bài mở rộng | `ext2_checks.py` TẤT CẢ PASS (OBSERVED 15:5xZ) | CLOSED |
| B37 | Trích dẫn ngoài nguồn | L40–L43, L10 | WebSearch 2026-10-24; hội nghị của Transformer (NeurIPS 2017) và DDPM (NeurIPS 2020) chỉ nguồn thứ cấp; RMSprop không có bài báo (bài giảng Coursera, số tiểu mục 6e/6.5 mâu thuẫn → không ghi); −log 4 của GAN không có trong nguồn tìm được → tự kiểm sympy | CLOSED (ghi rõ phần thứ cấp) |
| B32 | Cách đọc Nesterov, Adagrad, RMSprop, Adadelta | Lời đọc L10 | 2 lượt probe, xem §3 | CLOSED Nesterov, Adadelta; **OPEN** Adagrad, RMSprop |
| B34 | Cách đọc “Newton” | L11 | Chưa probe; L10 bỏ chữ khỏi lời đọc | OPEN (ghi vào `fix` L11) |
| B26, B20 | “mô-men-tum”, “ép-xi-lôn”; “logarit” | L09–L10; L12 | — | OPEN (không đổi) |

## 2. Lộ trình (OBSERVED `lv.py curriculum` → 44 bài, 11 đã có đặc tả, 0 lỗi)

L40 UMAP, L41 Attention & Transformer, L42 VAE & GAN, L43 Diffusion — nguồn và kiểm: `audit/SYLLABUS_CS115.md` §8. L00 cập nhật “bài 34–43: mở rộng tuỳ chọn” và đã build lại (654,1 s, verify PASS).

## 3. Phát âm (OBSERVED 16:05Z, 16:16Z; 3 ngữ cảnh × small + medium, ngưỡng 5/6, đối chứng âm 0/6 cả 4 từ)

| Từ | Đọc thô | Đã thử | Chọn | Kết quả |
|---|---|---|---|---|
| Nesterov | 0/6 (“Nestle Vault”) | Nê-xtê-rốp 0, Nét-xtê-rốp 0, Nê-xtơ-rốp 0, Nét-tơ-rốp 0 | **Nê-sờ-tê-rốp** | 5/6 — CLOSED |
| Adadelta | 0/6 (“AdaData”) | A-đa-đen-ta 4, A-đa-đen-tà 4 | **A-đa-đeo-ta** | 5/6 — CLOSED |
| Adagrad | 0/6 (“A đắt gác”) | A-đa-grét 1, Ê-đa-grát 0, A-đa-gơ-rát 1 | A-đa-grát | chặt 1/6, tiền tố 5/6 — **OPEN** |
| RMSprop | 0/6 (“mơ pop”) | R M S prop 1, a-rờ-em-ét-prốp 0, ar-em-ét-prốp 0 | a-rờ em ét prốp | 2/6 — **OPEN** |

Giảm rủi ro cho hai từ OPEN: lời đọc chỉ nói tên ở 3 câu mỗi từ (mở đầu, giới thiệu, tổng kết); các chỗ khác dùng tên gọi tiếng Việt “cách cộng dồn” (Adagrad) và “cách trung bình trượt” (RMSprop) — trên màn hình vẫn có tên đầy đủ.

## 4. L10: thiết kế và kiểm (OBSERVED)

- Ví dụ gốc: thung lũng dẹt f = x² + 25y² — GD tách thành hai hệ số (1 − 2η), (1 − 50η); η = 0,035: x chậm (0,93), y đổi phía (−0,75); η = 0,1: y phân kỳ (−4); tốc độ học riêng 0,25 và 0,01 cho cả hai hệ số 0,5.
- Nesterov (dạng Sutskever, cùng cách viết Momentum của tài liệu): bước 2 = 0,813 (Momentum 0,84); 30 bước: vượt tối đa 4,06 so với 4,81, cách đáy 0,13 so với 0,60.
- Adagrad: bước đầu trên thung lũng (0,1; 0,1) → (0,9; 0,9) (GD văng tới y = −4); điểm mạnh với đặc trưng hiếm (bước 1 so với 0,5); điểm yếu: gradient không đổi → bước η/√k → 0.
- RMSprop: bước η/√(1 − 0,9ᵏ) → η; bước đầu 3,16η do không hiệu chỉnh độ lệch (nối lỗi 4 bài 9).
- Adadelta: bước đầu ≈ −0,0032 với ε = 10⁻⁶ — không cần η nhưng phụ thuộc ε. Ký hiệu bước viết b_k (Δ đã là “định thức” ở bài 8 — lint chặn).
- So sánh 10 bước: η = 0,1 → RMSprop 0,027 / Adam 0,15 / Adagrad 7,97; η = 0,5 → Adagrad 0,0003 / RMSprop 0,009 / Adam 0,85 → thứ hạng đổi theo η (sửa A18 theo hướng chứng minh bằng số).
- Mọi số mô phỏng có check **mô phỏng lại trong biểu thức** (không chép số) và đối chứng âm: đổi số kỳ vọng → cả 4 check thành False.
- Xem bằng mắt: khung 23 (bảng thung lũng), 30 (Nesterov), 42 (Adagrad — sửa: tiêu đề hiện “G_k”), 46 (đặc trưng hiếm), 56 (RMSprop), 63 (Adadelta), 75 (so sánh), 97 (quiz).

## 5. Luật mới chặn tái phát

- **E25** (FAIL): tiêu đề scene có `_ ^ \ $` (lỗi thật L09, L10). Quét 11 bài: chỉ L10 dính, đã sửa. Ca thử trong fixture.
- **E26** (WARN): check chỉ so hai hằng số chép tay (lỗi thật bản nháp L10). Quét 11 bài: 0. Ca thử trong fixture.

## 6. Kiểm toàn bộ

ASR L10 qua 3 lượt (OBSERVED): lượt 1 — 108 câu, TB 0,928, **29 cờ**. Phân loại: (a) ASR chép đúng chính tả tiếng Anh của tên đã đọc Việt hoá (eta, epsilon, Adadelta…) → thêm bí danh vào `vi_text.ASR_ALIASES` CHỈ cho cách viết đúng (biến thể nghe sai vẫn bị cờ); (b) chữ g → “d/dê/dây” 12 khung (giọng Bắc gi = d) → `LETTER_HEARD["g"]`, chỉ ở vị trí gióng hàng; (c) nghe sai thật → viết lại 10 câu, giảm số lần đọc tên. Lượt 2: TB 0,956, 7 cờ. Lượt 3: 6 cờ, đều ghi `asr_reviewed` (Nesterov ×3, Adagrad/RMSprop ×2 — B32; “Ada Delta” tách hai chữ ×1), **0 chưa xem xét**.
Kiểm hồi quy bí danh mới: L09 chạy lại ASR → 0 cờ, TB 0,963 → 0,968 (không che lỗi nào đã có).

OBSERVED 16:54:19–16:54:53Z:

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
| L09 | 724,33 s | PASS | 0 |
| **L10** | **615,9 s (10,3 phút)** | **PASS** | **0** |

`tests/test_lint.py` 0 FAIL (gồm E25, E26 mới) · lint 11 bài 0 FAIL 0 WARN · `audit/verify_cs115_tex.py` 59/59 · `curriculum` 44 bài, 11 có đặc tả, 0 lỗi · không còn tiến trình pipeline.

## 7. Còn mở (NOT_VERIFIED)

- Người nghe: “A-đa-grát”, “a-rờ em ét prốp” (B32), “mô-men-tum”, “ép-xi-lôn” (B26), các câu cũ L01 (8), L02 (8), L04 (1), L05 (4), “Hết-sen” L07–L08.
- B34 “Newton” trước L11; B20 “logarit” trước L12; ICA số tập/trang.
- L01, L02 > 15 phút (có từ trước). Hiệu quả sư phạm: chưa đo.
