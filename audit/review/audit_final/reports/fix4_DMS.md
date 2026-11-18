# fix4_DMS — sửa DMS L00–L20 theo R2_DMS_A / R2_DMS_B (2026-11-15)

TRẠNG THÁI: XONG. Mọi SHOULD đã sửa (trừ mục ghi "không sửa" ở cuối). Người điều phối dựng lại đúng 16 bài ở mục 1.

## 1. Bài đổi → CẦN DỰNG LẠI (build/tts/asr)
L01, L02, L04, L05 (đã sửa trước bởi điều phối + hình Venn ở lần này), L06, L08, L09, L10, L11, L12, L13, L14, L16, L17, L18, L20  (16 bài).
KHÔNG đổi (giữ video cũ): L00, L03, L07, L15, L19.
Ngoài bài: lab `labs/DMS/` đổi `de.md` ở L01, L06, L09, L10, L11, L12, L13, L16, L17, L18 và `loi_giai.py` ở L13 (mong_doi.txt KHÔNG đổi ở bất kỳ lab nào); sổ `audit/review/screen_code/DMS.yaml` (đồng bộ L06, L08, L09, L10 vì khối mã đổi); `tools/registry/symbols.DMS.yaml` (thêm `dms_ntcn`); `audit/dms/plain_svg.py` (+`crown()`); `audit/dms/vparts/l08.py` (+kiểm bộ đếm).
Quy trình: sửa kịch bản vá `audit/dms/af2/lNN.py` (L16–L18: kịch bản vá mẫu `src/*.tpl.yaml`) rồi chạy lại kịch bản (sinh lại bài + lab + sổ + giáo án); khối `asr_reviewed` giữ nguyên, trừ câu bị đổi (L14: 1 câu bỏ). Kịch bản và bài khớp nhau (đã kiểm bằng chạy lại: kết quả y hệt trước khi sửa).

## 2. Đã sửa gì (R2 → hành động)
- P1 L12: "nguyên tố cùng nhau" + "ước chung lớn nhất" giảng tại chỗ (cảnh practice: ghi chú trên màn hình + 2 câu lời đọc có ví dụ 8 và 15 / 8 và 12; de.md); `introduces: dms_ntcn` (mục sổ mới); thêm step giảng `all(...)`/`sum(... for k ...)` trong quymo.
- Cú pháp Python vượt cơ bản (de.md có đoạn "Cú pháp cần dùng" kèm ví dụ nhỏ + hint ở cảnh practice nhắc tới; lời đọc không chữ Anh): L01 (`import`, `product(... repeat=n)`, `f(*dong)`), L06 (`combinations`, `f.values()`, hằng 2654435761 + `%` chồng + `[0] * m`: step giải thích riêng), L09 (`product/permutations`, `len(list())`), L10 (`factorial`, `combinations`, danh sách lồng `d[r][c]`), L11 (`comb`, `product`, `combinations_with_replacement`, `sum(1 for ...)` + cho phép dùng vòng lặp thường), L12, L16 (`sum(1 for e in canh if v in e)`), L17 (step giải thích `combinations`, danh sách `[a if ... else x for ...]`, `sum(1 for ...)`; de.md khung vòng lặp thường), L18 (step giải thích từ điển/tập `{...}`/`min(...)`; de.md).
- L04: hook/title/bảng nói "quân cờ dựng đứng (domino)" (lexicon DMS cấm đọc chữ domino → sửa phía màn hình cho khớp lời đọc).
- L05: MUST đã sửa trước (kiểm lại: "hai số 2 và 3 không có ước chung nào lớn hơn 1" đúng; 6 là bội chung vì vậy). Hình intuition: tô đỏ nhạt phần giao (path), khung 00033 xem lại: phần giao đỏ, khớp lời "vùng đỏ".
- L08: step mới chạy thật bộ đếm trên 4 việc (4 chọn + 4 trừ = 8 thao tác = n + số ràng buộc), bảng: 10^6 việc, 1 999 997 ràng buộc → 2 999 997 thao tác ≈ 3 phần nghìn giây (vparts/l08 chạy thật Kahn ở n = 10^6, khớp); câu "mang tên một nhà toán học" sửa lại.
- L09: rules (màn hình) "không phụ thuộc bước trước chọn gì"; dòng `print` tràn chia hai dòng (`so = 62 ** do_dai`); render 0 vấn đề.
- L10: "x mũ, n trừ k trên đầu, nhân y mũ k"; quymo thêm số đếm thật 1 000 người chia 10 nhóm → 49 500 cặp thay vì 499 500 (ít hơn hơn 10 lần), có trong `checks`.
- L02: câu "miền là tập các giá trị mà x được phép nhận" + ghi chú trên màn hình.
- L13: "mười chín chữ số" (2880067194370816120 và 1779979416004714189 đều 19 chữ số, đã `len(str(...))`); hint đệ quy → vòng lặp (khung mã Euclid mở rộng bằng vòng lặp ở de.md, `loi_giai.py` cũng viết bằng vòng lặp; đầu ra y hệt).
- L14: "chu kỳ chia hết p − 1" (intuition + verify + màn hình); bước giản ước tích cũ trong ý chứng minh (tích cũ không chia hết p nên có nghịch đảo → giản ước).
- L16: nhãn bảng "trường hợp xấu nhất cỡ (n−1)!/2 thứ tự (đồ thị bất kỳ n đỉnh)"; "đọc danh sách cạnh vài lượt (đếm bậc, kiểm liên thông)".
- L18: tiền đề E ≥ 3 + liên thông (đường 3 đỉnh loại ra); quymo thêm hình vương miện n = 3 (hai thứ tự, 3 màu / 2 màu, sinh bằng máy, lần tay), lời đọc nói rõ điều kiện kề i ≠ j, step giải thích cú pháp; de.md dòng 4–6 viết lại ("chỉ biết V và E, không có danh sách cạnh").
- L20: "Còn phía Git liệt kê…" (khớp màn hình và sources_L20); hook đọc đủ 2004/2007/mười giây và "hơn một trăm nghìn lần".

