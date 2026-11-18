# fix5 INT+ACB — vòng 5 theo R3_INT_ACB (P1 chuẩn chặt + SHOULD CONFIRMED + lỗi hiển thị + pháp lý)

## Sổ tác tử (ghi trước khi chạy)
- Điều phối: tác tử sửa vòng 5 (người quyết nội dung pháp lý/lương/Squad Lending/UIT chung).
- Fork INT: INT L00–L08 -> báo cáo chi tiết `fix5_INT_ACB_INT.md`.
- Fork ACB: ACB L00–L08 -> báo cáo chi tiết `fix5_INT_ACB_ACB.md`.
- Hai fork chạy song song (tổng 2 tác tử, dưới trần 4). Bị ngắt: tiếp tục bằng SendMessage.

## Quyết định chung INT↔ACB (một người quyết)
1. Squad Lending: ở MỌI chỗ nói "tên nhóm lấy từ một tin tuyển dụng đã lưu, chưa kiểm"; không viết như kinh nghiệm/chức danh thật của người học.
2. UIT: "dự kiến tốt nghiệp cuối năm 2026" (không còn "11/2026").
3. Ngưỡng sinh trắc học (10 triệu mỗi lần / 20 triệu mỗi ngày) ở INT L05, INT L06 và ACB L06 cùng một mức hedge: "báo chí nêu; có nơi gắn Thông tư 50/2024 (đã được sửa đổi bởi Thông tư 77/2025), có nơi gắn Quyết định 2345; chưa đối chiếu văn bản gốc; chưa kiểm biên 'trên' hay 'từ'; không nêu số điều/phụ lục".
4. OCB: lần đầu trong bài ghi "OCB, ngân hàng nơi bạn đang làm" (hoặc đúng cách các bài khác của khoá đã ghi).
5. Lương ACB: "Thương lượng", tháng 13 + thưởng 1–4 tháng theo tin ACB đã lưu, ghi "ngày đọc tin 2026-11, kiểm lại tin hiện hành".

## Tiến độ: 18/18 bài đã sửa. CẢ 18 BÀI ĐỔI => CẦN DỰNG LẠI (build/tts/asr): INT L00–L08, ACB L00–L08. Đã chạy lv.py render (khung PNG mới), chưa có mp4/srt mới.
Chi tiết: `fix5_INT_ACB_INT.md`, `fix5_INT_ACB_ACB.md`. Đổi ngoài YAML bài: `curriculum/int.yaml` (UIT), `curriculum/acb.yaml` (L06 hedge, L08 title "Tín dụng bán lẻ"), `labs/ACB/L00/{de.md,mong_doi.txt,loi_giai.py}` (P99), `audit/int/verify_int.py`, `audit/acb/verify_acb.py` (hàm fixes5), sổ `audit/review/screen_code/INT.yaml`, `ACB.yaml` (khoá sổ tay/sha; ACB L01 symbol 0 0 sha + read_check cập nhật tay theo tiền lệ vòng trước vì khuôn OFS đổi chữ), `tools/registry/symbols.ACB.yaml` (+acb_ttl).

## Cổng thật
- INT (fork): lint 9/9 0F/0W; render 9/9 0 vấn đề; verify_int 208 PASS; lab_gate INT 9 PASS; screen_code INT PASS 83, 0 STALE/MISSING/ORPHAN; test_e52 0 FAIL; curriculum int 0 lỗi; check_curricula_graph 0; arith_scan 246 phép 0 FAIL; check_course_refs 0; check_next_refs 0; check_legal 111 lượt 0 FAIL.
- ACB (fork): lint 9/9 0F/0W; render 9/9 0 vấn đề; verify_acb 287 PASS; lab_gate ACB 9 PASS (196 lab); test_e52 0 FAIL; curriculum acb 0 lỗi; check_course_refs 0; check_next_refs 0; arith_scan 0 FAIL; check_legal ACB 0 FAIL; screen_code ACB: fork báo 1 STALE (L01 symbol 0 0) -> điều phối đã sửa sổ; kết quả chạy lại cuối ở mục dưới.
- Lời đọc/bài (trần 2300): INT 2287/2289/2285/2285/2277/2293/2231/1850/2298; ACB 2287/1990/2294/2007/1984/2292/2177/2300/2290.

## Cổng điều phối chạy lại sau cùng (2026-11-15)
screen_code ACB 62 khối PASS 83, 0 STALE/FAIL/MISSING/ORPHAN; screen_code INT 60 khối PASS 83, 0; tests/test_e52 0 FAIL; lv.py lint 18/18 bài 0 FAIL 0 WARN (INT 35/32/26/34/31/39/30/37/44; ACB 31/28/35/28/29/33/29/34/30 PASS); lv.py curriculum int và acb: 9 bài, 0 lỗi.

## P1 chưa giảng còn lại (ước lượng của người sửa, chưa có người đọc xác nhận)
INT: L00 0, L01 0, L02 0–1, L03 0–1, L04 0–1, L05 0–1, L06 0–2 (đã giảng TLS/mTLS, IBM MQ, TCP, NAPAS, Spring, yêu cầu dở; bỏ ORDER BY…FOR UPDATE và OCB), L07 0–1, L08 0–1. ACB: tất cả ≈ 0 (biên 1 mục ở L02 "kênh truyền nhị phân", L04 "CIF").

## Pháp lý/chung (đã thống nhất INT↔ACB)
Cùng chuỗi hedge ở INT L05, INT L06, ACB L06 ("báo chí nêu... Thông tư 50/2024 (đã được sửa đổi bởi Thông tư 77/2025)... Quyết định 2345; chưa đọc nguyên văn; chưa kiểm biên "trên"/"từ"; không nêu số điều/phụ lục"; lint E29 cấm "bản gốc" nên dùng "chưa đọc nguyên văn"). Squad Lending ghi "tên nhóm lấy từ tin tuyển dụng đã lưu, chưa kiểm" ở ACB L00, ACB L08, INT L08. UIT "dự kiến cuối năm 2026" ở mọi chỗ.

## Không sửa / mở
- Số điều/phụ lục TT 50/77, QĐ 2345: cần người có văn bản gốc, ghi cùng lúc INT L05/L06 + ACB L06.
- INT L06 quiz phương án B vẫn dài nhất; ACB L01 quiz "hàng đợi riêng cho mỗi khách" (PLAUSIBLE) và ACB L02 hook ISO 20022 (đã hedge "cần kiểm") không sửa.
- Câu mới/đổi chưa nghe bằng tai người. Chưa đổi tên tệp `L07_salary_negotiation_50m_gross.yaml` (đề xuất ở fix4_INT_ACB_B.md).
