# Báo cáo kiểm định AF4 v2 — RBM L00–L09 (độc lập, CHỈ ĐỌC 100%)

**Kết luận tổng thể: NO-GO**

*(Đã đọc toàn bộ `lessons/rbm/L00..L09`, `labs/rbm/L00..L09/{de.md,loi_giai.py,mong_doi.txt}`, `curriculum/rbm.yaml`, `audit/rbm/verify_rbm.py`, `audit/review/screen_code/rbm.yaml`, `audit/layout_RBM.tsv` và chạy kiểm chứng độc lập bằng `.venv\Scripts\python.exe`.)*

---

## 1. Bảng tóm tắt chỉ số (`RBM L00–L09`)

| Chỉ số | Kết quả | Ghi chú |
|---|---|---|
| `lv.py lint` (`L00–L09`) | **10 / 10 PASS** (`0 FAIL`, `0 WARN`) | Thời lượng ước lượng `10,2–15,8` phút (tất cả `>= 9` phút) |
| Số bài `MUST = 0` | **0 / 10** (`L00–L06, L09` vướng `covers:`/P1; `L02, L08, L09` vướng `de.md`; `L07` vướng `covers:`+`_`) | Đã sửa triệt để lộ `loi_giai.py`/`mong_doi.txt` trước `pause: 30` ở cả 10 bài |
| Số bài `P1 = 2` (đường chính / chuẩn chặt cả `practice` & `de.md`) | **10 / 10** (đường chính) · **0 / 10** (chuẩn chặt) | Đường chính toán học sạch (`^T`, `⇒` đã giảng); `L07, L08` đạt `1` (chỉ thiếu `_`), `L00–L06, L09` = `0` (thiếu `*`, `and`, `acos`, `degrees`, list comp lồng, mặc định, `q_conj`, `vết tr(A)`) |
| Số bài `P8 = 2` | **7 / 10** (`L00, L01, L03–L07`) | `L02, L08, L09` = `1` (`de.md` thiếu định dạng/thứ tự nghiệm hoặc dùng `q_conj` chưa giảng); 10/10 ẩn lời giải & output sau `pause: 30`, số liệu khác ví dụ bài |
| Số bài `P9 = 2` | **8 / 10** (`L00, L01, L03, L04, L06–L09`) | `L02, L05` = `1` (có `Hai mức quy mô:` ở `recap`, thiếu cảnh/bảng quy mô ở thân bài) |
| `verify_rbm.py` | **92 / 92 PASS** | Khớp SymPy/NumPy/checklib |
| `screen_code.py check --course RBM` | **36 / 36 PASS** (`FAIL 0`, `STALE 0`, `MISSING 0`, `ORPHAN 0`, `WARN 0`) | `other/text 18`, `run/python 18`, `unverified_claims: 0` |
| `lab_gate.py RBM` & chạy trực tiếp `loi_giai.py` | `lab_gate.py` trong sandbox bị `Git\bin\bash.exe` exit `-1073741502` (ngoài sandbox `task-7560` đã đạt `18 PASS · 0 FAIL`) · Python trực tiếp `L00–L09`: **10 / 10 `rc=0` khớp `mong_doi.txt`** | Khớp 100% `mong_doi.txt` |
| `audit/layout_RBM.tsv` | **2 byte (0 dòng cảnh báo)** | 0 tràn khung |
| Trạng thái MP4 (`out/rbm/L00–L09`) | **Đang dựng lại trong `build_queue.py` (`task-7660`)** | L01–L09 đang chờ tới lượt trong hàng đợi tuần tự |

---

## 2. Đối chiếu từng bài & trạng thái dựng MP4 (`L00–L09`)

