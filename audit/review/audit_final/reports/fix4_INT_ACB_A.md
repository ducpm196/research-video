# fix4 INT_ACB phần A — INT L00–L03 (fork A, 2026-11-15)

Cả 4 bài đã đổi => CẦN DỰNG LẠI (build/tts/asr) L00, L01, L02, L03. Đã chạy `lv.py render` nên `out/INT/L0x/frames` là khung mới (chưa có mp4/srt mới).
Nguồn sửa: YAML viết tay (Edit/Python giữ CRLF của L01–L03), không đổi tên tệp.

## Cổng thật (sau khi sửa xong cả 4 bài)
- lv.py lint: L00 0F/0W (35 PASS), L01 0/0 (32), L02 0/0 (26), L03 0/0 (34). lv.py render: 0 vấn đề cả 4 (105/96/92/89 khung).
- verify_int.py: 207 PASS, 0 FAIL. lab_gate INT: 9 PASS, 0 FAIL. screen_code check INT: 60 khối, PASS 83, FAIL/STALE/MISSING/ORPHAN 0 (đổi khoá sổ `INT L03 example 3 0` -> `4 0` và `twin_of` vì tách step).
- tests/test_e52.py: 0 FAIL. arith_scan: 244 phép, 0 FAIL. lv.py curriculum curriculum/int.yaml: 9 bài, 0 lỗi (không phải sửa curriculum/int.yaml).
- check_course_refs.py INT: 9 vấn đề R4 ("bài cuối khoá" nói ở INT L04 hook.1/recap.0 và INT L07 recap.1) — không có ở L00–L03; thuộc phần L04–L08 (fork B). Bản chạy toàn kho quá lâu, chỉ chạy riêng khoá INT.

## Số từ lời đọc (tổng `say`)
| Bài | trước | sau |
|---|---|---|
| L00 | 2236 | 2293 |
| L01 | 1998 | 2146 |
| L02 | 2016 | 2133 |
| L03 | 2023 | 2157 |
Tất cả ≤ 2300.

## Term đăng ký mới trong tools/registry/symbols.INT.yaml (chỉ thêm, nhóm L00)
- `int_cong_tich_hop` (term `(?i)cổng tích hợp`) — introduces ở INT L00 prereq step 0.
- `int_chi_muc` (term `(?i)chỉ mục`) — introduces ở INT L00 concept step 1 (bảng giải nghĩa từ trên kim tự tháp).
- `int_luong` (term `(?i)\bluồng (nhẹ|nặng|ảo|hệ điều hành|truyền thống)\b|\bbể luồng\b|\bđa luồng\b`) — introduces ở INT L00 quymo step 1.
`assumes` đã thêm: L01 `int_luong`, `int_chi_muc`; L03 `int_luong`, `int_chi_muc`. L02 không dùng term mới.

### CẦN ĐIỀU PHỐI: bài L04–L08 (fork B) phải thêm `assumes` (lint hiện FAIL E52 do term mới)
- L04: `int_luong` (quymo step 1)
- L05: `int_luong` (prereq step 0)
- L06: `int_luong` (hook step 1), `int_chi_muc` (prereq step 2), `int_cong_tich_hop` (quiz step 1)
- L07, L08: lint 0 FAIL (không dùng).

