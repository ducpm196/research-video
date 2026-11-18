# fix10 CS112 L15–L29 (sửa theo R7_CS112_B) — 2026-11-17

Không chạy build/tts/asr/git/docker. Không đổi bài ngoài L15–L29. Có chạy `tools/lv.py render` (chỉ khung hình) và các cổng. Lưu ý vận hành: máy rất tải (nhiều tiến trình dựng của đội khác) nên mỗi lần `lint` mất 1–2 phút; vài vòng lặp nền của tôi chạy chồng nhau làm tệp kết quả tạm bị trộn, nên số liệu cuối lấy từ lần chạy lại từng bài (xem "Cổng").

## 1. Git Bash (mục chung 15 bài)
Mỗi bài, ở cảnh `practice`, thêm MỘT step trước step "Kết quả mong đợi" (step có `clear: true`, step sau cũng `clear: true`): bảng 3 hàng "đọc trước: việc | làm thế nào | gõ trong Git Bash" cùng khuôn/wording như CS115 (`fix6_CS115_A.md`) và DMS:
- mở Git Bash: cửa sổ gõ lệnh trên Windows (đi kèm Git for Windows); vào thư mục bài làm, bấm chuột phải vào chỗ trống, chọn Open Git Bash here;
- chạy: `python <tên>.py` (các dòng `print` hiện ngay bên dưới);
- chấm: `bash labs/cham.sh CS112 Lxx <tên>.py` (`bash` chạy tệp chấm `labs/cham.sh` với khoá, mã bài, tên tệp; in ĐÚNG khi mọi dòng khớp kết quả mong đợi).
Tên tệp đúng từng bài (tsp4.py, tui.py, lich.py, doi_tien.py, chuoi.py, lis_lcs.py, qhtt.py, donhinh.py, nhanh.py, ngan_nhat.py, cay_khung.py, np_khoi.py, mini_btl.py, tong_on.py, timsort_mo_phong.py). Lời đọc 2 câu, không có từ Latin (lexicon báo "Bash"/"Windows" nên đã bỏ khỏi lời, tên chỉ nằm trên màn hình); chân trang cũ rút gọn (phần giải thích `bash`/`cham.sh` đã chuyển sang bảng) và câu chấm bài trong lời đọc rút từ 4 còn 3 câu (đã bỏ một mục `focus` tương ứng). Không dùng "như đã học".

## 2. Mục riêng (5) và yếu cùng họ
| Bài | Mục | Sửa |
|---|---|---|
| L15 | "4!", "19!" | ô trên màn hình "n! = n · (n−1) · (n−2) ⋯ 1 (n giai thừa), ví dụ 4! = 24" + một câu lời đọc ở hook (`focus` thêm 1 mục); `assumes` thêm `dots` |
| L17 | "[1, 4)" | câu mở của prereq nói "ngoặc vuông gồm điểm đầu, ngoặc tròn không gồm điểm cuối" + ô chú thích "[a, b) = từ a tới b…" |
| L18 | "Θ(n)" | lời "…Theta của n, tức số bước tăng cùng bậc với n: gấp đôi n thì gấp đôi số bước" + ô Θ(n) trên màn hình; `introduces: [bigTheta]` |
| L26 | "bit" | step mới đầu cảnh `sym` (trước sym.0 và pseudo.0): bảng "bit = một chữ số 0 hoặc 1 khi viết số ở hệ hai (14 → 1110: 4 bit)" và hàng `W.bit_length()` (14 → 4, 14000 → 14, 10⁹ → 30 bit; đã tính bằng Python); bước bảng `bit_length` cũ ở gợi ý bỏ; "chứng chỉ" định nghĩa tại sym.0 ("bằng chứng ngắn cho đáp án có") |
| L28 | "ε" | ô trên màn hình "ε (đọc: ép-xi-lon) là một số dương nhỏ tuỳ ý, ví dụ 0,1" + câu lời đọc trước quiz.2 (`focus` cập nhật); "tổng Sigma" thêm "(cộng lại nhiều số hạng)" ở hook |
| L16 | Σ | "(∑ = cộng lại mọi số hạng: p₁x₁ + p₂x₂ + p₃x₃)" trong sym.0 (viết bằng LaTeX) |
| L19, L20, L24, L25 | Θ | ô "Θ = cùng bậc tăng" tại chỗ Θ dùng lần đầu (L19: n gấp 10 thì n³ gấp 1000; L20: n gấp đôi thì n² gấp 4) |
| L22 | `<=` | đổi thành chữ "nhỏ hơn hoặc bằng 24"; công thức khối Klee–Minty đưa lên màn hình Đề: c_j = 2^(n−j); A_ij = 2^(i−j+1) nếu j < i, 1 nếu j = i, 0 nếu j > i; b_i = 5^i (đã chạy lại bằng `af2b_calc.klee_minty(4)`: c = [8, 4, 2, 1], b = [5, 25, 125, 625], A khớp); `introduces: [sub2]` cho A_ij |
| L23 | ⌈ ⌉, "lá", log₂, "khoá" | ô tại chỗ: "log₂ n = số lần chia đôi n để còn 1", "lá = nút ở cuối cây, không có nút con", "⌈x⌉ = làm tròn lên (⌈9,49⌉ = 10)", "khoá (giá trị dùng để sắp xếp)" |
| L24 | "chu trình âm", "32 bit tràn" | ô tại negative.1 ("đường đi vòng về chỗ cũ mà tổng trọng số nhỏ hơn 0") và ở lỗi 3 ("số nguyên 32 bit: 32 chữ số 0/1, lớn nhất 2³¹−1; cộng 1 thì tràn, quay vòng sang số âm nhỏ nhất") |
| L29 | "CAV 2015", "phản ví dụ" | "(hội nghị quốc tế về kiểm chứng bằng máy)"; "phản ví dụ (ví dụ cụ thể làm kết luận sai)" |

