# fix5 ACB (L00–L08), vòng 5 — theo R3_INT_ACB

## Tiến độ: 9/9 bài đã sửa. CẢ 9 BÀI ACB ĐỔI => CẦN DỰNG LẠI (build/tts/asr): L00, L01, L02, L03, L04, L05, L06, L07, L08.
Đã chạy `lv.py render` lần cuối cho L01, L03, L06 (các bài còn lại render sạch ở lần trước, sau đó chỉ sửa chữ trong L06); khung PNG mới ở `out/ACB/Lxx/frames`; chưa có mp4/srt mới. Đã xem các khung PNG L01 (49), L02 (61), L03 (71, 77), L04 (57), L05 (64), L06 (0, 41), L08 (79) khi sửa tràn.

## Cổng thật (chạy sau cùng)
- lv.py lint 9/9: 0 FAIL, 0 WARN (L00 31, L01 28, L02 35, L03 28, L04 29, L05 33, L06 29, L07 34, L08 30 PASS).
- lv.py render: 9/9 bài 0 vấn đề (đã sửa 7 chỗ tràn: L01 code+symbol, L02 code, L03 quymo, L04 code, L05 code, L06 symbol+hook, L07 code, L08 quymo).
- verify_acb.py: 287/287 PASS (thêm hàm `fixes5()` 30 kiểm cho mọi chỗ sửa: tính lại 33,3 s, 300 tiến trình, 5 ms, 0,065 s, thứ tự khử trùng/giữ tiền, nhãn Squad Lending, mốc UIT, hedge pháp lý, v.v.).
- lab_gate ACB: 9 PASS, 0 FAIL (196 lab) — chạy lại lần cuối ở nền (xem tin nhắn cuối).
- tests/test_e52.py 0 FAIL; lv.py curriculum curriculum/acb.yaml: 9 bài, 0 lỗi; check_course_refs ACB 0; check_next_refs 550 lời hẹn 0 lệch; arith_scan ACB 0 phép, 0 FAIL; check_legal ACB 111 lượt dẫn 0 FAIL; check_curricula_graph chạy được (không lỗi).
- screen_code check --course ACB: 62 khối, PASS 82, FAIL 0, MISSING 0, ORPHAN 0, **STALE 1**: `ACB L01 symbol 0 0` (sổ sha=aba0a48615307afc, thật=d92ca5e662ef39a5).
  **CẦN ĐIỀU PHỐI XỬ LÝ**: sổ tay (không thuộc phần sinh của gen_sc_acb.py) phải đổi `sha` thành `d92ca5e662ef39a5` và sửa `read_check`/`unverified_claims` của khoá đó (khuôn OFS không còn `:MV:SV`, nay là `TÊN.TRƯỜNG=GIÁ.TRỊ`; bài ghi "cú pháp rút gọn"). Tôi không tự sửa sổ (đã thử một lần rồi hoàn tác nguyên trạng). `audit/acb/gen_sc_acb.py` đã chạy lại (53 mục khối, 18 nguồn: sinh lại cảnh `code` L00–L08; L04 code thêm một step nên khoá đổi tự động; L05 code thêm một step).
- Lời đọc (tổng `say`, trần 2300): L00 2287, L01 1990, L02 2294, L03 2007, L04 1984, L05 2292, L06 2177, L07 2300, L08 2290.

## Chung
- Quyết định chung (fix5_INT_ACB.md): Squad Lending ghi "tên nhóm lấy từ một tin tuyển dụng đã lưu, chưa kiểm" ở ACB L00 quiz và L08 hook (tên bài/cảnh L08 đổi thành "Tín dụng bán lẻ", curriculum/acb.yaml L08 title đổi theo; tên tệp giữ nguyên); UIT "dự kiến tốt nghiệp cuối năm 2026" (hết "11/2026"); OCB "ngân hàng nơi bạn đang làm" ở L00, L01, L04, L07, L08; tin lương ACB "đã lưu, đọc tháng 11 năm 2026" ở L00 và L05.
- Pháp lý L06 theo chuỗi thống nhất với INT: "báo chí nêu; có nơi gắn Thông tư 50/2024 (đã được sửa đổi bởi Thông tư 77/2025), có nơi gắn Quyết định 2345; chưa đọc nguyên văn; chưa kiểm biên 'trên' hay 'từ'; không nêu số điều/phụ lục". Lint chặn cụm "bản gốc" (E29) nên dùng "chưa đọc nguyên văn". Đổi cùng lúc: tiêu đề bài, mục tiêu 1, hook, prereq, concept, recap, `curriculum/acb.yaml` (title + mục tiêu 1, covers không đổi). Thêm "ví dụ thiết kế, không phải quy định" cho hạn vé 3 phút, nhắc `hmac.compare_digest` (L06, L07).
- Term E52: thêm `acb_ttl` vào tools/registry/symbols.ACB.yaml (introduces ở L00 prereq, assumes ở L02). Không thêm term khác.
- Lab: chỉ ACB L00 đổi (dòng 3 đầu ra "dat P99" → "duoi 200", `vuot P99` → `vuot 200`): `labs/ACB/L00/de.md`, `mong_doi.txt`, `loi_giai.py`; mong đợi trên màn hình L00 khớp.
- Không còn TAB; CRLF giữ nguyên ở 9 YAML; các mục asr_reviewed mồ côi đã xoá bằng script riêng (L00 1, L01 1, L02 4, L03 1, L06 1; còn lại sạch).

