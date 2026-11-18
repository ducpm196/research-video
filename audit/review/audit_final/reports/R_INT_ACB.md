# S01 INT+ACB: đã đọc 17/17 bài (INT L00–L07, ACB L00–L08), 2026-11-14

Người đọc độc lập. Đọc trọn YAML (title, objectives, mọi `show`/`say`, checks, quiz), `curriculum/int.yaml`, `curriculum/acb.yaml`, `resources/job/JD.md` (cả phần VPBank cuối tệp), BRIEF_READ_S01 + sample_f/BRIEF + ADDENDUM. Không mở `reports/*` khác, `plan_*`, `handover_*`. Không sửa tệp nào trong kho ngoài báo cáo này. Tệp tạm: scratchpad `.../ria/`.

Quy ước chấm P1: người học đã học FND, JVA, JV2, PYT, BNK, BNX nên thuật ngữ của các khoá đó (thread, synchronized, index, Spring, SQL) tính vào cột "Cần biết trước", không trừ P1.

## 0. Kết luận theo ngưỡng

| Ngưỡng | Kết quả |
|---|---|
| MUST = 0 | **KHÔNG ĐẠT: 2 MUST** (M1 video chưa dựng lại cho 12/17 bài; M2 lab ACB L08 đề ≠ đáp án mong đợi). Nội dung YAML: 0 lỗi kiến thức MUST. |
| P1 = 2 ≥ 90% | ĐẠT: 16/17 = 94% (INT L05 = 1) |
| P8 = 2 = 100% | ĐẠT: 17/17 (ACB L08 vẫn là 2 vì màn hình khớp `mong_doi.txt`; lỗi nằm ở `de.md`, tính ở M2) |

## 1. Bảng chuẩn xác (chỉ lỗi có bằng chứng)

### MUST

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| M1: INT L05, L06, L07; ACB L00–L08 (12 bài) | MUST | toàn bài (mp4, srt, chapters, _frames.txt) | INT L07.srt dòng 15, 43, 135: "mức lương năm mươi triệu gross … bảy trăm đến tám trăm năm mươi triệu"; chapters.txt: "Nghệ thuật Đàm phán Mức lương 50 Triệu Gross"; ACB L06.srt dòng 3, 35: "đã ban hành Quyết định 2345 … ba quy tắc vàng trong Quyết định 2345" | `stat`: 12 mp4/srt/chapters/_frames.txt mang ngày 2026-11-10 (build_report `built_at` 2026-11-10T16:xx), YAML 2026-11-14 08:02–08:49; chỉ `frames/*.png` + `_capture.html` được dựng lại 11-14 (ví dụ ACB L06 `_frames.txt` 63 mục, thư mục `frames/` 102 ảnh). Người học xem mp4 sẽ nghe lại đúng điều AF2 đã gỡ: số lương 50 triệu không nguồn (INT L07), QĐ 2345 là căn cứ không kèm "chưa đọc" (ACB L06), và thiếu cảnh quy mô + lab (chapters ACB L07 chỉ 9 chương, không có "Quy mô", "Tự làm"). 5 bài INT L00–L04 mp4 dựng 11-14 09:01–09:33 sau YAML: mới. | Dựng lại mp4/srt cho 12 bài trước khi giao người học | CONFIRMED |
| M2: ACB L08 | MUST | practice + `labs/ACB/L08/de.md` mục 4 | `de.md`: "`giai ngan lan 1: chi tien` và `giai ngan lan 2: trung khoa, bo qua`"; màn hình + `mong_doi.txt`: "giai ngan lan 1 chi tien" (không dấu hai chấm) | Tôi làm đúng theo `de.md` (mau.py in có dấu hai chấm): `bash labs/cham.sh ACB L08 mau.py` → "KHÁC mong đợi: < giai ngan lan 1: chi tien / > giai ngan lan 1 chi tien" (2 dòng). Bỏ dấu hai chấm → ĐÚNG. 8 lab ACB còn lại làm theo `de.md` ra ĐÚNG ngay. | Sửa `de.md` L08 mục 4: bỏ hai dấu hai chấm | CONFIRMED |

### SHOULD

