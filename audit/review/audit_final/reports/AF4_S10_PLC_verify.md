# Báo cáo kiểm định độc lập Stage 10 — Khóa `PLC` (`L00–L13`, 14 bài)

**Kết luận tổng thể: `NO-GO`**

Lý do chính:
1. Có lỗi **MUST** về kiến thức ở `labs/PLC/L00/de.md` (gọi pha cú pháp là "pha 1" và pha ngữ nghĩa là "pha 2", mâu thuẫn trực tiếp với bảng 5 pha của bài `L00`).
2. **0/14 bài đạt `P1 = 2`** theo chuẩn P1 chặt (11 bài `P1 = 0`, 3 bài `P1 = 1`) do đưa cú pháp Python/C/Java (`def`, `return`, `while ... in (...)`, list comprehension, `@lru_cache`, `for ... in range(...)`, `with`, `try ... finally`, `void`, `tuple`, `(4,)`, `re.findall`, `r'...'`, `round`, `set`, `AST`, `BFS`, `VM`...) vào thân bài, `practice#1`, hoặc `de.md` mà chưa giảng tại chỗ hoặc chưa có trong bài trước cùng khóa.
3. **0/14 bài đạt `P8 = 2`**: `L01`, `L08`, `L13` **lộ toàn bộ `loi_giai.py` và `mong_doi.txt` ngay trước `pause`**; **14/14 tệp `labs/PLC/L*/de.md` thiếu đặc tả định dạng `stdout` và không tự đứng được**; **12/14 lab trùng số liệu/biểu thức ví dụ trong bài**; nhiều lab (`L00, L04, L05, L06, L08, L11`) lệch logic giữa mô tả trong `de.md` và cài đặt trong `loi_giai.py`.
4. **0/14 bài đạt `P9 = 2`**: **14/14 bài thiếu `<p class="note"><b>Hai mức quy mô:</b> ...`** trong `recap` và không có SVG 2 mức quy mô (chỉ `L02` có bảng 3 mức quy mô `10/100/1000` trong `pitfalls#3`; `L07, L08, L12, L13` có đề cập ý quy mô trong thân bài).
5. **14/14 bài có `covers:` lệch cảnh dạy thật** (tự động gắn `obj1->example, obj2->check, obj3->practice` cho `L00..L12` và `stage1, stage2, practice` cho `L13`).

---

## 1. Bảng tóm tắt số lượng bài đạt chuẩn (`PLC` — 14 bài `L00..L13`)

| Hạng mục kiểm định | Kết quả | Ghi chú chi tiết |
|---|---:|---|
| Số bài `MUST = 0` | **13 / 14** | `L00` dính 1 lỗi `MUST` ở `labs/PLC/L00/de.md` (lệch thứ tự pha so với bài giảng). 13 bài còn lại `MUST = 0`. |
| Số bài `P1 = 2` (chuẩn chặt) | **0 / 14** | `P1 = 1`: 3 bài (`L06, L10, L13`); `P1 = 0`: 11 bài (`L00..L05, L07..L09, L11..L12`). |
| Số bài `P8 = 2` | **0 / 14** | `P8 = 1`: 11 bài (`L00, L02..L07, L09..L12`); `P8 = 0`: 3 bài (`L01, L08, L13` do lộ lời giải trước `pause`). |
| Số bài `P9 = 2` | **0 / 14** | `P9 = 1`: 5 bài (`L02, L07, L08, L12, L13`); `P9 = 0`: 9 bài. 14/14 bài thiếu `Hai mức quy mô:` ở `recap`. |
| Số bài `spec_sha256` & `tts_sha256` khớp | **14 / 14** | Khớp 100% `lv.spec_digest(spec)` và `lv.tts_digest(frames)` ở cả 14 `build_report.json`. |
| Số bài `SRT == say` khớp | **14 / 14** | Khớp 100% ở cả 14 bài `out/PLC/L*/L*.srt`. |
| Số bài `asr_report.md` sạch | **14 / 14** | 14/14 bài có `thiếu audio: 0` và `chưa xem xét: 0`. |
| Số bài `lv.py lint` & `curriculum` đạt | **14 / 14** | 0 FAIL, 0 WARN trên cả 14 bài; `lv.py curriculum`: 14/14 bài, 0 lỗi. |
| Số bài `verify_plc.py` & `checks:` | **14 / 14** | `verify_plc.py`: **72/72 PASS** (`L09d` C++ và `L11e` C ghi `NOT_VERIFIED` do máy không có trình biên dịch C/C++); toàn bộ `checks:` trong 14 YAML đều PASS khi chạy `lint`. |
| Số bài `lab` chạy khớp `mong_doi.txt` | **14 / 14** | Chạy trực tiếp `.venv/Scripts/python.exe` trên 14 `loi_giai.py`: 14/14 exit 0 và `stdout == mong_doi.txt`. |
| `audit/layout_PLC.tsv` | **0 lỗi** | Tệp 2 byte (`\r\n`, trống = không có lỗi bố cục). |
| Số vấn đề `SHOULD` | **29 phát hiện** | Rải trên `covers:` (14 bài), `de.md` thiếu stdout & trùng ví dụ (14 bài), logic đề–code (6 bài), `L09` đọc `C++`, `L02` `factor` vs `atom`, bảng đọc `L01/L08/L13`, `L13` `objectives` khác dấu ngoặc. |

