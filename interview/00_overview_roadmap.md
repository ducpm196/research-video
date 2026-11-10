# CHUYÊN ĐỀ 0: KHUNG NĂNG LỰC TOÀN DIỆN VÀ LỘ TRÌNH TỪ CON SỐ 0 ĐẾN SENIOR BANKING 50M GROSS

> **Mục tiêu**: Định vị lộ trình học tập thực chất, khoa học và chặt chẽ dành cho người mới, người mất gốc để từng bước làm chủ kiến trúc ngân hàng, vượt qua hội đồng phỏng vấn ACB và đàm phán thành công mức lương 50 triệu gross/tháng.  
> **Cảnh báo sư phạm**: Video là công cụ tổng kết và phản xạ kiến trúc; năng lực thực chiến đòi hỏi thực hành trực tiếp mã nguồn, hiểu sâu cơ chế cấp phát bộ nhớ máy tính và đối soát luồng tiền phân tán.

---

## 1. ĐÁNH GIÁ THỰC TẾ: LIỆU XEM VIDEO CÓ ĐỦ ĐỂ ĐẬU SENIOR BANKING 50M GROSS?

### 1.1. Câu trả lời trung thực và khách quan
**KHÔNG ĐỦ NẾU CHỈ XEM 9 VIDEO ACB (khoảng 63 phút).**  
Nếu một người mới bắt đầu hoặc người mất gốc chỉ xem 9 video tại `D:\research-video\out\ACB` (tổng 62,92 phút, đo bằng ffprobe 2026-11-10 sau lần dựng lại gần nhất) rồi bước vào phòng phỏng vấn, rủi ro trượt ở vòng kỹ thuật rất cao: các video này là bản tóm tắt, không phải bài nền. Người chưa từng lập trình học khóa **JVA** (13 bài, 106,91 phút) trước, rồi khóa **BNK** (15 bài, 115,05 phút), rồi mới xem INT/ACB.

### 1.2. Ba rào cản chí mạng khiến việc học vẹt video thất bại:
1. **Bản chất của chuỗi video ACB (L00 đến L08)**:
   - Đây là **Cheat-Sheet Tinh hoa & Đề cương Phản xạ Kiến trúc Cấp cao** (High-Level Architectural Briefing) dành cho kỹ sư đã có nền tảng.
   - Video không thể thay thế hàng trăm giờ code Java, cấu hình Kafka, tối ưu câu lệnh SQL Oracle hay phân tích tệp vết mạng Wireshark.
2. **Chiều sâu phòng phỏng vấn ACB**:
   - *(Giả định, chưa có nguồn)* Hội đồng kỹ thuật thường có kiến trúc sư giải pháp, trưởng nhóm kỹ thuật và người phụ trách an toàn thông tin. Hỏi HR thành phần hội đồng thật khi được mời phỏng vấn.
   - Khi hỏi sâu về một khái niệm, hội đồng sẽ truy vấn liên tiếp 3 tầng:
     - *Tầng 1 (Khái niệm)*: SAGA Orchestration là gì? (Ứng viên học vẹt trả lời được).
     - *Tầng 2 (Sự cố)*: Khi Orchestrator gửi lệnh đền bù (Compensating Transaction) nhưng dịch vụ tài khoản đích bị sập mạng (Network Partition), hệ thống treo trạng thái gì?
     - *Tầng 3 (Dung lượng & Cấu hình lõi)*: Dung lượng hàng đợi In-Flight là bao nhiêu? Cấu hình tham số `max.poll.interval.ms` trong Kafka Consumer và cờ `INITRANS` trong bảng Oracle ra sao để không bị ORA-00060?
   - Người học vẹt sẽ lúng túng và bộc lộ sự thiếu hụt thực tế ngay lập tức.
3. **Thẩm định Lý lịch (Background Check) & Đối soát BHXH VssID**:
   - Ngân hàng có thể xác minh quá trình công tác (xác nhận của công ty cũ, lịch sử đóng BHXH mà ứng viên cung cấp). *Chưa có nguồn nào cho thấy ACB dùng quy tắc cứng kiểu "dưới X năm BHXH thì hạ lương"*; đừng dựa vào giả định đó.
   - Cách phòng thủ duy nhất bền vững: mốc thời gian trên CV khớp đúng với hợp đồng và sổ BHXH; vai trò ghi đúng như đã làm.

---

## 2. KIM TỰ THÁP NĂNG LỰC 5 TẦNG: TỪ MẤT GỐC ĐẾN SENIOR BANKING

Để thực sự trở thành Senior Banking 50M gross, người học cần bước qua 5 tầng năng lực tích hợp sẵn trong kho bài giảng của dự án (643 bài học đã dựng, đo 2026-11-08: 611 bài các khóa nền + 15 bài BNK + 8 bài INT + 9 bài ACB):

