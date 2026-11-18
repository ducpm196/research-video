# fix6 CS112 L15–L29 (sửa theo chuẩn P1 chặt, không có reader vòng 4 riêng) — 2026-11-16

Tiến độ: L15–L17 xong; L18–L20 xong; L21–L23 xong; L24–L26 xong; L27–L29 xong; đợt 2 (định nghĩa thuật ngữ còn lại, `clear` chống tràn, sổ screen_code) xong. KHÔNG chạy build/tts/asr/audit_all/git/docker; có chạy `tools/lv.py render` (chỉ khung hình).

## Cách làm
- Khuôn chung với `fix6_CS112_A.md` và DMS: bảng 3 cột "viết trong mã | đọc là | ví dụ" đặt NGAY TRƯỚC khối mã/gợi ý (step riêng, `clear: true`); một câu mở + một câu `say` cho mỗi hàng (hoặc một câu gộp khi lời đọc cũ đã giảng nghĩa), `focus` từng hàng. Lời đọc không nói tên lệnh Latin (tả bằng tiếng Việt), tên thật chỉ hiện trong bảng.
- Đa số mã Python ở L15–L29 chỉ nằm ở lab (de.md), còn trên màn hình chỉ có đầu ra; mục chưa giảng nằm ở (a) mã giả có từ khoá `for/while/if/return/break/==/!=/<=` và `a[i]` (L16, L17, L18, L23, L24, L25, L28), (b) lệnh nhắc trong cảnh Tự làm: đề và ô "Nếu kẹt" (L15, L16, L17, L18, L19, L21, L22, L25, L26, L28, L29), (c) chân trang `bash labs/cham.sh …` (cả 15 bài), (d) thuật ngữ dùng trước khi định nghĩa.
- Công cụ: `audit/cs112/fix6b.py` (sửa giữ nguyên kiểu xuống dòng LF/CRLF, `patch_cham`, `clear_next`, `ensure_clear`, `regen`) và các script ghi lại từng đợt `audit/cs112/fix6b_l16.py … fix6b_l29b.py`, `fix6b_gloss.py`, `fix6b_clear1.py`, `fix6b_clear2.py` (đã chạy MỘT lần; không chạy lại được vì kiểm duy nhất chỗ thay). Bài sinh từ mẫu (L17, L18, L21, L23, L24, L25, L26): sửa MẪU `audit/cs112/src/*.tpl.yaml` rồi `regen_b.gen`; các bài còn lại sửa YAML trực tiếp. Lab `labs/CS112/L15–L29` KHÔNG đổi.
- Không thêm mục vào `tools/registry/symbols.CS112.yaml` (cùng lý do như bản A: tránh buộc bài sau `assumes`); thuật ngữ định nghĩa tại chỗ bằng chữ trên màn hình + lời đọc. Né cụm "chữ số nhị phân" (đã thuộc `cs112_bit` giảng ở L09) bằng "chữ số khi viết ở hệ hai".
- `asr_reviewed`: so với bản làm việc trước khi sửa và với `git show HEAD:`: không mất mục hợp lệ nào do tôi; mọi mục còn khớp một câu `say` (kiểm bằng script so sánh, 15/15 bài "0 mục lệch"). Các câu nằm trong `asr_reviewed` không bị sửa chữ (ví dụ câu ôn Θ/Ω của L23, câu "Thuật toán đơn hình…" của L22). L24: sinh lại từ mẫu thêm 1 mục hợp lệ (câu "Lần ngược theo các cạnh đó…") mà bài cũ thiếu; L19/L22/L23/L28 có mục "mất so với HEAD" nhưng đã mất từ các vòng trước (câu đã đổi chữ), không phải do đợt này.

