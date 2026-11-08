# CHUYÊN ĐỀ 5: BẰNG CỬ NHÂN AI TẠI UIT VÀ GIÁ TRỊ CẤP SỐ NHÂN TRONG NGÂN HÀNG (THE UIT AI MULTIPLIER)

> **Mục tiêu**: Làm rõ giá trị vượt trội của Bằng Cử nhân Trí tuệ Nhân tạo tại **Đại học Công nghệ Thông tin (UIT - ĐHQG TP.HCM)** đối với một Kỹ sư Tích hợp Cấp cao (Senior Integration Engineer). Biến học vấn AI từ một "dấu chấm hỏi" thành **một lợi thế có thể chứng minh** khi ứng tuyển vào ACB, mà không nói quá điều mình đã làm.  
> **Thông tin đào tạo**: Đại học Công nghệ Thông tin (UIT – ĐHQG TP.HCM) | *Bachelor of Science in Artificial Intelligence (Articulated Degree)* | **Tháng 06/2025 – Tháng 11/2026 (dự kiến tốt nghiệp; chưa nhận bằng tính đến 2026-11-08)**.

> **Quy tắc trung thực của chuyên đề này (rà soát 2026-11-08)**: mọi con số trong Mục 3 (độ trễ, tỉ lệ, phần trăm) là **ví dụ minh họa / mục tiêu thiết kế**, không phải kết quả đo của ứng viên hay của ngân hàng nào. Dự án Isolation Forest/ONNX là **dự án học thuật UIT** (BN-0022: cần repo hoặc báo cáo làm bằng chứng). Tên môn trong Mục 2 phải được thay bằng tên học phần đúng trên bảng điểm UIT trước khi dùng (BN-0028).

---

## 1. TỔNG QUAN: VÌ SAO KỸ SƯ TÍCH HỢP NGÂN HÀNG LẠI CẦN NỀN TẢNG AI?

Đa số lập trình viên backend truyền thống nhìn bài toán tích hợp chỉ là:
`Nhận JSON từ Client -> Gọi HTTP sang Core Banking -> Lưu DB -> Trả về Client`.

Tuy nhiên, trong kỷ nguyên số hóa tài chính 2026, các ngân hàng hàng đầu như ACB đang đối mặt với các bài toán có độ phức tạp cao hơn nhiều:
1. **Lưu lượng lớn và tấn công tinh vi**: phát hiện gian lận phải chạy trong ngân sách độ trễ của luồng thanh toán (thường chỉ vài chục mili giây cho mọi bước kiểm tra cộng lại), nên mô hình phải nhẹ và chạy cục bộ.
2. **Chi phí cước viễn thông và hạ tầng bùng nổ**: Đòi hỏi các thuật toán tối ưu hóa định tuyến (Smart Routing) và phân bổ tài nguyên thông minh.
3. **Dữ liệu phân mảnh và phi cấu trúc**: Đòi hỏi so khớp đối soát ngữ nghĩa (Semantic Reconciliation) thay vì so khớp chuỗi ký tự thô sơ.
4. **Quy định pháp lý khắt khe**: Triển khai giải pháp sinh trắc học khuôn mặt theo Quyết định 2345/QĐ-NHNN với khả năng chống giả mạo (Anti-spoofing Liveness Detection).

Một Kỹ sư Tích hợp có nền tảng AI mang lại **giá trị cộng thêm**: hiểu luồng tích hợp ngân hàng, đồng thời đọc hiểu và đánh giá được các mô hình AI (giới hạn, độ trễ, sai số) khi chúng được đưa vào đường ống dữ liệu.

---

## 2. MA TRẬN NHÓM KIẾN THỨC AI ỨNG DỤNG VÀO HẠ TẦNG NGÂN HÀNG

> **Chưa xác minh (BN-0028)**: con số "38 môn" và tên các môn dưới đây **chưa được đối chiếu với bảng điểm hay chương trình đào tạo chính thức của UIT**. Trước phỏng vấn, mở bảng điểm, thay cột giữa bằng tên học phần thật đã học, và xóa dòng nào không học.

Bảng dưới nhóm kiến thức theo khối, kèm chỗ dùng được trong kiến trúc tích hợp ngân hàng:

