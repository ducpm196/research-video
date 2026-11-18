# fix2_S01 JV2: sửa vòng 2 theo báo cáo người đọc S01b_JV2 (2026-11-14)

Nguồn sửa: `audit/jv2/src/l01.py, l02.py, l03.py, l05.py, l06.py, l07.py, l08.py, l09.py`; sổ thuật ngữ `tools/registry/symbols.JV2.yaml` (thêm 11 mục `term:`); giáo án `curriculum/jv2.yaml` (2 chỗ). `lessons/jv2/*.yaml` do `gen.py` sinh lại; sổ mã màn hình `audit/review/screen_code/JV2.yaml` sinh lại bằng `screen_code.py gen-jv2` (diff 33 dòng: đổi khoá bước, 3 khối đổi chữ, 1 khối NhatKy mới). Không chạy build/tts/asr/audit_all/git/docker; không sửa YAML sinh ra bằng tay.

## 1. Bài đã đổi (để dựng lại)

L01, L02, L03, L05, L06, L07, L08, L09 (8 bài). L00 và L04 không đổi.
- Lời đọc đổi: L01, L02, L03, L06, L07, L08, L09. L05 chỉ đổi chữ chú thích trong khối mã (lời đọc giữ nguyên, TTS dùng cache) nhưng khung hình đổi nên vẫn phải dựng lại.
- L09: cảnh `intuition` tách bước NhatKy thành hai (từ 13 lên 14 step), nên số khung đổi (149 khung).
- Lab (`labs/JV2/*`): không đổi (gen sinh lại giống từng chữ; `lab_gate` 10 PASS).

## 2. MUST và SHOULD

MUST: 0 (báo cáo không có). SHOULD: báo cáo ghi 8 mục, sửa đủ 8 (mục 4 gom hai chỗ L08 + L06 thành một).

| # | Mục | Cách sửa |
|---|---|---|
| 1 | L06 nhãn "biên 2" đặt dưới chấm biên 1 triệu | SVG intuition step 1: nhãn "biên 1: 1 000 000 / 1 000 001" dời xuống x=780 (đúng chấm), nhãn "biên 2: 10 000 000 / 10 000 001" dời xuống x=1140 (đúng chấm 10 triệu). Đã xem khung 00022: nhãn nằm dưới đúng chấm. |
| 2 | L07 practice step 3 "Dòng số 15 có vòng for" | Gợi ý nay nói: dòng 15 là nơi nổ (`tong += phi(ds[i])`), điều kiện `i <= ds.length` nằm ở vòng `for` ngay trên nó, dòng 14; lời đọc khớp. Đã đếm lại bằng `de.md`: `for` ở dòng 14, thân ở dòng 15, dấu vết `TongPhi.java:15`. |
| 3 | L09 "nhiều gói" / "ba thư mục" | Thống nhất một cách nói: "dự án nhiều tệp trong một gói". Đổi ở: mục tiêu 1 của bài và `curriculum/jv2.yaml`, hook step 2 (hộp chữ + lời đọc), hàng ôn lại bài 0 ("một gói, thư mục khớp tên gói, một lệnh biên dịch cả gói"), trường `source`. `covers` trong bài không phụ thuộc chữ (chỉ số mục tiêu), không đổi; giáo án không có `covers` riêng. grep "nhiều gói|ba thư mục" ở L09, giáo án, lab: 0 chỗ. |
| 4 | L01 hook "chỉ có thể đi qua cửa thứ ba" | Lời đọc: "thì thường phải dùng cửa thứ ba là tệp, bên cạnh vài đường nâng cao hơn" (không nêu thuật ngữ mới). |
| 5 | L01 quiz step 3 "chắc chắn hết bộ nhớ" | Lời đọc: "nhiều khả năng hết bộ nhớ"; màn hình thêm chú "64 byte mỗi dòng là ước lượng, nên chỉ kết luận: nhiều khả năng hết bộ nhớ". |
| 6 | L06 quiz câu 1 (3 000 001 → 3 000) | Đề ghi "0,1% … làm tròn xuống đồng"; lời đọc đề cũng nói; đáp án thêm "0,1% × 3 000 001 = 3 000,001, cắt phần lẻ (làm tròn xuống đồng) còn 3 000" và lời đọc đáp án thêm một câu giải thích; thêm check `3000001 // 1000 == 3000`. |
| 7 | Làm tròn: L08 ",43" và L06 "584 năm" | L08 formula step 4 và example step 5: "≈ 1 755 616,44" (màn hình + lời đọc "bốn bốn"; check `round(640800000000 / 365000, 2) == 1755616.44` và `round(640800000 / 365, 2) == 1755616.44`). L06 scale step 1: "≈ 584,5 năm" (lời đọc "năm trăm tám mươi bốn phẩy năm năm"; check `round(2**64 / 1e9 / 3600 / 24 / 365.25, 1) == 584.5`); `curriculum/jv2.yaml` L06 `example` đổi theo "≈ 584,5 năm". |
| 8 | Chú thích tràn khung: L01 (00094), L05 (00088) | L01 `DocHet`: "// giữ MỌI dòng trong bộ nhớ" thành "// giữ MỌI dòng". L05 `ThamSoNhom` hàm chính: bớt 24 dấu cách đệm trước chú thích (chữ không đổi). Đã xem lại hai khung sau render: chú thích nằm trong khung. Sổ mã sinh lại (3 khối đổi sha). |

