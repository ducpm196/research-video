# Đọc mẫu độc lập đợt D — phần 1 (11 bài), 2026-11-10

Người đọc: tác tử AI, chỉ đọc, không xem `audit/review/full_review_c/*`. Đã đọc toàn bộ `title`, `objectives`, mọi `show` (cả chữ trong SVG), `say`, `checks`, quiz của 11 bài; mục giáo án `curriculum/<khoá>.yaml`; `audit/cas/sources_L08.md`, `audit/clc/sources_L12.md` (các khoá khác không có tệp nguồn trùng số bài). Mọi con số hiện hoặc đọc ra đã tính lại bằng Python (`.venv`, gồm cả gọi `tools/checklib.py` cho 8 ô số, `bnk_reconcile`, và chạy lại mô phỏng M/M/1 ra 49,6). Không thấy lượt nhắc khoá khác (mã hoặc tên) trong phần người học thấy/nghe và giáo án của 11 bài (grep tay; trường `source`/`requires_ext` bỏ qua).

| Bài | Mức (MUST/SHOULD) | Cảnh/bước | Phát hiện (trích nguyên chữ trong bài) | Bằng chứng (phép tính Python / nguồn / dòng YAML) | Tin cậy (cao/vừa) |
|---|---|---|---|---|---|
| CS115 L21 | MUST | `metrics` (tiêu đề cảnh), `objectives` bài + giáo án | Tiêu đề cảnh: “Bốn chỉ số: mỗi cái là một xác suất có điều kiện”; mục tiêu: “Tính tỉ lệ đúng, độ chuẩn xác, độ phủ, F1 và đọc chúng như xác suất có điều kiện” | F1 = 2PR/(P+R) là trung bình điều hoà, không phải xác suất; tỉ lệ đúng là P(đúng), không có điều kiện. Chính bảng của cảnh ghi nghĩa tỉ lệ đúng là “đúng bao nhiêu phần”, chỉ precision/recall có dạng P(·∣·). `lessons/cs115/L21_danh_gia_phan_loai.yaml` dòng 89 (title), dòng 16 (objective). Phần thân đúng nên có thể hạ xuống SHOULD; câu khẳng định thì sai | cao |
| CS115 L21 | SHOULD | `verify` lời đọc; `in_ai`; `pitfalls` lỗi 3 | “độ chuẩn xác chính là xác suất hậu nghiệm ta đã tính bằng định lý Bayes”; “chọn ngưỡng trên tập kiểm định”; màn hình “đường cong ROC và diện tích AUC” | “hậu nghiệm”, “định lý Bayes”, “tập kiểm định” không được giảng lại trong bài (phần ôn chỉ định nghĩa P(A∣B) và tập kiểm tra). ROC/AUC không được giải nghĩa, lời đọc lại không nói hai tên này. Dòng 182, 192, 215 | vừa |
| CSA L05 | SHOULD | `nand` bước 0; `objectives`; recap | Mục tiêu “Giải thích vì sao một loại cổng NAND dựng được mọi mạch”; màn hình “Chỉ cần nó là dựng được mọi cổng” | Bài chỉ dựng NOT, AND, OR từ NAND. Thiếu bước then chốt: AND/OR/NOT dựng được *mọi* bảng chân trị (ví dụ OR của các dòng ra 1). XOR cũng không được dựng. Từ “dựng được NOT/AND/OR” bài nhảy thẳng tới “mọi mạch”. Dòng 17, 143, 149, 247 | vừa |
| CLD L10 | SHOULD | `pitfalls` lỗi 3; recap | “Định luật Little thì luôn đúng”; chuỗi recap “$L = \lambda W$ luôn đúng” | Cảnh `sym` nói đúng điều kiện “Đúng cho mọi hệ ổn định”, nhưng lỗi 3 và recap bỏ điều kiện. Chính lỗi 2 của bài là ví dụ hệ không ổn định (λ = 120 > μ = 100, “hàng đợi dài mãi”), ở đó L và W không có trung bình hữu hạn. Dòng 170–171, 215, 219 | vừa |
| ACB L05 | SHOULD | khắp bài (hook, prereq, concept SVG, check, recap) | “Kafka”, “Kafka Streams”, “Debezium CDC”, “Router Worker”, “NAPAS”, “Core”, “Idempotency Key”, “giải pháp kiến trúc chuẩn Senior”, “Nghẽn I/O”, “gọi API” | Màn hình dùng các từ này mà không định nghĩa bằng lời thường ngay lần đầu. Riêng Kafka chỉ được gọi gián tiếp là “hàng đợi sự kiện” trong lời đọc; Kafka Streams, NAPAS, Core, Senior, I/O, API thì không có định nghĩa nào. Dòng 128–146 (SVG) và bảng hook/pitfall | vừa |
| ACB L05 | SHOULD | recap | “tự tin nhận mức đãi ngộ 50 triệu gross”; lời đọc “đàm phán mức lương 50 triệu gross tại ACB” | Bài này không định nghĩa “gross”, và con số không có căn cứ ngay trong bài (căn cứ nằm ở L00: “mức đề xuất” dựa tin tuyển dụng). “tự tin nhận” biến mức đề xuất thành kết quả chắc chắn. Dòng 460, 467 | vừa |
| ACB L05 | SHOULD | `concept` bước 0 (chữ trong SVG) | “Phân tích 10,000 lệnh” | Cùng bài viết dấu thập phân bằng dấu phẩy (“$2{,}5$ giây”) và số nghìn bằng khoảng trắng (“$10\,000$”, “5 000”). Theo cách viết số tiếng Việt, “10,000” đọc là mười phẩy không. Dòng 128 | vừa |
| ACB L05 | SHOULD | `prereq` bước 0–1 | Màn hình “Quy mô bài toán thực tế: Một tập đoàn có $10\,000$ nhân viên, mức lương bình quân $15$ triệu đồng”; bảng ghi “hàng nghìn tài khoản con” nhưng lời đọc nói “hàng chục nghìn lệnh con” | Số giả định nhưng gọi là “thực tế”, thiếu “(số minh hoạ)”; phép tính 10 000 × 15 000 000 = 150 000 000 000 vẫn đúng. Màn hình và lời đọc lệch cỡ số (nghìn với chục nghìn). Dòng 81, 95, 102 | vừa |
| AGT L11 | SHOULD | `pitfalls` lỗi 2, lỗi 4 | “từ tố đầu vào (số minh hoạ: bước đầu 2000, mỗi bước thêm 500)”; “đo ‘thành công mọi lần’” | Trong bài không có chỗ nào giải thích “từ tố” (đơn vị đếm văn bản mà mô hình đọc/tính tiền) hay “thành công mọi lần” (chạy k lần đều thành công). Đây là khái niệm của bài 7–8, dùng lại mà không nhắc định nghĩa (luật B.4). Dòng 134, 145. Mọi số của bài tính lại đều đúng: 0,98⁴ = 0,9224, 0,95⁶ = 0,7351, 0,9975⁶ = 0,9851, 0,9996⁴ = 0,9984, 0,265/0,078 = 3,40, 19 500/12 000 = 1,625 | vừa |
| AIF L02 | SHOULD | hook, `example` bước 0 | “Cùng trò xếp 8 ô số của bài trước”; “Trạng thái 7 2 4 / 5 _ 6 / 8 3 1, đích _ 1 2 / 3 4 5 / 6 7 8” | Bài không nhắc lại luật chơi (trượt một ô kề vào chỗ trống, mỗi lần trượt tốn 1) và không nói “_” là ô trống, mà phép tính h₁, h₂ dựa vào cả hai. Dòng 34, 37, 107. Số đã kiểm bằng checklib: h₁ = 8, h₂ = 18, BFS = 26, A* mở 173 799 / 31 776 / 1 481 nút, 2·h₂ cho 30 bước với 633 nút, tỉ số 117 (đúng “hơn 100 lần”); quiz h₁ = 4, h₂ = 6, chi phí thật 8 | vừa |
| BCH L10 | SHOULD | `prereq` bước 3 | “mỗi nút theo chuỗi có <b>tổng công lớn nhất</b>” | “tổng công” (tổng công tính toán bỏ ra để đào các khối của chuỗi) và “nút” được dùng lại từ bài 6 mà không giải nghĩa một câu nào. Dòng 70–71. Số tính lại đều đúng: 10⁶/250/600 = 6,67; 10⁶/12/600 = 138,9; tỉ số 20,83; 0,8 s; 25,6 s; 576 000; 16,67 | vừa |
| CLC L12 | SHOULD | `prereq`; `quiz` bước 1 | “chạy ở 2 vùng, mỗi vùng gánh đủ 100% tải”; “bật phiên bản hoá như bài 4” | “vùng” (một khu trung tâm dữ liệu độc lập về địa lý) được dùng xuyên bài, “phiên bản hoá” (giữ các bản cũ của đối tượng để khôi phục khi xoá nhầm) được đưa ra làm lời khuyên, nhưng cả hai đều không được định nghĩa trong bài. Dòng 63, 353–355. Mọi mốc và số khớp `sources_L12.md`: 257 phút, 169, 120, 52,56, 4,89, ×250 000, 6,342 triệu năm, 1250, 4,32 phút | vừa |
| CS112 L12 | SHOULD | khắp bài | Dùng $\Theta$, $O$, $\Omega$ và “thế ngược” (“Thay vì thế ngược từng bài”, “Tính đúng bằng thế ngược”) | Không có câu nào nhắc định nghĩa ba ký hiệu tiệm cận hay phép thế ngược. Chúng chỉ nằm trong `assumes`, tức kiến thức các bài trước, mà ba trường hợp của định lý lại phát biểu bằng chính các ký hiệu này. Dòng 9, 41, 201. Số tính lại đều đúng: 64/128/256/512 = 960; 1,5/1,75/1,875/1,999; T(32)/32² = 0,969; T(1024) = 2046; T(27) = 81; khe hở n·log n cho đúng n·log n·(log n + 1)/2 | vừa |

