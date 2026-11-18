# R2 INT+ACB: đã đọc 18/18 bài (INT L00–L08, ACB L00–L08), vòng 2 trên bản đã dựng lại — 2026-11-15

Cách làm: người điều phối chia 4 phần (A: INT L00–L03; B: INT L04–L08; C: ACB L00–L03; D: ACB L04–L08), mỗi phần đọc TRỌN digest chữ của từng YAML (mọi show/say/checks/quiz/lab), mục curriculum, SRT so `say` từng từ, spec_sha256, chạy lab bằng `cham.sh` (hoặc tính tay với lab `.md`), ≥5 khung hình mỗi bài. Người điều phối tự đối chiếu chéo QĐ 2345 INT/ACB (mục 1) và kiểm lại bằng grep lỗi TAB của ACB L05 (xác nhận). Không sửa/tạo tệp trong repo; không build/tts/asr/render/gen/git/docker.

Ngoại lệ cần khai (độ độc lập): fork INT-B grep "77/2025" làm lộ vài dòng `audit/legal/registry.yaml` (tệp nguồn pháp lý, không phải báo cáo); fork ACB-C mở nhầm 40 dòng đầu `audit/review/screen_code/ACB.yaml` (sổ mã màn hình); fork ACB-D dùng `audit/legal/registry.yaml` và tra web. Không phán đoán nào của MUST/SHOULD dựa vào các tệp đó làm bằng chứng duy nhất.

## 0. Kết luận theo ngưỡng chốt

| Chỉ tiêu | Ngưỡng | Kết quả | Đạt? |
|---|---|---|---|
| MUST | 0 | **0** (18 bài). Một chỗ biên: INT L01 hook step 1 "hàng triệu luồng ảo / cơ chế thu gom rác thế hệ mới" hứa quá phạm vi bài (xếp SHOULD; chấm nghiêm "giáo án hứa điều bài không dạy" thì thành MUST nhẹ) | ĐẠT (có chú thích) |
| P1 = 2 | ≥ 90% | **2/18 = 11%** (INT 1/9: chỉ L07; ACB 1/9: chỉ L05). Chấm theo đúng thang BRIEF: chỉ 2 khi không còn từ nào bị kẹt; 16 bài còn 1–5 thuật ngữ nền dùng mà không giảng tại chỗ | **KHÔNG ĐẠT** |
| P8 = 2 | 100% | **18/18 = 100%** (mỗi bài có lab có kết quả mong đợi, số khác ví dụ) | ĐẠT |
| P9 = 2 | (đo, không có ngưỡng) | 18/18 | — |
| spec_sha256 build_report == spec hiện tại | khớp hết | **18/18 khớp** (không "video cũ") | ĐẠT |
| SRT == `say` từng từ | — | **18/18, 0 lệch** (tổng ~35 000 từ) | ĐẠT |
| `checks` trong YAML chạy lại | — | INT 205/205 (83+122); ACB 175/175 (76+99) = **380/380** | ĐẠT |
| Mã trên màn hình chạy lại | — | tất cả đoạn chạy được đều khớp (Python/Java 21/sqlite); SQL ksqlDB, OFS, PL/SQL, Go, Redis, mã giả: chỉ đọc | ĐẠT |
| Lab | — | tự làm được 17/18 hoàn toàn, 1 phần (INT L08: lab không có bài hai con trỏ); `cham.sh` ĐÚNG cho mọi bài chấm được; `mong_doi.txt` khớp màn hình 18/18 | ĐẠT |

Tổng SHOULD: 27 (A 8, B 7, C 6, D 6); không MUST. Tổng P1–P7: INT L00 12, L01 12, L02 13, L03 12, L04 13, L05 12, L06 11, L07 13, L08 10; ACB L00 12, L01 13, L02 11, L03 11, L04–L08 đều 13. Kết luận Mất gốc: ĐỦ 14 bài, GẦN 4 bài (INT L06 = 11, INT L08 = 10, ACB L02 = 11, ACB L03 = 11); không bài CHƯA.

Bài đã đọc: INT L00_overview_zero_to_senior, L01_foundation_cs_java, L02_backend_microservices, L03_distributed_systems_senior, L04_banking_domain_t24_napas, L05_uit_ai_banking_multiplier, L06_interview_qa_bank_100, L07_salary_negotiation_50m_gross, L08_tin_dung_ban_le_va_doi_soat_cuoi_ngay; ACB L00_phong_van_tich_hop_acb, L01_tich_hop_core_t24_ibm_mq, L02_chuyen_mach_napas_iso8583, L03_streaming_ksqldb_notification_hub, L04_san_chuyen_nhuong_hop_dong_tien_gui, L05_cong_chi_luong_va_sao_ke_divide_conquer, L06_sinh_trac_hoc_qd2345_va_bao_mat_ngan_hang, L07_tai_khoan_dinh_danh_va_doi_soat_ba_ben, L08_squad_lending_tich_hop_cic_giai_ngan.

## 1. Đối chiếu nhất quán QĐ 2345 / sinh trắc học / lương giữa INT và ACB (người điều phối)

Grep toàn bộ lessons/int, lessons/acb, labs, curriculum: QĐ 2345 chỉ xuất hiện ở INT L05, INT L06 (+ labs/INT/L06/de.md) và ACB L06 (+ curriculum/acb.yaml L06). Các chuỗi "2345" khác là số giả (số tài khoản 12345678, STAN 123456...) hoặc `2345 - 2000 == 345` (check tầm thường ở ACB L06 quiz).

| Điểm | INT (L05, L06, de L06) | ACB L06 | Nhất quán? |
|---|---|---|---|
| Ngưỡng | trên 10 triệu một lần hoặc tổng ngày trên 20 triệu (L06 "vượt 20 triệu") | trên 10 triệu một lần hoặc tổng ngày vượt 20 triệu | Có |
| Căn cứ | TT 50/2024/TT-NHNN sửa đổi bởi TT 77/2025/TT-NHNN | như INT, thêm Phụ lục 01, hiệu lực 01/03/2026, bản hợp nhất 25/VBHN-NHNN, đối chiếu `audit/legal/registry.yaml` | Có (ACB chi tiết hơn; INT không nêu Phụ lục/ngày) |
| QĐ 2345 | "cũng hay được nhắc nhưng chưa đọc nguyên văn, chưa rõ còn áp dụng; bài không nêu số điều" | "chưa đọc nguyên văn, chưa rõ còn áp dụng hay đã được Thông tư thay"; ngày 18/12/2023 và hiệu lực 01/07/2024 chỉ nêu "theo bài phỏng vấn đã lưu" | Có: không bên nào nêu QĐ 2345 chắc hơn bên kia |
| Nguồn trong `source:` | TT 50/77 KHÔNG có trong `source:` của INT L05, L06 (chỉ trong chữ trên màn hình) | có | LỆCH NHẸ: SHOULD (INT-B) |
| Cách gọi | L05 "sinh trắc học", L06 "xác thực khuôn mặt" dùng thay nhau | "sinh trắc học khớp dữ liệu chip căn cước/VNeID" | Chấp nhận được |
| Hệ quả tính lại | — | quy tắc mô phỏng "quét xong tổng cộng dồn về 0" (lab mong_doi `3 thuong tong: 3`) nhãn giả định | khác INT (INT không mô phỏng); ACB-D SHOULD |

Rủi ro nguồn thứ cấp (ACB-D, PLAUSIBLE): báo chí/ngân hàng gắn 10/20 triệu vào QĐ 2345 (hiệu lực 01/07/2024); một nguồn gắn vào Phụ lục 02 TT 50; `audit/legal/registry.yaml` ghi TT 77/2025 Điều 10 thay Phụ lục 01, 02, 04 (từ 01/07/2026 với khách cá nhân, CHUA_KIEM). Cả INT lẫn ACB đều gắn 10/20 triệu vào "TT 50/2024 đã sửa đổi" mà chưa dẫn số điều; vì cả hai tự khai chưa đọc nguyên văn và dặn mở văn bản hiện hành nên chỉ là SHOULD, nhưng hôm nay (15/11/2026) đã qua 01/07/2026 nên nên đọc Phụ lục sau sửa đổi rồi ghi số điều ở CẢ HAI khoá cùng lúc để không lệch.

Lương (INT L00, L07; ACB L00): không có mức lương thật không nguồn. Mọi số (L = 40 triệu, 32–40 triệu, 520/560/680 triệu, "35 đến 40 triệu") gắn "số minh hoạ"; dữ kiện có nguồn duy nhất là lương tháng 13 cố định và thưởng 1–4 tháng lương, đối chiếu `resources/job/JD.md` dòng 72, 79 (nguồn bản đã lưu, chưa kiểm lại trang gốc, không có URL/ngày trên màn hình). INT và ACB L00 khớp nhau (cùng 520/560/680). Lưu ý: tên tệp `lessons/int/L07_salary_negotiation_50m_gross.yaml` chứa "50m" trái với lời bài "không đưa mức lương nào" (đường dẫn, không hiện trong video).

Tên người thật: chỉ có tên tác giả tài liệu (Auer/Cesa-Bianchi/Fischer 2002; SRE book 2016) và lý lịch người học trùng CV; không số không nguồn.

Phát hiện hiển thị đã tự xác nhận: `lessons/acb/L05_cong_chi_luong_va_sao_ke_divide_conquer.yaml` dòng 412 chứa ký tự TAB thật nên `\times` hỏng thành "1 000 000imes9/30" (khung `out/ACB/L05/frames/00052.png`); là dòng TAB duy nhất trong 18 bài (grep -P "\t").

## 2. Danh sách MUST/SHOULD chính (file:cảnh)

MUST: không có.
SHOULD đáng sửa trước (CONFIRMED trước):
- ACB L05 example step 3 (frame 00052): `\times` hỏng thành "imes" (YAML dòng 412, TAB thật).
- INT L06 example (title scene, chapters 04:01): "Kể Câu chuyện Sự cố Sản xuất Thực tế tại OCB" + "Tôi lập tức…" đọc như kinh nghiệm thật của ứng viên (rủi ro trung thực hồ sơ), step 0 nói "ví dụ minh hoạ".
- INT L07 example step 2 (đòn 3): "mức thưởng nào cũng thua" chỉ đúng cùng k; L=36,k=5: 648 > 600 (hoà vốn k≈3,67).
- INT L03 recap: hàng "Kafka Idempotent: không mất tin" sai nhãn (không mất tin do acks=all + min.insync.replicas).
- INT L02 chaythat step 2: "hãy đoán một hay hai" không có `pause`; INT L02 hook step 0 show/say lệch.
- ACB L01/L02/L03 check step 0: bảng sai–đúng đặt HẬU QUẢ dưới cột hành động; ACB L02 check say: "hạn mức 1500 mi li giây" (đúng: ngưỡng chờ); ACB L03 concept/symbol: ngưỡng 50k VND không gắn nhãn minh hoạ; ACB L07 pitfall step 0: say "nghẽn bộ nhớ" vs màn hình O(N²).
- INT L08 example vs quymo: so sánh N² (1 cặp) với mô hình sắp xếp (3 danh sách) không cùng đơn vị.
- ACB L06: nguồn 10/20 triệu + giả định "tổng về 0" + "Không đưa số CCCD vào vé (Luật 91/2025/QH15)" đặt như căn cứ pháp lý (xem mục 1).
- ACB L08 concept (frame 00022): chữ "Chuyển tiền qua NAPAS 247" chạm viền hộp 4; INT L01/L03 concept: nhãn con SVG ~14 px nhỏ.
- INT L04 check step 0 ("0400/0420 chỉ dùng khi đã biết chắc giao dịch thất bại"), INT L04 pitfall/quiz (thời điểm gốc trường 7).