## 3. P1: thuật ngữ giảng tại chỗ (đã ghi E52)

Mỗi thuật ngữ là một mục `term:` trong `symbols.JV2.yaml`; `introduces` đặt ở step đầu tiên có chữ đó; bài sau dùng ghi `assumes`.

| Bài | Thuật ngữ | Giảng ở đâu (tại chỗ) | id E52 |
|---|---|---|---|
| L02 | log₂ | scale step 0 (mới): hộp "log₂ n = số lần phải nhân đôi, bắt đầu từ 1, để tới n" + bảng 1→2→4→8→16 (log₂ 16 = 4), …→1 024 (log₂ 1 024 = 10), …→1 048 576 (log₂ 1 000 000 ≈ 20); step 2 nói "lôgarit cơ số hai" | `jv2_log2` (introduces L02; assumes L07) |
| L02 | cờ `sort -t, -k2,2 -k3,3nr` | check step 0 (tách đôi): dòng dữ liệu `mã,loại,tiền`, bảng ba cờ (`-t,` ngăn cột bằng phẩy; `-k2,2` khoá 1; `-k3,3nr` khoá 2, `n` so như số, `r` đảo ngược = giảm dần); kết quả 4,2,5,6,1,3 ở step 1 (đã chạy `sort` thật ra đúng 4 2 5 6 1 3) | `jv2_sort_flags` |
| L07 | log₂ n | scale step cuối: ghi chú + câu nhắc lại "lôgarit cơ số hai của n là số lần nhân đôi từ một để tới n, chia đôi từ n về một cũng cần đúng ngần ấy lần" (bài đứng trước L02 đã giảng) | `assumes: [jv2_log2]` |
| L03 | `TreeMap::new`, tham số giữa của `groupingBy` | hook step 2 (lần đầu xuất hiện): ghi chú + lời đọc "tạo bản đồ có thứ tự mới … ba thứ: khoá để gom, nơi chứa, cách tính trong nhóm"; sym bảng: hàng tham chiếu hàm thêm "tham chiếu tới hàm tạo", hàng `groupingBy` thêm "tham số giữa (có thể bỏ) là nơi chứa"; pitfalls step 5 (`toMap` 4 tham số): "ba: Long::sum hợp nhất; bốn: TreeMap::new nơi chứa" | `jv2_ctor_ref` (introduces L03; assumes L09) |
| L08 | UTC, hậu tố `Z`, T | sym step 1 hàng Instant: UTC = giờ quốc tế (múi giờ lệch 0), mẫu `2026-03-08T07:30:00Z` với T ngăn ngày giờ, Z = UTC; lời đọc thêm hai câu | `jv2_utc` |
| L08 | `PT23H`, `P3M` | sym step 1 hàng Duration/Period: `PT23H` = 23 giờ, `P3M` = 3 tháng (P mở đầu một khoảng, T ngăn phần giờ, H giờ, M tháng); nhắc lại ở intuition step 3 (kết quả PT23H) | `jv2_iso_dur` |
| L08 | tên múi giờ IANA `Asia/Ho_Chi_Minh` | intuition step 1 (mã `ZoneId.of(…)`): ghi chú "tên múi giờ theo danh mục quốc tế (IANA), dạng châu lục/thành phố; dùng thay `UTC+7` vì luật giờ mùa hè đổi theo nơi và năm" | `jv2_iana` |
| L09 | `Consumer<GiaoDich>` | intuition step 4 (khung `DocSoCai`): ghi chú "kiểu của một hàm nhận một giao dịch và không trả gì (gọi bằng `khiDoc.accept(g)`)" + lời đọc | `jv2_consumer` |
| L09 | `ds::add`, `t::them` | intuition step 10 (App): "tham chiếu hàm gắn với đối tượng, viết tắt của `g -> ds.add(g)`"; step 13 (AppDong) nhắc `t::them` cùng cách | `jv2_bound_ref` |
| L09 | `static { … }` | intuition step 6 (NhatKy, nay tách hai step): "khối khởi tạo tĩnh, chạy đúng một lần khi lớp được nạp lần đầu" | `jv2_static_init` |
| L09 | `%02d` | scale step 0 (TaoSoCai): `String.format("%02d", 7)` ra `07`, tài khoản `A07`, `A42` | `jv2_fmt02d` |
| L09 | `tail -n +2` | check step 0: "in từ dòng thứ 2 trở đi, tức bỏ tiêu đề; `|` nối sang `wc -l`" | `jv2_tail` |
| L09 | `TreeMap::new` (dùng ở BaoCao) | bài đứng trước L03 đã giảng | `assumes: [jv2_ctor_ref]` (cùng `jv2_handler` cũ) |