---

## 2. Chi tiết phát hiện theo mức `MUST` / `SHOULD` / `INFO`

### A. Mức `MUST` (chặn phát hành)
1. **`L00` — `labs/PLC/L00/de.md` dòng 3**:
   - **Trích**: `"Kiểm định chuỗi tokens mô phỏng trình phân tích: phát hiện ngoặc không cân bằng ở pha 1 và biến chưa gán ở pha 2."`
   - **Vì sao sai**: Bài `L00` (`sym#0`, `intuition#0`, `recap#0`) giảng 5 pha theo thứ tự: **pha 1 = từ vựng**, **pha 2 = cú pháp**, **pha 3 = ngữ nghĩa**, pha 4 = tối ưu, pha 5 = sinh mã. Gọi lỗi ngoặc (cú pháp) là **"pha 1"** và biến chưa gán (ngữ nghĩa) là **"pha 2"** sai kiến thức cốt lõi của chính bài L00 (Mục tiêu 1).
   - **Đề xuất sửa**: Sửa thành `"...ở pha cú pháp (pha 2) và biến chưa gán ở pha ngữ nghĩa (pha 3)"` đồng thời chỉnh cài đặt cho đúng mô hình pha.

2. **`L01`, `L08`, `L13` — `practice` lộ lời giải trước `pause` (vi phạm quy tắc P8 / kiểm tự làm)**:
   - **`L01` (`practice#1`, `practice#2` trước `pause` ở `practice#3`)**: Chiếu nguyên mã `loi_giai.py` (`import re; toks = re.findall(...); print(...)`) và nguyên `mong_doi.txt` (`count=5 toks=['x1', '=', '42', '+', 'y']`) trước khi yêu cầu người học bấm tạm dừng tự làm.
   - **`L08` (`practice#1`, `practice#2` trước `pause` ở `practice#3`)**: Chiếu nguyên mã `loi_giai.py` (8 dòng duyệt đồ thị) và nguyên `mong_doi.txt` (`alive=['A', 'B', 'C'] reclaimed_cycle=['D', 'E']`) trước `pause: 30`.
   - **`L13` (`practice#1`, `practice#2` trước `pause` ở `practice#3`)**: Chiếu nguyên mã `loi_giai.py` (`drop_pct = ...; est_tot = ...; print(...)`) và nguyên `mong_doi.txt` (`mem_vuln_drop=61.9% est_total=243`) trước `pause: 30`.
   - *(Ghi chú phân loại: nếu xét riêng phần kiến thức chuyên môn, `L01..L13` không sai kiến thức; nhưng nếu xét chuẩn nghiệm thu P8 không lộ lời giải trước `pause`, đây là lỗi chặn ở `L01, L08, L13`.)*

