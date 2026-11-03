# Báo cáo rà soát: `CS115_Toan_cho_Khoa_hoc_May_tinh_Full.tex`

- Phạm vi: toàn bộ 424 dòng của file .tex (bản duy nhất có trong thư mục dự án).
- Phương pháp: (1) chạy lại **mọi ví dụ số và công thức** bằng máy (`audit/verify_cs115_tex.py`, dùng sympy 1.14.0 / numpy 2.5.4);
  (2) đọc từng phát biểu khái niệm và tìm phản ví dụ bằng máy cho những phát biểu nghi sai.
- Nhãn bằng chứng: **OBSERVED** = đã chạy/đọc trong phiên này; **INFERRED** = suy luận, chưa kiểm bằng máy.
- Kết quả máy: `TOTAL=59 PASS=59 FAIL=0`, `checked_at=2026-10-24T04:16:52Z` (thêm T21a–c cho bài 7; trước đó 56/56 lúc 2026-10-24T03:35:38Z với T20a–f cho A3, A13 và L06; trước đó 50/50 lúc 2026-10-24T02:19:34Z với T16–T19 cho A23, A24, A9 và lề SVM khi đối chiếu đề cương — xem `audit/SYLLABUS_CS115.md`; trước đó 46/46 lúc 2026-10-23T22:37:06Z với T15a–f cho A22; trước đó 40/40 lúc 2026-10-23T18:38:13Z với T14a–d cho A21; trước đó 36/36 lúc 2026-10-23T07:02:33Z với T2d cho A20; 35/35 lúc 2026-10-22T03:16:56Z) (lệnh: `.venv/Scripts/python audit/verify_cs115_tex.py`).

## 1. Kết luận nhanh

| Hạng mục | Kết quả |
|---|---|
| Ví dụ số (phép chiếu, cực trị, MLE, backprop) | **Đúng hết**, mọi con số khớp với máy tính (OBSERVED: T1, T5, T7, T11) |
| Công thức (Gram-Schmidt, SVD↔trị riêng, PCA↔SVD, Gaussian, phương trình chuẩn, softmax, momentum, Jacobian) | **Đúng** (OBSERVED: T2–T4, T7c–d, T8a, T10, T12, T13) |
| Phát biểu khái niệm | **3 chỗ sai**, **10 chỗ thiếu điều kiện** (A20, A21, A22 thêm 2026-10-23; A23 thêm 2026-10-24), vài chỗ thuật ngữ/ký hiệu dễ gây nhầm (mục 2) |
| Biên dịch LaTeX | NOT_VERIFIED — máy không có LaTeX; nghi lỗi với emoji (mục 2, A19) |

## 2. Danh sách vấn đề (xếp theo mức độ)

### Sai — sửa trước khi dạy

| ID | Dòng | Tài liệu viết | Vì sao sai / thiếu | Bằng chứng | Cách viết đúng |
|---|---|---|---|---|---|
| A1 | 260 | Hàng “Không xác định”: *“Không thoả các tiêu chuẩn lồi/lõm → Điểm yên ngựa”* | Không thoả Sylvester **không** suy ra yên ngựa. Nếu có trị riêng bằng 0 (nửa xác định) thì phép thử **không kết luận được**. | OBSERVED T6b: f = x⁴ + y⁴ có Hessian tại (0,0) bằng 0 (không thoả Sylvester) nhưng (0,0) là **cực tiểu** | Thêm hàng: “Nửa xác định (có λ = 0) → chưa kết luận, phải xét thêm”. Yên ngựa ⇔ có cả λ > 0 và λ < 0 (với 2×2: det H < 0). |
| A5 | 138 | Cross-Entropy *“đảm bảo địa hình lồi, giúp GD hội tụ toàn cục”* | Chỉ đúng khi mô hình **tuyến tính theo w** (logistic/softmax regression). Với mạng neural, loss vẫn không lồi dù dùng CE. Ngoài ra dữ liệu tách được tuyến tính thì logistic loss không có cực tiểu hữu hạn. | OBSERVED T9: MSE∘sigmoid có đạo hàm bậc 2 âm (−0,120) → không lồi; BCE∘sigmoid ≥ 0 trên lưới → lồi (cho mô hình 1 tham số). Phần mạng neural: INFERRED (kiến thức chuẩn) | “Với logistic/softmax regression, CE cho hàm loss lồi theo w; với mạng nhiều lớp thì không còn lồi.” |
| A7 | 112, 117 | *“làm sai số giảm dần về 0”* | Mục tiêu là **nhỏ nhất**, hiếm khi bằng 0; loss huấn luyện bằng 0 thường là dấu hiệu quá khớp. | INFERRED | “… làm sai số nhỏ nhất có thể.” |