## Danh sách mục chưa giảng đã tìm (tự đọc từng step) và cách xử lý
| Bài | Mục chưa giảng (P1 chặt) | Xử lý |
|---|---|---|
| L15 | `itertools.permutations`, `range(1, 4)`, `INF = float("inf")` (Đề); "thứ tự từ điển" (scale); "vét cạn" dùng ở hook; chân trang chấm | bảng 3 hàng trước Đề; gloss "như xếp chữ"; "thử hết (vét cạn)" ở hook; chân trang |
| L16 | mã giả `for/if w[i] <= Rem/x[i] = 1; Rem = Rem - w[i]/break`; "mã giả"; `Fraction(p, w)`, `itertools.combinations`; "đống" (scale); chân trang | bảng 4 hàng trước mã giả + định nghĩa "mã giả"; bảng 2 hàng trước Đề; gloss "đống"; chân trang |
| L17 | mã giả `last = -1 // …`, `for`, `s[k] >= last`, `f[k]`, ghi chú `//` (dễ nhầm phép chia); `chon(ds, khoa)`, `s >= last`, `combinations`; chân trang | bảng 4 hàng; đổi `//` thành ngoặc; bảng 3 hàng trước Đề; chân trang |
| L18 | mã giả hai cách (`memo[n] != -1`, `return`, gán, `dp[0] = 0; dp[1] = 1`, `for i = 2..n`, ghi chú `//`); `dp[a - c]`, `1 + min(dp[a - c])`, `==` (gợi ý); "đệ quy thô"; "ngăn xếp" | bảng 5 hàng; bảng 3 hàng trước gợi ý; định nghĩa tại hook và ở ô giới hạn; chân trang |
| L19 | `for` lồng 3 tầng, `j = i + độ dài - 1`, `p[i-1] * p[k] * p[j]` (gợi ý); chân trang | bảng 3 hàng trước gợi ý; chân trang |
| L20 | chỉ chân trang (đề và gợi ý không có cú pháp mã; "tiền tố", "tìm kiếm nhị phân" đã có lời giải nghĩa tại chỗ) | chân trang |
| L21 | `Fraction(a, b)` (Đề); `a1*x + b1*y = c1`, `det = a1*b2 - a2*b1`, `x = (c1*b2 - c2*b1) / det` (gợi ý); chân trang | bảng 1 hàng trước Đề; bảng 3 hàng trước gợi ý (kèm ví dụ số đã tính lại: det = −2, x = 9/2); chân trang |
| L22 | `don_hinh(c, A, b, quy_tac)`, `Fraction`; `-c`, `(hệ số ở cột vào) * hàng ra` (gợi ý); "đỉnh kề"; chân trang | bảng 2 hàng trước Đề; bảng 2 hàng trước gợi ý; gloss "đỉnh kề" (chữ trên màn hình; câu lời đọc nằm trong asr_reviewed); chân trang |
| L23 | mã giả partition/quicksort (`a[hi]`, `lo - 1`, `for j = lo .. hi - 1`, `<=`, `return`, `if lo < hi`, đệ quy, ghi chú `//`); "biến toàn cục", "độ sâu đệ quy" (gợi ý/Đề); "ngăn xếp" (scale); chân trang | bảng 5 hàng; định nghĩa tại chỗ; chân trang; cắt lời ~150 từ để bù |
| L24 | mã giả `while`, `for mỗi cạnh u → v`; tiêu đề cảnh "bất đẳng thức tam giác" (chưa giảng); chân trang | bảng 2 hàng; đổi tiêu đề cảnh thành "không cạnh nào còn nới được"; chân trang; cắt lời để bù |
| L25 | mã giả hợp–tìm (`cha[x] != x`, `find` tự gọi, `ra == rb`, `return`, ghi chú `//`); `union` trả `False`, `!=` (gợi ý); chân trang | bảng 4 hàng; bảng 2 hàng trước gợi ý; đổi `//` thành ngoặc; chân trang |
| L26 | `W.bit_length()` (gợi ý); "tổng tập con"; chân trang | bảng 1 hàng; gloss "tổng tập con"; chân trang; cắt lời để bù |
| L27 | "ms", "KB", "ngôn ngữ thông dịch", "bậc tăng" (chữ trên màn hình); chân trang | gloss tại chỗ; chân trang |
| L28 | mã giả `if n == 1: return`, `for i = 1..n`, `f(nửa trái, n/2)`, ghi chú `//`; `math.log2` (gợi ý); chân trang | bảng 3 hàng; gloss `math.log2(8)` là 3; chân trang; cắt lời để bù |
| L29 | `s[n:n + 2] = [s[n] + s[n + 1]]` (lát cắt), "cờ" (gợi ý); "O(n)" trên màn hình; "JDK"; chân trang | định nghĩa tại hộp gợi ý kèm ví dụ s = [30, 20, 10], n = 1 → [30, 30]; "O(n)" → "cỡ n"; gloss JDK; chân trang |

