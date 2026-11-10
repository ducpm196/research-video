# TOC — đã đọc 15/15 bài

Đọc toàn bộ `show`, `say`, `checks`, quiz và đáp án của từng bài (2026-11-08). Bài có mẫu: L01, L02, L05, L06, L07, L09; chỉ L06 bị sửa → đã chạy `sync_tpl_from_lesson.py TOC --write`, mẫu `audit/toc/src/L06_van_pham_phi_ngu_canh.tpl.yaml` đã nhận câu sửa (kiểm lại: 0 mẫu lệch bài).

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 | đã sửa | lang: SHOULD — “$L_3$ = các số nhị phân (không 0 thừa ở đầu) chia hết cho 3 = {11, 110, …}” bỏ sót số 0 (chuỗi “0” thoả định nghĩa) → “số nhị phân **dương**”, khớp `checks` (`w[0] == '1'`) | Sipser 3e §0.2 (định nghĩa ngôn ngữ); tự kiểm định nghĩa | lint: 0 FAIL, 0 WARN, 31 PASS · render: 75 khung (0 vấn đề) |
| L01 | không phát hiện lỗi | — | Sipser 3e §1.1 | — |
| L02 | không phát hiện lỗi | — | Rabin–Scott (1959); Sipser 3e §1.2 | — |
| L03 | không phát hiện lỗi | — | Kleene (1956); Sipser 3e §1.3 | — |
| L04 | không phát hiện lỗi | — | Sipser 3e §1.4 | — |
| L05 | không phát hiện lỗi | — | Hopcroft–Ullman §4.4; Myhill–Nerode | — |
| L06 | đã sửa | hook: SHOULD — “nền của cú pháp **mọi** ngôn ngữ lập trình” tuyệt đối → “cách mô tả cú pháp của hầu hết ngôn ngữ lập trình” (nhiều ngôn ngữ có phần cú pháp ngoài phi ngữ cảnh, xử lý ở bước tách từ/kiểm ngữ nghĩa); mẫu đã đồng bộ | Aho, Lam, Sethi, Ullman, Compilers 2e §2.2, §4.2 | lint: 0 FAIL, 0 WARN, 29 PASS · render: 73 khung (0 vấn đề) |
| L07 | không phát hiện lỗi | — | Aho và cộng sự §4.2; Cantor (1962) | — |
| L08 | không phát hiện lỗi | — | Sipser 3e §2.2 | — |
| L09 | không phát hiện lỗi | — | Turing (1936); Sipser 3e §3.1 | — |
| L10 | đã sửa | evidence: SHOULD — “Năm 1936, ba mô hình ra đời” sai mốc: phép tính lambda từ 1932, hàm đệ quy tổng quát của Gödel 1934 → “Trong khoảng 1932 tới 1936” (màn hình + lời đọc, tách câu cho vừa phụ đề) | Stanford Encyclopedia of Philosophy, “The Church-Turing Thesis” (bản sửa 18/12/2023, truy cập 2026-11-08) | lint: 0 FAIL, 0 WARN, 25 PASS · render: 82 khung (0 vấn đề) |
| L11 | đã sửa | hook: SHOULD — “Năm 1936, Turing chứng minh [công cụ báo treo] không thể tồn tại”: bài 1936 chứng minh CIRC?/PRINT? không tính được — “rất gần” bài toán dừng, chưa phải đúng nó → viết mềm “chứng minh một bài toán rất gần với nó … Từ đó suy ra …” | Stanford Encyclopedia of Philosophy, “Turing Machines” (bản sửa 21/5/2025, truy cập 2026-11-08), §2.4.2–2.4.3 | lint: 0 FAIL, 0 WARN, 25 PASS · render: 77 khung (0 vấn đề) |
| L12 | đã sửa | pitfalls lỗi 2: SHOULD — “bộ kiểm kiểu … không bao giờ cho qua chương trình sai” tuyệt đối sai (chỉ chặn lỗi kiểu, và không phải hệ kiểu nào cũng chặt) → “bộ kiểm kiểu chặt có thể từ chối vài chương trình chạy đúng, đổi lại chặn được cả một loại lỗi (lỗi kiểu) — nhưng không bắt được mọi lỗi” | B. Pierce, Types and Programming Languages (2002), §1.1 (hệ kiểu là phương pháp bảo thủ, chỉ loại một lớp hành vi lỗi) | lint: 0 FAIL, 0 WARN, 24 PASS · render: 83 khung (0 vấn đề) |
| L13 | đã sửa | recap: SHOULD — “NP đầy đủ” xuất hiện trên màn hình mà bài chưa giải thích → “thuộc loại khó nhất của NP (NP đầy đủ)”, khớp lời đọc; SHOULD — câu báo bài sau “chọn sai cách chạy ô-tô-mát làm sập cả hệ thống” quy sự cố về một nguyên nhân, trái bài 14 (hậu kiểm ghi 11 nguyên nhân góp phần) → “có thể làm sập cả một hệ thống rất lớn”, khớp lời đọc | Sipser 3e §7.4 (NP đầy đủ); [CF19] trong `audit/toc/sources_L14.md` | lint: 0 FAIL, 0 WARN, 30 PASS · render: 78 khung (0 vấn đề) |
| L14 | không phát hiện lỗi | — (đã mở lại bài hậu kiểm Cloudflare 2019: “thử ở một thành phố” trước 14:52 và “Everything that occurred up to the point the rules were deployed was done ‘correctly’” đều đúng nguồn) | [CF19] blog.cloudflare.com (truy cập 2026-11-08); [CX07], [CX10], [R2], [TH68] theo `audit/toc/sources_L14.md` | — |

