# Báo cáo kiểm định độc lập WP-AF4-5 Stage 10 — Khoá TOC (`L00–L14`, 15 bài)

**Kết luận tổng thể: `NO-GO`** (chỉ đọc, không sửa bất kỳ tệp nào trên `D:\research-video`).

---

## 1. Tổng hợp kỹ thuật & tỷ lệ `P1`, `P8`, `P9`

- **Đối chiếu tính toán lý thuyết (`audit/toc/verify_toc.py`)**: **102/102 PASS**.
- **Chạy thật `labs/TOC/L*/loi_giai.py` bằng `.venv/Scripts/python`**: **15/15 khớp `mong_doi.txt`** (lưu ý: `lab_gate.py TOC` trả `0 PASS · 15 FAIL` với `rc=3221225794` / `0xC0000142` do lỗi khởi tạo DLL của Git Bash trong môi trường sandbox, không chạy được `cham.sh` qua bash con).
- **`curriculum/toc.yaml` ↔ `YAML` (`objectives`, `example`, `fix`)**: 15/15 khớp nội dung chính (`lv.py curriculum`: `15 bài, 15 đã có đặc tả, 0 lỗi`); riêng `covers:` trong cả 15 bài bị gắn máy móc theo `af2_upgrader.py` (`obj1→example/proof, obj2→verify, obj3→practice`), làm lệch cảnh thực dạy ở hầu hết các bài.
- **`L*.srt == say` & `build_report.json`**: **15/15 `srt == say` khớp 100%**; cả 15 MP4 dựng ngày `2026-11-20T01:30Z–01:55Z` sau thời điểm sửa YAML; 1 giọng duy nhất `vi-VN-NamMinhNeural` (`tts_sources`: `edge` / `edge?`).
- **`asr_report.md`**: **15/15** có `thiếu audio: 0`, `chưa xem xét: 0` (các câu gắn cờ đã đánh dấu `asr_reviewed`, ghi nhận `NOT_VERIFIED bằng tai người` theo `BN-07`).
- **`audit/layout_TOC.tsv` & ảnh PNG**: `layout_TOC.tsv` rỗng (`2 byte` = 0 lỗi bố cục); đã xem **32 ảnh PNG** mới nhất (`≥ 2 ảnh/bài`), **SVG không đè chữ/không tràn khung (15/15 ĐẠT)**.
- **Kiểm `"càng ..."` và đọc tiếng Việt trong `say`**: **0 câu `"càng ..."`** trong cả 15 bài; lời đọc `say` rõ ràng, tự nhiên, số và ký hiệu đọc thành lời Việt nhất quán.

| Chỉ số | P1 = 2 | P1 = 1 | P1 = 0 | P8 = 2 | P8 = 1 | P8 = 0 | P9 = 2 | P9 = 1 | P9 = 0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Số bài (/15)** | **0 (0.0%)** | **10 (66.7%)** | **5 (33.3%)** | **0 (0.0%)** | **2 (13.3%)** | **13 (86.7%)** | **2 (13.3%)** | **10 (66.7%)** | **3 (20.0%)** |

> **Lý do tỷ lệ P1=2 là 0% và P8=2 là 0% mang tính hệ thống:**
> 1. **13/15 bài (`L00–L09, L11, L13, L14`)** lộ nguyên `loi_giai.py` ở `practice#1` và đầu ra chạy thật ở `practice#2` **TRƯỚC** `practice#3` (`pause: 30`)!
> 2. **15/15 bài (`L00–L14`)** có `labs/TOC/L*/de.md` **thiếu định dạng `stdout`** (tên khoá `count_le3=...`, `s110=...`, v.v.).
> 3. **13/15 bài** có bảng `practice#0` rập khuôn dư hàng không dùng tới (như `f"{val:.3f}"`, `sum / len / max / min`) trong khi thiếu giải thích cú pháp thật dùng trong mã; **2/15 bài (`L10, L12`)** thiếu hẳn `practice#0`.
> 4. **9/15 bài (`L00, L02, L04, L05, L07, L08, L10, L11, L12`)** cài `loi_giai.py` kiểu đi đường tắt/gán cứng (đặc biệt `L08` kiểm chuẩn giả `for m in [0]`, `L10` bỏ qua `write`/`move`, `L05` viết `5 - 1 - 1`, `L12` viết 3 biến `True`).
> 5. **13/15 bài (`L00–L12`)** chưa đạt chuẩn `P9` (`Hai mức quy mô` định lượng + đánh đổi ở thân bài và `recap`).

---

## 2. Báo cáo chi tiết từng bài (`L00..L14`)

