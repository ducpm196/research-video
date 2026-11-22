# Báo cáo Kiểm định Độc lập WP-AF4-5 — Stage 9 CS115 (`L33–L43`)

- **Phạm vi**: 11 bài (`L33–L43`) trong `D:\research-video` (`curriculum/cs115.yaml`, `lessons/cs115/L33..L43_*.yaml`, `labs/CS115/L33..L43/{de.md,loi_giai.py,mong_doi.txt}`, `out/CS115/L33..L43/{build_report.json,L*.srt,asr_report.md,frames/*.png}`, `audit/layout_CS115.tsv`).
- **Kết luận chung**: **`NO-GO`** — Kiến thức toán học và hình ảnh SVG trong thân bài chính xác, khớp `curriculum ↔ YAML` và vượt các cổng máy (`lint` 0/0, `spec_sha256` 11/11 khớp, `SRT == say` 11/11 khớp, `layout_CS115.tsv` 0 lỗi, 27/27 PNG xem sạch). Tuy nhiên **cả 11/11 bài** đều vướng các lỗi hệ thống ở `practice`, `labs/.../de.md`, `covers:`, và thiếu quy mô/chú thích P1 ở `practice#0`/`de.md`.

---

## 1. Bảng tổng hợp toàn đợt (`L33–L43`)

| Bài | sha16 (YAML) | Thời lượng | `spec` / `SRT` / `lint` / `lab_py` | P1 (thân + `practice#0` + `de.md`) | P8 (`practice` + `de.md`) | P9 (thân / `recap`) | `covers:` | Số MUST | Số SHOULD | Kết luận |
|---|---|---|---|---|---|---|---|---|---|---|
| L33 | `99c642f03fdb20e6` | 9,11 phút | PASS / PASS / 0-0 / PASS | **0** | **0** | **0** / thiếu | Sai | 4 | 2 | NO-GO |
| L34 | `be0f2b51e411a13a` | 9,00 phút | PASS / PASS / 0-0 / PASS | **0** | **0** | **2** / thiếu | Sai | 3 | 2 | NO-GO |
| L35 | `22677f61a40a3fd0` | 8,84 phút | PASS / PASS / 0-0 / PASS | **1** | **0** | **2** / thiếu | Sai | 3 | 1 | NO-GO |
| L36 | `2fec11b01fa4d20e` | 8,34 phút | PASS / PASS / 0-0 / PASS | **0** | **0** | **1** / thiếu | Sai | 4 | 2 | NO-GO |
| L37 | `322373ba27bb1727` | 8,26 phút | PASS / PASS / 0-0 / PASS | **1** | **0** | **0** / thiếu | Sai | 3 | 3 | NO-GO |
| L38 | `f3a09e66f7aa93da` | 8,49 phút | PASS / PASS / 0-0 / PASS | **1** | **0** | **0** / thiếu | Sai | 4 | 1 | NO-GO |
| L39 | `c964696d6fed0e1b` | 9,04 phút | PASS / PASS / 0-0 / PASS | **1** | **0** | **0** / thiếu | Sai | 4 | 2 | NO-GO |
| L40 | `45ce50e6274aa293` | 7,85 phút | PASS / PASS / 0-0 / PASS | **1** | **0** | **1** / thiếu | Sai | 4 | 2 | NO-GO |
| L41 | `e32e25f265bd27a9` | 8,90 phút | PASS / PASS / 0-0 / PASS | **1** | **0** | **2** / thiếu | Sai | 3 | 1 | NO-GO |
| L42 | `660d46814b5e4a0f` | 9,45 phút | PASS / PASS / 0-0 / PASS | **1** | **0** | **0** / thiếu | Sai | 4 | 1 | NO-GO |
| L43 | `5f9453312aefa501` | 8,26 phút | PASS / PASS / 0-0 / PASS | **1** | **0** | **2** / thiếu | Sai | 4 | 1 | NO-GO |