Tổng: 15/15 bài đã đọc, 6 bài sửa; 0 mục MUST, 7 mục SHOULD (L00, L06, L10, L11, L12, L13 ×2).

## Không sửa và vì sao
- L01: máy chia hết cho 3 nhận cả ε và chuỗi có 0 ở đầu (“0”, “011”); bài đã nói rõ ở lỗi 3 nên không sửa.
- L08 tư duy “mỗi lần cho máy thêm một loại bộ nhớ, lớp bài toán giải được mở rộng” — câu khái quát sư phạm, đúng cho dãy ôtômat → ngăn xếp → băng của khoá; không coi là định lý.
- L09 hook “mọi máy tính ngày nay không tính được nhiều hơn nó” — đúng theo luận đề Church–Turing, được bài 10 giải thích ngay sau.
- L07 lỗi 4: Cantor (1962) cho tính mơ hồ không khả quyết — cùng thời có Floyd (1962), Chomsky–Schützenberger (1963); dẫn một tác giả là đủ, không sai.
- L11 lỗi 2: “dãy 3n + 1 … chưa ai biết” — giả thuyết Collatz vẫn mở theo nguồn Lagarias (2010) đã ghi; không có nguồn mới hơn trong phiên này.

## Việc cần người điều phối
- Lời đọc đổi ở L00, L06, L10, L11, L12 (L13 chỉ đổi màn hình) → cần dựng lại tts/asr/build (tôi không chạy).
- Đã xoá 2 mục `asr_reviewed` không còn câu tương ứng: L10 (“Năm 1936, ba mô hình ra đời độc lập…”), L11 (“Năm 1936, Turing chứng minh công cụ đó…”). Cả hai là mục chờ tai người cho cách đọc “Turing”; câu mới vẫn chứa “Turing” nên lượt asr sau cần xét lại.
- `rec()` TOC trong `audit/verify_plan_curricula.py` không đụng tới nội dung đã đổi.

## Kết quả cuối
- `audit/toc/verify_toc.py`: 102/102 PASS
- `lv.py curriculum curriculum/toc.yaml`: curriculum: 15 bài, 15 đã có đặc tả, 0 lỗi
- `sync_tpl_from_lesson.py toc`: tổng: 0 mẫu lệch bài
- `scan_ctrl.py`: không có lượt nào ở `lessons/toc`.