### `L00` — Bảng chữ cái, chuỗi và ngôn ngữ (`sha: c34508383694d1b2`, `srt==say: True`)
- **P1=1 | P8=0 | P9=0**
- **MUST**:
  - `practice#1` (`L00_chuoi_ngon_ngu.yaml:315`) lộ nguyên `loi_giai.py` và `practice#2` (`:318`) lộ `count_le3=15` trước `practice#3` (`pause: 30`, `:328`).
  - `labs/TOC/L00/de.md` thiếu định dạng `stdout` (`count_le3=<số>`).
- **SHOULD**:
  - `practice#0` (`:312`) giải thích thừa `f"{val:.3f}"`, `for x in ds:`, `len/max/min` nhưng không giải thích `range(4)` và `2**k` dùng trong mã; `loi_giai.py` (`sum(2**k for k in range(4))`) không liệt kê chuỗi như `de.md` yêu cầu; số liệu `≤ 3`, `15` trùng ví dụ `example`.
  - Thiếu `Hai mức quy mô` (P9=0) trong thân bài và `recap`.
  - `covers:` (`:351-357`) gắn sai cảnh: `obj1` ("Định nghĩa...") trỏ `example` (thực dạy ở `sym`/`concat`), `obj2` ("Hiểu ngôn ngữ...") trỏ `verify` (thực dạy ở `lang`).
- **INFO**: SVG cây nhị phân (`00031.png`) rõ đẹp; `verify_toc.py` 4/4 PASS.
- **PNG đã xem**: `out/TOC/L00/frames/00031.png` (SVG), `00070.png` (`practice#0`), `00071.png` (`practice#1`).

### `L01` — Ôtômat hữu hạn đơn định (DFA) (`sha: f805c7acb2c98cf3`, `srt==say: True`)
- **P1=1 | P8=0 | P9=1**
- **MUST**:
  - `practice#1` (`:291`) lộ nguyên `loi_giai.py` và `practice#2` (`:294`) lộ `s110=1 s111=0 all_2000=1` trước `pause: 30` (`:304`).
  - `labs/TOC/L01/de.md` thiếu định dạng `stdout` (`s110=... s111=... all_2000=...`).
- **SHOULD**:
  - `practice#0` (`:288`) thừa `f"{val:.3f}"`, thiếu giải thích `bin(n)[2:]`, `all(...)`, `int(ch)`; `de.md` dùng biến `rem` (viết tắt *remainder*) chưa chú thích; số liệu lab (`1..1999`, `110`, `111`) trùng hệt ví dụ `example`/`verify`/`curriculum`.
  - Thiếu 2 mức quy mô + đánh đổi (chỉ nêu định tính bộ nhớ cố định 3 trạng thái); `recap` chưa nhắc quy mô.
  - `covers:` `obj2` ("Thiết kế DFA...") trỏ `verify` thay vì `design`; `obj3` ("Kiểm DFA đầy đủ...") trỏ `practice` (trong `practice` không kiểm đầy đủ hàm chuyển) thay vì `verify`.
- **INFO**: SVG `dfa3` (`00026.png`) khớp bảng chuyển; `verify_toc.py` 6/6 PASS.
- **PNG đã xem**: `out/TOC/L01/frames/00026.png` (SVG + bảng), `00074.png` (`practice#0`).

### `L02` — Ôtômat không đơn định và phép dựng tập con (`sha: 4baa8e945faaaec2`, `srt==say: True`)
- **P1=0 | P8=0 | P9=1**
- **MUST**:
  - `labs/TOC/L02/de.md` **mâu thuẫn ký hiệu với bài**: đề viết dựng DFA `{q0}, {q0,q1}, {q0,q2}`, trong khi bài (`sym`, `example`) dùng trạng thái `A, B, C` và các tập `{A}, {A, B}, {A, C}`! Đồng thời `de.md` thiếu định dạng `stdout` (`dfa_states=... acc_101=... acc_110=...`).
  - `practice#1` (`:281`) lộ nguyên `loi_giai.py` và `practice#2` (`:284`) lộ kết quả trước `pause: 30` (`:294`).
  - `loi_giai.py` gán cứng DFA `delta = {0:..., 1:..., 2:...}` và `dfa_states=3`, **đi đường tắt không cài thuật toán dựng tập con (`subset_construct`)** như `de.md` yêu cầu.
- **SHOULD**:
  - `practice#0` (`:278`) thừa `f"{val:.3f}"`, `for x in ds:`, thiếu giải thích từ điển lồng `delta[st][ch]`; số liệu lab (`endswith('01')`, `'101'`) trùng ví dụ `example`/`verify`.
  - Thân bài (`pitfalls#3`, `quiz#1`) có các mức `n=2,3,4` (`3→4`, `4→8`, `5→16` cho `n+1` vs `2^n`), nhưng `recap` chưa nhắc đánh đổi kích thước này (`P9=1`).
  - `covers:` `obj2` ("Đổi NFA thành DFA...") trỏ `verify` thay vì `example`; `obj3` ("...DFA có thể lớn gấp 2ⁿ") trỏ `practice` thay vì `pitfalls`/`quiz`.