### Tỷ lệ đạt chuẩn
- **P1 = 2**: **0/11 (0%)** khi tính đủ thân bài + `practice#0` + `de.md` (`P1=1`: 8/11 = 72,7%; `P1=0`: 3/11 = 27,3%). *(Nếu chỉ tính riêng thân bài, 10/11 bài L34–L43 đạt sạch; chỉ L33 còn viết tắt `GD`/`MAP`/`KKT` chưa nhắc lại trên màn hình).*
- **P8 = 2**: **0/11 (0%)** (11/11 bài đều `P8 = 0`).
- **P9 = 2**: **0/11 (0%)** nếu yêu cầu cả thân bài lẫn `recap` có *Hai mức quy mô*; **4/11 (36,4%)** nếu chỉ xét thân bài (`L34, L35, L41, L43` đạt; `L36, L40` mức 1; `L33, L37, L38, L39, L42` mức 0).
- **Cổng máy & đối chiếu số**:
  - `lv.py curriculum curriculum/cs115.yaml`: `47 bài, 47 đã có đặc tả, 0 lỗi`.
  - `lv.py lint` trên cả 11 file: `0 FAIL, 0 WARN`.
  - `build_report.json` (`spec_sha256 == lv.spec_digest`), `L*.srt == say`, `voices == ['vi-VN-NamMinhNeural']`: **11/11 khớp 100%**.
  - `audit/review/arith_scan.py CS115`: `38 phép tính kiểm được, 0 FAIL`.
  - `audit/review/screen_code.py check --course CS115`: `100 khối — PASS 125 · FAIL 0`.
  - `audit/layout_CS115.tsv`: 2 bytes (`\r\n`, 0 lỗi bố cục).
  - Kiểm độc lập toàn bộ phép tính trong YAML + chạy trực tiếp `labs/CS115/L33..L43/loi_giai.py` so với `mong_doi.txt`: **11/11 khớp**. *(Lưu ý INFO: `audit/review/lab_gate.py CS115` báo `0 PASS · 47 FAIL` do `cham.sh` chạy dưới `Git Bash` không gọi được `python` trên môi trường này).*

---

## 2. Lỗi hệ thống chung trên toàn bộ 11 bài (`L33–L43`)

1. **[MUST — P8] Lộ lời giải `loi_giai.py` và stdout trước `pause` ở `practice` (11/11 bài):**
   - Trong cả 11 bài, `practice#1` (`Cài đặt kiểm chứng CS115:Lxx bằng Python`) in nguyên văn mã nguồn `loi_giai.py` lên màn hình, rồi `practice#2` (`Đầu ra chạy thật`) in kết quả, trong khi `pause: 30` lại nằm ở `practice#3`. Người học nhìn thấy toàn bộ đáp án trước khi được yêu cầu tự làm (trái ngược hoàn toàn với chuẩn khoá đã chốt ở `L18`, `L21`).
2. **[MUST — P8] `labs/CS115/L33..L43/de.md` thiếu quy cách định dạng stdout (11/11 bài):**
   - Không có `de.md` nào quy định chuỗi nhãn/định dạng in (`s1= ...`, `out_dim=...`, `vanish_20=...`, `adaboost_alpha=...`, `latent=...`, `kurt=...`, `target=...`, `w_near_01=...`, `weights=...`, `vae_kl=...`, `alpha_bar_1000=...`, số chữ số sau dấu phẩy), khiến người học chỉ đọc `de.md` không thể viết chương trình khớp `mong_doi.txt` / `cham.sh`.
3. **[MUST — `covers:`] Ánh xạ mục tiêu → phân cảnh sai (11/11 bài):**
   - `covers:` trong cả 11 bài bị gán máy móc vào các cảnh cuối (`example`, `verify`, `practice`), trỏ sai sang cảnh không dạy mục tiêu tương ứng.
4. **[SHOULD — P1] `practice#0` lệch cú pháp thực tế của `loi_giai.py` (10/11 bài `L34–L43`):**
   - Bảng `practice#0` sinh khuôn mẫu chứa `f"{val:.3f}"` dù không có `loi_giai.py` nào dùng `:.3f`, đồng thời bỏ sót nhiều cú pháp có mặt trong `loi_giai.py` (`//`, `**`, `+=`, `*=`, `range`, `zip`, `round`, `int()`, `abs()`, `:.2e`, `:.4f`, `:.5f`, `:.6f`, `:.1f`, list comprehension, tuple unpacking, ternary `if/else`).
