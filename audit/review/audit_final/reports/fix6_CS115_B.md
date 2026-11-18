# fix6 CS115 L12–L21, L44–L46 (chuẩn P1 chặt, không có reader vòng 4 riêng) — 2026-11-16

Tiến độ: L12–L14 xong; L15–L17 xong; L18–L20 xong; L21, L44–L46 xong; sổ screen_code, render, cổng xong. KHÔNG chạy build/tts/asr/audit_all/git/docker; có chạy `tools/lv.py render` (chỉ khung hình). Phạm vi: 13 bài `lessons/cs115/` (L00–L11 do tác tử khác; không đụng CS112; không sửa `lexicon_vi.*`, `symbols.*`).

## Cách làm
- Mỗi bài YAML viết tay; sửa bằng script ghi lại ở scratchpad (đọc bản gốc đã sao lưu rồi ghi lại, giữ CRLF; chạy lại được), kiểm bằng `tools/lv.py lint` từng bài.
- Gốc P1 chung (theo `R4_CS115_A.md`): cảnh `practice` bắt "Viết `<tên>.py`" + `bash labs/cham.sh` mà video không dạy. Cách sửa (khuôn như DMS/CS112): thêm step đầu cảnh practice "Đọc trước khi làm" = một đoạn (tạo tệp .py, mở Git Bash, `python <tên>.py`, dòng `import`) + bảng "viết trong mã | đọc là | ví dụ" (3–4 hàng) ĐỨNG TRƯỚC khối Đề; step "Đề" có `clear: true`; chân trang chấm bài có giải thích bằng chữ (`bash`, `labs/cham.sh`, khoá–bài–tên tệp) và 2 câu lời đọc; step "Nếu kẹt" thêm `clear: true` ở L12, L18, L19, L44 (render báo TRÀN). Lời đọc không nói tên Latin (tả bằng tiếng Việt), tên thật chỉ hiện trong bảng; mỗi bài tự đứng được (nhắc lại một dòng, không "như đã học").
- Không thêm sổ `symbols`/`lexicon` (tránh buộc `assumes` bài sau và làm bài khác STALE): thuật ngữ định nghĩa tại chỗ bằng chữ trên màn hình + lời đọc. `asr_reviewed`: mọi câu có mục được giữ nguyên (kiểm bằng script: 0 mục mất ở 13/13 bài; số mục: L12 9, L13 8, L14 7, L15 2, L16 1, L17 3, L18 3, L19 3, L20 22, L21 1, L44 3, L45 7, L46 10).