### Thiếu điều kiện — đúng nhưng dễ dùng sai

| ID | Dòng | Vấn đề | Bằng chứng | Bổ sung |
|---|---|---|---|---|
| A2 | 142, 258–259 | Sylvester chỉ áp dụng cho **xác định chặt** và ma trận **đối xứng**. Với nửa xác định, xét các định thức con góc trái trên là **không đủ**. Ghi Δ₁, Δ₂, Δ₃ chỉ đúng cho 3×3. | OBSERVED T6c: M = [[0,0],[0,−1]] có Δ₁ = 0, Δ₂ = 0 (đều ≥ 0) nhưng có trị riêng −1. T6a xác nhận quy tắc đan dấu (−, +, −) cho xác định âm. | Dạng tổng quát: xác định dương ⇔ mọi Δₖ > 0; xác định âm ⇔ (−1)ᵏΔₖ > 0. |
| A3 | 225, 240 | Hessian đối xứng **khi** các đạo hàm riêng cấp 2 liên tục (định lý Schwarz/Clairaut). | OBSERVED T20d (PHẢN VÍ DỤ q = xy(x²−y²)/(x²+y²): ∂/∂y(∂q/∂x) tại 0 = −1, ∂/∂x(∂q/∂y) tại 0 = 1); T20c (x³ + 2xy² có Hessian đối xứng, = Jacobian của gradient) | Thêm điều kiện. Video L06 phân cảnh symm. |
| A6 | 146, 210–214 | “PCA = SVD trên dữ liệu đã trừ trung bình” **đúng** nhưng cần nêu quy ước: X kích thước N×D (mỗi hàng 1 mẫu); trục chính = cột của V; λᵢ = σᵢ²/N. Bước trừ trung bình là **bắt buộc**. | OBSERVED T4a (khớp), T4b (không trừ trung bình → trục khác hẳn) | Nêu quy ước và dùng 1/N hay 1/(N−1) cho thống nhất với bài giảng gốc. |
| A8 | 311, 314 | Dạng tổng log của MLE cần giả thiết dữ liệu **độc lập cùng phân phối (i.i.d.)**. MAP bỏ được P(D) vì không phụ thuộc θ — tài liệu không giải thích. | OBSERVED T7a–b (MLE của μ = trung bình, đạo hàm bậc 2 = −N/σ² < 0) | Thêm hai câu này. |
| A9 | 337–342 | Mô hình có b nhưng loss chỉ có w: cần quy ước “thêm cột toàn số 1 vào X để gộp b vào w”. Công thức (XᵀX)⁻¹ cần XᵀX **khả nghịch**. | OBSERVED T8a (khớp nghiệm bình phương tối thiểu), T8b (cột trùng → XᵀX suy biến, hạng 3 < 4) | Nêu quy ước; khi suy biến dùng giả nghịch đảo hoặc thêm điều chuẩn L2. |
| A20 | 189–198 | Gram-Schmidt cần đầu vào **độc lập tuyến tính**. Tài liệu gọi đầu vào là “cơ sở” (đã ngầm có điều kiện) nhưng không nói hậu quả: nếu có x_k là tổ hợp của các vector trước thì v_k = 0 và bước u_k = v_k/‖v_k‖ chia cho 0. Ngoài ra dòng 195–197 viết ‖v_j‖², dòng 198 viết ‖v_i‖₂ (hai kiểu cho cùng một độ dài). | OBSERVED T2d (x₂ = 2x₁ → v₂ = 0) | Nêu điều kiện; gặp v_k = 0 thì bỏ x_k. Video L03 nêu ở lỗi 4 và giải thích ‖·‖₂ = ‖·‖ trong step ghi chú ký hiệu. |
| A21 | 205, 207, 213, 256–260 | Tài liệu **dùng** trị riêng/vector riêng (SVD, PCA, bảng xét dấu Hessian) nhưng **không định nghĩa**: thiếu A v = λ v, thiếu điều kiện **v ≠ 0** (v = 0 thoả với mọi λ), thiếu cách tìm (det(A − λI) = 0). Bảng dòng 256–260 xét dấu “tất cả λᵢ” ngầm cần trị riêng **thực** — đúng với Hessian đối xứng (A3), không đúng với ma trận bất kỳ (ma trận quay không có trị riêng thực). Hai tên cho một khái niệm: “giá trị riêng” (213), “trị riêng” (256). | OBSERVED T14a (v = 0), T14b (quay: λ² + 1 = 0), T14c (đối xứng → vector riêng vuông góc; không đối xứng thì không), T14d (trị riêng ≠ số trên đường chéo; tổng = vết, tích = định thức) | Video L04 định nghĩa đầy đủ, nêu v ≠ 0 (lỗi 1), ví dụ ma trận quay, ghi chú “giá trị riêng = trị riêng”. |
| A22 | 117, 223, 266–270 | Dòng 223 định nghĩa ∇f bằng các đạo hàm riêng nhưng tài liệu **không định nghĩa** đạo hàm / đạo hàm riêng. Phát biểu “chỉ hướng tăng nhanh nhất” thiếu điều kiện: f **khả vi** tại điểm đó (có đạo hàm riêng chưa đủ), **∇f ≠ 0** (tại điểm dừng không có hướng nào), hướng được so trong các vector **đơn vị** và tốc độ tăng = ‖∇f‖; chỉ đúng **tại chỗ** (−∇f không chỉ thẳng về điểm thấp nhất). Dòng 223 viết [ … ]ᵀ, dòng 269 viết ( … , … ) không ᵀ: cùng một vector. | OBSERVED T15a (đạo hàm x² tại 3 = 6), T15b (f = 3x + 4y: 3600 hướng, lớn nhất 5 = ‖∇f‖ tại (3/5, 4/5)), T15c (f dòng 266 tại (0,0): tốc độ theo u ≈ ∇f·u, lớn nhất √2), T15d (∇f(−1/3, 1/3) = 0), T15e (PHẢN VÍ DỤ xy/(x²+y²): đạo hàm riêng tại 0 bằng 0 nhưng f(t,t) = 1/2 → không khả vi), T15f (x² + 4y² tại (2,1): −∇f = (−4,−8) không cùng hướng (−2,−1)) | Video L05 định nghĩa đạo hàm từ độ dốc, đạo hàm riêng “giữ biến khác đứng yên”, suy ra hướng tăng nhanh nhất bằng cái bóng + Pytago của bài 1, nêu 3 điều kiện (phân cảnh derive) và lỗi 4. |
| A23 | 410 | LDA: *“Chiếu dữ liệu tối đa khoảng cách giữa các lớp”* thiếu một nửa tiêu chí Fisher: tối đa **tỉ số** (khoảng cách giữa hai tâm sau khi chiếu)² / (độ phân tán **trong** từng lớp sau khi chiếu). Chỉ kéo xa hai tâm có thể chọn hướng mà hai lớp chồng lấn nhiều. | OBSERVED T16: hai lớp cùng hiệp phương sai diag(9; 0,25), tâm lệch (3, 1): hướng Fisher S_w⁻¹(m₂ − m₁) có tỉ số Fisher 0,0067 và phân sai 12,2%; hướng nối hai tâm chỉ 0,0019 và 28,0% | “Tìm hướng chiếu để hai lớp cách xa nhau **so với độ trải của mỗi lớp**.” Ghi vào `fix` của bài LDA (L23). |
| A13 | 150, 357 | “Downstream = Upstream × Local” đúng với số vô hướng; với vector thì phép nhân là **nhân ma trận với Jacobian**, không phải nhân từng phần tử. | OBSERVED T20f (k(x + y, xy): J_ngoài·J_trong = [8, 7] = đạo hàm trực tiếp; nhân từng phần tử cho kết quả khác) | Ghi chú phạm vi. Video L06 phân cảnh chain_mat, lỗi 3, in_ai. |

