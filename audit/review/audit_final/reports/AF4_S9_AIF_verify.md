# Báo cáo kiểm định độc lập WP-AF4-5 Stage 9 — Khóa AIF (L00–L14, 15 bài)

**Kết luận: `NO-GO`** (chưa đạt chuẩn xuất xưởng AF2/AF4-5; cần sửa các lỗi `MUST` về lộ bài giải trước khi tự làm, đề lab thiếu/lệch thuật toán, `covers:` sai cảnh dạy thật, và 3 lỗi hiển thị SVG trước khi duyệt lại).

---

## 1. Tổng hợp cổng kỹ thuật & nhất quán dữ liệu (`OBSERVED`)

| Hạng mục | Kết quả | Chi tiết |
|---|---|---|
| `audit/aif/verify_aif.py` | **26/26 PASS** | 0 FAIL (tính lại độc lập toàn bộ số liệu L00–L14) |
| `tools/lv.py lint` (`L00..L14`) | **15/15 PASS** | `0 FAIL, 0 WARN` trên cả 15 bài |
| `tools/lv.py curriculum curriculum/aif.yaml` | **PASS** | `15 bài, 15 đã có đặc tả, 0 lỗi`; `title` và `objectives` khớp 15/15 |
| Biểu thức `checks:` trong 15 YAML | **159/159 PASS** | 0 FAIL |
| `build_report.json` (`spec_sha256 == lv.spec_digest`) | **15/15 khớp** | 100% đồng bộ giữa YAML và bản render/video |
| `out/AIF/L*/asr_report.md` | **15/15 sạch** | `chưa xem xét: 0` ở cả 15/15 bài |
| `out/AIF/L*/L*.srt == say` | **15/15 khớp 100%** | Khớp từng câu (`L00` 77/77 … `L14` 138/138) |
| `audit/layout_AIF.tsv` | **0 dòng lỗi** | Tệp rỗng (2 byte `\r\n`), không có lỗi tràn tự động |
| Chạy thật `labs/AIF/L*/loi_giai.py` vs `mong_doi.txt` | **15/15 khớp stdout** | Chạy trực tiếp bằng `.venv/Scripts/python` ra đúng `mong_doi.txt` 15/15. *(Ghi chú: `lab_gate.py AIF` báo `0 PASS · 15 FAIL` trong phiên này do `C:\Program Files\Git\bin\bash.exe` thoát mã 1 không in stdout/stderr trong sandbox Windows khi gọi `cham.sh`)* |
| `<p class="note"><b>Hai mức quy mô:</b> ...` | **0/15 bài (0%)** | Không bài nào có dòng ghi chú chuẩn này ở thân bài hay `recap` |
| `audit/aif/sources_L14.md` vs `L14` | **Khớp nguồn** | Năm chặng, số liệu DB02/AG16/AGZ17/AZ17/AZ18 và ghi chú `839 ván hoà (tính ra)` khớp nguồn; không nêu tên người trong `say` |

### Kiểm tra toàn bộ `say` và 5 câu chứa `"càng "`
- **Không có từ tiếng Anh/ký hiệu toán thô ngoài sổ phát âm (`lexicon_vi.yaml` / `lexicon_vi.AIF.yaml`)**: mọi từ như `Manhattan`, `Bayes`, `Markov`, `alpha`, `beta`, `gamma`, `logic`, `video`, `robot`, `camera`, `chip`, `nơ-ron`, `IBM` đều có luật đọc hoặc thuộc `foreign_ok`. Không có ký hiệu toán thô (`+ - * / = < > ^`) trong `say`.
- **5 câu chứa `"càng "`**:
  1. `L02 recap#0`: *"…và h càng sát chi phí thật thì càng mở ít nút."* — Không sai nghĩa, nhưng hơi gượng từ ngữ (`"thì mở càng ít nút"` tự nhiên hơn `"càng mở ít nút"`).
  2. `L03 sym#1`: *"Con số này càng gần 1 thì hàm đánh giá càng tốt."* — Rõ nghĩa (trong ngữ cảnh hai hàm đều chấp nhận được).
  3. `L04 prereq#1`: *"Số mũ càng âm thì kết quả càng gần 0."* — Chính xác với $e^{-x}$.
  4. `L12 intuition#0`: *"Giá trị lan ra từ ô cộng 1, càng xa càng nhỏ, và ô sát ô trừ 1 bị kéo xuống."* — Có vế kèm `"và ô sát ô trừ 1 bị kéo xuống"` nên không gây hiểu nhầm ô `(3,2)=0.660 < (1,3)=0.812`, tuy nhiên `"càng xa (theo đường đi an toàn)"` sẽ chặt hơn.
  5. `L14 pitfalls#1`: *"Bài học sai thứ ba là nghĩ càng nhiều dữ liệu càng tốt, cứ lấy mọi thế cờ của mỗi ván."* — Trích dẫn ngộ nhận để bác bỏ ngay sau đó, hoàn toàn rõ nghĩa.