| Nhóm môn học UIT | Các môn tiêu biểu trong chương trình | Ứng dụng thực chiến trong Kiến trúc Tích hợp Ngân hàng |
|:---|:---|:---|
| **Toán học & Cơ sở AI** | Giải tích, Đại số tuyến tính, Xác suất thống kê, Toán rời rạc, Lý thuyết đồ thị | Tính toán độ lệch Z-Score cho hạn mức giao dịch, ma trận ma-trận biến đổi tọa độ 3D trong xác thực sinh trắc học, tính toán xác suất rủi ro giao dịch. |
| **Cấu trúc Dữ liệu & Giải thuật nâng cao** | Thiết kế & Phân tích giải thuật, Cấu trúc dữ liệu nâng cao, Tối ưu hóa tổ hợp | Lý luận về thứ tự khóa (khóa tài nguyên theo một thứ tự toàn cục để không tạo chu trình chờ, giảm deadlock ORA-00060); Token Bucket Rate Limiter; chia để trị trong Statement Hub. |
| **Hệ thống Máy tính & Mạng** | Kiến trúc máy tính, Hệ điều hành nâng cao, Mạng máy tính phân tán | Quản lý luồng JVM (Virtual Threads Project Loom), tối ưu hóa bộ nhớ đệm CPU L1/L2/L3 cache-friendly data structures, bắt gói tin TCP Socket ISO 8583. |
| **Cơ sở dữ liệu & Phân tích Dữ liệu lớn** | Cơ sở dữ liệu nâng cao, Big Data Analytics, NoSQL, Hệ phân tán | Thiết kế phân vùng bảng Oracle Partitioning, mô hình Transactional Outbox, Streaming ksqlDB, Kafka Streams, CDC Debezium. |
| **Học máy & Học sâu (ML / DL)** | Machine Learning cơ bản & nâng cao, Deep Learning, Computer Vision | Mô hình Isolation Forest, Autoencoder phát hiện bất thường; suy luận ONNX Runtime nhúng trong Java (độ trễ phải đo bằng benchmark của chính mình). |
| **Thị giác Máy tính (Computer Vision)** | Thị giác máy tính, Xử lý ảnh số, Nhận dạng mẫu | Hiểu nguyên lý OCR thẻ CCCD, kiểm tra người thật (liveness) và chống giả mạo khuôn mặt; QĐ 2345/QĐ-NHNN quy định khi nào phải xác thực sinh trắc học, còn công nghệ do nhà cung cấp giải pháp đảm nhận. |
| **Xử lý Ngôn ngữ Tự nhiên & Trích xuất Thông tin** | NLP, Information Retrieval, Large Language Models (LLM) | Dùng Sentence-Transformers vector embeddings để so khớp tự động sao kê đối soát tài chính giữa ngân hàng và đối tác thu hộ. |
| **Kỹ thuật MLOps & Kỹ nghệ Phần mềm** | MLOps, CI/CD, Containerization (Docker/K8s), Cloud Computing | Đóng gói mô hình AI thành Microservices siêu nhẹ, triển khai Kubernetes, quản lý versioning mô hình và dữ liệu (Model/Data Lineage). |

---

## 3. BA BÀI TOÁN KỸ THUẬT MINH CHỨNG "GIÁ TRỊ CẤP SỐ NHÂN"

### 3.1. Phát hiện Gian lận Thời gian thực (Real-Time Fraud Detection on Kafka Pipeline)
- **Kiến trúc tích hợp**:
  - Khi luồng sự kiện thanh toán đi qua Kafka (`payment.inbound.topic`), thay vì chỉ kiểm tra các rule tĩnh (như số tiền > 50M), worker tích hợp thư viện `onnxruntime-java`.
  - Mô hình **Isolation Forest** và **Autoencoder** đã được huấn luyện ngoại tuyến (Offline Training) để nắm bắt phân phối bình thường của khách hàng.
  - Khi có giao dịch mới, worker trích xuất vector đặc trưng (Feature Vector): Tốc độ di chuyển địa lý (Geovelocity $v > 800\text{ km/h}$), Z-score số tiền so với lịch sử 30 ngày, tần suất giao dịch trong 5 phút.
  - Điểm bất thường (Anomaly Score) được suy luận trực tiếp trong Java runtime qua ONNX Runtime (lõi C++). **Mục tiêu thiết kế** là vài mili giây mỗi lần suy luận để nằm gọn trong ngân sách độ trễ của cổng thanh toán; con số thật phải đo bằng benchmark (JMH hoặc đo p95/p99) trên máy và mô hình của mình trước khi nói ra.

