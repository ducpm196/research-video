# wp5_cs112_a — nâng CS112 L00–L14 lên chuẩn AF2 (2026-11-14)

## Tiến độ
- 15/15 bài L00…L14 đã sửa (id đúng `curriculum/cs112.yaml`; L15+ không chạm). Mỗi bài: `af2: true` + `covers`, mục tiêu mới cho cảnh quy mô và cảnh Tự làm, cảnh `scale` (đếm/đo thật ở ≥ 2 cỡ n) đặt trước `pitfalls`, cảnh `practice` (lab `labs/CS112/Lxx`, `pause`, kết quả mong đợi hiện nguyên văn + lệnh `cham.sh`) đặt trước `recap`, `lint` 0 FAIL 0 WARN.
- Bài sinh từ mẫu (L05, L06, L07, L14): sửa MẪU `audit/cs112/src/Lxx_*.tpl.yaml`, sinh lại bằng `audit/cs112/regen_a.py gen Lxx` (hình SVG trích một lần từ bài cũ ra `audit/cs112/fig/Lxx_*.svg`; kiểm vòng khứ hồi: mẫu cũ + hình = bài cũ, `git diff` rỗng). Các bài còn lại (L00–L04, L08–L13) sửa trực tiếp YAML bằng công cụ vá giữ CRLF.

## Việc đã làm mỗi bài (tóm tắt, số liệu thật)
| Bài | Cảnh quy mô (đo thật bằng mã Python hiện trên màn hình) | Lab (labs/CS112/Lxx) |
|---|---|---|
| L00 | so sánh hai vòng lồng: n = 1000 → 501 500, n = 2000 → 2 003 000 (×4); n = 10⁶ ≈ 5·10¹¹ (500 giây nếu 10⁹ phép/giây, số minh hoạ) | `dem_vong.py`: đếm chạy thân/so sánh vòng j = i+1..n |
| L01 | A = 1000n thua B = n² dưới n = 1000, thắng từ đó (n = 100, 1000, 10⁵) | `nguong.py`: tìm c, n₀ cho 2n²+10n+30 |
| L02 | n², 2ⁿ, n! ở n = 10, 20, 30 và thời gian ở 20/30/60 (10⁹ bước/giây, số minh hoạ) | `xep_hang.py`: "lần đầu hơn" khác "mãi mãi hơn" |
| L03 | mảng động 1 023 / 131 071 lần chép; chèn đầu mảng 499 500 / 4 999 950 000 lần dời (n = 10³, 10⁵) | `mang_dong.py`: chép gấp đôi vs thêm 10 ô; chèn đầu danh sách liên kết |
| L04 | đệ quy 500 tầng chạy, 5000 tầng tràn ngăn xếp (giới hạn mặc định 1000 của Python); hàng đợi ngây thơ 499 500 / 4 999 950 000 lần dời | `ngan_xep.py`: ngoặc, hàng đợi vòng, hậu tố |
| L05 | BST chèn tăng dần cao 999/1999, chèn giữa-trước cao 9/10 (n = 1000, 2000) | `cay_nhi_phan.py`: dựng BST, duyệt, chiều cao, bắt cây hỏng |
| L06 | dựng đống mảng tăng dần 992 / 99 990 lần đổi (n = 10³, 10⁵); ô băm dài nhất 1 vs n | `bam_dong.py`: băm dò tuyến tính 11 ô + đống lớn nhất |
| L07 | BFS lưới 100×100 và 1000×1000: lần nhìn 4n, khoảng cách 198/1998; ma trận kề n² vs danh sách n+2m | `do_thi.py`: danh sách kề, BFS, DFS, vùng liên thông |
| L08 | Tháp Hà Nội chạy thật 1 023 / 1 048 575 lần chuyển; thời gian ước 17 phút/12 ngày/34 năm/585 tỉ năm | `the_nguoc.py`: thế ngược giấy bút hai hệ thức, kiểm bằng mã |
| L09 | công thức đóng 2ⁿ−1 bằng số thực lệch từ n = 60 (tính dần số nguyên luôn đúng) | `ham_sinh.py`: hàm sinh T(n)=4T(n−1)+1, kiểm hệ số bằng mẫu số |
| L10 | tìm nhị phân 11 → 21 lời gọi, tìm lớn nhất 1 999 → 1 999 999 (n = 10³ → 10⁶) | `dem_loi_goi.py`: hệ số 2 vs hệ số 1, tìm nhị phân tệ nhất |
| L11 | T(n)/n = 5, 6, 7, 11 ở n = 2¹⁶, 2³², 2⁶⁴, 2¹⁰²⁴ | `doi_bien.py`: W(n)=√n·W(√n)+3n |
| L12 | sắp xếp trộn 8 415 / 1 493 143 lần so sánh (n = 10³, 10⁵) so với n log₂ n và n² | `dinh_ly_tho.py`: tra định lý thợ ba hệ thức, kiểm bằng tỉ số |
| L13 | chèn tệ nhất 499 500 / 1 999 000 (×4), tốt nhất 999 / 1 999 (×2) | `giam_de_tri.py`: Euclid, chèn đếm so sánh, kiểm trùng bằng sắp xếp trước |
| L14 | cây hoán vị 13 700 → 986 410 nút (n = 7 → 9); 8 và 10 quân hậu có tỉa 2 057 và 35 539 nút | `quay_lui.py`: hoán vị không phần tử đứng yên, có/không cắt tỉa |