## 3. Cổng (số thật, chạy sau sửa)
- lint 21 bài: 0 FAIL, 0 WARN (cả 21).
- render: 0 vấn đề ở 21/21 (L06/L08/L09/L12 từng tràn do khối mới, đã tách step; render lại 0).
- verify_dms: 326 PASS · 0 FAIL (lab 21, cảnh quy mô chạy thật 23).
- lab_gate DMS: 21 PASS · 0 FAIL (196 lab).
- lv.py curriculum curriculum/dms.yaml: 21 bài, 0 lỗi. check_curricula_graph: tham chiếu hỏng 0, chu trình 0, VER không PASS 0.
- tests/test_e52.py: 0 FAIL. screen_code check --course DMS: 74 khối, PASS 97, FAIL 0, STALE 0, MISSING 0, ORPHAN 0. arith_scan: 245 phép, 0 FAIL. check_course_refs DMS: 0 vấn đề.
- Lời đọc (đếm từ): max L20 2296, L18 2260, L19 2207; mọi bài ≤ 2300. Mỗi `say` 4–38 từ; câu mới ≥ 8 từ (kiểm so với bản trước).

## 4. P1 dự kiến
DMS A 11/11, DMS B 10/10 (L12 giảng tại chỗ; cú pháp Python giảng ở de.md/step giải thích). MUST 0.

## 5. Không sửa (và vì sao)
- L03 "tối giản" (P1 nhẹ, không nằm trong danh sách SHOULD của người đọc; hiểu qua ví dụ).
- L17 "ba điều tương đương chỉ chứng minh một chiều" (P2, người đọc không đề xuất sửa cụ thể; ngoài phạm vi nhiệm vụ này).
- Nghe âm thanh độc lập: chưa làm được (không chạy tts/asr); các câu mới đổi sẽ có cờ ASR mới sau khi dựng — cần xem xét như thường lệ.
