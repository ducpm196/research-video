# S01 BNX L24–L30: đã đọc 7/7 bài

Người đọc độc lập; người học giả định: đã học FND, JVA, JV2, PYT, BNK, BNX L00–L23 nhưng mỗi bài phải tự đứng được. Tiêu chí: `sample_f/BRIEF.md` + `ADDENDUM.md` (P1–P9). Ngưỡng: MUST 0; P1=2 ≥ 90%; P8=2 100%.

**Kết quả so với ngưỡng: MUST = 2 (KHÔNG đạt); P1=2 ở 0/7 bài (KHÔNG đạt); P8=2 ở 7/7 (đạt, có lưu ý về "thực nghiệm"); P9=2 ở 7/7.** Mọi bài ≤ 16 phút (lớn nhất L30 = 15,3 phút). Cả 7 `spec_sha256` trong `build_report.json` khớp spec_digest tính lại từ YAML hiện tại (khớp 7/7); sha256 16 ký tự của YAML nằm ở bảng 3.

## 1. Chuẩn xác — MUST (2)
| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L26 | MUST | `formula` step 2; `sym` bảng; `example` step 3 ($$② 6 pha chạy theo đúng thứ tự$$); curriculum "mvn package chạy 6 pha" | "Gọi `package` thì chạy mọi pha trước nó: … 6 pha khi gọi package"; `resources → compile → testResources → testCompile → test → jar` | Đây là 6 MỤC TIÊU (goal) của plugin được gắn vào vòng đời, không phải 6 pha. Chạy `mvn -o -B package | grep -- '--- ' | cut -c8-` (Maven 3.9.11, JDK 21): in `resources:3.3.1:resources`, `compiler:3.13.0:compile` … `jar:3.4.1:jar` = các dòng plugin:goal. Vòng đời mặc định của Maven có nhiều pha hơn (process-resources, compile, process-test-resources, test-compile, test, package…; tài liệu Maven "Introduction to the Build Lifecycle"). Lời đọc ở `example` nói đúng "sáu mục tiêu" nhưng `formula` và `sym` gọi là "pha" ⇒ màn hình ≠ lời đọc và sai thuật ngữ người học mang đi phỏng vấn | Gọi là "6 mục tiêu plugin, gắn vào các pha process-resources…package" | CONFIRMED (chạy Maven) + tài liệu Maven (kiến thức, không fetch) |
| L28 | MUST (giáo án hứa điều bài không dạy) | `example` step 5 ("Kết quả chạy thật"); curriculum L28 `example` + objective 2 | màn hình: "MySQL 8.4 / phien ban: 8.4.13" rồi "$$④ … MySQL: mã lỗi riêng$$"; hook: "MySQL báo một mã lỗi riêng"; curriculum: "MySQL báo ERROR 3572" | Objective 2 "So sánh lỗi khi xin khoá dòng không chờ ở PostgreSQL, MySQL, Oracle và SQL Server" và ví dụ giáo án nêu mã 3572, nhưng video (màn hình + lời đọc + SRT) KHÔNG hiện mã/thông báo MySQL nào; chỉ có số phiên bản. Bằng chứng chạy thật có tồn tại (cache chương trình `audit/bnx/progcache/L28.json`, mục ChayMy: "ERROR 3572 (HY000) … NOWAIT is set") nhưng không lên màn hình. Người học không thể so được 4 hệ; khung 00059 và 00047 đã xem xác nhận | Thêm dòng "ERROR 3572 (HY000)…" vào kết quả step 5 và đọc ra | CONFIRMED (khung L28/00047, 00059; cache) |