5. **[SHOULD — P9] `recap` thiếu "Hai mức quy mô" (11/11 bài) & thân bài thiếu quy mô (7/11 bài):**
   - Không có `recap` nào nhắc lại đối chiếu ở 2 mức quy mô/thời gian kèm đánh đổi. Trong thân bài, `L33, L37, L38, L39, L42` (P9=0) và `L36, L40` (P9=1) chưa đạt chuẩn 2 mức quy mô + đánh đổi.

---

## 3. Chi tiết từng bài (`L33–L43`)

### L33 — Tổng ôn: bảng thuật toán & 3 câu hỏi vàng (`99c642f03fdb20e6`)
- **Toán & sư phạm**: Đúng `curriculum` (`A14` KNN không có hàm mất mát; K-Means tổng bình phương; LDA tỉ số Fisher; hồi quy 4 căn phòng `w=1,4; b=0,5; MSE=0,05`; cụm `(0,1,10)` tâm `11/3` tổng bình phương `60,67` vs trung vị `1` tổng khoảng cách `10`). Không có câu `"càng ..."`. Lời đọc `say` rõ; `asr_report.md` có 2 cờ đã xem xét (`câu 10` "gradient descent", `câu 42` "sigmoid" — PARTIAL).
- **MUST**:
  1. `[P8]` `practice#1` (`frames/00069.png`) lộ nguyên văn `loi_giai.py` và `practice#2` lộ stdout trước `pause: 30` ở `practice#3`.
  2. `[P8]` `labs/CS115/L33/de.md` thiếu định dạng stdout (`s1= ...`, `s2= ...`, `s3= ...`) **và lệch hoàn toàn với `loi_giai.py`**: `de.md` ghi `(tabular 500, tabular 100k, non_linear_neighbors)`, không nêu quy tắc chọn (`n < 1000 -> Linear/Ridge`, else `Tree/Boosting`, `viz -> PCA/t-SNE`), trong khi `loi_giai.py` chạy `pick(500, 'tab')`, `pick(100000, 'tab')`, `pick(5000, 'viz')`.
  3. `[P1]` `de.md` dùng thuật ngữ tiếng Anh chưa chú thích **`tabular`**, **`non_linear_neighbors`**; `table#0`/`map#0` hiện `GD`, `KKT`, `MAP` chưa nhắc lại mở rộng ở bài tổng ôn; `practice#0` thiếu giải thích toán tử `==`, `<` và biểu thức điều kiện một dòng `... if n < 1000 else ...`.
  4. `[covers]` Sai hết 4 ánh xạ: `obj1 -> table` (đúng: `questions`), `obj2 -> apply_lin` (đúng: `table`+`verify`), `obj3 -> verify` (đúng: `symbols`), `obj4 -> practice` (đúng: `apply`+`quiz`; `practice` không áp 3 câu hỏi vàng).
- **SHOULD**:
  1. `[P9]` Cả thân bài và `recap` đều chưa có so sánh ≥2 mức quy mô + đánh đổi (`P9 = 0`).
  2. `[ASR]` `symbols#0`: `sigmoid` vẫn là nút thắt ASR (`sít moi`, đã gắn nhãn PARTIAL).

### L34 — Phép tích chập & mạng nơ-ron tích chập (CNN) (`be0f2b51e411a13a`)
- **Toán & sư phạm**: Đúng `curriculum` (tương quan chéo vs lật bộ lọc; `(N-K+2P)/S + 1`; tham số `K*K*C_vào*C_ra + C_ra = 448`; ma trận thưa 9×16; max pooling 0 tham số; ảnh 32×32 vs 64×64: 163 850 vs 655 370). Không có câu `"càng ..."`.
- **MUST**:
  1. `[P8]` `practice#1` lộ nguyên văn `loi_giai.py` và `practice#2` lộ stdout trước `pause: 30`.
  2. `[P8]` `labs/CS115/L34/de.md` thiếu định dạng stdout (`out_dim=14x14x16=3136`, `conv_params=448`) và không yêu cầu tính `dense = out_sz * out_sz * 16`.
  3. `[covers]` `obj2 -> sharing` (đúng: `size`), `obj3 -> verify` (đúng: `sharing`), `obj5 -> practice` (đúng: `sharing`).