### B. Mức `SHOULD`
1. **14/14 bài — `covers:` trỏ sai cảnh dạy thật**:
   - `L00..L12` đều gắn cứng `objective 1 -> example`, `objective 2 -> check`, `objective 3 -> practice`, bất chấp mục tiêu thật dạy ở cảnh nào:
     - `L00`: `obj1` (thứ tự 5 pha) trỏ `example` (lẽ ra `sym`/`intuition`); `obj3` (biên dịch vs thông dịch là cách cài đặt) trỏ `practice` (lẽ ra `impl`).
     - `L01`: `obj1` (regex) trỏ `example` (lẽ ra `prereq`/`sym`); `obj2` (khớp dài nhất/ưu tiên) trỏ `check` (lẽ ra `rules`/`example`); `obj3` (ôtômat) trỏ `practice` (lẽ ra `intuition`/`automaton`).
     - `L02`: `obj1` (văn phạm 3 tầng) trỏ `example` (lẽ ra `sym`); `obj2` (mỗi luật một hàm) trỏ `check` (lẽ ra `code`); `obj3` (tránh đệ quy trái) trỏ `practice` (lẽ ra `pitfalls#0`).
     - `L03`: `obj1` (cây đầy đủ vs AST) trỏ `example` (lẽ ra `sym`); `obj3` (đánh giá duyệt sau) trỏ `practice` (lẽ ra `example`).
     - `L04`: `obj3` (chọn biến không chụp giá trị) trỏ `practice` (lẽ ra `late`).
     - `L05`: `obj2` (mạnh/yếu) trỏ `check` (lẽ ra `sym`/`example`); `obj3` (hai trục độc lập) trỏ `practice` (lẽ ra `intuition`/`example#3`).
     - `L06`: `obj2` (hợp nhất) trỏ `check` (lẽ ra `unify`/`example`); `obj3` (suy luận vẫn là kiểm tĩnh) trỏ `practice` (lẽ ra `pitfalls#0`).
     - `L07`: `obj1` (hàm là giá trị) trỏ `example` (lẽ ra `prereq`/`sym`); `obj3` (lỗi vòng lặp) trỏ `practice` (lẽ ra `pitfalls#0`).
     - `L08`: `obj1` (ngăn xếp vs đống) trỏ `example` (lẽ ra `sym`/`intuition`); `obj3` (vì sao GC vẫn rò) trỏ `practice` (lẽ ra `pitfalls#0,#3`).
     - `L10`: `obj2` (chạy tay) trỏ `check` (lẽ ra `example`); `obj3` (thứ tự toán hạng trừ/chia) trỏ `practice` (lẽ ra `sym`/`pitfalls#0`/`quiz`, vì `practice` chỉ chạy `1+2*3` không có trừ/chia).
     - `L11`: `obj1` (gấp hằng số và giới hạn) trỏ `example` (lẽ ra `sym`/`limit`); `obj2` (mã chết + bất biến vòng lặp) trỏ `check` (lẽ ra `example`); `obj3` (giữ hành vi) trỏ `practice` (lẽ ra `intuition`/`limit`/`pitfalls#0-#1`).
     - `L12`: `obj2` (dùng chung phần cũ) trỏ `check` (lẽ ra `sharing`); `obj3` (an toàn đồng thời) trỏ `practice` (lẽ ra `hook`/`sym`/`sharing`).
     - `L13`: `obj1` (5 chặng 2019→2025) chỉ trỏ `stage1`; `obj2` (tính lại tỉ lệ/mật độ/giảm theo tuổi) chỉ trỏ `stage2`; `obj3` (chọn cách hợp quy mô + điều kiện đổi) trỏ `practice` (lẽ ra `quiz`).
   - *(Chỉ `L09` có `covers` tạm chạm được cả 3 mục tiêu, dù `obj1` chủ yếu ở `sym`.)*

2. **14/14 lab (`labs/PLC/L00..L13/de.md`) thiếu đặc tả `stdout` và không tự đứng được**:
   - Không một tệp `de.md` nào nêu định dạng dòng `stdout` mong đợi (`syn_err=1 sem_err=1`, `count=5 toks=...`, `p1=7 p2=9`, ...). Người học chỉ đọc `de.md` không thể viết đúng chuỗi in ra để khớp `mong_doi.txt`.
   - **12/14 lab** dùng trùng đúng dữ liệu/ví dụ trong bài giảng: `L01` (`'x1 = 42+y'`), `L02` (`'1+2*3'`, `'(1+2)*3'`), `L03` (`8 - 3 - 2`), `L04` (`x=1/x=2`), `L05` (`int + str`), `L06` (`f(x) = x + x`), `L07` (`make_counter()`, `c1` 3 lần, `c2` 1 lần), `L08` (`{A:[B], B:[C], C:[], D:[E], E:[D]}`), `L09` (`bad(1)`, `bad(2)`), `L10` (`1+2*3`), `L11` (`2 * 3 + x -> 6 + x`), `L13` (`223 -> 85`, `85 / 0.35 ≈ 243`). Chỉ `L00` và `L12` đổi sang ví dụ khác thân bài.