## 1b. Chuẩn xác — SHOULD (theo bài; mỗi mục: tệp/bước + bằng chứng)
| Bài | Cảnh/step | Trích | Vấn đề + bằng chứng đã chạy/đọc | Tin cậy |
|---|---|---|---|---|
| L24 | `formula` step 4, `quymo`, quiz 1 | "số dòng = số khách × số tài khoản mỗi khách"; "nối kèm tải … một câu" | `join fetch` là nối trong: khách không có tài khoản biến mất. Chạy Hibernate 7.1.0.Final + H2: thêm 1 khách không có tài khoản, `select k from Khach k join fetch k.tk` trả 500 khách trên 501 (thiếu điều kiện áp dụng; chưa nói `left join fetch`) | CONFIRMED |
| L24 | `pitfalls` Lỗi 2 | "làm cạn bể kết nối" | "bể kết nối" chưa được giảng ở L24 (prereq không có) | CONFIRMED |
| L25 | `hook` | "cùng một lỗi lại cho ba kết quả khác nhau" | Ca thứ ba ném loại lỗi khác (lỗi kiểm tra) nên không phải "cùng một lỗi" | CONFIRMED (đọc) |
| L25 | `pitfalls` Lỗi 4 | "Nuốt ngoại lệ ở hàm trong rồi không báo ra ngoài (catch rỗng)" | Nếu chính hàm trong bắt lỗi của nó thì proxy không thấy lỗi ⇒ không đánh dấu rollback-only. `UnexpectedRollbackException` chỉ xảy ra khi hàm NGOÀI bắt lỗi do hàm trong (qua proxy) ném. Chạy Spring 7.0.10: hàm ngoài `catch (RuntimeException)` lệnh gọi hàm trong `@Transactional` ném lỗi ⇒ ném `UnexpectedRollbackException`. Trích Spring docs (Transaction Propagation): "an inner transaction scope sets the rollback-only marker, the outer transaction has not decided…" | CONFIRMED |
| L25 | `check` + `formula` step 6 | "REPEATABLE_READ: 1000 → 1000" | Chạy H2 2.3.232: READ_COMMITTED 1000→1050; REPEATABLE_READ và SERIALIZABLE 1000→1000 (khớp). Nhưng đây là hành vi của H2: ở SQL Server REPEATABLE_READ giao dịch B sẽ bị chặn; Oracle không có REPEATABLE_READ. Bài không nêu "kết quả theo H2" | PLAUSIBLE (tài liệu từng hệ không fetch) |
| L25 | toàn bài | "luồng", "JDBC", "nguyên tử", "hàng đợi" | "luồng" (thread) là khái niệm then chốt của cảnh bể kết nối nhưng không giảng; JDBC xuất hiện ở tiêu đề cảnh `check` không giải thích | CONFIRMED |
| L26 | `formula` step 5 (Jenkinsfile) | `pipeline { agent any stages { … Deploy …` | Đoạn trích KHÔNG có khối `post { failure { … } }` dù objective 4 và hình nói về nhánh post; `agent any`, `sh` không được giải thích | CONFIRMED |
| L26 | `example` step 6–7 | màn hình: "Kết quả chạy thật" trên kết quả mô phỏng Python | Tiêu đề ngay trên "Build: xong / Test: that bai / post failure…" là "Kết quả chạy thật" trong khi cảnh trước ghi "MÔ PHỎNG bằng Python (không phải Jenkins)" và lời đọc nói "Kết quả mô phỏng" (nhãn trên màn hình lệch lời đọc) | CONFIRMED |
| L26 | `example` step 2 (khung 00038) | "bnx:l26:jar:1 / +- …commons-text… / \- …commons-lang3:jar:3.9:compile / \|  \- (…3.12.0 … omitted for conflict with 3.9)" | Màn hình ghép 2 lệnh (`dependency:tree` thường + `grep omitted` của bản verbose) thành một "cây" với nhãn "Kết quả chạy thật": dòng bị bỏ trông như con của lang3 3.9. Chạy `mvn -o -B -q dependency:tree -Dverbose`: dòng omitted nằm DƯỚI commons-text (`+- commons-text` rồi `\|  \- (…3.12.0 - omitted …)`), lang3 3.9 là nhánh riêng. Người học đọc cây sẽ hiểu sai quan hệ bắc cầu | CONFIRMED |
| L26 | `hook` | "Vì sao máy bạn chạy được mà máy chủ dựng thì không?" | Không có cảnh nào trả lời trực tiếp câu hỏi mở bài | CONFIRMED (đọc) |
| L27 | `formula` step 3 | "đó là cách ta tự cài chứ không phải đặc tả quy định" (về 500/400) | Phong bì dùng không gian tên SOAP 1.1 (`schemas.xmlsoap.org/soap/envelope/`, `faultcode soapenv:Client`); theo W3C Note SOAP 1.1 §6.2 phản hồi lỗi SOAP PHẢI dùng HTTP 500. Chưa kiểm được nguyên văn (w3.org trả 403 khi fetch) | PLAUSIBLE |
| L27 | `formula` step 2 (WSDL) | "bank.wsdl (trích)" rồi kết quả "2 message 1 portType …" | Đoạn trích trên màn hình chỉ có 1 `message` (LaySoDuOut) nên người học không đếm ra 2 từ màn hình | CONFIRMED |
| L27 | tiêu đề, `intuition` 2 | "SOAP/WSDL và SFTP"; "Kênh mã hoá (SFTP) lo bí mật đường truyền" | SOAP, SFTP không được khai triển/giảng (SFTP chỉ xuất hiện trong SVG; lời đọc không bao giờ nói "SFTP"); toàn bộ phần SFTP là thư mục cục bộ (có nhãn MÔ PHỎNG nhưng chữ nhỏ). Tên bài hứa nhiều hơn dạy | CONFIRMED (đọc + khung 00019) |
| L27 | `intuition` 1, recap, pitfalls Lỗi 1 | "mỗi lời gọi nặng gấp hơn mười lần (đo thật)"; "tệp … tự chứng minh được là đủ và đúng" | Tỉ lệ 12,3× (246/20) là của tải nhỏ vì chi phí cố định (đã chạy lại: 246/20=12,3; 211/16=13,19); khi dữ liệu lớn tỉ lệ giảm. Mã băm nằm CÙNG tệp chỉ bắt hỏng/thiếu ngẫu nhiên, không chứng minh nguồn (kẻ sửa tệp tính lại băm được); bài không nêu điều kiện | CONFIRMED (suy luận) |
| L28 | `hook`, recap, pitfalls Lỗi 3 | "MongoDB không khoá dòng như vậy mà dùng cập nhật có điều kiện" | Gợi ý đây là khác biệt giữa hai loại hệ; thực tế `UPDATE tk SET so_du=so_du-600 WHERE id=1 AND so_du>=600` cũng nguyên tử ở hệ quan hệ và là cách phổ biến; bài không nói | PLAUSIBLE |
| L28 | `check` + pitfalls Lỗi 3 | "Chạy thật, hai lần rút 600 từ 1000 chi ra 1200 mà chỉ trừ 600" | Là mô phỏng Python hai biến gán tay (`doc_a = doc_b = 1000`), không phải tranh chấp thật trên cơ sở dữ liệu; màn hình (khung 00053) không có nhãn "mô phỏng" (lời đọc chỉ nói "một từ điển") | CONFIRMED |
| L28 | `example` step 4–5 | "Oracle: ORA-00054: Failed to acquire a lock" | Mã ORA-00054 đúng; lời văn khác thông báo trong tài liệu Oracle ("resource busy and acquire with NOWAIT specified or timeout expired"). Cache chương trình cho thấy chuỗi này do chương trình thật in ra (không bịa) | PLAUSIBLE |
| L29 | `quymo` step 2 (khung 00059) | "1000 su kien: … so du -15" | Số dư âm không giải thích; đoạn sinh dữ liệu (`(i % 2, i % 97 + 1)`) không lên màn hình nên người học không tái hiện được (tôi chạy lại với nguồn: -15 và 35 khớp) | CONFIRMED |
| L29 | `formula` step 1, pitfalls Lỗi 1, `example` 1 | "nên chương trình lỗi cũng không sửa được lịch sử" | Chạy sqlite: `DROP TRIGGER khong_sua` rồi `UPDATE su_kien SET tien=900 WHERE seq=2` thành công (tien seq2=900). Bài không nói giới hạn: người có quyền DDL/quản trị vẫn gỡ được; cần quyền tối thiểu/chữ ký chuỗi băm. Cũng không dạy kiểm soát đồng thời khi ghi (phiên bản kỳ vọng) | CONFIRMED |
| L29 | toàn bài | "CQRS và Event Sourcing" | Hai thuật ngữ nằm ở tiêu đề và bảng CV cuối, không được khai triển/định nghĩa trong thân bài | CONFIRMED |
| L30 | `check` (khung 00054, 00058) | "cửa sổ bốn cuộc, ngưỡng năm mươi phần trăm hỏng, chờ một giây" | Chạy Resilience4j 2.3.0 (sha256 khớp README) với `slidingWindowSize(4)`, `minimumNumberOfCalls(4)`, `failureRateThreshold(50)`, `waitDuration 1s`: mặc định sau 1 cuộc tốt vẫn `HALF_OPEN`; chỉ về `CLOSED` khi thêm `permittedNumberOfCallsInHalfOpenState(1)`. Màn hình/lời đọc không nêu thông số này ⇒ kết quả "HALF_OPEN to CLOSED" không tái hiện được từ nội dung hiển thị | CONFIRMED |
| L30 | `check` | "hai bản không mở cùng lúc… Ba trạng thái … giống nhau, nên ta tin vào mô hình" | Bảng ngay đó cho thấy 3 so với 4 cuộc hỏng; kết luận "mô hình đúng" hơi mạnh (chỉ khớp ở cấu hình đã chọn) | PLAUSIBLE |
| L30 | `prereq`, `formula` step 3, quiz 1 | "gọi lại tối đa 4 lần"; "mỗi yêu cầu thành 1 + r cuộc gọi (r là số lần thử lại)"; quiz "Thử lại tối đa 5 lần … Hỏng cả 5 lần: … 750" | Hai nghĩa lẫn lộn: r = số lần thử LẠI (1+r cuộc), còn quiz/`ThuLai.java` dùng `toiDa` = tổng số lần gọi. Theo định nghĩa r, "thử lại 5 lần" là 6 cuộc, tổng chờ 50+100+200+400+800=1550 không phải 750 | CONFIRMED (đọc) |
| L30 | quiz câu 3 | "cầu dao + vách ngăn 50 chỗ + hạn chót 2 giây … một phần yêu cầu bị từ chối" | Đề: dịch vụ hay chậm 3–4 giây, 500 yêu cầu/giây. 50 chỗ ÷ 2 s ≤ 25 yêu cầu/giây ⇒ ~95% bị từ chối và mọi cuộc 3–4 s đều quá hạn. Đáp án "một phần" và "hợp lý nhất" che đi con số. Dòng "10 giây → 5 000 luồng" cũng giả định cuộc gọi treo hết hạn (nếu chỉ chậm 3,5 s thì ≈ 1 750) | CONFIRMED (tính) |
| L30 | `formula` step 6, `example` | CanBang.java (trích) | Đoạn trích dừng trước vòng lặp, thời điểm đến của 8 yêu cầu không hiện ⇒ không tái hiện được "máy 1 = 2, máy 2 = 1" | CONFIRMED |
| Lab | `labs/BNX/L29/de.md` | "Giả sử sự kiện `RUT 300` bị ghi nhầm. Không sửa kho: … (Thêm cả `RUT 300` rồi `NAP 300` vào cuối kho…)" | Kho 6 sự kiện không có `RUT 300`; ngoặc đơn tự thêm cả hai nên số dư cuối 500 = trước khi bù, và "không sửa kho" mâu thuẫn "thêm vào kho". `loi_giai.py` và `mong_doi.txt` khớp ngoặc đơn (cham.sh ĐÚNG) | CONFIRMED |