| Bài | Cảnh/step | Trích nguyên chữ | Vì sao + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| INT L00, INT L06, `labs/INT/L00` | L00 practice step 0/1/2; L06 prereq step 2 | "Oracle, MS SQL, JBoss, viết bản thiết kế, hỗ trợ mức 3 theo SLA … nhóm B"; "Hệ cũ, bản thiết kế, mức 3 là nhóm B" | JD.md dòng 190–191, 198: Senior Java Backend và Payment Hub TA171 (nhóm microservices) cũng "hỗ trợ ticket Production"/"Hỗ trợ L3"; VPBank Securities (nhóm mới) có Oracle. "Sở hữu một mảng nghiệp vụ + hỗ trợ mức 3" lấy từ phần TA192 mà JD.md dòng 179 tự ghi chưa kiểm chứng (trang bị cắt). Chính bài ghi "hỗ trợ vận hành … hầu hết tin đều cần". Phân biệt thật chỉ còn JBoss/JSP + SQL Server + sở hữu nghiệp vụ. "Hai nhóm" đúng JD ở mức tổng quát (JD.md dòng 127–131, 172). | Lời giải nói rõ JBoss/JSP là dấu hiệu chính; mức 3 và bản thiết kế có ở cả hai nhóm | CONFIRMED (đối chiếu JD.md) |
| ACB L08, INT L00 | L08 recap step 1; L00 concept step 3 | "nhiều tin tuyển dụng ngân hàng (bản đã lưu, chưa kiểm lại) mô tả vị trí giữ một mảng … phê duyệt tín dụng" | JD.md chỉ có một tin kiểu này (VPBank TA192, chưa kiểm chứng) cộng một tin ECM/BPM; "nhiều" nói quá | Đổi "nhiều" thành "một số" hoặc "ít nhất một" | PLAUSIBLE |
| INT L04 (check + quiz), INT L04 curriculum obj 6 | check step 0, step 1 | "mã phản hồi 68 (Giao dịch đang nghi vấn do ngân hàng thụ hưởng chưa trả lời kịp)"; "Mã lỗi 68 có nghĩa là ngân hàng thụ hưởng có thể đã cộng tiền" | Dòng `source` ghi "đặc tả kết nối NAPAS 247 chưa kiểm được"; ISO 8583 gốc: 68 = "response received too late". Màn hình khẳng định nghĩa NAPAS không kèm "cần kiểm" (các bài ACB L02 có kèm). | Thêm "(theo cách gọi phổ biến; đặc tả NAPAS cần kiểm)" | PLAUSIBLE |
| INT L04 (source, quiz CIC), ACB L08 (source, quiz) | prereq/concept step 2; L08 quiz step 1 | "Nợ chia 5 nhóm theo TT 31/2024/TT-NHNN: quá hạn 10–90 ngày là nhóm 2" | WebSearch (luatvietnam, lawnet): nhóm 2 = 10–90 ngày, nhóm 3 = 91–180 ngày khớp; nhưng TT 31/2024 đã được sửa bởi TT 37/2025/TT-NHNN (31/10/2025); cả hai bài không nhắc. INT L04 màn hình không ghi "nguồn thứ cấp" như dòng source. | Thêm "đã được TT 37/2025 sửa đổi một số điều; mở bản hợp nhất" | CONFIRMED (có sửa đổi); PLAUSIBLE (nội dung nhóm 2 giữ nguyên) |
| INT L05 step 3 (example), INT L06 check step 0, `labs/INT/L06/de.md` | | "QĐ 2345/QĐ-NHNN (ký 18/12/2023, hiệu lực 01/07/2024): bắt buộc xác thực sinh trắc học khi … trên 10 triệu … tổng … trên 20 triệu" | ACB L06 cùng khoá học ghi rõ "chưa đọc nguyên văn, chưa rõ còn áp dụng hay đã được Thông tư thay" và dùng TT 50/2024 sửa bởi TT 77/2025. Hai khoá tự mâu thuẫn. WebSearch (lsvn, MSB, vietnamnet): ngày hiệu lực 1/7/2024 và ngưỡng 10/20 triệu đúng; các nguồn không xác nhận QĐ 2345 còn hiệu lực sau TT 50/2024 (hiệu lực 1/1/2025). | Dùng cùng câu cảnh báo như ACB L06 | CONFIRMED (mâu thuẫn); PLAUSIBLE (lỗi thời) |
| ACB L06 | title, svg tầng "Kiến trúc Cổng Sinh trắc học Quyết định 2345", recap title; prereq step 0 hàng 3 | tiêu đề "Xác thực Sinh trắc học Quyết định 2345 …"; "Sau mỗi lần xác thực thành công, tổng cộng dồn tính lại từ 0" | Tiêu đề/nhãn lấy văn bản chưa kiểm làm căn cứ trong khi thân bài dùng TT 50/2024. Quy tắc "tổng về 0" nằm trong bảng đề "theo Thông tư 50/2024 … sửa đổi" nhưng không có nguồn (bài không nêu số điều), lab dựa vào nó. Bài đã tránh khẳng định số điều: ĐẠT. | Đổi tiêu đề; gắn nhãn "giả định của mô phỏng" cho quy tắc về 0 | PLAUSIBLE |
| INT L06 hook, `interview/06_…md`, `interview/07_…md`, ACB L00 quiz | hook; L00 quiz step 0 | hook: "trọn bộ 100 câu … nằm trong tệp câu hỏi đi kèm (interview/06_interview_qa_bank_100.md)"; ACB L00: "chỉ nhận 35 đến 40 triệu" | Video INT L07 (YAML) không còn số lương không nguồn: ĐẠT (mọi số là "số minh hoạ", số ACB có nguồn JD.md dòng 72, 79). Nhưng tệp đi kèm mà hook chỉ tới vẫn có: dòng 3 "bảo vệ vững chắc mức lương 50,000,000 VND Gross", dòng 720 "Khung lương 3 năm thường chỉ ở mức Middle (35–40M)" (không nguồn), interview/07 dòng 58, 68, 69 "42,000,000 … khung lương nội bộ", "46,000,000 + 4,000,000"; Câu 76 nêu tên người thật. Tệp nằm ở `interview/`, không ở `labs/`. ACB L00 quiz dùng "35 đến 40 triệu" không gắn "số minh hoạ". Tên tệp bài `…50m_gross` còn số. | Gắn "số minh hoạ" hoặc bỏ; đưa tệp 100 câu vào gói người học hoặc bỏ đường dẫn trên màn hình | CONFIRMED |
| ACB L03 | example step 2 | "SET noti:sent:{event_id} 1 EX 86400 NX … Chỉ đặt khoá sau khi nhà mạng xác nhận đã nhận tin, hoặc xoá khoá khi gửi lỗi"; say: "miễn là khoá chỉ được đặt sau khi nhà mạng xác nhận" | NX đặt trước khi gửi (claim rồi xoá khi lỗi) mâu thuẫn "đặt sau khi xác nhận"; kiểu "kiểm rồi đặt sau" không nguyên tử, hai bản trùng đồng thời cùng qua. Bài trình bày cả hai như một. | Chọn một cách: NX trước, xoá khi lỗi; nói rõ rủi ro mất khoá khi sập giữa chừng | CONFIRMED (suy luận) |
| ACB L05 | example step 3 vs quymo step 1 | "chia 4 đoạn: 7 + 7 + 7 + 9 = 30 ngày … xong trong khoảng 2,5 giây" | 2,5 s = 1 triệu / 4 / 100 000 chỉ đúng khi 4 đoạn bằng số bản ghi; chia theo ngày 7/7/7/9 thì đoạn 9 ngày có 300 000 bản ghi = 3,0 s | Nói "chia đều số bản ghi" hoặc đổi 3 giây | CONFIRMED (tính lại) |
| ACB L00 quymo, ACB L02 quymo | L00 quymo step 0 say; L02 quymo step 0 say | "một cụm Redis không còn gánh nổi 60 triệu khoá" / "48 triệu khoá, một cụm Redis không đủ" | 60 triệu khoá nhỏ cỡ vài GB vừa một máy; nút nghẽn thật là 1 triệu ghi/giây (L00) hay 800 000/s (L02) | Nêu nút nghẽn là thông lượng ghi | PLAUSIBLE |
| ACB L00 quiz, ACB L02 check, INT L04 check | L00 quiz step 1 | L00: "gửi thông báo đảo MTI 0420 (Reversal Advice) hoặc tra soát"; L02: "0420 nếu đặc tả quy định (cần kiểm)"; INT L04: "MTI 0400 là yêu cầu đảo" | Ba bài nói ba kiểu; gửi đảo khi nghi vấn thực chất là hoàn tiền, trái câu "không hoàn tiền ngay" cùng bài | Dùng chung câu của L02 | PLAUSIBLE |
| INT L04 | cả bài | 2296 từ lời đọc (cao nhất INT; trung bình 17 bài = 1 975) | Quá tải: ≥ 20 thuật ngữ mới (OFS, MTI, bitmap, STAN, RRN, khối PIN, XOR, HSM, TPK/ZPK/ZMK/LMK + 4 lệnh payShield, MAC, LTV, DTI, CIC, AZ, CASA, Cloud CA, OTP, B2B, EOD, TimSort, O()) trong 9 cụm chủ đề; bảng lệnh HSM (CA/CC/JE/JC) hiện trên màn hình nhưng lời đọc không đọc; lab 4 ý khác nhau. Video 15,2 phút (frames) vs 13–14 phút các bài INT khác. ACB L05 (2222 từ) cũng cao nhưng chỉ một cụm. | Tách hai bài (T24/OFS/ISO 8583/PIN; tín dụng + đối soát) | PLAUSIBLE |
| INT L02 | check, recap | cảnh Bloom Filter, recap mục 5 | Không có trong 8 mục tiêu/curriculum (mục tiêu 7 chỉ nói Filter/Interceptor/Aspect); REQUIRES_NEW: không nhắc bế tắc cạn bể (2 kết nối/giao dịch) | Thêm mục tiêu hoặc bỏ | CONFIRMED |
| INT L00 step 2 | example | "khi dòng chưa tồn tại, câu lệnh đó không khoá được gì" | Đúng Oracle/PostgreSQL; MySQL InnoDB có khoá khoảng (gap lock). Thiếu điều kiện áp dụng | Thêm "trên Oracle/PostgreSQL" | PLAUSIBLE |
| INT L03 | example step 4 | "Từng dòng: khoảng 10 000 × 2 = 20 000 lần đổi ngữ cảnh" | Oracle ≥ 10g tự lấy mảng 100 dòng trong cursor FOR loop; mô hình hai lần/dòng là đơn giản hoá (bài ghi "khoảng") | Ghi "mô hình đơn giản hoá" | PLAUSIBLE |
| INT L05 recap; ACB L01; ACB L04; ACB L00/L01 | L05 recap bảng; L01 step 2 say; L04 svg; L00 obj 1 vs hook | "giảm đáng kể bế tắc khoá"; "Tuyệt đối không dùng chung một hàng đợi hai chiều"; "2. Fiber API Gateway"; objective "không phải thiết kế nội bộ của ngân hàng nào" vs màn hình "kiến trúc tham chiếu rút từ kinh nghiệm làm ở OCB" | Khẳng định không số/tuyệt đối; Fiber là web framework không phải gateway; mục tiêu và màn hình lệch nhau về nguồn kiến trúc. Không bài nào khẳng định ACB dùng T24 (ĐẠT: mọi bài nhắc "tin tuyển dụng ACB không nói ACB dùng hệ core nào"). | Sửa chữ | PLAUSIBLE |
| ACB L07, INT L04 | L07 quymo; L04 example | 1e8 phép/s → 25 giờ vs 1e9 phép/s → 2,5 giờ cho cùng N = 3 triệu | Hai khoá, hai tốc độ giả định; đều ghi "số minh hoạ" nhưng người học thấy hai đáp số | Thống nhất giả định | CONFIRMED |
| INT L05, INT L06 | check/quiz | "Xin nghỉ phép dài ngày"; "Chỉ ngồi đợi đồng nghiệp giao việc" | Phương án sai quá hiển nhiên: kiểm lẽ thường, không kiểm hiểu (P5 = 1) | Thêm phương án gần đúng | PLAUSIBLE |
| ACB L07 lab | `de.md` | "có ở Core, không có ở NAPAS → `loi chuyen tien NAPAS, tra soat` … trường hợp khác → `bat thuong`" | Hai phân loại không có trên màn hình bài (ma trận 4 kịch bản); người học phải suy ra | Thêm hai dòng vào bảng màn hình | CONFIRMED |
| INT L00–L03, INT L04 | `asr_report.md` | | Còn câu "chưa xem xét": L00 4, L01 2, L02 3, L03 6; ASR L04 `checked_at` 2026-11-10 trước mp4 11-14 | Xem xét nốt | CONFIRMED |