## 3. Điểm yếu chung (giúp chốt)
- P1 là điểm hụt duy nhất so với ngưỡng: thuật ngữ nền dùng mà không giảng tại chỗ (luồng, JMS, NAPAS/TCP/socket, hex, phân vùng, băm, HTTP/409, CASA/AZ, Redis NX EX, con trỏ/cursor, chỉ mục). Mẫu số chấm nghiêm theo BRIEF; nếu nới (chấp nhận 1–2 từ phụ), tỉ lệ vẫn khó đạt 90% vì một nửa số bài có ≥3 từ.
- P3 (hình cơ chế) = 1 ở INT L00, L01, L03, L05, L06, L08 và ACB L00, L02, L03, L05: cơ chế chính chỉ có chữ/mã.
- Quiz phương án nhiễu lộ liễu (đáp án đúng thường dài nhất) ở cả ACB; check scene INT không có `pause`; INT L00 và L07 quiz dừng chỉ 5 giây cho phép tính 3–4 bước.
- Lab: mọi lab INT là giấy bút `.md` mà `cham.sh` không chấm `.md/.txt` (người học phải so mắt hoặc viết `.py`); ACB lab chấm được bằng `.py`.

---

# Chi tiết từng phần (nguyên văn báo cáo của người đọc, viết gọn)



<!-- part A -->
### Phần A (fork A): INT L00, L01, L02, L03 — đã đọc 4/4 bài

Bài đã đọc trọn (digest chữ của mọi scene/step: show, say, checks, quiz, lab) + curriculum/int.yaml + labs/INT/L00..L03 + SRT + khung hình: INT L00, INT L01, INT L02, INT L03. (INT L04–L08 và toàn bộ ACB do fork khác.)

#### 1. Chuẩn xác (chỉ lỗi có bằng chứng)
MUST = 0 cho 4 bài. SHOULD = 8.

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| INT L00 | — | | | không phát hiện MUST. Số tính lại khớp (xem mục 6) | | |
| INT L01 | SHOULD | hook step 1 (say) | say: "Ta nắm vững cơ chế thu gom rác thế hệ mới của máy ảo Java. Ta cũng làm chủ kỹ thuật lập trình đồng thời với hàng triệu luồng ảo trong Java 21." | Bài chỉ dạy bố cục thế hệ trẻ/già + Minor/Major/Full GC (không có G1/ZGC, "thế hệ mới" dễ bị hiểu là GC mới) và chỉ chạy 10 000 luồng ảo, không phải "hàng triệu". Hứa quá phạm vi bài | Đổi "thế hệ mới" thành "bố cục thế hệ trẻ và thế hệ già"; "hàng triệu" thành "hàng chục nghìn" | PLAUSIBLE (nếu người chấm hiểu "hứa điều bài không dạy" nghiêm thì thành MUST nhẹ) |
| INT L01 | SHOULD | concept step 0 (svg), L03 concept step 0 (svg) | nhãn con trong sơ đồ JVM ("Chứa đối tượng sống lâu năm", "Mặc định thường 1 MB mỗi luồng") và sơ đồ SAGA ("Bồi hoàn: Hoàn tiền CASA") | Cỡ chữ nhãn con trong SVG khoảng 14 px trên khung 1920, nhỏ hơn hẳn chữ thân bài; khung 00021.png (L01) và 00021.png (L03) | Tăng font-size SVG ≥ 20 | CONFIRMED (xem khung) |
| INT L02 | SHOULD | hook step 0 (show vs say) | show: "đã trừ tiền khách hàng nhưng không lưu lịch sử vào cơ sở dữ liệu"; say: "giao dịch bị trừ tiền nhưng không thể hoàn tác" | Hai mô tả khác nhau (mất nhật ký vs không hoàn tác); đồng thời say gán lớp vỏ ủy quyền cho "Spring Boot" (thực ra cơ chế AOP của Spring Framework) | Thống nhất một mô tả; nói "Spring" | CONFIRMED (chữ trong YAML) |
| INT L02 | SHOULD | chaythat step 2 (say) | "Trước khi chạy, hãy đoán số giao dịch sau lần gọi đầu là một hay hai." | Lời mời đoán nhưng step không có `pause`; video chạy tiếp ngay sang kết quả, mất tác dụng thí nghiệm "đoán rồi kiểm" | Thêm pause ≥ 15 | CONFIRMED |
| INT L02 | SHOULD | concept step 0 (svg) | sơ đồ: "Lớp vỏ Spring Proxy" bao cả "Hàm công khai ngoài" lẫn "Hàm Transactional" với nhãn "gọi qua this" | Cả hai hàm vẽ nằm trong khung proxy nên hình không cho thấy lời gọi nội bộ "đi vòng ngoài vỏ" như lời đọc; cơ chế bỏ vỏ chỉ được thấy rõ ở bản mô phỏng Java sau (chaythat) | Vẽ proxy chỉ bọc lối vào; mũi tên this nằm trong đối tượng thật, không qua proxy | PLAUSIBLE |
| INT L03 | SHOULD | check step 0/1 | "tại sao ngân hàng nên chọn mô hình SAGA Điều phối tập trung thay vì mô hình Tự phối hợp qua sự kiện?" / "(B) ... rất khó truy vết" | Tuyệt đối, thiếu điều kiện: tự phối hợp vẫn hợp lý khi ít bước/ít đội; lời đọc đã mềm hơn ("thường được ưu tiên") nhưng màn hình thì không | Thêm "khi quy trình nhiều bước (ở đây 8 dịch vụ)" lên màn hình | CONFIRMED |
| INT L03 | SHOULD | pitfall step 0 (show) | "Bảng giao dịch không phân vùng | Quét toàn bảng hàng chục triệu dòng làm đơ I/O" | Hệ quả viết như tự động xảy ra; thực tế chỉ khi truy vấn không dùng được chỉ mục (chính L01 vừa dạy chỉ mục tra 3–4 lần đọc). Thiếu điều kiện áp dụng | Thêm "khi truy vấn quét theo ngày mà không có chỉ mục phù hợp" | PLAUSIBLE |
| INT L03 | SHOULD | recap (show, bảng) | "Kafka Idempotent | Không mất tin đã xác nhận khi một broker hỏng; khử trùng do retry" | Không mất tin do `acks=all` + `min.insync.replicas=2` + `replication.factor=3` (scene symbol), còn idempotence chỉ khử trùng; nhãn hàng gộp hai tính chất vào một cơ chế | Đổi nhãn "Kafka acks=all + idempotent" | CONFIRMED (đối chiếu scene symbol step 0–1) |

Ghi chú không phải lỗi: (a) INT L00 symbol "Tin tuyển dụng ACB ghi lương tháng 13 cố định và thưởng cuối năm 1–4 tháng lương tuỳ xếp loại, còn mức lương ghi 'Thương lượng'" có nguồn trong repo: resources/job/JD.md dòng 72, 79 ("Dữ kiện chính thức duy nhất là lương tháng 13 và thưởng 1–4 tháng"), nhưng trên màn hình không ghi ngày/nguồn như bảng "hai nhóm vai trò" (có "đọc 2026-11"). Nên thêm "(tin ACB đã lưu, đối chiếu lại trước khi nộp)". (b) INT L03 đoạn PL/SQL `FORALL ... l_accounts(i).amount` (scene example step 3): chỉ đọc, không chạy (không có Oracle); cú pháp chuẩn của Oracle 11g trở đi, không thấy lỗi.

#### 2. Bảng độ sâu
Phút = tổng `duration` trong _frames.txt (gồm thời gian dừng 180 s của practice). spec khớp = out/INT/Lxx/build_report.json spec_sha256 == lv.spec_digest (bỏ asr_reviewed) của YAML hiện tại. SRT khớp = từ-theo-từ SRT == say (difflib ratio, số từ).

| Bài | sha16 | spec khớp | SRT khớp | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng P1–P7 | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| INT L00 | 7584bae878474958 | CÓ (63cd7d7b…) | CÓ (2236/2236 từ, 0 lệch, 103 khối) | 14,55 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ (sát ngưỡng) | CPU/bộ nhớ đệm, Heap, luồng nhẹ/nặng, "cổng tích hợp", SQL INSERT/UNIQUE cơ bản | concept step 2 nhắc "bộ nhớ đệm CPU, rò rỉ bộ nhớ Heap" chưa giảng (hẹn "chuyên đề sau"); chuỗi 4 bước chống trừ tiền kép chỉ có chữ/mã, không có sơ đồ luồng |
| INT L01 | d575a3b9a3da7e3a | CÓ (622db421…) | CÓ (1998/1998, 0 lệch, 89 khối) | 13,30 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ (sát ngưỡng) | luồng (thread) là gì, nhân CPU, biến kiểu long, synchronized, chỉ mục/index, đọc/ghi | "luồng" là khái niệm then chốt của bài nhưng không được giảng (nếu chấm khắt P1=0); false sharing, B-Tree không có hình (chỉ chữ + một sơ đồ JVM) |
| INT L02 | 1b6460534a68d2cf | CÓ (a7393600…) | CÓ (2016/2016, 0 lệch, 88 khối) | 13,32 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | Java (interface, lambda, ngoại lệ), HTTP, DispatcherServlet/Servlet, Controller | chaythat step 0–2: mã Java mô phỏng (interface, static class, lambda `(p, m, a) ->`, Proxy) không giảng cú pháp, người chưa lập trình đọc theo lời say mà không hiểu dòng mã; check Bloom không có pause, không bác từng phương án sai |
| INT L03 | 680ad9d397caffa9 | CÓ (1363defb…) | CÓ (2026/2026, 0 lệch, 82 khối) | 13,21 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ (sát ngưỡng) | SQL cơ bản (SELECT/UPDATE/WHERE), chỉ mục, con trỏ (cursor), ADR/thư mục trace, Debezium | SAGA/Outbox/2PC không có hình luồng thời gian (sơ đồ SAGA chỉ là cây ba ô, không có mũi tên bù trừ; Outbox chỉ chữ); pitfall "chỉ mục khoá ngoại" dựa chỉ mục chưa giảng |

Lý do điểm 1 ở P1 (chỗ cụ thể): L00 concept step 2 ("Nghẽn bộ nhớ đệm CPU, rò rỉ bộ nhớ Heap"), quymo step 1 ("luồng nhẹ", "luồng nặng"); L01 prereq step 1 ("biến kiểu long", "nhân CPU 1 ghi biến a"), concept step 0 ("luồng"); L02 chaythat step 0–1 (mã Java); L03 pitfall step 0 ("chỉ mục"), example step 3 ("con trỏ"), quiz step 0 ("thư mục trace (ADR)"). Lý do điểm 1 ở P3: L00, L01, L03 chỉ có đúng 1 sơ đồ SVG (kim tự tháp / bộ nhớ JVM / cây ba ô SAGA); cơ chế chính (4 bước chống trừ tiền kép, chia sẻ giả, B-Tree, 2PC vs SAGA, Outbox) không có hình. L02 đạt 2 nhờ sơ đồ proxy + mô phỏng chạy thật.

Quiz/pause: L00 quiz pause 5 s (thấp, nhưng practice 180 s); L01, L02, L03 quiz pause 15 s; check scene của cả bốn bài không có pause (chỉ có lời "mời bạn trả lời"). Giữ P5=2 vì lời giải theo từng bước + practice 180 s; ghi nhận điểm yếu.

#### 3. Lab (đã chạy như người học; cả bốn là bài giấy bút `.md`, cham.sh không chấm .md nên tính bằng Python rồi diff với mong_doi.txt)