Bài không có phát hiện: BNK L14 (tính lại 500 000 trừ dư, 1 500 000, 800 000, thứ tự trả về của `bnk_reconcile` = (khớp, chỉ ngân hàng, chỉ chuyển mạch, lệch tiền) khớp chữ trên màn hình) và CAS L08 (mọi sự kiện, giờ, con số khớp nguyên văn [GL17] trong `audit/cas/sources_L08.md`: 17:20, 19:00, 23:00, 23:30, 300 GB, “một hai giây”, 4 cách sao lưu, pg_dump 9.2/9.6, DMARC, 60 Mbps, ~18 giờ, 17:00/18:00 ngày 1/2, 5000/5000/700; tính lại 370 phút, 1350 phút, 3,6 lần, 18 giờ 30, 486 GB ghi rõ là ước lượng của bài, 7,4 giờ, 26,7 phút).

Ghi chú không xếp thành phát hiện (chưa đủ chắc):
- ACB L05: sơ đồ chia sao kê thành bốn đoạn thời gian “xử lý song song bằng Kafka Streams”. Kafka Streams song song theo phân vùng của chủ đề, không theo khoảng thời gian, nên câu này đơn giản hoá quá mức, nhưng là sơ đồ kiến trúc minh hoạ.
- CSA L05: “chip thật thường được chế tạo từ một vài loại cổng cơ bản” là cách nói đơn giản hoá (thư viện ô chuẩn có nhiều loại). Màn hình ghi “đại số Boole”, lời đọc nói “đại số lô-gích” (chú thích YAML dòng 13 cho biết đây là chủ ý).
- CLD L10: “con số kinh nghiệm hay gặp: 60–70%” không có nguồn, nhưng đã ghi là quy tắc kinh nghiệm “tuỳ dịch vụ”.

