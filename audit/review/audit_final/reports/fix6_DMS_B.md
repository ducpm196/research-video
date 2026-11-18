# fix6 DMS L11–L20 (sửa trước khi có báo cáo reader vòng 4; chuẩn P1 chặt) — 2026-11-16

Tiến độ: L11–L13 xong; L14–L16 xong; L17–L19 xong; L20 xong. Không chạy build/tts/asr/render/git/docker.
Khoá này CHƯA có báo cáo reader vòng 4 cho L11–L20: tôi tự đọc từng bài như người mất gốc (mọi `show`, `say`, quiz, gợi ý Tự làm) rồi áp công thức của `fix6_DMS_A.md`.

## Cách làm
- Hạ tầng mới `audit/dms/af2/fix6b.py` (dùng lại `fix6lib.py`, KHÔNG sửa `af2lib.py`/`fix6lib.py`):
  - `hint_parts2`: như `hint_parts` nhưng câu kết "Lời giải nằm trong thư mục thực hành…" được nói SAU các hàng của bảng gợi ý.
  - `asr_keep(lid)`: khôi phục mục `asr_reviewed` thêm tay sau AF2 (không có trong `base/`). Mục lấy nguyên văn từ bài/mẫu TRƯỚC khi sinh lại, lưu ở `audit/dms/af2/fix6b_asr_keep/Lnn.json`.
- Bẫy asr_reviewed (đã kiểm bằng cách sinh lại baseline TRƯỚC khi sửa gì): sinh lại từ `lNN.py` làm mất mục thêm tay ở L11 (1), L13 (1), L14 (4), L15 (1), L19 (1), L20 (3); ở L17 mục nằm trong MẪU `L17_cay.tpl.yaml` (2) nhưng bài đã dựng thiếu chúng (nay bài và mẫu cùng có, câu còn tồn tại trong lời đọc). Sau khi sửa: so từng bài với bản cũ (bản sao ở scratchpad) — không mất mục hợp lệ nào (L14 thêm `drop_asr` cho câu "nhớ chia số mũ cho p trừ 1" đã bị thay từ trước; L20: 19/19 mục, không mất không thừa).
- Mọi bài: bảng "viết trong mã → đọc là → ví dụ" đặt NGAY TRƯỚC khối mã ở cảnh `quymo` (thay bước "cú pháp mới" đặt SAU mã ở L12, L17, L18); gợi ý Tự làm có bảng cho mã xuất hiện trong gợi ý (L12–L16, L20); chân trang `bash labs/cham.sh …` có giải thích bằng chữ + lời đọc 4 câu (`patch_cham`, cả 10 bài). Lời đọc không nói tên hàm/từ khoá (lexicon): tả bằng tiếng Việt, tên thật chỉ hiện trong bảng.
- Sửa CẢ script vá `audit/dms/af2/l11..l20.py` và bài `lessons/dms/L11..L20` (bài sinh lại từ `base/` bằng script, chạy lại ổn định). L16–L18: sửa script (mẫu `audit/dms/src/L16–L18*.tpl.yaml` chỉ đổi ở L17: khôi phục 2 mục asr_reviewed), ghép hình như cũ.
- Lab (`labs/DMS/L11–L20`) và `curriculum/dms.yaml`: không đổi (so sánh từng tệp).

## Mục chưa giảng đã liệt kê khi đọc (P1 chặt) và cách xử lý
Cột "trước" = số mục tôi đếm trên bản hiện có; "sau" = ước còn lại.