Không phát hiện lỗi kiến thức MUST trong 17 YAML. Đã xác nhận đúng: ISO 8583 MTI/bitmap/MAC trường 64–128, khối PIN ISO 9564 định dạng 0 và lệnh Thales CA/CC/JE/JC, RFC 9457 (2023, thay RFC 7807), công thức HikariCP, JEP 444 và JEP 491 (Java 24), `-XX:-RestrictContended`, `spring.threads.virtual.enabled`, Kafka acks/min.insync.replicas/idempotence, zero-copy mất khi bật TLS, Kafka giữ mặc định 7 ngày, Oracle huỷ câu lệnh khi ORA-00060, ksqlDB stream–table join (stream–stream cần WITHIN), SRE "bốn tín hiệu vàng", Luật BVDLCN 91/2025/QH15.

## 2. Bảng độ sâu (một dòng mỗi bài)

Phút = từ thời lượng `frames` mới (INT L00–L04, mp4 mới) hoặc ước từ số từ lời đọc ÷ 150 (dấu ~; mp4 cũ chỉ 5–8 phút nên không dùng).

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | P8 | P9 | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| INT L00 | 026eb1e5bbd65d75 | 14,2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | SQL INSERT, Heap, Oracle/MS SQL | nhóm A/B dựa vào "mức 3" (xem SHOULD) |
| INT L01 | 477fc80f6b2b18c4 | 13,3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | luồng/thread, synchronized, chỉ mục, context switch, Tomcat | không |
| INT L02 | f02e3e95becb6f9d | 13,3 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 13 | 2 | 2 | ĐỦ | Servlet/DispatcherServlet, Controller, thread-safety | Bloom Filter ngoài mục tiêu |
| INT L03 | ed4b107d30a4b8be | 13,1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | WAL/redo log, SQL, PL/SQL, FOR UPDATE | mô hình đổi ngữ cảnh đơn giản hoá |
| INT L04 | 04f26f47a393dab2 | 15,2 | 2 | 1 | 1 | 2 | 2 | 2 | 1 | 11 | 2 | 2 | GẦN | TCP, XML/JSON, hex | quá tải; bảng lệnh HSM không đọc; bitmap/PIN chỉ chữ |
| INT L05 | 2a6e52df0da4858a | ~12,9 | 1 | 2 | 2 | 2 | 1 | 1 | 2 | 11 | 2 | 2 | GẦN | ln, độ lệch chuẩn, tích vô hướng, embedding 384 chiều, Kafka | Isolation Forest chỉ nêu tên; quiz lẽ thường |
| INT L06 | 9d2fa92b87b8938f | ~12,5 | 2 | 2 | 2 | 2 | 1 | 1 | 1 | 11 | 2 | 2 | GẦN | API Gateway, Outbox/CDC, Kafka cụm đôi, SLA | bộ 100 câu không có trong video; thiết kế 4 tầng 1 dòng/tầng |
| INT L07 | ef0f1a2d7eba8473 | ~11,7 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | thuế TNCN/BHXH (chỉ gross, không tính net) | không có net |
| ACB L00 | ffa8db6621120840 | ~13,2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | @Transactional, Oracle | quiz "35–40 triệu" chưa gắn minh hoạ |
| ACB L01 | 14f39dafb4a09be8 | ~12,1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | queue manager, broker, thread | không |
| ACB L02 | 84ec2fd22c99ff5e | ~13,6 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | dịch bit (đã giảng), hex | không |
| ACB L03 | 786ecfa9b9df6976 | ~12,0 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 13 | 2 | 2 | ĐỦ | Kafka partition, SQL JOIN | khử trùng NX vs "đặt sau" mâu thuẫn |
| ACB L04 | e319e79a1346a939 | ~11,8 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | SQL UPDATE, MVCC (chỉ nhắc), Go (đã giảng) | không |
| ACB L05 | ffaaaaa048b162ee | ~14,8 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | PL/SQL, Kafka Streams | chu trình chờ chỉ chữ/bảng, không vẽ; 2,5 s vs 3,0 s |
| ACB L06 | 3657fdc1fc713007 | ~12,4 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 13 | 2 | 2 | ĐỦ | HMAC (đã giảng), CCCD | tiêu đề "QĐ 2345"; quy tắc về 0 không nguồn |
| ACB L07 | 9bb475841db25d63 | ~13,5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | 2 | 2 | ĐỦ | LIKE/B-Tree, Redis | 2 loại phân loại lab không có trên màn hình |
| ACB L08 | f9af3de540e9cc8b | ~13,6 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 13 | 2 | 2 | ĐỦ | Go (đã giảng), sqlite | objective 5 gán chặn duyệt cho TT 31/2024 (TT chỉ định nghĩa nhóm; chặn là chính sách ví dụ) |