Không báo lỗi: số liệu L24–L30 (xem mục 6); sản phẩm/phiên bản: Hibernate 7.1.0.Final, Spring 7.0.10, AspectJ 1.9.24, H2 2.3.232, Maven 3.9.11, Resilience4j 2.3.0 tồn tại (jar có trong `audit/bnx/deps`, sha256 khớp README với các jar đã kiểm); "PostgreSQL 17.12", "MongoDB 8.3.17", "MySQL 8.4.13" và ảnh Oracle/SQL Server: không kiểm được (cấm docker; chỉ thấy cache đầu ra thật của MySQL/Oracle/SQL Server) ⇒ PLAUSIBLE (riêng "MongoDB 8.3.17" tôi không biết dòng phát hành này). `Msg 1222` cho NOWAIT ở SQL Server, ORA-00054, MySQL 3572, `could not obtain lock on row` của PostgreSQL: đúng mã theo hiểu biết của tôi (PLAUSIBLE, không fetch tài liệu). Spring docs (đã fetch): "exceeding the number of concurrent threads by at least 1" và UnexpectedRollbackException đúng như bài nêu.

## 3. Bảng độ sâu
(P1–P7 chấm 0/1/2; "Cần biết trước" = thuật ngữ/kỹ năng bài DÙNG mà không giảng tại chỗ)
| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L24 | fd18afcee348bb32 | 14,2 | 1 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 12 | ĐỦ | bể kết nối, ngoại lệ, phân trang, H2 | `join fetch` nối trong làm mất khách không có tài khoản (đã chạy); bể kết nối chưa giảng |
| L25 | dca912fd12670b79 | 14,0 | 0 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 11 | GẦN (có mục 0) | luồng (thread), JDBC, nguyên tử, hàng đợi, hết giờ | "luồng" then chốt chưa giảng; kết quả cô lập chỉ của H2; Lỗi 4 mơ hồ |
| L26 | ebac24d318aab80c | 14,5 | 1 | 1 | 1 | 2 | 2 | 1 | 1 | 2 | 2 | 10 | GẦN | Gradle là gì, mã băm/sha256, máy dựng, `agent any`/`sh`, Groovy | "6 pha" sai (MUST); cây ghép sai; thiếu khối `post`; hook không được trả lời |
| L27 | 35af19613f71ca59 | 14,5 | 0 | 2 | 1 | 2 | 2 | 1 | 1 | 2 | 2 | 9 | GẦN (có mục 0) | SOAP, SFTP, HTTP POST, CSV, XXE, KiB | SFTP/SOAP không được định nghĩa, SFTP chỉ là thư mục cục bộ; trích WSDL không đếm được; "không phải đặc tả" chưa chắc |
| L28 | 2d13590054548ddf | 14,5 | 1 | 2 | 1 | 2 | 2 | 1 | 1 | 2 | 2 | 10 | GẦN | Docker, EXPLAIN, MVCC, `$gte` (có giảng), mongosh | MySQL không hiện kết quả (MUST); "đọc rồi ghi" là mô phỏng không gắn nhãn; chưa nói UPDATE có điều kiện cũng dùng được ở hệ quan hệ |
| L29 | 06a96f83099ffe46 | 14,6 | 1 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 12 | ĐỦ | CQRS, Event Sourcing (chưa khai triển), sqlite | -15 không giải thích, trigger không phải bất khả xâm phạm, thiếu kiểm soát đồng thời khi ghi |
| L30 | 16bc53f57bac4807 | 15,3 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | luồng, cổng API, cân bằng tải, luỹ đẳng, burst | R4j thiếu thông số nửa mở; quiz 3 che số 95% từ chối; "thử lại tối đa" mơ hồ |