| Bài | Mục chưa giảng (cảnh → trích) | Cách xử lý | Trước | Sau |
|---|---|---|---|---|
| L11 | quymo: `for n in (10, 100, 1000):`; `range(n + 1)`, `range(n + 1 - a)`; `dem = 0`, `dem = dem + 1`; `(n + 2) * (n + 1) // 2`; `print(...)` và chữ `C(n+2, 2)` trong dấu nháy; practice.2 chân trang chấm bài | bảng 5 hàng trước mã; chân trang | 6 | 0 |
| L12 | quymo: `from itertools import permutations`, `from math import comb, factorial`; `for n in (6, 8)`; `vet = 0`; `permutations(range(n))`/`p`; `all(p[i] != i …)`, `(-1) ** k`, `sum(… for k …)` (giảng SAU mã), `print … 'vet can'`; practice.3 `1000 // (3 * 5)`; practice.1 "hàm toàn ánh" (giảng ở bài 6, không nhắc); chân trang | 2 bảng (4 + 5 hàng) trước mã, bỏ bước cú pháp đặt sau; bảng 1 hàng cho gợi ý; định nghĩa toàn ánh tại chỗ | 11 | 0 |
| L13 | quymo: `for a, b in ((…),…)`, `10 ** 6 + 3`, `x, y, buoc = a, b, 0`, `while y != 0`, `x, y, buoc = y, x % y, buoc + 1`, `min(a, b)`, `print(… 'gcd' …)`; practice.3 `a, b = b, a % b`, `x0, x1 = x1, x0 - q * x1`, `q = a // b`, `((a % n) * (b % n)) % n`, `(1 + 1000) % 7`; pitfalls.1 `%`, `==`, "C, Java"; chân trang | 2 bảng (4 + 3) trước mã; bảng 5 hàng cho gợi ý; bỏ `==` khỏi lỗi 1, giảng `%` | 13 | 0 |
| L14 | quymo: `for e in (100, 10 ** 6, 10 ** 12)`, `kq, a, x, phep = 1, 3, e, 0`, `while x > 0`, `if x % 2 == 1`, `kq * a % 1000007`, `phep = phep + 1 + x % 2`, `x // 2`, `pow(3, e, 1000007)`, `kq == pow(…)`, print; practice.3 `if e % 2 == 1`, `kq * a % n`, `e // 2`, `e % (p - 1)`; chân trang | 2 bảng (4 + 5) trước mã; bảng 4 hàng cho gợi ý | 14 | 0 |
| L15 | quymo: `for p, q in ((3, 11), …)`, `n, d, thu = p * q, 2, 1`, `while n % d != 0`, `d = d + 1`, print; practice.3 `(e * d) % L == 1`, `pow(x, e, n)`; chân trang | bảng 5 hàng trước mã; bảng 2 hàng gợi ý | 8 | 0 |
| L16 | quymo: `for n in (11, 1001)`, `bac = [0] * n`, `range(u + 1, n)`, `bac[u] = bac[u] + 1`, `sum(1 for b in bac if b % 2)`, `n * (n - 1) // 2`, print; "đồ thị đầy đủ" dùng trước định nghĩa (quiz); "vét cạn" dùng trước định nghĩa; practice.3 `sum(1 for e in canh if v in e)`; chân trang | 2 bảng (4 + 3) trước mã; định nghĩa đồ thị đầy đủ và vét cạn tại chỗ; bảng 1 hàng gợi ý | 10 | 0 |
| L17 | quymo: `from itertools import combinations`, `def la_cay(n, tap)`/`return`, `list(range(n))`, `for u, v in tap`, `nhan[u]`, `[a if x == b else x for x in nhan]`, `len(set(nhan)) == 1`, `combinations(combinations(range(n), 2), n - 1)`, `sum(1 for t in … if la_cay(n, t))`, print, `**` (đang giảng SAU mã); chân trang | 2 bảng (5 + 5) trước mã, bỏ bước cú pháp đặt sau | 12 | 0 |
| L18 | quymo: `def so_mau`, từ điển `mau = {}`, `v[0]`/`v[1]`, `{… for u in mau if … and …}`, `min(c for c in range(2 * n) if c not in ke)`, `max(mau.values()) + 1`, `[(s, i) for i in range(n) for s in 'ab']`, print (giảng SAU mã); verify "phản chứng" (giảng ở bài 3); "đồ thị hai phía" (practice, chưa định nghĩa); chân trang | 2 bảng (4 + 4) trước mã, bỏ bước cú pháp đặt sau; "phản chứng" và "hai phía" định nghĩa tại chỗ (cảnh vương miện) | 13 | 0 |
| L19 | quymo: `for m in (365, 10 ** 6, 2 ** 32)`, `khong_trung, n = 1.0, 0`, `while khong_trung > 0.5`, `khong_trung * (m - n) / m`, `round(n / m ** 0.5, 2)`, print; sym: "đồng khả năng"; practice.1 "hoán vị", "điểm cố định" (bài 12); chân trang | bảng 6 hàng trước mã; "đồng khả năng", "hoán vị/điểm cố định" nói bằng lời thường tại chỗ | 9 | 0 |
| L20 | prereq: "bit" dùng trước định nghĩa; stage3 "TLS" viết tắt; practice.3 `comb(k, 2)`; chân trang | bit định nghĩa ở cảnh ôn (chữ + lời); TLS có chú thích; bảng 1 hàng gợi ý | 4 | 0 |