## Theo bài (đã đổi — để requeue; số mục chưa giảng ước còn lại)
| Bài | Nguồn sửa | Số từ lời đọc (trước → sau) | Chưa giảng ước |
|---|---|---|---|
| L15 | YAML | 2058 → 2205 | 0 |
| L16 | YAML (CRLF giữ nguyên) | 1757 → 1951 | 0 |
| L17 | mẫu + gen | 1845 → 2047 | 0 |
| L18 | mẫu + gen | 1871 → 2089 | 0 |
| L19 | YAML | 1980 → 2096 | 0 |
| L20 | YAML (CRLF) | 2058 → 2075 | 0 |
| L21 | mẫu + gen | 2096 → 2251 | 0 |
| L22 | YAML | 2095 → 2270 | 0 |
| L23 | mẫu + gen | 2260 → 2296 | 0 |
| L24 | mẫu + gen | 2285 → 2299 | 0 |
| L25 | mẫu + gen | 1887 → 2065 | 0 |
| L26 | mẫu + gen | 2280 → 2295 | 0 |
| L27 | YAML | 1895 → 1918 | 0 |
| L28 | YAML (CRLF) | 2285 → 2299 | 0 |
| L29 | YAML (CRLF) | 2295 → 2299 | 0 (cạnh giới hạn) |

Ước lượng: 15/15 bài còn 0 mục chưa giảng (tự đánh giá; reader sẽ chấm lại sau khi dựng). Rủi ro còn lại ("yếu"): thuật ngữ nhắc lại một dòng ở bài xa (ví dụ "hàng đợi ưu tiên", "đống nhị phân" đã có dòng ôn ở prereq của L15, L24, L25; "đệ quy" ở L23, L25, L28 được giảng nghĩa ngắn trong bảng nhưng không có mục sổ riêng). L23, L24, L26, L28, L29 sát giới hạn 2300 từ (đo bằng tách theo khoảng trắng như `audit/cs112/wc_say.py`): sửa tiếp phải cắt thêm.

## Chuẩn xác (mục 2)
- `lint` chạy thật các `checks:` trong bài (L15 39, L24 26 phép, L29 48 PASS…): tất cả PASS; `audit/cs112/verify_cs112.py` 38 PASS · 15 FIX (ghi nhận từ bản thảo, 0 FAIL), `verify_cs112_a` 30 PASS, `_af2b` PASS, `_fix4` ĐÚNG, `_fix4b` ALL PASS, `_p2` 37 PASS · 0 FAIL.
- Tự tính lại độc lập các số dùng trong bảng mới: L16 (24 : 15 = 1,6; 31,5), L18 (dp[8] = 2 từ dp[7], dp[4], dp[2] = 2, 1, 2 cho mệnh giá 1, 4, 6), L19 (1500 = 10·30·5), L21 (det = 1·1 − 3·1 = −2; x = (9·1 − 18·1)/(−2) = 9/2), L23 (hai bên chốt: 3 phần tử và 2 phần tử), L26 (14 = 1110 → 4 bit; 14000 → 14 bit; 2^39 < 10^12 ≤ 2^40), L29 (s = [30, 20, 10], n = 1 → [30, 30]). Không số nào sai.
- L24 hình Dijkstra: đọc toạ độ/nhãn trong `audit/cs112/fig/L24_G24*.svg` (G24, G24TREE, G24NEG, G24QUIZ): trọng số khớp với đồ thị trong lời đọc và `checks` (S→A 4, S→B 1, B→A 2, A→C 1, B→C 5, C→D 3, B→D 8; đồ thị âm 2, 3, −2; đồ thị quiz 1, 4, 2, 6, 3). Không phát hiện sai nên không sửa hình.
- L22 số bổ đề CLRS ("Bổ đề 29.7", chỉ ở header `source`, không lên màn hình/lời): không có sách để kiểm; đã BỎ số, ghi "chương Quy hoạch tuyến tính; số bổ đề chưa kiểm được với sách nên không ghi". Không bịa số khác.
- Chỗ nhảy chứng minh: đọc lại các bước chứng minh L15 (cận dưới), L16/L17 (đổi chỗ), L19 (hệ thức đoạn), L22 (hàng z = chứng chỉ), L23 (n! ≥ (n/2)^(n/2); C(n) = 2(n+1)H_n − 4n tại n = 6, 1000), L24 (chốt đỉnh), L26–L27 (T(n) = 3^(n−1)); không thấy bước nhảy cần sửa.

