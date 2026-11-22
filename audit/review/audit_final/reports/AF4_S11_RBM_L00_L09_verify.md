# Báo cáo kiểm định AF4 — RBM L00–L09 (đã đọc 10/10 bài, CHỈ ĐỌC 100%)

**Kết luận tổng thể: NO-GO**

## 1. Bảng tóm tắt toàn bộ chỉ số (`RBM L00–L09`)

| Chỉ số | Kết quả | Ghi chú |
|---|---|---|
| Số bài đã đọc đầy đủ (`YAML + lab + build + SRT + ASR + ≥6 PNG`) | **10 / 10** (`L00–L09`) | Tự kiểm tra, không mở `reports/` |
| Số bài `MUST = 0` | **0 / 10** | Cả 10 bài vướng: lộ `loi_giai.py` & `mong_doi.txt` trước `pause`, `de.md` không tự đứng/lệch `loi_giai.py`, `covers:` sai cảnh, P1 chặt (`practice`) |
| Số bài `P1 = 2` (chuẩn chặt gồm `practice` & `de.md`) | **0 / 10** | 10/10 bài `P1 = 0` (chủ yếu ở `practice`/`de.md` dùng Python & `bash` chưa giảng và bảng cách đọc không phủ hết; đường chính toán rất sạch, chỉ 2 vết nhỏ ở `L00`, `L01`) |
| Số bài `P8 = 2` | **0 / 10** | 10/10 bài `P8 = 1` (lộ full code + output trước `pause: 30`, số lab trùng ví dụ bài, `de.md` thiếu định dạng xuất & L00/L02/L05/L06/L07/L08 thiếu dữ liệu hoặc lệch `loi_giai.py`) |
| Số bài `P9 = 2` (2 mức quy mô/thời gian thân bài & `recap`) | **1 / 10** (`L08`) | `L07` đạt ở thân bài (`error`) nhưng thiếu ở `recap` (chấm 1); `L02`, `L09` = 1; `L00–L01, L03–L06` = 0 |
| Số bài `spec_sha256` khớp `lv.spec_digest` (`build_report.json`) | **10 / 10** | Khớp 100% ở tất cả 10 bài |
| Số bài `L*.srt == say` | **10 / 10** | Khớp 100% từng câu/chữ (sau chuẩn hoá khoảng trắng) |
| Số bài lab chạy thật khớp `mong_doi.txt` | **10 / 10** | 10/10 `loi_giai.py` chạy `rc=0`, stdout khớp từng ký tự `mong_doi.txt` |
| Số `checks:` YAML & `verify_rbm.py` | **293/293** & **92/92 PASS** | Tính lại bằng SymPy/NumPy khớp 100% số trên màn hình và `say` |
| Số phát hiện `SHOULD` | **13** | P9 thiếu/chưa đủ ở 9 bài (`L00–L07, L09`), `screen_code/RBM.yaml` gán sai `kind/lang` cho `practice 1 0` (10 bài), `L04 recap[1]` khẳng định tuyệt đối thiếu điều kiện, `L03` nhãn SVG chạm nhẹ |
| Số phát hiện `INFO` | **5 nhóm** | `"càng "` (2 câu `L06`, `L07` hợp lệ), 0 ký hiệu toán thô trong `say`, 0 câu `say` ngoài 4–38 từ, `layout_RBM.tsv` rỗng (2 byte), `asr_report.md` còn dòng `NOT_VERIFIED bằng tai người` (`chưa xem xét: 0`) |

---

## 2. Đối chiếu hạ tầng & tệp kiểm định (L00–L09)