P1=2: 0/7 bài (0%). P8=2: 7/7 (nhưng xem lưu ý mục 4). P9=2: 7/7 (mỗi bài đều có cảnh `quymo` ≥ 2 mức quy mô + bảng đánh đổi; một số dòng ghi rõ "suy ra", không đo).

Lưu ý lời đọc ≤ 16 phút: SRT cuối 14:14 / 14:02 / 14:32 / 14:27 / 14:27 / 14:34 / 15:19 (L24→L30); `timeline_seconds` 854,5 / 842,7 / 872,6 / 868,3 / 868,0 / 875,2 / 920,2 — đều dưới 16 phút (L30 sát nhất, 15,3).

Giáo án ↔ video (P7, E51): 7/7 mục tiêu có cảnh "covers"; lệch: L26 mục tiêu 1 "các pha" (nhãn sai), mục tiêu 4 "nhánh post" (đoạn mã không có post); L27 mục tiêu 4 "đếm" (WSDL trích 1 message); L28 mục tiêu 2 (thiếu MySQL, MUST); L30 mục tiêu 3 "So sánh … với Resilience4j thật" (thông số không hiển thị đủ). Ngoài ra "L27 title SFTP".

## 4. Lab (làm như người học, không xem loi_giai trước; một tác tử riêng làm, tôi đã đọc báo cáo và kiểm tên tệp)
| Bài | Tự làm được | Thời gian (ước phút / giây thực) | Kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L24 | Có | ~5 / 23 | đề không cho cột bảng `the`; không nói lúc đăng ký `set_trace_callback` (phải sau khi nạp dữ liệu) | Khớp: `Cach 1: 13 cau, tong so the 36` / `Cach 2: 1 cau, tong so the 36` |
| L25 | Có | ~4 / 23 | không kẹt | Khớp (5 dòng) |
| L26 | Có | ~5 / 20 | không kẹt | Khớp (maven A/B/X/Y/Z, gradle X/Y/Z) |
| L27 | Có | ~6 / 25 | không nói hex thường/hoa và mã hoá khi băm (đoán đúng) | Khớp (OK / THIEU DONG / SAI MA BAM ×2) |
| L28 | Có | ~4 / 25 | "`<ba số>`" không nói cách nhau bằng gì (đoán dấu cách) | Khớp |
| L29 | Có | ~5 / 34 | mục 3 của đề mâu thuẫn (xem 1b) | Khớp (500 (6) / 550 / 500 (2) / 500) |
| L30 | Có | ~7 / 41 | hiểu "đủ 600 ms" là `>=` | Khớp (9 gọi thật, 2 bị chặn) |
`cham.sh` chạy được trên máy này (Git Bash + Python 3.11); cả 7 bài tự làm qua cổng ngay lần đầu và `loi_giai.py` chính thức cũng ĐÚNG 7/7. Tôi tự chạy lại logic ở L26–L30 (xem mục 6) cho đầu ra giống mong_doi.
Lưu ý P8 (không tính vào ngưỡng): chỉ L24 dùng thư viện thật (sqlite3 + `set_trace_callback`) và L27 dùng `hashlib` thật; L25 (bảng tra tên ngoại lệ), L26 (từ điển), L28 (dict + hai biến), L29 (mảng), L30 (lớp tự viết) là mô phỏng — không lab nào chạy Spring/Maven/MongoDB/Resilience4j/SFTP dù `audit/bnx/deps/l24,l25,l26,l30` đã có jar. Cổng chỉ so đầu ra, lời giải hard-code vẫn qua. Đề L25 chữ ký `hoan_tac(loi, rollback_for)` không được chấm.