```
                        ▲
                       / \
                      / T5\  -> AI Multiplier & Deal Lương 50M (INT L05, L07)
                     /-----\
                    /  T4   \ -> Nghiệp vụ T24, NAPAS, Squad Lending (INT L04, ACB L00-L08)
                   /---------\
                  /    T3     \ -> Hệ phân tán, SAGA, Outbox, Kafka EOS (INT L03, DSY, EVT)
                 /-------------\
                /      T2       \ -> Microservices, Spring Boot, Redis, Oracle (INT L02, DBS, SWF)
               /-----------------\
              /        T1         \ -> Nền tảng CS, Java 21, JVM, B-Tree (INT L01, CS112, CSA, OSY)
             -----------------------
```

### Tầng 1: Khoa học Máy tính Cơ bản & Java 21 Hiện đại
- **Nguồn học video có sẵn**: `BNK` L00–L01 (Java, GC, đa luồng, luồng ảo), `CS112` (Cấu trúc dữ liệu & giải thuật), `DMS` (Toán rời rạc), `CSA` (Kiến trúc máy tính), `OSY` (Hệ điều hành), `NET` (Mạng máy tính).
- **Trọng tâm**:
  - Mô hình phân cấp bộ nhớ máy tính (số xấp xỉ, tùy CPU): Thanh ghi CPU (dưới 1ns), L1/L2/L3 Cache (khoảng 1–20ns), RAM (khoảng 100ns). Căn chỉnh dòng đệm 64-byte tránh chia sẻ giả (False Sharing).
  - Quản lý bộ nhớ JVM: Young Gen (Eden, S0, S1), Old Gen, Metaspace. Các thuật toán GC: G1GC, ZGC.
  - Lập trình đồng thời Java 21: Luồng ảo (Virtual Threads), `ReentrantLock`, `CompletableFuture`, cấu trúc cây B-Tree với độ phức tạp $O(\log_m N)$.

### Tầng 2: Kỹ nghệ Microservices Doanh nghiệp & Spring Boot
- **Nguồn học video có sẵn**: `BNK` L02–L06 (Spring, REST, SQL, PL/SQL, Redis), `DBS` (Cơ sở dữ liệu), `SWF` (Phần mềm đúng đắn), `SDP` (Mẫu thiết kế), `INT/L02`.
- **Trọng tâm**:
  - Vòng đời Spring Bean, Dynamic Proxy (Spring Boot mặc định CGLIB; JDK Proxy khi cấu hình), tránh lỗi tự gọi hàm nội bộ (self-invocation) làm `@Transactional` không có hiệu lực.
  - Quản lý giao dịch: Mức cô lập (Read Committed, Serializable), quy tắc Rollback (`rollbackFor = Exception.class`).
  - Thiết kế REST API chuẩn RFC 9457 Problem Details (thay RFC 7807), Idempotency Key, Khóa phân tán Redis (`SET NX EX 60`).

### Tầng 3: Hệ thống Phân tán Chịu lỗi & Event Streaming
- **Nguồn học video có sẵn**: `BNK` L07–L09 (Kafka, SAGA/Outbox, sổ cái), `DSY` (Hệ phân tán), `EVT` (Hướng sự kiện), `DEN` (Kỹ thuật dữ liệu), `SAR` (Kiến trúc hệ thống), `INT/L03`.
- **Trọng tâm**:
  - Giới hạn của 2PC, mô hình SAGA Orchestration với Camunda.
  - Mẫu Transactional Outbox kết hợp CDC Debezium tránh lỗi ghi kép (Dual Write); giao nhận vẫn là at-least-once nên consumer phải lũy đẳng.
  - Apache Kafka Semantics: Exactly-Once Semantics (EOS), Transactional Producer, Consumer Idempotency.
  - Tối ưu hóa Oracle 19c: Phân vùng bảng (Range/List Partitioning), giảm bế tắc ORA-00060 bằng khóa theo một thứ tự toàn cục (khóa từng dòng theo khóa tăng dần; không dựa vào `ORDER BY ... FOR UPDATE`) và index cho cột khóa ngoại.