| Bài | `sha16` YAML | `spec_digest` khớp | `SRT == say` (số câu) | `build_report` `tts_sources` / phút | `asr_report` (cờ / chưa xét / `NOT_VERIFIED`) | Lab chạy `loi_giai.py` == `mong_doi.txt` | `screen_code/RBM.yaml` SHA | `"càng "` / Toán thô trong `say` |
|---|---|---|---|---|---|---|---|---|
| L00 | `3c27b3002fa29fd2` | Khớp | Khớp (110) | `edge:107, edge?:3` / 12.6p | 11 / 0 / 3 | Khớp (`rc=0`) | Khớp 3/3 (nhưng `practice 1` ghi `other/text`) | 0 / 0 |
| L01 | `f016ca3984681f80` | Khớp | Khớp (99) | `edge:96, edge?:3` / 11.6p | 16 / 0 / 4 | Khớp (`rc=0`) | Khớp 3/3 (nt) | 0 / 0 |
| L02 | `cb8a41ab22ea89f4` | Khớp | Khớp (93) | `edge:90, edge?:3` / 10.5p | 26 / 0 / 22 | Khớp (`rc=0`) | Khớp 3/3 (nt) | 0 / 0 |
| L03 | `0e96eee096e7cb99` | Khớp | Khớp (88) | `edge:86, edge?:2` / 9.8p | 11 / 0 / 1 | Khớp (`rc=0`) | Khớp 3/3 (nt) | 0 / 0 |
| L04 | `7bef893cab6e944e` | Khớp | Khớp (77) | `edge:74, edge?:3` / 9.3p | 16 / 0 / 4 | Khớp (`rc=0`) | Khớp 3/3 (nt) | 0 / 0 |
| L05 | `78e081c88d35deb6` | Khớp | Khớp (92) | `edge:89, edge?:3` / 10.3p | 17 / 0 / 7 | Khớp (`rc=0`) | Khớp 3/3 (nt) | 0 / 0 |
| L06 | `41f54028c5c047ef` | Khớp | Khớp (107) | `edge:104, edge?:3` / 12.9p | 19 / 0 / 10 | Khớp (`rc=0`) | Khớp 3/3 (nt) | 1 (`prereq[0]`) / 0 |
| L07 | `d671fd364b899f0b` | Khớp | Khớp (90) | `edge:87, edge?:3` / 10.8p | 3 / 0 / 2 | Khớp (`rc=0`) | Khớp 3/3 (nt) | 1 (`hook[0]`) / 0 |
| L08 | `2f9061007432b49d` | Khớp | Khớp (92) | `edge:89, edge?:3` / 10.9p | 8 / 0 / 3 | Khớp (`rc=0`) | Khớp 3/3 (nt) | 0 / 0 |
| L09 | `d82f8f811113a475` | Khớp | Khớp (116) | `edge:113, edge?:3` / 13.6p | 6 / 0 / 5 | Khớp (`rc=0`) | Khớp 3/3 (nt) | 0 / 0 |

*(Ghi chú: `audit/rbm/sources_L*.md` chỉ có `sources_L17.md`, không có cho `L00–L09`; `audit/layout_RBM.tsv` dài 2 byte / rỗng).*

---

## 3. Danh sách phát hiện chi tiết (MUST / SHOULD / INFO)

### A. MUST (bắt buộc sửa)

1. **L00–L09 — P8 Thực nghiệm lộ toàn bộ mã lời giải (`loi_giai.py`) và kết quả (`mong_doi.txt`) TRƯỚC `pause: 30` (CONFIRMED)**
   - **Bằng chứng (`sha16` & dòng):**
     - `L00` (`3c27b3002fa29fd2`): `practice[1]` L381 (hiện toàn bộ `loi_giai.py`), `practice[2]` L384 (`rotated=(0.0, 1.0) det=1.0`) đứng trước `practice[3]` L394 (`pause: 30`, `"Hãy bấm tạm dừng và tự làm trước."`).
     - `L01` (`f016ca3984681f80`): `practice[1]` L369, `practice[2]` L372 trước `practice[3]` L382 (`pause: 30`).
     - `L02` (`cb8a41ab22ea89f4`): `practice[1]` L353, `practice[2]` L356 trước `practice[3]` L366 (`pause: 30`).
     - `L03` (`0e96eee096e7cb99`): `practice[1]` L300, `practice[2]` L303 trước `practice[3]` L313 (`pause: 30`).
     - `L04` (`7bef893cab6e944e`): `practice[1]` L301, `practice[2]` L304 trước `practice[3]` L314 (`pause: 30`).
     - `L05` (`78e081c88d35deb6`): `practice[1]` L324, `practice[2]` L327 trước `practice[3]` L337 (`pause: 30`).
     - `L06` (`41f54028c5c047ef`): `practice[1]` L393, `practice[2]` L396 trước `practice[3]` L406 (`pause: 30`).
     - `L07` (`d671fd364b899f0b`): `practice[1]` L300, `practice[2]` L303 trước `practice[3]` L313 (`pause: 30`).
     - `L08` (`2f9061007432b49d`): `practice[1]` L338, `practice[2]` L341 trước `practice[3]` L351 (`pause: 30`).
     - `L09` (`d82f8f811113a475`): `practice[1]` L388, `practice[2]` L391 trước `practice[3]` L401 (`pause: 30`).
   - **Đề xuất:** Đưa đề bài + `pause` lên `practice[1]` (hoặc sau bảng đọc), ẩn `loi_giai.py` và đầu ra cho tới **sau** `pause`; tách bước gợi ý / lời giải sau `pause`.

