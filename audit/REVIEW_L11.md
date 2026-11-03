# Bài L11 “Tối ưu lồi & phương pháp Newton” — 2026-10-24

Phạm vi (yêu cầu người dùng): “Dựa vào skill và source code và những gì đã có, tiếp tục làm video bài giảng tiếp theo.”
Nhãn: OBSERVED = chạy trong phiên này; CITED = nguồn ngoài có ngày truy cập; INFERRED = suy luận, chưa kiểm.

## 1. Nút thắt hợp đồng

| ID | Chưa xác định / chưa kiểm | Việc phụ thuộc | Bằng chứng đóng | Trạng thái |
|---|---|---|---|---|
| B34 | Cách đọc “Newton” | Lời đọc L11 (36 lần xuất hiện trong đặc tả) | Probe 3 ngữ cảnh × small + medium (§2); ASR toàn bài: **12/12** câu có “Newton” được cả small lẫn medium chép “Newton” | CLOSED ở mức ASR-checked; chưa nghe bằng tai |
| B38 | Cách đọc “Levenberg-Marquardt” | Lời đọc cảnh `alternatives` | Probe: thô 1/6, “Lê-ven-béc Mác-ca” 0/6, “Lơ-ven-béc Mác-cát” 0/6 | CLOSED bằng cách **không đọc**: tên chỉ hiện trên màn hình; lời đọc dùng tên mô tả “bình phương tối thiểu có giảm chấn” (damped least squares, CITED §4) |
| B39 | Trích dẫn ngoài nguồn môn học | Trường `source` của L11 | WebSearch 2026-10-24 (§4) | CLOSED, ghi rõ phần chỉ có nguồn thứ cấp |
| B26, B20, B32 | “mô-men-tum”, “ép-xi-lôn”; “logarit”; Adagrad, RMSprop | L09–L10; L12 | L11 không đọc các từ này (lời giới thiệu bài 12 nói “hàm mũ e mũ x và hàm ngược của nó”, tránh “logarit”) | OPEN (không đổi) |

## 2. Phát âm (OBSERVED 17:07:02Z, `scratchpad/l11_probe.py`, ngưỡng 5/6, đối chứng âm 0/6)

| Từ | Cách viết đã thử | Kết quả | Quyết định |
|---|---|---|---|
| Newton | “Newton” 2/6, “Niu-tơn” 3/6, “Niu tơn” 3/6; đối chứng “Niu-xơn” 0/6 | medium chép đúng “Newton” 3/3 với mọi cách viết; small chép theo âm Việt (“nêu tân”, “nưu tầng”) | lexicon `Newton → Niu-tơn` (cách phiên âm phổ thông: INFERRED, 1 nguồn web); bí danh ASR `newton` |
| Levenberg-Marquardt | thô 1/6, “Lê-ven-béc Mác-ca” 0/6, “Lơ-ven-béc Mác-cát” 0/6; đối chứng “… Mác-tin” 0/6 | không cách nào đạt ngưỡng | không đọc tên (B38) |
| parabol | không probe riêng; ASR toàn bài lượt 1: 7 câu, cả hai mô hình chép “parabon” / “para-bôn” / “parabola” | đúng âm Việt pa-ra-bôn | `foreign_ok` + bí danh `parabon`, `parabola` (chỉ dạng viết đúng âm) |

Kiểm hồi quy: không bài L00–L10 nào có “Newton” trong lời đọc hay “parabol” (grep OBSERVED), nên luật và bí danh mới không đổi video cũ.

## 3. ASR (OBSERVED)

- Lượt 1 (17:36:51Z): 98 câu, TB 0,944, **13 cờ**. Phân loại:
  - (a) “parabol” → “parabon”: thêm bí danh.
  - (b) câu ngắn bị nghe sai thật: “Thứ ba, quá đắt.” → “Quả Đắc”; “Newton có ba rủi ro.” → “rũi cho”; “cái bát” → “kái bác”; “âm gradient” → “amgradian”. Đã viết lại 4 câu (gộp câu, thêm ngữ cảnh).
  - (c) cặp âm dễ lẫn: xấp/sắp, xen/xem, đáy/đấy, kép/kết.
- Lượt 2 (17:40:46Z): 97 câu, TB 0,959, 5 cờ, tất cả thuộc nhóm (c) → ghi vào `asr_reviewed` kèm lý do. Lượt 3 (17:41:12Z): **0 câu chưa xem xét**.

## 4. Nguồn và sửa nguồn

- Nguồn môn học:
  - DC23 Chương 3 (tối ưu lồi; Newton và Gradient Descent).
  - Slide NN “Advanced algorithms”: Newton Δw = −H⁻¹g; quasi-Newton ước lượng H⁻¹; Hessian mạng nơ-ron có thể suy biến; conjugate gradient; Levenberg-Marquardt H ≈ JᵀJ khi hàm sai số là tổng bình phương.