---

## 2. Tỷ lệ `P1`, `P8`, `P9` toàn khóa (`L00..L14`)

| Chỉ số | Kết quả toàn khóa | Giải thích |
|---|---|---|
| **P1 (thuật ngữ/cú pháp tại chỗ)** | **0/15 (0%)** tính cả `practice` & `de.md` *(thân bài chính: 14/15 đạt mức 2, 1/15 mức 1 ở L00)* | Thân bài chính giảng tốt, nhưng **15/15 bài** vướng `practice#0` dùng bảng mẫu chung sai/thiếu token thực tế của `practice#1` (ví dụ `f"{val:.3f}"` có ở cả 15 bài dù 14/15 bài không dùng `:.3f`), chưa giảng `bash labs/cham.sh`, và `de.md` dùng thuật ngữ/viết tắt tiếng Anh chưa chú thích tại chỗ (`BFS/DFS`, `Heuristic`, `8-puzzle`, `CSP`, `MCTS`, `KB`, `MDP`, `p_fwd`, `John/Mary`, `Go`, `mcts_rate`…). |
| **P8 (thực nghiệm tự làm)** | **0/15 (0%)** theo chuẩn chặt `FND L00` *(cấu trúc có `practice` + `labs/`: 15/15 = 100%)* | Cả **15/15 bài** chiếu nguyên mã lời giải `loi_giai.py` ở `practice#1` và đáp án ở `practice#2` **trước** `practice#3` (*"Hãy bấm tạm dừng và tự làm trước"*), làm mất tính tự làm; đồng thời `de.md` không nêu định dạng đầu ra bắt buộc; riêng `L04`, `L13` `loi_giai.py` không cài đúng yêu cầu của `de.md`. |
| **P9 (quy mô/thời gian + hình SVG)** | **Hai mức quy mô: 0/15 (0%)**; Nội dung 2 mức quy mô+đánh đổi: **10/15 = 66,7%** (`P9=2`), **4/15** (`P9=1`), **1/15** (`P9=0`); SVG sạch không đè/chạm khung: **12/15 (80%)** | Không bài nào có `<p class="note"><b>Hai mức quy mô:</b> ...`; 3 bài có lỗi SVG trực quan khi xem PNG (`L04` chữ cắt ngang đường cong; `L08` chữ chạm viền dưới; `L13` chữ chạm hai cạnh khung). |

---

## 3. Chi tiết từng bài (`L00..L14`)

### Các lỗi hệ thống lặp lại ở 15/15 bài (áp dụng chung cho mọi bài dưới đây)
- **[MUST-SYS-1]** `practice#1` chiếu nguyên văn lời giải `loi_giai.py` và `practice#2` chiếu stdout ngay **trước** `practice#3` (*"Hãy bấm tạm dừng và tự làm trước"*). Theo chuẩn `FND L00`, phải giao đề + định dạng kết quả mong đợi + tạm dừng trước, chỉ gợi ý mở `loi_giai.py` sau khi tự thử.
- **[MUST-SYS-2]** `labs/AIF/Lxx/de.md` ở cả 15 bài chỉ mô tả bài toán bằng lời nhưng **không ghi rõ định dạng chuỗi đầu ra** (`key=value ...`) mà `mong_doi.txt` và `cham.sh` đòi hỏi.
- **[SHOULD-SYS-1]** `practice#0` là bảng boilerplate chung, lệch token với `practice#1` và không giảng `bash labs/cham.sh` (`L00..L14`).
- **[SHOULD-SYS-2]** Thiếu `<p class="note"><b>Hai mức quy mô:</b> ...` trong thân bài và `recap` (`0/15` bài).
- **[INFO-SYS-1]** `audit/review/screen_code/AIF.yaml` ghi sai toàn bộ 15 khối `practice 1 0` là `kind: other, lang: text` thay vì `kind: run, lang: python`.

---