2. **L00–L09 — Lab `de.md` không tự đứng, trùng số ví dụ, và lệch `loi_giai.py` ở L00, L02, L05, L06, L07, L08 (CONFIRMED)**
   - **Cả 10 bài (`L00–L09`):** `labs/RBM/Lxx/de.md` đều **không ghi định dạng chuỗi cần `print`** và độ làm tròn (`rotated=(0.0, 1.0) det=1.0`, `end_effector=(0.866, 1.500)`, `rk4=... err=... ok_lt_1e6=1`, v.v.), nên người học chỉ đọc `de.md` không thể qua `bash labs/cham.sh`. Đồng thời cả 10 lab dùng **y hệt số liệu của ví dụ trong bài** (vi phạm chuẩn lab số khác ví dụ).
   - **Lệch `de.md` vs `loi_giai.py` / thiếu dữ liệu:**
     - `L00` (`labs/RBM/L00/de.md` L3): `"Quay (1, 0) một góc 90°, kiểm tra det R == 1 và ma trận trực giao."` — `loi_giai.py` L1–6 không hề kiểm `R^T R = I`.
     - `L02` (`labs/RBM/L02/de.md` L3): `"Nhân quaternion q * v * q_conj và kiểm tra độ dài đơn vị ||q|| = 1."` — `loi_giai.py` L1–8 không hề kiểm `||q|| = 1`.
     - `L05` (`labs/RBM/L05/de.md` L3): `"Kiểm định cả hai bộ nghiệm góc khớp đều đưa đầu tay về cùng vị trí (0.866, 1.5)."` — thiếu `L1 = L2 = 1` hoàn toàn trong `de.md`, và đây chỉ là chạy động học thuận chứ không giải động học ngược.
     - `L06` (`labs/RBM/L06/de.md` L1–3): `"det J = L1 * L2 * sin(theta2)"` nhưng không cho giá trị `L1 = 1, L2 = 1`.
     - `L07` (`labs/RBM/L07/de.md` L1–3): `"x' = -x"`, `"10 bước h=0.1"` nhưng thiếu hoàn toàn điều kiện đầu `x(0) = 1`.
     - `L08` (`labs/RBM/L08/de.md` L3): `"Chạy 10 bước RK4 h=0.1 từ x=1 và so sai số với Euler (0.0192)."` — `loi_giai.py` L1–7 không hề tính/so với Euler `0.0192`, mà chỉ in `ok_lt_1e6=1`.