- **INFO**: Cả 2 SVG (`00012.png`, `00035.png`) rõ nét, không đè chữ; `verify_toc.py` 10/10 PASS.
- **PNG đã xem**: `out/TOC/L02/frames/00012.png` (SVG NFA), `00035.png` (SVG DFA), `00069.png` (`practice#0`).

### `L03` — Biểu thức chính quy và định lý Kleene (`sha: 3e7c7dfac15db3d0`, `srt==say: True`)
- **P1=1 | P8=0 | P9=0**
- **MUST**:
  - `practice#1` (`:321`) lộ nguyên `loi_giai.py` và `practice#2` (`:324`) lộ `matches=127 exact=1` trước `pause: 30` (`:334`).
  - `labs/TOC/L03/de.md` thiếu định dạng `stdout` (`matches=... exact=...`).
- **SHOULD**:
  - **P1**: `pitfalls#2` (`:260`) dùng chữ `"regex"` chưa chú thích là viết tắt của biểu thức chính quy (*regular expression*); `de.md` dùng `re.fullmatch(...)` và `s.endswith('01')` chưa giải thích (còn `loi_giai.py` dùng `re.compile(r'^(0|1)*01$')` + `pat.match(s)`); `practice#0` (`:318`) thừa `f"{val:.3f}"`, thiếu `1 << L`, `format(...)`, `re.compile`.
  - Số liệu lab (`(0|1)*01`, độ dài `≤ 8`) trùng ví dụ `example`.
  - Thiếu `Hai mức quy mô` trong thân bài và `recap` (P9=0).
  - `covers:` `obj2` ("Nắm thứ tự ưu tiên...") trỏ `verify` thay vì `prec`; `obj3` ("Biết định lý Kleene...") trỏ `practice` thay vì `kleene`.
- **INFO**: SVG đường đi trên NFA (`00023.png`) đẹp, rõ; `verify_toc.py` 7/7 PASS.
- **PNG đã xem**: `out/TOC/L03/frames/00023.png` (SVG), `00078.png` (`practice#0`).

### `L04` — Bổ đề bơm và ngôn ngữ không chính quy (`sha: 301371996d2af9cb`, `srt==say: True`)
- **P1=1 | P8=0 | P9=1**
- **MUST**:
  - `practice#1` (`:296`) lộ nguyên `loi_giai.py` và `practice#2` (`:299`) lộ `orig_eq=1 pumped=0000001111 valid=0` trước `pause: 30` (`:309`).
  - `labs/TOC/L04/de.md` thiếu định dạng `stdout`.
  - `loi_giai.py` dùng phép kiểm hằng đúng `orig_eq=int('0'*p=='0'*p)` (luôn là `1` với mọi chuỗi!), không kiểm `x+y+z == '0'*p + '1'*p` hay điều kiện `|xy| <= p, |y| >= 1`.
- **SHOULD**:
  - `practice#0` (`:293`) thừa `f"{val:.3f}"`, thiếu `.count('0')`; số liệu lab (`p=4`, `y='00'`, `0000001111`) trùng hệt `example` bước 1–3.
  - Thiếu 2 mức quy mô định lượng (chỉ nêu định tính `recap` "không đếm được tới vô hạn").
  - `covers:` `obj1` ("Phát biểu đúng bổ đề bơm...") trỏ `example` thay vì `sym`/`why`; `obj2` trỏ `verify` thay vì `example`; `obj3` ("chỉ dùng để bác bỏ") trỏ `practice` thay vì `pitfalls`.
- **INFO**: SVG vòng lặp trên DFA `1001` (`00024.png`) rõ đẹp; `verify_toc.py` 18/18 PASS.
- **PNG đã xem**: `out/TOC/L04/frames/00024.png` (SVG), `00077.png` (`practice#0`).

### `L05` — Tối thiểu hoá DFA (`sha: cc3a7d4254beba90`, `srt==say: True`)
- **P1=1 | P8=0 | P9=1**
- **MUST**:
  - `practice#1` (`:325`) lộ nguyên `loi_giai.py` và `practice#2` (`:328`) lộ `min_dfa_states=3` trước `pause: 30` (`:338`).
  - `loi_giai.py` **đi đường tắt hoàn toàn**: chỉ viết `raw_states = 5; unreachable = 1; merged_pair = 1; min_states = raw_states - unreachable - merged_pair`, không chạy thuật toán đánh dấu cặp hay phân hoạch tương đương nào như `de.md` nêu!
  - `labs/TOC/L05/de.md` thiếu định dạng `stdout` (`min_dfa_states=...`).