### Thuật ngữ, ký hiệu, nhận định chưa có nguồn

| ID | Dòng | Vấn đề |
|---|---|---|
| A4 | 277 | Không sai nhưng kết luận yếu: Hessian là hằng và xác định dương → f lồi chặt → **cực tiểu toàn cục**, giá trị f(−1/3, 1/3) = −1/3 (OBSERVED T5e). |
| A10 | 98 | “Tổng hợp từ 18 nguồn bài giảng gốc”: NOT_VERIFIED — thư mục chỉ có 1 file. |
| A11 | 206 vs 299; 300 vs 346 | Cùng chữ Σ cho ma trận giá trị kỳ dị (SVD) và ma trận hiệp phương sai; cùng σ cho độ lệch chuẩn và hàm sigmoid. Người mới rất dễ nhầm → video phải nói rõ. |
| A12 | 361 | Cổng max khi x = y: đạo hàm không xác định, cần nêu quy ước chọn nhánh. |
| A14 | 405 | Cột “Hàm Loss / Độ đo” với KNN: KNN không huấn luyện, không có loss; khoảng cách chỉ là độ đo. |
| A15 | 206 | “Giá trị đơn lẻ” — thuật ngữ thông dụng là **giá trị kỳ dị** (singular value). |
| A18 | 286 | “Adam … phổ biến nhất” là nhận định, không có nguồn. |
| A19 | 3, 43–79 | Dùng `inputenc` + pdfLaTeX với emoji (🧠 ⚠️ 📖 🔢) trong tiêu đề hộp: pdfLaTeX thường báo lỗi ký tự Unicode chưa định nghĩa. NOT_VERIFIED (không có LaTeX để biên dịch); nên dùng XeLaTeX/LuaLaTeX hoặc bỏ emoji. |
| A24 | 408 | K-Means: *“Inertia (Tổng khoảng cách)”* — inertia là tổng **bình phương** khoảng cách tới tâm. Khác biệt có hậu quả: bước “tính lại tâm = trung bình” chỉ tối ưu cho tổng bình phương; với tổng khoảng cách thì tâm tối ưu là trung vị (OBSERVED T17: {0, 1, 10} → 11/3 so với 1). Ghi vào `fix` của bài phân cụm (L24). |

