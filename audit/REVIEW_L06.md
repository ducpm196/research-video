# Hoàn thiện lộ trình theo nhận xét + rà soát L01–L05 + làm L06 — 2026-10-24

Phạm vi:
1. Kiểm bản nhận xét về độ phủ lộ trình (người dùng dán vào chat) với đề cương và slide môn học, rồi sửa `curriculum/cs115.yaml`.
2. Chạy lại toàn bộ kiểm tra của L01–L05.
3. Làm bài L06 `lessons/L06_jacobian_hessian_chuoi.yaml` → `out/L06/`.

Nhãn: OBSERVED = chạy trong phiên này; CITED = kết quả phiên trước, kèm ngày; INFERRED = suy luận, chưa kiểm bằng máy.
Môi trường: Python 3.13.5 (`.venv`), Windows 11.

## 1. Nút thắt hợp đồng (contract bottleneck)

| ID | Chưa xác định / chưa kiểm | Việc phụ thuộc | Bằng chứng đóng | Trạng thái |
|---|---|---|---|---|
| B13 | Bản nhận xét nói lộ trình thiếu những gì “đề cương yêu cầu”, nhưng không trích dòng nào của đề cương | Sửa lộ trình | Đọc đề cương CS115.O11 (sha256 `0d289ba3cc37ace4…`) và 12 PDF môn học bằng `pdftotext` + `grep`. Bảng kiểm từng ý ở `audit/SYLLABUS_CS115.md` §3. Kết quả: 4 ý sai hoặc thiếu nguồn (KKT/Lagrange, t-SNE, tỉ lệ điểm 40/60, CG/LM nằm ở slide chứ không phải đề cương); 1 nhóm bị bỏ sót (Nesterov, Adagrad, RMSprop, Adadelta, MLP, Batch norm, cross-validation, hyperparameters, Decision Tree/RF) | CLOSED |
| B14 | Thêm bài vào giữa lộ trình có làm lệch số “bài N” mà video cũ đã đọc không | Số hiệu bài | `grep` trên `lessons/*.yaml`: L02–L05 đọc “bài 7, 8, 11, 13, 15” → giữ nguyên số L00–L16; bài mới L17–L26 chèn đúng vị trí học. `lv.py curriculum` → 27 bài, 0 lỗi; đối chứng âm (đặt L19 trước L13) → FAIL đúng | CLOSED |
| B12 | Cách đọc “Hessian” | ~25 câu L06 | `h_probe.py` + `h_probe2.py` (13 cách viết × 4 ngữ cảnh × small + medium, có đối chứng âm). Cách cũ “Hét-xi-ần” bị medium nghe “hết xương” 3/4, trùng đối chứng âm “Hét-xương”. **“Hết-sen”**: 8/8 đúng nguyên văn ở cả hai mô hình; đối chứng âm “Hết-sương” không bị nghe thành “sen” | CLOSED (phần máy) — độ tự nhiên: NOT_VERIFIED bằng tai |
| B15 | Tính kết hợp (AB)C = A(BC): quy tắc chuỗi dạng ma trận cần nó, nhưng bài 2 chưa dạy | Phân cảnh chain_mat | Dạy và thử bằng số ngay đầu chain_mat (cả hai cách đều ra 12); sympy check | CLOSED |
| B16 | Câu L07 “bài sau” và các ghi chú `fix` của L07 | L07 | Không đổi. A1, A2, A4 đã có từ trước; L06 đã dạy Hessian = Jacobian của gradient và tính đối xứng | OPEN → L07 (không chặn L06) |

## 2. Lộ trình sau khi sửa (OBSERVED)

Trước đây có 17 bài, nay có **27 bài** (`lv.py curriculum` → 0 lỗi, 03:35:39Z). Thứ tự học:

L00 … L08 → **L17** (Nesterov, Adagrad, RMSprop, Adadelta) → **L18** (tối ưu lồi, Newton, quasi-Newton/CG/LM) → L09 … L13 → **L19** (quá khớp, L1/L2, cross-validation) → L14, L15 → **L20** (MLP, Batch norm, hyperparameters) → **L21** (Lagrange/KKT, ngoài đề cương) → **L22** SVM → **L23** LDA → **L24** phân cụm → **L25** GMM + EM → **L26** cây quyết định → **L16** tổng ôn (dời xuống cuối).

Không thêm: t-SNE (không có trong nguồn nào); NMF (chỉ có ở slide 2024 — **quyết định mở cho người dùng**).

Rà soát nguồn có thêm 2 mục và 4 phép kiểm:
- **A23**: dòng 410, LDA thiếu vế phân tán trong lớp; phép kiểm T16.
- **A24**: dòng 408, inertia là tổng *bình phương* khoảng cách; phép kiểm T17.
- **T18**: Ridge làm XᵀX + λI khả nghịch.
- **T19**: lề của SVM bằng 2/‖w‖.