## Cổng (chạy thật, 2026-11-16)
- `tools/lv.py lint` từng bài L15–L29: 0 FAIL, 0 WARN.
- `tools/lv.py curriculum curriculum/cs112.yaml`: 30 bài, 0 lỗi. `tests/test_e52.py`: 0 FAIL.
- `audit/cs112/verify_cs112*.py` (6 tệp): như trên, 0 FAIL.
- `audit/review/screen_code.py check --course CS112`: 97 khối — PASS 144 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0. Sổ `audit/review/screen_code/CS112.yaml` cập nhật bằng Edit từng mục (không script): bảng chèn trước mã nên khoá bước dịch chỉ số (L15 practice 1→2; L16 rule 0→1, practice 1→2; L17 rule 0→1 kèm sha mới, practice 1→2; L18 twoways 0→1 (2 khối, sha mới); L21 practice 1→2 và 2→3; L22 practice 1→2; L23 idea 2→3 (sha mới); L24 dijkstra 0→1; L25 dsu 0→1 (sha mới); L28 example 0→1 (sha mới)) và 7 mục `twin_of` của nguồn đối chiếu.
- `audit/review/lab_gate.py CS112`: 30 PASS · 0 FAIL. `audit/review/arith_scan.py`: 256 phép, 0 FAIL. `audit/check_curricula_graph.py`: thoát 0 (0 VER lỗi).
- `tools/lv.py render` từng bài L15–L29 (không nằm trong hàng dựng còn lại): lượt đầu tràn ở cảnh `practice`/`rule`/`twoways`/`idea` vì bảng mới chèn trước step cũ; đã thêm `clear: true` cho step sau bảng và step gợi ý ("Nếu kẹt"), rút gọn bảng L23 (idea); lượt cuối **0 vấn đề ở cả 15 bài**. Xem khung PNG: `out/CS112/L18/frames/00017.png` (bảng mã giả hai cách), `00022.png` (khối mã sau bảng), `out/CS112/L23/frames/00018.png` (bảng partition, trước khi rút gọn: sát đáy; đã rút), `out/CS112/L24/frames/00018.png` (bảng while/for), `out/CS112/L22/frames/00107.png` (bảng gợi ý).

## Việc chưa làm được / lưu ý cho người điều phối
- Cần dựng lại (build + tts + asr) cả 15 bài; lời đọc mới (nhất là câu "đọc là" trong bảng và 4 câu chân trang) chưa qua tai/ASR. Câu có "trừ một", "mũ", "hệ hai", "lát cắt" cần xem ASR; chưa thêm `asr_reviewed` cho câu mới.
- Lab không đổi; `labs/CS112/*/de.md` vẫn có "Cú pháp cần dùng (nếu chưa gặp)" riêng.
- Bài có mẫu: nếu sau này sinh lại từ mẫu, nhớ rằng mẫu L24 giờ chứa mục `asr_reviewed` mà bài cũ thiếu (đã đồng bộ).
- Tiêu đề cảnh L24 `verify` đổi (id không đổi).
- Tệp thay đổi: `lessons/cs112/L15…L29_*.yaml`, `audit/cs112/src/L17,L18,L21,L23,L24,L25,L26_*.tpl.yaml`, `audit/review/screen_code/CS112.yaml`, `audit/cs112/fix6b*.py`.