- **SHOULD**:
  - `practice#0` (`:322`) thừa `f"{val:.3f}"` (mã chỉ có 3 phép gán và trừ); số liệu lab (`5`, `1`, `1`, `3`) trùng hệt ví dụ `example`.
  - P9 chỉ nhắc `NFA 4 vs DFA 8` ở `pitfalls#3`, thiếu 2 mức quy mô và thiếu ở `recap`.
  - `covers:` `obj2` ("Chạy thuật toán đánh dấu cặp...") trỏ `verify` thay vì `example`; `obj3` ("DFA tối tiểu là duy nhất...") trỏ `practice` thay vì `unique`.
- **INFO**: SVG 4 trạng thái (`00022.png`) rõ đẹp, không đè chữ; `verify_toc.py` 8/8 PASS.
- **PNG đã xem**: `out/TOC/L05/frames/00022.png` (SVG), `00083.png` (`practice#0`).

### `L06` — Văn phạm phi ngữ cảnh và cây suy dẫn (`sha: b2b886eaaeafc09d`, `srt==say: True`)
- **P1=1 | P8=0 | P9=0**
- **MUST**:
  - `practice#1` (`:286`) lộ nguyên `loi_giai.py` và `practice#2` (`:289`) lộ `catalan_3=5` trước `pause: 30` (`:299`).
  - `labs/TOC/L06/de.md` thiếu định dạng `stdout` (`catalan_3=...`).
- **SHOULD**:
  - **P1**: `recap#1` (`:314`) hiển thị `"thẻ HTML"` chưa giải thích viết tắt `HTML` trên màn hình (`say` tránh đọc thành "thẻ lồng trong trang mạng"); `practice#0` (`:283`) thừa `f"{val:.3f}"`, `sum/max/min`, thiếu giải thích `1 << 6`, `(m >> i) & 1`, `.append()`; `de.md` dùng `C_3` chưa chú thích lại.
  - Số liệu lab (`độ dài 6`, `C_3 = 5`) trùng ví dụ `example`.
  - Thiếu `Hai mức quy mô` trong thân bài và `recap` (P9=0).
  - `covers:` `obj2` ("Viết suy dẫn và vẽ cây...") trỏ `verify` thay vì `derive`/`example`; `obj3` ("Hiểu phi ngữ cảnh...") trỏ `practice` thay vì `sym`/`pitfalls`.
- **INFO**: SVG cây suy dẫn `0011` (`00024.png`) rõ ràng; `verify_toc.py` 6/6 PASS.
- **PNG đã xem**: `out/TOC/L06/frames/00024.png` (SVG), `00068.png` (`practice#0`).

### `L07` — Văn phạm mơ hồ và phân tích cú pháp biểu thức (`sha: 69fd7aaa769b4bde`, `srt==say: True`)
- **P1=1 | P8=0 | P9=1**
- **MUST**:
  - `practice#1` (`:291`) lộ nguyên `loi_giai.py` và `practice#2` (`:294`) lộ `precedence=7 left_to_right=9` trước `pause: 30` (`:304`).
  - `loi_giai.py` **đi đường tắt hoàn toàn**: chỉ viết `expr_prec = 1 + (2 * 3); expr_left = (1 + 2) * 3`, không cài bộ phân tích cú pháp ưu tiên như `de.md` yêu cầu ("Cài bộ phân tích ưu tiên nhân chia trước cộng trừ trên `'1+2*3'` vs cây ngoặc trái").
  - `labs/TOC/L07/de.md` thiếu định dạng `stdout`.
- **SHOULD**:
  - `practice#0` (`:288`) thừa `f"{val:.3f}"`; số liệu lab (`1+2*3=7`, `(1+2)*3=9`) trùng hệt `hook`/`prereq`/`trees`/`example`.
  - P9: `verify` có dãy số cây Catalan `1, 2, 5, 14` cho `1..4` phép toán, nhưng thiếu phân tích quy mô/đánh đổi ở quy mô lớn và thiếu ở `recap`.
  - `covers:` `obj2` ("Khử mơ hồ bằng phân tầng...") trỏ `verify` thay vì `example`; `obj3` ("Hiểu vì sao trình biên dịch không được đoán ý") trỏ `practice` thay vì `pitfalls`.
- **INFO**: SVG hai cây `1+2×3` (`00017.png`) rõ, cân đối; `verify_toc.py` 7/7 PASS.
- **PNG đã xem**: `out/TOC/L07/frames/00017.png` (SVG), `00069.png` (`practice#0`).