## 3. Lỗi tìm thấy khi làm L06 (đã sửa)

| # | Lỗi | Phát hiện bằng | Sửa |
|---|---|---|---|
| G1 | 13 chỗ ngắt dòng giữa công thức, ví dụ “= 24 tại x =⏎1” hay “(vì⏎đạo hàm…)”; ma trận phân số chật | Xem 57 khung cuối | Mỗi ý một `<p>`, công thức dài dùng `$$`, thêm `\\[14pt]` giữa hai hàng ma trận |
| G2 | Câu 3 bài tự làm dùng chữ `a` mà bảng chưa định nghĩa (luật 16) | Xem khung | Ghi “Trong: a = x² + 1” |
| G3 | Lỗi 4: lời giải thích lẫn một con số thừa | Đọc lại khi soạn | Viết lại; thêm sympy check cho 0,5 |
| G4 | Bản dựng đầu dài 15,1 phút (906 s) | `build` | Viết gọn 15 câu → 14,3 phút |
| G5 | 22 câu bị ASR gắn cờ | `lv.py asr` | Thêm 7 bí danh chính tả gốc, quy tắc đồng âm giọng Bắc gi/d và s/x (chỉ áp ở vị trí đã gióng hàng), J → “di”; viết lại 10 câu (chữ cái D, W; “vuông → vùng”; tên đứng đầu câu). Kết quả: 3 câu còn cờ, đã ghi lý do |
| G6 | Gọi TTS một lần bị lỗi `NoAudioReceived` | `tts` | `build` đọc lại câu đó: 0 lỗi |

## 4. Bằng chứng (OBSERVED, `checked_at` lấy từ đầu ra công cụ)

| Kiểm tra | Lệnh | Kết quả |
|---|---|---|
| Tự kiểm công cụ | `tests/test_lint.py` | 0 FAIL (03:35:44Z); thêm 5 ca E17, trong đó 2 đối chứng âm (khác thanh “giá”, khác nguyên âm “sắp” không bị coi là đồng âm) |
| Lint L01–L06 | `lv.py lint` | 0 FAIL, 0 WARN cả 6 bài; L06 có 42 phép kiểm sympy |
| Verify L01–L06 | `lv.py verify` | PASS cả 6 bài: 1121,73 s; 1114,1 s; 902,9 s; 873,9 s; 851,07 s; 857,67 s |
| Audit nguồn | `audit/verify_cs115_tex.py` | `TOTAL=56 PASS=56 FAIL=0` (03:35:38Z). T16 lượt đầu FAIL do dữ liệu thử sai; đã sửa dữ liệu, giữ nguyên kỳ vọng |
| Lộ trình | `lv.py curriculum` | 27 bài, 6 có đặc tả, 0 lỗi (03:35:39Z) |
| Video L06 | `lv.py build` | 857,67 s = 14,3 phút; 151 khung, 15 chương |
| Khớp tiếng–hình L06 | `sync_check.py` (9 điểm) | 0 lệch (03:35:36Z) |
| ASR L06 | `lv.py asr` (small + medium) | 151 câu, độ khớp trung bình 0,967; 3 câu gắn cờ, 0 câu chưa xem xét (03:34:56Z) |
| ASR L01–L05 sau khi đổi `vi_text` | `lv.py asr` | Số câu chưa xem xét: 8 / 8 / 1 / 4 / 0. L01 giảm từ 9 xuống 8 nhờ quy tắc gi/d, s/x |
| Khung đã xem bằng mắt | Read ảnh ghép | Lượt 1: 57 khung cuối của mọi bước. Lượt 2: 38 khung của 9 phân cảnh đã sửa |

## 5. Còn mở (NOT_VERIFIED)

- **Cần người nghe ở L06**: cách đọc “Hết-sen” cho “Hessian” có tự nhiên không, vì ASR không phân biệt được e/ê. Ba câu trong `asr_reviewed` (khung 105, 109, 146). Các câu có “phẩy” (đạo hàm, số thập phân).
- **Câu chờ người nghe của bài cũ**: L01 8, L02 8, L03 1, L04 4.
- **Quy tắc đồng âm gi/d, s/x** dựa trên phát âm giọng Bắc của giọng đọc NamMinh. Đây là INFERRED từ đặc điểm phương ngữ; nó khớp với mọi bản chép quan sát được, nhưng chưa có người nghe xác nhận.
- **NMF**: chờ người dùng quyết định có thêm bài không.
- **L21 (Lagrange/KKT)** nằm ngoài đề cương: người dùng có thể bỏ.
- **Hiệu quả sư phạm** với người học thật: chưa đo.