- **SHOULD**:
  1. `[P1]` `de.md` dùng **`C_in`**, **`C_out`**, **`bias`** chưa chú thích (bài dạy dùng `C_vào`, `C_ra`, `hệ số tự do`/`hệ số chặn`); `practice#0` kê `f"{val:.3f}"` không dùng nhưng thiếu phép chia nguyên `//` và gán nhiều biến `n, k, p, s = ...`.
  2. `[P8/P9]` Lab lặp lại đúng số `448` (`3×3, 3→16`) của `hook` và `sharing`; `recap` chưa nhắc lại 2 mức quy mô `32×32` vs `64×64` (thân bài `pitfalls` Lỗi 4 đã có).

### L35 — Mạng nơ-ron hồi tiếp (RNN), lan truyền ngược theo thời gian & LSTM (`22677f61a40a3fd0`)
- **Toán & sư phạm**: Đúng `curriculum` (`hồi tiếp` ≠ `hồi quy`, $h_1=0{,}7616; h_2=0{,}3634; h_3=0{,}9749$; đạo hàm lùi $0{,}0248\cdot 0{,}434 \approx 0{,}0108$; $0{,}5^{10}\approx 0{,}000977$; $1{,}5^{50}\approx 638\text{ triệu}$; cắt theo chuẩn $(30,40)\to(3,4)$ vs kẹp từng chiều $(5,5)$). Không có `"càng ..."`.
- **MUST**:
  1. `[P8]` `practice#1` lộ `loi_giai.py` và `practice#2` lộ stdout trước `pause: 30`.
  2. `[P8]` `labs/CS115/L35/de.md` thiếu định dạng stdout (`vanish_20=... explode_20=...`, `clipped_norm=...`).
  3. `[covers]` `obj1 -> hand_back` (đúng: `sym_rnn`/`unroll_pic`), `obj2 -> example` (sai: `example` chỉ đếm 620 tham số; đúng là `sym_rnn`), `obj4 -> practice` (sai: `practice` không có LSTM; đúng là `lstm`).
- **SHOULD**:
  1. `[P1/P9]` `de.md` dùng `clip=5.0` không chú thích; `practice#0` kê `:.3f`, `sum/len/max` dư và thiếu `**`, `:.5f`, `:.2f`. `recap` chưa nhắc lại 2 mốc bước thời gian (`k=1, 10, 50` ở thân bài `bptt`).

### L36 — Boosting: AdaBoost & gradient boosting (so với rừng ngẫu nhiên) (`2fec11b01fa4d20e`)
- **Toán & sư phạm**: Đúng `curriculum` ($\alpha=\frac{1}{2}\ln\frac{1-\varepsilon}{\varepsilon}$, 10 mẫu $\varepsilon=0{,}2\to 0{,}25 / 0{,}0625$, tỉ lệ 5 vòng $4^5=1024$; GBDT trên $(1,2,3,10)$ MSE $12{,}5\to 3{,}5\to 1{,}25$, 50 vòng $\to 0{,}5$). Không có `"càng ..."`.
- **MUST**:
  1. `[P8]` `practice#1` lộ `loi_giai.py` và `practice#2` lộ stdout trước `pause: 30`.
  2. `[P8]` `labs/CS115/L36/de.md` thiếu định dạng stdout (`adaboost_alpha=...`, `gbdt_f2=... rem=...`) **và thiếu giá trị đầu vào `y=10.0, f=0.0`** (người học không thể tái tạo `7.50` và `2.50` từ `de.md`).
  3. `[P1]` `de.md` viết sai chính tả **`GDBT`** (thay vì `GBDT`), và cả `GBDT` lẫn `GDBT` đều **chưa từng được giảng/mở rộng trong bài**; `de.md` dùng `lr=0.5` chưa chú thích.
  4. `[covers]` `obj2 -> gb_example` (sai: `gb_example` là GBDT, AdaBoost là `reweight`), `obj4 -> practice` (sai: `practice` không so sánh rừng ngẫu nhiên; đúng là `vs_forest` + `pitfalls#0`).