3. **L00–L09 — `covers:` trỏ sai cảnh dạy thực tế (CONFIRMED)**
   - Tất cả 10 bài đều gán máy móc `objective 1 -> example, 2 -> check, 3 -> practice`:
     - `L00` (L417–423): `obj 2` ("Kiểm RᵀR = I và det R = 1") trỏ `check` (đúng là `props`); `obj 3` ("Phân biệt quay một điểm với đổi khung toạ độ") trỏ `practice` (đúng là `frames` / `pitfalls`).
     - `L01` (L405–411): `obj 3` ("Giải thích khoá gimbal...") trỏ `practice` (đúng là `gimbal`).
     - `L02` (L389–395): `obj 3` ("Biết q và −q cùng là một phép quay") trỏ `practice` (đúng là `props`).
     - `L03` (L339–345): `obj 2` ("Ghép nhiều biến đổi đúng thứ tự và đổi khung qua chuỗi") trỏ `check` (đúng là `chain`); `obj 3` ("Tính nghịch đảo...") trỏ `practice` (đúng là `chain`).
     - `L04` (L337–343): `obj 3` ("Tính khoảng cách đầu tay tới gốc...") trỏ `practice` (đúng là `reach`).
     - `L05` (L360–366): `obj 2` ("...nhận ra điểm ngoài tầm với") trỏ `check` (thiếu `reach`); `obj 3` ("Biết vì sao dùng atan2 thay cho arctan(y/x)") trỏ `practice` (đúng là `sym` / `pitfalls`; `practice` không dùng `atan2`).
     - `L06` (L429–435): `obj 2` ("Tính det J = L₁L₂ sin θ₂...") trỏ `check` (đúng là `singular`); `obj 3` ("Thấy vận tốc khớp bùng nổ...") trỏ `practice` (đúng là `near`).
     - `L07` (L336–342): `obj 1` ("Đọc phương trình vi phân x′ = f(x)...") trỏ `example` (đúng là `sym`); `obj 3` ("Ước lượng sai số: giảm h một nửa...") trỏ `practice` (đúng là `error`).
     - `L08` (L374–380): `obj 2` ("So sai số với Euler cùng bước và cùng công sức") trỏ `check` (đúng là `compare`); `obj 3` ("Biết bậc cao không cứu được bước quá lớn với hệ cứng") trỏ `practice` (đúng là `stiff`).
     - `L09` (L424–430): `obj 3` ("Phân biệt điều kiện ổn định của hệ liên tục và hệ rời rạc") trỏ `practice` (đúng là `discrete`).