### L00 — `Tác tử và môi trường: mô tả bài toán AI`
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `covers:` sai toàn bộ 3 mục tiêu: `obj 1` (PEAS) trỏ `example` (đếm 8 trạng thái), đúng ra là `sym`; `obj 2` (5 tiêu chí môi trường) trỏ `check` (đối xứng 2 ô), đúng ra là `sym` + `quiz`; `obj 3` (tác tử hợp lý = tối đa hóa hiệu năng kỳ vọng) trỏ `practice` (mã 2 ô), đúng ra là `pitfalls` (Lỗi 2).
- **SHOULD**:
  - `practice#0` ghi `f"{val:.3f}"` (không dùng trong `practice#1`), thiếu giải thích `range(4)`, `elif`, `len()`, `+= 1`, chỉ số danh sách `clean[pos]`.
  - `de.md` dùng ký hiệu/tiếng Anh `pos in (0,1)`, `dirty_A,B in (0,1)` chưa chú thích (`P1`).
  - `loi_giai.py` gán cứng `for _ in range(4):` và `elif pos == 0: pos = 1` (chỉ chạy đúng đúng 1 cấu hình đầu `pos=0, [1,1]`, không phải vòng lặp tổng quát theo trạng thái bất kỳ).
  - `sym#0` dùng chữ viết tắt `PEAS` (chỉ chú thích là chữ cái đầu tiếng Anh, chưa dịch từng chữ Performance/Environment/Actuators/Sensors); thiếu `Hai mức quy mô:`; `P9` nội dung = 1 (2 ô vs 3 ô nhưng chưa rõ đánh đổi ở quy mô lớn).
- **P1/P8/P9**: `P1=0` (chặt: `practice#0`+`de.md`; thân bài: 1) · `P8=1` (lộ bài giải, đề thiếu format) · `P9=1`.
- **PNG đã xem**: `out/AIF/L00/frames/00022.png` (SVG sạch), `out/AIF/L00/frames/00065.png` (`practice#0` sạch).

### L01 — `Bài toán tìm kiếm: trạng thái, hành động, tìm theo chiều rộng và chi phí đều`
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `de.md` ghi `Tìm đường ngắn nhất BFS vs độ sâu DFS trên đồ thị trạng thái`, nhưng **cả `BFS` lẫn `DFS` chưa từng được giảng/đặt tên trong bài L01** (`L01` chỉ nói "tìm theo chiều rộng" và "tìm chi phí đều"), và `loi_giai.py` **không hề cài đặt DFS**.
  - `loi_giai.py` in `expanded=5` bằng `len(seen)` — về kỹ thuật, 5 là số nút **đã sinh/đã thăm** (`S, A, B, C, G`), không phải số nút **đã mở** (`expanded`: `S, A, B` = 3 nút trước khi lấy `G`!).
  - `covers:` lệch: `obj 1` (5 thành phần) trỏ `example`, đúng ra là `sym`; `obj 3` (vì sao cần tập đã thăm) trỏ `practice`, đúng ra là `pitfalls` (Lỗi 3) + `practice`.
- **SHOULD**:
  - `practice#0` ghi `f"{val:.3f}"` (không dùng), thiếu giải thích `collections.deque`, `popleft()`, `set` `{'S'}`, `tuple` `('S', 0)`, `len()`, `break`, `while`.
  - `sym#1` nhắc tên `"Dijkstra"` nhưng chưa giải thích đây là tên thuật toán tìm đường ngắn nhất theo chi phí tăng dần (chỉ nói "giống thuật toán đường đi ngắn nhất" trong `say`). Thiếu `Hai mức quy mô:`.
- **P1/P8/P9**: `P1=0` (chặt; thân bài: 2) · `P8=1` · `P9=2` (nội dung có 8-puzzle `181 440` vs 15-puzzle `1,05·10^13`).
- **PNG đã xem**: `out/AIF/L01/frames/00022.png` (SVG sạch), `out/AIF/L01/frames/00062.png` (`practice#0` sạch).

### L02 — `Tìm kiếm có thông tin: A* và hàm đánh giá chấp nhận được`
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `covers:` lệch: `obj 1` (`f = g + h`) trỏ `example`, đúng ra là `sym`; `obj 3` ("hàm đánh giá tốt giảm số nút phải mở") trỏ `practice` (chỉ tính `h1, h2` trên 1 trạng thái, **không chạy A* hay đếm số nút mở**), đúng ra là `example` step 2.
- **SHOULD**:
  - `loi_giai.py` gán cứng hằng số `<= 26` (`admissible=int(h1 <= h2 <= 26)`) thay vì kiểm bằng BFS/A* thật hoặc giải thích rõ trong `de.md`.
  - `de.md` dùng `Heuristic A*`, `8-puzzle`, `admissible` chưa chú thích (`L02` YAML chỉ dùng "hàm đánh giá", "trò xếp 8 ô số", "chấp nhận được").
  - `practice#0` ghi `f"{val:.3f}"`, `max / min` (không dùng), thiếu `enumerate()`, `//`, `%`, `abs()`, `int()`, generator expression `sum(1 for ...)` và `<` (`&lt;=`).
  - `say` `recap#0`: `"càng mở ít nút"` -> nên viết `"mở càng ít nút"`. Thiếu `Hai mức quy mô:`.