### Tầng 4: Nghiệp vụ Ngân hàng Lõi, Chuyển mạch & Tín dụng Bán lẻ
- **Nguồn học video có sẵn**: `BNK` L10–L14 (T24/OFS/IBM MQ, ISO 8583, đối soát, khối PIN/HSM, tình huống), `INT/L04` và trọn bộ `ACB/L00` đến `ACB/L08`.
- **Trọng tâm**:
  - Temenos T24 Core Banking: Bản tin OFS (dạng chuỗi phân cách; có biến thể XML qua adapter), tích hợp hàng đợi IBM MQ (JMS Correlation ID).
  - Chuyển mạch NAPAS 247: Bản tin ISO 8583 MTI 0200/0210, HSM *dịch* (translate) PIN Block giữa các khóa mà PIN không bao giờ ra dạng rõ, mã xác thực MAC ở trường 64 (hoặc 128 khi có bitmap phụ).
  - Sáu trụ cột tín dụng bán lẻ Squad Lending: Thấu chi sổ tiết kiệm, lương, thẻ tín dụng, BNPL, thế chấp, trả góp.
  - Đối soát tài chính 3 bên: So khớp file EOD, quy trình hạch toán đảo nợ và bù trừ tự động.

### Tầng 5: Bộ nhân Công nghệ UIT AI & Nghệ thuật Đàm phán 50M Gross
- **Nguồn học video có sẵn**: `INT/L05`, `INT/L06`, `INT/L07`.
- **Trọng tâm**:
  - Biến văn bằng Cử nhân AI tại UIT thành lợi thế cạnh tranh độc bản.
  - 3 ý tưởng AI ứng dụng (mức nguyên mẫu học thuật / thiết kế, không phải hệ thống đã vận hành): phát hiện bất thường qua ONNX Runtime, định tuyến với Multi-Armed Bandit, đối soát ngữ nghĩa bằng Sentence-Transformers.
  - Chiến lược đàm phán dựa trên giá trị có bằng chứng, gói thu nhập năm 700M – 850M VNĐ (50M × 13 tháng cố định + 1–4 tháng thưởng theo tin tuyển dụng ACB), và mốc thời gian công tác khớp hồ sơ BHXH.

---

## 3. DANH MỤC VIDEO VÀ TÀI LIỆU TOÀN BỘ KHÓA HỌC

Thời lượng, mã băm và trạng thái kiểm định của từng video **chỉ ghi ở một nơi** để không lệch nhau: [`MASTER_CURRICULUM_INDEX.md`](file:///D:/research-video/interview/MASTER_CURRICULUM_INDEX.md) (Mục 4–6, số đo ffprobe). Thứ tự học đề xuất:

1. **BNK L00 → L14** (`out/BNK/`): bài nền từ con số 0 cho đúng chủ đề phỏng vấn (Java, đa luồng, Spring, REST, SQL, PL/SQL, Redis, Kafka, SAGA/Outbox, sổ cái, T24/OFS/IBM MQ, ISO 8583, đối soát, khối PIN/HSM, tình huống).
2. **INT L00 → L07** (`interview/video/00_*.mp4` … `07_*.mp4`): khung năng lực, ôn kiến thức, ngân hàng câu hỏi, đàm phán.
3. **ACB L00 → L08** (`interview/video/L00.mp4` … `L08.mp4`): tóm tắt nghiệp vụ tích hợp ngân hàng theo chủ đề.
4. Đọc `06_interview_qa_bank_100.md`, tự trả lời không nhìn đáp án, rồi so.

---

## 4. CHIẾN LƯỢC ĐỐI THOẠI KHI BỊ TRA HỎI VỀ BẰNG UIT AI

Khi phỏng vấn, nếu bị hỏi: *"Em học Cử nhân AI tại UIT, tại sao không theo đuổi AI mà lại nộp hồ sơ vào vị trí Kỹ sư Tích hợp Ngân hàng?"*

**Kịch bản trả lời mẫu** (nói bằng lời của mình):
> *"Thưa các anh chị trong Hội đồng Kỹ thuật ACB, mục tiêu nghề nghiệp nhất quán của em là trở thành Kỹ sư Kiến trúc Tích hợp Cấp cao (Principal Integration Architect).*  
> *Khi làm tích hợp tín dụng với Core T24 qua IBM MQ và phối hợp luồng NAPAS với đội Switch, em thấy nhiều bài toán (phát hiện bất thường, so khớp đối soát lệch mô tả) khó giải bằng luật tĩnh thuần túy.*  
> *Vì vậy em học Cử nhân AI tại UIT – ĐHQG TP.HCM song song với công việc, dự kiến tốt nghiệp 11/2026. Chương trình cho em nền xác suất thống kê, tối ưu và học máy; em đã làm một nguyên mẫu học thuật phát hiện bất thường (Isolation Forest xuất ONNX).*  
> *Em không định chuyển hẳn sang AI; em muốn là kỹ sư tích hợp đánh giá được mô hình AI khi đưa vào luồng ngân hàng: đặt ở đâu, đo độ trễ thế nào, và khi mô hình sai thì luồng tiền vẫn an toàn."*