4. **L00–L09 — P1 chặt: Mục chưa giảng (chủ yếu ở `practice`, `de.md`, và 2 điểm nhỏ ở đường chính) (CONFIRMED)**
   *(Ghi chú: Khoá `RBM` không dạy Python hay Bash ở bài nào trong `curriculum/rbm.yaml`; cột cuối ghi rõ bảng cách đọc `practice[0]` có phủ mục đó hay không).*
   - **L00 (`3c27b3002fa29fd2`):**
     - `prereq[0]` L78: `(dấu $^T$)` — dùng ký hiệu chuyển vị `^T` trước khi định nghĩa ở `prereq[3]` L115 (`chuyển vị M^T`) | bảng cách đọc: N/A.
     - `practice[1]` L381: `t = math.pi / 2`, `c, s = round(math.cos(t), 6), round(math.sin(t), 6)`, `c*1 - s*0`, `det:.1f` (`=`, `/`, `,` gán nhiều biến, `*`, `round`, `math.pi/cos/sin`, `:.1f`) | bảng cách đọc: **KHÔNG** (bảng chỉ phủ `import`, `f"{val:.3f}"`, `math.log/exp/sqrt`, `print`).
     - `practice[3]` L387: `bash labs/cham.sh RBM L00 duong_dan/bai_cua_ban.py` | bảng cách đọc: **KHÔNG**.
     - `de.md` L3: `det R == 1` (`==`) | bảng cách đọc: **KHÔNG**.
   - **L01 (`f016ca3984681f80`):**
     - `example[2]` L178: `\Rightarrow` (`introduces: [implies]`, nhưng `say` L185 không giảng/đọc nghĩa dấu `⇒`) | bảng cách đọc: N/A.
     - `practice[1]` L369: `p[0], -p[2], p[1]`, `equal={int(p1 == p2)}` (chỉ số 0-based `p[0]`, `=`, `int(...)`, `==`) | bảng cách đọc: **KHÔNG** (bảng chỉ phủ `lambda`, `f"{val:.3f}"`, `print`).
     - `practice[3]` L375: `bash labs/cham.sh RBM L01 duong_dan/bai_cua_ban.py` | bảng cách đọc: **KHÔNG**.
   - **L02 (`cb8a41ab22ea89f4`):**
     - `practice[1]` L353: `math.pi/4`, `math.cos`, `math.sin`, `w1,x1,y1,z1 = a; w2,x2,y2,z2 = b`, `q[0]`, `round(res[1],2)`, `print(...)` (`;`, chỉ số `[0]`, `round`, `math.cos/sin/pi`, `print(...)` — bảng L02 **thiếu cả dòng `print(...)`**) | bảng cách đọc: **KHÔNG**.
     - `practice[3]` L359: `bash labs/cham.sh RBM L02 duong_dan/bai_cua_ban.py` | bảng cách đọc: **KHÔNG**.
     - `de.md` L3: `q * v * q_conj` (viết tắt `q_conj` chưa từng giảng) | bảng cách đọc: **KHÔNG**.
   - **L03 (`0e96eee096e7cb99`):**
     - `practice[1]` L300: `a = tr2(*rot90(1, 0))` (`=` gán biến, toán tử bung đối số `*`) | bảng cách đọc: **KHÔNG**.
     - `practice[3]` L306: `bash labs/cham.sh RBM L03 duong_dan/bai_cua_ban.py` | bảng cách đọc: **KHÔNG**.
   - **L04 (`7bef893cab6e944e`):**
     - `practice[1]` L301: `t1, t2 = math.radians(30), math.radians(60)`, `math.cos`, `math.sin` | bảng cách đọc: **KHÔNG**.
     - `practice[3]` L307: `bash labs/cham.sh RBM L04 duong_dan/bai_cua_ban.py` | bảng cách đọc: **KHÔNG**.
   - **L05 (`78e081c88d35deb6`):**
     - `practice[1]` L324: `math.radians`, `math.cos`, `math.sin`, `round(...,3)`, `int(p1==p2)`, `print(...)` (bảng L05 **không có `print(...)`**) | bảng cách đọc: **KHÔNG**.
     - `practice[3]` L330: `bash labs/cham.sh RBM L05 duong_dan/bai_cua_ban.py` | bảng cách đọc: **KHÔNG**.
   - **L06 (`41f54028c5c047ef`):**
     - `practice[1]` L393: `math.sin(math.radians(t2))`, `:.1f`, `print(...)` (bảng L06 **không có `print(...)`**) | bảng cách đọc: **KHÔNG**.
     - `practice[3]` L399: `bash labs/cham.sh RBM L06 duong_dan/bai_cua_ban.py` | bảng cách đọc: **KHÔNG**.
   - **L07 (`d671fd364b899f0b`):**
     - `practice[1]` L300: `x = 1.0; h = 0.1`, `for _ in range(10): x += h * (-x)`, `abs(...)`, `:.4f`, `print(...)` (`;`, `_`, `range`, `+=`, `abs`, `print` không có trong bảng L07) | bảng cách đọc: **KHÔNG**.
     - `practice[3]` L306: `bash labs/cham.sh RBM L07 duong_dan/bai_cua_ban.py` | bảng cách đọc: **KHÔNG**.
   - **L08 (`2f9061007432b49d`):**
     - `practice[1]` L338: `;`, `range(10)`, `_`, `+=`, `abs`, `:.6f`, `:.2e`, `1e-6`, `<`, `int(...)`, `print(...)` (bảng L08 **không có `print(...)`**) | bảng cách đọc: **KHÔNG**.
     - `practice[3]` L344: `bash labs/cham.sh RBM L08 duong_dan/bai_cua_ban.py` | bảng cách đọc: **KHÔNG**.
   - **L09 (`d82f8f811113a475`):**
     - `practice[1]` L388: `tr, det = -3.0, 2.0` (`tr` là viết tắt *trace* chưa giảng — bài chỉ gọi "tổng đường chéo"), `disc`, `l1 < 0 and l2 < 0` (`and`), `int(...)`, `:.1f` | bảng cách đọc: **KHÔNG**.
     - `practice[3]` L394: `bash labs/cham.sh RBM L09 duong_dan/bai_cua_ban.py` | bảng cách đọc: **KHÔNG**.
     - `de.md` L3: `lambda^2 + 3*lambda + 2 = 0` (`*`) | bảng cách đọc: **KHÔNG**.