- **P1/P8/P9**: `P1=0` (chặt; thân bài: 2) · `P8=1` · `P9=1`.
- **PNG đã xem**: `out/AIF/L02/frames/00027.png` (SVG sạch), `out/AIF/L02/frames/00066.png` (`practice#0` sạch).

### L03 — `Thiết kế hàm đánh giá: nới lỏng bài toán, trội, hệ số nhánh hiệu dụng`
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `covers:` lệch: `obj 1` (nới lỏng luật) trỏ `example`, đúng ra là `sym` + `intuition`; `obj 2` (trội & `max`) trỏ `check`, đúng ra là `sym` + `pitfalls` (Lỗi 2).
- **SHOULD**:
  - `practice#0` ghi `f"{val:.3f}"` (nhưng code dùng `:.4f` và `:.2f`), thiếu `range(50)`, `**` (lũy thừa), `sum(mid**k for k in range(6))`.
  - Thiếu `Hai mức quy mô:`.
- **P1/P8/P9**: `P1=0` (chặt; thân bài: 2) · `P8=1` · `P9=2` (nội dung có `d=5` vs `d=26` + đánh đổi thời gian tính `h`).
- **PNG đã xem**: `out/AIF/L03/frames/00019.png` (SVG sạch), `out/AIF/L03/frames/00058.png` (`practice#0` sạch).

### L04 — `Tìm kiếm cục bộ: leo đồi, khởi động lại ngẫu nhiên, mô phỏng tôi luyện`
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - **Lỗi kỹ thuật & mâu thuẫn đề ↔ lời giải**: `de.md` ghi *"Leo đồi 4-Hậu: đếm cặp xung đột và bước giảm tốt nhất. Cho bàn cờ 4-Hậu `cols=[0, 1, 2, 3]` (mỗi hàng 1 hậu), đếm cặp ăn nhau theo cột/chéo và sau khi dời hàng 0 sang cột 1"*. Nhưng `loi_giai.py` **không hề cài thuật toán leo đồi**, cũng **không dời hàng 0 sang cột 1** (nếu dời sẽ thành `[1, 1, 2, 3]` có xung đột > 0), mà **gán cứng** lời giải đã biết `b1 = [1, 3, 0, 2]` để in `solved_conflicts=0`! Ngoài ra `de.md` quy ước mỗi phần tử là cột của hàng (`mỗi hàng 1 hậu`), trái với YAML `sym#0` (`hàng của hậu ở từng cột`).
  - **Lỗi SVG (`00021.png`)**: Nhãn `"cực tiểu địa phương: h = 1"` **đè cắt ngang** đường cong xanh dương (`<path>`).
  - `covers:` sai: `obj 1` (cực tiểu/cao nguyên) trỏ `example`, đúng ra là `sym` + `intuition`; `obj 3` ("vai trò của nhiệt độ trong mô phỏng tôi luyện") trỏ `practice` (chỉ đếm xung đột 4 hậu, **không có mô phỏng tôi luyện hay nhiệt độ `T`**), đúng ra là `example#4` + `pitfalls#1` + `quiz#0-1`.
- **SHOULD**:
  - `practice#0` ghi `f"{val:.3f}"`, `max / min` (không dùng), thiếu `abs()`, `range()`, `if ... or ...` bên trong `sum(...)`.
  - Thiếu `Hai mức quy mô:`.
- **P1/P8/P9**: `P1=0` (chặt; thân bài: 2) · `P8=0` (lộ bài giải + `loi_giai.py` gán cứng không cài theo đề) · `P9=1` (nội dung có 4-hậu vs 8-hậu, nhưng SVG hỏng `00021.png`).
- **PNG đã xem**: `out/AIF/L04/frames/00021.png` (**LỖI đè chữ**), `out/AIF/L04/frames/00063.png` (`practice#0`), `out/AIF/L04/frames/00064.png` (`practice#1` lộ mã), `out/AIF/L04/frames/00066.png` (`practice#3` hướng dẫn tự làm sau khi đã lộ mã).

### L05 — `Bài toán thoả ràng buộc: quay lui, lan truyền ràng buộc, chọn biến ít giá trị nhất`
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `covers:` sai: `obj 1` (biến, miền, ràng buộc) trỏ `example`, đúng ra là `sym`; `obj 2` (quay lui có kiểm tra tiến) trỏ `check` (chỉ kiểm 6×3=18), đúng ra là `example`; `obj 3` (chọn biến ít giá trị nhất) trỏ `practice` (chỉ vét cạn $3^7$, **không dùng quay lui hay chọn biến ít giá trị nhất**), đúng ra là `example`.
- **SHOULD**:
  - `de.md` dùng `CSP`, `Australia` (bài giảng nói "bản đồ Úc" và không dùng viết tắt `CSP`).
  - `practice#0` ghi `f"{val:.3f}"` (không dùng), thiếu `range()`, `**`, `//`, `%`, `all()`, phép gán cộng `+= 1`.
  - Thiếu `Hai mức quy mô:`.