## Đã sửa (2026-11-10)

Người điều phối đã sửa MUST của CS115 L21 (objectives dòng 16, tiêu đề cảnh `metrics`); tôi không chạm hai chỗ đó. Mọi phát hiện SHOULD được kiểm lại trên tệp và đều đúng, nên đã sửa cả 13. Không chạy build, render, tts hay asr.

| Bài | Phát hiện | Đã sửa thế nào |
|---|---|---|
| CS115 L21 | MUST: tiêu đề cảnh `metrics` và objectives | Người điều phối đã sửa; tôi không sửa lại |
| CS115 L21 | SHOULD: hậu nghiệm/Bayes, tập kiểm định, ROC/AUC | `verify`: lời đọc thay “xác suất hậu nghiệm … định lý Bayes” bằng “xác suất có bệnh khi đã biết máy báo dương, đúng con số 9 phần 108 của bài đó”; bỏ mục `asr_reviewed` cũ của câu này. `in_ai`: màn hình định nghĩa đường cong ROC và AUC (diện tích dưới đường cong, từ 0 tới 1, 0,5 ngang đoán bừa), lời đọc nêu hai tên viết tắt và nghĩa của chúng, `focus` thêm 1 phần tử. Lỗi 3: định nghĩa tập kiểm định (phần dữ liệu để riêng nữa, chỉ dùng để chọn ngưỡng và chỉnh mô hình) ở cả màn hình và lời đọc |
| CSA L05 | SHOULD: nhảy từ NOT/AND/OR thẳng tới “mọi mạch” | Thêm bước mới vào cảnh `nand` (clear): cách dựng mạch từ bảng chân trị bất kỳ (OR của các dòng ra 1, mỗi dòng là AND các đầu vào, đầu vào bằng 0 thì qua NOT trước), ví dụ XOR = (¬a ∧ b) ∨ (a ∧ ¬b) thử tại a = 1, b = 0, rồi kết luận NAND dựng được mọi mạch. Thêm 2 `checks`: công thức XOR, và cách dựng đúng cho cả 256 bảng chân trị 3 đầu vào. Đã chạy `sync_tpl_from_lesson.py CSA --write`, mẫu nay khớp |
| CLD L10 | SHOULD: “Định luật Little luôn đúng” | Cảnh `sym` thêm định nghĩa hệ ổn định (tốc độ đến nhỏ hơn tốc độ phục vụ, nên hàng đợi không dài mãi) ở màn hình và lời đọc, `focus` thêm 1 phần tử. Lỗi 3 và chuỗi tổng kết đổi thành “đúng cho mọi hệ ổn định” ở cả màn hình và lời đọc. Bỏ 2 mục `asr_reviewed` không còn câu tương ứng. Đã chạy `sync_tpl_from_lesson.py CLD --write`, mẫu nay khớp |
| ACB L05 | SHOULD: thuật ngữ chưa định nghĩa | Thêm bước mới vào `prereq` (bảng và lời đọc) định nghĩa Kafka, Kafka Streams, CDC (Debezium), Core Banking, NAPAS. Ô bảng hook không còn nêu Kafka Streams trước định nghĩa. Bỏ hoặc Việt hoá các từ còn lại: “Senior” thành “kỹ sư cấp cao” (4 chỗ); “gọi API” thành “gọi qua mạng”; “Nghẽn I/O” thành “Nghẽn đọc ghi đĩa”; “DB” thành “cơ sở dữ liệu”; “Router Worker” thành “Tiến trình định tuyến” (khớp lời đọc); “Kafka Topic / Phân vùng theo Batch” thành “Đẩy vào Kafka / Chia phần theo lô”; “transaction” thành “giao dịch cơ sở dữ liệu”. “Idempotency Key” được giải nghĩa thành khoá chống trùng (mã riêng của mỗi lệnh con, gặp lại mã đã xử lý thì bỏ qua); “PENDING” thành “trạng thái chờ xử lý (PENDING)” |
| ACB L05 | SHOULD: “50 triệu gross” | Phần tổng kết, ở cả màn hình và lời đọc, định nghĩa gross (lương trước khi trừ thuế và bảo hiểm) và ghi rõ đây là mức đề xuất ở bài 0, dựa trên tin tuyển dụng, không phải mức chắc chắn được nhận. Bỏ “tự tin nhận” và “Khẳng định đẳng cấp Senior”. Lời đọc tách thành 3 câu, `focus` nay 3 phần tử. Bỏ mục `asr_reviewed` cũ |
| ACB L05 | SHOULD: “10,000 lệnh” | Đổi thành “10 000 lệnh” |
| ACB L05 | SHOULD: số “thực tế” không nguồn; lệch nghìn với chục nghìn | “Quy mô bài toán thực tế” thành “Quy mô bài toán (số minh hoạ)”, lời đọc thêm “với số minh hoạ”. Bảng nay ghi “hàng chục nghìn lệnh con”, khớp lời đọc. Hook đổi “ngày 30 hàng tháng” thành “ngày cuối tháng”, khớp lời đọc |
| AGT L11 | SHOULD: “từ tố”, “thành công mọi lần” | Lỗi 2: màn hình và lời đọc nhắc lại định nghĩa “thành công mọi lần” của bài 7. Lỗi 4: màn hình và lời đọc định nghĩa từ tố (mẩu chữ mô hình đọc và viết; giá tính theo số từ tố), `focus` thêm 1 phần tử |
| AIF L02 | SHOULD: luật trò 8 ô số và ký hiệu “_” | Thêm bước đầu của `prereq`: khung 3 × 3, “_” là chỗ trống, mỗi bước trượt một ô kề vào chỗ trống tốn chi phí 1, cách ghi theo hàng với dấu “/”, ví dụ 4 cách trượt ở trạng thái đầu và 2 ở đích (có `checks` mới qua `alg.puz_moves`). Đổi tiêu đề cảnh cho khớp nội dung |
| BCH L10 | SHOULD: “tổng công”, “nút” | `prereq` bước 3 định nghĩa nút, công của một khối (số lần thử trung bình để tìm được khối) và tổng công, ở cả màn hình và lời đọc, kèm `focus` |
| CLC L12 | SHOULD: “vùng”, “phiên bản hoá” | Hook định nghĩa vùng (khu vực địa lý gồm nhiều trung tâm dữ liệu; kho ở mỗi vùng chạy riêng), `focus` thêm 1 phần tử. Đáp án câu 1 của quiz giải nghĩa phiên bản hoá (kho giữ bản cũ khi đối tượng bị ghi đè hay xoá, nên xoá nhầm vẫn lấy lại được) ở cả màn hình và lời đọc |
| CS112 L12 | SHOULD: Θ/O/Ω, “thế ngược” | Hook thêm ghi chú và câu đọc nhắc lại thế ngược (bài 8). `prereq` thêm bước đầu nhắc lại O, Ω, Θ (bài 1), kèm ví dụ 3n + 5 ∈ Θ(n) với n ≥ 5 (có `checks` mới). Tiêu đề cảnh đổi thành “Ôn lại: ký hiệu bậc, và đổi chỗ cơ số với số mũ” |
| BNK L14, CAS L08 | không có phát hiện | không sửa |

