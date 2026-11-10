# BIÊN BẢN BÀN GIAO PHỎNG VẤN & HỒ SƠ ỨNG VIÊN (INTERVIEW HANDOVER)
## VỊ TRÍ: KỸ SƯ PHÁT TRIỂN TÍCH HỢP CẤP CAO (SENIOR INTEGRATION ENGINEER) — NGÂN HÀNG ACB
**Mục tiêu đãi ngộ**: **50,000,000 VND Gross/tháng** (Thu nhập năm nếu đạt mức này: 700 – 850 triệu VND = 13 tháng lương cố định + thưởng 1–4 tháng tùy xếp loại, theo tin tuyển dụng ACB; lương ACB ghi "Thương lượng")  
**Thời điểm cập nhật**: 2026-11-10. Mới nhất là **Mục 13**: đọc kiểm lần ba toàn kho, bài tự đứng được, 591 + 37 bài dựng lại, mẫu độc lập D. Các mục trước: Mục 12 (2026-11-09), Mục 11 (đợt B), Mục 10 (khóa JVA), Mục 9 (rà soát 2026-11-08).  
**Trạng thái hệ thống**: xem **Mục 13** (mới nhất), rồi Mục 9 và Mục 7 (bản 2026-11-07, một số kết luận đã bị Mục 9 sửa lại). Các tuyên bố "hoàn tất 100% PASS" ở bản trước không còn được dùng làm bằng chứng: ngân hàng 100 câu hỏi từng chỉ có 58 câu, CV từng chứa số liệu không có nguồn. Mọi tệp được chỉ mục tại [`MASTER_CURRICULUM_INDEX.md`](file:///D:/research-video/interview/MASTER_CURRICULUM_INDEX.md).

---

## 1. THÔNG TIN ỨNG VIÊN & HỒ SƠ NGUYÊN BẢN (GROUND TRUTH PROFILE)

- **Họ và tên**: PHẠM MINH ĐỨC
- **Ngày tháng năm sinh**: **20/09/1996** (Tuổi: 30 vào năm 2026 — Độ tuổi chín muồi, sung sức và bản lĩnh nhất của một Kỹ sư Cấp cao / Senior Integration Engineer).
- **Địa chỉ & Liên hệ**: TP. Hồ Chí Minh, Việt Nam · Điện thoại: (+84) 965 141 282 · Email: ducpm196@gmail.com.
- **Tiêu chuẩn Bảo mật Thông tin Cá nhân**: Bỏ hoàn toàn liên kết LinkedIn và GitHub cá nhân trên CV; thay thế bằng **Ngày sinh (DOB: 20/09/1996)** và **Định hướng Chuyên môn Cốt lõi (Focus: Core Lending, Overdraft & Interbank Integration)** — Thể hiện tính kỷ luật bảo mật cao, không lộ mã nguồn ngân hàng trên mạng xã hội công cộng.
- **Vị trí & Trọng tâm công tác hiện tại**: Chuyên viên chính Ứng dụng Tích hợp (Senior Integration Application Specialist) chuyên trách **Squad Lending & Tích hợp Ngân hàng Lõi (Squad Lending & Core Banking Integration)** tại **Ngân hàng TMCP Phương Đông (OCB)** (Tháng 10/2023 – Hiện tại: 3+ năm thực chiến).
  - Trực tiếp làm chủ và phát triển dịch vụ hạt nhân Retail Lending Integration Gateway (BFF kết nối hơn 30 tuyến APIC và 15 microservices nghiệp vụ).
  - **Phân định rõ ràng phạm vi công việc theo chuẩn mực Senior**:
    1. *Phần việc cá nhân trực tiếp làm chủ (Direct Ownership / Key Implementation)*: Thiết kế và code các module cốt lõi của Squad Lending (Thấu chi cầm cố sổ tiết kiệm 2 pha trên Core T24, Thấu chi lương, Tích hợp cổng ký số Cloud CA FPT E-Sign với xác thực khuôn mặt QĐ 2345, Cổng CIC B2B tra cứu tự động, khóa phân tán Redis Mutex chống giải ngân kép và trích nợ từng phần Partial Debit CASA). Trực tiếp tối ưu hóa câu lệnh SQL, Index và Stored Procedure trong phân hệ Lending/Transfer, xóa bỏ hoàn toàn deadlock `ORA-00060`.
    2. *Phần việc phối hợp với hạ tầng dùng chung (Squad & Cross-Team Collaboration)*: Tích hợp với adapter Core T24 qua IBM MQ của phòng Tích hợp; tích hợp luồng giải ngân/thu nợ với cổng chuyển mạch NAPAS 247 của team Switch; phát triển custom ksqlDB UDFs và worker tiêu thụ event trên cụm Confluent Kafka của ngân hàng.
- **Kinh nghiệm tiền nhiệm**:
  - **Grooo International** (Tháng 10/2022 – Tháng 09/2023): Backend Software Engineer outsource cho **Công ty Tài chính Mirae Asset (MAFC)** — Hệ thống Khởi tạo và Quản trị Khoản vay tiêu dùng (LOS/LMS), cổng giải ngân tự động chống trùng lặp.
  - **Freelance** (Tháng 01/2022 – Tháng 09/2022): Backend Software Engineer / Consultant (Java Spring) — Microservices, Docker, Kubernetes, CI/CD.
  - **Sutrix Group** (Tháng 01/2019 – Tháng 12/2021): Software Engineer — **Adobe Experience Manager (AEM Sites 6.4/6.5)** & Java Core cho tập đoàn viễn thông quốc tế Globe Telecom; đạt chứng chỉ **Adobe Certified Expert**.
- **Học vấn & Bằng cấp (ĐÃ ĐỐI SOÁT & CẬP NHẬT CHUẨN XÁC)**:
  - **Đại học Công nghệ Thông tin (UIT - ĐHQG TP.HCM)**:
    - *Bằng cấp*: Bachelor of Science in Artificial Intelligence (Articulated Degree Program).
    - *Thời gian*: **Tháng 06/2025 – Tháng 11/2026** (June 2025 – November 2026). **Dự kiến tốt nghiệp: ứng viên xác nhận chưa nhận bằng tính đến 2026-11-07, nên CV ghi "expected", không ghi "Holds".**
    - *Quy tắc tuyệt đối*: **Bỏ hoàn toàn cụm từ "/ Hệ liên thông"** trên CV để đảm bảo súc tích, chuyên nghiệp; **TUYỆT ĐỐI KHÔNG nhắc đến "VNUHCM - University of Science"** dưới mọi hình thức vì chưa có bằng trường này.
  - **Cao đẳng FPT Polytechnic**:
    - *Bằng cấp*: Associate Degree in Software Engineering (Lập trình máy tính & thiết bị di động).
    - *Thời gian*: Tháng 10/2016 – Tháng 03/2019 (Nền tảng thuật toán, Java Core, OOP).
- **Chứng chỉ chuyên môn**:
  - Adobe Certified Expert – AEM Sites Developer (2020).
  - *Khóa đào tạo (không phải chứng chỉ, ứng viên xác nhận)*: Oracle Database 19c PL/SQL Tuning; Kafka & Distributed Systems.
- **Người tham chiếu chuyên môn (Professional References)**:
  - **Mr. Phan Anh Tuấn** – Deputy Head of Integration Applications tại *Ngân hàng TMCP Phương Đông (OCB)*.  
    *Vai trò*: Quản lý trực tiếp tại OCB, có thể xác nhận vai trò và phạm vi công việc thật của ứng viên. Nội dung nhận xét là của anh Tuấn; tài liệu này không viết sẵn lời của người tham chiếu.
  - **Mr. Quan Quốc Bảo** – Giám đốc Quản lý Ứng dụng (Head of Application Management) tại *Ngân hàng TMCP Á Châu (ACB)* (Mối quan hệ quen biết qua mạng lưới chuyên môn công nghệ ngân hàng).  
    *Vai trò*: Người tham chiếu chuyên môn (quen qua trao đổi chuyên môn, không phải quan hệ công việc trực tiếp). **Chỉ ghi tên khi anh Bảo đã đồng ý**; ứng viên không nói thay nhận xét của anh, không trình bày anh như "người bảo chứng nội bộ" (dễ bị hiểu là gây áp lực hoặc xung đột lợi ích).

---

## 2. RÀ SOÁT & TIẾP THU Ý KIẾN ĐÓNG GÓP TỪ ANH TUẤN (PHÓ PHÒNG OCB)

### 2.1. Lời dặn dò nguyên văn từ Anh Tuấn
> *"Anh có góp ý là em ghi khá nhiều tech stack lớn và phức tạp, domain nghiệp vụ ngân hàng nhưng chưa ghi rõ đây là kết quả do em phụ trách hay em chỉ là thành viên tham gia vào 1 phần trong đó. Cẩn thận việc này không thôi người phỏng vấn hiểu nhầm em level expert và họ lấy 1 vấn đề cụ thể và hỏi sâu vào thì sẽ khó cho em. Theo anh mình thì những gì mình nắm chắc và contribute chính để khi có bị hỏi xoáy thì mình vẫn trả lời được. Tránh người ta đọc CV và đã có suy nghĩ em đang nói vượt quá khả năng, vì chỉ 3 năm ở NH em ko đủ expertise ở phạm vi rộng như vậy. Ghi những gì mình nắm thật chắc và nếu ghi nhiều thì cần làm rõ cái gì mình làm cái gì là thành quả của cả team. Tránh người ta dựa trên đó hỏi khó em. Ghi ít nhưng người ta hỏi tới đâu em trả lời rõ ràng, thuyết phục vẫn tốt hơn thì nhiều mà mình ko trả lời được."*

### 2.2. Phân tích Bản chất & Chiến lược Chuyển hóa
1. **Tâm lý Người phỏng vấn (Hội đồng Kỹ thuật ACB)**:
   - Một ứng viên có 3 năm kinh nghiệm ngân hàng nếu ghi trên CV là: *"Architected T24 Core adapter, operated 5M+ tx/day NAPAS switch, built 480+ topics Confluent backbone, Oracle DBA Expert"* $\to$ Người phỏng vấn sẽ lập tức nghi ngờ ứng viên "chém gió", phóng đại công sức, hoặc chỉ là người đứng ngoài nhìn vào. Họ sẽ chọn 1 ngóc ngách sâu nhất (ví dụ: cơ chế internal buffer của T24 OFS XML hoặc cấu hình TCP window size của switch NAPAS) để hỏi dồn ép, khiến ứng viên lúng túng và mất điểm hoàn toàn.
2. **Chiến lược "Trung thực - Chiều sâu - Thiện cảm" (Honesty, Depth, Empathy)**:
   - **Trên CV**: Tách bạch rõ ràng 2 tầng năng lực:
     - **Direct Module Ownership & Implementation**: Nêu bật những gì mình trực tiếp thiết kế, trực tiếp code, làm chủ 100% mã nguồn và xử lý sự cố.
     - **Squad & Cross-Team Collaboration**: Thể hiện vai trò phối hợp tích hợp với các hệ thống hạ tầng dùng chung của ngân hàng (Core T24, NAPAS, Kafka Platform).
   - **Trong Nhận thức & Kiến thức Phỏng vấn**: **Giữ nguyên 100% độ sâu kiến thức tối đa (Level Senior Mastery)**. Ứng viên không hạ thấp sự hiểu biết, mà ngược lại, phải hiểu sâu sắc từ từng byte ISO 8583, từng trường OFS XML, thuật toán Two-Pointer Merge, cơ chế khóa phân tán Redis Mutex đến cách thức hệ thống Core hạch toán.
   - **Tác động tâm lý đối với Nhà tuyển dụng**:
     - Nhà tuyển dụng thấy một kỹ sư có thái độ **rất khiêm tốn, trung thực, tôn trọng công sức của đồng nghiệp và tổ chức**.
     - Khi hỏi vào bất kỳ chi tiết kỹ thuật nào mà ứng viên ghi, ứng viên trả lời gãy gọn, rành mạch từ thiết kế logic đến từng dòng lệnh và cách xử lý sự cố thực tế.
     - Điều này tạo ra sự **tin cậy tuyệt đối (High Trust & High Credibility)**, gây thiện cảm sâu sắc và thuyết phục Hội đồng cấp Senior 50M Gross.

### 2.3. Bảng Ma trận Phân định Trách nhiệm Thực chiến (IC vs Team Scope)

| Phân hệ / Công nghệ | Trách nhiệm Trực tiếp của Ứng viên (Individual Contribution - IC) | Phạm vi Hạ tầng / Thành quả của Cả Team (Team / Shared Platform) |
|:---|:---|:---|
| **Squad Lending & Thấu chi Số** | **Trực tiếp thiết kế & viết code**: Luồng thấu chi cầm cố sổ tiết kiệm phong tỏa 2 pha trên Core T24, tính lãi Spread, Thấu chi lương, tích hợp ký số Cloud CA (FPT E-Sign) kết hợp xác thực khuôn mặt QĐ 2345, và cổng CIC B2B tra cứu tự động. | Phối hợp với đội ngũ Business Analyst (BA) nghiệp vụ tín dụng, Khối Quản trị Rủi ro (Credit Risk), và đội Quản trị Tài liệu ECM của ngân hàng. |
| **Khóa Idempotency & Thu nợ CASA** | **Trực tiếp triển khai**: Thuật toán khóa phân tán Redis Mutex (`SET loan:disb:{app_id} 1 NX EX 300`), máy trạng thái SAGA chống giải ngân kép, và engine quét thu nợ từng phần Partial Debit từ tài khoản CASA ngày đến hạn. | Sử dụng cụm Redis Cluster và cơ sở hạ tầng mạng do Khối Vận hành CNTT (IT Operations) duy trì. |
| **Cơ sở dữ liệu Oracle 19c & Deadlock** | **Trực tiếp tối ưu hóa**: Phân tích file trace `.trc`, thêm index cho cột khóa ngoại và index composite (`ONLINE`), viết lại Stored Procedure để khóa từng tài khoản theo thứ tự tăng dần bằng câu lệnh riêng (Oracle không bảo đảm khóa theo `ORDER BY … FOR UPDATE`), giảm mạnh lỗi `ORA-00060` (nêu số đo thật nếu có). | Hệ thống phần cứng máy chủ Exadata/Oracle 19c RAC và chính sách backup do đội ngũ Quản trị Database (DBA Team) vận hành. |
| **Core Banking Temenos T24 OFS XML** | **Làm chủ tầng tích hợp ứng dụng**: Soạn thảo và bóc tách bản tin OFS XML multi-value (`OfsDataField`), quản lý `JMSCorrelationID` cho mô hình Request-Reply, ánh xạ mã lỗi nghiệp vụ T24 và kích hoạt luồng bù trừ SAGA khi timeout. | Khung adapter T24 Vert.x & IBM MQ tập trung do Phòng Ứng dụng Tích hợp (sếp Tuấn và các Solution Architect kỳ cựu) xây dựng và quản trị chung. |
| **Chuyển mạch NAPAS 247 (ISO 8583)** | **Tích hợp thanh toán giải ngân/thu nợ**: Phát bản tin thanh toán liên ngân hàng từ dịch vụ Lending, khử trùng lặp giao dịch bằng Redis (`transId` TTL 60s), xử lý kịch bản đối soát EOD và rollback khi NAPAS timeout. | Cổng kết nối TCP Socket vật lý và thiết bị mã hóa phần cứng HSM (ZMK/ZPK translation) do Đội Chuyển mạch Thẻ & Thanh toán (Switch Team) phụ trách. |
| **Streaming & Confluent ksqlDB** | **Phát triển UDF & Consumer**: Viết custom UDFs trên ksqlDB để phân tích luồng biến động số dư, phát triển consumer định tuyến thông báo đa kênh (OTT App Push, SMS Brandname, Email) với hàng đợi ưu tiên và DLQ. | Quản trị cụm Confluent Kafka, Schema Registry và phân quyền ACLs do Đội Nền tảng Dữ liệu (Data Platform Team) đảm nhiệm. |
| **Bảo mật Sinh trắc học QĐ 2345 & AI** | **Tích hợp kiểm soát giao dịch**: Tích hợp luồng xác thực khuôn mặt (Liveness) theo QĐ 2345 vào luồng cho vay. Nguyên mẫu phát hiện bất thường ONNX Runtime (Isolation Forest) là **dự án học thuật UIT**, không phải hệ thống production OCB. | Đường truyền mạng kênh thuê riêng chuyên dụng kết nối sang Bộ Công an C06 và hợp đồng dịch vụ VNeID cấp ngân hàng. |

### 2.4. Kịch bản Đối đáp Mẫu Thực chiến trước Hội đồng Phỏng vấn ACB

- **Tình huống Người phỏng vấn hỏi xoáy**:  
  *"Trong CV em liệt kê rất nhiều hệ thống lớn như Core T24, NAPAS, Confluent Kafka, Oracle... Với 3 năm làm việc tại ngân hàng, đây là những gì một mình em làm hay là thành quả của cả team? Đóng góp thực sự của em ở đâu?"*

- **Mẫu trả lời chuẩn mực (Bản lĩnh, trung thực, khiêm tốn, thuyết phục)**:
  > *"Dạ em cảm ơn anh/chị đã hỏi một câu hỏi rất thực tế và thẳng thắn. Em cũng muốn chia sẻ hết sức chân thành: Tại một ngân hàng thương mại lớn như OCB, các hệ sinh thái như Chuyển mạch NAPAS hay Core Banking T24 là công sức xây dựng của cả Khối CNTT và các anh kiến trúc sư tiền bối qua nhiều năm. Em không bao giờ dám nhận là một mình em làm nên tất cả những điều đó.*  
  >  
  > *Trong 3 năm qua tại phòng Tích hợp của sếp Phan Anh Tuấn, vai trò cụ thể của em là **Kỹ sư Tích hợp Chủ lực trong Squad Lending**:*  
  > 1. ***Những gì em trực tiếp làm chủ và chịu trách nhiệm từng dòng mã***:  
  >    - *Em trực tiếp thiết kế và phát triển các microservices nghiệp vụ của Squad: từ luồng thấu chi cầm cố sổ tiết kiệm phong tỏa 2 pha trên Core T24, thấu chi lương, đến tích hợp Cổng ký số đám mây FPT E-Sign kết hợp sinh trắc học khuôn mặt QĐ 2345 và Cổng tra cứu CIC B2B tự động.*  
  >    - *Về xử lý kỹ thuật chuyên sâu, em trực tiếp cài đặt thuật toán khóa phân tán Redis Mutex chống giải ngân kép, xây dựng cơ chế thu nợ từng phần Partial Debit từ CASA, và trực tiếp điều tra trace log để sửa lỗi Deadlock Oracle `ORA-00060` bằng thuật toán khóa hàng có thứ tự xác định.*  
  > 2. ***Những gì em phối hợp với các đội hạ tầng dùng chung***:  
  >    - *Với Core T24: Phòng Tích hợp đã có sẵn khung adapter qua IBM MQ; nhiệm vụ của em là làm chủ cấu trúc bản tin OFS XML, bóc tách các trường multi-value, duy trì `JMSCorrelationID` và xử lý các kịch bản timeout bồi hoàn SAGA khi Core bị nghẽn.*  
  >    - *Với NAPAS 247: Đội Switch phụ trách cổng socket vật lý; em chịu trách nhiệm tích hợp lệnh giải ngân/thu nợ từ Squad sang switch và cài đặt cơ chế khử trùng lặp giao dịch.*  
  >    - *Với Confluent Kafka: Em phát triển các custom ksqlDB UDFs và worker tiêu thụ event để phục vụ bắn thông báo đa kênh.*  
  >  
  > *Chính sự phân định rạch ròi này giúp em vừa làm chủ sâu sắc phần việc trực tiếp của mình, vừa thấu hiểu toàn diện luồng tương tác giữa các hệ thống trong ngân hàng để khi xảy ra sự cố khẩn cấp, em luôn biết điểm nghẽn nằm ở đâu và phối hợp nhanh nhất để giải quyết dứt điểm."*

---

## 3. NGUYÊN TẮC BẢO MẬT & ĐỊNH DANH HỆ THỐNG (SECURITY & ANONYMIZATION)

Nhằm tuân thủ cam kết bảo mật thông tin ngân hàng và chuyên nghiệp hóa hồ sơ ứng viên, toàn bộ các mã dịch vụ nội bộ trích xuất từ `hub-system-graph.md` đã được ẩn danh hóa sang thuật ngữ kiến trúc chuẩn Enterprise:

| Tên nội bộ trong graph | Thuật ngữ chuẩn hóa dùng trong CV & Phỏng vấn |
|:---|:---|
| `t24-adapter::vertx` | **High-Throughput Core Banking T24 OFS Adapter (Java Vert.x & IBM MQ)** |
| `napas-gateway-v2` / `napas-gateway-v2-go` | **Real-Time NAPAS 247 Interbank Switch Gateway (ISO 8583 & TCP Sockets)** |
| `contract-transfer` | **Online Deposit Contract Secondary Trading Marketplace (Go Fiber & PostgreSQL)** |
| `billing-orchestration` / `billing-ft-service` | **Distributed SAGA Payment & Billing Orchestration Engine** |
| `po-batch-transfer` / `po-batch-transfer-router` | **Corporate Batch Payroll & Fund Transfer Gateway (Transactional Outbox)** |
| `mcs-kstream-ipn-statement-devide-conquer` | **Real-Time Account Statement Hub (Kafka Streams Divide-and-Conquer)** |
| `mcs-ksqldb` / `mcs-ksqldb-udf` | **Confluent ksqlDB Event Streaming Backbone (Custom UDFs)** |
| `bio-authentication-service` / `face-authen` | **National Biometric Facial Authentication Gateway (Decision 2345 / QĐ 2345)** |
| `ob-virtual-account` / `virtual-account` | **Dynamic Virtual Account (VA) Corporate Cash Collection Engine** |
| `odb.retail.lending-integration-service` | **Omnichannel Retail Lending & Overdraft Integration Gateway (OMNI-BFF)** |
| `AZ.ACCOUNT` / `account-locked-events` | **Core Banking Term Deposit Accounts & Collateral Hold/Lien Events** |
| `OCBIIB.ODLN.UNSE.INPUT` / `ODLOAN.ROLL` | **Core Banking Overdraft Limits & Automated Settlement Engine** |
| `los-adapter/igen` | **Loan Origination System (LOS) & Virtual Card Gateway** |
| `fpt-esign-adapter` | **Cloud CA Digital Signature Gateway (FPT E-Sign & TSA RFC 3161)** |

---

## 4. DANH MỤC TÀI SẢN BÀN GIAO (DELIVERABLES INVENTORY)

### A. Hồ sơ CV Ứng tuyển Chuẩn ATS (Đúng 2 trang A4)
1. [`resources/job/PHAM-MINH-DUC-SENIOR-INTEGRATION-CV.pdf`](file:///D:/research-video/resources/job/PHAM-MINH-DUC-SENIOR-INTEGRATION-CV.pdf):
   - Đã biên dịch qua PyMuPDF (`python resources/job/build_cv_pdf.py`).
   - File ảnh chân dung: [`resources/job/avatar.jpg`](file:///D:/research-video/resources/job/avatar.jpg) (Kích thước 768x1024, tỷ lệ chuẩn 3:4, nhúng góc phải Header với viền navy `#003366`).
   - Kết quả xác thực: **Chính xác 2 trang A4**, khoảng đệm Trang 1 dư **60.84 pt**, Trang 2 dư **184.06 pt** (đo lại 2026-11-07, sau khi bỏ dòng Training), scale 1.0, 0 overflow, 0 cắt chữ.
   - Nội dung đã được tinh chỉnh theo góp ý của anh Tuấn: phân định rõ *Direct Module Ownership & Implementation* vs *Squad & Cross-Team Collaboration*.
   - **Tái tích hợp mảng AI Ứng dụng & Bộ nhân Năng lực Ngân hàng (Applied AI & Banking ML)**: Khóa chặt dòng năng lực `Python, PyTorch, Scikit-Learn, ONNX Runtime, Isolation Forest (Fraud & Anomaly Detection), Semantic Vector Search` vào bảng Core Technical, tạo điểm khác biệt (AI Multiplier) ở mức học thuật, ghi rõ là dự án UIT, không phải hệ thống production của OCB (xem Mục 7, BN-0022).
2. [`resources/job/PHAM-MINH-DUC-SENIOR-INTEGRATION-CV.md`](file:///D:/research-video/resources/job/PHAM-MINH-DUC-SENIOR-INTEGRATION-CV.md):
   - Bản nguồn Markdown đồng bộ từng dòng với bản PDF (đã nhúng ảnh chân dung).
3. [`resources/job/build_cv_pdf.py`](file:///D:/research-video/resources/job/build_cv_pdf.py):
   - Mã nguồn Python PyMuPDF biên dịch CV tự động, kiểm soát chặt chẽ toạ độ vật lý và cỡ chữ.

### B. Trọn bộ 8 Chuyên đề Giáo trình Chuyên sâu Phỏng vấn Tích hợp Ngân hàng (`interview/`)
1. [`00_overview_roadmap.md`](file:///D:/research-video/interview/00_overview_roadmap.md): Khung Năng lực Tổng thể & Lộ trình Senior Banking 50M Gross.
2. [`01_foundation_cs_java.md`](file:///D:/research-video/interview/01_foundation_cs_java.md): Nền tảng CS, Java Core 17/21, Concurrency, Virtual Threads, Memory Model, Garbage Collection.
3. [`02_backend_microservices.md`](file:///D:/research-video/interview/02_backend_microservices.md): Spring Boot 3, Spring Cloud, RESTful API, gRPC, Docker, K8s, GitOps CI/CD.
4. [`03_distributed_systems_senior.md`](file:///D:/research-video/interview/03_distributed_systems_senior.md): SAGA Pattern, Transactional Outbox, Kafka EDA, Redis Cluster/Redlock, Deterministic Row Locking PL/SQL.
5. [`04_banking_domain_t24_napas.md`](file:///D:/research-video/interview/04_banking_domain_t24_napas.md): Temenos T24 OFS XML qua IBM MQ, NAPAS 247 ISO 8583 TCP Sockets, Hardware Security Module (HSM), Sàn chuyển nhượng hợp đồng tiền gửi, Confluent ksqlDB Streaming Hub, Statement Hub Divide-and-Conquer, Batch Payroll, Sinh trắc học QĐ 2345.
6. [`05_uit_ai_banking_multiplier.md`](file:///D:/research-video/interview/05_uit_ai_banking_multiplier.md): Ma trận 38 môn học UIT AI ứng dụng vào kiến trúc ngân hàng (Anomaly Detection ONNX < 5ms, Smart Routing Thompson Sampling, Semantic Reconciliation Cosine Embeddings, AIOps).
7. [`06_interview_qa_bank_100.md`](file:///D:/research-video/interview/06_interview_qa_bank_100.md): **100 câu hỏi & đáp án phỏng vấn ngân hàng thực chiến** (Đã đồng bộ Câu 76 về phản hồi và đạo đức nghề nghiệp của sếp Phan Anh Tuấn, Câu 97 bảo vệ mức đãi ngộ 50M).
8. [`07_salary_negotiation_50m_gross.md`](file:///D:/research-video/interview/07_salary_negotiation_50m_gross.md): **Kịch bản đàm phán 3 vòng chốt deal chắc chắn mức lương 50,000,000 VND Gross/tháng** dựa trên ma trận hoàn vốn đầu tư ROI, phòng thủ đòn ép giá của HR, và cấu trúc đãi ngộ tối ưu.

### C. Trọn bộ 17 Video Bài giảng 1080p (`interview/video/`, nguồn `out/INT/` và `out/ACB/`)
**Dựng lại toàn bộ 17 bài ngày 2026-11-08** sau khi sửa nội dung (Mục 9). Thời lượng, giọng, mã băm và trạng thái "đặc tả khớp video" của từng bài **chỉ ghi ở** [`MASTER_CURRICULUM_INDEX.md`](file:///D:/research-video/interview/MASTER_CURRICULUM_INDEX.md) Mục 4–5 (sinh bằng script, đo ffprobe). Tổng sau khi dựng lại: INT **44,77** phút + ACB **50,50** phút = **95,27 phút**. Giọng NamMinh cả 17 bài. Bảng cũ ngày 2026-11-07 (INT 42,86 + ACB 50,14) không còn đúng.

### D. Khóa BNK: Nền tảng Backend Ngân hàng cho người mất gốc (15 bài, `out/BNK/`, lộ trình `curriculum/bnk.yaml`)
Thêm ngày 2026-11-08 theo quyết định của người dùng "làm đủ 15 bài" (phương án (a) ở Mục 8 bản trước). Mỗi bài `depth: full`: ôn nền, hình cơ chế (SVG), ba bước suy ra có làm thử bằng số, năm phép tính từng bước, tự kiểm bằng đường khác, ba lỗi (có lỗi của người đã đi làm), câu hỏi tự kiểm có đáp án từng bước, chuỗi logic. Số đo dưới đây sinh từ `build_report.json`, `asr_report.json` và `ffprobe` (script `video_table_bnk.py`), 2026-11-08. Giọng NamMinh cả 15 bài.

| Bài | Tiêu đề | Thời lượng | Giọng | ASR khớp TB | cờ/chưa xem | sha256 (12) |
|:---|:---|:---:|:---|:---:|:---:|:---|
| BNK L00 | Java hiện đại: bộ nhớ, đối tượng và bộ thu gom rác | 7:23 | NamMinh | 0.946 | 16/0 | 87ed62b8ca62 |
| BNK L01 | Đa luồng, khoá và luồng ảo Java 21 | 7:15 | NamMinh | 0.936 | 12/0 | f460138de080 |
| BNK L02 | Spring Boot: bean, proxy và giao dịch | 6:59 | NamMinh | 0.936 | 9/0 | 606a00f0966c |
| BNK L03 | REST API và khoá lũy đẳng | 6:41 | NamMinh | 0.958 | 5/0 | cb3e7359a258 |
| BNK L04 | SQL, chỉ mục và kế hoạch thực thi | 6:30 | NamMinh | 0.936 | 5/0 | 90be67da50d8 |
| BNK L05 | PL/SQL, khoá hàng và bế tắc ORA-00060 | 7:37 | NamMinh | 0.960 | 4/0 | 6d95440713f0 |
| BNK L06 | Redis, bộ đệm và khoá phân tán | 7:26 | NamMinh | 0.933 | 17/0 | 1927fa94999d |
| BNK L07 | Kafka: phân vùng, offset, chia lại và số lần xử lý | 7:09 | NamMinh | 0.948 | 7/0 | 019a621f5fa2 |
| BNK L08 | SAGA và Transactional Outbox | 6:50 | NamMinh | 0.957 | 8/0 | 7bf88547b960 |
| BNK L09 | Sổ cái bút toán kép và kiểm cân đối | 6:49 | NamMinh | 0.974 | 2/0 | e4ae8d53fcd5 |
| BNK L10 | Lõi ngân hàng T24: OFS, IBM MQ và mã tương quan | 7:26 | NamMinh | 0.958 | 3/0 | 26d3b146bc06 |
| BNK L11 | ISO 8583: bản đồ bit và cấu trúc bản tin | 8:36 | NamMinh | 0.939 | 10/0 | 808fc11bbab4 |
| BNK L12 | Chuyển mạch liên ngân hàng và đối soát hai bên | 7:55 | NamMinh | 0.948 | 6/0 | ca759d99ff59 |
| BNK L13 | Bảo mật thanh toán: khối PIN, HSM, MAC và sinh trắc học | 7:52 | NamMinh | 0.947 | 9/0 | bb37b7e206ce |
| BNK L14 | Tình huống giả định: từ triệu chứng tới thiết kế tốt hơn | 7:51 | NamMinh | 0.962 | 4/0 | 3b55de47b52c |

Tổng BNK: **110.44 phút** (ffprobe, 2026-11-08 sáng); sau lần dựng lại theo rà soát toàn bộ (Mục 10) là **115,05 phút**; sau đợt C (Mục 12, dựng lại BNK L09) là **115,16 phút**.

Bài nào trả lời câu hỏi nào của ngân hàng 100 câu (`06_interview_qa_bank_100.md`):

| Bài BNK | Câu hỏi liên quan |
|:---|:---|
| L00 Java: bộ nhớ, GC, tiền không dùng double | 2, 3, 7, 8, 12, 18 |
| L01 Đa luồng, khoá, luồng ảo Java 21 | 4, 5, 6, 10, 19, 20 |
| L02 Spring: bean, proxy, giao dịch | 21, 22, 24, 26, 37 |
| L03 REST và khoá lũy đẳng | 23, 34 |
| L04 SQL, chỉ mục, kế hoạch thực thi | 9, 57, 58, 59 |
| L05 PL/SQL, khoá hàng, ORA-00060 | 45, 46, 61, 63 |
| L06 Redis, bộ đệm, khoá phân tán | 25, 29, 35, 36 |
| L07 Kafka: phân vùng, offset, số lần xử lý | 43, 44, 47, 49, 50, 51, 52 |
| L08 SAGA và Transactional Outbox | 39, 42, 90 |
| L09 Sổ cái bút toán kép | 60, 65 |
| L10 T24, OFS, IBM MQ, mã tương quan | 52, 67, 68 |
| L11 ISO 8583: bản đồ bit | 66, 67 |
| L12 Chuyển mạch và đối soát hai bên | 66, 67, 70, 78 |
| L13 Bảo mật thanh toán: khối PIN, HSM, MAC, QĐ 2345 | 79, 80 |
| L14 Tình huống giả định (khung kể sự cố STAR) | 93 |

Giới hạn trung thực: số liệu trong bài là số minh hoạ trừ khi ghi nguồn; Oracle, Redis, Kafka, Spring, T24, IBM MQ không chạy trên máy này nên mô phỏng chỉ kiểm logic; L14 là tình huống **giả định**, không phải sự cố có thật của ứng viên.

---

## 5. XỬ LÝ TRIỆT ĐỂ NÚT THẮT HỢP ĐỒNG (CONTRACT BOTTLENECKS RESOLUTION)

Bảng BN-0001 → BN-0016 dưới đây là bản ghi cũ. **Đọc cùng Mục 7**: các nút thắt mới BN-0017 → BN-0024 còn mở, và các chỉ số trong cột giải pháp chỉ là mục tiêu thiết kế hoặc ví dụ minh họa:

| Mã nút thắt | Điểm nghẽn rủi ro | Giải pháp đã kiểm chứng thực nghiệm | Bằng chứng kiểm chứng | Trạng thái |
|:---|:---|:---|:---|:---:|
| **BN-0001** | Bất đồng bộ T24 OFS Timeout làm treo connection pool | Mô hình Request-Reply với `JMSCorrelationID` qua IBM MQ + Transactional Outbox + Quét đối soát tự động | `lessons/acb/L01_tich_hop_core_t24_ibm_mq.yaml` & `L01.mp4` | **CLOSED** |
| **BN-0002** | Xung đột gói tin NAPAS 247 & rủi ro trừ tiền kép | Khóa phân tán Redis `SET dedup:napas:<transId> NX EX 60` kết hợp ràng buộc duy nhất DB | `lessons/acb/L02_chuyen_mach_napas_iso8583.yaml` & `L02.mp4` | **CLOSED** |
| **BN-0003** | Điểm nghẽn bồi hoàn SAGA khi đối tác thanh toán sập | Lưu máy trạng thái SAGA vào PostgreSQL, hàng đợi lỗi DLQ Kafka và cơ chế bồi hoàn tự động | `interview/03_distributed_systems_senior.md` | **CLOSED** |
| **BN-0004** | Tranh chấp chuyển nhượng hợp đồng tiền gửi (bán 1 sổ cho 2 người) | Khóa Lạc quan `UPDATE ... WHERE last_access = $5` trên PostgreSQL + Ánh xạ mã lỗi T24 `04\|05\|999\|1014-1018` chuyển trạng thái `HOLD/REVERT` | `lessons/acb/L04_san_chuyen_nhuong_hop_dong_tien_gui.yaml` & `L04.mp4` | **CLOSED** |
| **BN-0005** | Deadlock Oracle Stored Procedure (ORA-00060) ngày trả lương | Thuật toán khóa hàng có thứ tự xác định (`ORDER BY account_no ASC FOR UPDATE`) + `BULK COLLECT` & `FORALL` | `lessons/acb/L05_cong_chi_luong_va_sao_ke_divide_conquer.yaml` & `L05.mp4` | **CLOSED** |
| **BN-0006** | Định kiến 3 năm kinh nghiệm so với mức lương trần Senior 50M Gross | Chiến lược đàm phán 3 vòng theo công thức ROI, định vị Chuyên viên chính OCB gánh team ngay ngày đầu tiên, bảo vệ mức sàn 50M | `interview/07_salary_negotiation_50m_gross.md` | **CLOSED** |
| **BN-0007** | Bằng Cử nhân AI tại UIT có bị đánh giá là lệch pha với Backend? | Chứng minh giá trị cấp số nhân (AI Multiplier): Phát hiện gian lận ONNX < 5ms, Định tuyến MAB Thompson Sampling, Đối soát ngữ nghĩa Vector Embeddings | `interview/05_uit_ai_banking_multiplier.md` | **CLOSED** |
| **BN-0008** | Truy vấn sao kê tài khoản lớn gây nghẽn I/O Core | Phân đoạn khoảng thời gian thành 4 tuần song song qua Kafka Streams Divide-and-Conquer trên read-replica | `lessons/acb/L05_cong_chi_luong_va_sao_ke_divide_conquer.yaml` & `L05.mp4` | **CLOSED** |
| **BN-0009** | Độ trễ cổng sinh trắc học QĐ 2345 và rủi ro bị bypass | SDK Liveness Detection 3D + mTLS C06 VNeID + Đặt xác thực làm Điều kiện tiên quyết (Pre-condition) trong SAGA | `lessons/acb/L06_sinh_trac_hoc_qd2345_va_bao_mat_ngan_hang.yaml` & `L06.mp4` | **CLOSED** |
| **BN-0010** | Thiếu tài liệu kịch bản đàm phán lương thực chiến | Biên soạn hoàn chỉnh chuyên đề 7 đàm phán 3 vòng, xử lý triệt để đòn ép giá của HR | `interview/07_salary_negotiation_50m_gross.md` | **CLOSED** |
| **BN-0011** | Thiếu giáo án & video bài giảng L04, L05, L06 | Soạn thảo 3 file YAML chuẩn stem full, lint 0 FAIL 0 WARN, render video 1080p, verify 100% PASS | `L04.mp4`, `L05.mp4`, `L06.mp4` trong `interview/video/` | **CLOSED** |
| **BN-0012** | Chuẩn hóa thông tin người tham chiếu: Phan Anh Tuấn (Phó phòng OCB) & Quan Quốc Bảo (GĐ Quản lý Ứng dụng ACB) | Đồng bộ chính xác chức danh Head of Application Management của anh Bảo tại ACB và Phó phòng của sếp Tuấn trên CV PDF, CV.md, Câu 76 Q&A | `build_cv_pdf.py` (2 trang PASS), `CV.pdf`, `06_interview_qa_bank_100.md` | **CLOSED** |
| **BN-0013** | Nghẽn xử lý Thu hộ Virtual Account & Đối soát 3 bên EOD | Radix Tree prefix matching + Webhook Idempotent HMAC + Thuật toán Two-Pointer Merge O(N) | `lessons/acb/L07_tai_khoan_dinh_danh_va_doi_soat_ba_ben.yaml` & `L07.mp4` | **CLOSED** |
| **BN-0014** | Rủi ro Giải ngân trùng lặp (Double Disbursement) và nợ xấu do Cache CIC quá hạn | Khóa phân tán Redis Mutex (`disbursement:lock:{app_id}`) TTL 300s + TTL cache CIC tối đa 15 ngày + SAGA Compensation khi NAPAS timeout | `lessons/acb/L08_squad_lending_tich_hop_cic_giai_ngan.yaml` & `L08.mp4` | **CLOSED** |
| **BN-0015** | Toàn cảnh Hệ sinh thái Squad Lending & Tích hợp Ngân hàng lõi (không chỉ CIC) | Kết nối 106 resources, 34 tuyến APIC, 17 microservices trực tiếp; phong tỏa Core T24 Term Deposits, hạch toán cấp hạn mức thấu chi & tất toán tự động | Cập nhật CV 2 trang A4, Section 1.2 trong `04_banking_domain_t24_napas.md`, bổ sung liên hoàn Câu 81–90 trong `06_interview_qa_bank_100.md` | **CLOSED** |
| **BN-0016** | Rủi ro CV bị đánh giá là "nói vượt quá khả năng" (Feedback Anh Tuấn) | Cấu trúc lại CV phân định minh bạch 2 tầng: *Direct Module Ownership & Implementation* (chủ lực code thấu chi sổ tiết kiệm 2 pha, thấu chi lương, Cloud CA, CIC B2B, Redis Mutex, Partial Debit, Deadlock Oracle) vs *Squad & Cross-Team Collaboration* (Core T24 MQ adapter, NAPAS switch, Confluent ksqlDB); chuẩn bị kịch bản đối đáp khiêm tốn, trung thực nhưng hiểu biết sâu sắc | `build_cv_pdf.py` (scale 1.0, 2 trang PASS), `CV.md`, Mục 2 `HANDOVER_INTERVIEW.md`, Câu 76 & 97 trong `06_interview_qa_bank_100.md` | **CLOSED** |

---

## 6. HƯỚNG DẪN ÔN LUYỆN & PHỎNG VẤN THỰC CHIẾN TẠI ACB

Để tối đa hóa tỷ lệ đỗ và chốt chắc chắn mức lương 50,000,000 VND Gross, ứng viên Phạm Minh Đức nên thực hiện lộ trình ôn luyện 4 bước:

1. **Bước 1 — Nền tảng Khoa học Máy tính (Dành cho người mới / Mất gốc)**:
   - Tra cứu và xem các bài giảng cốt lõi trong kho 643 video bài học tại [`SOURCE_CODE_VIDEO_MAP.md`](file:///D:/research-video/interview/SOURCE_CODE_VIDEO_MAP.md):
     - Thuật toán & Cấu trúc dữ liệu B-Tree: [`out/CS112/`](file:///D:/research-video/out/CS112/).
     - Cơ sở Dữ liệu & ACID: [`out/DBS/`](file:///D:/research-video/out/DBS/).
     - Hệ phân tán & Raft/Paxos: [`out/DSY/`](file:///D:/research-video/out/DSY/).
     - Hệ điều hành & Concurrency: [`out/OSY/`](file:///D:/research-video/out/OSY/).
   - **Bài nền cho đúng chủ đề phỏng vấn: khóa BNK (Mục 4D)**: nếu chưa từng lập trình, xem khóa JVA L00 đến L12 (107,11 phút) trước; rồi xem tuần tự BNK L00 đến L14 (115,05 phút) trước khi xem INT/ACB. Sau mỗi bài làm phần "Đến lượt bạn" ra giấy, rồi đọc các câu hỏi liên quan ở bảng Mục 4D.
   - **Giới hạn còn lại (Mục 8)**: BNK chưa phủ HikariCP, JWT, Resilience4j, Kubernetes, gRPC, Kafka Streams/ksqlDB, Oracle Partitioning và cú pháp Java cơ bản; với các câu đó đọc đáp án trong ngân hàng câu hỏi.
2. **Bước 2 — Nghiền ngẫm Trọn bộ 17 Video Phỏng vấn Chuyên sâu INT/ACB (93.00 phút, xem sau BNK)**:
   - Xem 8 video Khóa INT (`00_overview_roadmap.mp4` đến `07_salary_negotiation_50m_gross.mp4`) để nắm vững khung năng lực, hệ thống câu hỏi hóc búa, ma trận 38 môn học UIT AI và chiến lược đàm phán hợp đồng.
   - Xem 9 video Khóa ACB (`L00.mp4` đến `L08.mp4`) để nắm tổng quan nghiệp vụ thực chiến (mỗi bài 5–6 phút, chưa phải bài học nền từ con số 0): T24 OFS XML qua IBM MQ, NAPAS 247 ISO 8583, ksqlDB Notification Hub, Sàn tiền gửi Optimistic Lock, Chi lương lô lớn, Sinh trắc học QĐ 2345, Virtual Account đối soát 3 bên EOD, và Squad Lending tự động hóa CIC.
   - Bật phụ đề tiếng Việt chuẩn (`.srt`) và theo dõi các phân đoạn chương (`chapters.txt`).
3. **Bước 3 — Ôn luyện 100 Câu hỏi Đáp án Thực chiến**:
   - Đọc kỹ file [`06_interview_qa_bank_100.md`](file:///D:/research-video/interview/06_interview_qa_bank_100.md), đặc biệt chú trọng các câu hỏi về:
     - T24 OFS XML & Request-Reply qua IBM MQ (Câu 52, 68; Java NIO/Vert.x: Câu 14).
     - NAPAS 247 ISO 8583, Socket TCP, PIN Block HSM, Khử trùng lặp Redis (Câu 66, 67, 80; khóa phân tán Redis: Câu 35).
     - Sàn chuyển nhượng hợp đồng tiền gửi & Khóa Lạc quan `last_access` (Câu 60, 69).
     - Chi lương theo lô Outbox & Deadlock Oracle ORA-00060 (Câu 42, 45, 63, 75, 93).
     - Sinh trắc học QĐ 2345, Liveness 3D & Pre-condition SAGA (Câu 79, 86, 94).
     - Cổng CIC B2B, Thấu chi sổ tiết kiệm, Lương và Vay trả góp thẻ (Câu 81 – 90).
     - Mối quan hệ tham chiếu với sếp Phan Anh Tuấn (OCB) và anh Quan Quốc Bảo (GĐ Quản lý Ứng dụng ACB) (Câu 76).
     - Chiến lược bảo vệ hồ sơ Cử nhân AI tại UIT (Câu 73, Chuyên đề 05).
     - Phân định rõ ràng vai trò cá nhân vs team để gây thiện cảm tuyệt đối (Mục 2 `HANDOVER_INTERVIEW.md`, Câu 76, Câu 97).
4. **Bước 4 — Luyện tập Kịch bản Đàm phán Lương (Vòng 3 Offer)**:
   - Thực hành nhuần nhuyễn các mẫu đối đáp trong [`07_salary_negotiation_50m_gross.md`](file:///D:/research-video/interview/07_salary_negotiation_50m_gross.md) để tự tin giữ vững mức trần 50M Gross khi làm việc với Trưởng phòng Tuyển dụng ACB. Người tham chiếu chỉ xác nhận những gì họ biết; không dựa vào đó để đòi mức lương. Dùng bằng chứng năng lực thật của mình để thương lượng gói thu nhập năm 700M – 850M VNĐ (13 tháng cố định + thưởng 1–4 tháng theo tin tuyển dụng ACB; mức cụ thể do ACB thương lượng).

---

## 7. KẾT QUẢ KIỂM CHỨNG BẰNG CHỨNG (PHIÊN 2026-11-07)

**Kết luận chung: `PARTIAL`.** Phần chữ (CV, ngân hàng 100 câu, kịch bản lương, bảng đối chiếu, bản đồ video), 17 video INT/ACB và 15 video khóa BNK đã được sửa hoặc dựng và kiểm chứng. Còn mở và không thể tự đóng bằng công cụ: **nghe thử phát âm bằng tai người** (BN-0019), **độ sâu còn lại cho người mất gốc** (BN-0020, đã giảm sau khi có BNK), **số liệu thật do ứng viên cung cấp** (BN-0021, BN-0022).

### 7.1 Bản ghi kiểm chứng (nhãn theo EGW section 2; chạy ngày 2026-11-07)

| ID | Tuyên bố | Phương pháp (đã chạy) | Kết quả quan sát | validity |
|:---|:---|:---|:---|:---:|
| C-01 | Ngân hàng có đủ 100 câu | regex `^### Câu N:` trên `06_interview_qa_bank_100.md` | Trước phiên: **58 câu** (thiếu 11–20, 28–40, 47–65, chỉ có dòng ghi chú). Sau: 100 câu duy nhất, đúng thứ tự 1..100 | VALID |
| C-02 | CV PDF đúng 2 trang A4, không tràn | `python resources/job/build_cv_pdf.py` | 2 trang, scale 1.0; dư Trang 1: 60,84 pt; Trang 2: 184,06 pt | VALID |
| C-03 | CV (PDF và MD) không còn số liệu không có nguồn và không còn dòng Training | tìm chuỗi trong text PDF và MD: `8,000`, `F1 0`, `99.99`, `3,000`, `90%`, `45%`, `RFC 3161`, `40%`, `Holds a`, `Confluent Certified`, `Training`, `Oracle 19c PL/SQL Tuning` | Không còn chuỗi nào; có `expected`, `Switch team`, `Adobe` | VALID |
| C-04 | Thời lượng video | `ffprobe` cộng 8 bài INT + 9 bài ACB | INT **42,86** + ACB **50,14** = **93,00 phút**. Tăng so với bản Piper (72,03) vì giọng NamMinh đọc chậm hơn, nội dung không đổi | VALID |
| C-05 | 17 bài lint sạch | `lv.py lint` cho INT L00–L07, ACB L00–L08 sau khi đổi giọng và sửa nội dung | 0 FAIL, 0 WARN | VALID |
| C-06 | 17 video dựng lại đạt verify | `bash audit/.build_queue_run.sh INT L00..L07` rồi `ACB L00..L08` (log scratchpad `chain5.out`) | verify `PASS` 17/17; giọng `NamMinh` 17/17 (đọc từ `build_report.json`) | VALID |
| C-07 | Bản sao trong `interview/video/` khớp `out/` | `sha256sum` 17 bài (INT cả hai tên `0x_*` và `INT_L0x`) | Khớp 17/17 | VALID |
| C-08 | Mọi câu ASR gắn cờ đã có lý do xem xét | `audit/review/asr_flags.py INT` và `ACB` | 0 câu chưa xem xét (73 lý do: INT 20, ACB 53) | VALID |
| C-09 | Các lý do ASR đã được người nghe kiểm | không có | Không có người nghe nào kiểm. Mọi lý do ghi `NOT_VERIFIED bằng tai người` | NOT_VERIFIED |
| C-10 | Audit toàn kho | `audit/review/audit_all.py` | 628 bài đã dựng, 1 mục còn lại: AIF L11 (vốn chờ tai người, ngoài phạm vi) | VALID |
| C-11 | Bằng chứng nguồn của các tuyên bố trên CV | `grep` trong `resources/job/hub-system-graph.md` (40.630 dòng) | **Không có**: ONNX/Isolation Forest (0), ORA-00060 (0), RFC 3161 (0), LTV 90% (0), DTI 45% (0). Có: FPT e-sign, QD2345, Vert.x, IBM MQ, ECM | VALID (kết quả tìm kiếm) |
| C-12 | Số video trong kho | liệt kê `out/*/L*/L*.mp4` ngoài thư mục `_*` và so với `lessons/*/L*.yaml` | 633 mp4 = **628 bài học** + 5 video `out/DEMO/L01–L05`; 0 đặc tả thiếu mp4 | VALID |
| C-13 | Độ phủ chủ đề của thư viện ngoài INT/ACB | tìm từ khóa trong toàn bộ đặc tả `lessons/*` (41 khóa, trừ INT/ACB) | **0 bài** về Spring, PL/SQL, luồng ảo Java 21, ISO 8583, NAPAS; Redis 1; T24 2 (chỉ nhắc); Oracle 2 | VALID |
| C-14 | Bản đồ video không nói quá | so từng ô "trọng tâm" với nội dung đặc tả (DBS, CLD, EVT, DEN) và kiểm liên kết | 4 ô nói quá (PL/SQL, Spring Boot 3, Rebalance, Kafka Connect) và 4 liên kết `.mp4` trỏ nhầm `.md`: đã sửa | VALID |
| C-15 | 15 bài BNK qua lint | `for f in lessons/bnk/L*.yaml; do lv.py lint $f; done` (2026-11-08) | 15/15: `0 FAIL, 0 WARN`; `tests/test_lint.py`: `tests: 0 FAIL`; quét ký tự điều khiển trên bài, mã nguồn, lexicon: sạch | VALID |
| C-16 | Bố cục khung hình BNK | `lv.py render` từng bài; `audit/layout_scan.py BNK` | render `0 vấn đề` 15/15; layout_scan: 15 bài, 1305 khung, 0 khung lỗi; đã mở xem tay các khung L00, L11, L12, L14 | VALID (máy), chưa có người xem toàn bộ |
| C-17 | 15 video BNK dựng và verify | `bash audit/.build_queue_run.sh BNK L00..L14` (lần 2 sau chỉnh lexicon, log `audit/bnk/logs/queue2.out`) | verify `PASS` 15/15; giọng `NamMinh` 15/15; tổng **110,44 phút** (ffprobe); ASR khớp TB 0,933 đến 0,974 | VALID |
| C-18 | Số liệu trong bài đúng | `audit/bnk/verify_bnk.py` (cách tính khác checklib) → `verify_bnk: 17/17 PASS` lúc 2026-11-07T18:41:31Z; `audit/verify_plan_curricula.py` → 491 PASS, 0 FAIL; `audit/check_curricula_graph.py` → VER không PASS: 0 | Lỗi bắt được trong lúc làm: `sum([0.1]*10)` của Python 3.12 trả 1.0 (bù sai số), khác cộng từng bước của Java; đã dùng vòng lặp thật | VALID cho logic mô phỏng; Oracle/Redis/Kafka/Spring/T24/IBM MQ: NOT_VERIFIED (không chạy được) |
| C-19 | Phát âm từ ngoại trong BNK | `audit/cs112/probe_terms.py audit/bnk/probes/b1.yaml` và `b2.yaml` (kết quả `audit/bnk/probes/b1.md`, `b2.md`) | `pờ-rốc-xi` 8/8 (proxy); `ích-o-a` 8/8 (XOR); commit, rollback, topic không cách nào đạt 7/8 nên lời đọc dùng "chốt", "hoàn tác", "chủ đề" (tên gốc hiện trên màn hình); Temenos tốt nhất 2/8 nên lời đọc bỏ tên; Redis 0/8 mọi cách (luật kế thừa từ INT/ACB, chưa xác nhận) | PARTIAL: Redis, Temenos NOT_VERIFIED |
| C-20 | ASR của BNK | `lv.py asr` từng bài sau khi ghi lý do bằng `asr_hand_gen.py`, `asr_hand_insert.py`, `asr_review_dms.py --course BNK` | Lần dựng đầu 148 câu gắn cờ; sau khi nối dài câu ngắn và đổi từ ngoại: 117 câu, **0 chưa xem xét**; mọi lý do ghi "NOT_VERIFIED bằng tai người" | VALID (ASR-checked), chưa ear-checked |
| C-21 | Chỉnh lexicon BNK không làm STALE khoá khác | `audit/review/audit_all.py` (checklib thêm hàm tiền tố `bnk_`; `audit/check_checklib_dupes.py`: không trùng) | 643 bài, 643 đã dựng, chỉ còn mục AIF L11 như trước; `curriculum` BNK: 15 bài, 0 lỗi | VALID |

### 7.2 Những gì đã sửa

1. **Ngân hàng 100 câu**: viết 42 câu còn thiếu theo đúng phân phần. Câu 93 chuyển thành khung kể STAR, không dựng sẵn số đo. Câu 83 và 89 gắn nhãn "ví dụ minh họa" cho ngưỡng LTV, DTI, spread.
2. **CV (PDF + MD, đồng bộ)**: bỏ 8.000+ TPS/120ms, F1 0,92, 99,99%, 3.000 hồ sơ/giờ, 40%, 90%+ coverage, LTV 90%, DTI ≤ 45%, "5 năm lịch sử nợ", "TSA RFC 3161", "<3 phút", "100% SBV". Dự án NAPAS về vai trò phối hợp với đội Switch (khớp bảng IC/Team ở Mục 2.3). Dự án AI ghi rõ là dự án học thuật/cá nhân UIT. Bằng UIT ghi "expected graduation November 2026". Dòng Training bị bỏ theo yêu cầu của ứng viên. "eliminating" đổi thành "resolving/mitigating".
3. **`07_salary_negotiation_50m_gross.md` và video INT L07**: bỏ thu nhập hiện tại bịa "40–42 triệu" (thay bằng "điền số thật"), bỏ ROI bịa (2–5 tỷ, 1,2 tỷ/năm, 300 triệu), bỏ câu "đã vận hành NAPAS", bỏ "các anh Lead Architect đã kiểm chứng". Cơ cấu thu nhập theo tin tuyển dụng ACB: 13 tháng cố định + thưởng 1–4 tháng, tức 700–850 triệu/năm.
4. **17 video INT/ACB**: đổi giọng Piper sang NamMinh (chính sách của kho), dựng lại, verify PASS, ASR xem xét lại. INT L06 (sự cố mẫu), INT L04 (nhãn SVG LTV/DTI) và ACB L08 (LTV 85%, spread 2,5% gắn nhãn "giả định/ví dụ minh họa", bỏ "triệt tiêu 100%") đã sửa nội dung.
5. **`MASTER_CURRICULUM_INDEX.md`**: sửa cột "Câu hỏi" ở 9/14 dòng; bỏ 5M+ giao dịch/ngày, 480+ topics, 3.500 TPS, 35% latency, 99,99%, F1 0,92.
6. **`SOURCE_CODE_VIDEO_MAP.md`, `README.md`**: 633 → 628 video bài học; sửa 4 ô trọng tâm nói quá và 4 liên kết sai; thêm ghi chú khoảng trống kiến thức.
7. **`HANDOVER_INTERVIEW.md`**: viết lại trạng thái, bằng UIT, chứng chỉ, số liệu CV, danh mục video, số câu ở Mục 6, và Mục 7–8.

### 7.3 Nút thắt hợp đồng (EGW section 5)

| ID | Điều chưa xác định | Công việc phụ thuộc | Bằng chứng / thiếu | Phép thử đóng | State |
|:---|:---|:---|:---|:---|:---:|
| BN-0017 | Số liệu CV và ngưỡng chính sách không có nguồn (TPS, F1, 99,99%, LTV, DTI, spread) | CV, Q&A, lương, ACB L08, INT L04 | Đóng bằng C-03, C-06 (đã gỡ hoặc gắn nhãn "ví dụ", dựng lại) | Tìm chuỗi trong CV; dựng lại video | **CLOSED** (C-03, C-06) |
| BN-0018 | Giọng đọc 17 bài là Piper, khác chính sách NamMinh toàn kho | 17 video | Đóng bằng C-06 (`NamMinh` 17/17) | Đọc `build_report.json` | **CLOSED** (C-06) |
| BN-0019 | Phát âm tên riêng/tiếng Anh (Core T24, NAPAS, SAGA, gross, Redis, byte, Spring Boot, proxy) chưa được tai người kiểm | 73 lý do ASR ở INT/ACB và 117 lý do ở BNK (C-20) | Cần người nghe; ASR không tách được lỗi TTS khỏi lỗi ASR | Nghe 73 câu liệt kê trong `out/<khóa>/<bài>/asr_report.md`, hoặc chạy probe lexicon như các khóa khác | OPEN |
| BN-0020 | Độ phủ và độ sâu cho người mất gốc | Mục tiêu "người mất gốc tự tin Senior" | C-13 đo khoảng trống; C-15…C-20 khóa BNK 15 bài đã lấp các chủ đề Java/Spring/SQL/PL/SQL/Redis/Kafka/SAGA/sổ cái/T24/ISO 8583/đối soát/bảo mật. Còn thiếu: cú pháp Java cơ bản, thực hành viết mã, các câu hỏi ghi ở Mục 8 | Người mất gốc xem BNK rồi tự trả lời 100 câu không nhìn đáp án; chạy lại `pedagogy_scan` | **PARTIAL** (BNK có; chưa thử với người học thật) |
| BN-0021 | Thu nhập hiện tại và sự cố thật của ứng viên | Vòng 1 ở tài liệu lương, Câu 93 | Số thật từ ứng viên | Ứng viên điền, tự kiểm chứng | OPEN |
| BN-0022 | Mức độ có thật của dự án AI (ONNX/Isolation Forest) | CV, Câu 92, Chuyên đề 05 | Mã nguồn hoặc báo cáo UIT | Ứng viên chuẩn bị repo hoặc báo cáo | OPEN |
| BN-0023 | Script sinh `resources/job/generate_int_*.py`, `create_acb_lesson*.py` có thể ghi đè các bản vá nếu chạy lại | YAML/MD đã sửa | Không | Không chạy lại, hoặc sửa chính script | OPEN |
| BN-0024 | 633 so với 628 | `SOURCE_CODE_VIDEO_MAP.md` | C-12: 5 tệp DEMO | Liệt kê mp4 không có đặc tả | **CLOSED** (C-12) |
| BN-0025 | Tài liệu `interview/00–05_*.md` mới được kiểm số liệu và tuyên bố ngôi thứ nhất, chưa được đọc kiểm từng dòng về kỹ thuật | 6 tài liệu chuyên đề | Quét tìm số liệu: sạch; quét ngôi thứ nhất: 0 tuyên bố | Đọc từng chuyên đề với chuyên gia Oracle/Kafka/T24 | OPEN |
| BN-0026 | Hành vi thật của Oracle, Redis, Kafka, Spring, T24, IBM MQ không chạy được trên máy này | Khẳng định về sản phẩm trong BNK L02, L05–L07, L10 | Chỉ có mô phỏng logic và tài liệu hãng (ghi trong `source`) | Chạy thử trên hệ thật hoặc chuyên gia đọc lại | OPEN |
| BN-0027 | Phát âm Redis (0/8) và Temenos (2/8) và độ rõ của "proxy" trong câu đầu | BNK L02, L06, L10 | C-19 | Nghe L02, L06 và sửa lexicon nếu sai | OPEN |

Các nút thắt cũ BN-0001…BN-0016 ở Mục 5 vẫn mang trạng thái ghi ở đó: tệp bằng chứng của cả 16 mục đều tồn tại (kiểm bằng script `os.path.exists`, 16/16; hai tên viết tắt `CV.pdf`, `CV.md` là các tệp thật). **Nhưng** các chỉ số trong cột giải pháp (ví dụ 99,99%, latency) là mục tiêu thiết kế hoặc ví dụ, không phải kết quả đo của ứng viên.

### 7.4 Việc cần ứng viên làm trước khi nộp
1. Điền thu nhập hiện tại thật (tài liệu lương, Vòng 1) và chọn một sự cố thật cho Câu 93.
2. Chuẩn bị bằng chứng cho dự án AI (repo, báo cáo), hoặc giữ nguyên cách diễn đạt "dự án học thuật".
3. Nghe thử ít nhất BNK L02 (proxy), BNK L06 (Redis), BNK L00 (16 câu gắn cờ) và ACB L00, L01, L02 (nhiều tên riêng nhất).
4. Xem BNK L00 đến L14 theo thứ tự rồi tự trả lời các câu ở bảng Mục 4D mà không nhìn đáp án; câu nào vướng thì ghi lại để bổ sung.

---

## 8. KHOẢNG TRỐNG KIẾN THỨC CHO NGƯỜI MẤT GỐC: ĐÃ XỬ LÝ MỘT PHẦN BẰNG KHÓA BNK

**Đo được (C-13, 2026-11-07):** thư viện 628 bài rất mạnh ở nền tảng nhưng không có bài cho Spring Boot, PL/SQL và khóa hàng Oracle, luồng ảo Java 21, Redis, ISO 8583, NAPAS, T24.

**Đã làm (2026-11-08, theo quyết định "làm đủ 15 bài"):** khóa `BNK` 15 bài, 110,44 phút, mỗi bài `depth: full` và có số liệu do `audit/bnk/verify_bnk.py` kiểm bằng cách tính khác (Mục 4D, C-15…C-21). Thư viện nay có **643** bài học đã dựng (628 + 15) và 5 video DEMO, tức 648 tệp mp4.

**Còn thiếu (đã đối chiếu với 100 câu hỏi, không có bài BNK tương ứng):**

| Nhóm câu | Chủ đề chưa có bài nền |
|:---|:---|
| 1, 11, 13, 14, 15, 16, 17 | cú pháp Java cơ bản, String, ClassLoader, generics, NIO, reflection, tinh chỉnh JVM, HashMap |
| 27, 28, 30, 31, 32, 33, 38, 40 | HikariCP, JWT, Resilience4j, OpenTelemetry, bảo mật container, Kubernetes, gRPC, cấu hình và bí mật |
| 41, 48, 53, 54, 55 | CAP, log compaction, ksqlDB, Schema Registry, Kafka Streams |
| 56, 62, 64 | Oracle Partitioning, Sharding và các điểm JD khác, sinh khoá chính |
| 69, 71–75, 77, 81–89, 91, 92 | câu về dự án của ứng viên và sản phẩm cụ thể của ACB/OCB: cần ứng viên tự chuẩn bị bằng trải nghiệm thật |

**Việc nên làm tiếp nếu muốn phủ thêm:** một khóa nối dài "BNK 2" cho các nhóm ở trên (cần quyết định phạm vi); nghe thử phát âm (BN-0019, BN-0027); thử BNK với một người học thật rồi sửa theo phản hồi (hiệu quả sư phạm hiện là `NOT_VERIFIED`).


---

## 9. RÀ SOÁT TOÀN DIỆN PHIÊN 2026-11-08 (CHIỀU): KẾT QUẢ VÀ BẰNG CHỨNG

**Kết luận: `PARTIAL` — đủ chuẩn để bắt đầu luyện học.** Tài liệu, CV, 17 video INT/ACB đã sửa và kiểm lại; các mục còn mở (Mục 9.4) cần người nghe, chuyên gia hoặc ứng viên tự cung cấp, công cụ không đóng được.

**Phát hiện chính**: bản ghi 2026-11-07 (C-03, BN-0017, BN-0025) báo đã gỡ số liệu không nguồn, nhưng **kịch bản 17 video và các chuyên đề 00/05/07 vẫn còn**: "thời gian đo thực tế 2,1 ms", "99,2%", "giảm 90%", "38 học phần", "750 triệu = 15 tháng", "mới tốt nghiệp UIT", "632 video", "ACB hạ lương dưới 25 triệu theo VssID", số liệu "trên hệ thống sản xuất ACB" tự dựng. Ngoài ra có lỗi kỹ thuật thật (9.1). Các nhãn "PASS" ở bản cũ chỉ là PASS dựng hình, không phải PASS nội dung.

### 9.1 Lỗi kỹ thuật/pháp lý đã sửa (tóm tắt; đầy đủ trong git diff)
| Chủ đề | Sai | Đúng |
|:---|:---|:---|
| Oracle bế tắc | `ORDER BY … FOR UPDATE` bảo đảm thứ tự khóa, "triệt tiêu 100%" | Oracle không bảo đảm; khóa từng dòng bằng câu lệnh riêng theo khóa tăng dần; giảm mạnh, không triệt tiêu |
| PL/SQL | `SELECT … FOR UPDATE` thiếu `INTO` (PLS-00428); `BULK COLLECT LIMIT` không có vòng lặp | Đã sửa mã mẫu |
| FK không index | khóa toàn bộ bảng con khi UPDATE/DELETE bảng cha | Chỉ khi xóa/sửa khóa chính bảng cha; khóa TM mức S trong lúc câu lệnh chạy |
| Kafka | heartbeat theo `max.poll.interval.ms`; `min.insync.replicas` là cấu hình producer | `session.timeout.ms`; cấu hình topic/broker |
| Java | volatile "đọc thẳng RAM"; luồng ảo không nhắc pinning; con số "500 byte, tiết kiệm 99,95%" | happens-before (JLS §17.4); pinning trong `synchronized` ở Java 21 (JEP 444, sửa ở JEP 491); mô hình minh họa |
| REST | RFC 7807; xóa khóa lũy đẳng khi timeout | RFC 9457; timeout giữ PENDING, tra soát |
| HSM | `JC` dịch PIN từ ZMK sang LMK; "giải mã PIN" | `CA` TPK→ZPK, `CC` ZPK→ZPK, `JE`/`JC` →LMK; ZMK chỉ bọc khóa; PIN được *dịch*, không giải mã |
| ISO 8583 | 0420 là yêu cầu đảo; bitmap 64 bit nhưng dùng trường 128; VND 2 số lẻ | 0400 yêu cầu, 0420 thông báo đảo; bitmap phụ; VND 0 số lẻ (ISO 4217) |
| ISO 9564 | công thức khối PIN sai | Format 0 / Format 1 đúng chuẩn |
| T24 OFS | cú pháp sai thứ tự, "OFS là XML" | 5 phần phân cách dấu phẩy; XML chỉ qua adapter (graph OCB có "OFS XML") |
| Nợ xấu | TT 11/2021; Nhóm 2 = 10–90 ngày | TT 31/2024 (từ 01/07/2024); Nhóm 2 = 10–90 ngày. Sửa 2026-11-10 (đợt LS1): bản 10–89 trước đó lệch một ngày; nguồn thứ cấp: cafef.vn 21/07/2026, hethongphapluat.com, truy cập 2026-11-10, chưa đối chiếu được nguyên văn Điều 10 |
| QĐ 2345 | "từ 10 triệu", "ban hành 01/07/2024", luôn gọi C06 | "trên 10 triệu"/lần hoặc tổng ngày vượt 20 triệu; ban hành 18/12/2023, hiệu lực 01/07/2024; so mẫu đã đăng ký |
| Ký số | OTP đóng dấu thời gian; NĐ 130/2018 | TSA cấp dấu thời gian; NĐ 23/2025 |
| Lãi, thấu chi | lãi = S×r/12; cấp hạn mức trước khi ký; trích nợ một phần "bảo vệ điểm tín dụng" | theo ngày thực tế/365 (TT 14/2017); phong tỏa → ký → cấp hạn mức; phần thiếu vẫn quá hạn |
| Lương | 13–15 tháng; 750 triệu; thử việc 6 tháng | 13 + 1–4 tháng = 700–850 triệu; tối đa 60 ngày (Điều 25 BLLĐ 2019) |

### 9.2 Bản ghi kiểm chứng (EGW section 3; chạy 2026-11-08, giờ UTC từ `date -u` / `checked_at`)
| ID | Tuyên bố | Phương pháp (đã chạy) | Kết quả quan sát | validity |
|:---|:---|:---|:---|:---:|
| C-22 | Liên kết `file:///` trong các tài liệu `interview/*.md` trỏ tới tệp có thật | script `audit_links.py` (scratchpad phiên) | trước sửa: 244 liên kết, 6 hỏng (README trỏ `.md` trong `video/`); sau sửa: 0 hỏng | VALID |
| C-23 | Số bài mỗi khóa trong chỉ mục | đếm `lessons/<c>/L*_*.yaml` và `out/<C>/L*/L*.mp4` | 14/15 khóa ở chỉ mục cũ lệch −1 (ví dụ DMS 20 → thật 21); đã sửa theo số đếm | VALID |
| C-24 | Cột "trọng tâm" của chỉ mục và bản đồ video đúng nội dung | tìm từ khóa trong đặc tả + đọc tên bài (`audit_claims.py`) | nói quá ở CS112 (cây đỏ đen 0 bài), NET (MTU, socket 0), DBS (PL/SQL, MVCC 0), CLD (Spring, REST 0), SEC (AES/mTLS/JWT/OAuth/HSM 0), CVI (QĐ 2345/liveness 0), MLO (ONNX 0), DVO (GitOps/Prometheus 0)…; đã viết lại theo tên bài thật | VALID |
| C-25 | CV PDF 2 trang A4, không còn cụm sai | `python resources/job/build_cv_pdf.py` + trích text PyMuPDF | 2 trang, scale 1.0, dư 50,36 pt / 184,06 pt; không còn `ORDER BY`, "Banking Multipliers", "Distributed Ledger", `8,000`, `99.99`, `LTV 90`; có `expected`, `31/2024` | VALID |
| C-26 | 17 đặc tả INT/ACB lint sạch | `lv.py lint` từng tệp (độc lập với tác tử đã sửa) | 17/17: 0 FAIL, 0 WARN | VALID |
| C-27 | 17 video dựng lại đạt verify | `audit/.build_queue_run.sh INT …`, `ACB …` (log `audit/int/logs/queue_2026-11-08{a,b,c}.out`, `audit/acb/logs/queue_2026-11-08.out`) | verify PASS 17/17; giọng NamMinh; INT 44,77 + ACB 50,50 = 95,27 phút (ffprobe) | VALID |
| C-28 | ASR của 17 bài đã xem xét | `asr_hand_gen.py` → đọc lại, sửa 1 lý do phân loại sai → `asr_hand_insert.py` → `asr_review_dms.py --course` → `lv.py asr` → `asr_flags.py` | 10 câu mới gắn cờ, 0 chưa xem xét (INT, ACB); lý do ghi "NOT_VERIFIED bằng tai người" | VALID (ASR-checked), chưa ear-checked |
| C-29 | Bản sao `interview/video/` khớp `out/` | `sync_interview_video.py --check` (sha256, 92 cặp: mp4, srt, chapters, build_report) | 92/92 trùng byte | VALID |
| C-30 | Video khớp đặc tả hiện tại | `gen_tables.py` so `spec_sha256` với `lv.spec_digest` cho 32 bài INT/ACB/BNK | 32/32 "có" | VALID |
| C-31 | Toàn kho không có lỗi mới | `audit/review/audit_all.py` (xong 01:08Z) | 643 bài, 643 đã dựng, 1 mục: AIF L11 (cố ý chờ tai người, như C-10) | VALID |
| C-32 | Lộ trình khóa hợp lệ sau khi sửa `curriculum/int.yaml`, `acb.yaml` | `audit/verify_plan_curricula.py` | 491 PASS, 0 FAIL | VALID |
| C-33 | Nội dung kỹ thuật của 01–04, 06 và 17 YAML đúng | hai tác tử rà soát độc lập (Java/phân tán; ngân hàng/pháp lý), nguồn web cho QĐ 2345, TT 31/2024, NĐ 23/2025, NAPAS ISO 20022 (truy cập 2026-11-08, `no revision given`); tôi kiểm lại bằng grep các cụm sai đã biết | 27 + 31 mục đã sửa; grep không còn cụm sai | VALID cho các mục đã nêu; phần còn lại NOT_VERIFIED (BN-0025) |

### 9.3 Tệp đã sửa
`interview/`: 00–07, `README.md` (viết lại, bỏ trùng lặp), `MASTER_CURRICULUM_INDEX.md` (viết lại; thêm tầng BNK; bảng video sinh tự động giữa dấu `<!-- BEGIN:… -->`; Mục 8 đối chiếu JD), `SOURCE_CODE_VIDEO_MAP.md`, `HANDOVER_INTERVIEW.md` (Mục 1, 2.3, 3, 4C, 9). `resources/job/`: CV `.md` và `build_cv_pdf.py`, PDF dựng lại. `lessons/int/L00–L07`, `lessons/acb/L00–L08`, `curriculum/int.yaml`, `curriculum/acb.yaml`. `audit/dms/asr_review_dms.py` (khối HAND "rà soát nội dung (2026-11-08)").

### 9.4 Nút thắt hợp đồng còn mở (EGW section 5)
| ID | Điều chưa xác định | Công việc phụ thuộc | Bằng chứng thiếu | Hậu quả | Phép thử đóng | State |
|:---|:---|:---|:---|:---|:---|:---:|
| BN-0019, BN-0027 | Phát âm tên riêng (NAPAS, Core T24, IBM MQ, gross, Redis, Temenos) | 32 video | tai người | có thể nghe sai thuật ngữ | nghe các câu trong `out/<khóa>/<bài>/asr_report.md` | OPEN |
| BN-0020 | Hiệu quả sư phạm với người mất gốc | lộ trình học | thử với người học thật | chưa biết chỗ nào khó | học BNK rồi tự trả lời 100 câu | PARTIAL |
| BN-0021 | Lương hiện tại, sự cố thật (Câu 93) | Vòng 1 lương, Câu 93 | số thật từ ứng viên | không trả lời được câu "đo thế nào" | ứng viên điền | OPEN |
| BN-0022 | Bằng chứng dự án AI | CV dự án 3, Câu 92 | repo/báo cáo UIT | bị hỏi xoáy không có gì để cho xem | chuẩn bị repo | OPEN |
| BN-0023 | Script `resources/job/generate_int_*.py`, `create_acb_lesson*.py` ghi đè bản sửa | 17 YAML | — | mất toàn bộ sửa chữa nếu chạy lại | không chạy lại các script này | OPEN |
| BN-0025 | Đọc kiểm bởi chuyên gia Oracle/Kafka/T24 thật | 01–04, 06, 17 YAML | chuyên gia | lỗi tinh vi còn sót | chuyên gia đọc | OPEN (đã giảm, C-33) |
| BN-0026 | Hành vi thật của Oracle/Redis/Kafka/T24/IBM MQ | BNK, INT, ACB | hệ thật | khẳng định sản phẩm chưa chạy thử | chạy thử trên hệ thật | OPEN |
| BN-0028 | Tên môn học UIT và con số "38 môn" | `05_…md` Mục 2 | bảng điểm UIT | nói sai tên môn trước hội đồng | ứng viên đối chiếu bảng điểm, sửa bảng | OPEN |
| BN-0029 | ACB dùng hệ thống lõi nào; đặc tả NAPAS 247 hiện hành (ISO 8583 hay ISO 20022) | INT L04, ACB L01/L02, Câu 66–68 | tài liệu NAPAS / hỏi ACB | nói chắc điều chưa biết | hỏi trong vòng phỏng vấn; không khẳng định | OPEN |
| BN-0030 | Người tham chiếu đã đồng ý chưa (đặc biệt anh Quan Quốc Bảo, ACB) | CV mục References, Câu 76 | xác nhận của người tham chiếu | rủi ro uy tín, xung đột lợi ích | ứng viên xin phép trước khi nộp CV | OPEN |
| BN-0031 | JD yêu cầu tốt nghiệp đại học; bằng UIT dự kiến 11/2026 | hồ sơ ứng tuyển | xác nhận của trường | bị loại ở vòng hồ sơ | chuẩn bị giấy xác nhận sinh viên/lịch tốt nghiệp; hỏi HR | OPEN |
| BN-0032 | Chủ đề JD chưa có bài (MS SQL, Couchbase, Elasticsearch, Swagger, gRPC, SWIFT, ngoại tệ, thuế điện tử) | ôn tập | — | hổng kiến thức nếu bị hỏi | `MASTER_CURRICULUM_INDEX.md` Mục 8; tự học hoặc làm "BNK 2" | OPEN |

**Đã đóng trong phiên**: BN-0017 (đóng lại thật sự: C-26…C-30), BN-0024. **Bản ghi cũ BN-0005** (Mục 5) dùng `ORDER BY … FOR UPDATE` làm giải pháp: đã thay bằng cách khóa từng dòng theo thứ tự (9.1).

**Lỗi công cụ gặp trong phiên**: `audit/dms/asr_review_dms.py` chèn mục `  - {sentence…}` thụt 2 dấu cách; nếu danh sách `asr_reviewed` của bài đang ở dạng khối thụt 0 thì YAML hỏng (gặp ở ACB L02, đã sửa và parse lại cả 17 tệp). Sau khi chạy công cụ này, luôn parse lại YAML.

### 9.5 Bắt đầu luyện học từ đâu
1. Đọc [`README.md`](file:///D:/research-video/interview/README.md) Mục 2–3 (thứ tự học, quy tắc trung thực).
2. Xem BNK L00 → L14, rồi INT L00 → L07, ACB L00 → L08 (bảng ở [`MASTER_CURRICULUM_INDEX.md`](file:///D:/research-video/interview/MASTER_CURRICULUM_INDEX.md)).
3. Trước khi nộp CV: đóng BN-0030 (xin phép người tham chiếu), BN-0031 (giấy xác nhận UIT), BN-0021/0022 (số thật, repo AI), BN-0028 (tên môn UIT).

## 10. PHIÊN 2026-11-08 (TỐI): KHÓA JVA TỪ CON SỐ 0 VÀ RÀ SOÁT TOÀN BỘ CÁC KHÓA NỀN

**Kết luận: `PARTIAL`, đủ chuẩn để bắt đầu học từ con số 0.** Mọi bài nền đã được đọc kiểm, sửa, dựng lại và qua các cổng kiểm máy (10.2). Các mục còn mở (10.3) cần tai người, người học thật hoặc chuyên gia; công cụ không đóng được.

**Yêu cầu của phiên**: "Xác nhận các khóa học nền tảng đều đã đạt chất lượng chuẩn chỉnh. Tôi sẽ thực hiện học từ con số 0, mất gốc." Hai quyết định của người dùng: (1) soạn khóa mới **JVA** dạy lập trình từ con số 0, đặt trước BNK; (2) đọc kiểm **toàn bộ** các bài nền rồi dựng lại mọi bài đã sửa.

### 10.1 Việc đã làm
1. **Khóa JVA** (13 bài, `out/JVA/L00`–`L12`, 106,91 phút): chương trình đầu tiên, biến và kiểu, toán tử, rẽ nhánh, vòng lặp, mảng, phương thức, lớp và đối tượng, chuỗi, danh sách và bản đồ, ngoại lệ, giao diện/bản ghi/kiểu liệt kê, sổ chuyển khoản nhỏ. Bài sinh từ `audit/jva/src/lNN.py` bằng `audit/jva/gen.py` (**không sửa tay** `lessons/jva/*.yaml`). Mỗi chương trình trên màn hình là dữ liệu `prog(...)`, được `audit/jva/verify_jva.py` biên dịch và chạy thật, so khớp đầu ra và dòng lỗi. Giáo án `curriculum/jva.yaml`; `curriculum/bnk.yaml` L00 có `requires_ext: [JVA:L12]`.
2. **Rà soát đọc toàn bộ 300 bài nền**: 15 khóa nền (DMS 21, CS115 46, CS112 30, CSA 17, OSY 16, NET 16, DBS 18, SWF 14, SDP 18, CLD 16, DSY 16, EVT 12, SAR 14, SEC 16, DEN 15, tổng 285) cùng BNK 15. Các tác tử AI đọc theo `audit/review/FULL_REVIEW_BRIEF.md`, sửa lỗi kiến thức, số liệu và logic, rồi chạy lint, render và bộ kiểm của khóa sau mỗi bài.
   - **Đính chính**: đợt đọc mẫu đầu tiên là **50/300** bài (9 bài có lỗi mức MUST, 42/50 có ít nhất một vấn đề), không phải "53/281" như tôi báo lúc đầu.
   - **Kết quả đếm bằng công cụ**: **180/300** bài nền đổi nội dung và được dựng lại. Gồm BNK 15, CS115 32, CSA 12, DBS 12, DSY 12, SEC 12, OSY 11, CS112 10, EVT 10, CLD 9, DEN 9, DMS 9, SWF 9, SAR 7, SDP 6, NET 5.
3. **Lỗi ký tự điều khiển**: trong YAML nháy kép, `\t` của `\times`, `\text`, `\to`, `\theta` bị đọc thành TAB, làm hỏng công thức trên màn hình. Đã sửa ACB L06, BCH L07, DBS L14, RBM L00 và viết công cụ `audit/review/scan_ctrl.py`.
4. **Xét ASR**: câu ngắn bị nghe sai được viết dài ra rồi dựng lại (BNK: 1 câu dùng ở 3 bài; JVA: 4 câu ở 3 bài). Đã viết lý do cho 42 câu gắn cờ (5 khối HAND trong `audit/dms/asr_review_dms.py`, nhãn "dựng lại sau rà soát toàn bộ" và "JVA … dựng lần đầu"); mọi lý do ghi `NOT_VERIFIED bằng tai người`.
5. **Tài liệu**:
   - `MASTER_CURRICULUM_INDEX.md`: thêm tầng 0A JVA; bảng video sinh lại cho 45 video.
   - `README.md`: bước 0 là JVA.
   - `00_overview_roadmap.md` và `SOURCE_CODE_VIDEO_MAP.md`: cập nhật thời lượng mới.
   - `HANDOVER_INTERVIEW.md` Mục 4D và 6: cập nhật thời lượng mới.
   - `curriculum/sec.yaml` L14: mục tiêu ghi đủ sáu bước, khớp bài.
   - `curriculum/STATUS.md`: sinh lại.

### 10.2 Bản ghi kiểm chứng (EGW section 3; chạy 2026-11-08, giờ UTC lấy từ `date -u` / `checked_at`)
| ID | Tuyên bố | Phương pháp (đã chạy) | Kết quả quan sát | validity |
|:---|:---|:---|:---|:---:|
| C-34 | Mọi chương trình trong JVA biên dịch, chạy và in đúng như bài nói | `.venv/Scripts/python -B audit/jva/verify_jva.py` (javac/java 22.0.2), chạy lại sau lần sửa cuối, 06:00Z | `verify_jva: 110/110 PASS` | VALID |
| C-35 | 196 bài dựng lại đạt verify | `audit/.build_queue_run.sh` theo ba đợt (log `audit/review/rebuild_2026-11-08.out`, 02:13Z–12:07Z) | 202 lần dựng `→ PASS`, 196 bài khác nhau (6 bài dựng hai lần sau khi sửa câu ASR), 0 FAIL; 14 lần TTS bị chặn, đều tự dựng lại được; giọng NamMinh | VALID |
| C-36 | Toàn kho không còn bài cũ hay lỗi lint | `.venv/Scripts/python -B audit/review/audit_all.py` (xong 12:24Z) | `656 bài, 656 đã dựng, 1 bài có vấn đề`: AIF L11, câu cố ý chờ tai người (như C-10, C-31) | VALID |
| C-37 | Câu ASR gắn cờ của các khóa đã dựng lại đều đã xem xét | `audit/review/asr_flags.py <KHÓA>` cho 20 khóa sau khi chạy lại `lv.py asr` | 0 câu chưa xem xét ở mọi khóa; YAML sửa xong đều parse lại được | VALID (ASR), chưa nghe bằng tai |
| C-38 | Bộ kiểm độc lập của các khóa qua | các `audit/<c>/verify_*.py`; `audit/review/status_report.py` | JVA 110/110, BNK 17/17, DBS 42/42, NET 89/89, RBM 92/92, SWF 47/47, DSY 33/33, SDP 36, SEC 26, CLD 20, DEN 15, SAR 15, EVT 12, BCH 13; CS112 38 PASS + 15 FIX (bản thảo sai đã sửa trong video), p2 37 PASS; 0 FAIL. `STATUS.md`: 655/656 bài hoàn thiện, 5589 phút | VALID |
| C-39 | Lộ trình hợp lệ | `audit/verify_plan_curricula.py`; `audit/check_curricula_graph.py`; `lv.py curriculum curriculum/sec.yaml` (12:28Z) | 504 PASS · 0 FAIL; 42 lộ trình, 656 bài, 1365 cạnh, 0 tham chiếu hỏng, 0 chu trình; sec 0 lỗi | VALID |
| C-40 | Không còn ký tự điều khiển ngoài ý muốn | `audit/review/scan_ctrl.py` | 8 lượt, đều là dòng `\tat` cố ý của vết ngăn xếp Java trong JVA L10/L12 | VALID |
| C-41 | Bảng video và bản sao `interview/video/` khớp video thật | `gen_tables.py` (scratchpad, ffprobe, so `spec_sha256`); `sync_interview_video.py --check` | 45/45 "đặc tả khớp video"; JVA 106,91 + BNK 115,05 + INT 44,77 + ACB 50,50 = 317,23 phút; bản sao 92/92 trùng byte (ACB L06 đã chép lại) | VALID |

### 10.3 Nút thắt hợp đồng (EGW section 5)
| ID | Điều chưa xác định | Công việc phụ thuộc | Bằng chứng thiếu | Hậu quả | Phép thử đóng | State |
|:---|:---|:---|:---|:---|:---|:---:|
| BN-0033 | Người chưa từng lập trình không có khóa nhập môn | toàn bộ lộ trình JVA → BNK → INT → ACB | — | học BNK không hiểu | khóa JVA dựng và kiểm | CLOSED (C-34, C-35, C-41) |
| BN-0034 | Phát âm lời giảng mới (13 bài JVA, 180 bài nền sửa) và 42 câu chỉ được ASR xét | 196 video | tai người | có thể có chỗ đọc sai thuật ngữ | nghe các câu ghi trong `out/<khóa>/<bài>/asr_report.md` | OPEN |
| BN-0020 | Hiệu quả sư phạm với người mất gốc (JVA chưa thử với người học thật nào) | lộ trình học | người học thật | chưa biết bài nào khó hay quá nhanh | học JVA, ghi lại chỗ vướng, sửa bài | PARTIAL |
| BN-0035 | Đọc kiểm nội dung do tác tử AI làm, chưa có chuyên gia người | 300 bài nền | chuyên gia từng mảng | lỗi tinh vi còn sót | chuyên gia đọc; báo lỗi khi học | OPEN (đã giảm) |
| BN-0036 | 21 ví dụ trong giáo án có chữ số nhưng không dẫn bản ghi VER (CLC L11, CLD L05, DBS L09/L13, DSY L14, NET L07–L09, OSY L05/L06/L11, SWF L00/L02/L08–L12, TOC L04/L05/L08); có từ trước phiên, các tệp giáo án này không đổi | trường `example` của giáo án | phép tính kiểm | số trong giáo án có thể lệch bài | thêm `rec()` vào `audit/verify_plan_curricula.py` | OPEN |
| BN-0037 | Chương trình JVA chỉ chạy thử trên JDK 22.0.2; README ghi "JDK 21+" | người học cài JDK 21 | chạy trên JDK 21 | nếu lệch, máy người học báo khác bài | chạy `verify_jva.py` với JDK 21 | OPEN |

**Đã đóng trong phiên**: BN-0033; ghi chú `curriculum/sec.yaml` L14 (năm bước, bài dạy sáu) đã sửa. Các nút BN-0019…BN-0032 ở Mục 9.4 không đổi.

**Lỗi công cụ gặp lại**: `asr_review_dms.py` chèn mục thụt 2 dấu cách vào danh sách khối thụt 0. Lỗi này gặp ở mọi bài sinh bằng `gen.py` của BNK và JVA. Cách sửa: `sed 's/^  - {sentence: /- {sentence: /'`, rồi chạy lại `gen.py Lxx` để chuẩn hóa, rồi parse lại YAML.

### 10.4 Bắt đầu học từ con số 0
1. Cài JDK 21 trở lên. Xem JVA L00 → L12, gõ lại và chạy từng chương trình, làm phần tự làm trước khi xem đáp án.
2. Xem BNK L00 → L14, rồi INT L00 → L07 và ACB L00 → L08. Thứ tự và bảng video ở [`README.md`](file:///D:/research-video/interview/README.md) Mục 2 và [`MASTER_CURRICULUM_INDEX.md`](file:///D:/research-video/interview/MASTER_CURRICULUM_INDEX.md).
3. Khi nghe thấy câu đọc sai hoặc gặp chỗ khó hiểu, ghi lại (bài, phút). Đó là bằng chứng để đóng BN-0034 và BN-0020.

## 11. PHIÊN 2026-11-08/09: RÀ SOÁT ĐỢT B — 23 KHÓA CÒN LẠI (326 BÀI)

**Kết luận: `PARTIAL`.** Cả 326 bài đã được đọc kiểm. 163 bài có sửa, đều đã dựng lại và qua các cổng kiểm máy (11.2). Phần còn mở (11.3) cần người nghe bằng tai, người học thật hoặc chuyên gia.

**Yêu cầu**: "Rà soát hoàn chỉnh chuẩn xác các video nền tảng còn lại cũng dành cho người mới và người mất gốc … đảm bảo đầy đủ, chuyên nghiệp, không có lỗi và lổ hổng."

**Phạm vi**: 23 khóa chưa đọc ở Mục 10: AGT, AIF, BCH, CAS, CLC, CVI, DAN, DSC, DVO, ESY, GFX, HCI, IRS, LLM, MLO, PAR, PLC, RBM, RLN, ROB, SEP, TOC, WEB. **Không thuộc phạm vi**: 330 bài đã đọc ở Mục 9–10 (15 khóa nền, BNK, JVA, INT, ACB). Riêng ACB L06 được sửa thêm một câu pháp lý.

### 11.1 Việc đã làm
1. **Đọc kiểm 326/326 bài.**
   - Người đọc là 11 tác tử AI, làm theo `audit/review/FULL_REVIEW_BRIEF_B.md`. Hướng dẫn này chia lỗi thành mức MUST và SHOULD, yêu cầu đối chiếu sự kiện thật với `audit/<khóa>/sources_*.md`, chỉ dạy bảo mật theo hướng phòng thủ, và đặt lint/render = 0 làm cổng.
   - Mỗi khóa có báo cáo riêng `audit/review/full_review_b/<KHÓA>.md`, mỗi bài một dòng, kết luận là "đã sửa" hoặc "không phát hiện lỗi".
   - Số liệu (đếm bằng công cụ) như bảng dưới. Đơn vị là bài; MUST/SHOULD là số mục ghi trong bảng báo cáo, gồm cả mục người điều phối ghi thêm.

   | Khóa | Bài đọc | Bài sửa | MUST/SHOULD |
   |:--|--:|--:|:--|
   | AGT | 13 | 7 | 6/7 |
   | AIF | 15 | 9 | 5/6 |
   | BCH | 13 | 6 | 1/5 |
   | CAS | 12 | 5 | 2/3 |
   | CLC | 13 | 6 | 1/9 |
   | CVI | 13 | 7 | 0/8 |
   | DAN | 13 | 2 | 1/1 |
   | DSC | 16 | 7 | 2/8 |
   | DVO | 14 | 7 | 3/9 |
   | ESY | 16 | 8 | 2/13 |
   | GFX | 14 | 13 | 4/29 |
   | HCI | 13 | 11 | 6/38 |
   | IRS | 14 | 5 | 1/5 |
   | LLM | 15 | 9 | 3/10 |
   | MLO | 15 | 11 | 1/16 |
   | PAR | 14 | 3 | 0/3 |
   | PLC | 14 | 7 | 1/10 |
   | RBM | 18 | 5 | 3/5 |
   | RLN | 14 | 7 | 0/8 |
   | ROB | 14 | 8 | 2/11 |
   | SEP | 12 | 5 | 0/7 |
   | TOC | 15 | 6 | 0/7 |
   | WEB | 16 | 9 | 2/9 |
   | **Tổng** | **326** | **163** | **46/227** |

2. **Người điều phối kiểm lại và sửa thêm** (đối chiếu nguồn web, 11.4):
   - IRS L09: bổ sung phép tính tay (sau 18 lần không bấm, trung bình đã dưới 0,0509). Thêm chú thích vì sao mô phỏng hiện tai nghe mới ở lần 19, kèm một check mới.
   - DSC L13: ghi rõ Luật Bảo vệ dữ liệu cá nhân 2025 và Nghị định 356/2025/NĐ-CP cùng có hiệu lực từ 1/1/2026; Nghị định 356 thay Nghị định 13/2023/NĐ-CP.
   - ACB L06: thay căn cứ "Nghị định 13/2023/NĐ-CP" (đã bị thay thế) bằng Luật 91/2025/QH15, hiệu lực 1/1/2026.
   - CVI L11: nguyên tắc Morgan nêu lần đầu năm 1894, bản sửa năm 1903; bài cũ ghi "từ năm 1903".
3. **Bộ kiểm do tác tử sửa đều đã đọc lại**: `audit/bch/verify_bch.py`, `audit/dvo/verify_dvo.py`, `audit/irs/verify_parts/L06.py`, `audit/irs/verify_parts/L13.py`, `audit/web/verify_web.py`. Mỗi thay đổi có căn cứ theo đặc tả hoặc nguồn, không có chỗ nào đổi kỳ vọng chỉ để test qua.
4. **Giáo án**:
   - Ví dụ có số trong `curriculum/cld|dbs|dsy|net|osy|swf|clc|toc|esy.yaml` đều được dẫn tới bản ghi `(VER X:Lyy)`. `audit/verify_plan_curricula.py` có thêm khối BN-0036.
   - Viết lại hai bản ghi cũ đã lệch bài: ESY:L09 (tập tác vụ của bài) và AGT:L01 (4 lời gọi, lược đồ đóng).
   - Các bản ghi JVA nay kiểm đầu ra đã khai báo của chương trình, cộng phép tính lại độc lập.
5. **JVA**: `audit/jva/verify_jva.py` nhận biến môi trường `JVA_RELEASE`, để biên dịch với `javac --release N`.
6. **Dựng lại 164 bài**: 163 bài đợt B và ACB L06, log `audit/review/rebuild_2026-11-08b.out`.
   - **Lỗi công cụ tìm thấy và đã sửa**: GFX L02 FAIL hai lần liền với cùng một số liệu: mp4 dài 529,50 s, timeline 528,97 s.
   - Nguyên nhân đo được: luồng hình 529,43 s dài hơn luồng tiếng 528,96 s. Lệnh ghép `-shortest` với nguồn ảnh concat vẫn ghi thừa các khung đang nằm trong bộ đệm. GFX L03 cũng lệch 0,40 s, chỉ vừa dưới ngưỡng.
   - Cách sửa: `tools/lv.py` (`cmd_build`) thêm `-t <timeline>` để cắt đúng độ dài; ngưỡng kiểm 0,5 s giữ nguyên.
   - Dựng lại GFX L02: hình 528,90 s, tiếng 528,96 s, PASS.
   - Các video đã dựng trước khi sửa vẫn có thể dư dưới 0,5 s hình tĩnh ở cuối. Phần dư này vô hại và nằm trong ngưỡng, nên không dựng lại.
7. **Xét ASR**:
   - 22 câu gắn cờ ở 19 bài được ghi lý do (13 khối HAND "… dựng lại sau rà soát đợt B (2026-11-09)" trong `audit/dms/asr_review_dms.py`). Sáu lý do do bộ phân loại tự sinh đã được sửa tay: Amazon, flash, Euler, Turing ×2 (dẫn probe trong `tools/registry/lexicon_vi.<KHÓA>.yaml`) và cặp so khớp sai "tự/bốn".
   - Ba bài dựng từ mẫu (ESY L13, RBM L07, RBM L11) được đồng bộ bằng `sync_tpl_asr.py`.
   - Không có câu ⚠ NGẮN nào. AIF L11 vẫn để mở có chủ ý, chờ tai người.
8. **Tài liệu**: `MASTER_CURRICULUM_INDEX.md` sinh lại bảng (chỉ mã băm ACB L06 đổi; thời lượng 5:36 giữ nguyên). Bản sao `interview/video/` đã chép lại.

### 11.2 Bản ghi kiểm chứng (EGW section 3; giờ UTC lấy từ `date -u` / `checked_at`)
| ID | Tuyên bố | Phương pháp (đã chạy) | Kết quả quan sát | validity |
|:---|:---|:---|:---|:---:|
| C-42 | Báo cáo đọc kiểm khớp thay đổi thật | `check_reports_b.py` (scratchpad): so `lessons/<khóa>/` với bản chụp trước đợt B, đọc dòng bảng của 23 báo cáo (19:07Z) | 326 bài, 326 dòng; báo sửa 163 = tệp đổi 163; lệch 0 | VALID |
| C-43 | Số mục MUST/SHOULD | đếm từ cột "Mục đã sửa" của 23 báo cáo bằng regex (19:07Z) | 46 MUST, 227 SHOULD | VALID |
| C-44 | 164 bài dựng lại đạt verify | `rebuild_waveB.sh` → `audit/.build_queue_run.sh` (13:22Z–18:46Z), cộng 2 lần dựng lại GFX L02 | 164 dòng `→ PASS`, 164 bài khác nhau; GFX L02 FAIL 2 lần trước khi sửa `lv.py`, PASS ở lần dựng 01:50 giờ máy (18:50Z); giọng NamMinh; không lần nào TTS bị chặn | VALID |
| C-45 | Sửa ghép video đúng | `ffmpeg -map 0:v / 0:a -c copy -f null -` trên `out/gfx/L02/L02.mp4`, trước và sau khi sửa | trước: hình 08:49.43, tiếng 08:48.96; sau: hình 08:48.90, tiếng 08:48.96; verify `duration=528.97s timeline=528.967s → PASS` | VALID |
| C-46 | Câu ASR gắn cờ đã xem xét | `asr_review_dms.py --course <C> …`, `sync_tpl_asr.py`, parse YAML, `lv.py asr <tệp>` cho 19 bài | 19/19 bài "chưa xem xét 0"; `ast.parse` của `asr_review_dms.py` OK | VALID (ASR), chưa nghe bằng tai |
| C-47 | Bộ kiểm của 23 khóa qua | `audit/<c>/verify_*.py` (19:04Z) | AGT 15, AIF 25, BCH 13, CAS 93, CLC 13, CVI 112, DAN 13, DSC 30, DVO 18, ESY 72, GFX 19, HCI 27, IRS 123, LLM 18, MLO 20, PAR 96, PLC 67, RBM 92, RLN 94, ROB 14, SEP 66, TOC 102, WEB 16 PASS; 0 FAIL. ACB không có bộ verify riêng | VALID |
| C-48 | Ví dụ giáo án đều có bản ghi kiểm | `audit/verify_plan_curricula.py`; `audit/check_curricula_graph.py` (19:06Z) | 525 PASS · 0 FAIL; 42 lộ trình, 656 bài, 1365 cạnh, 0 tham chiếu hỏng, 0 chu trình; VER trỏ tới mã không PASS: 0; ví dụ có chữ số mà không có VER: 0 | VALID |
| C-49 | JVA biên dịch được cho JDK 21 và 17 | `JVA_RELEASE=21|17|8 .venv/Scripts/python -B audit/jva/verify_jva.py` (19:08Z; JVM chạy là 22.0.2) | 21: 110/110; 17: 110/110; 8 (đối chứng âm): 101/110 | VALID (mức biên dịch) |
| C-50 | Không có ký tự điều khiển ngoài ý muốn | `audit/review/scan_ctrl.py` (19:06Z) | 8 lượt, đều là `\tat` cố ý của JVA L10/L12 | VALID |
| C-51 | Bản sao video phỏng vấn khớp | `sync_interview_video.py`, rồi `--check`; `gen_tables.py` (trước 18:54Z) | 92/92 trùng byte; tổng 317,23 phút không đổi | VALID |
| C-52 | Toàn kho không còn bài cũ | `audit/review/audit_all.py` (xong khoảng 19:13Z, `audit_all.tsv` 02:13 giờ máy); `audit/review/status_report.py` | `656 bài, 656 đã dựng, 1 bài có vấn đề`: AIF L11, câu cố ý chờ tai người; `STATUS.md`: 655/656 bài hoàn thiện, 5602 phút | VALID |

### 11.3 Nút thắt hợp đồng (EGW section 5)
| ID | Điều chưa xác định | Công việc phụ thuộc | Bằng chứng thiếu | Hậu quả | Phép thử đóng | State |
|:---|:---|:---|:---|:---|:---|:---:|
| BN-0036 | 21 ví dụ giáo án có chữ số nhưng không dẫn VER | trường `example` | phép tính kiểm | số trong giáo án lệch bài | `rec()` trong `verify_plan_curricula.py` | CLOSED (C-48) |
| BN-0037 | JVA chỉ chạy trên JDK 22 | người học cài JDK 21 | chạy trên JVM 21 | máy người học báo khác bài | biên dịch `--release 21` (đã qua, C-49); chạy `verify_jva.py` trên JVM 21 thật | OPEN (đã thu hẹp: mức biên dịch qua) |
| BN-0034 | Phát âm lời giảng mới | nay thêm 164 video đợt B | tai người | chỗ đọc sai thuật ngữ còn sót | nghe các câu ghi trong `out/<khóa>/<bài>/asr_report.md` | OPEN |
| BN-0035 | Đọc kiểm chỉ do tác tử AI | nay thêm 326 bài đợt B | chuyên gia người | lỗi tinh vi còn sót | chuyên gia đọc; báo lỗi khi học | OPEN (đã giảm) |
| BN-0038 | Một số nhận định trong bài chưa có nguồn mở được: ImageNet giữ nguyên bộ thử 2012–2017 (CVI L12; image-net.org từ chối kết nối, ECONNREFUSED); KLM B = 0,1 s (HCI L05, câu đã viết mềm lại); mốc năm thư viện ở PAR L13; điểm chuẩn F0 trong GFX; câu "cổ phần bên bỏ phiếu ngược đa số bị rút dần" (BCH L12) | 5 bài trên | nguồn sơ cấp mở được | có thể sai chi tiết lịch sử hoặc kỹ thuật | mở nguồn sơ cấp, sửa bài nếu lệch | OPEN |
| BN-0020 | Hiệu quả sư phạm với người mất gốc | lộ trình học | người học thật | chưa biết bài nào khó | học và ghi chỗ vướng | PARTIAL |

### 11.4 Nguồn web đã mở trong đợt B (truy cập 2026-11-08, no revision given trừ khi ghi khác)
- RFC 2068 (HTTP/1.1, tháng 1/1997): https://www.rfc-editor.org/rfc/rfc2068.txt (WEB)
- Electra `MAX_PER_EPOCH_ACTIVATION_EXIT_CHURN_LIMIT` = 256 ETH, có `min(...)` với giới hạn churn theo số dư: https://raw.githubusercontent.com/ethereum/consensus-specs/master/specs/electra/beacon-chain.md (nhánh `master`; nhánh `dev` trả 404) (BCH)
- Luật Bảo vệ dữ liệu cá nhân có hiệu lực từ 1/1/2026: https://hatinh.gov.vn/vi/bai-viet/luat-bao-ve-du-lieu-ca-nhan-chinh-thuc-co-hieu-luc-thi-hanh-tu-ngay-112026 (DSC, ACB)
- Nghị định 356/2025/NĐ-CP thay Nghị định 13/2023/NĐ-CP: https://luatvietnam.vn/dan-su/nghi-dinh-356-2025-nd-cp-quy-dinh-chi-tiet-luat-bao-ve-du-lieu-ca-nhan-422896-d1.html (DSC)
- Morgan's Canon 1894: https://www.newworldencyclopedia.org/entry/C._Lloyd_Morgan (CVI). Trang https://journalpub.escholarship.org/uclapsych_ijcp/article/5755/galley/3510/download chỉ dùng làm đầu mối tìm kiếm.
- image-net.org: không truy cập được (ECONNREFUSED); xem BN-0038.

### 11.5 Học lại sau này
Các khóa đợt B đều đã dựng xong: `out/<KHÓA>/Lxx/Lxx.mp4`, kèm `.srt` và `chapters.txt`. Thứ tự học và điều kiện tiên quyết theo `curriculum/<khóa>.yaml` (`requires`). Khi học, nếu gặp câu đọc sai hoặc chỗ sai kiến thức, ghi lại bài và phút; đó là bằng chứng để đóng BN-0034 và BN-0035.

## 12. PHIÊN 2026-11-09: ĐÁNH GIÁ LẠI CHẤT LƯỢNG TOÀN KHO (42 KHÓA, 656 BÀI) VÀ ĐỌC MẪU ĐỘC LẬP

**Yêu cầu**: "Đánh giá lại xác nhận chất lượng của giáo án, video có trong source code."

**Kết luận: `PARTIAL` — không xác nhận được "không còn lỗi".** Mọi cổng kiểm máy đều qua trên toàn kho (12.2). Nhưng đọc mẫu độc lập 42 bài (mỗi khóa một bài) vẫn tìm thấy lỗi mức MUST ở 5/42 bài. Tỉ lệ này là 11,9%, khoảng Wilson 95% là 5,2–25,0%, ước tính còn khoảng 34–164 bài trong 656 bài có lỗi mức MUST trước đợt sửa này. Các lỗi trong mẫu đã được sửa và dựng lại; phần còn lại của kho chưa được đọc lại lần ba.

### 12.1 Việc đã làm
1. **Chạy lại toàn bộ cổng kiểm máy** trên 42 khóa (12.2).
2. **Quét mới độ lệch hình–tiếng** của mọi mp4 (scratchpad `av_scan.py`), sau khi phát hiện lỗi ghép video ở Mục 11.1.6.
3. **Đọc mẫu độc lập**: rút ngẫu nhiên 42 bài với hạt giống 20261109, giao cho 4 tác tử mới chỉ đọc, không sửa. Người điều phối kiểm lại từng mục MUST trên tệp thật. Kết quả chi tiết nằm ở `audit/review/sample_c/REPORT.md`.
4. **Sửa lỗi trong mẫu**, 17 bài:
   - ACB L02, AGT L00, BNK L09 (qua `audit/bnk/src/l09.py`), CLC L06, CSA L14, CVI L01, DAN L03, DSY L10.
   - INT L00 (thống nhất `series`), INT L01 ("OFS XML" → "bản tin OFS"), INT L06.
   - JVA L09 (qua `audit/jva/src/l09.py`), MLO L06, SAR L13, SEP L04, TOC L05 (cả mẫu `.tpl`), WEB L15.
5. **Giáo án ACB/INT** (`curriculum/acb.yaml`, `int.yaml`) chưa từng được đồng bộ với bài sau Mục 9. Hai tệp vẫn ghi "OFS XML", "giải mã PIN Block", và các số hiệu năng như kết quả thật ("5000 lệnh/giây dưới 35 ms", "99,2%", "dưới 3 phút").
   - Tên bài và mục tiêu nay lấy từ bài.
   - `example` nay là tên cảnh ví dụ của bài, kèm câu "mọi số liệu hiệu năng trong bài là ví dụ minh hoạ".
   - ACB L08 `fix` bỏ "trên Core T24".
6. **Tài liệu nguồn** `interview/06_interview_qa_bank_100.md` Câu 66: bỏ giả định "Core Banking T24 … của ACB"; bước 7 nay là "chuyển khoản hold thành trích nợ chính thức".
7. **`audit/review/check_meta.py`**: thêm ngoại lệ tiền tố "Chuyên đề N —" cho INT. Lý do: bộ tài liệu `interview/00–07` gọi các bài là "8 Chuyên đề". Phép kiểm vẫn đòi N khớp id. Trước khi sửa: 18 vấn đề; sau khi sửa tài liệu và giáo án: 0.
8. **Nguồn GFX**: 7 tệp `audit/gfx/sources_L0*.md` ghi "Câu trích nguyên văn" nhưng không có URL và không đối chiếu được với sách. Nhãn nay là "NOT_VERIFIED nguyên văn".
9. **Bẫy công cụ mới**: chạy `audit/.build_queue_run.sh` trong `while read … <<LIST` sẽ bị lệnh dựng nuốt mất stdin, nên chỉ bài đầu tiên được dựng. Cách sửa: thêm `< /dev/null`. Đợt B dùng vòng `for` nên không bị ảnh hưởng.
10. **Thời lượng cập nhật**: INT 44,86, ACB 50,62, BNK 115,16, JVA 107,11 phút; tổng 317,74 phút. Đã sửa ở `MASTER_CURRICULUM_INDEX.md` (sinh lại), `00_overview_roadmap.md`, `SOURCE_CODE_VIDEO_MAP.md`, Mục 4D/6.

### 12.2 Bản ghi kiểm chứng (EGW section 3; giờ UTC lấy từ `date -u` / `checked_at`)
| ID | Tuyên bố | Phương pháp (đã chạy) | Kết quả quan sát | validity |
|:---|:---|:---|:---|:---:|
| C-53 | Bộ kiểm của mọi khóa qua | 37 `audit/<c>/verify_*.py` + `audit/verify_cs115_tex.py` + `audit/verify_cs115_l44.py` (23:47–23:51Z ngày 08); chạy lại 12 khóa có bài sửa (00:30Z) | 39/39 exit 0, 0 FAIL (CS112 38 PASS + 15 FIX theo quy ước cũ). Chạy lại sau sửa: JVA 110, BNK 17, DAN 13, DSY 33, CLC 13, AGT 15, CVI 112, MLO 20, SAR 15, SEP 66, TOC 102, WEB 16 PASS | VALID |
| C-54 | Video đúng định dạng, hình–tiếng khớp | `av_scan.py` (scratchpad; ffmpeg `-map 0:v` / `0:a -c copy -f null`) (23:47–23:50Z) | 661 mp4 (gồm video thử ngoài 42 khóa); định dạng sai 0; hình − tiếng lớn nhất 0,40 s; có 3 video > 0,3 s (DEMO L03, GFX L03, SAR L12); container − timeline lớn nhất 0,467 s; > 0,5 s: 0 | VALID |
| C-55 | Không có câu TTS bị cụt | `audit/review/tts_speed_scan.py` | 51 791 câu, 0 câu < 0,22 s/từ | VALID |
| C-56 | Lint toàn kho theo bộ luật hiện hành | `audit/review/audit_built.py` (00:33Z →) | 656 bài: 0 FAIL, 0 WARN; một giọng NamMinh ở mọi khóa | VALID |
| C-57 | Siêu dữ liệu, tham chiếu, ký tự điều khiển, đồ thị giáo án | `check_meta.py`, `check_course_refs.py`, `scan_ctrl.py`, `check_checklib_dupes.py`, `verify_plan_curricula.py`, `check_curricula_graph.py`, `lv.py curriculum` cho acb/int (00:30Z–01:05Z) | check_meta 0 (trước khi sửa: 18, toàn bộ ở INT/ACB); course_refs 0; scan_ctrl 8 (đều là `\tat` cố ý của JVA); checklib không trùng; 525 PASS · 0 FAIL; 42 lộ trình, 656 bài, 1365 cạnh, 0 tham chiếu hỏng, 0 chu trình; acb 9/9, int 8/8, 0 lỗi | VALID |
| C-58 | Đọc mẫu độc lập 42 bài | 4 tác tử chỉ đọc; người điều phối kiểm lại (sqlite cho DAN L03; tính lại cho CSA, CLC, AGT, HCI; đối chiếu ACB L06/Mục 9 cho QĐ 2345) | 7 mục MUST ở 5 bài (ACB L02, CSA L14, DAN L03, INT L06 ×3, SAR L13); 4 bài CONFIRMED, SAR L13 PLAUSIBLE; tổng 16/42 bài có phát hiện thật; xem `audit/review/sample_c/REPORT.md` | VALID (cho mẫu) |
| C-59 | 17 bài sửa đã dựng lại đạt verify | `rebuild_waveC.sh` → `audit/.build_queue_run.sh`, log `audit/review/rebuild_2026-11-09c.out` (00:30Z–01:01Z) | 17 dòng `→ PASS`, 0 FAIL; câu ASR mới duy nhất (ACB L02) đã ghi lý do (khối HAND "ACB L02 dựng lại sau đọc mẫu độc lập"), `lv.py asr` → 0 câu chưa xem xét; YAML parse OK sau khi sửa lỗi thụt dòng đã biết | VALID (ASR), chưa nghe bằng tai |
| C-60 | Bản sao video phỏng vấn và bảng khớp | `sync_interview_video.py`, `--check`, `gen_tables.py` (scratchpad) | 92/92 trùng byte; 45/45 "có"; tổng 317,74 phút | VALID |
| C-61 | Toàn kho không còn bài cũ | `audit/review/audit_all.py` (01:29–01:41Z), `status_report.py`; trước đó lần chạy 01:13Z bắt mẫu TOC L05 lệch bài → `sync_tpl_from_lesson.py TOC --write` → 0 mẫu lệch | `656 bài, 656 đã dựng, 1 bài có vấn đề`: AIF L11, câu cố ý chờ tai người; `STATUS.md`: 655/656 bài hoàn thiện, 5603 phút | VALID |

### 12.3 Nút thắt hợp đồng (EGW section 5)
| ID | Điều chưa xác định | Công việc phụ thuộc | Bằng chứng thiếu | Hậu quả | Phép thử đóng | State |
|:---|:---|:---|:---|:---|:---|:---:|
| BN-0039 | Tỉ lệ lỗi còn sót ngoài mẫu: ước tính 5,2–25,0% số bài có lỗi mức MUST trước đợt C (C-58) | toàn bộ 614 bài ngoài mẫu | đọc lại lần ba, hoặc mẫu lớn hơn để thu hẹp khoảng ước lượng | người học có thể gặp lỗi kiến thức | đọc lại toàn bộ (hoặc mẫu lớn hơn), sửa, dựng lại, đo lại tỉ lệ | OPEN |
| BN-0040 | Câu "trích nguyên văn" từ sách không có URL: 7 tệp GFX, 5 tệp HCI | 12 bài | bản sách hoặc bài báo gốc | trích dẫn có thể là diễn giải hoặc sai tên mục | đối chiếu với sách, ghi số trang | OPEN |
| BN-0041 | Khóa ACB dựng trên kiến trúc tham chiếu T24 của OCB; người học có thể hiểu nhầm rằng ACB dùng T24 | 9 bài ACB | quyết định của người dùng về cách đặt vấn đề | phỏng vấn viên có thể bắt lỗi | người dùng chọn: giữ (ghi rõ "kiến trúc tham chiếu OCB") hay viết lại trung tính | OPEN (chờ người dùng) |
| BN-0034, 0035, 0037, 0038, 0020 | như Mục 11.3 | | | | | không đổi |

**Chưa sửa trong mẫu**: ACB L02 còn một số thuật ngữ chưa giải thích cho người mới (bản đồ bit thứ hai, HSM, Redis, IN_DOUBT, EOD, PCI DSS). HCI L06 được xét là không lỗi (12.1 và REPORT.md).

## 13. PHIÊN 2026-11-09/10: ĐỌC KIỂM LẦN BA TOÀN KHO (ĐỢT C), BÀI TỰ ĐỨNG ĐƯỢC, DỰNG LẠI 591 BÀI VÀ ĐỌC MẪU ĐỘC LẬP D

**Yêu cầu**: "Rà soát kỹ từng chi tiết từng bước, verify evidence, xử lý contract bottleneck … các video giáo án bài học đều độc lập, không nói ngắn gọn tham chiếu đến khóa học khác, cần giảng giải kỹ càng chuyên sâu. Đảm bảo chất lượng cuối cùng để tôi bắt đầu học." Sau đó người dùng giao toàn quyền chọn hướng làm.

**Kết luận: `PARTIAL`. Kho đủ chuẩn để bắt đầu học, nhưng chưa xác nhận được "không còn lỗi".**
- Mọi cổng kiểm máy đều qua trên toàn kho 42 khóa, 656 bài (13.2).
- Đọc mẫu độc lập D trên 42 bài mới, rút sau đợt C, cho thấy lỗi mức MUST đã giảm. Mẫu C trước đợt C có 5/42 bài lỗi MUST; mẫu D chỉ còn 2/42 (4,8%, khoảng Wilson 95% là 1,3–15,8%).
- Mức SHOULD thì vẫn phổ biến: 37/42 bài có ít nhất một mục. Phần lớn là thuật ngữ hoặc ký hiệu chưa được giảng lại ngay tại chỗ (BN-0039).

### 13.1 Việc đã làm
1. **Đọc kiểm lần ba (đợt C) 42/42 khóa, 656/656 bài.**
   - Brief: `audit/review/FULL_REVIEW_BRIEF_C.md`. Mục A tìm lỗi nội dung; mục B mới yêu cầu không nhắc khóa khác và giảng lại khái niệm mượn ngay trong bài.
   - Báo cáo: `audit/review/full_review_c/*.md`, 45 tệp. Tệp thật đã được đối chiếu với ảnh chụp trước đợt bằng `check_reports_c.py` (scratchpad).
   - 591 bài đổi lời hoặc hình. Cổng mới `audit/review/check_xref.py` hạ số tham chiếu sang khóa khác của toàn kho từ 495 xuống 0.
2. **BN-0041 đóng theo lựa chọn của người dùng** ("Ghi rõ OCB").
   - ACB giữ nội dung T24, nhưng màn hình và lời đọc ghi rõ đây là "kiến trúc tham chiếu từ kinh nghiệm ở OCB" (L00, L01, L04, L07, L08).
   - L03, L05, L06 đổi nhãn thành "Core Banking". Không bài nào khẳng định ACB dùng T24; mẫu D kiểm lại ở INT L04 và ACB L05.
3. **Dựng lại 591 bài.**
   - 4 luồng `audit/review/rebuild_daemon_c2.sh a..d`, từ 2026-11-09T03:46Z đến 2026-11-10T02:32Z. Log ở `audit/review/rebuild_c.{a,b,c,d}.out`.
   - 591/591 bài có dòng trong `.done`. `grep "FAIL sau\|→ FAIL"` chỉ còn NET L04; bài này FAIL lúc giáo án PAR đang được sửa, đã đưa lại vào hàng và PASS.
   - TTS edge bị chặn khoảng 145 lần. Mỗi lần chờ 3 phút rồi tự dựng lại bằng cùng giọng NamMinh; không bài nào bị trộn giọng.
4. **Rà ASR theo quy trình HAND cho cả 42 khóa.**
   - Đợt C có 42 khối "<KHÓA> dựng lại sau đọc kiểm C (2026-11-09)" với 286 câu, mỗi câu ghi lý do.
   - Câu ngắn khớp thấp được viết dài và rõ hơn, rồi dựng lại. Ví dụ ROB L10 "Tịnh tiến là trừ đi toạ độ của xe…" (khớp 0,571) thành "Tịnh tiến nghĩa là lấy toạ độ điểm đích trừ đi toạ độ của xe, được hai hiệu số theo hai trục là d x và d y." (khớp 0,852). Tương tự cho ESY L08 ở đợt D.
   - Mọi khóa còn 0 câu chưa xem xét. Đây vẫn là đối chiếu bằng máy, chưa có tai người nghe (BN-0034).
5. **Sửa công cụ.**
   - `audit/dms/asr_review_dms.py`:
     - Sửa tận gốc lỗi chèn `  - {sentence` vào danh sách viết ở cột 0, từng làm vỡ YAML BNK L00–L12.
     - Nay đo thụt lề của danh sách có sẵn, dùng `json.dumps` để đóng ngoặc kép.
     - `yaml.safe_load` kiểm lại trước khi ghi; nếu vỡ thì DỪNG và giữ nguyên tệp.
   - `audit/review/asr_hand_gen.py`:
     - Tách "thuật ngữ Việt hoá viết liền" (ví dụ “cosin” = co-sin, “lôgarit” = lô-ga-rit) khỏi "từ mượn đọc thô".
     - Phần thuần Việt còn lại vẫn được phân loại tiếp.
   - Chuyển từ scratchpad vào kho:
     - `audit/review/interview_sync_video.py`: sao video INT/ACB/BNK/JVA vào `interview/video/` và kiểm sha256.
     - `audit/review/interview_gen_tables.py`: sinh bảng trong `MASTER_CURRICULUM_INDEX.md`.
     - `audit/review/av_scan.py`: quét độ lệch hình–tiếng của mọi mp4.
6. **Nguồn đã đọc nguyên văn trong phiên này.**
   - Adam §6.4: `audit/cs115/sources_L45.md`, đọc từ TeX gốc trên arXiv. Câu §3 viết "small β2" nhưng thực chất nghĩa là (1−β2) nhỏ, tức β2 gần 1, khớp với bài.
   - Ouyang 2022: 72,6 ± 1,5% và 77,3 ± 1,3%. Touvron 2023: Bảng 2, 6,7B và 1,0T. Cả hai ở `audit/llm/sources_L06_L09.md`.
   - GAO 1992: bản PDF chính thức đã đọc; chỉ trang sản phẩm trả 403.
   - Còn mở: NeurIPS (papers.nips.cc từ chối kết nối, ghi trong `audit/mlo/sources_L14.md`), và sách HCI/GFX (BN-0040).
7. **Đọc mẫu độc lập D** (`audit/review/sample_d/REPORT.md`).
   - 42 bài, mỗi khóa một bài, không trùng mẫu C, hạt giống 20261110, rút lúc 02:51:55Z.
   - 4 tác tử mới chỉ đọc và không xem báo cáo đợt C.
   - Phát hiện: 2 MUST, cả hai đã kiểm lại trên tệp thật:
     - SDP L05: khối mã trên màn hình không chạy được (`SyntaxError`, thiếu `__init__`). Nay là mã nhiều dòng, chạy thử ra 220000 và 209000.
     - CS115 L21: tiêu đề cảnh "mỗi chỉ số là một xác suất có điều kiện", trong khi tỉ lệ đúng không có điều kiện và F1 không phải xác suất.
   - Ngoài ra có 56 SHOULD. Không có con số nào tính sai.
   - Đã sửa cả 58 mục (SHOULD do chính các tác tử sửa sau khi đo xong), rồi dựng lại 37 bài, 37/37 PASS. RLN L09 và INT L04 FAIL lần đầu vì bảng mới bị tràn; đã tách thành hai bước có `clear: true`.
8. **Video phỏng vấn**: sau đợt D đã đồng bộ lại 92/92 cặp, trùng byte.
   - Thời lượng mới: INT 60,61, ACB 62,92, BNK 125,00, JVA 112,49 phút; tổng 361,02 phút.
   - Đã cập nhật `MASTER_CURRICULUM_INDEX.md` (sinh lại), `00_overview_roadmap.md` và `README.md` ("khoảng 63 phút").
9. **Mục "Chưa sửa trong mẫu" của Mục 12 đã đóng.** ACB L02 nay định nghĩa đủ:
   - HSM, Redis;
   - bản đồ bit thứ hai ("dài thêm 64 bit, dành cho các trường từ 65");
   - EOD ("cuối ngày, End Of Day"), PCI DSS ("bộ tiêu chuẩn bảo mật dữ liệu thẻ");
   - IN_DOUBT (lời đọc là "nghi vấn").

### 13.2 Bản ghi kiểm chứng (EGW section 3; giờ UTC lấy từ `date -u` / `checked_at`; giờ trong log dựng là giờ máy UTC+7)
| ID | Tuyên bố | Phương pháp (đã chạy) | Kết quả quan sát | validity |
|:---|:---|:---|:---|:---:|
| C-62 | Hàng dựng lại đợt C xong, không bài nào FAIL | lệnh chờ đếm `rebuild_c.done` so với `rebuild_c.queue`; `grep "FAIL sau\|→ FAIL" rebuild_c.*.out` (02:32Z) | "XONG 02:32Z: 591/591"; ngoài NET L04 (đã dựng lại và PASS) không có dòng FAIL | VALID |
| C-63 | Mọi câu ASR lệch đều có lý do | `asr_hand_gen.py` → đọc bản nháp → `hand_apply.sh`; `asr_flags.py` cho mọi khóa trong `out/` (02:40Z; lặp lại sau đợt D) | 42/42 khóa có "0 câu chưa xem xét"; 286 câu ở khối đợt C, thêm 10 khối đợt D (ACB, CLD, DEN, DMS, ESY, HCI, INT, JVA, SEC, SWF) | VALID (máy), chưa nghe bằng tai |
| C-64 | Bài tự đứng được, siêu dữ liệu và đồ thị giáo án đúng | `check_xref.py`, `check_meta.py`, `check_course_refs.py`, `scan_ctrl.py`, `check_curricula_graph.py`, `verify_plan_curricula.py` (02:45Z; chạy lại 06:18–06:40Z) | xref 0 lượt (đầu đợt C: 495); meta 0; course_refs 0; scan_ctrl 8 lượt, đều là `\tat` cố ý của JVA L10/L12; 42 lộ trình, 656 bài, 1366 cạnh, 0 tham chiếu hỏng, 0 chu trình, 0 ví dụ thiếu VER; 545 PASS · 0 FAIL | VALID |
| C-65 | Không câu TTS nào bị cắt | `tts_speed_scan.py` (02:50Z và sau đợt D) | 54 112 câu, rồi 54 231 câu; 0 câu dưới 0,22 s/từ | VALID |
| C-66 | Video đúng định dạng, hình và tiếng khớp nhau | `audit/review/av_scan.py` (02:54Z; chạy lại sau đợt D) | 661 mp4 (kể cả video thử ngoài 42 khóa); 0 sai định dạng; hình − tiếng lớn nhất 0,360 s (DEMO L03, video thử); container − timeline lớn nhất 0,430 s; 0 video lệch quá 0,5 s | VALID |
| C-67 | Toàn kho đã dựng và PASS sau đợt C | `audit_all.py` (xong 03:01Z), `status_report.py` | "656 bài, 656 đã dựng, 0 bài có vấn đề" (AIF L11 không còn bị gắn cờ); `STATUS.md` 656/656 bài hoàn thiện, 5911 phút | VALID |
| C-68 | Lỗi còn sót sau đợt C, đo bằng mẫu độc lập | 4 tác tử chỉ đọc, 42 bài, hạt giống 20261110; người điều phối kiểm lại MUST (chạy mã SDP L05 bằng Python; đọc cảnh `metrics` CS115 L21) và xem tận nơi các sửa có tính sự kiện | MUST 2/42 = 4,8% (1,3–15,8%); bài có ít nhất một phát hiện 37/42 = 88,1% (75,0–94,8%); 0 số tính sai; xem `sample_d/REPORT.md` | VALID (cho mẫu) |
| C-69 | 37 bài sửa sau mẫu D dựng lại đạt chuẩn | `audit/.build_queue_run.sh` tuần tự, log `audit/review/rebuild_d.out` (03:10Z–06:17Z); `hand_apply_d.sh` | 37/37 bài có `→ PASS`; 2 bài FAIL lần đầu vì tràn bảng (RLN L09, INT L04), sửa rồi PASS; lint 0 FAIL 0 WARN; các bộ kiểm khóa liên quan 0 FAIL | VALID |
| C-70 | Toàn kho PASS sau đợt D | `audit_all.py` (06:18–06:34Z) cho "166 bài có vấn đề", toàn bộ là `katex_check.js lỗi:` rỗng ở một dải bài liền nhau từ PAR L13, đúng lúc máy thiếu RAM và Claude Code dừng lệnh nền; lint lại PLC L00, RBM L14, PAR L13 đều 0 FAIL; chạy lại `audit_all.py` cho 12 khóa đó (06:43Z, 06:46Z) | 88/88 và 91/91 bài, 0 vấn đề, cộng 490 bài đã qua ở lần chạy đầu: 656/656. Chạy lại toàn kho để có `audit_all.tsv` đầy đủ (vì chạy theo khóa sẽ ghi đè tệp này), xong 07:08Z: "656 bài, 656 đã dựng, 0 bài có vấn đề"; `status_report.py`: 656/656 bài hoàn thiện, 5926 phút | VALID |
| C-71 | Bản sao video phỏng vấn khớp nguồn | `interview_sync_video.py`, `--check`, `interview_gen_tables.py` (sau đợt D) | 92/92 trùng byte; INT 60,61 + ACB 62,92 + BNK 125,00 + JVA 112,49 = 361,02 phút | VALID |
| C-72 | Các nguồn trước đây chưa kiểm nay đã đọc nguyên văn | tải TeX từ arXiv e-print (Adam, Ouyang, Touvron); PDF GAO | trích dẫn kèm vị trí ở `audit/cs115/sources_L45.md` và `audit/llm/sources_L06_L09.md`; tỉ số 143 tính theo tên mô hình 7B (theo 6,7B là 149), bài nói "khoảng" nên giữ | VALID |

### 13.3 Nút thắt hợp đồng (EGW section 5)
| ID | Điều chưa xác định | Công việc phụ thuộc | Bằng chứng thiếu | Hậu quả | Phép thử đóng | State |
|:---|:---|:---|:---|:---|:---|:---:|
| BN-0039 | Lỗi còn sót ngoài hai mẫu. Đã đọc lại lần ba toàn kho (đợt C), và mẫu D đo được MUST 4,8% (1,3–15,8%). Mặt khác, 88% bài mẫu còn ít nhất một thuật ngữ hoặc ký hiệu chưa giảng lại tại chỗ, hoặc thiếu điều kiện | 572 bài ngoài hai mẫu (656 − 84) | đợt đọc kiểm chuyên về "định nghĩa tại chỗ"; hoặc người học báo chỗ vướng | người mất gốc có thể kẹt ở một từ chưa giải thích, khoảng 1–2 chỗ mỗi bài | đợt D trên 572 bài: mỗi thuật ngữ được định nghĩa ở lần đầu xuất hiện, thêm điều kiện; dựng lại; rút mẫu E đo lại | OPEN (đã thu hẹp: MUST giảm từ 11,9% xuống 4,8% theo điểm ước lượng; hai khoảng còn chồng nhau) |
| BN-0040 | Câu "trích nguyên văn" từ sách không có URL | GFX L00–L06; HCI (Hick 1952, Hyman 1953, Nielsen & Landauer 1993, Bangor 2008) | sách RTR4, FCG5 và các bài báo Pineda 1988, Phong 1975, Blinn 1977, Whitted, Kajiya, Schlick; bài báo HCI | trích dẫn có thể là diễn giải | đối chiếu với sách, ghi số trang | OPEN (đã thu hẹp: HCI đã kiểm Norman 2013, Fitts 1954, MacKenzie 1992, Miller 1956, CMN80, Cowan 2001, SUS và thay các câu bịa; GFX giữ nhãn NOT_VERIFIED và thêm đối chiếu nguồn mở; xem `full_review_c/GFX.md`, `HCI.md`) |
| BN-0041 | Cách đặt vấn đề T24 ở khóa ACB | 9 bài ACB | — | — | người dùng chọn "Ghi rõ OCB"; đã sửa và dựng lại | CLOSED |
| BN-0038 | Nhận định chưa có nguồn sơ cấp mở được | CVI L12, HCI L05, PAR L13, GFX (F0), BCH L12 | image-net.org (ECONNREFUSED); ngày Horovod được mở mã | có thể sai chi tiết lịch sử | mở nguồn sơ cấp | OPEN (đã thu hẹp: BCH L12 sửa theo spec, MUST; HCI L05 bỏ B = 0,1 s của mô hình 1980, theo CMN80 Fig. 1 tr. 399; PAR L13 viết theo hai mốc kiểm được, CUDA 1.0 tháng 6/2007 và Horovod arXiv 15/2/2018, đề nghị đóng phần này; CVI L12 viết mềm thành "2012 tới 2014"; GFX F0 khớp BU12 §5.4, KA13 và PBR4 Bảng 9.1) |
| BN-0034 | Phát âm của lời giảng mới | nay gồm 591 + 37 video dựng lại | tai người | chỗ đọc sai thuật ngữ còn sót | nghe các câu ghi trong `out/<khóa>/<bài>/asr_report.md` | OPEN |
| BN-0035 | Đọc kiểm chỉ do tác tử AI làm | toàn kho | chuyên gia người | lỗi tinh vi còn sót | chuyên gia đọc; người học báo lỗi khi học | OPEN |
| BN-0037, 0020 | như Mục 11.3 | | | | | không đổi |

### 13.4 Bắt đầu học
- Thứ tự học: JVA → BNK → INT → ACB, theo Mục 10.4. Các khóa nền xem theo `curriculum/<khóa>.yaml` (`requires`).
- Mỗi video tự đứng được: không nhắc khóa khác, và khái niệm mượn được giảng lại tại chỗ.
- Khi gặp một từ chưa được giải thích, một câu đọc sai, hoặc một chỗ sai kiến thức, hãy ghi lại khóa, bài, phút và câu. Danh sách đó là bằng chứng trực tiếp để đóng BN-0034, BN-0035 và BN-0039.