### `L08` — Ôtômat đẩy xuống (`sha: a4b3db59071e5a9f`, `srt==say: True`)
- **P1=0 | P8=0 | P9=1**
- **MUST**:
  - **`loi_giai.py` và `practice#1` (`:284`) có phép kiểm giả/đường tắt nghiêm trọng**:
    `ok = all(pda(bin(m)[2:]) == (bin(m)[2:].startswith('0') and False) for m in [0])`
    1) Chỉ lặp trên `[0]` (`m=0`, chuỗi `'0'`) chứ **KHÔNG hề kiểm chuẩn toàn bộ chuỗi dài `<= 12`** như `de.md` yêu cầu!
    2) Vế phải `(bin(m)[2:].startswith('0') and False)` **luôn bằng `False`**, không phải kiểm tra dạng `0^n 1^n`!
    3) Dùng `bin(m)[2:]` sẽ không sinh được chuỗi bắt đầu bằng `'0'` (ngoài `'0'`), và biến `ok` không được in ra!
    4) Hàm `pda(s)` dùng `else:` nên mọi ký tự khác `'0'` (như `'2'`, `'a'`) đều bị coi là `'1'`!
  - `practice#1` (`:284`) lộ nguyên `loi_giai.py` và `practice#2` (`:287`) lộ `pda_0011=1 pda_0101=0 pda_001=0` trước `pause: 30` (`:297`).
  - `labs/TOC/L08/de.md` thiếu định dạng `stdout`.
- **SHOULD**:
  - **P1**: Thân bài (`equiv#0`, `objectives`) dùng viết tắt **`PDA`** mà **chưa từng giải thích `PDA` là viết tắt của ôtômat đẩy xuống (*Pushdown Automaton*)** tại chỗ; `de.md` dùng `PDA`, `stack`, `pop` (chưa chú thích tiếng Việt); `practice#0` (`:281`) thừa `f"{val:.3f}"`, thiếu giải thích `.append()`, `.pop()`, `all(...)`, `bin(...)`.
  - Các chuỗi kiểm tra `0011`, `0101`, `001` trong `loi_giai.py` trùng y nguyên ví dụ `example` & `pitfalls#1`.
  - `covers:` `obj2` ("Chạy PDA nhận 0ⁿ1ⁿ và ghi vết...") trỏ `verify` thay vì `example`; `obj3` ("PDA tương đương CFG, NPDA > DPDA") trỏ `practice` thay vì `equiv`/`pitfalls`.
- **INFO**: SVG ngăn xếp (`00024.png`) rất rõ; `verify_toc.py` 7/7 PASS.
- **PNG đã xem**: `out/TOC/L08/frames/00024.png` (SVG), `00071.png` (`practice#0`), `00072.png` (`practice#1` — lộ mã & dòng `for m in [0]`).

### `L09` — Máy Turing: băng, đầu đọc và bảng chuyển (`sha: 6968b139df036f30`, `srt==say: True`)
- **P1=1 | P8=0 | P9=1**
- **MUST**:
  - `practice#1` (`:266`) lộ nguyên `loi_giai.py` và `practice#2` (`:269`) lộ `tm_inc=1100` trước `pause: 30` (`:279`).
  - `labs/TOC/L09/de.md` thiếu định dạng `stdout` (`tm_inc=...`).
- **SHOULD**:
  - `practice#0` (`:263`) thừa `f"{val:.3f}"` và `sum/max/min`, thiếu giải thích `while`, `list(...)`, `.insert()`, `.join()`; số liệu lab (`'1011' -> '1100'`) trùng hệt ví dụ `example`/`prereq`.
  - Thiếu 2 mức quy mô + đánh đổi (chỉ giải thích băng vô hạn là mô hình khả năng tính).
  - `covers:` `obj1` ("Mô tả máy Turing...") trỏ `example` thay vì `sym`; `obj3` ("Hiểu băng vô hạn...") trỏ `practice` thay vì `pitfalls`.
- **INFO**: SVG băng máy Turing (`00012.png`) đẹp, rõ đầu đọc đỏ; `verify_toc.py` 5/5 PASS.
- **PNG đã xem**: `out/TOC/L09/frames/00012.png` (SVG + bảng), `00057.png` (`practice#0`), `00058.png` (`practice#1`).

### `L10` — Luận đề Church–Turing và máy Turing vạn năng (`sha: d18da279e609a75b`, `srt==say: True`)
- **P1=0 | P8=1 | P9=1**
- **MUST**:
  - **`loi_giai.py` đi đường tắt không cài máy Turing vạn năng**: chỉ viết `for ch in tape: st, _, _ = tbl[(st, ch)]`, bỏ qua hoàn toàn ký hiệu ghi (`write`) và bước di chuyển đầu đọc (`move = 1` trái/phải/đứng yên), nên đây chỉ là một bộ chạy DFA đi một chiều chứ không phải bộ thông dịch UTM như `de.md` nêu!
  - **P1**: `de.md` và `practice#0` dùng viết tắt **`UTM`** ("Máy Turing vạn năng (UTM)", "bộ thông dịch UTM nhỏ") **chưa từng xuất hiện hay chú thích trong thân bài** (thân bài chỉ dùng chữ $U$), đồng thời `de.md` viết bằng tiếng Anh `(state, sym) -> (new_state, write, move)` và diễn đạt tối nghĩa `"cộng chẵn bit 1"` (thực chất là kiểm tra tính chẵn-lẻ của số bit `1`, in `odd_ones=1`).
  - `labs/TOC/L10/de.md` thiếu định dạng `stdout` (`final_state=... odd_ones=...`).