3. **Logic đề ↔ code (`de.md` vs `loi_giai.py`) lệch ở 6 bài**:
   - `L00`: Đề nói "Kiểm định chuỗi tokens", code chỉ đếm `s.count('(') == s.count(')')` trên chuỗi thô `'(1+2'` (`')('` cũng qua).
   - `L02`: Đề gọi hàm tầng 3 là `factor`, nhưng bài giảng `L02` toàn bộ gọi là `atom`.
   - `L04`: Đề nói "bộ thông dịch nhỏ so sánh lookup tĩnh vs ngăn xếp gọi động", nhưng `loi_giai.py` gán cứng `return x_global` và `env_stack[-1]['x']` chứ không tra chuỗi môi trường.
   - `L05`: Đề nói "duyệt AST bắt lỗi `int + str`", nhưng `loi_giai.py` chỉ là `op == '+' and lhs_t == rhs_t` (không duyệt AST, phép `-` trả `False`).
   - `L06`: Đề nói "hợp nhất biến kiểu từ ràng buộc", nhưng `loi_giai.py` khai báo `constraints` rồi không đọc mà gán cứng `env = {'param_x': 'int'}`.
   - `L08`: Đề yêu cầu "Quét BFS", nhưng `loi_giai.py` (và `practice#1`) dùng `u = q.pop()` — đó là **DFS**, không phải BFS (`pop(0)` / `deque.popleft()`).
   - `L11`: `fold()` trong `loi_giai.py` chỉ rút gọn phép `*`, không xử lý `+`, `-`, `/`.

4. **Kiểm `say` và TTS (`L09`, `L12`, `L13`, `L02`)**:
   - **`L09` (`prereq#0`, `sym#0`, `example#4`)**: `say` viết thô `C++` (có dấu `+`), khiến TTS đọc rơi `++` thành `"C"` (`xe`) — bằng chứng tại `out/PLC/L09/asr_report.md` dòng 20 (`"như dấu và trong C++."` → `"như giấu và trông xe."`) và dòng 28 (`"Trong C++ với tham chiếu"` → `"Trong xe với tham chiếu"`). Trong khi `L13` viết `"C cộng cộng"` nên không bị lỗi.
   - **`L12 recap#2`, `L13` (10 step)**: `say` chứa ký tự `%` thô (`76%`, `70%`...); `tools/vi_text.py` đã đổi `%` → `" phần trăm "` trước TTS nên ASR không lỗi, nhưng nên chuẩn hóa chữ trong `say` cho nhất quán.
   - **Từ `"càng "`**: xuất hiện ở `L02 recap#0` (`"tầng càng sâu thì gắn càng chặt"`) và `L13 decay#0` (`"Mã càng cũ càng ít lỗi"`), `stage1#0` (`"Mã càng nhiều, vấn đề càng tệ hơn"`). Kiểm tra ngữ nghĩa: cả 3 câu đều chính xác về mặt logic/toán học.

5. **Bảng "viết trong mã / đọc và hiểu là" ở `practice#0` (`L01`, `L08`, `L13`)**:
   - `L01 practice#0` giải thích `f"{val:.3f}"`, `sum / len / max / min` nhưng `practice#1` không dùng `.3f` hay `sum/max/min`, trong khi lại dùng `re.findall`, `r'...'`, `[=+*/-]` chưa được bảng phủ.
   - `L08 practice#0` giải thích `f"{val:.3f}"` (không dùng ở `practice#1`), không phủ `{'A'}`, `set(adj) - alive`, `while q:`, `.pop()`, `.add()`, `.append()`, `sorted()`.
   - `L13 practice#0` giải thích `f"{val:.3f}"` (code dùng `:.1f`), không phủ `round(...)`.

