# fix4_CS112_B — sửa CS112 L15–L29 theo R2_CS112_B (2026-11-15)

## Tiến độ
XONG 15/15 bài (L19 không phải sửa). Không chạy build/tts/asr/git/docker.

## Bài đổi → cần DỰNG LẠI (lời đọc/màn hình đổi)
L15, L17, L18, L20, L21, L22, L24, L25, L26, L27, L28, L29.
Chỉ đổi `de.md` lab (video không đổi, chỉ cần lab_gate): L16, L23. L19: không đổi.
Số từ lời đọc sau sửa: L15 2058 · L16 1757 · L17 1845 · L18 1871 · L19 1980 · L20 2058 · L21 2096 · L22 2095 · L23 2260 · L24 ~2285 · L25 1887 · L26 2280 · L27 1895 · L28 2283 · L29 2295 (đều ≤ 2300; mọi câu 4–38 từ).

## P1 (4 chỗ + cú pháp lab)
- L20: "tăng hẳn" định nghĩa ngay ở hook (mỗi số lớn hơn số đứng ngay trước, không cho bằng); hook bỏ "nền của các công cụ so sánh tệp" (không nguồn) → "bài toán liên quan tới việc so sánh tệp".
- L21: prereq thêm step "mặt phẳng toạ độ" (trục, điểm (a, b), đường thẳng, nửa mặt phẳng; A(16, 0) nằm trên trục); thuật ngữ E52 `cs112_toa_do` (symbols.CS112.yaml, `introduces`).
- L28: bẫy 2 (đếm số mục từ a đến b = b − a + 1, từ 5 đến 3 ra −1), bẫy 5 (log₂(n¹⁰) = 10 log₂ n khác (log₂ n)¹⁰), bẫy 9 (điều kiện đều đặn a·f(n/b) ≤ c·f(n), c < 1) nay có định nghĩa tại chỗ.
- L29: bỏ IllegalArgumentException khỏi màn hình (thay bằng "phép so sánh tự viết mâu thuẫn → hàm có thể báo lỗi", có lời đọc); "commit" = lần ghi thay đổi vào kho mã.
- Cú pháp lab (khối "Cú pháp cần dùng" trong de.md, qua audit/cs112/gen_labs_b.py): L16 (Fraction, combinations, sorted key), L17 (key=lambda, combinations), L18 (dict, biến đếm, global), L20 (tập con, combinations), L22 (Fraction, min key), L23 (global, biến đếm), L24 (key=lambda, list.index, lần ngược), L25 (hợp–tìm: cha/size, không dùng all(union...)).

## SHOULD CONFIRMED (kiểm bằng mã: audit/cs112/verify_cs112_fix4b.py, tính lại độc lập)
- L24 negative/rounds: thêm "chu trình âm tới được từ S" (màn hình + lời + check phản ví dụ S→A 1, B→C 1, C→B −3).
- L24 scale: 4 967/49 641 → 2 455/25 182 (đúng định nghĩa "chỉ nới cạnh tới đỉnh chưa chốt"; định nghĩa ghi trong bài; số cũ 4 967/49 641 ghi kèm là số cạnh được xét). Hàm mới `dijkstra_relax_count` trong af2b_calc.py.
- L25 scale: 196/54 624/637 269 → 195/54 676/637 336 (sắp TĂNG như Kruskal; `sort_compares(desc=False)`, L16 giữ giảm dần).
- L18 scale: "Python mặc định ~1000 tầng; ngôn ngữ khác mức khác nhưng hữu hạn" (lời không đọc tên Python theo lexicon CS112).
- L28 bẫy 16: n = 16 (120 so sánh so với 64); bẫy 18: nguồn ở đỉnh giữa cạnh 5 và một cạnh 3 (6 so với 8).
- L21 vertex: thêm "miền có đỉnh (như mọi biến không âm)".

