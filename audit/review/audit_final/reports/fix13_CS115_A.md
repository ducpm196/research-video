# fix13 CS115 L00–L11 (vòng r13, 6 việc nhỏ sau item-verifier) — 2026-11-18

CHỈ đổi chữ trên màn hình (`show`/`focus`). KHÔNG câu `say` nào đổi: số từ lời đọc giữ nguyên (L00 2298, L01 2299, L02 2300, L03 2297, L04 2298, L05 2298, L06 2296, L07 2298, L08 2300, L09 2300, L10 2277, L11 2297); băm `lv.sentences` không đổi.

## Việc đã làm
1. L06, L07: ô "đọc là" của hàng `def f(x, y):` thêm "`x**2` là x mũ 2 (hai dấu sao liền nhau là lũy thừa)" (bảng R2, trước lần `**` đầu tiên).
2. L08 Sarrus: ba đường đi lên tô BA màu (đỏ, tím, xanh dương) cả ở ô trong ma trận lẫn ở ba tích trong dòng "lên (ba màu)", cùng màu từng cặp; đường đi xuống màu lục. Đã xem khung 76.
3. L05: ô "đọc là" của `delta = vet * vet - 4 * dt` giải nghĩa "vết (tổng hai số trên đường chéo) bình phương trừ 4 lần định thức". Đã xem khung 122.
4. L11: bảng R3 thêm hàng thứ 4 (vẫn ≤ 4 hàng): `"[" + ", ".join(str(x) for x in g) + "]"` — in list Fraction: `Fraction(0, 1)` in ra `0` qua `int(x)` hoặc `str(x)`, nối bằng `", ".join(…)`; ví dụ in `[0, 0]`.
5. Cả 12 bài: `focus` câu đầu của practice.0 thành `[["1.2", 2, 3], "1.3", "1.4"]` → hai ghi chú "Git Bash…" và "kho…" được viền cùng hàng "tạo tệp" khi đọc câu đầu (số mục focus vẫn 3 = số câu).
6. Tuỳ chọn: `white-space:nowrap` cho ô mã gãy dòng: L00 (R3 hàng f-string), L01 (hai hàng `sum(...)`, `print(f"Pytago…")` — đã xem khung 145), L02 (hàng `sum(A[i][k] …)`), L05 (hàng `(vet - math.isqrt(25)) // 2`), L07 (hàng comprehension `round(...)`); L00 SVG nhãn "w = 3,4: tổng 0,16" dời (x 868, y 351) để chân chữ không đè đường đứt đỏ; L03 hàng `if/elif/else` ghi chú "ra = hạng A, rm = hạng ma trận mở rộng".

## Bài đã đổi
L00–L11 (cả 12: việc 5). Riêng: L00, L01, L02, L03, L05, L06, L07, L08, L11 (việc 1–4, 6); L04, L09, L10 chỉ việc 5.

## Cổng
- lint L00–L11: 0 FAIL, 0 WARN. `verify_cs115_af2`: 184 PASS · 0 FAIL. `screen_code CS115`: PASS 59, FAIL/STALE/MISSING/ORPHAN 0 (không đổi chỉ số step nên không đổi khoá sổ). Số từ lời đọc ≤ 2300 (không đổi).
- `tools/lv.py render` L00–L11: cả 12 bài 0 vấn đề (không tràn). Khung đã xem: L01 145, L05 122, L08 76.
