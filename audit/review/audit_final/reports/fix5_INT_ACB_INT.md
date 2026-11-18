# fix5 INT (fork INT) — 9/9 bài đã sửa

## KẾT LUẬN: CẢ 9 BÀI INT (L00–L08) ĐỔI => CẦN DỰNG LẠI (build/tts/asr). Đã chạy lv.py lint + render (khung PNG mới); chưa có mp4/srt mới.

## Bài đã sửa
| Bài | Đổi gì | Lời đọc | P1 chưa giảng (ước lượng) |
|---|---|---|---|
| L00 | kim tự tháp mở rộng (polygon 10..690) hết tràn "TẦNG 4"; lời đọc tầng hai "dịch vụ nhỏ, khung Spring Boot và kho dữ liệu Redis"; recap chuỗi dọc; step "Cách đọc đoạn mã" (525600 = 365×24×60, 10**-2, round, for); điều kiện "nếu mỗi yêu cầu giữ một kết nối"; UIT "cuối năm 2026"; tin ACB "đọc 2026-11, kiểm lại tin hiện hành" | 2287 | 0 |
| L01 | Full GC có điều kiện (G1/ZGC giảm mạnh); step "Cách đọc mã Java" + step "Cách chạy" (javac/java, JDK 21); step đọc Python (while, *=, cao,suc = 0,1, 10**4); nano giây = một phần tỉ giây; "0,5" | 2289 | 0 |
| L02 | Singleton/trạng thái khả biến + PostConstruct giảng; failover; "đổi ngữ cảnh"; tên khoá thống nhất `trans:{requestId}` + giải `{requestId}`/TTL; rủi ro REQUIRES_NEW cạn bể (số giao dịch chính < cỡ bể); step đọc Java (setIfAbsent, `!`, 409, try/catch, 202) + step đọc Python | 2285 | 0-1 |
| L03 | sơ đồ SAGA có mũi tên ra lệnh + mũi tên đỏ nét đứt bồi hoàn; FK bung chữ ở chỗ dùng đầu tiên; WAL/redo log = cuốn sổ ghi mọi thay đổi; sendfile/page cache/socket buffer/4 đối số; step đọc PL/SQL (:=, LEAST, SELECT INTO, BULK COLLECT LIMIT, EXIT WHEN, FORALL) + step đọc Python; "mô hình rút gọn" cho 2PC/SAGA; recap chuỗi dọc tách 2 step | 2285 | 0-1 |
| L04 | 17 phút vs 300 giây (khoá 300 s hết hạn trước nên chưa chặn nhầm; chỉ chặn nhầm nếu khoá sống > 17 phút); bản tin mẫu thêm trường 7 và 41; step đọc Python (<<, [-13:-1], :016X, int(,16), ^) + step đọc Python quymo; câu CV T24/OCB thêm "theo hồ sơ của bạn ... kể đúng phần việc thật" | 2277 | 0-1 |
| L05 | hedge pháp lý (dưới); "mô hình đồ thị", "mạng nơ-ron sâu" giải nghĩa; step đọc Java ONNX (khối số/tensor), Python ucb, Python quymo; JSON gloss; UIT cuối năm 2026; OCB "ngân hàng nơi bạn đang làm" + "theo hồ sơ" | 2293 | 0-1 |
| L06 | TLS/mTLS, IBM MQ, TCP, NAPAS, Spring giải nghĩa (sơ đồ ghi chú rõ + bảng giải nghĩa riêng + lời đọc); "yêu cầu dở" = yêu cầu đã nhận chưa xong, ví dụ 100×2=200 (step riêng); bỏ "ORDER BY...FOR UPDATE"; bỏ OCB (nơi bạn từng làm); hedge pháp lý; step đọc SQL UPDATE/SET/WHERE, đọc Python | 2286 | 0-1 |
| L07 | example s2: câu mẫu minh hoạ, chỗ điền [năm]/[nơi làm], bỏ tên công ty/năm thật (hết chồng freelance/Grooo); UIT cuối năm 2026; ghi ngày đọc tin ACB; step đọc Python (for/range, +=, *=, in) | 1850 | 0-1 |
| L08 | "ba lớp" -> "hai lớp chặn + một lớp phát hiện" (mục tiêu, bảng, lời đọc, recap nhất quán); Squad Lending "lấy từ tin tuyển dụng đã lưu, chưa kiểm" (màn hình + lời đọc); step giải nghĩa tài sản bảo đảm/cầm cố/tín chấp; step đọc mã giả (&&, .size(), .rrn, ++, ==, giả định RRN duy nhất); step đọc Python; ghi chú thứ tự phong toả là minh hoạ | 2298 | 0-1 |