Bài không có mã trong cảnh quy mô (L20, bài hành trình) chỉ có 4 mục như trên. Mã trong `de.md` và lời giải của lab không đổi; cú pháp ở đó đã có đoạn "Cú pháp cần dùng (chưa học ở đâu trước đó…)" riêng trong `de.md`.

## Chuẩn xác (SHOULD / điều kiện) đã sửa
- L12 "Tổng đó luôn bằng 1" → "bằng 1 với mọi m từ 1 trở lên, vì khai triển một trừ một mũ m ra 0" (chữ + lời); verify "Không còn kiểu nào khác" thiếu bước: thêm "mỗi nhóm đổi mũ có ít nhất 2 người, mà 4 chỉ tách thành 2+2 hoặc một nhóm 4" (ghi chú + lời).
- L13 "chia hai vế của đồng dư" thiếu điều kiện: thêm "chỉ chia được khi số chia và mô-đun không có ước chung nào lớn hơn 1"; "số bước tỉ lệ với số chữ số" → "số bước nhiều nhất tỉ lệ…"; lỗi 1 bỏ `== -1` khỏi màn hình.
- L14 "khi và chỉ khi gcd = 1" thiếu chiều ngược: thêm "nếu a x ≡ 1 thì mọi ước chung của a và n chia hết 1".
- L17 bổ đề lá: đỉnh cuối đường dài nhất có thể kề đỉnh liền trước → "ngoài đỉnh liền trước nó"; bước quy nạp thêm "bỏ lá vẫn liên thông vì không đường đi nào giữa hai đỉnh khác đi qua lá".
- L18 dòng "2 000 000 đỉnh" của bảng là ngoại suy (code chỉ chạy n = 10, 100) → ghi "(suy ra theo quy luật, chưa chạy)"; hai câu lý do lặp ở cảnh K5 được thay bằng "sẽ suy ra từng bước ngay sau đây" (có điều kiện ≥ 3 cạnh).
- L19 cận "256 bit" → "nếu hàm băm không có điểm yếu" (chữ + lời).
- Tự tính lại độc lập bằng Python (`dmsB/recalc.py`, 36 nhóm kiểm, 0 sai): mọi số/đáp án quiz ở L11–L20 (D_n, thời gian ước lượng, 88 bước Euclid, 10/27/53 phép nhân, 2^2048 có 617 chữ số, RSA 4→31→4, bảng đếm cây, màu vương miện n/2, ngày sinh 23/1178/77164, 585 năm, 122 295, 0,0116…). Không số nào sai. Không có SHOULD nào về nhãn hình phát hiện thêm ngoài dòng ngoại suy của L18.

## Số từ lời đọc (≤ 2300)
L11 1956 · L12 2297 · L13 2188 · L14 2283 · L15 2148 · L16 2135 · L17 2153 · L18 2290 · L19 2285 · L20 2299. (L12/L14/L18/L19/L20 sát trần: đã cắt câu lặp ít giá trị — xem dưới.)
Cắt để giữ trần: L12 bỏ câu "Dòng tính tổng…" (đã có trong bảng) và câu "Ví dụ 8 và 15…" (còn trên màn hình); L14 bỏ "Cả ba lần kết quả khớp phép tính có sẵn"; L18 rút gọn lời cảnh vương miện, bỏ hai câu lặp ở cảnh K5, bỏ "Đồ thị vẫn chỉ cần đúng 2 màu…" và "Cận bậc lớn nhất cộng một…" (còn trong hộp trên màn hình); L19 bỏ ba câu ít giá trị và rút gọn lời kết; L20 bỏ "Hôm nay ta đi qua năm chặng…" và rút gọn lời kết.