## Mục chưa giảng đã tìm (tự đọc từng step; đủ mục yếu) và cách xử lý
| Bài | Mục chưa giảng (P1 chặt) | Xử lý |
|---|---|---|
| L12 | practice: "Viết xacsuat.py", chạy .py, chân trang `bash labs/cham.sh`, `t = t * 0.2`, `math.log(0.2)`, `math.exp(s)`, `1.126e-35` (chữ e ≠ số e); "cơ số" (sym_exp); "thư viện numpy: np.log" (ghi chú); dấu ⟹ (ln_rules, lần đầu); `1,0·10^-10` ở bảng quymo | bảng 4 hàng; chân trang; gloss "cơ số = số được nhân lặp lại"; bỏ vế numpy; ghi chú "⟹ đọc là suy ra" + lời; lời đọc đọc ra "1 nhân 10 mũ âm 10 = 0 phẩy, chín số 0, rồi 1" |
| L13 | practice: bayes.py, chạy, chân trang, dấu chấm thập phân, số không cách nhóm, chia lấy phần nguyên (gợi ý đề); "hằng số"; "tính chất tuyến tính" (lời đọc, show; dùng trước khi giảng) | bảng 3 hàng; chân trang; "hằng số = hai số cố định"; thay bằng "nhân và cộng cùng với X", "theo hai tính chất vừa học" |
| L14 | practice: chuan.py, `math.erf` (2 chỗ), `abs`/`|X−μ|`, `-1 + (i + 0.5) * h` (gợi ý), chân trang; "tham số" (sym_normal); `x_i` ở tổng cột | bảng 3 hàng; chân trang; gloss "tham số = con số quyết định hình dạng"; gloss $x_i$ |
| L15 | practice: hiep.py, `x = [1, 2, 4, 5]`, `n = 4`, `Fraction`, `[[5/2, 2], [2, 5/2]]`, chân trang; `Σᵀ` dùng chưa giảng ᵀ; chữ in đậm = vector | bảng 4 hàng; chân trang; "Σᵀ: chuyển vị = đổi hàng thành cột" (chữ + lời); "chữ in đậm là vector"; thêm `clear` ở sym_Sigma (render TRÀN) |
| L16 | practice: pca.py, `Fraction(14, 5)`, `[1, 1]`, `[[…]]`, chân trang; `np.linalg.svd`/numpy; dấu ⟹ (link, lần đầu); kích thước $4\times 2$ | bảng 3 hàng; chân trang; gloss numpy + lời; ghi chú ⟹ + lời; "bảng 4 hàng 2 cột" |
| L17 | practice: mle.py, `0.75`, `True`, `[1/2, 1/4, …]`, chân trang; chữ viết tắt MLE/MAP (hook, chỉ ở màn hình); dấu ⟹ (mle) | bảng 3 hàng; chân trang; hook ghi rõ "viết tắt MLE/MAP = ước lượng hợp lý cực đại/hậu nghiệm cực đại" + 1 câu; ghi chú ⟹ + lời |
| L18 | practice: hoiquy.py, `x = [0, 1, 2, 3]`, `Fraction(9, 10)`, `[[4, 6], [6, 14]]`, chân trang; ŷ ở hook chưa giải; ⟹ (prereq, lần đầu); `np.linalg.lstsq` | bảng 3 hàng; chân trang; "ŷ đọc y nón: giá thuê dự đoán" (chữ + lời); ghi chú ⟹ + lời; "thư viện tính toán số numpy" |
| L19 | practice: chinhquy.py, `Fraction(1, 10)`, `[28/29, 28/29]`, `a=3 -> 2`, chân trang; ⟹ (lasso_hand) | bảng 3 hàng; chân trang; ghi chú ⟹ + lời |
| L20 | practice: logistic.py, `1 / (1 + math.exp(-z))`, `math.log`, danh sách và `0.09` (print bỏ số 0 thừa), chân trang; ∂ dùng trước khi giải thích (gradient s0); ⟹; ngoặc Iverson `[k là lớp đúng]`; "NumPy" ở bảng quymo | bảng 3 hàng; chân trang; lời step 0 nêu "ký hiệu cong là đạo hàm riêng"; ⟹ (chữ + lời); giải ngoặc vuông bằng 1/0 (chữ + lời); "thư viện tính toán số" |
| L21 | practice (mã thật trên màn hình): `that = [1] * 5 + [0] * 15`, `doan = [1, 1, 1, 1, 0] + [1, 1, 1] + [0] * 12`, `Fraction`, chân trang | bảng 4 hàng (gán danh sách, lặp `* 5`, nối `+`, `Fraction`) trước Đề; chân trang |
| L44 | practice: tincay.py, `1.96`, `[0.8079, 0.8721]`, `True`, `math.ceil`, chân trang | bảng 4 hàng; chân trang |
| L45 | practice: adam.py, `[0.001, …]`, `1.0e-08`, chân trang; chặng 5: `Adam(weight_decay=0)`, `AdamW(weight_decay=0.01)`, `Adam(decoupled_weight_decay=True)`, `amsgrad=False`, `True/False`, `optim.AdamW` (chặng 4); SHOULD: bài 19 viết phạt λΣw² (gradient 2λw) còn bài này λ/2·w² (gradient λw) mà prereq nói "bài 19 … λ nhân w" | bảng 2 hàng; chân trang; đoạn "Cách đọc `Tên(đối_số=giá_trị)`; `=`; True/False" + 1 câu trước bảng mã chặng 5; gloss `optim.AdamW`; chữ + lời nêu hai cách đặt λ chỉ lệch hệ số 2 |
| L46 | practice: nghichdao.py, `Fraction(1, 100)`, `[[3, -2], [-7, 5]]`, nhãn `M.w`, "gần suy biến" (chưa định nghĩa), chân trang; `X ∈ ℝ^{N×D}` (∈, ℝ) chưa nhắc lại | bảng 3 hàng + định nghĩa "suy biến / gần suy biến"; chân trang; "∈ đọc là thuộc, ℝ là tập số thực" (chữ + thêm 1 câu lời) |