| Bài | `yaml_sha16` | `build_report` `spec_sha256[:16]` | `built_at` | Phút (`lint`) | Lab `loi_giai.py == mong_doi.txt` | `"càng "` / Toán thô `say` |
|---|---|---|---|---|---|---|
| L00 | `ef34ae2f88f7d1ce` | `d31e79204d2d0bce` (lệch — đang dựng) | `2026-11-20T10:07:49Z` | 14.5 | Khớp (`rc=0`) | 0 / 0 |
| L01 | `b063a74dabbc3958` | `bdb801df139cedce` (chờ queue) | `2026-11-20T04:21:11Z` | 13.5 | Khớp (`rc=0`) | 0 / 0 |
| L02 | `babcf0410a609d59` | `a17798adda7eb251` (chờ queue) | `2026-11-20T04:23:55Z` | 11.3 | Khớp (`rc=0`) | 0 / 0 |
| L03 | `73d035c058324f37` | `a1e3b7e237a86393` (chờ queue) | `2026-11-20T04:26:10Z` | 10.6 | Khớp (`rc=0`) | 0 / 0 |
| L04 | `e7b5380a4a84e294` | `3d5b5862207df951` (chờ queue) | `2026-11-20T04:28:03Z` | 10.2 | Khớp (`rc=0`) | 0 / 0 |
| L05 | `af25825e029f30cd` | `c2920bc94459e017` (chờ queue) | `2026-11-20T04:30:17Z` | 11.4 | Khớp (`rc=0`) | 0 / 0 |
| L06 | `116df244c213ac07` | `cb0472d55f683f3c` (chờ queue) | `2026-11-20T04:33:23Z` | 15.3 | Khớp (`rc=0`) | 1 (`prereq[0]`) / 0 |
| L07 | `abf489e47d68ce4f` | `5e9baa4f0469cd74` (chờ queue) | `2026-11-20T04:36:17Z` | 12.1 | Khớp (`rc=0`) | 1 (`hook[0]`) / 0 |
| L08 | `5e8241475bf98564` | `cd6d014bec80eff2` (chờ queue) | `2026-11-20T04:38:30Z` | 11.9 | Khớp (`rc=0`) | 0 / 0 |
| L09 | `0c191f2ae195c6f2` | `a2b2cff7c6edb270` (chờ queue) | `2026-11-20T04:41:14Z` | 15.8 | Khớp (`rc=0`) | 0 / 0 |

---

## 3. Danh sách phát hiện chi tiết (`MUST` / `SHOULD` / `INFO`)

### A. MUST (bắt buộc sửa)

1. **L00, L01, L02, L03, L04, L06, L07 — `covers:` vẫn trỏ sai cảnh dạy thực tế (CONFIRMED)**
   - `L00` L429–430: `obj 2` ("Kiểm RᵀR = I và det R = 1") trỏ `check` (`check` chỉ nhân theo hàng và quay `-30°`), đúng phải là `props` (L257–284). (`obj 1` nên trỏ `sym` hoặc `example`).
   - `L01` L419–420: `obj 3` ("Giải thích khoá gimbal...") trỏ `check` (`check` chỉ nhân `Rz Rx` và `Rx Rz`), đúng phải là `gimbal` (L246–286).
   - `L02` L396–397: `obj 1` ("Nhân hai quaternion theo bảng i, j, k") trỏ `formula` (`formula` chỉ giới thiệu `q` và phép kẹp `q(0,v)q⁻¹`, không dạy bảng `i, j, k`), đúng phải là `sym` (L124–158).
   - `L03` L349–350: `obj 3` ("Tính nghịch đảo của một biến đổi cứng") trỏ `check` (`check` làm từng phép không dùng ma trận), đúng phải là `chain` (L217–226).
   - `L04` L346–347: `obj 3` ("Tính khoảng cách đầu tay tới gốc, chuẩn bị cho vùng với tới") trỏ `practice` (chỉ có bảng hướng dẫn lab), đúng phải là `reach` (L209–235).
   - `L06` L440–441: `obj 2` ("Tính det J = L₁L₂ sin θ₂ và nhận ra cấu hình kỳ dị") trỏ `check` (`check` chỉ kiểm hình học cột 1 và nhích `1°`), đúng phải là `singular` (L268–299).
   - `L07` L342–345: `obj 1` ("Đọc phương trình vi phân x′ = f(x)...") trỏ `example` (đúng là `sym`); `obj 2` ("Giải gần đúng bằng phương pháp Euler") trỏ `check` (`check` không lặp Euler mà tính `0,9¹⁰` bằng bình phương liên tiếp và `1/e`), đúng phải là `formula` hoặc `example`.