Điểm P1 dự kiến: 2 ở 10/10 bài (L00, L01, L04, L05, L06 vốn đã 2; L02, L03, L07, L08, L09 nay không còn thuật ngữ dùng mà chưa giảng). Chưa có người đọc độc lập chấm lại: đây là dự kiến, không phải kết quả.

## 4. Độ dài (ước lượng thời lượng lời đọc, 150 từ/phút)

| Bài | Trước | Sau |
|---|---|---|
| L01 | 15,7 | 15,7 (2 356 từ) |
| L02 | 14,0 | 15,0 (2 253 từ) |
| L03 | 15,2 | 15,7 (2 358 từ) |
| L05 | 16,1 | 16,1 (không đổi lời đọc) |
| L06 | 14,0 | 14,3 (2 141 từ) |
| L07 | 15,7 | 16,0 (2 397 từ ≤ 2 400) |
| L08 | 14,3 | 15,0 (2 252 từ) |
| L09 | 16,5 | 16,0 (2 398 từ ≤ 2 400): thêm 6 thuật ngữ, cắt tương ứng ở hook, ôn lại, hình dung, công thức, quy mô, lỗi hay gặp, quiz, tổng kết; không bỏ mục tiêu nào |

L04 (16,4) và L05 (16,1) không thuộc phạm vi sửa lời đọc nên giữ nguyên, không thêm dài.
Câu `say` mới/đổi: 94 câu mới theo so với `.srt` cũ ở 7 bài (con số của L09 không đáng tin vì `.srt` L09 là bản dựng cũ); không câu mới nào < 8 từ hoặc > 38 từ (đã đo bằng script; hai câu mới ngắn 7 từ được nối dài lên 8–9 từ). Câu cũ ngắn của L09 (ôn lại, quiz, tổng kết) giữ nguyên.