- **P1/P8/P9**: `P1=0` (chặt; thân bài: 2) · `P8=1` · `P9=2` (7 vùng `2187` vs 100 vùng `3^100`).
- **PNG đã xem**: `out/AIF/L05/frames/00021.png` (SVG đồ thị Úc sạch), `out/AIF/L05/frames/00053.png` (SVG tam giác WA-NT-SA sạch), `out/AIF/L05/frames/00055.png` (`practice#0` sạch).

### L06 — `Trò chơi đối kháng: cực đại–cực tiểu và cắt tỉa alpha–beta`
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `covers:` lệch: `obj 3` ("vì sao thứ tự xét nước đi quyết định lượng cắt tỉa") trỏ `practice` (chỉ duyệt cố định từ trái sang phải trên 1 cây, **không đổi thứ tự nước đi**), đúng ra là `pitfalls#0` + `quiz#2`.
- **SHOULD**:
  - `de.md` dùng `Minimax` (không có trong `say`), `MAX` (không giải thích tại chỗ trong `de.md`).
  - `practice#0` ghi `f"{val:.3f}"`, `sum / len` (không dùng), thiếu `break`, `+= 1`, `-999`/`999` làm cận vô cực giả định.
  - Thiếu `Hai mức quy mô:`.
- **P1/P8/P9**: `P1=0` (chặt; thân bài: 2) · `P8=1` · `P9=2` (cây 9 lá vs cờ vua `b=35, d=4`).
- **PNG đã xem**: `out/AIF/L06/frames/00014.png` (SVG sạch), `out/AIF/L06/frames/00049.png` (`practice#0` sạch).

### L07 — `Tìm kiếm cây Monte Carlo và công thức UCB1`
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `covers:` sai: `obj 1` (4 bước chọn, mở rộng, mô phỏng, lan truyền ngược) trỏ `example` (tính UCB1 và chạy 2 máy đánh bạc, **không chạy 4 bước MCTS**), đúng ra là `sym` + `intuition`; `obj 3` ("chọn nước đi cuối cùng theo số lượt thăm") trỏ `practice` (chỉ tính UCB1 để chọn `B`, không chọn theo số lượt thăm), đúng ra là `pitfalls#0` + `quiz#2`.
- **SHOULD**:
  - `de.md` dùng `MCTS` (chưa từng xuất hiện hay giải thích trong toàn bộ bài `L07` YAML!), `c=sqrt(2)` (không có trong `L07` YAML).
  - `practice#0` ghi `f"{val:.3f}"` (code dùng `:.4f`), thiếu biểu thức điều kiện `'B' if ub > ua else 'A'`.
  - Thiếu `Hai mức quy mô:`.
- **P1/P8/P9**: `P1=0` (chặt; thân bài: 2) · `P8=1` · `P9=1`.
- **PNG đã xem**: `out/AIF/L07/frames/00018.png` (SVG sạch), `out/AIF/L07/frames/00065.png` (`practice#0` sạch).

### L08 — `Lôgic mệnh đề cho tác tử: mô hình, kéo theo lôgic, kiểm mô hình`
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - **Lỗi SVG (`00021.png`)**: Hai nhãn đáy `"KB kéo theo α: nằm trọn bên trong"` và `"không kéo theo: có phần ở ngoài"` (`y="336"` trong `height="340"`) có phần chân chữ (`g, p, q`) **chạm sát viền cam dưới của khung**.
  - `covers:` sai: `obj 1` (phân biệt mô hình, thỏa được, kéo theo) trỏ `example`, đúng ra là `sym` + `pitfalls#1`; `obj 2` (kiểm $KB \models \alpha$ bằng liệt kê mô hình) trỏ `check` (suy luận theo luật, không liệt kê), đúng ra là `example` + `practice`; `obj 3` (lỗi khẳng định hệ quả) trỏ `practice` (chỉ kiểm chuỗi đúng $P \to Q \to R$, **không kiểm lỗi khẳng định hệ quả**), đúng ra là `hook` + `pitfalls#0`.
- **SHOULD**:
  - `de.md` dùng `KB = {P=>Q, Q=>R, P}` và `KB |= R` chưa chú thích tại chỗ (`=>`, `|=` khác ký hiệu KaTeX `\to`, `\models` trong bài).
  - `practice#0` ghi `f"{val:.3f}"`, `sum / len / max / min` (chỉ dùng `len`), thiếu list comprehension có `if`, `all()`, `not ... or ...`, `int()`, `_, _, r` (unpacking bỏ qua biến).
  - Thiếu `Hai mức quy mô:`.
