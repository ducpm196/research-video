# Báo cáo kiểm định độc lập WP-AF4-5 Stage 9 — CS115 (`L22–L32`, 11 bài)

**Kết luận: `NO-GO`** (chưa đạt chuẩn xuất xưởng AF2 / WP-AF4-5; cả 11/11 bài đều vướng các lỗi `MUST` hệ thống và có lỗi `MUST` chuyên môn/ký hiệu cục bộ tại `L22`, `L25`, `L28`, `L30`, `L31`).

---

## 1. Tổng hợp cổng kỹ thuật & nhất quán dữ liệu (`OBSERVED`)

| Hạng mục | Kết quả (`L22–L32`) | Chi tiết |
|---|---|---|
| `tools/lv.py curriculum curriculum/cs115.yaml` | **PASS** | `47 bài, 47 đã có đặc tả, 0 lỗi`; `title` của `L22–L32` khớp 11/11 với `curriculum/cs115.yaml` và các điểm `fix:` cốt lõi đều đã đưa vào thân bài. |
| `tools/lv.py lint` (`L22..L32`) | **11/11 PASS** | `0 FAIL, 0 WARN` trên cả 11 bài (`L22`: 28 PASS, 1352 từ; `L23`: 33 PASS, 1772 từ; `L24`: 28 PASS, 1542 từ; `L25`: 27 PASS, 1529 từ; `L26`: 26 PASS, 1490 từ; `L27`: 25 PASS, 1164 từ; `L28`: 27 PASS, 1358 từ; `L29`: 29 PASS, 1607 từ; `L30`: 28 PASS, 1458 từ; `L31`: 21 PASS, 1283 từ; `L32`: 31 PASS, 1428 từ — mọi bài đều dưới trần `2 300` từ). |
| Biểu thức `checks:` trong 11 YAML | **182/182 PASS** | Chạy lại độc lập qua `sympy`/`numpy`/`math`: 0 FAIL (`L22`: 17, `L23`: 22, `L24`: 17, `L25`: 16, `L26`: 15, `L27`: 14, `L28`: 16, `L29`: 18, `L30`: 17, `L31`: 10, `L32`: 20). |
| `build_report.json` (`spec_sha256` & `tts_sha256`) | **11/11 khớp** | `lv.spec_digest == spec_sha256` và `lv.tts_digest == tts_sha256` khớp 11/11; tất cả dùng `vi-VN-NamMinhNeural`. |
| `out/CS115/L*/L*.srt == say` | **11/11 khớp 100%** | Ghép các block phụ đề SRT khớp chính xác từng ký tự với chuỗi `say` trong YAML của cả 11/11 bài. |
| `out/CS115/L*/asr_report.md` | **11/11 sạch cờ chưa duyệt** | `thiếu audio: 0`, `chưa xem xét: 0` ở cả 11/11 bài (tổng 57 câu gắn cờ đều có ghi chú `asr_reviewed`, trong đó còn 8 câu `< 0.8` gắn `NOT_VERIFIED bằng tai người` hoặc chữ cái/thanh điệu tại `L23, L25, L26, L27, L29`). |
| `audit/layout_CS115.tsv` | **0 dòng lỗi (nhưng bỏ sót `L25 hook#0`)** | Tệp trống (2 byte), không ghi lỗi tự động; tuy nhiên **kiểm bằng mắt phát hiện `L25/frames/00000.png` bị đường đỏ cắt ngang chữ `"sát điểm"` và chạm `"lề lớn nhất"`**. |
| Chạy thật `labs/CS115/L*/loi_giai.py` vs `mong_doi.txt` | **11/11 khớp stdout** | Chạy trực tiếp bằng `.venv/Scripts/python.exe -B` khớp 100% `mong_doi.txt` (dù có lỗi logic/ký hiệu giữa `de.md` và `loi_giai.py` ở `L22, L28, L30, L31`). |
| `<p class="note"><b>Hai mức quy mô:</b> ...` | **0/11 bài (0%)** | Không bài nào có dòng ghi chú chuẩn `Hai mức quy mô:` ở thân bài hay `recap`. |