## 5. Người học kẹt ở đâu
- L24: Lỗi 2 ở `pitfalls` — "làm cạn bể kết nối" (bể kết nối chưa giảng); phần còn lại theo được.
- L25: `intuition` hình 2 / `quymo` — "3 luồng, bể 3" (luồng chưa giảng; JDBC ở cảnh `check`).
- L26: `formula` step 2 — "6 pha": đối chiếu với dòng `--- compiler:3.13.0:compile` thấy khác; và `example` kết quả cây — dòng "omitted" trông là con của lang3 3.9.
- L27: tiêu đề + `prereq` — SOAP/SFTP chưa được định nghĩa; `formula` step 2 — không đếm được "2 message" từ đoạn trích.
- L28: `example` step 5 — "MySQL: mã lỗi riêng" mà không thấy mã; `hook` "năm hệ" nhưng chỉ có mã Oracle trên màn hình 00047.
- L29: tiêu đề — CQRS/Event Sourcing không khai triển; `quymo` — "so du -15" không giải thích.
- L30: `check` — "HALF_OPEN to CLOSED sau 1 cuộc tốt" khó tái hiện (thiếu thông số); quiz 1 — "thử lại tối đa 5 lần" (5 lần gọi hay 5 lần thử lại).

## 6. Số đã tính lại / mã đã chạy
Chạy lại từ mã trên màn hình hoặc dựng lại đúng mô tả (Java 21 Temurin 21.0.13; jar ở `audit/bnx/deps`, sha256 kiểm cho hibernate-core, h2, resilience4j-circuitbreaker, spring-tx, aspectjweaver — khớp README); khoảng 90 giá trị/dòng, tất cả khớp con số trên màn hình:
- L24: Hibernate 7.1.0.Final + H2 2.3.232 — 6/51/501 vs 1; 2 lần find = cùng đối tượng, 1 câu; sửa + truy vấn = 1 UPDATE trước chốt; detach rồi sửa = 0 UPDATE, 1500/2000; sửa rồi detach trước flush = 0 UPDATE; 1500 đối tượng, sau clear 0; LazyInitializationException (11/11 khớp); sqlite trace = 51 câu. Bổ sung ngoài bài: join fetch mất khách không có tài khoản (500/501).
- L25: Spring 7.0.10 + AspectJ 1.9.24 — proxy true; 4 ca (1000/0, 1000/1, 900/0, 1000/0); proxy true / nội bộ false; đoạn cắt 1 lần; cô lập H2 1050/1000/1000; bể 3/3→3, 3/4→0, 6/6→6, 6/7→0 (14/14 khớp); thêm: hàm ngoài nuốt lỗi → UnexpectedRollbackException.
- L26: Maven 3.9.11 (offline) — tree verbose, 6 dòng plugin:goal (khớp tên/phiên bản 3.3.1/3.13.0/3.2.5/3.4.1), dựng 2 lần: không outputTimestamp KHAC, có GIONG; bộ phân giải tự viết, mô phỏng Jenkins; số máy 1/67/6667, 30/10 (khớp). Không dựng lại được số gói 1/9/34 (thiếu phụ thuộc offline) — CHƯA KIỂM; Gradle/Jenkins không chạy (bài cũng nói vậy).
- L27: băm theo khối: 24000 B/1 khối/`796b27ae9211` và 24 000 000 B/367 khối/`0ddfcd0e4e82` (trùng cả mã băm 12 ký tự); `kiem` 3 ca; 246/20=12,3; 211/16=13,19; 2e6×40=8e7 → 1221 khối; 24e9 → 366 211; DOCTYPE mặc định đọc được tệp ("BI-MAT-123") còn `disallow-doctype-decl` → SAXParseException. Không chạy SoapDemo (nguồn không đủ trên màn hình): 200/500/400 và 246/211 byte CHƯA KIỂM.
- L28: Python 2 dòng khớp; PostgreSQL/Mongo/MySQL/Oracle/SQL Server không chạy (cấm docker); quy tắc n−1 và các số 250 000/2 500 000 (249 999/2 499 999), 900→500→100→từ chối đã tính tay khớp; đầu ra MySQL/Oracle/SQL Server thấy trong cache chương trình.
- L29: trigger chặn UPDATE/DELETE, 3 sự kiện; 1000/700/750/630; sai 130, bù 580/7 sự kiện; −15 và 35 (với nguồn sinh dữ liệu); 2500%1000=500, 2500500%1000=500, 7 300 000%5000=0; quiz 600/735 (khớp).
- L30: tự cài: 7 gọi thật/2 chặn; 12 cuộc ở 100 và 10 000 yêu cầu (so với 400/40 000); luyện tập 9/2 từng dòng khớp mong_doi; xô token [5,2], [4,2]; 750; Resilience4j 2.3.0: CLOSED→OPEN sau 4 hỏng, chặn 2, OPEN→HALF_OPEN→CLOSED (cần `permittedNumberOfCallsInHalfOpenState(1)`).
Khác biệt tìm được: không có số tính sai; chỉ có khác biệt hiển thị (cây L26) và cấu hình R4j (L30).