## 5. Cổng đã chạy (số thật, sau sửa)

| Cổng | Kết quả |
|---|---|
| `verify_jv2` (có phép đo DuaTranh xác suất; không phải chạy lại) | 88/88 PASS (chạy hai lần, cả hai PASS; lần cuối sau mọi sửa) |
| `lv.py lint` L00..L09 | 0 FAIL, 0 WARN cả 10 bài |
| `lv.py render` 8 bài đã đổi | 0 vấn đề (L09 lần đầu tràn khung 36–38 do ghi chú `static`; đã tách bước NhatKy thành hai, render lại 0 vấn đề) |
| `lab_gate.py JV2` | 10 PASS · 0 FAIL (76 lab được bài tham chiếu) |
| `lv.py curriculum curriculum/jv2.yaml` | 10 bài, 10 đã có đặc tả, 0 lỗi |
| `check_curricula_graph.py` | 46 lộ trình, 728 bài, tham chiếu hỏng 0, chu trình 0, VER không PASS 0 |
| `tests/test_e52.py` | 0 FAIL |
| `screen_code.py check --course JV2` | 250 khối: PASS 348 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0 |
| `check_meta` / `check_next_refs` / `arith_scan` | 0 vấn đề / 551 lời hẹn, 0 lệch / 240 phép tính, 0 FAIL |
| `check_xref` | 14 lượt tham chiếu sang khoá khác, chỉ ở BNX (JV2: không có) |
| `check_course_refs` | hai lần chạy ở vòng kiểm giữa chừng không in vấn đề nào; lần chạy cuối quá chậm (quét toàn kho), chưa kết thúc khi viết báo cáo. Người điều phối chạy lại khi dựng. |

Khung hình đã xem sau render (≥ 3 mỗi bài đã đổi): L01 00094, 00096; L02 00075, 00082; L03 00006; L05 00088; L06 00022, 00118; L07 00150; L08 00017, 00032; L09 00032, 00036, 00045, 00087.

## 6. Mục không sửa, và lý do

- L00 heredoc `cat > … <<'EOF'` và `ClassNotFoundException`; L04 nhãn Spring ở hook; L05 `C(4,2)` và "lõi CPU"; L06 cờ JUnit `execute -cp out -c … --details=summary`: người đọc vẫn chấm P1 = 2 cho 5 bài này (đã liệt kê đủ cách, hoặc chỉ để đọc, lab không dùng). Không thêm chữ để khỏi kéo dài bài (L04, L05 đã ≥ 16 phút).
- L09 `parallel()` / `groupingByConcurrent`: báo cáo xếp "giải thích bằng chức năng", không phải chỗ kẹt; giữ nguyên.
- L03 hook step 2: dòng cuối của khối mã (`Collectors.groupingBy(…summingLong(GiaoDich::soTien)));`) nhô khoảng 8 px qua viền trong của khung mã (vẫn nằm trong thẻ ngoài, đọc được). Có từ trước, báo cáo không nêu; sửa cần đổi mã `ThongKe` (đổi số dòng của ba khối khác và sổ mã) nên để nguyên, ghi ở đây để người điều phối quyết.
- Sổ `term:` có thể bắt nhầm bài khác của khoá trong tương lai (ví dụ chữ UTC, Consumer dùng ở bài sau): lint sẽ báo E52 và người sửa phải `assumes` hoặc giảng lại.

## 7. Việc người điều phối cần làm

Dựng lại (TTS, ASR, build) L01, L02, L03, L05, L06, L07, L08, L09. Câu mới có chữ cái đọc rời, ASR có thể gắn cờ và cần xem xét, chưa kiểm bằng tai: L08 "U T C", "chữ T", "chữ Z", "P T hai mươi ba H"; L02 "chữ n", "chữ r" của cờ `sort`; L09 "hai dấu hai chấm". Đây là cách đọc theo thông lệ kho (xem `lexicon_vi.JV2.yaml` mục `foreign_ok`), chưa thử bằng ASR.