### Kiểm tra câu chứa `"càng "` & phát âm tiếng Việt trong `say`
- **Không có ký hiệu toán thô (`+ - * / = < > ^ \`) trong `say`** ở cả 11 bài.
- **2 câu chứa `"càng "` trong `L22–L32` đều chính xác và rõ nghĩa**:
  1. `L29 spectral#1`: *"Trị riêng thứ hai càng nhỏ, đồ thị càng gần đứt thành hai mảnh."* — Chính xác (liên hệ trực tiếp độ liên thông đại số Fiedler $\lambda_2$ của Laplacian).
  2. `L30 mix_pic#0`: *"Các cột phía dưới cho thấy điểm càng nằm về bên trái thì phần cam càng lớn, còn ba điểm bên phải gần như toàn màu xanh."* — Chính xác với hai hình chuông tâm 2 và tâm 6 có cùng $\sigma^2=4$.

---

## 2. Tỷ lệ `P1`, `P8`, `P9` toàn chặng (`L22–L32`)

| Chỉ số | Tỷ lệ đạt chuẩn (`= 2`) | Diễn giải |
|---|---|---|
| **P1 (thuật ngữ/cú pháp tại chỗ)** | **0/11 (0%)** *(tính chặt gồm thân bài + `practice#0` + `de.md`)*; **Thân bài riêng:** 6/11 đạt 2, 5/11 đạt 1 (`L22, L23, L25, L30, L32`) | **11/11 bài** dùng bảng `practice#0` boilerplate lệch token thực tế so với `practice#1` (mọi bài đều có `f"{val:.3f}"` dù 9/11 bài không dùng `:.3f`, thiếu `bash labs/cham.sh`, thiếu hàm thực tế dùng như `math.hypot`, `math.log2`, `math.pi`, `zip`, `abs`, `round`, `set`, `**2`, ternary `if/else`, list comprehension); và **11/11 `de.md`** có thuật ngữ/ký hiệu chưa chú thích hoặc lệch bài giảng (`n_in+n_out`, `s1^2`, `IG`, `gamma_1`/`trách nhiệm hậu nghiệm`, `V/H`, `đơn vị nat`, `dq`). |
| **P8 (thực nghiệm tự làm)** | **0/11 (0%)** | **11/11 bài** chiếu nguyên mã lời giải `loi_giai.py` ở `practice#1` và đáp án `mong_doi.txt` ở `practice#2` **ngay trước** `practice#3` (`pause: 30` *"Hãy bấm tạm dừng và tự làm trước"*); **11/11 `de.md`** thiếu định dạng chuỗi stdout bắt buộc; **1/11** trùng số liệu ví dụ trong bài (`L24` `[5, 3, 2]`) và **1/11** trùng tham số quiz (`L25` `w=(3, 4)`). |
| **P9 (quy mô + hình SVG)** | **`Hai mức quy mô:` 0/11 (0%)**; Nội dung 2 quy mô/đánh đổi trong thân bài: **7/11 = 63,6%** (`P9=2`: `L22, L23, L26, L27, L28, L29, L32`), **4/11** (`P9=1`: `L24, L25, L30, L31`); SVG sạch: **10/11 (90,9%)** | Không bài nào có `<p class="note"><b>Hai mức quy mô:</b> ...` trong thân bài/`recap`; `L25` có 1 lỗi SVG cắt chữ (`00000.png`); 4 bài (`L24, L25, L30, L31`) chỉ mới tính ví dụ nhỏ hoặc nhắc khái niệm, thiếu so sánh hai mức quy mô cụ thể kèm thời gian/chi phí. |

---

## 3. Các lỗi hệ thống áp dụng chung cho cả `11/11` bài (`L22–L32`)

- **[MUST-SYS-1 — Lộ lời giải trước `pause` (`P8`)]**: Ở cả 11 bài, `practice#1` chiếu nguyên văn `loi_giai.py` và `practice#2` chiếu stdout thật (`mong_doi.txt`) trước `practice#3` (`pause: 30`). Cần đưa bảng đề + định dạng đầu ra + `pause` lên trước khi gợi ý/chiếu lời giải.
- **[MUST-SYS-2 — `de.md` thiếu định dạng stdout (`P8`)]**: Cả 11 tệp `labs/CS115/L22..L32/de.md` không ghi rõ mẫu chuỗi `key=value` từng dòng như `mong_doi.txt` đòi hỏi khi chấm bằng `cham.sh`.
- **[MUST-SYS-3 — `covers:` ánh xạ sai cảnh (`L22–L32`)]**: Cả 11 bài đều gắn `covers:` theo mẫu tự động sai (`obj 1 -> cảnh ví dụ đầu`, `obj 2 -> cảnh kế`, `obj 3–4 -> verify`, `obj cuối -> practice`), lệch hoàn toàn với nội dung mục tiêu thật sự.
- **[SHOULD-SYS-1 — `practice#0` boilerplate lệch token (`P1`)]**: Bảng `viết trong mã → đọc và hiểu là` ở cả 11 bài dùng mẫu chung (chứa `f"{val:.3f}"`, `lambda x: ...`, `for x in ds:`, `math.log / exp / sqrt`, `sum / len / max / min` bất kể code bài có dùng hay không) và không giải thích `bash labs/cham.sh`.
- **[SHOULD-SYS-2 — Thiếu `Hai mức quy mô:` (`P9`)]**: 0/11 bài có dòng `<p class="note"><b>Hai mức quy mô:</b> ...` ở thân bài hay `recap`.
- **[INFO-SYS-1 — `screen_code/CS115.yaml` phân loại sai]**: Các mục `CS115 L22..L32 practice 1 0` trong `audit/review/screen_code/CS115.yaml` đều đang ghi `kind: other, lang: text` thay vì `kind: run, lang: python`.

---

## 4. Báo cáo chi tiết từng bài (`L22..L32`)

### L22 — `Đồ thị tính toán & lan truyền ngược (backpropagation)`
- **Toán & kiểm số**: 17/17 `checks` PASS; phép tính $f = xy + \max(x, y) = 9$, gradient $(3, 3)$, nơ-ron logistic ($z=0 \to 0{,}25$, $L=0{,}693 \to 0{,}576$), $\mathbf{W}^T\mathbf{g}=(-2,-2)^T$, sai phân trung tâm và quiz khớp hoàn toàn.
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - **Sai ký hiệu biến trong `loi_giai.py` & `mong_doi.txt`**: `de.md` hỏi `f=(x+y)*z` tại `(-2,5,-4)` và `dx,dy,dz`, nhưng `loi_giai.py` dòng 6 in `print(f"f={f:.1f} dq=z={dz:.1f}")` cho ra `dq=z=3.0`. Với `q = x + y = 3`, đạo hàm $\frac{\partial f}{\partial q} = z = -4{,}0$, còn $\frac{\partial f}{\partial z} = q = 3{,}0$ — viết `dq=z=3.0` vừa gán nhầm giá trị `dz=q=3.0` cho `dq`, vừa xuất `dq` vốn không có trong `de.md`.
  - `MUST-SYS-3` (`covers:`): `obj 1` (vẽ đồ thị & lượt tiến) trỏ `example` (lượt lùi) → phải là `graph`; `obj 2` (quy tắc gửi xuống) trỏ `neuron` → `rule` + `flow_pic` + `example`; `obj 3` (4 cổng) trỏ `verify` → `gates`; `obj 4` (nơ-ron logistic) trỏ `verify` → `neuron`; `obj 5` (gradient checking + vector) trỏ `practice` (chỉ vô hướng) → `verify` + `vector`.
- **SHOULD**:
  - `SHOULD-SYS-1` (`practice#0` ghi `f"{val:.3f}"` không dùng, thiếu `:.1f`, `:.6f`, `:.2e`, `abs()`, `1e-5`); `SHOULD-SYS-2`.
  - `P1` thân bài: `title` có `backpropagation` chưa nói ở lời đọc; `neuron#0` viết `BCE` chưa nhắc lại viết tắt của *Binary Cross-Entropy*; `verify#0` có `code` chưa Việt hoá.
  - `P8` lab: `f = (x + y)*z` trùng đúng cấu trúc hàm của `quiz` câu 1 (chỉ đổi số).
- **INFO**: ASR 83 câu, 7 gắn cờ (0 `< 0.8`, 0 chưa xem xét; 4 câu chữ cái/lệch âm `tiến/tiếng`, `đổi/đuổi` ghi `NOT_VERIFIED bằng tai người`).
- **P1/P8/P9**: `P1=0` (thân: 1) · `P8=0` · `P9=1` (có `1 000 000` vs `1 lượt tiến + 1 lượt lùi` ở `hook`, thiếu `Hai mức quy mô:`).
- **PNG đã xem**: `out/CS115/L22/frames/00006.png` (SVG `graph` sạch), `00012.png` (SVG `flow_pic` sạch), `00017.png` (bảng `gates` sạch), `00067.png` (`practice#0`), `00068.png` (`practice#1` lộ mã), `00070.png` (`practice#3` hướng dẫn tự làm sau khi đã lộ mã).

### L23 — `Mạng perceptron nhiều lớp (MLP): hàm kích hoạt, khởi tạo, Batch normalization & hyperparameters`
- **Toán & kiểm số**: 22/22 `checks` PASS; XOR ReLU, $\sigma'(0)=0{,}25$, $0{,}25^{10}\approx 9{,}54\times 10^{-7}$, mô phỏng 10 lớp tanh Xavier (`[0.0, 0.957, 0.232]`, 78% bão hòa), BatchNorm `(2,4,6)`, trung điểm không lồi `1.6875`, đếm `79 510` tham số, quiz `43` tham số đều chính xác.
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `MUST-SYS-3` (`covers:`): `obj 1` (XOR 1 vs 2 lớp) trỏ `init` → `hook` + `mlp` + `xor_pic`; `obj 2` (hàm phi tuyến) trỏ `count` → `why_nonlinear`; `obj 3` (so sánh sigmoid/tanh/ReLU) trỏ `verify` → `activations`; `obj 4` (khởi tạo Xavier) trỏ `verify` → `init`; `obj 5` (BatchNorm, dropout, hyperparameters) trỏ `practice` (không có BatchNorm/dropout/siêu tham số) → `batchnorm` + `hyper`.
- **SHOULD**:
  - `SHOULD-SYS-1` (`practice#0` ghi `for x in ds:` và `f"{val:.3f}"` trong khi code dùng list comprehension, `:.6e`, `:.4f`, `math.exp`, `math.sqrt`, `max`); `SHOULD-SYS-2`.
  - `de.md` (`P1`/`P8`): ghi `"biến thể ReLU tại -3, 0, 4"` (thực tế `loi_giai.py` tính hàm **ReLU chuẩn** `max(0.0, v)`, không phải biến thể như Leaky ReLU); dùng `n_in+n_out` không giải thích (bài giảng dùng $n_{\text{vào}}, n_{\text{ra}}$).
  - `P1` thân bài: `hyper#0` dùng `epoch` (chưa giải thích nghĩa 1 lượt duyệt hết tập huấn luyện); `nonconvex#0` dùng `MSE` chưa nhắc tên; `activations#1` `show` có `Leaky ReLU` nhưng `say` bỏ qua.
- **INFO**: ASR 100 câu, 7 gắn cờ (1 câu `< 0.8`: frame 23 `1`→`mục`, 0 chưa xem xét).
- **P1/P8/P9**: `P1=0` (thân: 1) · `P8=0` · `P9=1` (có `10 lớp`, `784→100→10 = 79 510`, thiếu `Hai mức quy mô:`).
- **PNG đã xem**: `out/CS115/L23/frames/00000.png` (SVG `hook` sạch), `00013.png` (SVG `xor_pic` sạch), `00021.png` (bảng `activations` sạch), `00084.png` (`practice#0` sạch).

### L24 — `Tối ưu có ràng buộc: nhân tử Lagrange & điều kiện KKT (cầu nối sang SVM)`
- **Toán & kiểm số**: 17/17 `checks` PASS; vườn $x=y=5$, $\lambda=5$, nới ràng buộc $5{,}25\approx 5$, phân loại $(5,3,2) \to (0{,}5; 0{,}3; 0{,}2)$, KKT $(x-3)^2$, phản ví dụ $x^2 \le 0$ đều khớp.
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `MUST-SYS-3` (`covers:`): `obj 1` (gradient cùng phương) trỏ `categorical` → `geometry` + `sym_lagrange`; `obj 2` (lập hàm Lagrange & giải hệ) trỏ `verify` → `sym_lagrange` + `verify`; `obj 3` (MLE phân loại) trỏ `verify` → `categorical` + `practice`; `obj 4` (4 điều kiện KKT) trỏ `verify` → `kkt` + `quiz#1`; `obj 5` (điều kiện cần/đủ) trỏ `practice` (không có Slater/lồi) → `when`.
- **SHOULD**:
  - **Trùng số liệu ví dụ (`P8`)**: `de.md` dùng đúng `[5, 3, 2]` — trùng y hệt ví dụ `5 mèo, 3 chó, 2 chim` trong `categorical` và `verify`. Nên đổi sang bộ đếm khác (vd `[6, 3, 1]` hoặc `[4, 4, 2]`). Ngoài ra, `kkt_equal` thực chất kiểm tra phương trình dừng của **Lagrange** (ràng buộc đẳng thức $\sum p_k = 1$), chưa kiểm bất đẳng thức $p_k \ge 0$.
  - `SHOULD-SYS-1` (`practice#0` liệt kê `lambda x: ...` và `f"{val:.3f}"` không dùng trong `loi_giai.py`, thiếu `sum`, `len`, `zip`, `round`, `set`, `int`); `SHOULD-SYS-2`.
  - `P1` thân bài: `prereq#0`/`quiz#0` dùng `MLE` chưa giải thích lại tên đầy đủ trong bài (chỉ đọc "ước lượng hợp lý cực đại" ở `quiz#0`).
- **INFO**: ASR 91 câu, 6 gắn cờ (0 `< 0.8`, 0 chưa xem xét).
- **P1/P8/P9**: `P1=0` (thân: 2) · `P8=0` · `P9=1` (chỉ có 1 ví dụ 3 lớp & grid 100 001 bước trong `verify`, chưa rõ hai mức quy mô/đánh đổi).
- **PNG đã xem**: `out/CS115/L24/frames/00008.png` (SVG `geometry` sạch), `00076.png` (`practice#0` sạch).

### L25 — `Support Vector Machine: lề lớn nhất, hinge loss & kernel`
- **Toán & kiểm số**: 16/16 `checks` PASS; lề $2/\|w\|$, KKT $\alpha = (0{,}5; 0; 0; 0{,}5; 0; 0)$, hinge vs logistic, kernel $(xz+1)^2$, Gram âm định $- (x-z)^2$ đều khớp.
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - **Lỗi hiển thị SVG (`00000.png` — `hook#0`)**: Trong `L25_svm.yaml` dòng 60 & 63, đường thẳng đỏ `x1=170, y1=380 -> x2=250, y2=20` **cắt ngang chữ `đ` trong nhãn `"sát điểm"`** (`x=130, y=375`), và đầu trên của đường đỏ (`x=250, y=20`) cùng đường xanh lá (`x=240`) **chạm sát chữ `l` của nhãn `"lề lớn nhất"`** (`x=246, y=40`).
  - `MUST-SYS-3` (`covers:`): `obj 1` (lề $2/\|w\|$) trỏ `kernel` → `sym_margin` + `margin_pic` + `verify`; `obj 2` (tối ưu & vector hỗ trợ qua KKT) trỏ `verify` → `optimization`; `obj 3` (hinge loss vs logistic) trỏ `verify` → `hinge`; `obj 4` (mẹo hàm nhân) trỏ `verify` → `kernel`; `obj 5` (điều kiện hàm nhân hợp lệ) trỏ `practice` (không kiểm ma trận Gram) → `valid_kernel`.
- **SHOULD**:
  - `SHOULD-SYS-1` (`practice#0` ghi `f"{val:.3f}"`, `math.log / exp / sqrt`, `sum / len / max / min`, nhưng `loi_giai.py` dùng `math.hypot(*w)`, `max()`, `:.1f`, `:.2f` và không dùng `log/exp/sqrt/sum/len/min`); `SHOULD-SYS-2`.
  - `P8` lab: `w=(3, 4)` trùng với `quiz` câu 1 (`w=(3; 4)` cho lề `0.4`).
  - `P1` thân bài: `valid_kernel#0` nêu tên `"điều kiện Mercer"` nhưng không giải thích đây là định lý đặc trưng tính hợp lệ của hàm nhân.
- **INFO**: ASR 85 câu, 7 gắn cờ (1 câu `< 0.8`: frame 57 `tính→tín, lề→Lê`, 0 chưa xem xét).
- **P1/P8/P9**: `P1=0` (thân: 1) · `P8=0` · `P9=0` (chỉ có 6 điểm nhỏ & 3601 hướng dò; cộng thêm SVG lỗi ở `00000.png`).
- **PNG đã xem**: `out/CS115/L25/frames/00000.png` (**LỖI đường đỏ cắt ngang `"sát điểm"` và chạm `"lề lớn nhất"`**), `00014.png` (SVG `margin_pic` sạch), `00025.png` (bảng `hinge` sạch), `00070.png` (`practice#0` sạch).

### L26 — `Phân tích phân biệt tuyến tính (LDA) — tiêu chí Fisher`
- **Toán & kiểm số**: 15/15 `checks` PASS; $J(3,1)=16/13\approx 1{,}23$, $J(1/3,4)=5$, sai số lý thuyết `30,4% / 29,0% / 13,2%`, mô phỏng 800 điểm `12,2% / 28,0%` chính xác.
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `MUST-SYS-3` (`covers:`): `obj 1` (vì sao kéo xa 2 tâm chưa đủ) trỏ `hand_J` → `hook` + `shadow_pic`; `obj 2` (tính $J$) trỏ `vs_pca` → `sym_fisher` + `hand_J`; `obj 3` (tìm $w \propto S_w^{-1}(m_2-m_1)$) trỏ `verify` → `solution`; `obj 4` (LDA vs PCA) trỏ `verify` → `vs_pca`; `obj 5` (tối đa $C-1$ chiều, $S_w$ khả nghịch) trỏ `practice` (chỉ in `3 - 1`, không kiểm $S_w$ suy biến) → `multi`.
- **SHOULD**:
  - `de.md` (`P1`/`P8`): ghi `J = (m1-m2)^2 / (s1^2+s2^2)` nhưng không định nghĩa `s1^2` là tổng bình phương độ lệch $\sum (x-m_1)^2$ hay phương sai mẫu/tổng thể $\frac{1}{n}\sum (x-m_1)^2$ (`loi_giai.py` dùng tổng bình phương chưa chia `n` nên ra `J=4.00`; nếu chia `n=3` sẽ ra `J=12.00`, khác `mong_doi.txt`).
  - `SHOULD-SYS-1` (`practice#0` ghi `f"{val:.3f}"`, `max / min` không dùng; thiếu generator comprehension `sum(... for x in ...)` và `**2`); `SHOULD-SYS-2`.
  - `P1` thân bài: `in_ai#0` viết `("Fisherfaces")` bằng tiếng Anh không giải thích, `say` bỏ qua; `PCA` nhắc lại từ bài 16 nhưng chưa giải thích viết tắt.
- **INFO**: ASR 83 câu, 5 gắn cờ (2 câu `< 0.8`: `S w` → `SVCAP/fvk`, `nghịch đảo` → `nghiệt đạo`, 0 chưa xem xét).
- **P1/P8/P9**: `P1=0` (thân: 2) · `P8=0` · `P9=1` (có 2 lớp 800 điểm & 10 lớp chữ số, thiếu so sánh chi phí + thiếu `Hai mức quy mô:`).
- **PNG đã xem**: `out/CS115/L26/frames/00000.png` (SVG `hook` sạch), `00013.png` (bảng `sym_fisher` sạch), `00030.png` (SVG `shadow_pic` sạch), `00068.png` (`practice#0` sạch).

### L27 — `K láng giềng gần nhất (KNN): học lười, khoảng cách L1/L2, chọn K`
- **Toán & kiểm số**: 14/14 `checks` PASS; $d_1=7, d_2=5$, ví dụ 8 điểm (`0,28; 0,82; 0,82`), LOO-CV 200 điểm (`23,5% → 14,0%`), L1 vs L2, chuẩn hoá thang đo `1,00 / 0,19 / 14,00` vs `1,41 / 19,00 / 14,04` chính xác.
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `MUST-SYS-3` (`covers:`): `obj 1` (L1 vs L2) trỏ `example` (chỉ dùng L2) → `sym_dist` + `l1_vs_l2`; `obj 2` (chạy KNN bằng tay) trỏ `scaling` → `example` + `quiz`; `obj 3` (học lười) trỏ `verify` → `algorithm`; `obj 4` (chọn K bằng CV) trỏ `verify` → `choose_k`; `obj 5` (chuẩn hoá thang đo) trỏ `practice` → `scaling` + `practice`.
- **SHOULD**:
  - `SHOULD-SYS-1` (`practice#0` ghi `f"{val:.3f}"`, `math.log / exp / sqrt`, nhưng `loi_giai.py` dùng `math.hypot`, `u[0]-v[0]`, `:.1f`, `:.2f`); `SHOULD-SYS-2`.
  - `P1` thân bài & `de.md`: viết tắt `KNN` có ở `title` và `de.md` nhưng **không hề xuất hiện hoặc được giải thích trong thân bài (`hook`..`recap`)** — bài chỉ nói "K láng giềng gần nhất".
- **INFO**: ASR 74 câu, 1 gắn cờ (`0.769`: `P`→`T`, `Q`→`quỷ`, 0 chưa xem xét).
- **P1/P8/P9**: `P1=0` (thân: 2) · `P8=0` · `P9=1` (có `O(1)` vs `O(N)` và 200 điểm, thiếu ví dụ quy mô lớn cụ thể & `Hai mức quy mô:`).
- **PNG đã xem**: `out/CS115/L27/frames/00017.png` (SVG `example` sạch), `00061.png` (`practice#0` sạch).

### L28 — `Cây quyết định & rừng ngẫu nhiên (entropy, chỉ số Gini)`
- **Toán & kiểm số**: 16/16 `checks` PASS cho phần thân bài (dùng $\ln$: `0.693`, `0.562`, `0.637`, gain `0.131` vs `0.216`, Gini `0.125` vs `0.167`, 25 cây `98.3%`).
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - **Mâu thuẫn cơ số logarit giữa bài giảng và lab (`L28`)**: Toàn bộ thân bài `L28` định nghĩa và tính Entropy bằng **lôgarit tự nhiên $\ln$** ($H(0{,}5; 0{,}5) = \ln 2 \approx 0{,}693$), nhưng `labs/CS115/L28/loi_giai.py` và `mong_doi.txt` lại dùng **`math.log2`** (`H_root=1.000`, `H_split=0.7219`, `info_gain=0.2781`), còn `de.md` **không hề nói dùng cơ số 2 ($\log_2$)**. Người học làm đúng theo bài giảng dùng `math.log` sẽ ra `H_root=0.693` và bị `cham.sh` chấm trượt!
  - `MUST-SYS-3` (`covers:`): `obj 1` (chuỗi câu hỏi có/không) trỏ `gain_hand` → `hook` + `tree`; `obj 2` (entropy, Gini, độ lợi) trỏ `tree` → `sym_impurity` + `gain` + `gain_hand`; `obj 3` (chọn câu hỏi tốt nhất) trỏ `verify` → `gain` + `verify`; `obj 4` (cây sâu quá khớp & giới hạn) trỏ `verify` → `forest` + `pitfalls#1`; `obj 5` (rừng ngẫu nhiên) trỏ `practice` (lab chỉ tính entropy/Gini 1 nút chia, **không cài rừng ngẫu nhiên**) → `forest`.
- **SHOULD**:
  - `SHOULD-SYS-1` (`practice#0` thiếu `math.log2`, `**2`, `if x>0` trong `sum(...)`); `SHOULD-SYS-2`.
  - `de.md` (`P1`): dùng viết tắt `IG` chưa từng giới thiệu trong bài học (bài chỉ viết "độ lợi" / "độ lợi thông tin").
- **INFO**: ASR 74 câu, 3 gắn cờ (0 `< 0.8`, 0 chưa xem xét).
- **P1/P8/P9**: `P1=0` (thân: 2) · `P8=0` · `P9=1` (có cây 2 tầng 8 thư vs cây sâu từng mẫu + 25 cây độc lập, thiếu `Hai mức quy mô:`).
- **PNG đã xem**: `out/CS115/L28/frames/00007.png` (bảng `sym_impurity` sạch), `00026.png` (SVG `tree` sạch), `00061.png` (`practice#0` sạch).

### L29 — `Phân cụm: K-Means, phân cụm phân cấp & phân cụm phổ (ma trận Laplacian)`
- **Toán & kiểm số**: 18/18 `checks` PASS; inertia $\{0,1,10\}$, 4 bước K-Means `246 → 89,2 → 41,68 → 4`, cực tiểu địa phương `26` vs `1,5`, phân cấp liên kết đơn `7`, Laplacian trị riêng `[0.0, 0.095, 2.0, 2.105]`, vét cạn 62 gán nhãn = 31 cách chia khớp hoàn toàn.
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `MUST-SYS-3` (`covers:`): `obj 1` (mục tiêu J & tâm = trung bình) trỏ `kmeans` → `sym_inertia`; `obj 2` (chạy tay & J giảm) trỏ `verify` → `kmeans` + `km_pic`; `obj 3` (cực tiểu địa phương, khởi tạo, chọn K) trỏ `verify` → `local_min`; `obj 4` (phân cụm phân cấp) trỏ `verify` → `hierarchical`; `obj 5` (phân cụm phổ & Laplacian) trỏ `practice` (chỉ chạy K-Means 1D, **không có phân cụm phổ/Laplacian**) → `spectral`.
- **SHOULD**:
  - `SHOULD-SYS-1` (`practice#0` có `for x in ds:`, `f"{val:.3f}"` nhưng code dùng `:.2f`, `abs()`, `**2`, ternary `0 if ... else 1`, `.append()`, nested `for`); `SHOULD-SYS-2`.
  - `P1` thân bài: `sym_inertia#0` giữ từ tiếng Anh `(inertia)` mà không đọc trong `say` (chỉ có ở `show` như tên tiếng Anh).
- **INFO**: ASR 92 câu, 9 gắn cờ (3 câu `< 0.8`: `Laplacian`→`Lắp La Siang`, `cụm đầu`→`cũng đâu`, `toán dừng`→`bán dưng`, 0 chưa xem xét).
- **P1/P8/P9**: `P1=0` (thân: 2) · `P8=0` · `P9=1` (có `2^6 - 2 = 62` và nhận xét nhiều điểm tăng nhanh, thiếu số liệu quy mô lớn & `Hai mức quy mô:`).
- **PNG đã xem**: `out/CS115/L29/frames/00010.png` (SVG `km_pic` sạch), `00076.png` (`practice#0` sạch).

### L30 — `Mô hình hỗn hợp Gauss (GMM) & thuật toán EM`
- **Toán & kiểm số**: 17/17 `checks` PASS; $r_{31}=0{,}731$, $N_1=2{,}592, w_1=0{,}432, \mu_1=1{,}982$, 4 vòng EM LL `[-17.19, -13.567, -12.070, -11.456, -11.456]`, bẫy $\sigma \to 0$ (`0.40, 3.99, 39.89`) chính xác.
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - **Lệch thuật ngữ và ký hiệu nghiêm trọng giữa bài học và lab (`L30`)**: Bài giảng `L30` xuyên suốt dùng ký hiệu **$r_{ik}$** và gọi là **"độ thuộc về"**; nhưng `de.md` và `loi_giai.py`/`mong_doi.txt` lại yêu cầu tính **`gamma_1`** và gọi là **"trách nhiệm hậu nghiệm"**, đồng thời tiêu đề `de.md` hứa **"cập nhật trung bình"** nhưng `loi_giai.py` **chỉ làm bước E (tính `gamma1, gamma2, sum`), không hề cập nhật trung bình**.
  - `MUST-SYS-3` (`covers:`): `obj 1` (mô hình hỗn hợp) trỏ `em_hand` → `model`; `obj 2` (bước E bằng Bayes) trỏ `iterate` → `e_step` + `mix_pic` + `em_hand`; `obj 3` (bước M) trỏ `verify` → `m_step` + `em_hand`; `obj 4` (LL không giảm & nối K-Means) trỏ `verify` → `iterate`; `obj 5` (bẫy phương sai co về 0) trỏ `practice` → `singular`.
- **SHOULD**:
  - `SHOULD-SYS-1` (`practice#0` ghi `f"{val:.3f}"` và `math.log` không dùng; thiếu `math.pi`, `**2`, `:.6f`, `:.1f`); `SHOULD-SYS-2`.
  - `P1` thân bài: `EM` không viết tên đầy đủ tiếng Anh; `MLE`, `MAP` không nhắc lại tên tiếng Anh; `log-likelihood` trong `iterate#0` không chú thích tại chỗ.
- **INFO**: ASR 75 câu, 1 gắn cờ (0 `< 0.8`, 0 chưa xem xét).
- **P1/P8/P9**: `P1=0` (thân: 1) · `P8=0` · `P9=1` (chỉ có 6 điểm 1D, thiếu bài toán nhiều chiều có số đo quy mô + `Hai mức quy mô:`).
- **PNG đã xem**: `out/CS115/L30/frames/00008.png` (SVG `mix_pic` sạch), `00012.png` (bảng `e_step` sạch), `00060.png` (`practice#0` sạch).

### L31 — `Phân rã ma trận không âm (NMF): học “các phần” của dữ liệu`
- **Toán & kiểm số**: 10/10 `checks` PASS; SVD `[3.532, 1.878, 0, 0]`, 200 vòng NMF `12.857 → 0.0001` đều khớp.
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - **Mâu thuẫn ký hiệu giữa bài giảng và `de.md` (`L31`)**: Trong `L31` cảnh `sym_nmf#1` (`notation_note: true`), bài học **chủ động bỏ ký hiệu $\mathbf{V} \approx \mathbf{W}\mathbf{H}$ để dùng $\mathbf{X} \approx \mathbf{A}\mathbf{B}$** nhằm tránh trùng $\mathbf{H}$ (Hessian) và $\mathbf{W}$ (trọng số). Thế nhưng `labs/CS115/L31/de.md` lại viết tiêu đề `A>=0, B>=0` rồi trong đề bài dùng `V=[4, 6]`, `A=[[2]]`, `H=[[1, 1]]` (`H <- H * (A^T V)/(A^T A H)`), trộn lẫn hai hệ ký hiệu! Ngoài ra, với 1 hàng `A=[[2]]`, $h_j$ trong tử và mẫu triệt tiêu hoàn toàn ($h_j \cdot \frac{2 v_j}{4 h_j} = \frac{v_j}{2}$), nên bước 1 nhảy ngay về nghiệm đúng `err=0.0` và bước 2 lặp lại y hệt bước 1.
  - `MUST-SYS-3` (`covers:`): `obj 1` (NMF tổng không âm) trỏ `vs_svd` → `sym_nmf` + `parts_pic`; `obj 2` (so với SVD) trỏ `run` → `vs_svd`; `obj 3` (quy tắc nhân giữ không âm & giảm E) trỏ `verify` → `updates` + `run` + `verify` + `practice`; `obj 4` (không duy nhất, phụ thuộc khởi tạo, chọn K) trỏ `practice` → `run#1` + `pitfalls#2` + `quiz#1`.
- **SHOULD**:
  - `SHOULD-SYS-1` (`practice#0` ghi `f"{val:.3f}"` không dùng; thiếu `zip()`, `range(1, 3)`, `**2`, `:.1f`); `SHOULD-SYS-2`.
- **INFO**: ASR 71 câu, 3 gắn cờ (0 `< 0.8`, 0 chưa xem xét).
- **P1/P8/P9**: `P1=0` (thân: 2) · `P8=0` · `P9=1` (chỉ có ma trận $4\times 4$ và lưu ý $K \ll N, D$, thiếu quy mô thực tế & `Hai mức quy mô:`).
- **PNG đã xem**: `out/CS115/L31/frames/00011.png` (SVG `parts_pic` sạch), `00015.png` (bảng `vs_svd` sạch), `00056.png` (`practice#0` sạch).

### L32 — `t-SNE: trực quan hoá dữ liệu nhiều chiều bằng xác suất láng giềng`
- **Toán & kiểm số**: 20/20 `checks` PASS; $p=(0{,}806; 0{,}180; 0{,}015)$, $H=0{,}545$, perplexity `1.72`, phân phối t ở $d=1,2,3$ (`0.5, 0.2, 0.1`), $d\approx 2{,}53$, KL `0.368` vs `0.511` đều khớp.
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `MUST-SYS-3` (`covers:`): `obj 1` (mục tiêu vẽ 2D giữ láng giềng) trỏ `p_hand` → `hook`; `obj 2` (tính $p$) trỏ `reading` → `sym_p` + `p_hand`; `obj 3` (độ bối rối) trỏ `verify` → `perplexity` + `p_hand`; `obj 4` (đuôi dày & KL) trỏ `verify` → `sym_q` + `tail_pic` + `kl` + `verify`; `obj 5` (đọc hình t-SNE) trỏ `practice` (chỉ tính KL 2 phần tử) → `reading` + `pitfalls`.
- **SHOULD**:
  - `SHOULD-SYS-1` (`practice#0` ghi `f"{val:.3f}"`, `math.exp / sqrt` không dùng; thiếu `zip()`, `abs()`, `int()`, `:.6f`); `SHOULD-SYS-2`.
  - `de.md` (`P1`): ghi `(đơn vị nat)` nhưng **khái niệm/đơn vị `nat` chưa từng được dạy trong `L32` hay `L12, L20`**.
  - `P1` thân bài: `sym_q#0` có `(phân phối t của Student)` và `kl#0` có `KL(P||Q)` không giải thích chữ Student/KL; `t-SNE` không mở rộng cụm tiếng Anh; `perplexity#0` viết `perplexity` trong `show` nhưng không chú thích cách đọc trong `say`.
- **INFO**: ASR 80 câu, 4 gắn cờ (0 `< 0.8`, 0 chưa xem xét).
- **P1/P8/P9**: `P1=0` (thân: 1) · `P8=0` · `P9=1` (có `784 chiều → 2 chiều` và `10 000 cặp`, thiếu chi phí tính cặp $O(N^2)$ & `Hai mức quy mô:`).
- **PNG đã xem**: `out/CS115/L32/frames/00024.png` (bảng `sym_q` sạch), `00028.png` (SVG `tail_pic` sạch), `00065.png` (`practice#0` sạch).

---

## 5. Danh sách đầy đủ 36 PNG đã xem

- **L22**: `out/CS115/L22/frames/00006.png`, `00012.png`, `00017.png`, `00067.png`, `00068.png`, `00070.png`
- **L23**: `out/CS115/L23/frames/00000.png`, `00013.png`, `00021.png`, `00084.png`
- **L24**: `out/CS115/L24/frames/00008.png`, `00076.png`
- **L25**: `out/CS115/L25/frames/00000.png` (**lỗi SVG cắt chữ**), `00014.png`, `00025.png`, `00070.png`
- **L26**: `out/CS115/L26/frames/00000.png`, `00013.png`, `00030.png`, `00068.png`
- **L27**: `out/CS115/L27/frames/00017.png`, `00061.png`
- **L28**: `out/CS115/L28/frames/00007.png`, `00026.png`, `00061.png`
- **L29**: `out/CS115/L29/frames/00010.png`, `00076.png`
- **L30**: `out/CS115/L30/frames/00008.png`, `00012.png`, `00060.png`
- **L31**: `out/CS115/L31/frames/00011.png`, `00015.png`, `00056.png`
- **L32**: `out/CS115/L32/frames/00024.png`, `00028.png`, `00065.png`

---

## 6. Kết luận `NO-GO` & Việc cần sửa trước khi duyệt lại

1. **Sửa `practice` trên 11/11 bài (`L22–L32`)**: Bỏ lộ `loi_giai.py` và `mong_doi.txt` trước `pause: 30`; viết lại `practice#0` khớp 100% cú pháp Python thực tế của từng bài + giảng `bash labs/cham.sh`.
2. **Sửa `labs/CS115/L22..L32/de.md` & `loi_giai.py`**:
   - Ghi rõ định dạng stdout từng dòng ở cả 11 `de.md`.
   - **L22**: Sửa `dq=z={dz:.1f}` trong `loi_giai.py` và `mong_doi.txt` (không gán nhầm `dz` vào `dq`).
   - **L23**: Sửa `"biến thể ReLU"` thành `"hàm ReLU"` và chú thích `n_in, n_out`.
   - **L24**: Đổi số liệu `[5, 3, 2]` để không trùng ví dụ trong bài.
   - **L26**: Ghi rõ `s1^2 = sum((x - m1)^2)` (tổng bình phương độ lệch, chưa chia `n`).
   - **L28**: Thống nhất cơ số logarit (`log2` trong `de.md` hoặc đổi `loi_giai.py` sang `math.log` theo đúng bài học).
   - **L30**: Thống nhất tên biến/khái niệm (`r_1`, `"độ thuộc về"` như bài học, hoặc bổ sung bài giải cập nhật trung bình đúng như tiêu đề `de.md`).
   - **L31**: Thống nhất ký hiệu `X ≈ A·B` (không trộn `V, H` của Lee & Seung vào `de.md`) và chọn ví dụ không bị triệt tiêu $h_j$ ngay ở bước 1.
   - **L32**: Giải thích `(đơn vị nat)` hoặc bỏ chữ `nat` khỏi `de.md`.
3. **Sửa `L25 hook#0` SVG**: Dời nhãn `"sát điểm"` (`x=130, y=375`) sang trái hoặc dùng `text-anchor="end"` để không bị đường đỏ cắt ngang, và nhích `"lề lớn nhất"` khỏi đường đỏ/xanh lá.
4. **Sửa `covers:` trên 11/11 bài** về đúng cảnh dạy thật của từng mục tiêu.
5. **Bổ sung `<p class="note"><b>Hai mức quy mô:</b> ...` và chú thích các thuật ngữ tiếng Anh/viết tắt còn thiếu (`P1`, `P9`)** rồi dựng lại video, kiểm tra `spec_sha256` / `asr` / `layout_scan` / `screen_code`.