## 7. Khung hình đã xem (≥ 5/bài) và lỗi hiển thị
Tôi xem trực tiếp L24 (00015, 00044, 00057, 00078, 00097) và L26/00038; hai tác tử đọc độc lập xem phần còn lại rồi tôi kiểm lại từng nhận xét với YAML/chạy mã. Đã xem: L24 00015/00044/00057/00078/00097; L25 00001/00018/00046/00059/00073/00101; L26 00020/00038/00042/00046/00058/00086; L27 00019/00031/00043/00057/00076; L28 00001/00034/00047/00053/00059; L29 00020/00045/00059/00081/00100; L30 00035/00054/00058/00086/00094. Không có chữ tràn/đè/cắt nặng ở khung nào. Lỗi hiển thị/khớp lời:
- L26/00038: cây ghép (đã nêu); L26/00020: mũi tên "hỏng" không chạm ô `post failure`, tiêu đề "cây phụ thuộc và đường ống dựng" nhưng chỉ có đường ống; L26/00042: tiêu đề "Chạy thật" chỉ hiện mã, kết quả GIONG/KHAC ở khung sau; L26/00086: chữ xám trên nền cam, nhắc `de.md`.
- Nhãn mô phỏng: L26/00020 và L27/00019 CÓ nhãn "MÔ PHỎNG" nhưng chữ nhỏ, xám (~22 px). L28/00053 (mô hình Python dict) và L30/00094 (đồng hồ giả: chỉ có chữ "đồng hồ giả" trong đề) không có nhãn mô phỏng; L25/00018 sơ đồ không ghi "thật/mô phỏng" (chỉ có dòng xám "đo thật ở phần ví dụ").
- Chữ trên màn hình thiếu so với lời đọc: L29/00081 (đề 800,150,90,40 không hiện lúc đọc đáp án), L30/00086 ("chín yêu cầu", tốc độ nạp), L30/00054 ("sáu cuộc hỏng", "một giây mười"), L27/00057 (mã băm cắt 12 ký tự không ghi chú; lời "65 536 byte" vs màn hình "64 KiB").
- L29/00100: mũi tên "→" lẻ cuối dòng; L30/00058: cột 3 trộn tiếng Anh OPEN/HALF_OPEN/CLOSED; nhiều khung để trống > nửa màn hình dưới; hộp cam sát mép trái (L28/00053, L29/00081, L30/00086, L30/00094); L24/00015 nhãn "UPDATE khi chốt" chạm viền ô "bảng trong cơ sở dữ liệu" (nhỏ).