## 3. SHOULD
- L23 scale: "từ n = 2 000" thành "từ khoảng n = 1 000" (chữ và lời đọc: "từ khoảng 1000 phần tử đã vượt giới hạn mặc định 1000 tầng").
- L24 scale: nhãn cột "nới mọi cạnh, dừng khi không đổi (tối đa n − 1 vòng)".
- L25 SVG hợp–tìm (`audit/cs112/dsu_svg.py` → `fig/L25_DSU.svg`, rồi `regen`): nhãn chia hai dòng và đặt dưới hình (không đè nút 5, không ra ngoài viền; khung cao 590).
- L26 SVG Venn (`audit/cs112/pnp_svg.py` → `fig/L26_PNP.svg`): nhãn "NP: kiểm được chứng chỉ nhanh" đặt trong elip (y = 82); nhãn P và NP-đầy đủ xuống dòng, nằm trọn trong elip con.
- L22: công thức Klee–Minty lên màn hình (xem trên).

## 4. Số từ lời đọc (đo như `wc_say.py`)
L15 2249; L16 1971; L17 2081; L18 2125; L19 2116; L20 2095; L21 2271; L22 2269; L23 2292; L24 2294; L25 2085; L26 2294; L27 1938; L28 2296; L29 2292 (mọi bài ≤ 2300). Để bù lời thêm vào, đã cắt các ý ít giá trị (câu "Bài sau" rút gọn, câu "Điều cần mang theo", một số vế phụ trong bẫy; L28 bỏ vài vế; L29 bỏ cụm "như bài tổng ôn đã nói" ở cả chữ và lời; L23/L24/L26/L28 cắt 20–40 từ). Không cắt quiz/quy mô/Tự làm.
`asr_reviewed`: so từng mục với lời đọc sau khi sửa (script so sánh): 15/15 bài "0 mục lệch"; không sửa chữ câu nào nằm trong `asr_reviewed`.

## 5. Sổ screen_code CS112
Bước Git Bash chèn trước khối "Kết quả mong đợi" nên khoá khối đầu ra dịch +1 step ở cảnh practice (L15 2→3; L16 2→3; L17 2→3; L18 1→2; L19 1→2; L20 1→2; L21 hai khối 2→3 và 3→4; L22 2→3; L23–L29 1→2). Sửa bằng Edit từng khoá trong `audit/review/screen_code/CS112.yaml` (không script, sha không đổi vì chữ khối không đổi).