## INT L00
- P1: "cổng tích hợp" giảng ở prereq step 0 (màn hình + lời); "bộ nhớ đệm CPU / heap (vùng nhớ động) / rò rỉ" giảng tại concept step 2 (thêm đoạn giải nghĩa + câu lời); "luồng / luồng nặng / luồng nhẹ" giảng ở quymo step 1; "chỉ mục" (mục lục sách) giảng ở concept step 1; SQL cơ bản ở example step 2: cơ sở dữ liệu = bảng hàng–cột, INSERT = thêm một hàng, UNIQUE = cột không được hai hàng cùng giá trị (tách thành 2 step để khỏi tràn). Ghi "tin đã lưu, đối chiếu lại trước khi nộp hồ sơ" cho tin ACB ở symbol step 0.
- SHOULD: check step 0 thêm `pause: 15`; quiz step 0 `pause: 5 -> 25` (phép tính 3 bước).
- Cắt để giữ ≤ 2300: bỏ câu "Tầng bốn có hai chuyên đề…", bỏ câu thứ hai của hook step 1, rút câu hook step 0, bỏ câu chúc ở recap. Xoá 3 mục asr_reviewed cũ (câu không còn).
## INT L01
- Hook: "thế hệ mới" -> "bố cục thế hệ trẻ và thế hệ già … cùng các đợt thu gom rác"; "hàng triệu luồng ảo" -> "hàng chục nghìn luồng ảo"; thêm giải nghĩa "luồng" ở hook (màn hình + lời).
- P1: biến / kiểu long / nhân CPU (prereq step 1, lời + màn hình), chỉ mục (symbol step 1: nhắc lại mục lục sách), vào ra (chờ mạng/đĩa), synchronized (example step 2), Spring Boot/Tomcat/request (example step 4), bất biến (quiz), heap/GC/đối tượng/biến cục bộ (concept: tách step, thêm bảng giải nghĩa).
- SVG JVM: max-height 340 -> 440 (nhãn con ~22 px trên khung 1920; trước ~16 px) và tách giải nghĩa sang step riêng để không tràn. Check step 0 thêm `pause: 15`.
## INT L02
- Hook: show và say cùng một mô tả ("các bước ghi kèm theo không được hoàn tác"), và nói "Spring" thay "Spring Boot" ở lời đọc.
- chaythat: `pause: 15` sau câu "hãy đoán"; giảng ngắn interface/implements/static class (step 0) và lambda `(p, m, a) ->`, `m.invoke` (step 1) cả màn hình + lời; check step 0 `pause: 15`.
- Sơ đồ proxy vẽ lại: lớp vỏ chỉ bọc lối vào; "gọi qua this" nằm trong "Đối tượng thật (không có vỏ)", mũi tên không đi qua vỏ.
- P1: REST/HTTP/mã trả về và Redis được nói bằng lời ở prereq step 0; "con trỏ nội bộ" -> "ngay trên chính đối tượng thật"; DispatcherServlet giảng tại chỗ ở quiz (màn hình + lời).
## INT L03
- Recap: hàng Kafka đổi nhãn "Kafka acks=all + idempotent" và nói rõ không mất tin nhờ acks=all + 2 bản đồng bộ; lũy đẳng chỉ khử trùng do producer tự gửi lại.
- Check: câu hỏi và phương án B có điều kiện "quy trình nhiều bước (8 dịch vụ)", "ít bước, ít đội thì vẫn có thể hợp lý"; `pause: 15`.
- Pitfall: thêm điều kiện "truy vấn theo ngày mà không có chỉ mục phù hợp" (màn hình + lời); nhắc lại chỉ mục.
- P1: SQL cơ bản (SELECT/WHERE/UPDATE), con trỏ (cursor) giảng ở example step 5 (tách step), ADR/tệp vết (quiz), Debezium (một công cụ mã nguồn mở), SAGA/CASA/gạch nợ/máy trạng thái giảng trước sơ đồ (tách concept step 0 thành 2 step), chỉ mục ở pitfall.
- SVG SAGA: max-height 300 -> 440 (nhãn con ~20 px).
## Mục không sửa / ghi nhận
- P3 (hình cơ chế): SAGA vẫn là cây ba ô (không vẽ mũi tên bù trừ); Outbox, 2PC vs SAGA, B-Tree vẫn chỉ chữ/mã — cần thêm sơ đồ mới (việc vẽ lớn, không nằm trong danh mục SHOULD được giao).
- L02 SHOULD "check Bloom không bác từng phương án sai": chưa viết thêm (không nằm trong nhiệm vụ).
- L03 SHOULD "Kafka giao ít nhất một lần" (phần ACB) không thuộc INT. L00 "luồng" sau này (L04–L08) cần assumes như trên.
- Ảnh khung đã xem: L00 (concept/quymo), L01 00012/00023/00034/00046, L02 00022, L03 00024/00043/00046 (đã sửa tràn sau đó).