- **SHOULD**:
  1. `[P1]` `practice#0` kê `:.3f` dư và thiếu `range(...)`, `+=`, biến `_`.
  2. `[P9]` Thân bài chỉ có tỉ lệ qua 5 vòng trên 1 ví dụ nhỏ (`P9 = 1`), `recap` thiếu quy mô.

### L37 — Autoencoder: nén phi tuyến bằng mạng nơ-ron (so với PCA) (`322373ba27bb1727`)
- **Toán & sư phạm**: Đúng `curriculum` (cổ chai, AE tuyến tính 1 lớp ẩn trùng không gian con PCA với loss `4.0`, bài toán vòng tròn phi tuyến). Câu `"càng ..."` (`tradeoff#0`: *"Cổ chai càng hẹp thì nén càng mạnh nhưng khôi phục càng mất mát"*) chuẩn xác.
- **MUST**:
  1. `[P8]` `practice#1` lộ `loi_giai.py` và `practice#2` lộ stdout trước `pause: 30`.
  2. `[P8]` `labs/CS115/L37/de.md` thiếu định dạng stdout (`latent=[...]` làm tròn 3 chữ số, `recon_mse=...` định dạng `:.2e`).
  3. `[covers]` `obj3 -> verify` (sai: `verify` kiểm PCA tuyến tính qua SVD, phi tuyến là `nonlinear`), `obj4 -> practice` (sai: `practice` không dạy mã không duy nhất/đánh đổi, đúng là `tradeoff` + `pitfalls#2`).
- **SHOULD**:
  1. `[P8]` Lab dùng cùng hướng `(1/sqrt(2), 1/sqrt(2))` như ví dụ bài học và phụ thuộc vào sai số dấu phẩy động IEEE-754 `recon_mse=2.47e-31` (nếu viết phép trừ khác thứ tự hoặc đổi biểu thức toán học tương đương có thể ra `0.00e+00` và bị `cham.sh` chấm sai).
  2. `[P1]` `practice#0` kê `:.3f` và `math.log/exp` dư, thiếu `zip`, `round`, `sum/len`, list comprehension.
  3. `[P9]` Thân bài (`pitfalls` Lỗi 4 chỉ đổi đơn vị m vs mm, không phải quy mô dữ liệu/hệ thống) và `recap` chưa có 2 mức quy mô + đánh đổi (`P9 = 0`).

### L38 — Phân tích thành phần độc lập (ICA): tách các nguồn bị trộn lẫn (`f3a09e66f7aa93da`)
- **Toán & sư phạm**: Đúng `curriculum` (`Cov=0` chưa độc lập; độ nhọn $\mathbb{E}[y^4]-3$, đều $-1{,}2$, trộn hai nguồn $-0{,}6$; làm trắng $\text{Cov}=\mathbf{I}$, lệch $9{,}5^\circ$; lab `kurt = -1.3600`). Không có `"càng ..."`.
- **MUST**:
  1. `[P8]` `practice#1` lộ `loi_giai.py` và `practice#2` lộ stdout trước `pause: 30`.
  2. `[P8]` `labs/CS115/L38/de.md` **mâu thuẫn với `loi_giai.py`**: `de.md` yêu cầu `vs dấu đảo -x`, còn `loi_giai.py` lại tính `kurt([-2.0 * x for x in xs])` (`scaled_neg_kurt`, tức nhân `-2`); ngoài ra `de.md` thiếu định dạng stdout (`kurt=... scaled_neg_kurt=...`, `sign_scale_invariant=...`).
  3. `[P1]` `de.md` dùng thuật ngữ tiếng Anh chưa chú thích **`excess kurtosis`**, **`kurtosis`** (trong bài chỉ dùng tiếng Việt `độ nhọn`) và biến `sd` chưa định nghĩa.
  4. `[covers]` `obj2 -> hand_mix` (đúng: `prereq`), `obj3 -> verify` (đúng: `algorithm`+`example`), `obj4 -> practice` (sai: `practice` không kiểm điều kiện nguồn chuẩn/thứ tự; đúng: `gaussian` + `example#1`).