## 6. Công cụ / tệp đổi
`audit/cs112/fix6b.py` (thêm `ensure_clear`, `clear_next`), `fix10b_gitbash.py`, `fix10b_items.py`, `fix10b_items2.py`, `fix10b_cut.py`, `fix10b_cut2.py`, `fix10b_svg.py`, `fix10b_say2.py`, `fix10b_lint1.py` (mỗi script chạy một lần). Bài sinh từ mẫu (L17, L18, L21, L23, L24, L25, L26): sửa `audit/cs112/src/*.tpl.yaml` rồi `regen_b.gen`; các bài khác sửa YAML trực tiếp. Lab không đổi.

## 7. Cổng (chạy thật, 2026-11-17, lần cuối sau mọi sửa)
- `tools/lv.py lint` từng bài L15–L29: 0 FAIL, 0 WARN. Lỗi lint gặp và đã sửa: L16 (∑ gõ Unicode lẫn LaTeX → dùng `$\sum$`; từ "Bash", "Windows" trong lời đọc → bỏ khỏi lời), L15 (`dots` → thêm vào `assumes`), L18 (`introduces: [bigTheta]` + focus câu cuối), L22 (A_ij → `introduces: [sub2]` + giải nghĩa "ô hàng i, cột j"), L24 (câu có ghi chú mới thiếu `focus` → thêm).
- `tools/lv.py render` từng bài (lượt cuối): 0 vấn đề ở cả 15 bài (L15 113 khung … L29 106 khung). Lỗi render gặp và đã sửa: L24 cảnh `scale` tràn vì tiêu đề cột dài làm cột 2 gập dòng → tiêu đề "nới mọi cạnh (tối đa n − 1 vòng)" (cụm "dừng khi không đổi" chuyển lên dòng chú thích) và nhãn hàng ngắn lại. Đã xem PNG: `out/CS112/L17/frames/00093.png` (bước Git Bash), `L25/frames/00041.png` (SVG hợp–tìm sau sửa: nhãn hai dòng dưới hình, không đè nút 5, trong khung), `L24/frames/00018.png`, `L23/frames/00018.png`, `L22/frames/00107.png`.
- `tests/test_e52.py`: 0 FAIL. `tools/lv.py curriculum curriculum/cs112.yaml`: 30 bài, 0 lỗi.
- `audit/cs112/verify_cs112*.py` (6 tệp): 38 PASS · 15 FIX · 0 FAIL; `_a` 30 PASS; `_af2b` PASS; `_fix4` ĐÚNG; `_fix4b` ALL PASS; `_p2` 37 PASS.
- `audit/review/screen_code.py check --course CS112`: 97 khối — PASS 144 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0.
- `audit/review/lab_gate.py CS112`: 30 PASS · 0 FAIL. `audit/review/arith_scan.py`: 258 phép, 0 FAIL.

## 8. Đề xuất requeue và số mục chưa giảng ước còn lại
Requeue cả 15 bài CS112 L15–L29 (lời đọc và khung đổi ở mọi bài). Mục chưa giảng ước còn lại: 0 ở cả 15 bài (tự đánh giá; reader đo lại). Rủi ro còn: L18 "ngăn xếp lời gọi" ở twoways chỉ có định nghĩa ở cảnh scale (M yếu, chưa đổi); các bài sát trần 2300 từ (L23, L24, L26, L28, L29).

## 9. Lưu ý vận hành
- Máy rất tải nên lint/render mỗi bài mất 1–2 phút; một số vòng lặp nền của tôi chạy chồng nhau (hai ba bản cùng ghi `/tmp`), không ảnh hưởng tệp bài. Tôi đã dừng các tác vụ nền của mình bằng TaskStop. Hai lần định dừng cưỡng bức các tiến trình python/bash còn sót đều bị bộ phân loại quyền từ chối (đúng, vì có thể chạm tiến trình dựng của đội khác); không đi vòng. Không tiến trình ngoài phạm vi CS112 bị chạm.
- Câu lời đọc mới (Git Bash 2 câu, bit, ε, `n!`, Θ, ngoặc nửa mở) chưa qua tai/ASR.