2. **L02, L08, L09 — P8 `de.md` chưa 100% tự đứng để người học tự qua `cham.sh` (CONFIRMED)**
   - `labs/rbm/L08/de.md` L4: chỉ ghi `In đúng 1 dòng err_euler=... err_rk4=... gain=...x.` — **thiếu hoàn toàn quy cách làm tròn** cho cả 3 giá trị (`err_euler` `:.4f`, `err_rk4` `:.2e`, `gain` số nguyên `:.0f` cho ra `6935x`).
   - `labs/rbm/L09/de.md` L3–4: ghi `In đúng 1 dòng eigs=(l1, l2) stable=0/1.` — **thiếu quy ước thứ tự** (`l1 >= l2` để ra `(-2.0, -3.0)` thay vì `(-3.0, -2.0)`) và **thiếu độ làm tròn** (`:.1f`). Ngoài ra L3 dùng từ `vết tr(A)` chưa từng giảng trong bài `L09` (bài chỉ gọi "tổng đường chéo").
   - `labs/rbm/L02/de.md` L3–4: dùng ký hiệu `q_conj` chưa từng giảng trong bài (`L02` chỉ viết `q^{-1}` / "đổi dấu phần vector"); và L4 ghi `(làm tròn 3 chữ số)` chung cho cả `norm_q=... rotated=(x, y, z)`, nhưng `mong_doi.txt` lại trộn `norm_q=1.000` (`:.3f`) với `rotated=(-1.232, 1.866, 0.0)` (`round(..., 3)` -> `0.0`).

3. **L00–L09 — P1 chặt ở `practice` (bảng `viết trong mã` còn sót ký hiệu/hàm trong `loi_giai.py`) (CONFIRMED)**
   - **L00:** thiếu list comprehension lồng `[[... for j in range(2)] for i in range(2)]`, generator `max(... for i in range(2) for j in range(2))`, chỉ số 2 chiều `R[0][0]`, gán nhiều biến `c, s = ...`, tuple `(x, y)`.
   - **L01:** dùng tuple ngoặc tròn `(1, 1, 0)` chưa giải thích.
   - **L02:** thiếu giải nén 4 biến `w1, x1, y1, z1 = a`, tuple `(...)`.
   - **L03:** thiếu **toán tử `*` bung đối số** trong `tr(*rot90(2, 1))`, `rot90(*tr(2, 1))`, thiếu `lambda x, y:` hai đối số.
   - **L04:** thiếu gán nhiều biến `L1, L2 = 1.2, 0.8`.
   - **L05:** thiếu **toán tử `*` bung đối số** `*sols[0]`, **toán tử `and`**, hàm **`acos`** & **`degrees`**, giải nén nhiều biến trong `for a, b in sols`.
   - **L06:** thiếu **tham số mặc định** `L1=1.0, L2=0.5`, chỉ số 2 chiều `J[0][0]`.
   - **L07, L08:** thiếu biến ẩn `_` trong `for _ in range(...)`.
   - **L09:** thiếu **toán tử `and`**, chỉ số 2 chiều `A[0][0]`, `tr` / `"vết tr(A)"`.

---

### B. SHOULD

1. **L04 `recap[1]` (L333–334) — Màn hình (`show`) vẫn thiếu điều kiện `"của tay máy chuỗi hở"`, lệch với `say` (CONFIRMED)**
   - `say` L334: `"động học thuận của tay máy chuỗi hở luôn có đúng một đáp án..."`
   - `show` L333: `"động học thuận luôn có đúng một đáp án, tính thẳng được."`

2. **L02, L05 — P9 mới có ở `recap`, thiếu cảnh/bảng so sánh 2 mức quy mô ở thân bài (`P9 = 1`) (CONFIRMED)**
   - `L02` chỉ có `Hai mức quy mô:` ở `recap[0]` L378; `L05` chỉ có `Hai mức quy mô:` ở `recap[0]` L352.