- **SHOULD**:
  - `practice` chỉ có 2 step (`pause: 30` rồi output), **thiếu `practice#0` (bảng giải mã ký hiệu mã)** (nhưng ưu điểm là **không lộ lời giải trước pause**).
  - Thiếu 2 mức quy mô định lượng (chỉ nêu định tính tính nhanh vs tính được và 10 000 vòng chưa dừng); `recap` chưa nhắc quy mô.
  - `covers:` `obj1` ("Phát biểu luận đề Church–Turing...") trỏ `example` (thực dạy ở `sym`/`evidence`/`pitfalls`); `obj2` ("Hiểu máy Turing vạn năng...") trỏ `verify` thay vì `universal`/`example`; `obj3` ("Phân biệt tính được với tính nhanh") trỏ `practice` thay vì `verify`/`pitfalls`.
- **INFO**: SVG băng UTM (`00027.png`) rất rõ; `verify_toc.py` 7/7 PASS.
- **PNG đã xem**: `out/TOC/L10/frames/00027.png` (SVG), `00004.png` (bảng `prereq`), `00076.png` (`practice#0` — bảng hướng dẫn có `pause: 30`).

### `L11` — Bài toán dừng không khả quyết (`sha: 8bce00af3d4a7b2a`, `srt==say: True`)
- **P1=1 | P8=0 | P9=1**
- **MUST**:
  - `practice#1` (`:287`) lộ nguyên `loi_giai.py` và `practice#2` (`:290`) lộ `contradict_true=1 contradict_false=1` trước `pause: 30` (`:300`).
  - `labs/TOC/L11/de.md` thiếu định dạng `stdout`.
- **SHOULD**:
  - **P1**: `de.md` dùng thuật ngữ tiếng Anh **`diagonalization H(P,P)`** chưa chú thích (bài dùng "chéo hoá" và $H(P, \langle P \rangle)$); `practice#0` (`:284`) thừa `f"{val:.3f}"`.
  - `loi_giai.py` đặt `def H(prog, x): return True` nhưng không hề dùng `prog, x`, hàm `contradiction` chỉ so `h_says_halt != (not h_says_halt)`.
  - P9: `pitfalls#1` nêu Collatz `6 → 8 bước (max 16)` vs `27 → 111 bước (max 9232)` và `recap#1` nêu đánh đổi 3 chiều (bỏ sót/báo nhầm/không trả lời), nhưng không phải 2 mức quy mô hệ thống; `covers:` `obj1` ("Phân biệt khả quyết và nửa khả quyết") trỏ `proof` thay vì `sym`, `obj3` ("không có thuật toán cho MỌI đầu vào") trỏ `practice` thay vì `pitfalls`.
- **INFO**: SVG máy `D` (`00018.png`) rất rõ ràng; `verify_toc.py` 4/4 PASS.
- **PNG đã xem**: `out/TOC/L11/frames/00018.png` (SVG), `00072.png` (`practice#0`).

### `L12` — Quy dẫn và định lý Rice (`sha: 76d1747c62e55f6b`, `srt==say: True`)
- **P1=1 | P8=1 | P9=1**
- **MUST**:
  - `loi_giai.py` **giả lập rỗng hoàn toàn**: chỉ gán 3 hằng số `semantic_only = True; nontrivial_has_yes = True; nontrivial_has_no = True` rồi in `rice_undecidable=1` — không nhận đầu vào hay kiểm tra ví dụ chương trình có/không có tính chất.
  - `labs/TOC/L12/de.md` thiếu định dạng `stdout` (`rice_undecidable=...`).
- **SHOULD**:
  - **P1**: `recap#2` (`:323`) nhắc tới `P` và `NP` trước khi bài 13 định nghĩa; `de.md` dùng ký hiệu `L(M)` chưa giải thích trong bài (`L12` chỉ dùng `P`, `Q`, `B`, `A`); `practice` chỉ có 2 step, thiếu `practice#0` (bảng giải mã ký hiệu mã — nhưng không lộ lời giải trước `pause`).
  - P9: `pitfalls#1` có nêu đánh đổi bộ kiểm kiểu (chấp nhận từ chối nhầm vài chương trình đúng để chặn lỗi kiểu), `pitfalls#3` kiểm 100 bước có giới hạn, nhưng thiếu 2 mức quy mô và thiếu ở `recap`.
  - `covers:` `obj2` ("Phát biểu định lý Rice và kiểm hai điều kiện") trỏ `verify`, `obj3` ("Phân biệt ngữ nghĩa với cú pháp") trỏ `practice` thay vì `classify`.