| Bài | tự làm được | thời gian | kẹt ở đâu | mong_doi khớp |
|---|---|---|---|---|
| INT L00 | CÓ (sau khi xem video) | ~5 phút | không kẹt; de.md cho sẵn công thức, chỉ phải đổi 25 ms = 0,025 s và nhận ra JBoss/JSP/MS SQL = nhóm B | KHỚP (200; 262.8; B) — diff chỉ khác CRLF |
| INT L01 | CÓ | ~5 phút | de.md ghi sẵn "số tầng nhỏ nhất h sao cho 500^h ≥ 80 000 000" nên không cần suy ra; chạy thêm mã Java LuongAo trên màn hình (JDK 21.0.13, javac+java): in "xong 10000 tac vu" | KHỚP (3; 4; 2000 MB; 4000000 byte) |
| INT L02 | CÓ | ~5 phút | không kẹt; chạy mã TuGoi.java ghép từ 3 step (javac + java): in đúng 6 dòng như màn hình, "so giao dich: 1" rồi "2". Phải tự ghép 3 mảnh mã thành một tệp (video không nói ghép thế nào) | KHỚP (34; 1700; 1360) |
| INT L03 | CÓ | ~6 phút | không kẹt; de.md cho từng công thức một dòng một dòng (hầu như điền số) | KHỚP (12; 48000; 24; 30 ms; 33; 333) |

Nhận xét lab: cả bốn đề cho công thức từng dòng nên kiểm "áp dụng số mới", chưa kiểm "tự thiết lập". Không có lab chạy mã Java/PL/SQL cho người học tự gõ (mã chạy chỉ nằm trên màn hình).

#### 4. Người học kẹt ở đâu
- INT L00: concept step 2 (bảng "Nghẽn bộ nhớ đệm CPU, rò rỉ bộ nhớ Heap") — CPU cache/Heap chưa giảng; còn lại theo được.
- INT L01: prereq step 1 ("Một biến kiểu long dài 8 byte... Nhân CPU 1 liên tục ghi biến a") — người chưa lập trình không biết biến, kiểu long, nhân; sau đó "luồng" chưa giảng.
- INT L02: chaythat step 0 (mã `interface Dv { void chuyen(); ... }`, `static class DvThat implements Dv`) và step 1 (lambda `(p, m, a) ->`) — đọc theo lời say được nhưng không hiểu dòng mã.
- INT L03: example step 3 ("FETCH cur_payroll BULK COLLECT INTO l_accounts LIMIT 1000") — "con trỏ"/cursor và SQL cơ bản chưa giảng; pitfall step 0 ("chỉ mục trên cột khoá ngoại") dùng "chỉ mục" chưa giảng.

#### 5. Số tính lại / mã đã chạy
- `checks` trong YAML (python eval): L00 24/24, L01 21/21, L02 15/15, L03 23/23 = 83/83 đúng.
- Mã/số trên màn hình chạy lại: L00 mã Python quymo (6 dòng) khớp; L01 mã Python B-Tree (3 dòng) khớp + Java LuongAo chạy được; L02 Java TuGoi (6 dòng) khớp + Python bể kết nối (4 dòng) khớp; L03 Python 2PC vs SAGA (4 dòng) khớp. Mã chỉ đọc, không chạy: L00 SQL INSERT/Redis SET; L02 Java Redis + RFC 9457 JSON; L03 PL/SQL (LEAST/GREATEST + FOR UPDATE, BULK COLLECT/FORALL), sendfile. Tổng đã chạy: 8 đoạn, 8 khớp.
- Số trong lab/đáp án: 4 lab × mọi dòng = 4+4+3+6 = 17/17 khớp mong_doi.txt.
- Công thức tay đối chiếu: 99,99% -> 52,56 phút/năm (525 600 × 0,0001); 99,95% -> 262,8; (13+k)·40 = 560..680; log_1000(1e7)=2,33 -> 3 tầng; 8·2+1=17; 17/0,020=850; 50000·0,020=1000; 4+3=5+2.

#### 6. Khung hình đã xem (≥ 5 mỗi bài) và lỗi hiển thị
- L00: 00001, 00033, 00055, 00065, 00087, 00100 (6 khung). Không tràn/đè. Nhẹ: recap hiển thị chuỗi "1. ... ↓ 2. ..." liền thành đoạn thay vì danh sách dọc (00100); khung 00087 (quiz) bảng đáp án chiếm nửa bề ngang, nửa dưới trống.
- L01: 00013, 00021, 00026, 00045 (code Java 'Thực hành'/khung này là Bước 2 luồng ảo), 00054, 00073, 00088 (7 khung). Nhẹ: nhãn con SVG JVM nhỏ (00021). Công thức LaTeX hiển thị đúng.
- L02: 00020, 00029, 00043, 00053, 00070, 00086 (6 khung). Mã Java/Python đọc được, không cắt. Sơ đồ proxy xem S3 ở mục 1.
- L03: 00021, 00022, 00041, 00049, 00066, 00080 (6 khung). Sơ đồ SAGA nhãn con nhỏ (00021/00022); khung quiz có nút "Dừng video, tự làm rồi xem tiếp" đúng.
- Lời đọc: không bài nào có lệch SRT–say (0 lệch trên 4 bài), nên không có chỗ SRT thiếu câu/sai số.

#### 7. Số pháp lý / lương / tỉ lệ / tên người thật / nguồn
- Văn bản pháp lý (QĐ, TT, NĐ, luật): không có trong INT L00–L03 (grep "2345", "sinh trắc", "Thông tư", "Nghị định", "Luật": 0 trong lời đọc/màn hình; chỉ có chuỗi khớp trong khối asr_reviewed là ghi chú nội bộ). RFC 9457 (IETF 2023, thay RFC 7807): đúng, có nguồn ghi trên màn hình.
- Lương: chỉ INT L00 (symbol + quiz): L = 40 triệu là "số minh hoạ" (ghi rõ 5 lần), T = L × (13 + k), k 1–4: sai khác gói 560–680 triệu đúng phép tính; dữ kiện "ACB ghi lương tháng 13 cố định và thưởng 1–4 tháng, lương Thương lượng" có nguồn ở resources/job/JD.md:72,79 (xem ghi chú (a)); không có khung lương thị trường nào bị nêu thành số (đúng quy tắc không số không nguồn).
- Tỉ lệ/phí: các số 99,99%/99,95%, 20 ms, 17 kết nối đều được ghi "số minh hoạ"; công thức bể kết nối 2×nhân+đĩa có nguồn (wiki PostgreSQL/HikariCP) ghi trên màn hình, ghi rõ "không phải định lý".
- Tên người thật: không có. Tên tổ chức: ACB (chỉ dẫn tin tuyển dụng, câu "Làm chủ... tại ACB" ở recap là khẳng định mục tiêu, không phải số liệu), UIT (L00 pitfall: "dự kiến tốt nghiệp 11/2026" đi kèm "dự kiến"), Temenos T24 (mô tả đúng "phần mềm ngân hàng lõi của hãng Temenos"; L00 không nói ACB dùng T24).
- Số hiệu năng (GC "hàng giây", L1 1 ns/RAM 100 ns, TPS…): đều có "xấp xỉ, minh hoạ, tuỳ đời CPU/phải đo".

#### 8. Trích QĐ 2345 / sinh trắc học
Không có chỗ nào trong INT L00–L03. (Để người điều phối đối chiếu: L04–L08 do fork khác đọc.)

#### 9. Nhận xét chung
- 0 MUST; 8 SHOULD, không cái nào làm sai kiến thức nghiệp vụ; hai nhóm chính: nhãn/hình (SVG nhỏ, proxy, recap Kafka) và lời hứa/điều kiện (L01 hook, L03 check/pitfall).
- spec khớp 4/4, SRT = say 4/4 (video đã dựng đúng bản YAML hiện tại).
- P1=2: 0/4 bài (đều 1; L01 có thể 0 nếu coi "luồng" là khái niệm then chốt chưa giảng); P8=2: 4/4; P9=2: 4/4.
- Điểm mạnh: mỗi bài có bảng quy mô ×1/×10/×100 và mã chạy thật; số đều tự tính lại khớp; lab đối chiếu mong_doi khớp.
- Điểm yếu: nền lập trình (thread, biến, interface/lambda, SQL, chỉ mục, con trỏ) được giả định; hình cơ chế thưa; check scene không có pause.


<!-- part B -->
### R2 INT phần B (fork B): đã đọc 5/5 bài — INT L04, L05, L06, L07, L08

Đọc trọn digest (title, objectives, mọi step show/say, checks, quiz, lab) + mục curriculum/int.yaml + de.md/loi_giai.md/mong_doi.txt + SRT so với say + 6–8 khung hình mỗi bài. Không mở báo cáo/handover/plan cũ. Ngoại lệ cần khai: tìm "77/2025" bằng grep lộ ra 3 dòng của audit/legal/registry.yaml (dòng 58, 106 nói về TT 50/77 và QĐ 2345); tôi không dựa vào chúng để chấm.

#### Spec / video
| Bài | sha16 YAML lúc đọc | spec_sha256 build_report == spec hiện tại | SRT == say (từ-từ, difflib) |
|---|---|---|---|
| L04 | c73e6d4b81c43808 | KHỚP (6fbf21e4…) | 1963/1963 từ, ratio 1.0, 0 lệch |
| L05 | 6dc645a20f20b946 | KHỚP (3c89e0a4…) | 2141/2141, 1.0, 0 lệch |
| L06 | becc3936424a5e50 | KHỚP (b8b79c0c…) | 1898/1898, 1.0, 0 lệch |
| L07 | 309a3d09375ae7a0 | KHỚP (5ab11fd4…) | 1759/1759, 1.0, 0 lệch |
| L08 | d24469771719e253 | KHỚP (9d0c9330…) | 1875/1875, 1.0, 0 lệch |
Spec khớp 5/5; SRT khớp 5/5. Không có "video cũ".