3. **Sai số định lượng nhỏ ở `L00`, `L01` và nhãn SVG sát nhau ở `L01 example[0]` (CONFIRMED)**
   - `L00 recap[0]` L410: `show` viết `"Robot 1 m lệch góc 1° sai vài mm"` (thực tế `1 m · sin 1° ≈ 17,5 mm`, tức `~1,7 cm`).
   - `L01 pitfalls[4]` L327: viết `"Góc cổ tay nhỏ (5°): đổi thứ tự quay sai nhẹ (~0,04 rad)"` (thực tế góc sai lệch `≈ 0,0076 rad ≈ 0,44°`).
   - `L01 example[0]` L165: nhãn trục `y` (`y=234.8`) và nhãn `(0, 1, 0)` (`y=252.8`) đứng sát nhau theo chiều dọc.

4. **Chưa dựng lại xong MP4 `out/rbm/L00–L09`** (hàng đợi `task-7660` đang chạy).

---

## 4. Bảng chấm điểm từng bài (`L00–L09`)

| Bài | `yaml_sha16` | Phút | P1 (chính / chặt) | P8 | P9 | Lỗi chính cần xử lý |
|---|---|---|---|---|---|---|
| L00 | `ef34ae2f88f7d1ce` | 14.5 | 2 / 0 | 2 | 2 | `covers[2]` (`check`→`props`); P1 `practice` thiếu list comp lồng/generator/`R[0][0]`/`c, s =`; `recap[0]` `"1° sai vài mm"`→`~1,7 cm` |
| L01 | `b063a74dabbc3958` | 13.5 | 2 / 0 | 2 | 2 | `covers[3]` (`check`→`gimbal`); P1 `practice` thiếu tuple `(...)`; `pitfalls[4]` `0,04 rad`→`~0,008 rad`; SVG `example[0]` nhãn `y` sát `(0, 1, 0)` |
| L02 | `babcf0410a609d59` | 11.3 | 2 / 0 | 1 | 1 | `covers[1]` (`formula`→`sym`); `de.md` dùng `q_conj` & lệch `1.000` vs `0.0`; P1 `practice`; P9 thiếu ở thân bài |
| L03 | `73d035c058324f37` | 10.6 | 2 / 0 | 2 | 2 | `covers[3]` (`check`→`chain`); P1 `practice` thiếu `*rot90(...)`, `lambda x, y:` |
| L04 | `e7b5380a4a84e294` | 10.2 | 2 / 0 | 2 | 2 | `covers[3]` (`practice`→`reach`); `recap[1]` `show` thiếu `"của tay máy chuỗi hở"`; P1 `practice` thiếu `L1, L2 = ...` |
| L05 | `af25825e029f30cd` | 11.4 | 2 / 0 | 2 | 1 | P1 `practice` thiếu `*sols[0]`, `and`, `acos`, `degrees`, `for a, b in`; P9 thiếu ở thân bài |
| L06 | `116df244c213ac07` | 15.3 | 2 / 0 | 2 | 2 | `covers[2]` (`check`→`singular`); P1 `practice` thiếu tham số mặc định `L1=1.0`, `J[0][0]` |
| L07 | `abf489e47d68ce4f` | 12.1 | 2 / 1 | 2 | 2 | `covers[1,2]` (`example`/`check`→`sym`/`example`); P1 `practice` thiếu biến `_` |
| L08 | `5e8241475bf98564` | 11.9 | 2 / 1 | 1 | 2 | `de.md` thiếu định dạng `:.4f`, `:.2e`, `:.0f`; P1 `practice` thiếu biến `_` |
| L09 | `0c191f2ae195c6f2` | 15.8 | 2 / 0 | 1 | 2 | `de.md` thiếu thứ tự `l1 >= l2`, `:.1f` & `vết tr(A)`; P1 `practice` thiếu `and`, `A[0][0]` |