## Từng bài (đổi gì; mục P1 chưa giảng còn lại theo ước lượng)
- L00 (P1≈0): giảng tại chỗ "0200/0210" (concept, nhãn SVG "0200 hỏi, 0210 đáp"), "NAPAS 247" = 24/7, TTL (prereq: màn hình + lời "viết tắt là tê tê e lờ"), OCB, Squad Lending (quiz). SHOULD: bỏ "đạt P99" (nói P99 không cộng được, 155 ms chỉ là ước lượng; mã in "duoi 200"; practice/lab đổi), quiz s2 thêm "có mạng đảo ngay khi hết giờ", UIT, ngày đọc tin lương. Cắt câu nhóm 1 "cũng có hỗ trợ mức 3" và câu thừa để giữ ≤ 2300.
- L01 (P1≈0): bỏ `MV:SV` khỏi khuôn OFS (nay `TÊN.TRƯỜNG=GIÁ.TRỊ`, ghi "cú pháp rút gọn, hỏi lại bản mô tả chính thức"), giảng COMPANY, mã FT; mã Python bỏ biểu thức sinh (hàm `ofs(app, opts, user, tid, tien)` với `kv = "DEBIT.AMOUNT=" + tien`, cùng đầu ra), thêm "cách đọc" `def`, `+`, `",".join`.
- L02 (P1≈0): concept vẽ lại thứ tự: 2 Cổng thanh toán (khử trùng lặp trước) → 3 Core Banking (giữ tiền) → 4 Switch, đường vòng về Core ở ô 3; recap cùng thứ tự; nhãn cột "lệnh mỗi giây lúc đỉnh"; "băm" → "chia theo tài khoản"; `format(bits,"016X")` giảng; mã giải mã đổi từ biểu thức liệt kê sang vòng `for … if … append` kèm cách đọc `range`, `append`; check s2 thêm hedge 0400.
- L03 (P1≈0): bí danh `e`/`pê` giảng (màn hình + lời), OTP nối với "mật mã dùng một lần"; quymo ×100 cần 3 tiến trình ở đỉnh 1500/giây (×10 000: 300; thêm check số); hook Kafka "mỗi ngăn nhỏ của chủ đề giữ đúng thứ tự".
- L04 (P1≈0): `:id`/`?`/`(7,)`/`.rowcount` giảng (step mới "Cách đọc hai chỗ lạ trong mã"), ba cột khoá, trạng thái REVERT (ghi chú dưới bảng + lời); "25 ms" → hai yêu cầu cách nhau 5 ms; "409 ngay, không chờ" → chỉ chờ bằng một câu cập nhật.
- L05 (P1≈0): hook/pitfall khớp số của quymo (10 000 lệnh 50 s, 1 triệu lệnh hơn một giờ); sao kê ×10 000 phân biệt chia đều (10 s) và chia theo ngày tối đa 30 đoạn (33,3 s); tiêu đề cảnh symbol bỏ "Bulk Collect"; mã bỏ `khoa.get(tk, ai)` thay `tk in khoa and khoa[tk] != ai` (cùng đầu ra) + step "Cách đọc điều kiện"; `INTO v_bal`, `r.acc` giảng; bảng check có cột hậu quả; ngày đọc tin lương.
- L06 (P1≈0): VNeID, `expires_at` (số giây từ 1/1/1970; step vé tách hai step, bảng nguyên lý an toàn); hedge pháp lý như trên; nhắc compare_digest.
- L07 (P1≈0): EOD, lũy đẳng (idempotent) giảng ở hook; 0,065 s ghi "chỉ tính phép so, cả đối soát cỡ 180 giây"; 3 triệu dòng = tổng mọi đối tác; compare_digest (step mới); LIKE '8888%' ghi "tuỳ hệ quản trị, chưa kiểm"; OCB.
- L08 (P1≈0): `ctx` (màn hình + lời "xê tê ích"), lũy đẳng giảng ở cảnh code; bảng điều phối thêm bước 1 "Tra CIC qua mTLS" (mục tiêu 4 có cảnh chạy từng bước, không đổi mục tiêu nên covers/curriculum không đổi) và step mới "Lỗi sau khi đã khoá sổ" (ký số lỗi/hết hạn ⇒ nhả khoá; nhả lỗi ⇒ ghi để đối soát); quymo CIC/giây là trung bình; Squad Lending có nhãn.

## Không sửa / mở
- STALE ledger ACB L01 symbol 0 0 (xem trên).
- ACB L01 quiz "hàng đợi riêng cho mỗi khách" (tuyệt đối, PLAUSIBLE), L02 hook "đặc tả NAPAS có thể là ISO 20022" (đã hedge "cần kiểm"), L03/L04/L08 ghi nhận "tính theo trung bình" chỉ sửa ở L03/L08; L04 "mã lỗi 68 NAPAS" thuộc INT. Không bịa số điều/phụ lục.
- Câu mới/đổi chưa nghe bằng tai người (ASR phải chạy lại sau dựng).