(sha16 = sha256 16 ký tự đầu của YAML lúc đọc; mọi tệp đọc trong một phiên, không đổi.)

## 3. Lab

Làm như người học: đọc `de.md`, tự viết `mau.py` trong scratchpad không mở `loi_giai.py` trước, chấm `bash labs/cham.sh`. INT: `cham.sh` trả "chưa hỗ trợ đuôi tệp này" cho `.md` (đúng như `de.md` ghi), nên tính tay bằng Python rồi `diff` với `mong_doi.txt`. Thời gian là thời gian máy của tôi (viết + chạy), không phải ước lượng thời gian người học; người học ước 15–45 phút/bài (de.md ghi pause 150–300 s cho phần tự làm).

| Bài | tự làm được | thời gian (máy) | kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| INT L00–L07 | có (giấy bút, 3–7 dòng) | < 1 phút mỗi bài | L00: dòng nhóm A/B mơ hồ vì "mức 3" ở cả hai nhóm; còn lại không | 8/8 khớp từng dòng; tính lại độc lập 8/8 khớp `mong_doi.txt`; không có chấm máy |
| ACB L00 | có | ~1 phút | không | ĐÚNG; khớp màn hình |
| ACB L01 | có | ~1 phút | không (đề định nghĩa rõ phần đầu/phần cặp) | ĐÚNG |
| ACB L02 | có | ~2 phút | không (đề đã nói trường 128 → vị trí 64) | ĐÚNG |
| ACB L03 | có | ~2 phút | xô thẻ: phải tự suy ra cộng giây trôi (có gợi ý ở step 2) | ĐÚNG |
| ACB L04 | có | ~1 phút | không | ĐÚNG |
| ACB L05 | có | ~2 phút | mô phỏng vòng chờ (đề đủ luật) | ĐÚNG |
| ACB L06 | có | ~2 phút | không | ĐÚNG |
| ACB L07 | phần | ~2 phút | hai phân loại (`loi chuyen tien NAPAS`, `bat thuong`) chỉ có trong de.md | ĐÚNG |
| ACB L08 | phần | ~2 phút | `de.md` ghi "giai ngan lan 1: chi tien", mong đợi là "giai ngan lan 1 chi tien" → KHÁC (M2); đổi theo mong_doi thì ĐÚNG | `mong_doi.txt` khớp màn hình; ĐÚNG sau khi bỏ dấu hai chấm |