#### 2. Bảng chuẩn xác (chỉ lỗi có bằng chứng)
MUST: 0.
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L04 | SHOULD | check step0 (màn hình) | "MTI 0400 là yêu cầu đảo, 0420 là thông báo đảo; cả hai chỉ dùng khi đã biết chắc giao dịch thất bại, không phải để truy vấn" | Khẳng định tuyệt đối. Với giao dịch thẻ theo ISO 8583, hết giờ chờ (chưa biết kết cục) chính là lúc bên gửi phát 0400 (timeout reversal) và lặp đến khi được xác nhận. Câu đúng cho luồng chuyển khoản 247 chỉ nếu đặc tả NAPAS quy định như vậy, mà bài tự ghi "cần kiểm". | Thêm điều kiện "trong luồng chuyển khoản liên ngân hàng NAPAS 247 (cần kiểm đặc tả); với giao dịch thẻ, đảo khi timeout là thông lệ" | PLAUSIBLE (không có đặc tả NAPAS để kiểm) |
| L04 | SHOULD | pitfall step1, quiz step0–2 | "Khoá nguyên tử Redis theo STAN và RRN, kèm mã thiết bị và thời điểm gửi" | Nếu "thời điểm gửi" được sinh lại ở mỗi lần gửi lại thì khoá khác nhau và khử trùng lặp thất bại; chỉ đúng khi dùng thời điểm gốc của bản tin (trường 7), giữ nguyên khi gửi lại. Bài không nói. | Ghi rõ "thời điểm gốc (trường 7), không đổi khi gửi lại" | PLAUSIBLE |
| L06 | SHOULD (trung thực hồ sơ) | example (tiêu đề cảnh + chapters.txt 04:01) step1–3 | Tiêu đề "Thực hành: Kể Câu chuyện Sự cố Sản xuất Thực tế tại OCB"; step1: "Tôi lập tức truy cập thư mục nhật ký cảnh báo của Oracle…" | Tiêu đề và câu ngôi thứ nhất đọc như một sự cố có thật của ứng viên tại OCB, trong khi step0 nói "ví dụ minh họa (hãy thay bằng sự cố thật của bạn)". Người học vội có thể kể lại như kinh nghiệm thật. Curriculum 'example' cũng dùng cùng tên. | Đổi tiêu đề thành "Khung kể một sự cố (ví dụ minh họa)" | CONFIRMED (chữ trên màn hình/chapters) |
| L07 | SHOULD | example step2 (đòn 3), frame 00041 | "mức thưởng nào cũng thua" | Bảng chỉ so cùng k (1–4 tháng) giữa L=36 và L=40. Đòn 3 là "thưởng rất cao": nếu đề nghị L=36 kèm k=5 thì 36×(13+5)=648 > 40×(13+2)=600. Điểm hoà vốn k=600/36−13≈3,67 không được nêu. Lập luận chỉ đúng khi cùng k. | Thêm "Nếu bên kia hứa k lớn hơn, hỏi k phải ≥ 3,67 mới bằng; và k có bảo đảm không" | CONFIRMED (phép tính Python) |
| L05, L06 | SHOULD (nguồn) | L05 example step3; L06 check step0; labs/INT/L06/de.md | "Thông tư 50/2024/TT-NHNN (sửa đổi bởi Thông tư 77/2025/TT-NHNN)… trên 10 triệu… tổng trong ngày trên 20 triệu" | Trường `source:` của hai spec không liệt kê TT 50/77 (L05 source chỉ có interview/05…, chương trình UIT; L06 source chỉ có "bộ câu hỏi tự biên soạn"). TT 50/2024/TT-NHNN và ngưỡng 10/20 triệu khớp hiểu biết của tôi; TT 77/2025/TT-NHNN: chưa kiểm được. Việc nêu QĐ 2345 là "chưa đọc nguyên văn, chưa rõ còn áp dụng" là đúng cách, nhưng bằng chứng nằm ngoài spec. | Thêm TT 50 và 77 vào `source:` kèm ngày đọc | PLAUSIBLE |
| L08 | SHOULD | example step0 vs quymo | nested "(3×10^6)^2 = 9×10^12 phép so sánh" so với "3×N×⌈log₂N⌉ + 2×(N+N)" | Hai phía không cùng đơn vị: vòng lặp lồng chỉ tính một cặp danh sách (N²), mô hình sắp xếp tính cả 3 danh sách và 2 lượt duyệt. Hai cặp lồng nhau là 2×9×10^12. Kết luận không đổi (2,5 giờ vs 0,21 giây là cỡ độ lớn) nhưng so sánh không ngang. | Nói rõ "một cặp" hoặc nhân đôi | CONFIRMED (đọc code ở quymo step0) |
| L08 | SHOULD | pitfall step1 | "thời gian sống của khoá ít nhất gấp đôi thời gian chờ tối đa" | Là quy tắc kinh nghiệm, trình bày như quy tắc; lớp chặn thật là ràng buộc duy nhất (bài đã nêu ngay sau). Thiếu chữ "thường dùng". | Thêm "quy tắc kinh nghiệm" | PLAUSIBLE |
| L04, L05, L07, L08 | — | các số/ngày/tên | OCB, Sutrix, Grooo, Mirae Asset Finance, ngày 01/2019, 10/2023, tốt nghiệp 11/2026 | Tiểu sử người dùng (L04 hook, L05 prereq/check, L06 5-tầng, L07 example); không nằm trong `source:` nào nhưng thuộc dữ kiện đã chốt của hồ sơ. Ghi nhận, không báo lỗi. L07 `source:` ghi tin ACB "đọc 2026-11" nhưng không có URL: chưa kiểm được nguồn gốc. | — | — |

Không phát hiện lỗi cho: số/mã chạy trên màn hình (xem mục 6), MTI/bitmap/PIN block, lệnh HSM CA/CC/JE/JC, STAN 6 chữ số, "mã 68 = phản hồi quá muộn" (ghi chú ISO 8583), UCB1 (Auer 2002), Z-score, cosine, ORA-00060, "bốn tín hiệu vàng" (SRE book 2016), nhóm nợ 10–90 ngày (đúng hiểu biết, bài đã gắn cờ cần đối chiếu bản hợp nhất).

#### 3. Bảng độ sâu
| Bài | sha16 | spec | SRT | Phút (ước theo _frames) | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng(P1–P7) | Mất gốc | P8 | P9 | Cần biết trước (dùng mà không giảng tại chỗ) | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L04 | c73e6d4b81c43808 | khớp | khớp | 14,8 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | 2 | 2 | hệ mười sáu (hex) và XOR từng chữ số hex; Redis; "bể luồng chặn"; khoá UNIQUE ở CSDL | hex không được dạy trước khi lab bắt XOR tay (chỉ mẹo "nếu kẹt" về nhóm 8 bit) |
| L05 | 6dc645a20f20b946 | khớp | khớp | 13,9 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 12 | ĐỦ | 2 | 2 | độ lệch chuẩn; tích vô hướng và độ dài véc tơ; Kafka, CDC Debezium, phân vùng bảng Oracle, bộ giới hạn tốc độ, bộ nhớ đệm L1/L2/L3 (bảng prereq chỉ nêu tên) | sơ đồ đường dẫn kép không có mũi tên nối nhánh với kết quả (frame 00016); UCB1/cosine chỉ có công thức, không có hình |
| L06 | becc3936424a5e50 | khớp | khớp | 12,8 | 1 | 2 | 1 | 2 | 2 | 2 | 1 | 11 | GẦN | 2 | 2 | SAGA, Outbox, CDC, luồng ảo Java 21, B-Tree, thanh ghi (chỉ hiện tên trên sơ đồ 4 tầng, frame 00022) | sơ đồ 4 tầng là danh sách xếp chồng, không có luồng dữ liệu; tiêu đề "Bộ 100 câu" nhưng bài chỉ dạy 5 tình huống |
| L07 | 309a3d09375ae7a0 | khớp | khớp | 12,5 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 13 | ĐỦ | 2 | 2 | không đáng kể (gross, net, BHXH, BATNA đều giảng) | quiz tính chỉ dừng 5 giây (pause: 5) cho phép tính 4 bước; scene check (tình huống) không có pause |
| L08 | d24469771719e253 | khớp | khớp | 15,3 | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 10 | GẦN | 2 | 2 | mảng/chỉ số, vòng lặp while, i++/j++ (curriculum ghi requires_ext PYT:L00–L03); CASA; "sắp xếp ngoài bộ nhớ" | hai con trỏ chỉ có mã giả (không khởi tạo i,j), không chạy tay trên hai danh sách 4–5 phần tử; lab không có bài hai con trỏ; không hình hai con trỏ chạy |
P1=2: 1/5 (20%). P8=2: 5/5 (100%). P9=2: 5/5. Ghi chú nghiêm: L05 và L06 có nhiều tên công nghệ chỉ hiện trên bảng/sơ đồ; chấm nghiêm theo rubric ("≥3 từ chưa giảng") sẽ là P1=0, tôi cho 1 vì các từ đó không gánh phần lập luận chính.

#### 4. Lab (chạy như người học; tự viết lời giải trong scratchpad r2/work_Lxx, không nhìn loi_giai.*; chấm bằng labs/cham.sh)
Cả 5 lab là giấy bút (.md). cham.sh không chấm .md/.txt (đuôi lạ → "chưa hỗ trợ đuôi tệp này"), nên tôi viết cùng đáp án bằng .py để chấm.
| Bài | tự làm được (có/không/phần) | thời gian | kẹt ở đâu | mong_doi khớp |
|---|---|---|---|---|
| L04 | có (sau khi biết hex) | ~20 phút tay | XOR từng cặp chữ số hex (FF⊕45=BA) nếu chưa biết hex; bit 41 nằm "nhóm 6" cần tự suy | cham.sh ĐÚNG, 5/5 dòng khớp mong_doi.txt |
| L05 | có (cần máy tính bỏ túi có ln, căn) | ~15 phút | ln 210, căn; hiểu "số lần thử của kênh" | ĐÚNG, 7/7 |
| L06 | có | ~10 phút | không kẹt; định dạng "262.8" tự đoán | ĐÚNG, 6/6 |
| L07 | có | ~8 phút | dòng 4 (phụ cấp cần có) cần đảo công thức, có gợi ý "nếu kẹt" | ĐÚNG, 4/4 |
| L08 | phần (lab không có bài hai con trỏ; chỉ đếm số phép so sánh) | ~12 phút | ⌈log₂ 2 000 000⌉ = 21 (có gợi ý); không có bài chạy tay hai con trỏ | ĐÚNG, 5/5 |
Màn hình "Đáp án để đối chiếu" khớp mong_doi.txt ở cả 5 bài (đã đối chiếu từng dòng).

#### 5. Người học kẹt ở đâu (chỉ xem đúng video này và các bài INT trước nó)
- L04: chỗ đầu tiên: prereq step1 "bật bit 3, 4 → 0011 0000 = 30" rồi step2 "XOR từng chữ số hệ mười sáu"; hệ mười sáu chưa được dạy trong video. Sau đó quymo "bể luồng chặn vẫn gánh được" (không giải thích bể luồng).
- L05: prereq step0 bảng "Cơ sở dữ liệu lớn: Phân vùng bảng Oracle, xử lý luồng sự kiện Kafka, CDC Debezium" (tên chưa giảng); rồi symbol step0 công thức cosine "‖u‖‖v‖" (độ dài véc tơ chưa dạy, chỉ tính ví dụ 2 chiều).
- L06: concept step0 "Máy trạng thái SAGA", "Hộp thư Outbox CDC" (không giảng, không đọc); example step1 "tệp vết chấm trc", "Deadlock Graph" (hiện tên, lời đọc giảng nghĩa vừa đủ).
- L07: không kẹt.
- L08: example step2 mã giả "while (i < core.size() && j < napas.size())… i++" (không khởi tạo i, j; không có ví dụ hai danh sách nhỏ); trước đó "sắp xếp ngoài bộ nhớ" ở quymo step1.

#### 6. Số đã tính lại / mã đã chạy
- `checks` trong YAML (eval, có import math): L04 20/20, L05 28/28, L06 19/19, L07 24/24, L08 31/31 → 122/122 khớp.
- Mã trên màn hình chạy lại: L04 (bitmap 3020000008001000, khối PIN 04122D789ABCDEF6, bảng STAN 3 mức) khớp; L05 (4400,0; 18,67; 1,21; 1,77; 0,992; bảng nhân xử lý 6 dòng) khớp; L06 (120/1200/12000; 1/3/24 máy; 99,96%; 210,2 phút) khớp; L07 (60,0/194,8/352,0) khớp; L08 (2,5 giờ vs 0,21 giây; 250/2,37; 25000/27,3; 0,3/3,0/30,0 GB) khớp → 5/5 đoạn mã, mọi dòng khớp.
- Tính thêm độc lập: Z=(30−2)/1,5; đường chim bay TP.HCM–Singapore ≈1 100 km (khoảng 1 095 km tính tay từ toạ độ, đúng); 525 600×0,0001=52,56; 0,9995³ → 99,85% và 788,0 phút; mã đáp án 5 lab đều khớp mong_doi.txt (cham.sh ĐÚNG).
- Mã Java mã giả (L05 ONNX, L08 hai con trỏ): chỉ đọc, không chạy.