6. **Khác biệt nhỏ `curriculum/plc.yaml` vs `lessons/plc/L*.yaml`**:
   - `title`: `curriculum` bỏ tiền tố `Bài N — ` (bình thường theo mẫu).
   - `L13 objectives`: `curriculum` viết `(2019 → 2025)`, `L13.yaml` viết `từ 2019 tới 2025` (nội dung trùng khớp).

### C. Mức `INFO`
- **Kiểm nguồn `L13` (`audit/plc/sources_L13.md`)**: Toàn bộ số liệu và mốc 2019–2025 trong `L13` (`70%`, `5/130 -> 96.2%`, `90%`, `80%`, `<1%`, `7/8` tổ hợp Rule of 2, `1.5 triệu dòng`, `223 -> 85` giảm `61.9%`, `76% -> 35%`, `293 -> 243`, `20/tháng -> 240`, `1500` cận trên, `2` chỗ `unsafe` UWB, `24%`, `2.5 năm`, `3.4x..7.4x`, `e^2 ≈ 7.39`, `4.1 năm`, `<20%`, `5 triệu dòng`, `0.2/MLOC` vs `1000/MLOC` = `5000x`, `4%` = `200 000` dòng, `4x` rollback, `25%` review time) đều khớp 100% với `sources_L13.md` và `verify_plc.py`.
- **`audit/review/screen_code/PLC.yaml`**: Khớp với các khối mã nguồn Python/EBNF/text đã ghim `sha` trong bài; kiểm chứng độc lập `verify_plc.py` đạt 72/72 PASS.

---

## 3. Liệt kê toàn bộ mã PNG đã xem trực tiếp (`44 PNG`, 3–4 khung/bài)

Đã mở đọc trực tiếp bằng `read_file` trong `out/PLC/L*/frames/`:
- **L00**: `00024.png` (SVG dây chuyền 5 trạm), `00067.png` (practice), `00071.png` (recap)
- **L01**: `00027.png` (SVG ôtômat), `00076.png` (practice code — lộ giải), `00082.png` (recap)
- **L02**: `00026.png` (SVG cây lời gọi đệ quy), `00071.png` (practice), `00075.png` (recap)
- **L03**: `00024.png` (SVG duyệt sau cây `8-3-2`), `00066.png` (practice), `00070.png` (recap)
- **L04**: `00019.png` (SVG 3 hộp môi trường tĩnh/động), `00070.png` (practice), `00074.png` (recap)
- **L05**: `00024.png` (SVG bảng 2 trục 4 ô), `00080.png` (practice), `00084.png` (recap)
- **L06**: `00021.png` (SVG dây chuyền 3 khâu hợp nhất), `00060.png` (practice), `00064.png` (recap)
- **L07**: `00017.png` (SVG ngăn xếp/đống bao đóng), `00065.png` (practice), `00069.png` (recap)
- **L08**: `00023.png` (SVG ngăn xếp/đống khung `f`), `00027.png` (SVG vòng `D<->E`), `00073.png` (practice code — lộ giải), `00079.png` (recap)
- **L09**: `00017.png` (SVG 2 nhãn 1 đối tượng), `00068.png` (practice), `00072.png` (recap)
- **L10**: `00022.png` (SVG cây đánh số + ngăn xếp 5 lệnh), `00071.png` (practice), `00075.png` (recap)
- **L11**: `00019.png` (SVG 3 trạm tối ưu), `00064.png` (practice), `00068.png` (recap)
- **L12**: `00023.png` (SVG dữ liệu bất biến qua 3 trạm), `00075.png` (practice), `00079.png` (recap)
- **L13**: `00017.png` (SVG trục thời gian 5 chặng), `00021.png` (SVG biểu đồ cột giảm theo tuổi), `00113.png` (practice code — lộ giải), `00119.png` (recap)

**Đánh giá hiển thị**: Tất cả **44/44 PNG** sắc nét, không đè chữ, không cắt khung, không tràn viền, công thức và SVG đều rõ ràng, dễ đọc.

---

## 4. Chi tiết P1 chặt (liệt kê từng mục chưa giảng + bảng cách đọc có phủ không)