Chạy thêm `loi_giai.py` 9/9 ĐÚNG (kiểm chéo).

## 4. Người học kẹt ở đâu (chỗ đầu tiên không theo được)

- INT L00: concept step 3 / practice: gán tin tuyển dụng nhóm A hay B bằng "hỗ trợ mức 3, bản thiết kế" trong khi cùng bài nói hai thứ này ở hầu hết tin.
- INT L01: example step 2 "chặn vào ra bên trong synchronized" (synchronized chưa giảng; người học JVA đã biết).
- INT L02: quiz "Filter … Web Container … DispatcherServlet" chưa giảng (người học JVA/JV2 đã biết).
- INT L03: concept step 1 "đọc nhật ký giao dịch của cơ sở dữ liệu (WAL / redo log)".
- INT L04: prereq step 2 "Lệnh HSM (họ Thales payShield): CA … CC … JE/JC … TPK/ZPK/LMK" bảng dày, lời đọc bỏ qua.
- INT L05: symbol step 0 "Score_k = μ̂ + c√(ln N / N_k)" (ln, "cận tin cậy trên") và step 2 "model.encode … 384 chiều".
- INT L06: hook "tệp câu hỏi đi kèm (interview/06_…)" không có trong gói video + labs; concept step 0 bốn tầng, mỗi tầng một dòng.
- INT L07: không kẹt.
- ACB L00: không kẹt.
- ACB L01: quymo "nhiều bộ quản lý hàng đợi" chưa giảng (nhẹ).
- ACB L02: không kẹt.
- ACB L03: example step 2 "chỉ đặt khoá sau khi nhà mạng xác nhận" mâu thuẫn "NX" ngay trên lệnh.
- ACB L04: không kẹt (mã Go đã giảng).
- ACB L05: không kẹt; step 3 "xong trong 2,5 giây" không khớp chia 7/7/7/9.
- ACB L06: prereq step 0 hàng 3 "Sau mỗi lần xác thực thành công, tổng cộng dồn tính lại từ 0" không biết lấy ở đâu.
- ACB L07: lab, phân loại "bat thuong".
- ACB L08: lab, dấu hai chấm.