#### 7. Khung hình đã xem (≥5/bài)
- L04: 00014 (MTI/bitmap), 00028 (sơ đồ hàng đợi), 00042 (mã + kết quả), 00047 (bảng STAN), 00066 (quiz đáp án), 00081 (tổng kết). Không lỗi hiển thị.
- L05: 00001 (hook), 00016 (đường dẫn kép), 00025 (công thức, LaTeX hiển thị đúng), 00028, 00050 (bước 3 + QĐ), 00076 (quiz), 00092 (tổng kết). Lỗi nhẹ: 00016 hộp "Quyết định tức thời" và "Phân tích Đồ thị AI" không có mũi tên nối.
- L06: 00012, 00022 (4 tầng), 00030 (SLA, công thức "E < 0,001%" hiển thị đúng), 00038, 00055, 00083. Không lỗi.
- L07: 00018 (3 vòng), 00030 (công thức), 00041 (bảng đòn 3), 00050 (mã Python), 00068 (quiz), 00087 (tổng kết). Không lỗi.
- L08: 00012, 00018 (6 phân hệ), 00040 (O-notation, mũ hiển thị đúng), 00043, 00045 (mã giả, đọc được), 00050 (mã + kết quả), 00060 (bẫy khoá), 00085. Không lỗi.
- Lưu ý công cụ: bản digest của tôi bỏ chữ `<`; đã đối chiếu YAML gốc (L06 `teamSize < 10`, `E < 0,001%`; L08 `i < core.size()`), khung hình hiển thị đúng.

#### 8. Số pháp lý / lương / nguồn (INT L04–L08)
| Bài | Số/văn bản | Nguồn trong bài | Đánh giá |
|---|---|---|---|
| L04 | ISO 8583:1987, MTI 0400/0420, mã 68 | `source:` ghi "theo hiểu biết về chuẩn… chưa mở", "đặc tả NAPAS chưa kiểm được", màn hình ghi "cần kiểm" | Đúng với hiểu biết của tôi; hedge rõ. SHOULD về 0400 (mục 2) |
| L05 | TT 50/2024/TT-NHNN, TT 77/2025/TT-NHNN; ngưỡng 10 triệu/lần, 20 triệu/ngày; QĐ 2345 | Không có trong `source:`; màn hình tự ghi cách dùng | Ngưỡng khớp TT 50; TT 77 chưa kiểm được; QĐ 2345 ghi "chưa đọc nguyên văn, chưa rõ còn áp dụng" |
| L06 | như L05 + SLA 99,99% / 120 ms / 10 000 TPS | "yêu cầu giả định của đề bài, không phải số liệu của ngân hàng nào" | Số minh hoạ ghi rõ, không phải số thực |
| L07 | Lương: không có mức lương nào (mọi số là minh hoạ); tháng 13 cố định, thưởng 1–4 tháng = tin tuyển dụng ACB đọc 2026-11 | `source:` có; không URL | Không có số lương không nguồn. Tên tệp `L07_salary_negotiation_50m_gross` chứa "50m" (đường dẫn, không hiện trong video) trái với lời bài "không đưa mức lương nào". Thời gian thử việc: "cần kiểm lại văn bản hiện hành" (đúng cách) |
| L08 | TT 31/2024/TT-NHNN (nhóm 2: 10–90 ngày; nhóm 3: 91–180), TT 37/2025/TT-NHNN sửa đổi | `source:` ghi 2 nguồn thứ cấp + cần bản hợp nhất; màn hình ghi cần đối chiếu | Hedge đủ; nhóm 10–90 ngày khớp hiểu biết; số điều không nêu. Không kiểm được TT 37/2025 |
| L04–L08 | Tên người thật | Chỉ có: Auer/Cesa-Bianchi/Fischer 2002 (L05), sách SRE Google 2016 (L06), Temenos/Thales payShield (L04) | Đúng, có chú thích |

#### Trích QĐ 2345 / sinh trắc học / lương (nguyên chữ, để đối chiếu với ACB)
- L05 example step3 (màn hình): "Phân biệt với quy định của Ngân hàng Nhà nước: theo Thông tư 50/2024/TT-NHNN (sửa đổi bởi Thông tư 77/2025/TT-NHNN), chuyển tiền trực tuyến trên 10 triệu đồng một lần hoặc tổng trong ngày trên 20 triệu đồng phải xác thực sinh trắc học. Đó là ngưỡng theo quy định, khác ngưỡng điểm rủi ro của mô hình. Quyết định 2345/QĐ-NHNN cũng hay được nhắc nhưng chưa đọc nguyên văn, chưa rõ còn áp dụng; bài không nêu số điều, khi làm thật hãy mở văn bản hiện hành."
- L05 say (cùng step): "Theo Thông tư 50 năm 2024, đã được sửa đổi, chuyển tiền trực tuyến trên 10 triệu một lần hoặc tổng ngày trên 20 triệu phải xác thực sinh trắc học… Quyết định 2345 cũng hay được nhắc, nhưng bài chưa đọc nguyên văn nên không dựa vào nó."
- L06 check step0 (màn hình): "theo Thông tư 50/2024/TT-NHNN (sửa đổi bởi Thông tư 77/2025/TT-NHNN), phải xác thực khuôn mặt khi một lần chuyển trên 10 triệu đồng hoặc khi tổng chuyển trong ngày vượt 20 triệu đồng. Quyết định 2345/QĐ-NHNN cũng hay được nhắc nhưng chưa đọc nguyên văn, chưa rõ còn áp dụng; bài không nêu số điều." (say step0 không đọc phần QĐ 2345 và không đọc số thông tư; say step1: "…luôn phải xác thực khuôn mặt theo đúng quy định.")
- L06 labs/INT/L06/de.md: "…(theo Thông tư 50/2024/TT-NHNN, sửa đổi bởi Thông tư 77/2025/TT-NHNN; Quyết định 2345/QĐ-NHNN chưa đọc nguyên văn, chưa rõ còn áp dụng nên không dùng làm căn cứ…)"; curriculum L06 objective 5: "Xác định khi nào bắt buộc xác thực khuôn mặt theo ngưỡng một lần chuyển trên 10 triệu hoặc tổng trong ngày trên 20 triệu".
- L06 lab step2 (màn hình): "Ngưỡng sinh trắc học: một lần trên 10 triệu, hoặc tổng trong ngày trên 20 triệu."
- L06 nhận xét: trong INT, "sinh trắc học" ở L05/lab L06 và "xác thực khuôn mặt" ở L06 quiz được dùng thay nhau; L06 thu hẹp thành "khuôn mặt".
- L04, L07, L08: không nhắc QĐ 2345. L08 concept: "Xác thực khuôn mặt + OTP" (Cloud CA), kèm prereq "(khung pháp lý cần kiểm lại khi dẫn)".
- L07 lương: chỉ khung tháng 13 cố định + thưởng 1–4 tháng lương (tin ACB) và số minh hoạ L=32/34/36/38/40; câu "tin tuyển dụng chính thức thường ghi lương là «Thương lượng»". Không có mức lương nào được khẳng định là thật.

#### 9. Nhận xét chung
- Chuẩn xác tốt: MUST 0; 122/122 check, mọi mã màn hình chạy khớp, spec/SRT khớp 5/5.
- Điểm yếu lớn nhất là P1 (nền): 1/5 bài đạt 2, vì bảng/sơ đồ nêu tên công nghệ (SAGA, Outbox, CDC, Kafka, hex, con trỏ) mà không giảng; P1 sẽ không đạt ngưỡng 90% cho phần này.
- P8 và P9 mạnh: cả 5 bài có lab giấy bút số mới + đáp án + "nếu kẹt"; cả 5 có bảng 2–3 mức quy mô/thời gian.
- L08 yếu nhất về sư phạm (GẦN, 10): thuật toán hai con trỏ không có hình/ví dụ nhỏ, lab không kiểm hiểu hai con trỏ.
- Lab là giấy bút nhưng cham.sh không chấm .md/.txt: người học phải tự so mắt hoặc viết chương trình; nên cho phép chấm tệp văn bản.
- Trung thực hồ sơ làm tốt (gắn cờ "minh hoạ", "chưa đọc nguyên văn"); chỗ còn lệch: tiêu đề L06 "Sự cố … Thực tế tại OCB".


<!-- part C -->
### R2 ACB phần C (L00–L03): đã đọc 4/4 bài

Bài đã đọc trọn (digest toàn bộ scene/step/quiz/checks/lab + chạy lab + 5–7 khung hình): ACB L00, L01, L02, L03.
Ghi chú quy trình: lúc dò nguồn mã tôi mở nhầm 40 dòng đầu `audit/review/screen_code/ACB.yaml` (sổ mã màn hình, không phải báo cáo đọc; thấy mục L01 symbol và L03 symbol). Các phán đoán dưới đây về cú pháp OFS/ksqlDB là của tôi, không dựa vào sổ đó.

#### 1. Chuẩn xác (Phần A)

MUST: 0. SHOULD: 4 (đều nhẹ).

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L00 | — | | | không phát hiện lỗi kiến thức. Mọi số (600 000; 36 triệu; 155 ms; 15,5/1 550/155 000; 6 000/600 000/60 triệu; 520/560/680 triệu) chạy lại khớp | | |
| L01 | SHOULD | check/step 0 (bảng) | cột "cách xử lý sai lầm": "Gây lệch sổ cái hoặc trừ tiền 2 lần" | nhãn cột sai: ô này là HẬU QUẢ, không phải cách xử lý; ghép hàng 3 với "Chỉ hoàn tiền khi có kết quả đối soát" thành cặp sai–đúng không tương ứng | đổi nhãn hoặc bỏ hàng, hoặc viết hành động sai thật ("hoàn tiền ngay khi chưa tra soát") | CONFIRMED |
| L02 | SHOULD | check/step 0 (bảng) | cột "hành động sai lầm": "Gây thất thoát 10 triệu đồng của ngân hàng" | cùng lỗi nhãn: là hậu quả, đứng cạnh "Đối soát tự động với tệp quyết toán cuối ngày" | như L01 | CONFIRMED |
| L02 | SHOULD | check/step 0 (lời đọc) | "vượt quá hạn mức 1500 mi li giây" | dùng sai thuật ngữ: 1500 ms là ngưỡng chờ (timeout), "hạn mức" trong ngân hàng là hạn mức tiền; người mất gốc dễ nhầm với hạn mức giao dịch | đổi thành "ngưỡng chờ" (màn hình đã ghi "ngưỡng chờ") | CONFIRMED |
| L03 | SHOULD | check/step 0 (bảng) | "Làm thất lạc mã xác thực của khách" (cột "cách xử lý sơ cấp") | cùng lỗi nhãn (hậu quả, không phải hành động); hàng 3 cột phải "Đẩy các tin nhắn thường vào hàng đợi chờ xử lý sau" không đối ứng | như L01 | CONFIRMED |
| L03 | SHOULD | symbol/step 0, concept | "Ngưỡng SMS ≥ 50k VND" / "từ 50 nghìn đồng trở lên, hệ thống sẽ gửi tin nhắn" | ngưỡng 50 000 đồng là quy tắc minh hoạ (trường `source` ghi "ngưỡng... là số minh hoạ") nhưng ở cảnh concept/symbol không gắn nhãn "minh hoạ" (chỉ gắn ở hook, quymo, practice) | thêm "(ngưỡng minh hoạ)" vào hộp sơ đồ và dòng chú dưới câu SQL | CONFIRMED |
| L03 | SHOULD | example/step 2 | "Kafka giao ít nhất một lần, nghĩa là một sự kiện có thể đến hai lần" | thiếu điều kiện: đó là mặc định at-least-once; Kafka có producer idempotent/giao dịch (exactly-once trong Kafka–Kafka). Phần kết luận đúng vì tác dụng phụ ra ngoài (gửi SMS) vẫn at-least-once | thêm "ở cấu hình mặc định và với tác dụng phụ ra ngoài Kafka" | PLAUSIBLE |