| Bài | Mục chưa giảng (cảnh/step + trích chữ) | Bảng cách đọc có phủ không? | Điểm P1 |
|---|---|---|---:|
| `L00` | (1) `pitfalls#3`: `def xu_ly(n):`, `if n >= 0:`, `return` (cú pháp Python chưa giảng); (2) `quiz#0`: `if (x > 1 { y = 2 }` (dấu `{ }`); (3) `de.md`: `tokens`, `pha 1 / pha 2` (lệch thuật ngữ) | Không có bảng | **0** |
| `L01` | (1) `practice#1`: `re.findall(...)`; (2) `practice#1`: `r'...'` (raw string); (3) `practice#1`: `[=+*/-]` (dấu `-` cuối lớp ký tự); (4) `de.md`: `Lexer` | Có bảng ở `practice#0`, **không** phủ 3 mục trên (`re.findall`, `r'...'`, `[=+*/-]`) | **0** |
| `L02` | (1) `prereq#1`: `def` / `return`; (2) `code#0`: `while peek() in ("+", "-"):`, `;`, `(op, v, term())`; (3) `practice#0` & `de.md`: `Parser`, `factor` (bài dùng `atom`) | Không có bảng | **0** |
| `L03` | (1) `prereq#1`: `def` / `return` (chưa giảng ở L00–L02); (2) `pitfalls#2`: `//` (`phép // của Python`); (3) `check#0` bảng: `2**3**2` (toán tử `**` không giảng trên màn hình) | Không có bảng | **0** |
| `L04` | (1) `hook#0`/`prereq#0`: `# ...` (chú thích `#`); (2) `pitfalls#3`: `round(...)` và `gia(x, thue=0.1)` (tham số mặc định); (3) `practice#0` & `de.md`: `lexical`, `lookup` | Không có bảng | **0** |
| `L05` | (1) `example#1`: `1.0f` (hậu tố `f` kiểu float trong C); (2) `example#1`: `0x3F800000` (tiền tố `0x`); (3) `de.md`: `AST` (chưa từng giới thiệu trong `L03` hay `L05`) | Không có bảng | **0** |
| `L06` | (1) `unify#0`, `example#2`, `check#0`: `bool` (trên màn hình chỉ ghi `bool`, chỉ lời đọc dịch "đúng sai"); (2) `de.md`: `+ : (int, int) -> int` (ký pháp hàm 2 đối chưa dạy) | Không có bảng | **1** |
| `L07` | (1) `hook#0`: `n += 1`, `;`; (2) `sym#0`: `list(map(...))`; (3) `pitfalls#0`: `[lambda: i for i in range(3)]` (list comprehension + `range`) và `lambda i=i: i`; (4) `pitfalls#3`: `c = {}`, `not in`, `c[x]`; (5) `de.md`: `closure` (chỉ có ở `practice#0`, chưa giảng ở thân bài) | Không có bảng | **0** |
| `L08` | (1) `pitfalls#2`: `with`, `try … finally`; (2) `practice#1`: `{'A'}`, `set(adj) - alive`, `while q:`, `.pop()`, `.add()`, `.append()`, `sorted()`; (3) `de.md`: `BFS`, `mark-sweep` | Có bảng ở `practice#0`, **không** phủ các mục trên | **0** |
| `L09` | (1) `sym#0`: `void` (`void f(int x)`); (2) `example#4`: `a, b = b, a` (hoán đổi bộ); (3) `pitfalls#3`: `dict(a)` | Không có bảng | **0** |
| `L10` | (1) `recap#0`: `a ∘ b` (ký hiệu `∘` chưa từng xuất hiện trước đó); (2) `practice#0` & `de.md`: `Stack VM` (chữ viết tắt `VM` chưa giảng) | Không có bảng | **1** |
| `L11` | (1) `prereq#1`: `for i in range(4):`; (2) `example#0`: `s += a[i] * ...`; (3) `example#3`: `DEBUG = False`, `...`; (4) `de.md`: `AST` | Không có bảng | **0** |
| `L12` | (1) `example#0`: `from functools import reduce`, `range(1, 7)`; (2) `pitfalls#3`: `@lru_cache` (cú pháp decorator `@`); (3) `de.md`: `tuple`, `(4,)` (tuple 1 phần tử) | Không có bảng | **0** |
| `L13` | (1) `stage3#2`: `tranh chấp` (chưa định nghĩa tại chỗ, bài `L12` chỉ dùng `mất cập nhật`); (2) `practice#1`: `round(...)` | Có bảng ở `practice#0`, **không** phủ `round(...)` | **1** |