## SHOULD khác
- L15: ghi quy ước phá hoà (đường nhỏ nhất từ điển) ở màn hình + lời; pitfalls "cận yếu đi (42 thay vì 53)" + check `tsp5_child_lb`.
- L17: lời đọc quiz "bắt đầu 4, kết thúc 7".
- L22: bỏ "xoay chỉ cỡ vài lần số ràng buộc" (→ "trong các bài ngẫu nhiên đo ở bảng, 2 tới 16 lần"), bỏ "Khachiyan chậm hơn trong thực tế"; tiêu đề cảnh hạ giọng. Số bổ đề CLRS ở header `source`: CHƯA kiểm được, không sửa.
- L27: "không chạy nổi" → "báo cáo bỏ qua; ngoại suy 2138·3⁵ ms ≈ 9 phút, chạy được nhưng lâu"; P7: mục tiêu 3 "Mô tả bộ kiểm thử năm nhóm…", mục tiêu 4 "Nêu các mục của nhật ký…" (sửa mục tiêu, không thêm lab).
- L28 P7: mục tiêu 1 "Mô tả sáu nhóm dạng bài…", mục tiêu 3 "Nêu mười chín bẫy…".
- L29: pitfalls "hơn 67 triệu (ví dụ dựng được: 2 mũ 26)"; stage3 "đúng khi vào hàm gộp"; intuition đọc thêm 3 mốc 2015/2021/2025; quiz câu 2 đọc hàng "chỉ kiểm thử với mảng thật lớn" (>500 triệu đơn vị nhớ).
- Hình P3 mới (sinh từ mã, kiểm bằng máy): L18 cây F(5) ghi nhớ (audit/cs112/memo_tree_svg.py: 9 lời gọi so với 15); L20 truy vết LCS tô ô (bảng + lời); L25 hợp–tìm trước/sau (dsu_svg.py); L26 sơ đồ P ⊆ NP, NP-đầy đủ (pnp_svg.py, ghi rõ giả định P ≠ NP). KHÔNG làm: L24 Dijkstra từng bước dạng hình đồ thị (bảng d sau mỗi lần chốt đã có sẵn) — đề xuất làm sau nếu cần.
- Cắt để ≤ 2300 từ: L24 (ba câu verify/prereq), L28 (7 câu/đoạn thừa ở prereq, quiz, practice, recap), L29 (recap, stage1, stage3).

## Công cụ mới/đổi (chỉ phần B)
audit/cs112/regen_b.py (extract/gen mẫu L17, L18, L21, L23–L26, giữ LF), wc_say.py, memo_tree_svg.py, dsu_svg.py, pnp_svg.py, verify_cs112_fix4b.py; af2b_calc.py (thêm tsp5_child_lb, dijkstra_relax_count, sort_compares(desc)); gen_labs_b.py (de.md); verify_cs112_af2b.py (L24d, L25c đổi số); tools/registry/symbols.CS112.yaml (+cs112_toa_do); audit/review/screen_code/CS112.yaml (sha khối L24 negative 1 0). Mẫu `*.tpl.yaml` đã sửa: L17, L18, L21, L24, L25, L26 (bài sinh qua regen_b.py gen).

## Số liệu cổng thật (cả khoá CS112, chạy 2026-11-15)
- lv.py lint L15–L29: 15/15 bài 0 FAIL 0 WARN.
- lv.py render (bài đổi L15, 16–18, 20–22, 24–29): 0 vấn đề mỗi bài (L24 và L25 từng tràn/đè nhãn, đã sửa).
- verify_cs112_fix4b: ALL PASS (10 mục); verify_cs112_af2b: PASS 0 lỗi; verify_cs112: PASS 38, FIX 15, FAIL 0.
- lab_gate CS112: 30 PASS · 0 FAIL. test_e52: 0 FAIL. arith_scan: 245 phép, 0 FAIL.
- lv.py curriculum curriculum/cs112.yaml: 30 bài, 0 lỗi. check_curricula_graph: 0 lỗi.
- screen_code check --course CS112: 97 khối, PASS 144, FAIL/STALE/MISSING/ORPHAN 0 (một STALE L24 negative 1 0 đã cập nhật sha).

## Chưa làm / ghi chú
- Không có người đọc lại; P1 dự kiến 15/15 nếu 4 vá được chấp nhận.
- `asr_reviewed` cho câu mới chưa có; mục `asr_reviewed` cũ của L28 bẫy 16 đã rút gọn theo câu tách.
- Tên "Dijkstra/Kruskal…" vẫn chỉ trên màn hình. Tệp bài sinh L17–L26 phải sửa qua mẫu rồi `regen_b.py gen`.
