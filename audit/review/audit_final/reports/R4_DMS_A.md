# R4 DMS L00–L10 (vòng 4, đọc độc lập, P1 chặt): 11/11 bài — ghi lại bởi người điều phối từ tin nhắn của reader (a6abdb5f0b847fd29)

## 1. Tóm tắt
MUST 0/11 vi phạm (đạt). P1=2: 0/11 (mọi bài P1=0). P8=2: 11/11. P9=2: 11/11. spec khớp 11/11. SRT khớp 11/11 (lưu ý: SRT sinh từ `caption` của đặc tả nên khớp là hiển nhiên; âm thật chỉ có asr_report làm chứng). Lab ĐÚNG 11/11. 14/14 khối mã Python trên màn hình chạy khớp. ~70 số tính lại khớp. SHOULD 6. Mất gốc: GẦN 11/11 (tổng 12, một mục 0 ở P1; L07 = 10).
ASR nghe "một" thành "mục" ở 4 câu "bằng một" (L04 ×2, L09 "0 giai thừa bằng 1", L10 "x và y cùng bằng 1") — chưa rõ do ASR hay TTS; cần nghe thử.

## 2. SHOULD
| Bài | Cảnh | Trích | Lý do | Đề xuất |
|---|---|---|---|---|
| L01 | demorgan.0–.1 | "Luật De Morgan có hai vế" … "cả hai vế đều sai" | "vế" hai nghĩa trong cùng cảnh (hai vế của ≡; hai toán hạng của ¬p ∨ ¬q) | "hai phía của dấu tương đương" / "hai thành phần của phép hoặc" |
| L03 | contradiction.1 ① | "phân số tối giản (a, b không cùng chia hết cho 2 — rút gọn trước là được)" | tối giản = không có ước chung > 1, không chỉ "không cùng chẵn" | "không có ước chung lớn hơn 1, nên đặc biệt không cùng chẵn" |
| L05 | quymo.1 | "bao hàm–loại trừ chỉ tốn 3 phép chia" / lời "luôn chỉ là ba phép chia" | với k điều kiện có 2^k − 1 số hạng | thêm "với hai điều kiện (2 và 3)" |
| L07 | equivalence.1 | "Định lý: các lớp tương đương rời nhau và phủ kín tập A" | chỉ phác "rời nhau"; thiếu ý "phủ kín" (a thuộc lớp của a nhờ phản xạ) — CONFIRMED | thêm một dòng "mỗi a thuộc lớp của a vì phản xạ" |
| L09 | pitfalls.1 tiêu đề | "Lỗi 2. Nhân khi số cách ở bước sau thay đổi theo bước trước chọn (sai)" | mơ hồ so với perms.0 (3×2×1 vẫn nhân đúng) | "…thay đổi tuỳ bước trước chọn *cái nào*" |
| L10 | quymo.1 | "1 000 người chia 10 nhóm đều nhau: chỉ còn 49 500 cặp thay vì 499 500" | chỉ đúng khi chỉ cần cặp cùng nhóm — CONFIRMED | thêm "khi chỉ cần so các cặp cùng khoá" |
Khác: L07 quiz.1 (khung 00084) dấu "." lẻ rớt xuống dòng riêng trong hộp tô sáng (P3 nhỏ); L07 P2=1, P3=1 (tổng 10).
Thuật ngữ dùng trước khi định nghĩa / không nhắc lại: "va chạm" (L06 quymo.2, định nghĩa ở pitfalls.2), "phản ví dụ" (L02 verify.0), "khoá băm" (L10 quymo.1), "vét cạn" (L07 quymo, định nghĩa ở L10), "PIN" (L09), "32 bit" (L06).