## 3. Ghi nhận kiểm chứng (verification records)

```yaml
claim_id: C-0001
claim: "Mọi ví dụ số và công thức trong .tex đúng về mặt tính toán (35 phép kiểm)"
basis: OBSERVED
spec_evidence: "CS115_Toan_cho_Khoa_hoc_May_tinh_Full.tex#L176-L388"
impl_evidence: "audit/verify_cs115_tex.py"
method: ".venv/Scripts/python audit/verify_cs115_tex.py"
observed: "TOTAL=35 PASS=35 FAIL=0, exit=0"
runtime: "Python 3.12.10, sympy 1.14.0, numpy 2.5.4, Windows 10 19045"
validity: VALID
checked_at: "2026-10-22T03:16:56Z"
---
claim_id: C-0002
claim: "Bảng dòng 260 sai: không thoả Sylvester không suy ra yên ngựa"
basis: OBSERVED
method: "T6b, T6c trong audit/verify_cs115_tex.py (phản ví dụ x^4+y^4 và M=[[0,0],[0,-1]])"
observed: "T6b PASS, T6c PASS"
validity: VALID
checked_at: "2026-10-22T03:16:56Z"
---
claim_id: C-0003
claim: "Phát biểu dòng 138 (CE luôn lồi, hội tụ toàn cục) chỉ đúng cho mô hình tuyến tính"
basis: OBSERVED (phần MSE không lồi / BCE lồi, mô hình 1 tham số) + INFERRED (phần mạng neural)
method: "T9a, T9b"
observed: "min d2(MSE∘σ) = -0.1202; min d2(BCE∘σ) = 0.000335"
validity: VALID cho phần OBSERVED; NOT_VERIFIED cho phần mạng neural
checked_at: "2026-10-22T03:16:56Z"
---
claim_id: C-0004
claim: "Gram-Schmidt (dòng 189-198) với đầu vào phụ thuộc tuyến tính cho v_k = 0, nên bước chuẩn hoá chia cho 0 (A20)"
basis: OBSERVED
method: "T2d trong audit/verify_cs115_tex.py (x1 = (3,4), x2 = (6,8))"
observed: "T2d PASS, v2 = [0, 0]; TOTAL=36 PASS=36 FAIL=0, exit=0"
validity: VALID
checked_at: "2026-10-23T07:02:33Z"
---
claim_id: C-0005
claim: "Tài liệu dùng trị riêng/vector riêng mà không định nghĩa; định nghĩa cần v != 0; ma trận không đối xứng có thể không có trị riêng thực (A21)"
basis: OBSERVED
method: "T14a-d trong audit/verify_cs115_tex.py"
observed: "T14a-d PASS; T14b nghiệm lam = ±i; TOTAL=40 PASS=40 FAIL=0, exit=0. (Lần chạy đầu T14b FAIL do chính câu lệnh kiểm: sp.solve không nhận domain=; đổi sang sp.solveset, kỳ vọng giữ nguyên)"
validity: VALID
checked_at: "2026-10-23T18:38:13Z"

claim_id: C-0006
claim: "Tài liệu dùng đạo hàm/đạo hàm riêng mà không định nghĩa; “∇f chỉ hướng tăng nhanh nhất” cần f khả vi, ∇f ≠ 0, chỉ đúng tại chỗ (A22)"
basis: OBSERVED
method: "T15a-f trong audit/verify_cs115_tex.py"
observed: "T15a-f PASS (T15b: max 4,9999993 tại (0,6; 0,8); T15c: max 1,414215; T15e: q(t,t) = 1/2); TOTAL=46 PASS=46 FAIL=0, exit=0"
validity: VALID
checked_at: "2026-10-23T22:37:06Z"


claim_id: C-0007
claim: "Bổ sung khi đối chiếu đề cương: LDA cần tỉ số Fisher (A23); inertia là tổng bình phương (A24); Ridge làm XᵀX + λI khả nghịch (A9); lề SVM = 2/‖w‖"
basis: OBSERVED
method: ".venv/Scripts/python audit/verify_cs115_tex.py (T16–T19)"
observed: "T16 PASS (Fisher 0,0067 vs 0,0019; phân sai 0,122 vs 0,28) — lượt đầu FAIL vì dữ liệu thử chọn sai (hiệu hai tâm gần song song trục dài của hiệp phương sai), đã sửa dữ liệu thử, giữ kỳ vọng; T17 PASS (11/3 vs 1); T18 PASS (det = λ(λ² + 79λ + 28)); T19 PASS (2/5); TOTAL=50 PASS=50 FAIL=0, exit=0"
validity: VALID
checked_at: "2026-10-24T02:19:34Z"

claim_id: C-0008
claim: "L06: Jacobian/Hessian/quy tắc chuỗi — A3 (Hessian đối xứng cần đạo hàm cấp 2 liên tục) và A13 (quy tắc chuỗi với vector = nhân ma trận Jacobian) chuyển từ INFERRED sang OBSERVED"
basis: OBSERVED
method: ".venv/Scripts/python audit/verify_cs115_tex.py (T20a–f)"
observed: "T20a–f PASS (T20c: H(1,2) = [[6,8],[8,4]]; T20d: (−y, x) → −1 và 1; T20f: [8, 7]); TOTAL=56 PASS=56 FAIL=0, exit=0"
validity: VALID
checked_at: "2026-10-24T03:35:38Z"

claim_id: C-0009
claim: "Bài 7: bảng định thức con 2×2 (kể cả Δ₂ < 0 ⇒ yên ngựa, Δ₂ = 0 ⇒ chưa kết luận) khớp dấu trị riêng; Sarrus = định thức 3×3; độ cong theo hướng = uᵀHu; ví dụ dòng 266 là cực tiểu toàn cục (A4)"
basis: OBSERVED
method: ".venv/Scripts/python audit/verify_cs115_tex.py (T21a–c); đối chứng âm: luật sai “chỉ xét det > 0 ⇒ đáy” trên cùng 3000 ma trận"
observed: "T21a PASS (0 lệch / 3000), T21b PASS (200/200), T21c PASS; TOTAL=59 PASS=59 FAIL=0, exit=0. Đối chứng âm: luật sai lệch 314/3000 → phép quét phân biệt được"
validity: VALID
checked_at: "2026-10-24T04:16:52Z"
```