---

### B. SHOULD

1. **L00–L07, L09 — P9 Quy mô / thời gian thiếu hoặc chưa đủ 2 mức trong thân bài & `recap` (CONFIRMED)**
   - `L00, L01, L03, L04, L05, L06`: Không có cảnh phân tích ≥ 2 mức quy mô/thời gian + đánh đổi (P9 = 0). (`L06` có 4 góc gần kỳ dị trong `near`, không phải quy mô hệ/thời gian và `recap` không nêu đánh đổi quy mô).
   - `L02`: Chỉ nhắc bằng lời `"Khi sai số làm tròn tích lũy..."` ở `props[1]` L270, không có số liệu ở ≥ 2 mốc bước cập nhật và không nhắc trong `recap` (P9 = 1).
   - `L07`: Thân bài `error[0]` L202–215 có 3 mức bước (`h = 0.1; 0.05; 0.025` ↔ `10; 20; 40 bước`) + đánh đổi `"tốn gấp 10 lần số bước"`, nhưng `recap` L321–329 không nhắc lại đánh đổi 2 mức quy mô này (P9 = 1 theo chuẩn có ở cả thân bài & `recap`).
   - `L09`: Có diễn biến theo thời gian `t = 0, 1, 2` và `k = 0..3`, thiếu 2 mức quy mô kích thước hệ (`2×2` vs `N×N`) + đánh đổi trong thân bài & `recap` (P9 = 1).
2. **L00–L09 — `audit/review/screen_code/RBM.yaml` gắn nhãn sai cho khối mã Python (`practice 1 0`) (CONFIRMED)**
   - Cả 10 mục `RBM L00..L09 practice 1 0` (vd `audit/review/screen_code/RBM.yaml` L3–8) đều là mã Python thật nhưng lại ghi `kind: other`, `lang: text`, `reason: Đầu ra mong đợi chính xác của lab...`.
3. **L04 — Khẳng định tuyệt đối thiếu điều kiện ở `recap[1]` (CONFIRMED)**
   - `L04` (`7bef893cab6e944e`) L329–330: `"động học thuận luôn có đúng một đáp án"` — chỉ đúng cho tay máy chuỗi hở (như 2 khâu phẳng), không đúng cho cơ cấu song song. Nên thêm `"với tay máy chuỗi hở"`.
4. **L03 — Nhãn SVG hơi sát nhau ở `example[1]` (`00029.png`) (CONFIRMED)**
   - Trong `out/RBM/L03/frames/00029.png`, dòng chữ `"① quay rồi tịnh tiến"` chạm nhẹ phần trên của điểm `(0, 1)`. Vẫn đọc được, nên dịch `y` lên một chút.

---

### C. INFO

1. **`"càng "` trong `say`:** Xuất hiện 2 lần (`L06 prereq[0]` L110 `"Bước nhích càng nhỏ thì tỉ số này càng sát đạo hàm."`; `L07 hook[0]` L44 `"nó quay càng nhanh thì chậm đi càng nhanh"`). Đều là tiếng Việt tự nhiên, ASR nghe đúng (`0` lỗi TTS).
2. **Ký hiệu toán thô trong `say`:** `0/10` bài.
3. **Độ dài câu `say` (4–38 từ):** `0/10` bài vi phạm.
4. **ASR (`asr_report.md`):** `0` thiếu audio, `0` chưa xem xét ở cả 10 bài; tổng số câu vẫn giữ thẻ `NOT_VERIFIED bằng tai người` là `L00: 3, L01: 4, L02: 22, L03: 1, L04: 4, L05: 7, L06: 10, L07: 2, L08: 3, L09: 5` (chủ yếu từ ngoại/chữ cái `quaternion`, `sin`, `theta`, `r`, `p`).
5. **Layout (`audit/layout_RBM.tsv`):** Tệp dài 2 byte (0 cảnh báo tràn khung); toàn bộ các khung hình PNG đã mở sắc nét, KaTeX và phụ đề rõ ràng.