Kiểm đặc biệt đã làm và KHÔNG thấy lỗi: ISO 8583:1987 (field 3, 4, 11, 37, 52, 64, 128; bitmap 0x72 và 0xF2; bit 1 = bitmap thứ hai; MTI 0200/0210/0400/0420; VND 0 số lẻ theo ISO 4217); bitmap `3020000008000000`/`7200000000000000`/`3020000008800000`/`B020000008000000 0000000000000001`; Little L = N × W; Spring tự gọi hàm nội bộ; Oracle khoá ngoại thiếu chỉ mục; BOTHRESH/BOQNAME; ksqlDB LEFT JOIN + CASE với NULL (`NULL = TRUE` rơi xuống nhánh sau, khớp mã Python `None`); stream–stream JOIN cần WITHIN.

#### 2. Bảng độ sâu

(P1 chấm nghiêm: 2 chỉ khi không còn từ nào kẹt.)

| Bài | sha16 YAML | spec khớp | SRT khớp | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ACB L00 | c45a30757ea2a3f6 | Có (52a96d64f2a7…) | Có (2066/2066 từ, ratio 1.0) | 14,1 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ (sát ngưỡng) | NAPAS (không định nghĩa trong bài), Spring Boot/framework, socket/TCP (chỉ trên sơ đồ), API REST, "Core Banking" chỉ gloss "hệ thống lõi", SLA (gloss một nửa), Python cơ bản (đã gọi PYT) | P1: ≥3 từ không giảng (NAPAS, TCP/socket, Spring Boot); P3: sơ đồ 4 hộp chỉ liệt kê tên, không vẽ cơ chế SAGA/dedup; cảnh SAGA (check) chỉ chữ |
| ACB L01 | ccecb35d369e3196 | Có (f6d8d61f4043…) | Có (1842/1842, 1.0) | 12,9 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | JMS (trong JMSCorrelationID, không giảng), microservice, consumer, Python hàm/từ điển (giảng thoáng) | P1: JMS, microservice, consumer chưa giảng; cú pháp OFS chưa kiểm nguồn (ghi ở `source`, màn hình chỉ ghi "ví dụ minh họa") |
| ACB L02 | a8c991f302517b4b | Có (4bade9a65b16…) | Có (2077/2077, 1.0) | 14,7 | 1 | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 11 | GẦN | ràng buộc UNIQUE trong CSDL, byte, toán tử `\|` và vòng for Python, đổi hex↔nhị phân (chỉ nói "một chữ số thay bốn bit"), "đối soát ba bên" | P2: nhảy 0111 0010 → 72 không viết 0111=7, 0010=2; bài chỉ dạy ráp bitmap, KHÔNG dạy giải mã nhưng lab đòi giải mã `5030…`; P3: bitmap không có hình, sơ đồ 4 hộp thứ tự khác lời đọc (lời đọc phải chú thích "ô vẽ ở cuối hình") |
| ACB L03 | ddcb2ad4eafb576e | Có (b6b9b329f9f6…) | Có (1837/1837, 1.0) | 13,6 | 1 | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 11 | GẦN | phân vùng (partition) Kafka, microservice, consumer/tiến trình song song, SMS Brandname (chỉ gloss), SQL cơ bản (JOIN/CASE), `import heapq` | P1: "phân vùng" dùng ở quymo mà chưa giảng; P2/P3: xô thẻ chỉ giảng bằng lời, không có ví dụ số hay hình, trong khi lab đòi cài đặt |

P1=2: 0/4. P8=2: 4/4. P9=2: 4/4. Spec khớp 4/4, SRT khớp 4/4.

Căn cứ P8/P9: mỗi bài có cảnh practice với số khác ví dụ, kết quả mong đợi trên màn hình, lệnh chấm `cham.sh`, lời giải ở `labs/ACB/Lxx/loi_giai.py` (P8=2). Mỗi bài có cảnh quymo ×1/×100/×10 000 và cảnh/ô "theo thời gian" (L00 không có hàng thời gian riêng nhưng có đánh đổi theo quy mô; L01 hàng đợi ứ; L02 TTL 30 vs 90 giây; L03 khoá 24 giờ vs 1 giờ) cùng đánh đổi nêu rõ (P9=2).

Quiz (cả 4): có dừng 15 giây, lời giải 2 bước; phương án nhiễu yếu (L01 B/C/D, L02 B/C/D, L03 B/C/D rõ là sai). Vẫn cho P5=2 vì kiểm hiểu và có lời giải; ghi nhận làm điểm yếu nhỏ.

#### 3. Lab (tự làm trong scratchpad r2/work_Lxx/mau.py, chấm bằng cham.sh)

| Bài | tự làm được | thời gian (ước cho người học; tôi làm vài phút) | kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L00 | Có, ĐÚNG ngay lần 1 | ~10 phút | Gần như không; có thể kẹt cú pháp `print` nhiều giá trị và định dạng đúng dòng 3 (`toan trinh: 130 ms, dat P99`) → mẫu có trong de.md | Khớp (5 dòng) |
| L01 | Có, ĐÚNG lần 1 | ~20–25 phút | tách `tin.split(",")` rồi ghép lại "ofs dau" kết thúc bằng hai dấu phẩy (hơi rối); làm tròn lên `-(-a // b)` chưa dạy, chỉ gợi ý "làm tròn lên" | Khớp (8 dòng) |
| L02 | Có, ĐÚNG lần 1 (khi đã biết `int(x,16)` và `>>`) | ~30 phút | Giải mã `5030000000000000`: bài không dạy `int("..",16)` và dịch phải `>>`; chỉ có gợi ý "xét từng trường 1..64". Bitmap B cần thêm trường 1 và bitmap phụ `0000000000000001`: đề giải thích đủ nhưng dễ nhầm vị trí 64 | Khớp (7 dòng) |
| L03 | Có, ĐÚNG lần 1 | ~30 phút | Xô thẻ: lời đọc chỉ nói bằng lời, lab đòi cài (`min(3, the + giây trôi)`); gợi ý "Nếu kẹt" nêu thuật toán đủ để làm. Định dạng `uu tien` dùng `" \| "` | Khớp (4 dòng) |

`loi_giai.py` của cả 4 bài chạy ĐÚNG; lời giải của tôi trùng logic.

#### 4. Người học kẹt ở đâu (chỗ đầu tiên không theo được)

- L00: hook (scene hook): không kẹt; chỗ đầu tiên khó là scene concept "Dịch PIN... Socket TCP nhị phân" (socket/TCP/NAPAS chưa định nghĩa trong bài này) và code scene (Python giả định PYT).
- L01: scene symbol step 1 là ổn; kẹt đầu tiên ở quiz "JMSCorrelationID" (JMS chưa giảng) và ở code scene (hàm, từ điển `.pop`).
- L02: scene symbol step 1: "Viết gọn tám bit đó theo hệ mười sáu, tức một chữ số thay cho bốn bit, ta được bảy hai" — không viết 0111→7, 0010→2; sau đó code scene `bits | (1 << (64 - n))` dùng toán tử `|` chưa giảng.
- L03: scene quymo "nên Kafka phải có ít nhất hai phân vùng" (phân vùng chưa giảng ở bài này); scene pitfall nói xô thẻ bằng lời, không có ví dụ số.

#### 5. Số đã tính lại / mã đã chạy

- `checks` trong YAML: 20 + 17 + 23 + 16 = 76 biểu thức, 76 đúng.
- Mã trên màn hình đã chạy lại: L00 (5 dòng) khớp; L01 (hàm `ofs` + ghép trả lời) khớp 5/5 dòng; L02 (bandobit, `dat`) khớp 5/5 dòng; L03 (kenh, heapq) khớp theo `checks` và lab 4/4. SQL ksqlDB và OFS: chỉ đọc, không chạy (không có ksqlDB/T24).
- Số tính lại bằng Python: Little 5000×0,035=175, ceil(5000/28)=179, 50→2, 500 000→17 858; 8000×0,12=960, 80→9,6, 800 000→96 000; 4000×60=240 000; 500×1440=720 000, 5 000 000×1440=7,2 tỉ, 83 333/500→167; bitmap 4 giá trị; 90 000×65/100=58 500. Tất cả khớp (có tính cả số trên cột "Quy mô" của 4 bài). Tổng lab mong_doi 4/4 khớp.
- Spec/SRT: `spec_digest` bỏ asr_reviewed khớp `build_report.json spec_sha256` ở 4/4 (L00 52a96d64f2a748da, L01 f6d8d61f40436575, L02 4bade9a65b169ad0, L03 b6b9b329f9f6dfcd). So SRT với `say` theo từng từ: 0 khác biệt ở 4/4.

#### 6. Khung hình đã xem (frames/*.png; 1 khung = 1 khối SRT)

- L00: 00000 (hook), 00025 (sơ đồ 4 tầng), 00033 (bảng độ trễ), 00040 (mã Python), 00068 (bảng quy mô), 00078 (đáp án quiz), 00104 (tổng kết) — 7 khung.
- L01: 00000, 00020 (sơ đồ request/reply), 00028 (OFS ráp), 00045 (mã Python), 00066 (bảng quy mô), 00078 (lời giải quiz) — 6 khung.
- L02: 00000, 00024 (sơ đồ), 00038 (bitmap), 00058 (mã khoá), 00079 (theo thời gian), 00085 (quiz câu hỏi + nút "Dừng video"), 00101 (tổng kết) — 7 khung.
- L03: 00000, 00021 (sơ đồ), 00029 (SQL), 00064 (bảng quy mô), 00076 (lời giải quiz), 00088 (tổng kết) — 6 khung.
Lỗi hiển thị: không thấy chữ tràn/đè/cắt; cỡ chữ đọc được; LaTeX hiển thị đúng. Lưu ý nhỏ: sơ đồ L02 vẽ "Core Banking" ở ô 4 cuối trong khi lời đọc nói Core đã giữ tiền từ trước (lời đọc có chú thích); sơ đồ L03 ô 4 ghi "Email sao kê định kỳ" nhưng câu SQL gửi EMAIL cho biến động nhỏ (không phải sao kê định kỳ) — mâu thuẫn nhãn nhẹ, không xếp mức.

#### 7. Số pháp lý / lương / tên người thật / nguồn (L00–L03)

- Không có số văn bản pháp lý, mức phí ngân hàng hay tỉ lệ pháp định trong 4 bài.
- L00 lương: "35 đến 40 triệu", "L = 40 triệu", 520/560/680 triệu đều gắn rõ "số minh hoạ, không phải số có nguồn"; dữ kiện có nguồn duy nhất: lương tháng 13 cố định và thưởng cuối năm 1–4 tháng, khớp `resources/job/JD.md` dòng 72 và 79 (nguồn bên thứ ba/JD, bài tự ghi "bản đã lưu, CHƯA kiểm lại trang gốc"; ACB ghi "Thương lượng"). Không có khung lương thị trường (bài nói rõ "chỉ có ở các bài tổng hợp chưa kiểm chứng"). Đạt yêu cầu "không số không nguồn".
- L00 mô tả công việc ACB ("thủ tục lưu trữ Oracle/SQL Server, Java Spring Boot, nghiệp vụ ngân hàng là lợi thế"): khớp JD.md dòng 6, 66, 116.
- Tên/lý lịch người học (UIT dự kiến 11/2026; OCB Squad Lending, 3 năm; Mirae Asset): khớp `resources/job/PHAM-MINH-DUC-SENIOR-INTEGRATION-CV.md` (OCB 3+ năm, Squad Lending, MAFC, UIT 06/2025–11/2026 dự kiến). Chức danh "Chuyên viên chính" là cách dịch của "Senior Integration Application Specialist" trong CV, chưa kiểm được ở tài liệu gốc khác. Không có tên người thật nào khác.
- Số hiệu năng (TPS, ms, TTL, hệ số 1,5, 70%...): đều gắn "số minh hoạ/giả định", trường `source` nêu rõ không phải số của ngân hàng nào.
- Đặc tả NAPAS và OFS của Temenos: bài tự ghi "cần kiểm"/"chưa kiểm được" (L00, L02 trên màn hình; L01 chỉ ở trường `source`).