Không đổi mục giáo án nào. Mục tiêu và tiêu đề các bài vẫn giữ nguyên, trừ tiêu đề cảnh, mà giáo án không chứa tiêu đề cảnh. Bài CSA L05 nay dạy đủ mục tiêu “Từ bảng chân trị dựng mạch” và “NAND dựng được mọi mạch”.

Tệp đã đổi:
- lessons/acb/L05_cong_chi_luong_va_sao_ke_divide_conquer.yaml
- lessons/agt/L11_tong_hop.yaml
- lessons/aif/L02_a_sao.yaml
- lessons/bch/L10_mo_rong.yaml
- lessons/clc/L12_hanh_trinh_luu_tru_doi_tuong.yaml
- lessons/cld/L10_hang_doi.yaml, audit/cld/src/L10_hang_doi.tpl.yaml (đồng bộ bằng công cụ; bản cũ ở out/_tpl_backup/cld/)
- lessons/cs112/L12_chia_de_tri_dinh_ly_tho.yaml
- lessons/cs115/L21_danh_gia_phan_loai.yaml
- lessons/csa/L05_mach_logic.yaml, audit/csa/src/L05_mach_logic.tpl.yaml (đồng bộ bằng công cụ; bản cũ ở out/_tpl_backup/csa/)
- audit/review/sample_d/part_1.md (mục này)