- **P1/P8/P9**: `P1=0` (chặt; thân bài: 2) · `P8=1` · `P9=1` (nội dung có 3 biến vs 20/100 biến, nhưng SVG chạm viền).
- **PNG đã xem**: `out/AIF/L08/frames/00021.png` (**LỖI chạm viền dưới**), `out/AIF/L08/frames/00057.png` (`practice#0` sạch).

### L09 — `Suy diễn tiến, suy diễn lùi và luật Horn`
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `covers:` sai: `obj 2` (chạy suy diễn lùi) trỏ `check` (liệt kê 64 mô hình), đúng ra là `example#3` + `quiz#2`; `obj 3` (so sánh hai chiều & giới hạn luật Horn) trỏ `practice` (chỉ chạy suy diễn tiến), đúng ra là `pitfalls#1-2`.
- **SHOULD**:
  - `practice#0` thiếu `while True:`, `break`, `set` (`{'A', 'B'}`, `<=` kiểm tập con, `.add()`), `.append()`, `",".join(...)`.
  - `de.md` dùng `luật Horn` (bài `say` tránh đọc chữ Horn, chỉ ghi chữ in 1 lần ở `sym#0`), `A,B -> L -> M -> P -> Q`.
  - Thiếu `Hai mức quy mô:`.
- **P1/P8/P9**: `P1=0` (chặt; thân bài: 2) · `P8=1` · `P9=2` (6-7 biến vs 1000 biến + đánh đổi tiến/lùi/Horn).
- **PNG đã xem**: `out/AIF/L09/frames/00016.png` (SVG sạch), `out/AIF/L09/frames/00054.png` (`practice#0` sạch).

### L10 — `Lập kế hoạch: biểu diễn hành động bằng điều kiện và hiệu ứng`
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `covers:` sai: `obj 1` (biểu diễn tiền điều kiện, thêm, xóa) trỏ `example`, đúng ra là `sym`; `obj 2` (tìm kế hoạch bằng tìm kiếm) trỏ `check` (chỉ chứng minh cận dưới 3 bước), đúng ra là `example` + `practice`; `obj 3` (đạt từng mục tiêu con riêng lẻ thất bại) trỏ `practice` (chỉ tìm đường ngắn nhất đảo chồng khối), đúng ra là `pitfalls#0` + `quiz#1`.
- **SHOULD**:
  - `de.md` dùng `BFS` (chưa nhắc lại trong L10), `T` (không chú thích `T` là bàn), `A/B/C -> C/B/A`.
  - `practice#0` ghi `f"{val:.3f}"` (không dùng), code `practice#1` dùng cú pháp Python nâng cao rất nặng cho người mới (`dict()`, `tuple(sorted(s.items()))`, `deque`, `popleft()`, `set(c) - set(c.values()) | {'T'}`, `dict(c, **{b: dst})`, `**` unpacking) nhưng không giải thích chữ nào trong `practice#0`!
  - Thiếu `Hai mức quy mô:` và toàn bộ bài chỉ có quy mô 3 khối (`P9=0`).
- **P1/P8/P9**: `P1=0` (chặt; thân bài: 2) · `P8=1` · `P9=0`.
- **PNG đã xem**: `out/AIF/L10/frames/00017.png` (SVG sạch), `out/AIF/L10/frames/00057.png` (`practice#0` sạch).

### L11 — `Mạng Bayes: phân rã phân phối đồng thời và suy diễn`
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `covers:` sai: `obj 3` ("hiện tượng giải thích loại trừ") trỏ `practice` (chỉ tính `P(B|J,M)`, không tính `P(B|A)` vs `P(B|A,E)`), đúng ra là `pitfalls#1`.
- **SHOULD**:
  - `de.md` dùng `P(Trom | John, Mary)`, `P(B|J,M)`, `P(E)`, `A`, `chuẩn Russell-Norvig`: tên `John, Mary` và `Russell-Norvig` **không có trong `show`/`say` của L11** (L11 chủ động dùng `hàng xóm 1`, `hàng xóm 2`), và `de.md` không chép bảng `A, J, M` đầy đủ nên không tự đứng được.
  - `practice#0` ghi `f"{val:.3f}"` (code dùng `:.4f`), thiếu `dict` tra cứu tuple `(1,1):.95`, toán tử 3 ngôi `p_b if b else 1-p_b`, `+=`.
  - Thiếu `Hai mức quy mô:`.