## Cổng (chạy thật, 2026-11-16)
- `tools/lv.py lint` từng bài L11–L20: 0 FAIL, 0 WARN.
- `tools/lv.py curriculum curriculum/dms.yaml`: 21 bài, 0 lỗi. `tests/test_e52.py`: 0 FAIL.
- `audit/dms/verify_dms.py`: 324 PASS · 0 FAIL (lab 21, cảnh quy mô chạy thật 22).
- `audit/review/screen_code.py check --course DMS`: 72 khối — PASS 95 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0 (sổ cập nhật bằng `ledger_sync` của script, công cụ chính thức).
- `audit/review/arith_scan.py DMS`: 22 phép, 0 FAIL. Chạy KHÔNG đối số bị lỗi `yaml.scanner.ScannerError` ở một bài của khoá khác đang được tác tử khác sửa dở (không phải bài DMS); cần chạy lại toàn bộ khi các tác tử kia xong.
- `audit/review/lab_gate.py DMS`: 21 PASS · 0 FAIL (196 lab được bài tham chiếu). `audit/check_curricula_graph.py`: 0 tham chiếu hỏng, 0 chu trình, 0 VER lỗi. Lab `labs/DMS/L11–L20` không đổi so với trước (so sánh từng tệp), nên đầu ra `mong_doi.txt` và `labs/cham.sh` giữ nguyên.

## Bổ sung sau thông báo "TRÀN bảng" (tách bảng)
- `fix6b.read_steps` (bọc `fix6lib.read_steps`, ý mở thứ hai 8 từ), `flat`, `hint_steps2`. Mọi bảng cách đọc quymo ≤ 4 hàng/step: L11 (3+2), L12 (4, 3+2), L13 (4, 3), L14 (4, 3+2), L15 (3+2), L16 (4, 3), L17 (3+2, 3+2), L18 (4, 4), L19 (3+3). Gợi ý Tự làm: L13 tách hai step (3 + 2 hàng, step sau `clear`, kèm dòng "Lời giải ở …"); các gợi ý khác ≤ 4 hàng.
- Kiểm bằng mã trên bài sinh: không bảng nào > 4 hàng; mọi step đứng ngay sau bảng cách đọc đều `clear: true`.
- Số từ sau tách: L11 1965 · L12 2296 · L13 2197 · L14 2292 · L15 2157 · L16 2135 · L17 2171 · L18 2290 · L19 2294 · L20 2299 (L12 cắt thêm 4 cụm ngắn).
- `tools/lv.py render` thử một lần (L12) bị bộ phân loại quyền TỪ CHỐI; không đi vòng. Cần người điều phối dựng/xem khung.

## Lưu ý cho người điều phối
- Chưa nghe/ASR/render lại: lời đọc mới cần dựng lại ASR; các hàng bảng đọc mã mới nhiều chữ (đặc biệt L17 hàng 5, L18 hàng 3–4, L12 hàng "all", L14 hàng "if x % 2 == 1") cần xem ≥ 3 khung PNG sau khi dựng (cột "đọc là" dài có thể tràn). Mỗi bảng ≤ 6 hàng/khung; L12, L13, L14, L17, L18 có HAI bước bảng liên tiếp (clear) trước mã.
- Bài đã đổi (requeue): L11, L12, L13, L14, L15, L16, L17, L18, L19, L20.
- L17: nay `asr_reviewed` có 2 mục ở CẢ mẫu và bài (trước đây chỉ ở mẫu): ASR cũ đã dùng cho dựng trước có thể đã ghi nhận; không cần xử lý thêm.
- Sinh lại bài từ `lNN.py` giờ giữ asr_reviewed qua `fix6b.asr_keep`; mục mới thêm tay sau này phải ghi vào `fix6b_asr_keep/Lnn.json` (hoặc `repl`) nếu muốn sống sót qua lần sinh lại.