---

## 5. Bảng độ sâu & đánh giá `L00–L13`

| Bài | sha16 lúc đọc | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | Mất gốc | P8 | P9 | Chỗ thiếu chính | Cần biết trước |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|---|
| `L00` | `79fe4945a4b2bc38` | 8.6 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 0 | P1 (`def, return, { }`), `de.md` sai pha, thiếu stdout, P9=0 | Cú pháp hàm Python, `{ }`, `bash` |
| `L01` | `c60ba8911b166694` | 10.3 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 0 | P1 (`re.findall, r'...'`), lộ giải trước `pause`, `covers:` lệch, P9=0 | Mô-đun `re`, raw string `r'...'`, `Lexer` |
| `L02` | `2adf86ee2362fb3a` | 9.0 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 1 | P1 (`def, in, tuple`), `de.md` dùng `factor` ≠ `atom`, thiếu `Hai mức quy mô` ở `recap` | Hàm Python, tuple, `while ... in` |
| `L03` | `1ab68b29d27c050b` | 8.2 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 0 | P1 (`def, //, **`), `covers:` lệch, `de.md` thiếu stdout, P9=0 | Toán tử Python `//`, `**` |
| `L04` | `692c80a668602010` | 8.2 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 0 | P1 (`#, round, thue=0.1, lexical`), `loi_giai` gán cứng, P9=0 | Chú thích `#`, `round`, tham số mặc định, `lexical` |
| `L05` | `4d067cfc44feb556` | 9.6 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 0 | P1 (`1.0f, 0x, AST`), `loi_giai` không duyệt AST, P9=0 | Hệ 16 `0x`, hậu tố `f` trong C, `AST` |
| `L06` | `26c2c07c9917eea3` | 7.4 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 12 | ĐỦ | 1 | 0 | P1 (`bool`, `(int, int) -> int`), `loi_giai` không đọc `constraints`, P9=0 | Kiểu `bool`, ký pháp hàm nhiều đối |
| `L07` | `91082d8977d9dfd9` | 7.9 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 1 | P1 (`+=, list(map), list comp, {}, not in`), `covers:` lệch, thiếu `recap` P9 | List comprehension, `range`, `dict {}` |
| `L08` | `7cc65e20c6a5bdc1` | 9.6 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 1 | P1 (`with, try/finally, set, pop, BFS`), lộ giải trước `pause`, code là DFS≠BFS | `with`, `try/finally`, `set`, `BFS/DFS` |
| `L09` | `dfa0f46699cd17e4` | 8.3 | 0 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ | 1 | 0 | P1 (`void, a,b=b,a, dict()`), TTS đọc rơi `++`, `de.md` thiếu stdout, P9=0 | C/C++ `void`, tuple unpacking, `dict()` |
| `L10` | `d0804d6d2f87d842` | 8.4 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 12 | ĐỦ | 1 | 0 | P1 (`∘, VM`), `covers: obj3->practice` lệch nặng, P9=0 | Ký hiệu `∘`, viết tắt `VM` |
| `L11` | `0581b572f57228d2` | 8.0 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 0 | P1 (`for/range, +=, a[i], False, AST`), `covers:` lệch, P9=0 | Vòng lặp `for/range`, mảng `a[i]`, `False`, `AST` |
| `L12` | `7fb955496d610816` | 9.4 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 1 | P1 (`from..import, range(1,7), @lru_cache, tuple, (4,)`), `covers:` lệch, thiếu `recap` P9 | `from ... import`, decorator `@`, `tuple`, `(4,)` |
| `L13` | `98b51de914579e77` | 17.5 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 12 | ĐỦ | 0 | 1 | P1 (`tranh chấp, round`), lộ giải trước `pause`, `covers:` lệch, thiếu `recap` P9 | `tranh chấp` (race condition), `round(...)` |

*(Ghi chú: về độ sâu lý thuyết thuần túy `P2..P6`, cả 14 bài đều rất tốt, có hình cơ chế SVG rõ, ví dụ tính tay từng bước, tự kiểm độc lập, quiz có dừng và giải từng bước, mẹo người đi làm thực tế; điểm bị kéo xuống chủ yếu nằm ở `P1` cú pháp mã chưa giảng trước, `P7 covers:`, `P8` thực hành, và `P9` phần `recap`.)*