- **P1/P8/P9**: `P1=0` (chặt; thân bài: 2) · `P8=1` · `P9=2` (5 nút 10 vs 31 số, 6 nút 12 vs 63 số, `n` biến ẩn `2^n`).
- **PNG đã xem**: `out/AIF/L11/frames/00024.png` (SVG sạch), `out/AIF/L11/frames/00073.png` (`practice#0` sạch).

### L12 — `Lập kế hoạch khi bất định: lặp giá trị và lặp chính sách`
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `covers:` sai: `obj 1` (phương trình Bellman) trỏ `example`, đúng ra là `sym` + `check`; `obj 2` (chạy lặp giá trị & đọc chính sách) trỏ `check` (chỉ kiểm điểm bất động), đúng ra là `example` + `practice`; `obj 3` ("chính sách đổi theo thưởng mỗi bước") trỏ `practice` (cố định `r=-0.04`), đúng ra là `pitfalls#0`.
- **SHOULD**:
  - **Lệch số vòng lặp `de.md` ↔ `loi_giai.py`**: `de.md` yêu cầu `"Chạy 20 vòng lặp giá trị"`, nhưng `loi_giai.py` chạy `for _ in range(30):` (dù kiểm tra bằng Python cho thấy cả 20 lẫn 30 vòng đều hội tụ về `U0=0.900, U1=0.950`), và `u[0]` trong `loi_giai.py` gán cứng hướng đi phải không dùng `max`.
  - `de.md` dùng `MDP`, `p_fwd`, `r`, `gamma` (MDP không dùng viết tắt này trong L12 YAML; `p_fwd`, `r` chưa giải thích; mô hình 3 ô chuỗi thẳng chưa mô tả tường chắn/trượt đứng yên 0,2 là gì).
  - `practice#0` ghi `sum / len / min` (không dùng), thiếu `range(30)`, gán chỉ số `u[1] = ...`.
  - Thiếu `Hai mức quy mô:`.
- **P1/P8/P9**: `P1=0` (chặt; thân bài: 2) · `P8=1` · `P9=1`.
- **PNG đã xem**: `out/AIF/L12/frames/00019.png` (SVG sạch), `out/AIF/L12/frames/00064.png` (`practice#0` sạch).

### L13 — `Tổng hợp: khi nào tìm kiếm, khi nào suy luận, khi nào học`
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - **Mâu thuẫn `de.md` ↔ `loi_giai.py`**: `de.md` yêu cầu *"Tính tỉ lệ giảm nút khi cắt từ độ sâu 80 xuống độ sâu 4 với hệ số nhánh b=35"*, nhưng `loi_giai.py` **không hề tính tỉ lệ giảm nút**, chỉ tính `log10(35)*80` và `35**4` (`log10_tree=123.5 depth4_nodes=1500625`).
  - **Lỗi SVG (`00018.png`)**: Chữ `"đường → 1–3, cấu hình → 4–5"` **chạm sát hai cạnh trái/phải** của hộp màu xanh lục (`width="320"`).
  - `covers:` sai: `obj 1` (chọn cách tiếp cận) trỏ `example`, đúng ra là `sym` + `intuition` + `quiz`; `obj 2` (vì sao cần hàm đánh giá học được) trỏ `check` (chỉ đếm chữ số `35^80`), đúng ra là `example#3`; `obj 3` (nối AI cổ điển với học máy) trỏ `practice` (chỉ tính `80*log10(35)` và `35**4`), đúng ra là `example#3` + `recap#1`.
- **SHOULD**:
  - `practice#0` ghi `f"{val:.3f}"` (code dùng `:.1f`), `exp / sqrt` (không dùng, code dùng `math.log10` và `**`).
  - Thiếu `Hai mức quy mô:`.
- **P1/P8/P9**: `P1=0` (chặt; thân bài: 2) · `P8=0` (lộ bài giải + `loi_giai.py` không tính đúng yêu cầu `de.md`) · `P9=1` (nội dung có 2 quy mô, nhưng SVG chạm khung `00018.png`).
- **PNG đã xem**: `out/AIF/L13/frames/00018.png` (**LỖI chữ chạm cạnh hộp**), `out/AIF/L13/frames/00054.png` (`practice#0` sạch).

### L14 — `Tình huống chuyên gia theo dòng thời gian: máy chơi cờ từ Deep Blue tới AlphaZero`
- **MUST**:
  - `MUST-SYS-1`, `MUST-SYS-2`.
  - `covers:` lệch: `obj 1` (5 chặng 1988–2018) chỉ trỏ `stage1` (1/5 chặng); `obj 2` (tốc độ lý thuyết, hiệu suất, cờ vây, mô phỏng/giây, ván hòa) chỉ trỏ `stage2`; `obj 3` (chọn tìm kiếm viết tay vs tự chơi kèm điều kiện đổi) trỏ `practice` (chỉ tính 3 con số, không có quyết định/điều kiện đổi), đúng ra là `quiz#2`.