Ước lượng còn lại (tự chấm, reader sẽ chấm lại): **0 mục chưa giảng ở 13/13 bài.** Rủi ro "yếu" còn lại: L12 công thức độ dốc hai phía `(f(x + h) − f(x − h)) / (2h)` ở hộp "Nếu kẹt" (ký hiệu toán, không có hàng bảng riêng; đã bỏ hàng để giữ ≤ 2300 từ); tên riêng chỉ nhắc ở ghi chú/xem trước (Mahalanobis, Gaussian, Dirichlet, Laplace, Ridge/Lasso, dropout, ROC/AUC, PyTorch) — mỗi tên đều đi kèm một câu giải nghĩa tại chỗ hoặc nằm ở khung xem trước.

## Theo bài (đã đổi — để requeue; số mục chưa giảng ước còn lại)
| Bài | Số từ lời đọc (trước → sau) | Chưa giảng ước |
|---|---|---|
| L12 | 2227 → 2299 | 0 (yếu: công thức độ dốc hai phía) |
| L13 | 2271 → 2300 | 0 |
| L14 | 1833 → 2022 | 0 |
| L15 | 1919 → 2064 | 0 |
| L16 | 2171 → 2286 | 0 |
| L17 | 1995 → 2112 | 0 |
| L18 | 2080 → 2202 | 0 |
| L19 | 1830 → 1952 | 0 |
| L20 | 1987 → 2120 | 0 |
| L21 | 1699 → 1825 | 0 |
| L44 | 1966 → 2085 | 0 |
| L45 | 2283 → 2300 | 0 |
| L46 | 1616 → 1767 | 0 |

Đo bằng tách theo khoảng trắng (như `audit/cs112/wc_say.py`). L12, L13, L45 sát giới hạn: sửa tiếp phải cắt thêm. Để vừa 2300 đã cắt ý ít giá trị ở L12 (thước lôgarit, ghi chú cách viết log), L13 (ôn phân số, vài câu tổng kết), L45 (câu điều kiện/ghi chú tên ở các chặng, "Một giá trị mặc định…" ở recap, đoạn cuối pitfalls/quiz) — không bỏ mục tiêu `covers`; câu hiệu chỉnh `focus` đã đồng bộ (lint E31 sạch).