Ghi chú P1: tất cả mục trong danh sách R3 mục 6 của INT đã được giảng tại chỗ (lời đọc + màn hình) hoặc bỏ khỏi đường chính; mục còn lại là các từ tên riêng/kỹ thuật nhẹ (ví dụ JBoss/JSP, Debezium, ADR) và cú pháp nhỏ chưa tách. Mỗi bài ước lượng ≤ 1 mục.

## Chuỗi hedge pháp lý đã dùng (INT L05 example + L06 check; ACB L06 cần cùng mức)
Màn hình: "báo chí nêu, chuyển tiền trực tuyến của khách cá nhân [trên 10 triệu đồng một lần hoặc tổng trong ngày trên 20 triệu đồng] phải xác thực khuôn mặt/sinh trắc học. Có nơi gắn ngưỡng này với Thông tư 50/2024/TT-NHNN (đã được sửa đổi bởi Thông tư 77/2025/TT-NHNN), có nơi gắn với Quyết định 2345/QĐ-NHNN; chưa đọc nguyên văn các văn bản này, chưa kiểm biên "trên" hay "từ"; bài không nêu số điều hay phụ lục."
Lời đọc L05: "Theo báo chí, ... Có nơi gắn ngưỡng này với Thông tư 50 năm 2024, đã được sửa đổi, có nơi gắn với Quyết định 2345, và tôi chưa đọc nguyên văn." L06: "Ngưỡng mười triệu mỗi lần và hai mươi triệu mỗi ngày do báo chí nêu, tôi chưa đọc nguyên văn, nên làm thật bạn phải mở văn bản hiện hành."
Lưu ý: lint E29 cấm cụm "bản gốc/văn bản gốc" nên dùng "chưa đọc nguyên văn" thay "chưa đối chiếu văn bản gốc". `source:` ở front-matter L05/L06 giữ như vòng trước.

## Quyết định chung đã áp dụng
Squad Lending (INT L08 nhãn "chưa kiểm" ở màn hình + lời); UIT "dự kiến cuối năm 2026" ở L00, L05, L07 và `curriculum/int.yaml` (3 chỗ); lương ACB ghi "đọc 2026-11, kiểm lại tin hiện hành" (L00, L07); OCB: L04/L05 "ngân hàng nơi bạn đang làm", L06 bỏ OCB; không đổi ACB.

## Cổng thật (chạy lại sau sửa)
- lv.py lint 9/9: 0 FAIL, 0 WARN (PASS 35/32/26/34/31/39/30/37/44). lv.py render 9/9: 0 vấn đề (L00 105 khung, L01 105, L02 103, L03 97, L04 99, L05 101, L06 102, L07 93, L08 106).
- verify_int: 208 PASS, 0 FAIL (sửa verify_int: L06 quymo khối mã ở step 1 và 3; kiểm UIT "cuối năm 2026" thay "11/2026").
- lab_gate INT: 9 PASS, 0 FAIL (196 lab). tests/test_e52.py: 0 FAIL. lv.py curriculum curriculum/int.yaml: 9 bài, 0 lỗi. check_curricula_graph: 0 lỗi. arith_scan: 246 phép, 0 FAIL. check_course_refs INT: 0. check_next_refs: 550 lời hẹn, 0 lệch. check_legal: 111 lượt dẫn, 0 FAIL.
- screen_code INT: 60 khối, PASS 83, FAIL/STALE/MISSING/ORPHAN/WARN 0.
- Tổng lời đọc (say) mỗi bài đều ≤ 2300 (cao nhất L08 2298, L05 2293).

## Đổi ngoài YAML bài
- `curriculum/int.yaml`: 3 mục tiêu/fix ghi "cuối năm 2026" (đồng bộ mục tiêu bài).
- `audit/int/verify_int.py`: mô tả ở trên.
- `audit/review/screen_code/INT.yaml` (sửa khoá sổ tay như vòng trước): `INT L06 quymo 0 0/0 1/1 0/1 1` -> `1 0/1 1/3 0/3 1` (chèn step trước và giữa); `INT L01 example 4 0` -> `6 0` (chèn 2 step); sha mới `INT L02 symbol 1 0` (tên khoá Redis `trans:{requestId}`, read_check cập nhật) và `INT L04 symbol 1 0` (thêm trường 7, 41; read_check ghi thêm).
- Mục asr_reviewed mồ côi (câu đã đổi) đã xoá: L03 (1), L04 (1), L05 (1), L06 (1), L08 (2).

## Không sửa / mở
- Câu hỏi trắc nghiệm L06: phương án B vẫn dài nhất (SHOULD nhẹ, chưa cân độ dài).
- ASR/tai người: các câu mới/đổi chưa nghe bằng tai.
- Đối chiếu văn bản gốc TT 50/77, QĐ 2345 (số điều, phụ lục, biên "trên/từ"): vẫn cần người có văn bản gốc, làm đồng thời INT L05/L06 và ACB L06.
- Đổi tên tệp `L07_salary_negotiation_50m_gross.yaml`: không làm (như vòng 4).