- CITED (WebSearch 2026-10-24, no revision given):
  - Gradient liên hợp: Hestenes & Stiefel, *J. Res. NBS* 49 (1952) 409–436 (trang NIST).
  - Levenberg, *Q. Appl. Math.* 2 (1944) 164–168.
  - Marquardt, *J. SIAM* 11 (1963) 431–441. Tên bài có hai cách ghi; chỉ ghi số tập/trang.
  - BFGS: 4 bài báo năm 1970 (Fletcher; Goldfarb; Shanno, trang 647–656/657 chưa thống nhất; Broyden). Chỉ ghi “1970”, không ghi trang.
  - “damped least squares” lấy từ Wikipedia và ghi chú bài giảng HMC; đây là nguồn thứ cấp.
- **A4** (tex dòng 266–277): tài liệu kết luận “cực tiểu địa phương”. Bài giảng nói rõ đó là đáy **toàn cục** vì hàm lồi. Khung 33 đã xem.
- **A5** (tex dòng 138): Cross-Entropy “đảm bảo địa hình lồi”. Bài giảng nêu là Lỗi 4: điều này chỉ đúng khi mô hình tuyến tính theo trọng số.

## 5. Thiết kế và kiểm toán học (OBSERVED, `scratchpad/l11_nums.py` + 37 check trong đặc tả)

- Dây cung:
  - (w − 3)² có f(3) = 0 ≤ 9, nên lồi.
  - w⁴ − 2w² có f(0) = 0 > −1, nên không lồi.
  - Phép thử f″: 2, và 12w² − 4 = −4 tại w = 0.
- Đáy giả: f = w⁴ − 2w² + w có đáy địa phương 0,84 (f ≈ −0,07) và đáy toàn cục −1,11 (f ≈ −2,06). Mô phỏng GD với η = 0,05, 200 bước, xuất phát từ w = 1, dừng ở 0,84.
- Newton một chiều:
  - (w − 3)² tới đáy sau 1 bước.
  - w² + w⁴/4: 0,4 → 0,052 → 0,00014 → 2,6·10⁻¹².
- **Sửa trong lúc làm:** bản nháp ghi “số chữ số 0 gấp đôi mỗi bước” (hội tụ bậc hai). Ví dụ này thực ra hội tụ **bậc ba** vì f‴(0) = 0, cụ thể w_{k+1} = 2w³/(2 + 3w²), số chữ số 0 là 1 → 3 → 11. Đã sửa lời giảng thành số quan sát được và thêm check đếm chữ số 0.
- Newton nhiều chiều (giải hệ bằng phép khử, ký hiệu **d**, không dùng Δ):
  - Thung lũng bài 10: d = (−1, −1), tới đáy sau 1 bước.
  - Hàm bài 8: d = (−1/3, 1/3), tới đáy sau 1 bước; ∇f tại điểm mới = 0.
- Rủi ro:
  - x² − y² nhảy vào yên ngựa (0, 0).
  - −w² nhảy tới đỉnh.
  - 10⁶ trọng số cho 10¹² ô, tức 8 TB với 8 byte mỗi ô.
- Gradient liên hợp trên thung lũng (số học chính xác): (7500/7813, −12/7813), rồi tới đúng (0, 0) ở bước 2.
- Levenberg-Marquardt:
  - Hessian − JᵀJ = 0 khi phần dư tuyến tính theo tham số; khác 0 khi phi tuyến (sympy).
  - Với c = 10⁴, c·d ≈ −Jᵀr, đúng hướng GD.
- Đối chứng âm (OBSERVED): đổi số kỳ vọng ở 5 check mô phỏng (GD đáy giả, Newton, CG, LM, quiz) thì cả 5 check thành FAIL.
- Xem bằng mắt các khung:
  - 18: SVG dây cung, đã sửa để dây cung chạm đúng đồ thị (tính bằng tham số Bézier);
  - 25: ký hiệu ⇔;
  - 33, 38, 41, 49 (cuối example), 60 (pitfall/rủi ro), 67, 70, 72, 88 (quiz), 97 (cuối).
  - Lỗi bắt bằng mắt đã sửa:
    - dây cung lệch khỏi đồ thị;
    - viết **H** lẫn với **H**_f, đã thống nhất thành **H**_f;
    - từ tiếng Anh “loss”, đã đổi thành “hàm sai số”;
    - trích sai số dòng tex (272 → 266).

## 6. Kiểm toàn bộ

Kết quả ở bảng chạy cuối của `final_check.sh` (báo cáo trong chat, `checked_at` kèm theo).
L11: `out/L11/L11.mp4` 595,67 s (9,9 phút), verify PASS, lint 0 FAIL / 0 WARN, ASR 0 câu chưa xem xét.

## 7. Còn mở (NOT_VERIFIED)

- Người nghe: “Niu-tơn” (small chép theo âm Việt), 5 câu trong `asr_reviewed`. Các mục mở cũ: B26, B32, L01 (8), L02 (8), L04 (1), L05 (4).
- B20 “logarit”: phải probe trước khi viết lời L12.
- ICA: thiếu số tập/trang. Trang bài Shanno 1970 chưa thống nhất (không dùng trong bài).
- L01, L02 dài hơn 15 phút (có từ trước). Hiệu quả sư phạm: chưa đo.