### 3.2. Định tuyến Thanh toán Thông minh (Intelligent Routing với Multi-Armed Bandit)
- **Vấn đề**: Ngân hàng có nhiều kênh chuyển tiền (NAPAS 247, CITAD, Kết nối song phương Bilateral Direct API). Các kênh thường xuyên biến động về độ trễ và tỷ lệ lỗi vào giờ cao điểm.
- **Giải pháp AI**:
  - Áp dụng bài toán **Multi-Armed Bandit** (kiến thức học tăng cường; xem CS115 Bài 39). Công thức dưới là **UCB1**; Thompson Sampling là cách khác (lấy mẫu từ phân phối Beta của tỉ lệ thành công mỗi kênh), không dùng công thức này:
    $$\text{Score}_k = \hat{\mu}_k + c \sqrt{\frac{\ln N}{N_k}}$$
  - Hệ thống tự động theo dõi tỷ lệ phản hồi thành công $\hat{\mu}_k$ của từng cổng trong cửa sổ trượt 15 phút.
  - Khi một kênh nghẽn làm tỷ lệ lỗi tăng, điểm của kênh đó giảm và lưu lượng **được phép** chuyển sang kênh khác giảm theo. **Giới hạn thực tế**: chọn kênh chuyển tiền còn bị ràng buộc bởi quy định và nghiệp vụ (hạn mức, giờ chốt, loại giao dịch, kênh nào được dùng cho giao dịch nào), nên bandit chỉ chọn trong các kênh hợp lệ; đây là ý tưởng thiết kế, không phải hệ thống ứng viên đã vận hành.

### 3.3. Tự động hóa Đối soát Tài chính bằng Vector Embeddings
- **Vấn đề**: Đối tác thanh toán hóa đơn (Điện, Nước, Thuế, Vé máy bay) xuất file đối soát có trường nội dung mô tả sai lệch chính tả và không tuân thủ quy chuẩn cú pháp, khiến kế toán phải dò tay hàng nghìn giao dịch mỗi ngày.
- **Giải pháp AI**:
  - Sử dụng mô hình ngôn ngữ **Sentence-Transformers** để sinh vector 384 chiều biểu diễn ngữ nghĩa của chuỗi mô tả giao dịch.
  - Thực hiện tính toán độ tương đồng Cosine:
    $$\text{CosineSimilarity}(\vec{v}_1, \vec{v}_2) = \frac{\vec{v}_1 \cdot \vec{v}_2}{\|\vec{v}_1\| \|\vec{v}_2\|}$$
  - Kết hợp với ràng buộc số tiền và thời gian, các cặp có độ tương đồng cao được **đề xuất** khớp, người vận hành duyệt các cặp dưới ngưỡng. Tỉ lệ khớp đúng phải đo trên tập dữ liệu có nhãn; không nêu phần trăm khi chưa đo. Khớp tiền tuyệt đối vẫn bắt buộc so khóa chính xác (mã giao dịch, số tiền), embedding chỉ hỗ trợ phần mô tả.

---

## 4. CHIẾN LƯỢC TRẢ LỜI PHỎNG VẤN VỀ BẰNG CẤP UIT AI

Khi Ban tuyển dụng hoặc Lãnh đạo ACB hỏi:
*"Bạn làm về Tích hợp hệ thống Backend, tại sao lại đi học Cử nhân Trí tuệ Nhân tạo tại UIT? Liệu có phải bạn đang định hướng chuyển nghề sang làm Data Scientist/AI Engineer?"*

**Khung câu trả lời mẫu** (nói bằng lời của mình, chỉnh theo trải nghiệm thật):
> *"Dạ thưa anh/chị, mục tiêu của em nhất quán: **trở thành kỹ sư kiến trúc tích hợp giỏi trong ngành ngân hàng**.*  
> *Khi làm tích hợp tín dụng tại OCB (Core T24 qua IBM MQ, phối hợp luồng NAPAS 247 với đội Switch) và trước đó ở dự án cho vay tiêu dùng của Mirae Asset Finance, em thấy nhiều bài toán như phát hiện bất thường hay so khớp đối soát lệch mô tả khó giải bằng luật if-else thuần túy.*  
> *Vì vậy em học chương trình **Cử nhân Trí tuệ Nhân tạo tại UIT – ĐHQG TP.HCM** song song với công việc, dự kiến tốt nghiệp 11/2026. Em đã làm một nguyên mẫu học thuật phát hiện bất thường bằng Isolation Forest xuất sang ONNX để hiểu chi phí suy luận. Em không định chuyển hẳn sang Data Scientist; em muốn là kỹ sư tích hợp hiểu được mô hình AI khi chúng được đưa vào luồng ngân hàng: đặt nó ở đâu, đo độ trễ thế nào, và khi mô hình sai thì luồng tiền vẫn an toàn."*