- **SHOULD**:
  1. `[P1/P9]` `practice#0` kê `:.3f` dư, thiếu `sum`, `len`, `abs`, `int`, `**`; thân bài và `recap` thiếu 2 mức quy mô + đánh đổi (`P9 = 0`).

### L39 — Học tăng cường: MDP, phương trình Bellman & Q-learning (`c964696d6fed0e1b`)
- **Toán & sư phạm**: Đúng `curriculum` (chiết khấu $\gamma\in[0,1)$, ví dụ 3 ô A–B–C, 3 lượt Q-learning, $\varepsilon$-greedy 300 lượt hội tụ `[8.1, 9.0], [9.0, 10.0]`). Câu `"càng ..."` (`sym_return#0`: *"phần thưởng càng muộn càng bị giảm giá trị"*) hợp lý với $0<\gamma<1$ (nếu $\gamma=0$ thì mọi bước sau bằng 0 ngay lập tức).
- **MUST**:
  1. `[P8]` `practice#1` lộ `loi_giai.py` và `practice#2` lộ stdout trước `pause: 30`.
  2. `[P8]` `labs/CS115/L39/de.md` tiêu đề ghi `Q-learning 2 trạng thái với ε-tham lam` nhưng nội dung chỉ tính 1 bước cập nhật công thức, và thiếu định dạng stdout (`target=... td_err=...`, `q_new=...`).
  3. `[covers]` `obj1 -> qlearning` (đúng: `hook`+`bellman`), `obj2 -> verify` (đúng: `sym_return`+`bellman`), `obj4 -> practice` (sai: `practice` không có thăm dò; đúng: `qlearning`+`explore`).
- **SHOULD**:
  1. `[P8/P1]` Lab trùng tham số `alpha=0.5, gamma=0.9, maxQ'=10` với `qlearning#0`; `practice#0` kê `:.3f` dư, thiếu tuple unpacking.
  2. `[P9]` Thân bài và `recap` chưa có 2 mức quy mô + đánh đổi (`P9 = 0`).
  3. `[INFO]` Từ `Q-learning` chỉ xuất hiện trên màn hình (`title`, `explore#1`), chưa được đọc to trong `say`.

### L40 — UMAP: giảm chiều bằng đồ thị láng giềng (so với t-SNE) (`45ce50e6274aa293`)
- **Toán & sư phạm**: Đúng `curriculum` (trọng số $e^{-(d-\rho)/\sigma}$, đối xứng hoá $a+b-ab = 0{,}8035$ / $0{,}7642$, BCE $0{,}546$ nhỏ nhất tại $v=w$, khẳng định so sánh t-SNE là thực nghiệm không phải định lý). Câu `"càng ..."` (`graph_pic#0`) đúng chú thích hình.
- **MUST**:
  1. `[P8]` `practice#1` lộ `loi_giai.py` và `practice#2` lộ stdout trước `pause: 30`.
  2. `[P8]` `labs/CS115/L40/de.md` **lệch `loi_giai.py`** và thiếu định dạng stdout: `de.md` nêu `[0, 1, 5, 6]` nhưng `loi_giai.py` không dùng mảng này, không nêu `w21=0.0` trong `de.md`, không hỏi điều kiện `keeps_cluster` (`w_near > 10 * w_cross`), và thiếu định dạng `w_near_01=... w_cross_12=...`, `keeps_cluster=...`.
  3. `[covers]` `obj2 -> compare` (sai: `compare` so sánh t-SNE, phép đối xứng hoá ở `sym_w`+`hand_w`), `obj4 -> practice` (sai: `practice` không so sánh t-SNE; đúng: `compare`+`pitfalls`).
- **SHOULD**:
  1. `[P1]` `de.md` và `practice#3` dùng `1-NN` chưa giải thích viết tắt `NN`; `practice#0` kê `:.3f` dư và thiếu `int()`.
  2. `[P9]` Thân bài mới nêu định tính *"với hàng triệu điểm, t-SNE chậm"* (`P9 = 1`), chưa có bảng số ≥2 mức quy mô; `recap` thiếu quy mô.