---

## 6. Người học kẹt ở đâu (góc nhìn người mất gốc từ số 0)

- **L00**: Kẹt ở `pitfalls#3` (`def xu_ly(n):`, `if n >= 0:`, `return`) vì chưa từng học cú pháp hàm/rẽ nhánh Python; sang lab `L00/de.md` bị rối vì đề gọi cú pháp là "pha 1" và ngữ nghĩa là "pha 2" (trái bảng 5 pha vừa học) và không biết phải in chuỗi `syn_err=1 sem_err=1`.
- **L01**: Kẹt ở `practice#1` (`re.findall(r'[A-Za-z_]\w*|\d+|[=+*/-]', ...)`) vì bảng đọc `practice#0` chỉ giải thích chung chung `import thu_vien` và `f"{val:.3f}"`, không giảng `re.findall` hay `r'...'`; ngoài ra xem `practice#1-#2` là thấy luôn đáp án trước khi kịp bấm dừng làm.
- **L02**: Kẹt ở `code#0` (`while peek() in ("+", "-"):`, `v = (op, v, term())`) vì chưa biết toán tử `in` hay cấu trúc tuple 3 phần tử; khi mở `L02/de.md` gặp tên hàm `factor` dù cả bài chỉ dạy `atom`.
- **L03**: Kẹt ở `pitfalls#2` (`phép // của Python`) và `check#0` (`2**3**2`) vì chưa biết toán tử `//` và `**` trong Python.
- **L04**: Kẹt ở `hook#0` (`# biến cục bộ`) và `pitfalls#3` (`round(...)`, `thue=0.1`) do chưa giảng cú pháp chú thích và tham số mặc định; mở `de.md` gặp thuật ngữ `lexical` và `lookup` chưa từng xuất hiện trong bài.
- **L05**: Kẹt ở `example#1` (`1.0f`, `0x3F800000`) do không giải thích hậu tố `f` và tiền tố `0x`; mở `de.md` gặp viết tắt `AST` chưa từng giảng ở `L03` hay `L05`.
- **L06**: Kẹt nhẹ ở `unify#0` (`int = bool` — màn hình viết `bool`, chỉ tai nghe mới biết là "đúng sai") và `de.md` viết kiểu hàm 2 đối `+ : (int, int) -> int` khác ký pháp `'a → 'b` trong bài.
- **L07**: Kẹt nặng ở `pitfalls#0` (`[lambda: i for i in range(3)]`, `lambda i=i: i`) và `pitfalls#3` (`c = {}`, `if x not in c:`) — có tới 3 cấu trúc Python nâng cao (list comprehension, giá trị mặc định trong lambda, từ điển) chưa được giảng trước.
- **L08**: Kẹt ở `pitfalls#2` (`with`, `try … finally`) và `practice#1` (`set(adj) - alive`, `while q:`, `.pop()`, `.add()`, `sorted()`), thêm `de.md` yêu cầu `BFS` chưa từng giảng (mà code mẫu lại viết DFS).
- **L09**: Kẹt khi nghe ở `sym#0`/`example#4` vì TTS đọc `C++` thành `"C"` (`xe`), và trên màn hình gặp `void f(int x)`, `a, b = b, a`, `dict(a)` chưa giải thích.
- **L10**: Kẹt nhẹ ở `recap#0` (`a ∘ b`) và `practice#0`/`de.md` (`Stack VM` — chưa giới thiệu viết tắt `VM`).
- **L11**: Kẹt ở `prereq#1` (`for i in range(4):`), `example#0` (`s += a[i] * ...`), `example#3` (`DEBUG = False`), và `de.md` (`AST`).
- **L12**: Kẹt ở `example#0` (`from functools import reduce`, `range(1, 7)` dừng ở 6), `pitfalls#3` (`@lru_cache`), và `de.md` (`tuple`, `(4,)`).
- **L13**: Kẹt nhẹ ở `stage3#2` (`tranh chấp` chưa giảng nghĩa tại chỗ) và `practice#1` (`round(...)`); ngoài ra lộ đáp án ngay trước `pause`.