## Cổng (số thật, 2026-11-14)
- `tools/lv.py lint` từng bài L00–L14: 0 FAIL 0 WARN.
- `audit/cs112/verify_cs112_a.py` (mới): 30 PASS · 0 FAIL — ghép nguyên văn khối mã trên màn hình ở cảnh `scale`, chạy thật, so khối kết quả; chạy lời giải mỗi lab = `mong_doi.txt`.
- `tools/lv.py curriculum curriculum/cs112.yaml`: 30 bài, 0 lỗi. `audit/check_curricula_graph.py`: 0 vấn đề. `tests/test_e52.py`: 0 FAIL.
- Sổ screen_code CS112: 56 mục mới (khối mã `run` chạy thật + khối kết quả `output of:` + nguồn lab `Lxx_lab`) điền bằng `audit/cs112/ledger_a.py` từ `ledger_specs_a.yaml`; kết quả `screen_code.py check --course CS112`, `lab_gate.py CS112`, `arith_scan.py`, `lv.py render`: xem mục "Cổng cuối" bên dưới.

## P1 / thuật ngữ
Giảng tại chỗ bằng một câu lời thường trong bài đã thêm: thuật toán (L00), bất đẳng thức, tử/mẫu của phân số (L01), số mũ/lũy thừa (L00), "đa thức", "hàm mũ", ε (L02), phép gán (L03), phân thức (L09). Không thêm mục `term:` vào `symbols.CS112.yaml` (để không làm bài L15+ của tác tử song song báo E52 giả); bài CS112 đã khai `assumes` đúng như cũ. P1 dự kiến: ≥ 90% bài đạt 2 (các bài đều có bước ôn nền `prereq` nhắc lại khái niệm bài trước và định nghĩa ký hiệu bằng `introduces`).

