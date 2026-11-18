# fix6 CS112 L00–L14 (sửa theo R4_CS112_A, chuẩn P1 chặt) — 2026-11-16

Tiến độ: L00–L02 xong; L03–L05 xong; L06–L08 xong; L09–L11 xong; L12–L14 xong; sổ screen_code cập nhật; cổng chạy xong (xem cuối). KHÔNG chạy build/tts/asr/git/docker. KHÔNG chạy `tools/lv.py render` (xem "Việc chưa làm được").

## Cách làm
- Khuôn chung (giống DMS fix6): bảng 3 cột "viết trong mã | đọc là | ví dụ" đặt NGAY TRƯỚC mỗi khối mã của cảnh `scale` (step riêng, `clear: true`); một câu mở (focus tiêu đề bảng) + đúng một câu `say` cho mỗi hàng (focus từng hàng). Lời đọc không nói từ khoá/tên hàm (lexicon): tả bằng tiếng Việt, tên thật chỉ nằm trong bảng.
- Đơn giản hoá mã khi cú pháp lạ không phải điều bài dạy: L06 (`i, dem = c, dem + 1` thành hai dòng; `sum(... for ...)` thành vòng `for` + `dem +=`; từ điển `{}`/`.get`/`.values()` thành `[0] * m`, `o[k % m] += 1`, `max(o)`; `[k * n for k in range(n)]` thành `range(0, n * n, n)`). Đầu ra các khối này không đổi (verify_cs112_a ghép nguyên văn và chạy thật: PASS).
- Mỗi bài: chân trang chấm bài (`bash labs/cham.sh ...`) giải thích bằng chữ trên màn hình (bash chạy tệp lệnh; cham.sh là tệp chấm; khoá/bài/tên tệp; in ĐÚNG khi mọi dòng trùng) + một mệnh đề trong lời đọc.
- Bài sinh từ mẫu (L05, L06, L07, L14): sửa `audit/cs112/src/*.tpl.yaml` rồi `regen_a.py gen`; không sửa bài sinh ra. Các bài còn lại sửa YAML trực tiếp. Lab (`labs/CS112/L00–L14`) không đổi.
- Thuật ngữ định nghĩa tại chỗ bằng lời + dòng trên màn hình (KHÔNG thêm mục mới vào `symbols.CS112.yaml`, để khỏi buộc L15–L29 phải `assumes` thêm; các mục `introduces` cũ giữ nguyên, riêng `cs112_dem0` ở L08 chuyển sang step bảng đứng trước mã).
- `asr_reviewed`: so với bản đã staged bằng `git show :...`: không mất mục hợp lệ nào, trừ L00 bỏ 1 mục (câu "Và hai vòng lặp lồng nhau chạy bao nhiêu bước, câu trả lời dẫn tới tổng Sigma." đã được viết lại gọn hơn nên mục không còn hợp lệ). Mục chưa staged của L05 (tpl) và L12 giữ nguyên (đã vào bài sau khi sinh lại).