#### 8. Trích QĐ 2345 / sinh trắc học / hạn mức (L00–L03)

Không có chỗ nào nhắc QĐ 2345 trong L00–L03. Chỗ gần nhất:
- L00 concept (sơ đồ): "API Gateway · mTLS & khuôn mặt"; lời đọc "Tầng một là kênh số tiếp nhận yêu cầu và xác thực danh tính."
- L02 concept (sơ đồ): "Xác thực sinh trắc học"; lời đọc "ứng dụng số nhận yêu cầu chuyển tiền và xác thực sinh trắc học của khách hàng."
- "Hạn mức" chỉ xuất hiện như từ dùng sai ở L02 check ("hạn mức 1500 mi li giây", đã nêu ở SHOULD).
Nhất quán QĐ 2345 INT/ACB cần đối chiếu ở ACB L06 (phần fork khác).

#### 9. Nhận xét chung

- Chuẩn xác tốt: 0 MUST; spec/SRT/mã/số đều khớp; mọi số liệu hiệu năng và lương đều gắn nhãn minh hoạ/có nguồn.
- Điểm yếu lớn nhất là P1 (từ chưa giảng tại chỗ) và P3: bài ACB dựa nhiều vào khái niệm đã dạy ở bài trước cùng khoá hoặc PYT (requires_ext), nên nếu học lẻ thì kẹt ở TCP/socket/phân vùng/UNIQUE/JMS.
- L02 và L03: lab đòi kỹ năng chưa dạy trên video (giải mã hex bằng `int(...,16)` và `>>`; cài xô thẻ) — gợi ý "Nếu kẹt" cứu được nhưng video nên có ví dụ số tương ứng.
- Ba cảnh "check" (L01, L02, L03) dùng bảng sai–đúng nhãn lệch (hậu quả đặt dưới cột hành động): sửa chung bằng một mẫu.
- Lab chạy sạch, đề đủ để tự làm, mong_doi khớp màn hình ở 4/4.


<!-- part D -->
### R2 phần D — ACB L04–L08: đã đọc 5/5 bài (digest trọn từng bài, chạy lab, 5–6 khung hình mỗi bài)

Bài đã đọc: lessons/acb/L04_san_chuyen_nhuong_hop_dong_tien_gui, L05_cong_chi_luong_va_sao_ke_divide_conquer, L06_sinh_trac_hoc_qd2345_va_bao_mat_ngan_hang, L07_tai_khoan_dinh_danh_va_doi_soat_ba_ben, L08_squad_lending_tich_hop_cic_giai_ngan (cùng labs/ACB/L04..L08 và out/ACB/L04..L08).

Tổng: MUST 0; SHOULD 6 (2 CONFIRMED, 4 PLAUSIBLE). spec_sha256 khớp 5/5. SRT = say từ-theo-từ 5/5 (độ khớp 1.0, 0 chênh). P1=2: 1/5. P8=2: 5/5.

#### 2. Bảng chuẩn xác (chỉ lỗi có bằng chứng)

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| ACB L04 | — | | | không phát hiện lỗi (18/18 checks, 2 khối mã chạy khớp, lab ĐÚNG) | | |
| ACB L05 | SHOULD | example step 3 (Bước 4 Divide-and-Conquer), khung 00052.png | `$1\,000\,000 <TAB>imes 9 / 30 = 300\,000$` (lessons/acb/L05...yaml dòng 412 có ký tự TAB thật) | `\times` bị YAML nuốt thành TAB + "imes": khung hình hiện "1 000 000imes9/30 =" đúng ngay phép tính 300 000 bản ghi của đoạn 9 ngày. Kết quả 300 000 đúng (1e6*9/30), chỉ hiển thị hỏng. grep -P "\t" trên 18 bài INT+ACB: chỉ có dòng này | thay bằng `\\times` hoặc `\times` trong chuỗi YAML đơn/khối; dựng lại | CONFIRMED |
| ACB L06 | SHOULD | hook step 0; prereq step 0; recap | "Thông tư 50/2024/TT-NHNN, sửa đổi bởi Thông tư 77/2025/TT-NHNN ..., Phụ lục 01." / "giao dịch trên 10 triệu đồng một lần, hoặc tổng trong ngày vượt 20 triệu đồng, phải xác thực sinh trắc học" | Ngưỡng 10 triệu/lần, 20 triệu/ngày trong báo chí và ngân hàng (vnreview, Báo Đầu tư, MSB, Tạp chí Ngân hàng) được gắn với QĐ 2345/QĐ-NHNN (hiệu lực 01/07/2024); một nguồn (hoatieu.vn) gắn 10/20 triệu với Phụ lục 02 TT 50/2024 (OTP kèm sinh trắc học), không phải Phụ lục 01. audit/legal/registry.yaml ghi 77/2025 Điều 10 thay Phụ lục 01, 02, 04 áp dụng từ 01/07/2026 (khách cá nhân) và ngưỡng 10/20 thuộc nhóm chuyển cho chủ tài khoản khác, "xác thực mạnh = sinh trắc + thêm một yếu tố": nguồn thứ cấp, CHUA_KIEM. Bài nói "ngưỡng ghi ở TT 50/2024 đã sửa đổi" nhưng không chứng minh con số còn nằm trong Phụ lục 01 sau khi Điều 10 thay phụ lục (hôm nay 15/11/2026 đã quá 01/07/2026). Tôi tìm web không thấy nguồn chính thức nêu 10/20 trong Phụ lục 01 sau sửa đổi. Cảnh đã tự khai "chưa đọc nguyên văn" nên không phải MUST | Hoặc đọc nguyên văn Phụ lục sau 77/2025 rồi ghi số điều, hoặc nói rõ "con số 10/20 phổ biến trên báo gắn QĐ 2345 và chưa đối chiếu Phụ lục mới" và thêm điều kiện "chuyển cho chủ tài khoản khác" | PLAUSIBLE |
| ACB L06 | SHOULD | prereq step 0 hàng 3 + code step 0 + lab | "sau mỗi lần xác thực thành công, tổng cộng dồn tính lại từ 0 (giả định minh hoạ, không có số điều)" | Đã gắn nhãn giả định, nhưng đây là quy tắc có vẻ trái cách hiểu phổ biến "tổng trong ngày > 20 triệu"; lab mong_doi `3 thuong tong: 3` (sau hai lần quét, tổng cả ngày 40 triệu) dạy người học kết quả mà thực tế có thể phải quét lại. Người học dễ mang quy tắc này vào buổi phỏng vấn | Thêm một câu nói rõ "thực tế hỏi ngân hàng/đọc văn bản có reset hay không", hoặc đổi lab sang cộng dồn không reset | PLAUSIBLE |
| ACB L06 | SHOULD | symbol step 0 (vé) | "Không đưa số CCCD vào vé (Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15)." | Câu đặt Luật 91/2025/QH15 làm căn cứ cấm đưa số CCCD vào vé; luật quy định nguyên tắc giảm thiểu dữ liệu, không có điều cấm cụ thể này (không kiểm được số điều; registry không có mục 91/2025/QH15 đã đọc nguyên văn trong phần tôi xem). Là khuyến nghị thiết kế, không phải điều luật | đổi thành "nên tránh đưa số CCCD vào vé theo nguyên tắc giảm thiểu dữ liệu (Luật 91/2025/QH15, chưa kiểm số điều)" | PLAUSIBLE |
| ACB L07 | SHOULD | pitfall step 0 (SAY) | SAY: "Thứ ba là dùng vòng lặp lồng nhau gây nghẽn bộ nhớ khi đối soát." ; SHOW: "Độ phức tạp O(N²) làm sập hệ thống sau nửa đêm" | Lời đọc nói "nghẽn bộ nhớ", màn hình nói O(N²); hậu quả của vòng lặp lồng nhau là thời gian tính (9 000 giây ở cảnh quymo ngay sau), không phải bộ nhớ. Lời đọc lệch màn hình ở điểm kiến thức nhỏ | sửa SAY: "khiến thời gian đối soát tăng theo bình phương số bản ghi" | CONFIRMED |
| ACB L08 | SHOULD | hook step 1 / quiz step 1 | "Nhóm 2 (nợ cần chú ý: quá hạn từ 10 đến 90 ngày, Thông tư 31/2024/TT-NHNN ...)" | Nhóm 2 theo Điều 10 còn gồm khoản được điều chỉnh kỳ hạn lần đầu còn trong hạn và các trường hợp ở khoản 2, 3 Điều 10 (LawNet bản dịch, Home Credit); bài rút gọn thành "quá hạn 10–90 ngày". Cảnh đã ghi nguồn thứ cấp và "đã bị TT 37/2025 sửa đổi" (web xác nhận TT 37/2025 sửa TT 31/2024; chưa xác nhận Điều 10 có đổi không) | thêm "(định nghĩa rút gọn: còn trường hợp điều chỉnh kỳ hạn...)" | PLAUSIBLE |
| ACB L08 | SHOULD (hiển thị nhỏ) | concept step 0, khung 00022.png | "Chuyển tiền qua NAPAS 247" | dòng chữ chạm/đè viền phải của hộp 4 và đường nối | rút ngắn "NAPAS 247" hoặc nới hộp | CONFIRMED |
| ACB L07 | — | | | ngoài mục trên không phát hiện lỗi (23/23 checks gồm log2, 3 khối mã chạy khớp) | | |

#### 3. Bảng độ sâu

| Bài | sha16 YAML lúc đọc | spec khớp | SRT khớp | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước (dùng, không giảng tại chỗ) | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ACB L04 | 80555855f10bdadb | có (1518c437) | có, 1773/1773 từ | 13,7 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | HTTP và mã 409/Timeout, "sổ cái", adapter, SELECT FOR UPDATE (OFS/CIF/Core lấy từ L01), Go (có chú thích) | HTTP 409 chỉ nêu như mã, không giảng HTTP; quiz phương án B/C/D lộ liễu sai |
| ACB L05 | a6e347d7e4c7a0aa | có (988a1cc0) | có, 2266/2266 | 16,7 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "tiến trình", read replica (ngoặc đơn), Oracle/PL/SQL (có giảng ngắn) | P3: công thức 300 000 bản ghi hỏng hiển thị (xem SHOULD); lab đòi tự dựng kiểm vòng chờ nhưng bài chỉ dạy bảng khoá, không có mã phát hiện vòng |
| ACB L06 | 39f325afffb344b5 | có (f7974d53) | có, 1889/1889 | 14,8 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | băm/SHA-256 (txn_hash), chứng chỉ số/TLS (L00), API/Gateway/403, JSON, 1:1 so khớp | "mã băm" dùng mà không giảng tại chỗ; điều kiện áp dụng ngưỡng thiếu (xem SHOULD) |
| ACB L07 | 94a00caf6ae662ff | có (a858affd) | có, 2093/2093 | 15,9 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | HTTP header/POST/payload, Redis `SET ... NX EX 120`, B-Tree, hash join/sort-merge join, topic | thuật ngữ HTTP và Redis cú pháp xuất hiện ở bảng, không giảng; hash join chỉ nói "chính là sắp xếp rồi trộn" |
| ACB L08 | f3562d6084dee70f | có (0056b16b) | có, 2069/2069 | 15,9 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | CASA, AZ, tất toán, Partial/Auto-Debit, Go, sổ cái, B2B | CASA/AZ/Partial Debit chỉ nêu tên; "tất toán" chưa giảng |