---

## 4. Bảng chấm độ sâu từng bài (`P1–P9`)

| Bài | `sha16` | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng (P1–P7) | Mất gốc | P8 | P9 | Chỗ thiếu chính / Cần biết trước |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | `3c27b3002fa29fd2` | 12.6 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | 1 | 0 | `^T` dùng trước định nghĩa; cú pháp Python & `bash` ở `practice`/`de.md`; lộ giải trước `pause`; thiếu P9 |
| L01 | `f016ca3984681f80` | 11.6 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | 1 | 0 | `⇒` chưa giảng lời đọc; tuple `[0]`, `int`, `==`, `bash` ở `practice`; lộ giải trước `pause`; thiếu P9; `covers[3]` sai |
| L02 | `cb8a41ab22ea89f4` | 10.5 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | 1 | 1 | `;`, `[0]`, `round`, `print`, `bash`, `q_conj` ở `practice`/`de.md`; lộ giải trước `pause`; P9 chỉ nhắc lời; `covers[3]` sai |
| L03 | `0e96eee096e7cb99` | 9.8 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | 1 | 0 | `*rot90(...)`, `=`, `bash` ở `practice`; lộ giải trước `pause`; thiếu P9; `covers[2,3]` sai |
| L04 | `7bef893cab6e944e` | 9.3 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | 1 | 0 | `math.radians/cos/sin`, `bash` ở `practice`; lộ giải trước `pause`; thiếu P9; `covers[3]` sai |
| L05 | `78e081c88d35deb6` | 10.3 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | 1 | 0 | `radians/cos/sin/round/int/print/bash`; `de.md` thiếu `L1=L2=1`; lộ giải trước `pause`; thiếu P9; `covers[2,3]` sai |
| L06 | `41f54028c5c047ef` | 12.9 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | 1 | 0 | `sin/radians/:.1f/print/bash`; `de.md` thiếu `L1=L2=1`; lộ giải trước `pause`; thiếu P9 quy mô/thời gian; `covers[2,3]` sai |
| L07 | `d671fd364b899f0b` | 10.8 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | 1 | 1 | `;`, `_`, `range`, `+=`, `abs`, `print`, `bash`; `de.md` thiếu `x(0)=1`; lộ giải trước `pause`; P9 thiếu ở `recap`; `covers[1,3]` sai |
| L08 | `2f9061007432b49d` | 10.9 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | 1 | 2 | `;`, `range`, `+=`, `:.2e`, `1e-6`, `int`, `print`, `bash`; `de.md` lệch `loi_giai.py`; lộ giải trước `pause`; `covers[2,3]` sai |
| L09 | `d82f8f811113a475` | 13.6 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | GẦN | 1 | 1 | `tr`, `disc`, `and`, `int`, `:.1f`, `bash`; lộ giải trước `pause`; thiếu P9 quy mô hệ; `covers[3]` sai |

---

## 5. Khung hình PNG đã mở xem trực tiếp (67 khung hình, ≥ 6 khung/bài)