## 5. Số đã tính lại / mã đã chạy

- 362/362 biểu thức `checks` trong 17 YAML đánh giá True (Python).
- 31/31 khối mã Python trên màn hình có "Kết quả chạy thật/khi chạy" chạy lại ra đúng từng dòng (INT L00–L06, ACB L00–L08; thư viện chuẩn, sqlite3, heapq, hmac).
- Java 21.0.13: `LuongAo` (INT L01, 10 000 luồng ảo) in "xong 10000 tac vu" trong 0,36 s; `TuGoi` (INT L02, ráp 3 cảnh) in đúng 6 dòng (số giao dịch 1 rồi 2): 2/2 khớp. Chỉ đọc, không chạy được: Oracle PL/SQL (INT L03, ACB L05), SQL Oracle (INT L06), Redis, Go (INT L05/ACB L04/L08), ONNX Java, ksqlDB, OFS, ISO 8583 thật; các bài ACB đều ghi "mô phỏng" trên màn hình khi mã thay hệ thật (ĐẠT), INT L02 `TuGoi` ghi "MÔ PHỎNG … không phải Spring thật" (ĐẠT).
- Tính tay độc lập mọi đáp số lab: 8 lab INT + 9 lab ACB = 17/17 khớp `mong_doi.txt` (INT bằng script riêng, ACB bằng `cham.sh`).
- Tính tay các con số quan trọng trên màn hình (không nằm trong checks): bản đồ bit INT L04 `3020000008001000`, khối PIN `04122D789ABCDEF6` (XOR ISO 9564 f0), N log N ACB L07 `2469 / 446180 / 64 549 593`, Little ACB L01 `175 / 179 / 17 858`, chuỗi INT L06 `99,96 % / 210,2 phút`, UCB1 `1,21 / 1,77 / 1,13 / 1,93`: khớp. Không tìm thấy số tính sai; một số lệch logic (ACB L05 2,5 vs 3,0 s) ghi ở SHOULD.
- Web đã kiểm: QĐ 2345 (ngày hiệu lực, ngưỡng) và TT 31/2024 (nhóm nợ, bị TT 37/2025 sửa): nêu ở SHOULD. Không kiểm được: nội dung Công báo 1279+1280, 825+826, TT 77/2025 hiệu lực 01/3/2026, bản hợp nhất 25/VBHN-NHNN (chỉ dựa vào `audit/legal/registry.yaml` được trích trong bài; không mở).