### L41 — Cơ chế attention & Transformer (`e32e25f265bd27a9`)
- **Toán & sư phạm**: Đúng `curriculum` (hàng softmax cộng = 1, chia $\sqrt{d}$ đưa phương sai $15{,}98\to 0{,}998$ với $d=16$, bất biến hoán vị khi thiếu positional encoding, chi phí $n^2$: 1000→1M, 2000→4M, 4000→16M; giải thích minh bạch độ lệch `0,001` do làm tròn ở `verify#1`). Câu `"càng ..."` (`attn_pic#0`) đúng.
- **MUST**:
  1. `[P8]` `practice#1` lộ `loi_giai.py` và `practice#2` lộ stdout trước `pause: 30`.
  2. `[P8]` `labs/CS115/L41/de.md` thiếu định dạng stdout (`weights=[...] sum=...`, `attn_out=...`).
  3. `[covers]` `obj2 -> verify` (đúng: `example`), `obj3 -> verify` (sai: chia $\sqrt{d}$ ở `sqrt_d`), `obj4 -> practice` (sai: `practice` không có mã hoá vị trí hay $n^2$, đúng là `order`).
- **SHOULD**:
  1. `[P1/P9]` `practice#0` kê `:.3f` và `math.log` dư, thiếu `round`, `sum`, list comprehension; `recap` mới nhắc `chi phí n²`, chưa nhắc lại 2 mức quy mô ở `order`.

### L42 — Mô hình sinh (1): Variational Autoencoder & GAN (`660d46814b5e4a0f`)
- **Toán & sư phạm**: Đúng `curriculum` (ELBO $\le \ln p(1)\approx -1{,}5155$, tích phân KL kiểm bằng sympy, mẹo tham số hoá lại $z=\mu+\sigma\varepsilon$, GAN $D^* = p_{\text{thật}}/(p_{\text{thật}}+p_{\text{giả}})$ và trò chơi $-\ln 4$). Không có `"càng ..."`.
- **MUST**:
  1. `[P8]` `practice#1` lộ `loi_giai.py` và `practice#2` lộ stdout trước `pause: 30`.
  2. `[P8]` `labs/CS115/L42/de.md` thiếu định dạng stdout (`vae_kl=...`, `gan_nash_d=0.50 val=...`) và không nhắc in `gan_nash_d=0.50`.
  3. `[P1]` `de.md` dùng thuật ngữ **`cân bằng Nash`** chưa từng được giảng trong L42 hay bất kỳ bài trước nào của CS115.
  4. `[covers]` `obj3 -> verify` (sai: `verify` kiểm ELBO, mẹo tham số hoá lại là `reparam`), `obj4 -> practice` (sai: `practice` chỉ tính $-\ln 4$, trò chơi GAN & $D^*$ là `gan`).
- **SHOULD**:
  1. `[P1/P9]` `practice#0` kê `:.3f`, `math.exp/sqrt` dư và thiếu `**`; thân bài và `recap` chưa có 2 mức quy mô + đánh đổi (`P9 = 0`).

### L43 — Mô hình sinh (2): mô hình khuếch tán (diffusion) (`5f9453312aefa501`)
- **Toán & sư phạm**: Đúng `curriculum` (công thức gộp $\bar{\alpha}_t$, phân biệt $\beta_t$ với Momentum/Adam $\beta$, lịch tuyến tính $0{,}0001\to 0{,}02$ qua $T=1000$ cho $\bar{\alpha}_{1000}\approx 4{,}04\cdot 10^{-5}$, mô phỏng 200 000 mẫu khớp 1,89 và 0,32, đánh đổi tốc độ sinh chậm vs huấn luyện ổn định). Không có `"càng ..."`.
- **MUST**:
  1. `[P8]` `practice#1` lộ `loi_giai.py` và `practice#2` lộ stdout trước `pause: 30`.
  2. `[P8]` `labs/CS115/L43/de.md` thiếu định dạng stdout (`alpha_bar_1000=...`, `noise_scale=...`).
  3. `[P8]` Số liệu lab (`T=1000`, `0.0001 -> 0.02`, ra `4.04e-05`) **trùng hoàn toàn 100%** với ví dụ `schedule` và `noise_pic` trong thân bài.
  4. `[covers]` `obj2 -> schedule` (sai: công thức gộp nhiều bước là `closed`+`two_steps`), `obj3 -> verify` (đúng: `schedule`), `obj4 -> practice` (sai: `practice` không có MSE/sinh chậm, đúng là `reverse`).