## 3. Mục chưa giảng (P1 chặt) — nguyên nhân hệ thống
Không bài nào dạy cú pháp Python trong cảnh `quymo`/`practice`; cả khoá dựa vào `requires_ext: PYT:L00–L03` (chuẩn chặt không tính). Chân trang mọi bài "Chấm bằng Git Bash: `bash labs/cham.sh DMS Lxx ten.py`" không được giải thích. Bảng "viết trong mã → đọc là" chỉ có ở L01 example.0, phủ `!`, `&&`, `||`, `>=`, `==`, `!=`, `y % 2` (kiểu C) và không phủ Python.
Số mục chưa giảng (K không có lời giảng + M lời chỉ nói nghĩa chung) theo bài: L00 5, L01 5, L02 4, L03 4, L04 3, L05 4, L06 6, L07 6, L08 6, L09 5, L10 4.
Danh sách theo bài (cảnh → trích):
- L00: quymo.0 `for n in (10, 20):`; `2 ** n`, `10 ** 9`; `range(2 ** n)`, `dong = dong + 1`; practice.2 `int((p == 1 and q == 0) or r == 1)`; practice.1 chân trang `bash labs/cham.sh DMS L00 bang.py`.
- L01: quymo.0 `def dung(x):` `return x <= 0 or x >= 10`; `2 ** 32 // 2` (`//` giảng ở bài 0, không nhắc lại); `**`; `lech = lech + 1`; practice.1 `bash labs/cham.sh DMS L01 …`.
- L02: quymo.0/.1 `for n in (10, 100, 1000):`; practice.2 `[x for x in D if not (điều kiện)][0]`; verify.0 "phản ví dụ"; practice.1 chân trang.
- L03: quymo.0 `for n in (10, 100, 1000):`; `if (a + b) % 2 == 0:`; `range(1, n + 1, 2)`; practice.1 chân trang.
- L04: quymo.0 `for n in (10, 1000, 1000000):`; practice.2 `while tong(n) == sai(n)`; practice.1 chân trang.
- L05: quymo.0 `for n in (100, 10 ** 6):`; `if x % 2 == 0 or x % 3 == 0:`; `10 ** 6`, `n = 10 ** 12`; practice.1 chân trang.
- L06: quymo.0 `for n in (1000, 10000, 100000):`; `dem[o] = dem[o] + 1`; `(n + m - 1) // m`; "va chạm" (quymo.2); "32 bit" (quymo.1); practice.1 chân trang.
- L07: quymo.0 `for n in (9, 30, 100):`; `a % 3 == b % 3 and … not a % 3 == c % 3`; quymo.1 `lop = {}`, `lop.get(x % 3, 0) + 1`, `lop.values()`; practice.2 `all(R(a, c) for a in A for b in A for c in A if R(a, b) and R(b, c))`; "vét cạn"; practice.1 chân trang.
- L08: quymo.0 `for n in (6, 8):`; `hang.index(1) < hang.index(2)`; `from itertools import permutations` / `permutations(range(1, n + 1))`; quymo.1 `sau = {1: [2, 3], …}`, `while san_sang:`, `.pop()`, `.append(w)`, `dem[w] = dem[w] - 1`; practice.2 `not any(c != a and … for c in S)`; practice.1 chân trang.
- L09: quymo.0 `for do_dai in (4, 6):`; `10 ** do_dai`, `62 ** do_dai`, `10 ** 9`; practice.2 `product(..., repeat=k)`, `permutations(..., k)`; "PIN"; practice.1 chân trang.
- L10: quymo.0 `for n in (8, 100, 1000):`; quymo.1 "dùng khoá băm"; practice.2 `hang[i] + hang[i + 1]`; practice.1 chân trang.

## 4. Gợi ý sửa của reader
Bảng "viết trong mã → đọc là" cho `for … in (…)`, `range`, `%`, `**`, `//`, `def`/`return`, `.get`, `.index`, `while`, `.pop()`/`.append()` ngay trước/trong mỗi cảnh có mã; giải thích chân trang chấm bài tại L00 và lặp một dòng ở mọi bài; hoặc chuyển phần mã nặng (L07, L08) sang de.md và chỉ giữ kết quả trên màn hình; nhắc lại định nghĩa thuật ngữ dùng lại.