## Mục không làm / còn mở (nêu rõ)
- Chưa chạy người đọc độc lập; P1/P8 là dự kiến.
- Tên riêng không đọc trong lời (lexicon CS112: Python, Euclid không đạt ASR): lời đọc của cảnh mới nói "một ngôn ngữ lập trình, tên hiện trên màn hình", "thuật toán tìm ước chung lớn nhất"; các câu `say` mới là câu TTS mới → cần dựng + ASR lại (người điều phối). `asr_reviewed` của các câu đã đổi được bỏ khi lint báo E30 (L00, L03).
- Mã giả (pseudo) cũ của bài (vòng `for (i = 1; …)`, `node.next = head`, …) giữ nguyên là mã giả kiểu C đã có trong sổ screen_code; chỉ mã Python MỚI (cảnh scale và lab) chạy thật.
- Tốc độ 10⁹ bước/giây, 1 bước chuyển/giây (Tháp Hà Nội) là số minh hoạ, đã ghi "(số minh hoạ)" trên màn hình và `source`.
- Độ dài lời đọc: L00 2 288 từ (đã cắt ~220 từ cũ để vừa), L12 2 212 từ; còn lại < 2 100. Đề xuất: L06 (băm + đống, 2 077 từ) và L12 (2 212 từ) là hai bài nặng nhất — nếu người đọc thấy quá dài thì tách phần băm khỏi phần đống (cuối khoá, không đánh số lại).
- `labs/CS112/Lxx/loi_giai.py` dùng chú thích tiếng Việt có dấu trong mã (UTF-8; chạy được qua `cham.sh`).

## Tệp đã thêm/đổi (phạm vi mình)
- Bài: `lessons/cs112/L00…L14_*.yaml` (L05/L06/L07/L14 sinh từ mẫu); mẫu `audit/cs112/src/L05_cay, L06_bam_dong, L07_do_thi, L14_quay_lui .tpl.yaml`.
- Lab: `labs/CS112/L00…L14/{de.md,mong_doi.txt,loi_giai.py}`.
- Công cụ/kiểm: `audit/cs112/{verify_cs112_a.py, ledger_a.py, ledger_specs_a.yaml, regen_a.py, frames_index_a.py}`, `audit/cs112/fig/L05_*.svg, L06_*.svg, L07_*.svg, L14_*.svg`.
- Sổ: `audit/review/screen_code/CS112.yaml` (chỉ thêm mục khối L00–L14 và nguồn `Lxx_lab`).
- KHÔNG đổi: `curriculum/cs112.yaml` (không có trường `objectives` ở giáo án), `symbols.CS112.yaml`, `lexicon_vi.CS112.yaml`, mọi tệp CS115.

## Cổng cuối
- `audit/review/screen_code.py check --course CS112`: 88 khối, PASS 129 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 (gồm cả mục của phần L15+ của tác tử khác).
- `audit/review/lab_gate.py CS112`: 22 PASS · 0 FAIL (mọi lab L00–L14 được bài tham chiếu; lời giải chạy thật qua `labs/cham.sh`, đối chứng âm đạt).
- `audit/review/arith_scan.py`: 243 phép tính, 0 FAIL.
- `tools/lv.py render` L00–L14: 0 vấn đề (lần đầu L07, L10, L11 báo tiêu đề cảnh xuống 2 dòng → đã rút gọn 3 tiêu đề, render lại sạch; L12 rút gọn cho an toàn). Đã xem bằng mắt khung scale của L00, L07, L14 và khung kết thúc L00.
- Độ dài lời đọc sau cùng: L00 2 287 · L01 1 877 · L02 1 876 · L03 1 826 · L04 1 692 · L05 2 009 · L06 2 077 · L07 1 789 · L08 1 739 · L09 1 547 · L10 2 074 · L11 1 660 · L12 2 212 · L13 1 806 · L14 1 640 (từ).
- Chưa chạy (đúng chỉ dẫn): build/tts/asr/audit_all/git/docker; các câu `say` mới cần người điều phối dựng và nghe ASR.