## 6. Khung hình đã xem và lỗi hiển thị

Mỗi bài xem 6 ảnh (lưới 3×2 ghép từ `frames/*.png`): mở đầu, ôn nền, ví dụ/quymo, bẫy, quiz, tự làm/tổng kết; thêm 1 lưới 6 ảnh sơ đồ SVG (INT L02, L03; ACB L01, L05, L07, L08). Tệp: INT L00 `00000, 00009, 00060, 00078, 00083, 00089`; INT L01 `00000, 00009, 00053, 00067, 00070, 00078`; INT L02 `00000, 00009, 00051, 00067, 00069, 00077`; INT L03 `00000, 00008, 00048, 00062, 00065, 00072`; INT L04 `00000, 00010, 00059, 00073, 00079, 00087`; INT L05, L06 `00000, 00009, 00031, 00045, 00066, 00082`; INT L07 `00000, 00008, 00025, 00035, 00039, 00041`; ACB L00 `00000, 00012, 00038, 00055, 00080, 00099`; ACB L01 `00000, 00011, 00035, 00051, 00074, 00092`; ACB L02 `00000, 00012, 00038, 00055, 00080, 00099`; ACB L03 `00000, 00010, 00033, 00048, 00071, 00088`; ACB L04 `00000, 00011, 00036, 00052, 00076, 00095`; ACB L05, L07, L08 và ACB L06 theo `s2_*`/`sheet_*` (6 ảnh mỗi bài, chỉ số 0, 12, 38, 56, 81, 100 hoặc tương đương).
- Lưu ý: 12 bài mp4 cũ nên khung hình `frames/` (dựng 11-14) khác nội dung mp4/srt; tôi chỉ dùng frames để kiểm màn hình và dùng srt/chapters để kiểm mp4.
- Lỗi hiển thị: không thấy chữ tràn, đè, bị cắt ở 17 bài. Nhận xét: khoảng 40% chiều cao khung trống dưới nội dung; sơ đồ SVG chiếm ~25% khung và chữ nhỏ (đọc được ở 1920 px, khó ở 640 px); khối mã dùng chữ nhỏ. INT L06 khung 1 hiện đường dẫn `interview/06_interview_qa_bank_100.md` người học không có.
- Lệch lời đọc: srt INT L00–L04 (mp4 mới) khớp `say` ở các cảnh kiểm; ACB/INT L05–L07 srt cũ lệch (xem M1).