Ghi chú chấm: P5 chấm 2 cho cả 5 bài (có dừng 15 s, lời giải theo bước) nhưng phương án nhiễu của quiz đều lộ liễu (L04-L08), nên quiz kiểm "chọn đáp án hợp lý" hơn kiểm hiểu sâu. Tổng 5 bài: P1=2 ở 1/5 (20%); P8=2 ở 5/5 (100%); P9=2 ở 5/5.

#### 4. Lab

| Bài | tự làm được | thời gian ước | kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| ACB L04 | có (không nhìn loi_giai; cham.sh ĐÚNG ngay lần 1) | ~15 phút | không kẹt; chỉ cần biết rowcount và set Python (có trong bài) | khớp: màn hình bài ra "mua 1: 1 / mua 2: 0 / ver: 8", lab ra A:1,B:0,C:0, ver 4, lãi 20400000, 164384, mất 20235616, hai dòng máy trạng thái; chạy được |
| ACB L05 | có (cham.sh ĐÚNG lần 1) | ~30 phút | chỗ viết hàm mô phỏng "đang chờ không giữ thêm khoá" và kiểm A chờ B và B chờ A; bài chỉ dạy từ điển khoá, đề phải tự suy ra luật; không cần kiến thức ngoài | khớp 6 dòng |
| ACB L06 | có (cham.sh ĐÚNG lần 1) | ~25 phút | không kẹt nếu đã xem code hmac trong bài; "lấy 8 ký tự hệ mười sáu đầu" = hexdigest()[:8] hơi khó với người chưa thấy | khớp 9 dòng (HMAC chạy thật, đầu ra không phụ thuộc khoá tự chọn) |
| ACB L07 | có (cham.sh ĐÚNG lần 1) | ~25 phút | phân loại ba nguồn: đề nêu rõ năm nhãn, nhưng "có ở Core và ERP, thiếu NAPAS" rơi vào nhánh "có ở Core không có ở NAPAS" của đề, người học phải đọc kỹ thứ tự nhánh | khớp 13 dòng |
| ACB L08 | có (cham.sh ĐÚNG lần 1) | ~25 phút | không kẹt; in `7.5` của 4.8+2.7 đúng (không có lỗi số thực, nhưng bài không cảnh báo cách làm tròn float) | khớp 8 dòng |

#### 5. Người học kẹt ở đâu (chỉ xem video này + bài trước cùng khoá)

- L04: không kẹt nặng; chỗ đầu tiên chậm là concept step 2: tên bản tin "ACCOUNT_T24_DEPOSIT_OFS ... AZ_ACCOUNT_T24_OFS_AMD" (dựa vào OFS ở L01) và example step 1: "HTTP 409 Conflict (Sổ đã bán)" khi HTTP chưa được giảng.
- L05: symbol step 0: "FROM TABLE(p_acc_list) ORDER BY 1 ... FOR UPDATE" (PL/SQL chưa học, chỉ có chú thích một dòng); example step 3: công thức bị hỏng "1 000 000imes9/30".
- L06: symbol step 0: JSON vé "txn_hash": "sha256(amount|to_account|txn_id)" và "signature": "MEUCIQ..." (băm/chữ ký chưa giảng tại chỗ).
- L07: example step 0: "Khoá phân tán Redis SET va:dedup:TXN_8888 NX EX 120 chặn nhanh bản tin trùng" (cú pháp Redis, header HTTP chưa giảng); symbol: "POST /api/v1/webhook/billing-clear | Host: ... X-Event-ID".
- L08: concept step 0: "Khoá phong tỏa sổ AZ / Cấp hạn mức thấu chi CASA / Trích nợ Partial Debit" (CASA, AZ, Partial Debit chưa giảng); symbol step 1 mã Go (có chú thích).

#### 6. Số đã tính lại / mã đã chạy

- `checks` trong YAML: 99 biểu thức (L04 18, L05 21, L06 18, L07 23, L08 19) chạy bằng eval Python có `import math`: 99/99 đúng (lần đầu chạy L07 thiếu import math trong tay chạy của tôi, đã chạy lại).
- Khối mã trên màn hình đã chạy: L04 2, L05 3, L06 4 (vòng ngưỡng + dựng vé + hàm kiểm + bốn lần gọi), L07 3, L08 3 = 15/15 cho đầu ra y hệt màn hình. Chỉ đọc, không chạy: SQL UPDATE và Go (L04), PL/SQL (L05), Go (L08).
- Số tự tính lại (phép tính tay/Python): L04 458 904, 34,54 triệu, 3,98 s, 399,98 s (6,67 phút); L05 150 tỉ, 0,5/50/5 000 s, 83 phút, 0,1/10/1 000 s, 300 000 bản ghi, 10→15→12→14→13; L06 ngưỡng 22/17/23, 1,5/150/15 000, 900/90 000/9 000 000, 3 000 000; L07 N², N·log2N (2 469; 446 180; 64 549 593), 9 000 s, 0,065 s; L08 85 triệu, 349 315, 0,03/2,8/278, 5 triệu/500 triệu/50 tỉ, 1 109 589: tất cả khớp màn hình và lời đọc.
- Lab: 5/5 tự viết, cham.sh in ĐÚNG, rc=0 (mã giải ở r2/work_ACB_L0x/mau.py trong scratchpad).
- SRT so say: 5/5 khớp từng từ (srtcheck.py: ratio 1.0, 0 chênh).
- spec_sha256 build_report.json = spec_digest bỏ asr_reviewed: 5/5 khớp.

#### 7. Khung hình đã xem

- L04: 00000 (hook), 00020 (kiến trúc 4 tầng), 00050 (mã sqlite), 00070 (quymo), 00078 (quiz), 00094 (tổng kết). Không lỗi hiển thị.
- L05: 00000, 00028 (kiến trúc), 00052 (Bước 4: LỖI công thức "imes"), 00065 (mã khoá có thứ tự), 00088 (quymo), 00114 (tổng kết).
- L06: 00000 (văn bản pháp lý: hiển thị QĐ 2345 rõ "chưa đọc nguyên văn"), 00025, 00055, 00080, 00100. Không lỗi hiển thị.
- L07: 00020 (bảng VA tĩnh/động), 00048 (ví dụ con trỏ), 00062 (mã hai con trỏ), 00082 (quymo; dấu hai chấm mồ côi cuối dòng tiêu đề, nhỏ), 00092 (quiz). Không lỗi nặng.
- L08: 00005 (bảng sản phẩm + cảnh báo T24/OCB), 00022 (kiến trúc: chữ hộp 4 chạm viền), 00036 (công thức), 00070 (quymo), 00100 (tổng kết, đủ đọc).

#### Số pháp lý/lương/nguồn

- Không có số lương, phí hay tên người thật nào trong 5 bài (ngoài tên tổ chức: OCB, ACB, NAPAS, CIC, Temenos).
- Số pháp lý có trong bài: TT 50/2024/TT-NHNN, TT 77/2025/TT-NHNN (hiệu lực 01/03/2026), bản hợp nhất 25/VBHN-NHNN, QĐ 2345/QĐ-NHNN (18/12/2023, 01/07/2024), Luật 91/2025/QH15 (L06); TT 31/2024/TT-NHNN Điều 10, TT 37/2025/TT-NHNN (L08). Đều có trường `source` và khai trạng thái đọc (bản gốc/ thứ cấp / chưa đọc) cả trong lời đọc và màn hình. Tra web của tôi: TT 77/2025 ký 31/12/2025, hiệu lực 01/03/2026 (luatvietnam); TT 37/2025 sửa TT 31/2024 (vbpl.moj.gov.vn); nhóm 1 là quá hạn dưới 10 ngày, nhóm 2 đến 90 ngày (LawNet): khớp bài. Mâu thuẫn: nguồn gắn ngưỡng 10/20 triệu vào QĐ 2345 và một nguồn gắn vào Phụ lục 02 TT 50 (xem SHOULD L06).
- Số minh hoạ (lãi suất 6,8%, 7%, 0,1%, LTV 85%/80%/90%, biên độ 2,5%/2,7%, hạn vé 180 s, ngưỡng khớp 0,85, tỉ lệ gửi lại 0,1%, thời gian ms): tất cả được gắn "số minh hoạ/giả định" trên màn hình hoặc lời đọc. Không phát hiện số thực tế không nguồn.

#### Trích QĐ 2345 / sinh trắc học (để đối chiếu INT/ACB)

ACB chỉ nhắc QĐ 2345 trong L06 (L04, L05, L07, L08 không nhắc; L08 chỉ có "người ký xác nhận bằng sinh trắc học hoặc OTP theo chính sách ngân hàng", không số hiệu). Nguyên văn L06:
- source: "Quyết định 2345/QĐ-NHNN (theo tài liệu phỏng vấn đã lưu: ngày 18/12/2023, hiệu lực 01/07/2024; CHƯA đối chiếu bản gốc, chưa rõ quan hệ với Thông tư 50/2024, bài không khẳng định số điều)".
- objective 1 (và curriculum/acb.yaml dòng 115): "Nêu quy tắc ngưỡng sinh trắc học: trên 10 triệu một lần hoặc tổng ngày vượt 20 triệu, theo Thông tư 50/2024 đã sửa đổi; Quyết định 2345 chưa đọc nguyên văn".
- hook step 0 SHOW: "Quyết định 2345/QĐ-NHNN (theo bài phỏng vấn đã lưu: ngày 18/12/2023, hiệu lực 01/07/2024) — chưa đọc nguyên văn, chưa rõ còn áp dụng hay đã được Thông tư thay." và "Bài chỉ dùng ngưỡng ghi ở Thông tư 50/2024 đã sửa đổi: giao dịch trên 10 triệu đồng một lần, hoặc tổng trong ngày vượt 20 triệu đồng, phải xác thực sinh trắc học khớp dữ liệu đã đối chiếu chip căn cước (hoặc VNeID). Bài không nêu số điều, số khoản; khi làm việc thật hãy mở văn bản hiện hành."
- hook step 0 SAY: "Quyết định 2345 cũng được nhắc tới, nhưng bài này chưa đọc được nguyên văn, nên không khẳng định số điều."
- recap SAY: "nói rõ văn bản nào đã đọc nguyên văn, văn bản nào chưa."
- ACB L06 cũng có hai check tầm thường `'2345 - 2000 == 345'` (quiz).
Điểm người điều phối cần đối chiếu với INT: INT phải dùng cùng cách gắn ngưỡng (TT 50/2024 sửa đổi, QĐ 2345 chưa đọc, ngày 18/12/2023 và 01/07/2024 theo tài liệu lưu) và cùng điều kiện; nếu INT nêu ngưỡng hoặc "hiệu lực" của QĐ 2345 chắc chắn hơn ACB, đó là lệch.

#### 8. Nhận xét chung

- 5 bài sạch về kiến thức: MUST 0; số liệu, mã, lab chạy đúng; video dựng đúng spec hiện hành, SRT trùng lời đọc.
- Điểm yếu nhất còn lại là hiển thị (L05 công thức "imes"; L08 hộp kiến trúc) và pháp lý L06 (ngưỡng 10/20 gắn Phụ lục 01 chưa kiểm sau sửa đổi 77/2025; quy tắc "tổng về 0 sau quét" là giả định).
- Cấu trúc đều nhau (hook, prereq, kiến trúc, mã, tình huống, pitfall, quymo ×1/×100/×10 000 kèm "theo thời gian", quiz, lab) giúp P8 và P9 đạt 5/5.
- P1 là điểm hụt: L04, L06, L07, L08 dùng 3–5 thuật ngữ nền (HTTP/header, băm, CASA, Redis cú pháp) không giảng tại chỗ; chỉ L05 giảng đủ.
- Quiz có phương án nhiễu quá lộ (đúng là phương án dài nhất, ba cái kia vô lý): đo nhớ hơn đo hiểu.