## 8. Nhận xét chung
- Kỹ thuật chạy thật mạnh: Hibernate, Spring, Maven, Resilience4j đều tái hiện đúng mọi con số; không có số tính sai ở 7 bài; spec_sha256 khớp 7/7.
- Điểm yếu lặp lại: P1 — mỗi bài đều có thuật ngữ then chốt không giảng tại chỗ (luồng, SOAP/SFTP, CQRS/Event Sourcing, bể kết nối…); 0/7 bài đạt P1=2, nên ngưỡng P1 ≥ 90% chưa đạt.
- MUST còn lại: L26 (pha vs mục tiêu) và L28 (MySQL có chạy thật nhưng không hiện trong video).
- Lệch giữa cái "chạy thật" và cái lên màn hình: cây L26 ghép hai lệnh, thông số R4j và nguồn sinh dữ liệu L29 bị lược; nên in đủ lệnh + kết quả nguyên văn.
- Nhãn mô phỏng: có ở L26 (Jenkins) và L27 (SFTP) nhưng chữ nhỏ; thiếu ở L28 (đọc rồi ghi) và L30 (đồng hồ giả); L26 gán "Kết quả chạy thật" cho kết quả mô phỏng.
- Quy mô/thời gian (P9) làm tốt ở cả 7 bài (bảng quy mô + đánh đổi), nhưng đáp án quyết định L30 câu 3 chưa tính số (≈ 95% từ chối).
- Lab: cả 7 qua cổng dễ nhưng đều ở mức mô phỏng/viết lại quy tắc; L29 đề tự mâu thuẫn; thiếu một bài tập chạy thư viện thật dù jar đã có.
- Giới hạn bài viết của tôi: Docker (L28), SoapDemo (L27 200/500/400) và số gói 1/9/34 (L26) CHƯA KIỂM; sản phẩm 'PostgreSQL 17.12', 'MongoDB 8.3.17' PLAUSIBLE.