## Theo bài (đã đổi, số mục chưa giảng ước còn lại)
| Bài | Bảng đọc mã thêm | Thuật ngữ / SHOULD / P2 | Từ | Chưa giảng ước |
|---|---|---|---|---|
| L00 | scale: def/hàm, vòng for + range (cả vòng trong), `+=`, return, print (5 hàng) | "hằng số" (số cố định không đổi theo n) và "e ≈ 2,718" định nghĩa tại chỗ; **P2** ③ Σ i²: một dòng quy nạp (công thức tại n trừ tại n−1 bằng n²), tổng k số lẻ = k² chứng minh bằng tổng ②; bỏ step "hai ký hiệu thường đi cặp", gọn hook/recap/pitfalls để ≤ 2300 | 2296 | 0 |
| L01 | scale: def, return và `*`, for, print (4 hàng) | f(n), g(n) = hàm đếm bước/hàm gọn, "hằng số"; "bậc" = số mũ lớn nhất của n; **SHOULD tiêu đề**: thêm step định nghĩa chặt o, ω (∀c > 0 ∃n₀, ví dụ n ∈ o(n²) với c = 0,01, n₀ = 100) nên tiêu đề giữ nguyên | 2127 | 0 |
| L02 | scale: import math + math.factorial, for, `*` và `**`, print (4 hàng) | quy tắc ④ ln n = log₂ n · ln 2 ở cảnh ôn (định nghĩa ln, "hằng số"); **P2** chuỗi chuẩn ≺: thêm phép tính n²/n³ = 1/n (0,1 ở n=10; 0,01 ở n=100) | 2056 | 0 |
| L03 | scale: def/return, gán hai biến, range, `==`, `+=`/`*=`, print với `//` (6 hàng) | `sys.getsizeof` = hàm cho biết dung lượng bộ nhớ; "duyệt hết" = xem lần lượt từng phần tử | 2180 | 0 |
| L04 | scale: def/return, `==`, for, print (4 hàng) | – | 1877 | 0 |
| L05 | 2 bảng: hàm chèn (gán hai biến, `while True`, `x[0]` và `i = 1 if ... else 2`, `is None`, `+=`; 5 hàng) và hàm đo (`[... for k in thu_tu[1:]]`, `max([0] + [...])`, `//`, nối danh sách `[m] + ... + ...`, `list(range(1, n + 1))`; 5 hàng) | "cạnh" = đoạn nối cha với con, định nghĩa ở cảnh `terms` (trước chiều cao); cắt ý ít giá trị để bù (≈ 220 từ) | 2297 | 0 |
| L06 | 3 bảng: `break` + đổi chỗ; `range(len(a) // 2 - 1, -1, -1)` + `list(range(n))`; `[0] * m`, `o[k % m] += 1`, `range(0, n * n, n)` | **P2** Σ d/2^d = 2: nếu gọi tổng là S thì nửa S bằng 1/2 + 1/4 + 1/8 + … = 1 (cả chữ và lời, kèm kiểm số) | 2297 | 0 |
| L07 | scale: import deque, gán ba biến + từ điển, `while hang:`, `popleft()`, `for u, v in (...)`, điều kiện `0 <= u < c and ... not in d` (6 hàng) | **SHOULD**: bfs thêm "cả sáu thành phố đều đã được đánh dấu, nên từ A tới được tất cả"; "đồ thị dày" = có rất nhiều cạnh | 2094 | 0 |
| L08 | scale: `==`, `return` trần, `dem[0] += 1` (danh sách một ô), lời gọi đệ quy, for (5 hàng) | `introduces: cs112_dem0` chuyển sang step bảng | 1931 | 0 |
| L09 | scale: `for _ in range(n - 1)`, số thực và số nguyên (`2.0 ** n`), `int(...)`, `==` cho True/False (4 hàng) | bỏ câu giảng lặp trong lời đọc mã | 1771 | 0 |
| L10 | 2 bảng: `return -1`, `//`, `A[m] == x`; gán ba biến + `list(range(n))`, `max` (3 + 2 hàng) | **SHOULD**: "T(n) ≤ n − 1 với mọi n là lũy thừa của 2" (cả chữ và lời) | 2232 | 0 |
| L11 | scale: import math + `math.isqrt`, `**`, `//` (3 hàng) | bỏ câu giảng lặp | 1746 | 0 |
| L12 | 2 bảng: `len(a) // 2`, cắt `a[:m]`/`a[m:]`, gán ba biến + `[]`, `while t and p`, `pop(0)` + `if ... else` + `append`, `kq + t + p` (6 hàng); `[(i * 7919) % n for ...]` (1 hàng) | **P2** thêm step "Vì sao đúng" cho ba trường hợp (tầng i tốn aⁱ f(n/bⁱ): TH1 mỗi tầng xuống nặng gấp bᵋ > 1, TH2 mọi tầng cùng cỡ × log n tầng, TH3 điều kiện đều đặn cho tổng ≤ f(n)/(1 − c)), kèm kiểm số; cắt ≈ 230 từ ở hook, ôn, cây, pitfalls, verify, quiz | 2287 | 0 |
| L13 | 2 bảng: `break`, đổi chỗ, `j -= 1`; `list(range(n, 0, -1))`, `list(range(n))` | **SHOULD tiêu đề**: đổi "tìm kiếm nhị phân" thành "thuật toán Euclid" (cả `curriculum/cs112.yaml`); "ước chung lớn nhất" định nghĩa ngay ở kinds.0; "tìm tuần tự" định nghĩa tại chỗ | 1963 | 0 |
| L14 | 3 bảng: `not in` + `append`/`pop()`; `enumerate` + `all(... for ...)`; `(n ** (n + 1) - 1) // (n - 1)` | "Omega lớn = ít nhất cỡ" (chữ + lời); "dãy nhị phân" = dãy ba chữ số 0 hoặc 1 | 1915 | 0 |

Ước lượng: 15/15 bài còn 0 mục chưa giảng (mức tự đánh giá; reader chấm lại sau khi dựng). 4 SHOULD đã sửa (L07, L10, L01, L13) và 4 chỗ P2 (L00, L02, L06, L12). Mọi bài ≤ 2300 từ lời đọc (cao nhất L05/L06 2297, L00 2296).