## Sửa theo reader (R_WP5_CS112_A.md, 2026-11-14)
**MUST (2/2):** L04 tiêu đề `scale` → "hàng đợi dời hàng tỉ lần" (4 999 950 000 ≈ 5 tỉ); L08 mã `chuyen` lời gọi thứ hai → `chuyen(n - 1, b, a, c, dem)` (chạy lại có kiểm luật: n = 3 xong ở cọc C đủ 3 đĩa, 7 nước, không lần nào đặt đĩa lớn lên đĩa nhỏ; số đếm 1023 / 1 048 575 không đổi).
**P1 (4/4):** L05 giảng "cây con" (terms), "suy biến" (degenerate); L07 giảng "láng giềng" (sym), "chu trình", "vùng liên thông", "đồ thị có hướng" (dfs); L09 giảng "chuyển vế", "quy đồng", "đa thức" tại chỗ; L14 giảng "hoán vị" ở hook. L05 thêm P2: vì sao AVL cao Θ(log n) (số nút tối thiểu 1, 2, 4, 7, 12, 20: gấp đôi sau chừng hai tầng, có `checks`) và cách đổi con trỏ khi xoay trái (cả lời đọc lẫn chữ trên màn hình).
**SHOULD:** L00 `scale` đổi sang đúng vòng của ví dụ chính (j từ n−y đến y: 252 001 và 1 004 001 lần, 10⁶ → ≈250 giây, hơn 4 phút) và lời đọc "ví dụ chính"; L00 lỗi 3 "tăng chậm, cùng cỡ lôgarit" (khớp cảnh sums). L07 "bốn số in ra" + giải thích lần nhìn = 4n (kể cả hướng ra ngoài lưới) so với n + 2m. L14 một quy ước đếm "nút" (kể cả gốc): `prune` nay nói 17 nút (16 lần đặt) và 341 nút/256 lá khi không kiểm; `scale` so với số nút không tỉa (n^(n+1) − 1)/(n − 1) = 19 173 961 và 11 111 111 111, thay cho n^n (số lá). L03 giải thích n(n − 1)/2 (lần chèn thứ k dời k − 1) và nêu kiểu danh sách của chương trình chính là mảng động. L02 lỗi 3 viết lại thành câu độc lập. L06 thêm xoá khỏi bảng băm dò tuyến tính (ô "đã xoá", không để trống). Số nhóm bằng dấu cách trong `say`: viết liền (L03, L06, L08, L13, L14; quét lại 15 bài không còn chỗ nào). L09 `equation` tách bước ghép/chia thành hai step (hết chạm khung), lời đọc "x chia cho tích của 1 trừ x và 1 trừ 2x". Lab L08, L09, L11, L12: đề (de.md và màn hình) không ghi sẵn công thức đóng/đáp số trường hợp; nhãn dòng in đổi thành "cong thuc dong" (L08, L09; sửa `loi_giai.py`, `mong_doi.txt`, de.md, màn hình đồng bộ).
**Không sửa (có lý do):** `pause` 240–600 giây của cảnh practice (đổi sẽ thành khoảng lặng rất dài trong video; thời gian làm lab đã ghi ở de.md); bảy hàm ở hook L02 chỉ hiện (đổi sẽ thêm lời đọc dài); nhãn hệ số L05 cỡ 22 px (nằm trong hình sinh `treesvg.py`, đọc được ở toàn màn hình); P6 L06 (tụ cụm, đổi m) và hệ số tăng mảng L03 chỉ nêu một phần; video mp4/srt cũ (người điều phối dựng lại, các câu `say` mới/đổi cần ASR).
**Cổng sau sửa:** lint 15/15 bài 0 FAIL 0 WARN; `verify_cs112_a.py` 30 PASS · 0 FAIL; `lv.py render` 15/15 bài 0 vấn đề; `screen_code.py check --course CS112` 94 khối PASS 141 · FAIL 0 · STALE 0; `lab_gate.py CS112` 30 PASS · 0 FAIL; `arith_scan` 243 phép, 0 FAIL; `tests/test_e52.py` 0 FAIL; `lv.py curriculum` 30 bài 0 lỗi. Lời đọc (từ): L00 2 292 · L01 1 877 · L02 1 876 · L03 1 877 · L04 1 692 · L05 2 111 · L06 2 111 · L07 1 861 · L08 1 737 · L09 1 588 · L10 2 074 · L11 1 660 · L12 2 212 · L13 1 805 · L14 1 660 (đều ≤ 2 300).
Bài sinh từ mẫu đã sửa ở mẫu rồi `regen_a.py gen` (L05, L06, L07, L14).