- **L00 (8):** `00000.png` (hook), `00038.png` (SVG intuition), `00041.png` (SVG example), `00084.png` (quiz), `00096.png` (practice bảng), `00097.png` (practice code), `00100.png` (practice bash/pause), `00106.png` (recap)
- **L01 (6):** `00000.png` (hook), `00023.png` (SVG intuition), `00027.png` (SVG example), `00076.png` (quiz), `00086.png` (practice code), `00096.png` (recap)
- **L02 (7):** `00000.png` (hook), `00026.png` (SVG intuition), `00065.png` (quiz), `00078.png` (practice bảng), `00079.png` (practice code), `00081.png` (practice bash/pause), `00089.png` (recap)
- **L03 (7):** `00000.png` (hook), `00023.png` (SVG intuition), `00029.png` (SVG example — chạm nhẹ nhãn `① quay rồi tịnh tiến` vào `(0, 1)`), `00062.png` (quiz), `00074.png` (practice code), `00076.png` (practice bash/pause), `00083.png` (recap)
- **L04 (6):** `00000.png` (hook), `00016.png` (SVG intuition), `00027.png` (SVG example), `00055.png` (quiz), `00065.png` (practice code), `00073.png` (recap)
- **L05 (7):** `00000.png` (hook), `00021.png` (SVG intuition), `00044.png` (SVG example), `00051.png` (SVG reach), `00067.png` (quiz), `00078.png` (practice code), `00088.png` (recap)
- **L06 (6):** `00000.png` (hook), `00034.png` (SVG intuition), `00066.png` (SVG singular), `00083.png` (quiz), `00094.png` (practice code), `00103.png` (recap)
- **L07 (6):** `00000.png` (hook), `00028.png` (SVG intuition), `00039.png` (SVG example), `00063.png` (quiz), `00077.png` (practice code), `00086.png` (recap)
- **L08 (7):** `00000.png` (hook), `00022.png` (SVG intuition), `00069.png` (quiz), `00079.png` (practice bảng), `00080.png` (practice code), `00083.png` (practice bash/pause), `00088.png` (recap)
- **L09 (7):** `00000.png` (hook), `00041.png` (SVG intuition), `00072.png` (SVG complex), `00092.png` (quiz), `00103.png` (practice code), `00106.png` (practice bash/pause), `00112.png` (recap)

---

## 6. Người học kẹt ở đâu (nếu mất gốc và chỉ xem `RBM L00–L09`)

- **L00:** Kẹt nhẹ ở `prereq[0]` (`"(dấu $^T$)"` chưa giải thích tới tận `prereq[3]`), sau đó kẹt nặng ở `practice[1]/practice[3]/de.md` (cú pháp Python `=`, `math.pi`, `round`, `:.1f`, lệnh `bash`, `==`, và `de.md` đòi kiểm trực giao nhưng không cho định dạng in).
- **L01:** Kẹt nhẹ ở `example[2]` (ký hiệu `\Rightarrow` trên màn hình không được đọc/giảng), rồi kẹt ở `practice[1]/de.md` (`p[0]`, `int(p1 == p2)`, `bash`, và `de.md` thiếu định dạng xuất).
- **L02:** Kẹt ở `practice[1]/de.md` (`;`, giải nén 4 biến, `q[0]`, `round`, `print`, `q_conj` trong `de.md`, thiếu kiểm `||q||=1` trong `loi_giai.py`, thiếu định dạng xuất).
- **L03:** Kẹt ở `practice[1]` (`tr2(*rot90(1, 0))` dùng toán tử `*` bung tuple chưa giảng) và `de.md` (thiếu định dạng xuất).
- **L04:** Kẹt ở `practice[1]` (`t1, t2 = math.radians(30), math.radians(60)`) và `de.md` (thiếu định dạng xuất `:.3f`).
- **L05:** Kẹt ở `practice[1]` (`round(...,3)`, `int(p1==p2)`, `print`) và `de.md` (thiếu `L1 = L2 = 1`, thiếu hai bộ góc ở thân đề, thiếu định dạng xuất).
- **L06:** Kẹt ở `practice[1]` (`math.sin(math.radians(t2))`, `:.1f`, `print`) và `de.md` (thiếu `L1 = L2 = 1`, thiếu định dạng xuất).
- **L07:** Kẹt ở `practice[1]` (`x = 1.0; h = 0.1`, `for _ in range(10): x += h * (-x)`, `abs`, `:.4f`, `print`) và `de.md` (thiếu `x(0) = 1`, thiếu định dạng xuất).
- **L08:** Kẹt ở `practice[1]` (`;`, `range`, `+=`, `:.2e`, `1e-6`, `<`, `int`, `print`) và `de.md` (đề bảo so với Euler `0.0192` nhưng `loi_giai.py` lại kiểm `ok_lt_1e6=1`, thiếu định dạng xuất).
- **L09:** Kẹt ở `practice[1]` (`tr` không giải thích là tổng đường chéo, `disc`, `and`, `int`, `:.1f`) và `de.md` (thiếu định dạng xuất).