## Sổ screen_code (công cụ chính thức)
- `audit/cs112/ledger_specs_a.yaml`: dịch chỉ số step của cảnh `scale` (bảng chèn trước mã nên mã lùi step) cho L00–L14 bằng regex trên tên khoá; sau đó `audit/cs112/ledger_a.py` ghi lại 59 khối + 15 nguồn lab. Mục cũ không còn khối (khoá `scale` cũ) gỡ bằng `ledger_a.drop_entry` (hàm chính thức của công cụ, không sửa tay bằng script thô).
- Còn FAIL/MISSING/STALE chỉ ở L15–L25 (bài của tác tử khác đang làm song song), không ở L00–L14.

## Cổng (chạy thật, 2026-11-16)
- `tools/lv.py lint` từng bài L00–L14: 0 FAIL, 0 WARN (số PASS: L00 64, L01 43, L02 52, L03 32, … xem nhật ký phiên).
- `tools/lv.py curriculum curriculum/cs112.yaml`: 30 bài, 0 lỗi. `tests/test_e52.py`: 0 FAIL.
- `audit/cs112/verify_cs112.py` (38 PASS, 15 FIX, 0 FAIL), `verify_cs112_a.py` (30 PASS · 0 FAIL: có kiểm ghép nguyên văn khối mã mới L00–L14), `_af2b`, `_fix4`, `_fix4b`, `_p2`: đều 0 FAIL.
- `audit/check_curricula_graph.py`: 0 tham chiếu hỏng, 0 chu trình; mục "VER không PASS" chỉ liệt kê khoá khác, "VER của bài khác: 0".
- `audit/review/lab_gate.py CS112`: 30 PASS · 0 FAIL. `audit/review/arith_scan.py`: 256 phép, 0 FAIL.
- `screen_code.py check --course CS112`: không còn mục nào ở L00–L14 khác PASS (không FAIL/STALE/MISSING/ORPHAN); phần còn lại (L15+ đang được tác tử khác sửa) vẫn đỏ, không thuộc phạm vi này.
- Lint cuối cùng từng bài: L00 64 PASS, L01 43, L02 52, L03 32, L04 27, L05 36, L06 38, L07 33, L08 35, L09 34, L10 36, L11 30, L12 41, L13 29, L14 29 (tất cả 0 FAIL, 0 WARN).

## Việc chưa làm được / lưu ý cho người điều phối
- **Chưa render**: lệnh `tools/lv.py render lessons/cs112/<bài>.yaml` bị bộ phân loại quyền từ chối khi tôi chạy (đề gốc của tôi cấm render; tin nhắn bổ sung của người điều phối không thay đổi được quyền). Do đó chưa kiểm "TRÀN bảng"/chữ đè và chưa xem khung PNG. Cần người điều phối (hoặc người dùng) chạy render cho L00–L14 và xem ≥ 3 khung bài có bảng dài. Bảng rủi ro tràn nhất: L12 bảng 1 (6 hàng, ô "ví dụ" có hai cụm cắt danh sách và ô đọc dài ở hàng `kq.append(...)`), L07 (6 hàng, ô mã dài của `for u, v in (...)`), L14 bảng 2, L03 (6 hàng). Nếu tràn: tách hàng cuối sang step riêng cùng `clear: true` (mỗi bảng tách được vì mỗi hàng đã có câu `say` riêng; chỉ cần nhân đôi câu mở ≥ 8 từ), hoặc rút ô "đọc là".
- Chưa nghe/ASR lại lời mới; các câu mô tả ký hiệu bằng tiếng Việt ("hai dấu sao liền nhau", "hàm lấy lớn nhất") cần ASR/nghe thử.
- Lời đọc bài đã sát trần (L05, L06, L00, L12 ≥ 2287): mọi sửa tiếp theo phải cắt chỗ khác.

## Đợt 2 (chống TRÀN bảng, theo tin điều phối)
- Render lại bị từ chối quyền lần nữa (không đi vòng) nên làm tĩnh: mọi bảng "viết trong mã" tách thành ≤ 4 hàng/step, step sau có `clear: true`. Tách: L00 (5 → 3+2), L03 (6 → 3+3), L05 (hai bảng 5 → 3+2), L07 (6 → 3+3), L08 (5 → 3+2), L12 (6 → 3+3); phần sau không thêm câu mở nên số từ không đổi. Bài sinh từ mẫu (L05, L07) sửa .tpl rồi regen_a.py gen.
- Lint 0/0 cả 6 bài; lời đọc không đổi (L00 2296, L03 2180, L05 2297, L07 2094, L08 1931, L12 2287). Khoá step cảnh scale trong ledger_specs_a.yaml đã dịch, ledger_a.py + drop_entry: screen_code CS112 = PASS 144, FAIL/STALE/MISSING/ORPHAN 0.
- Vẫn cần người điều phối chạy render L00–L14 (không có claim `CS112_Lxx` trong rebuild.claims).