- **SHOULD**:
  1. `[P1/P9]` `practice#0` kê `:.3f` dư, thiếu `range`, `*=`, `**0.5`; `de.md` dùng `prod(...)`, `sqrt(...)` dạng mã; `recap` chưa nhắc lại 2 mốc thời gian ở `schedule` (`t=1, 100, 500, 1000`).

---

## 4. Danh sách PNG đã xem trực tiếp (27 khung)

- **L33**: `out/CS115/L33/frames/00003.png` (bảng `prereq`), `00011.png` (SVG `questions`), `00068.png` (`practice#0`), `00069.png` (`practice#1` lộ `loi_giai.py`).
- **L34**: `out/CS115/L34/frames/00010.png` (SVG `slide_pic`), `00025.png` (bảng `size`), `00064.png` (`practice#0`).
- **L35**: `out/CS115/L35/frames/00011.png` (SVG `unroll_pic`), `00064.png` (`practice#0`).
- **L36**: `out/CS115/L36/frames/00020.png` (SVG `stair_pic`), `00064.png` (`practice#0`).
- **L37**: `out/CS115/L37/frames/00013.png` (SVG `bottleneck_pic`), `00063.png` (`practice#0`).
- **L38**: `out/CS115/L38/frames/00006.png` (bảng `prereq`), `00014.png` (SVG `mix_pic`), `00064.png` (`practice#0`).
- **L39**: `out/CS115/L39/frames/00020.png` (SVG `value_pic`), `00067.png` (`practice#0`).
- **L40**: `out/CS115/L40/frames/00013.png` (SVG `graph_pic`), `00054.png` (`practice#0`).
- **L41**: `out/CS115/L41/frames/00012.png` (SVG `attn_pic`), `00068.png` (`practice#0`).
- **L42**: `out/CS115/L42/frames/00006.png` (bảng `prereq`), `00014.png` (SVG `gen_pic`), `00070.png` (`practice#0`).
- **L43**: `out/CS115/L43/frames/00012.png` (SVG `noise_pic`), `00054.png` (`practice#0`).

Tất cả 27 khung đều hiển thị sắc nét, không đè chữ, không tràn khung, không cắt công thức KaTeX.

---

## 5. Kết luận & khuyến nghị chốt

- **Kết luận**: **`NO-GO`** (không mở khoá cho `L33–L43`).
- **Các việc bắt buộc để chuyển sang `GO`**:
  1. Viết lại cảnh `practice` cho cả 11 bài theo đúng khuôn mẫu `L18`/`L21`: `practice#0` (chỉ giải thích đúng cú pháp `loi_giai.py` dùng) → `practice#1` (chỉ hiện đề bài + số liệu mới, đặt `pause: 300`, **tuyệt đối không lộ `loi_giai.py`**) → `practice#2` (`Kết quả mong đợi` + lệnh `cham.sh`) → `practice#3` (`Nếu kẹt`).
  2. Bổ sung vào `labs/CS115/L33..L43/de.md`: định dạng stdout chính xác từng dòng, sửa các điểm lệch/sai (`L33` `tabular`/`non_linear_neighbors`, `L36` `GDBT`→`GBDT` + giá trị khởi tạo `y, f`, `L38` `kurtosis`→`độ nhọn` + `-2x` thay `-x`, `L40` dữ liệu khớp `loi_giai.py`, `L42` bỏ/giảng `cân bằng Nash`), và đổi số liệu lab của `L43` (và cân nhắc `L34`/`L37`/`L39`) để không trùng ví dụ trong bài.
  3. Sửa lại `covers:` cho cả 11 bài trỏ đúng cảnh dạy từng mục tiêu.
  4. Bổ sung phân cảnh/bảng **Hai mức quy mô** cho `L33, L36, L37, L38, L39, L40, L42` và tóm tắt quy mô vào `recap` của cả 11 bài (`L33–L43`).
  5. Chạy `render` + `build` + `asr` lại sau khi sửa.