## 7. Mục tiêu giáo án ↔ video (E51)

- `curriculum/int.yaml`, `curriculum/acb.yaml`: `objectives` của 17 mục giống từng chữ `objectives` trong YAML; mỗi mục tiêu có cảnh `covers` tương ứng; `example` khớp tiêu đề cảnh ví dụ. Với INT L00–L04 (mp4 mới) video phủ mục tiêu; với 12 bài còn lại mp4 cũ KHÔNG phủ mục tiêu "So sánh ×1, ×100, ×10 000" và "Trả lời câu có số/Viết mã … số mới" (không có cảnh quymo/practice trong chapters.txt).
- Lệch giáo án: INT L02 (Bloom ngoài mục tiêu), INT L04 `fix` ("tách luồng gửi nhận bất đồng bộ qua correlation ID") chỉ được dạy ở 1 bước trong khi `example` là đối soát, INT L06 tiêu đề "100 câu" vs video 5 tình huống (hook nói thật), ACB L06 tiêu đề/slug QĐ 2345 vs thân TT 50/2024, ACB L08 mục tiêu 5.

## 8. Nhận xét chung

- Nội dung YAML sau AF2 sạch về kiến thức: 0 lỗi MUST, mọi phép tính khớp, mã chạy lại ra đúng, ranh giới "mô phỏng" rõ ở ACB và INT L02.
- Điểm nghẽn thật là sản phẩm video: 12/17 mp4 chưa dựng lại; INT L07 và ACB L06 mp4 vẫn nói 50 triệu và "Quyết định 2345" như căn cứ. Phải dựng lại trước khi người học dùng.
- Lab: 17/17 làm được; chỉ ACB L08 `de.md` lệch mong đợi một dấu hai chấm (lab INT không chấm máy).
- Số lương: bài INT L07 YAML không còn số không nguồn; còn dư trong tệp đi kèm `interview/06, 07` (50 triệu mục tiêu, "Middle 35–40M", 42 triệu "khung nội bộ") và quiz ACB L00.
- Pháp lý: ACB L06 xử lý đúng (QĐ 2345 CHƯA KIỂM, TT 50/2024 sửa bởi TT 77/2025, không nêu số điều); INT L05/L06/lab dùng QĐ 2345 như hiện hành là mâu thuẫn nội bộ; TT 31/2024 cần ghi TT 37/2025.
- "Hai nhóm vai trò" khớp JD ở mức tổng quát nhưng tiêu chí phân biệt "mức 3" yếu; ghi đúng "bản đã lưu, chưa kiểm lại".
- INT L04 là bài duy nhất quá tải thật (2296 từ, > 20 thuật ngữ, 15,2 phút); INT L05/L06 mỏng ở P6 và quiz kiểm lẽ thường.
- Quy mô/thời gian (P9) tốt: cả 17 bài có bảng ×1/×100/×10 000 hoặc mốc thời gian kèm đánh đổi; ACB L05 có thêm "chỗ nghẽn còn lại" rất đáng giá.