- **SHOULD**:
  - `de.md` dùng `Deep Blue`, `AlphaZero`, `Go`, `mcts_rate` (`MCTS` không có trong L14; `Deep Blue`, `AlphaZero` chỉ hiện trên màn hình chứ không giảng viết tắt trong `de.md`).
  - `practice#0` ghi `f"{val:.3f}"` (code dùng `:.1f` và `:.0f`), thiếu dấu gạch dưới trong số lớn `2_500_000`.
  - Thiếu `<p class="note"><b>Hai mức quy mô:</b> ...` (dù bài hành trình có 5 chặng quy mô/thời gian rất rõ).
- **P1/P8/P9**: `P1=0` (chặt; thân bài: 2) · `P8=1` · `P9=2` (5 chặng thời gian + đánh đổi ở `quiz#2`).
- **PNG đã xem**: `out/AIF/L14/frames/00018.png` (SVG trục thời gian sạch), `out/AIF/L14/frames/00023.png` (SVG hai cây sạch), `out/AIF/L14/frames/00121.png` (`practice#0` sạch).

---

## 4. Danh sách đầy đủ 34 PNG đã xem

- `out/AIF/L00/frames/00022.png`, `00065.png`
- `out/AIF/L01/frames/00022.png`, `00062.png`
- `out/AIF/L02/frames/00027.png`, `00066.png`
- `out/AIF/L03/frames/00019.png`, `00058.png`
- `out/AIF/L04/frames/00021.png`, `00063.png`, `00064.png`, `00066.png`
- `out/AIF/L05/frames/00021.png`, `00053.png`, `00055.png`
- `out/AIF/L06/frames/00014.png`, `00049.png`
- `out/AIF/L07/frames/00018.png`, `00065.png`
- `out/AIF/L08/frames/00021.png`, `00057.png`
- `out/AIF/L09/frames/00016.png`, `00054.png`
- `out/AIF/L10/frames/00017.png`, `00057.png`
- `out/AIF/L11/frames/00024.png`, `00073.png`
- `out/AIF/L12/frames/00019.png`, `00064.png`
- `out/AIF/L13/frames/00018.png`, `00054.png`
- `out/AIF/L14/frames/00018.png`, `00023.png`, `00121.png`

---

## 5. Kết luận & Khuyến nghị hành động (`NO-GO`)

1. **Sửa `practice` (15/15 bài)**: Bỏ bước chiếu trước mã `loi_giai.py` trước khi tạm dừng; cập nhật `practice#0` thành bảng giải thích đúng **từng ký hiệu/hàm Python thật sự có trong bài** + giải thích lệnh `bash labs/cham.sh ...`.
2. **Sửa `labs/AIF/L*/de.md` & `loi_giai.py`**:
   - Ghi rõ định dạng stdout mong đợi trong cả 15 `de.md`, chú thích mọi từ tiếng Anh/viết tắt (`BFS/DFS`, `MCTS`, `CSP`, `MDP`, …).
   - **L04**: Viết lại `loi_giai.py` cài leo đồi thật (hoặc sửa `de.md` khớp hoàn toàn với phép dời cụ thể & quy ước cột/hàng của bài học, không gán cứng `b1 = [1, 3, 0, 2]`).
   - **L13**: Cài tính thật tỉ lệ giảm nút đúng như `de.md` hỏi (hoặc sửa `de.md` khớp với `log10_tree` & `depth4_nodes`).
   - **L12**: Thống nhất `20` vs `30` vòng lặp và dùng `max` cho cả `u[0]`.
   - **L01**: Bỏ `vs độ sâu DFS` hoặc cài thật, và sửa `expanded` thành `visited`/`generated` (hoặc đếm đúng số nút mở = 3).
3. **Sửa `covers:` (15/15 bài)**: Ánh xạ lại `objective 1/2/3` về đúng cảnh dạy thật trong từng bài thay vì mẫu `[example, check, practice]` tự động.
4. **Sửa 3 SVG (`L04`, `L08`, `L13`) & bổ sung `Hai mức quy mô:` (`L00..L14`)**: Dịch nhãn `cực tiểu địa phương: h = 1` ở `L04`, tăng `viewBox height` lên `360` ở `L08`, nới rộng hộp `width="370"` hoặc thu gọn chữ ở `L13`; thêm `<p class="note"><b>Hai mức quy mô:</b> ...` ở cả 15 bài, rồi dựng lại và kiểm tra `spec_sha256` / `asr` / `screen_code`.