- **INFO**: SVG đường ống quy dẫn (`00015.png`) rất đẹp; `checks:` trong YAML và `screen_code` (`L12_Q_doi_chieu`) khớp chuẩn.
- **PNG đã xem**: `out/TOC/L12/frames/00015.png` (SVG), `00004.png` (bảng `prereq`), `00078.png` (`practice#0` — bảng hướng dẫn có `pause: 30`).

### `L13` — Độ phức tạp theo máy Turing: P, NP từ góc nhìn mô hình (`sha: a1514f52c696d06c`, `srt==say: True`)
- **P1=0 | P8=0 | P9=2**
- **MUST**:
  - **P1 & sư phạm nặng**: `labs/TOC/L13/de.md` và `loi_giai.py` dùng bài toán **`SAT gán biến`** và **`công thức CNF 3 mệnh đề`** với **`O(m) bước`**, trong khi **TOÀN BỘ bài L13 từ đầu tới cuối chỉ dạy bài toán Tổng tập con (Subset Sum), HOÀN TOÀN KHÔNG ĐỀ CẬP hay giải thích `SAT`, `CNF`, `mệnh đề (clause)` hay `O(m)`**! Người học mất gốc mở `de.md` sẽ bị kẹt hoàn toàn.
  - `practice#1` (`:302`) lộ nguyên `loi_giai.py` và `practice#2` (`:305`) lộ `cert_steps=3 verified=1` trước `pause: 30` (`:315`).
  - `labs/TOC/L13/de.md` thiếu định dạng `stdout` (`cert_steps=... verified=...`).
- **SHOULD**:
  - `practice#0` (`:299`) giải thích `for x in ds:`, `f"{val:.3f}"`, `sum / len / max / min`, hoàn toàn lệch với `practice#1` (dùng `all(any(...))`, `abs(...)`, không có `for x in ds:`, `f"{val:.3f}"`, `sum/len/max/min`); thân bài `recap#1` nhắc `NP đầy đủ` ngắn gọn (`say` nói "loại khó nhất của NP").
  - `covers:` `obj1` ("Định nghĩa P... và NP...") trỏ `example` thay vì `sym`; `obj2` ("hai định nghĩa NP là một") trỏ `verify` thay vì `equiv`/`example`; `obj3` ("Đặt P, NP vào bức tranh chung") trỏ `practice` thay vì `picture`.
- **INFO**: **P9=2** (n=6 → 64; n=10 → 100 vs 1024; n=20 → 400 vs 1,048,576; n=60 → 3600 vs >10^18, >30 năm; `recap` tóm tắt rõ bậc thang và đánh đổi xấp xỉ/vét cạn); SVG cây nhánh (`00024.png`) rõ đẹp; `verify_toc.py` 4/4 PASS.
- **PNG đã xem**: `out/TOC/L13/frames/00024.png` (SVG), `00076.png` (`practice#0`).

### `L14` — Tình huống chuyên gia theo dòng thời gian: biểu thức chính quy từ Thompson tới RE2 (`sha: e3231c529e716b7e`, `srt==say: True`)
- **P1=0 | P8=0 | P9=2**
- **MUST**:
  - `practice#1` (`:528`) lộ nguyên `loi_giai.py` và `practice#2` (`:531`) lộ `backtrack=536870912 nfa_states=59 speedup=3000000x` trước `pause: 30` (`:541`).
  - `labs/TOC/L14/de.md` thiếu định dạng `stdout`.
  - **Lệch thuật ngữ/công thức giữa bài và lab (`P1=0`)**: `de.md` yêu cầu tính `"số trạng thái tuyến tính củaThompson/RE2"` (thiếu dấu cách `"củaThompson"`) theo `O(nm)` và `loi_giai.py` tính `nfa_states = 2 * n + 1 = 59`, trong khi **thân bài L14 không dùng ký hiệu `O(nm)` và không giảng công thức `2*n + 1 = 59`** (bài dạy tập vị trí cỡ `n + 1 = 30` và `n*(n+1) = 870` lần xét!).