Kết quả kiểm sau sửa:
- `lv.py lint`: 0 FAIL, 0 WARN ở cả 9 bài đã sửa.
- Bộ kiểm khoá:
  - verify_agt: 15 PASS · 0 FAIL
  - verify_aif: 26 PASS · 0 FAIL
  - verify_bch: 13/13 PASS
  - verify_clc: 13/13 PASS
  - verify_cld: 20 PASS · 0 FAIL
  - verify_cs112: 38 PASS, 15 FIX, 0 FAIL
- ACB, CS115, CSA không có tệp verify riêng.
- `audit/verify_plan_curricula.py`: 545 PASS · 0 FAIL.
- `scan_ctrl.py`: 8 lượt, đều là 8 lượt `\tat` cố ý của JVA, không có lượt mới.
- `sync_tpl_from_lesson.py` CLD và CSA: khớp.
- Cần dựng lại (build, tts, render): 9 bài đã đổi lời và hình. Nên chạy `render` trước cho AGT L11 bước lỗi 4 (thêm một dòng ghi chú trên bước vốn đã có hộp và bảng) và ACB L05 bước `prereq` mới (bảng bốn dòng), vì có thể tràn khung.
- `lv.py curriculum`: 0 lỗi ở cả 9 khoá: ACB 9 bài, AGT 13, AIF 15, BCH 13, CLC 13, CLD 16, CS112 30, CS115 46, CSA 17.