## Chuẩn xác (mục 2)
- `lint` chạy lại các `checks:` của từng bài: tất cả PASS. `audit/verify_cs115_af2.py` 184 PASS · 0 FAIL; `verify_cs115_l44.py` 16 PASS · 0 FAIL; `verify_cs115_tex.py` 59 PASS · 0 FAIL.
- Tự tính lại độc lập (Python thuần): tổng cột chuẩn tắc L14 (2/10/100 cột = 0,7041/0,6835/0,6827; erf(1/√2) = 0,6827); quy mô L14 (10^20 ô/10^9 = ≈ 3170 năm); L16 (K(N+D)+D = 89 984 ≈ 90 nghìn; 8,7 lần; 15,7 lần; 0,6 s và ≈ 10 phút); L18 (1000 giây ≈ 17 phút; 116 ngày; 5,6 giờ; tỉ 5 và 500 lần); L45 (632 ngày = 365 + 267; 0,99999^10000 = 0,905; 1−0,999^1000 = 0,632; 1−0,999^5000 = 0,9933; 0,9^100 ≈ 0,00003; 0,999^100 = 0,905); L44 (n = 3457,44 → 3458); L12 (1e-2 = 0,01; −ln 0,8808 = 0,1269; độ dốc hai phía của x² tại 1, h = 0,1 là 2); L13 (10000·2//100 = 200; Var = 1,7 − 1,21 = 0,49); L19 (det(XᵀX+λI) = λ(λ²+64λ+40), λ = 1 cho 105); L46 (t = 0,1/0,01/0,0001: số lớn nhất của nghịch đảo 11/101/10001, nghiệm đổi 0,01/0,1/10). Mọi hàng bảng mới có ví dụ số đã tính lại; không số nào sai.
- Lab L45 (bài mới): chạy `labs/CS115/L45/loi_giai.py` khớp `mong_doi.txt` (kết quả: bước Adam 0,001 ở cả hai trọng số; √ŝ = 10,0 và 0,1; phạt L2 kéo 1,0e-08 và 1,0e-06; tách rời 1,0e-07; tỉ số 100,0 và 1,0); các số trong bài L45 (632 ngày, 0,905, 0,632, 0,9933, 8,5% và 3,4% …) tính lại độc lập. Ngày tháng/phát biểu nguồn (arXiv 22/12/2014, 14/11/2017, bản 1.2 ngày 8/8/2019, "15% tương đối", mã hiện hành của thư viện) KHÔNG được kiểm lại với nguồn ngoài ở phiên này (không dùng mạng); vẫn dựa vào `audit/cs115/sources_L45.md` của đợt trước. Phát hiện duy nhất: quy ước λ khác bài 19 (SHOULD, đã sửa, xem bảng).
- Lab L46: `loi_giai.py` khớp `mong_doi.txt`; công thức nghịch đảo hai nhân hai và các bảng t được tính lại (ở trên).
- Không phát hiện bước chứng minh nhảy cần sửa ngoài các chỗ ghi ở bảng (⟹/Σᵀ/∂ được giải thích). Không có hình SVG nào bị đổi; hình L45/L46 không bị đụng.

## Cổng (chạy thật, 2026-11-16)
- `tools/lv.py lint` từng bài 13/13: 0 FAIL, 0 WARN.
- `tools/lv.py curriculum curriculum/cs115.yaml`: 47 bài, 0 lỗi. `tests/test_e52.py`: 0 FAIL.
- `audit/review/screen_code.py check --course CS115`: 34 khối — PASS 59 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0. Sổ `audit/review/screen_code/CS115.yaml` sửa bằng Edit từng mục: bảng "Đọc trước" chèn làm step đầu cảnh practice nên chỉ số step của mọi khối mã/kết quả trong cảnh này dịch +1 (L12, L13, L16, L18, L19, L44, L45: practice 1→2; L14, L15, L17, L20, L46: 1→2 và 2→3; L21: 0→1 và 1→2). Không đổi sha, không script.
- `audit/review/arith_scan.py`: 258 phép, 0 FAIL. `audit/check_curricula_graph.py`: thoát 0, 0 VER lỗi.
- `audit/review/lab_gate.py CS115`: 25 PASS · 0 FAIL (196 lab được bài tham chiếu). Lab `labs/CS115/L12–L21, L44–L46` không đổi.
- `tools/lv.py render` từng bài (cả 13 đều nằm trong hàng dựng đã xong, nên phải render): lượt đầu TRÀN ở L12 (practice), L15 (sym_Sigma), L18, L19, L44 (practice, bước "Nếu kẹt" nằm dưới kết quả + chân trang dài hơn); đã thêm `clear: true` (L12, L18, L19, L44 cho "Nếu kẹt"; L15 cho hai step của sym_Sigma); lượt cuối **0 vấn đề ở 13/13 bài**. Khung PNG đã xem: `out/CS115/L14/frames/00090.png` (bảng 3 hàng sau đoạn đọc trước), `L21/frames/00085.png` (bảng 4 hàng với mã danh sách), `L46/frames/00073.png` (đoạn đọc trước có định nghĩa suy biến), `L45/frames/00075.png` (đoạn "Cách đọc" + bảng mã chặng 5).

## Việc chưa làm được / lưu ý cho người điều phối
- Cần dựng lại (build + tts + asr) cả 13 bài: lời đọc mới (nhất là các câu "đọc là" trong bảng và 2 câu chân trang) chưa qua tai/ASR; chưa thêm `asr_reviewed` cho câu mới. Câu cần xem ASR: "Chữ e trong số này nghĩa là nhân mười mũ" (L12, L45), "gạch chéo" ở các câu phân số, "hai chữ cuối nghĩa là đúng và sai" (L45).
- `lab`: không đổi `labs/CS115/*` (de.md vẫn giải thích cú pháp riêng).
- Tệp thay đổi: `lessons/cs115/L12…L21, L44, L45, L46_*.yaml`, `audit/review/screen_code/CS115.yaml`. Script sửa nằm ở scratchpad (không lưu trong repo).