- **SHOULD**:
  - `practice#0` (`:525`) thừa `f"{val:.3f}"` (mã dùng `:.0f`, chưa giải thích `20e-6`); số liệu lab (`n=29`, `536870912`, `3000000`) trùng ví dụ `hook` & `stage2`; thân bài `stage3#1` và `quiz#1` hiển thị `KB` trên màn hình mà không chú thích kilobyte trên màn hình (`say` đọc "ki-lô-byte").
  - `covers:` `obj3` ("Chọn bộ máy khớp hợp với nguồn gốc...") trỏ `practice` (chỉ tính `2^29`, `59`, `3000000x`) thay vì `quiz` (nơi thực sự dạy chọn bộ máy kèm điều kiện đổi).
- **INFO**: **P9=2** xuất sắc (5 chặng 1968–2025, đa thức khớp `k²+7k+15` kiểm bằng điểm thứ tư `555`, 200/1000 mẫu, đánh đổi bộ nhớ vs tính năng); khớp `sources_L14.md` và `verify_toc.py` 8/8 PASS; hai SVG (`00026.png`, `00031.png`) rõ nét, không đè chữ.
- **PNG đã xem**: `out/TOC/L14/frames/00026.png` (SVG trục thời gian), `00031.png` (SVG hai cách khớp), `00136.png` (`practice#0`), `00137.png` (`practice#1`), `00138.png` (`practice#2`).

---

## 3. Danh sách toàn bộ PNG đã xem (32 khung)

- `out/TOC/L00/frames/`: `00031.png`, `00070.png`, `00071.png`
- `out/TOC/L01/frames/`: `00026.png`, `00074.png`
- `out/TOC/L02/frames/`: `00012.png`, `00035.png`, `00069.png`
- `out/TOC/L03/frames/`: `00023.png`, `00078.png`
- `out/TOC/L04/frames/`: `00024.png`, `00077.png`
- `out/TOC/L05/frames/`: `00022.png`, `00083.png`
- `out/TOC/L06/frames/`: `00024.png`, `00068.png`
- `out/TOC/L07/frames/`: `00017.png`, `00069.png`
- `out/TOC/L08/frames/`: `00024.png`, `00071.png`, `00072.png`
- `out/TOC/L09/frames/`: `00012.png`, `00057.png`, `00058.png`
- `out/TOC/L10/frames/`: `00004.png`, `00027.png`, `00076.png`
- `out/TOC/L11/frames/`: `00018.png`, `00072.png`
- `out/TOC/L12/frames/`: `00004.png`, `00015.png`, `00078.png`
- `out/TOC/L13/frames/`: `00024.png`, `00076.png`
- `out/TOC/L14/frames/`: `00026.png`, `00031.png`, `00136.png`, `00137.png`, `00138.png`

---

## 4. Kết luận chốt: `NO-GO`

Khoá TOC có phần nội dung cốt lõi, trực quan SVG, `checks:` toán học (`102/102`), và giọng đọc/ASR sạch (`srt==say 15/15`, `layout_TOC.tsv` 0 lỗi). Tuy nhiên cần **sửa trước khi GO**:
1. **Bỏ rò rỉ `loi_giai` trước `pause`** ở `practice` của **13 bài (`L00–L09, L11, L13, L14`)** (chỉ giữ bảng đọc mã khớp đúng mã thật, rồi `pause: 30` với đề bài, rồi mới hiện kết quả mong đợi).
2. **Bổ sung định dạng `stdout` rõ ràng** cho toàn bộ **15 tệp `labs/TOC/L*/de.md`**, sửa thuật ngữ/ký hiệu lệch trong `de.md` (`L02` `q0`→`A,B,C`; `L10` `UTM` + `"cộng chẵn bit 1"`; `L13` đổi lab sang Subset Sum hoặc dạy `SAT/CNF`; `L14` giảng `2n+1`/`O(nm)` hoặc đổi về `n+1=30`/`n(n+1)=870`), và **đổi số liệu lab khác ví dụ bài** để học viên không chép lại.
3. **Viết lại `loi_giai.py` thực chất (không đi đường tắt)** — đặc biệt `L08` kiểm chuẩn đủ 8191 chuỗi `<= 12` (sửa `for m in [0]` và kiểm ký tự `'1'`), `L02` chạy `subset_construct`, `L05` chạy thuật toán đánh dấu cặp, `L07` cài bộ phân tích ưu tiên thật, `L10` cài bộ thông dịch TM hỗ trợ `write` & `move` (T/P/Đ), `L00`/`L04`/`L11`/`L12`.
4. **Chuẩn hoá `P1` & `P9` & `covers:`**: đồng bộ bảng `practice#0` đúng với mã thật của từng bài (và thêm cho `L10, L12`), chú thích `PDA`, `regex`, `HTML`, `KB`, `NP`, bổ sung cảnh/đoạn `Hai mức quy mô` + `recap` cho `L00–L12`, và chỉnh `covers:` trỏ đúng cảnh dạy từng mục tiêu.
