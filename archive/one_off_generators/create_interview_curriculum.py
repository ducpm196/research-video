import yaml
import os

os.makedirs(r"D:\research-video\lessons\int", exist_ok=True)

# Curriculum definition
curriculum = {
    "course": "INT",
    "status": "active",
    "lessons": [
        {
            "id": "L01",
            "title": "Nền tảng Khoa học Máy tính, Java 21 Hiện đại, JVM và Đa luồng",
            "spec": "lessons/int/L01_foundation_cs_java.yaml",
            "requires": [],
            "objectives": [
                "Làm chủ mô hình phân cấp bộ nhớ máy tính, CPU Cache Line và bộ nhớ JVM",
                "Hiểu sâu cơ chế Garbage Collection và các tính năng Java 21 Virtual Threads",
                "Nắm vững độ phức tạp thuật toán và cấu trúc dữ liệu B-Tree trong cơ sở dữ liệu"
            ],
            "example": "truy xuất bộ nhớ đệm CPU trong 1 nano giây; khởi tạo một triệu luồng ảo tốn vài trăm byte bộ nhớ",
            "fix": ["Không dùng kiểu số thực cho tiền tệ mà bắt buộc dùng số thập phân chính xác với quy tắc làm tròn tường minh"]
        },
        {
            "id": "L02",
            "title": "Kỹ nghệ Microservices Doanh nghiệp, Spring Boot, REST API và Redis",
            "spec": "lessons/int/L02_backend_microservices.yaml",
            "requires": ["L01"],
            "objectives": [
                "Làm chủ vòng đời Spring Bean, Dynamic Proxy và xử lý triệt để lỗi tự gọi hàm nội bộ",
                "Nắm vững các mức lan truyền Transaction và quy tắc Rollback chuẩn mực ngân hàng",
                "Thiết kế REST API chuẩn RFC 7807, cơ chế Idempotency và cấu hình Connection Pool"
            ],
            "example": "cấu hình connection pool 30 kết nối phục vụ 5000 request; khóa phân tán Redis khử trùng lặp trong 120 giây",
            "fix": ["Không gọi hàm nội bộ cùng class khiến mất proxy transaction mà tách service hoặc inject qua ApplicationContext"]
        },
        {
            "id": "L03",
            "title": "Hệ thống Phân tán, SAGA Pattern, Kafka EOS và Tối ưu hóa Oracle 19c",
            "spec": "lessons/int/L03_distributed_systems_senior.yaml",
            "requires": ["L01", "L02"],
            "objectives": [
                "Hiểu rõ hạn chế của giao thức 2PC và làm chủ mô hình SAGA Orchestration trong ngân hàng",
                "Triển khai mẫu Transactional Outbox với CDC Debezium khử triệt để hiểm họa ghi kép",
                "Tối ưu hóa bảng ghi Oracle 19c bằng Partitioning và triệt tiêu bế tắc khóa ORA-00060"
            ],
            "example": "xử lý 50000 thông điệp mỗi giây qua Kafka với Zero Message Loss; giảm thời gian khóa dòng xuống 5 mili giây",
            "fix": ["Không thực hiện ghi kép vào cơ sở dữ liệu và hàng đợi mà gom vào cùng transaction ACID qua bảng outbox"]
        },
        {
            "id": "L04",
            "title": "Nghiệp vụ Ngân hàng Toàn diện: Core T24, Chuyển mạch NAPAS và Squad Lending",
            "spec": "lessons/int/L04_banking_domain_t24_napas.yaml",
            "requires": ["L01", "L02", "L03"],
            "objectives": [
                "Làm chủ bản tin OFS XML trên Temenos T24 và kết nối hàng đợi IBM MQ bất đồng bộ",
                "Nắm vững cấu trúc bản tin ISO 8583 MTI 0200 cổng NAPAS 247 và bảo mật giải mã PIN",
                "Bao quát 6 trụ cột tín dụng bán lẻ Squad Lending: Thấu chi sổ tiết kiệm, lương, thẻ và cổng CIC"
            ],
            "example": "xử lý 8000 TPS cổng NAPAS độ trễ 120 mili giây; giải ngân thấu chi sổ tiết kiệm trong 60 giây",
            "fix": ["Không giải ngân khi chưa hoàn tất phong tỏa sổ cái Core T24 và kiểm tra khử trùng lặp khóa phân tán"]
        },
        {
            "id": "L05",
            "title": "Ứng dụng AI Ngân hàng: Minh chứng Bằng Cử nhân AI UIT và Lợi thế Cạnh tranh",
            "spec": "lessons/int/L05_uit_ai_banking_multiplier.yaml",
            "requires": ["L01", "L02", "L03"],
            "objectives": [
                "Làm rõ ma trận 38 môn học Cử nhân AI tại Đại học Công nghệ Thông tin UIT ĐHQG-HCM",
                "Làm chủ 3 bài toán cấp số nhân: Phát hiện gian lận sub-5ms, định tuyến thông minh và đối soát ngữ nghĩa",
                "Bảo vệ bản lĩnh phỏng vấn trước câu hỏi về bằng cấp liên thông và vị thế Kỹ sư Cấp cao"
            ],
            "example": "suy luận mô hình học máy trong 3 mili giây qua ONNX runtime; đối soát tự động đạt 99.2 phần trăm chính xác",
            "fix": ["Không dùng quy tắc tĩnh để bắt gian lận mà áp dụng mô hình phân tách cô lập suy luận ngay trong luồng"]
        },
        {
            "id": "L06",
            "title": "Bộ 100 Câu hỏi Phỏng vấn Thực chiến Senior Banking và Kỹ thuật Phản xạ",
            "spec": "lessons/int/L06_interview_qa_bank_100.yaml",
            "requires": ["L01", "L02", "L03", "L04", "L05"],
            "objectives": [
                "Làm chủ phản xạ 5 nhóm câu hỏi: Khoa học máy tính, Microservices, Hệ phân tán, Nghiệp vụ bank và Thiết kế hệ thống",
                "Nắm vững phương pháp trả lời đào sâu 5 tầng kỹ thuật và giải thích sự cố sản xuất thực tế",
                "Chứng minh phẩm chất Kỹ sư Cấp cao luôn đặt an toàn dòng tiền và tính toàn vẹn hệ thống lên hàng đầu"
            ],
            "example": "phản xạ trôi chảy 100 câu hỏi chuyên sâu; thiết kế hệ thống thanh toán 10000 TPS đạt độ sẵn sàng 4 số 9",
            "fix": ["Không trả lời chung chung lý thuyết mà luôn gắn liền với số liệu đo lường, mã lỗi hệ thống và kịch bản thực chiến"]
        },
        {
            "id": "L07",
            "title": "Chiến lược và Kịch bản Đàm phán Chốt Mức Lương 50 Triệu Gross tại ACB",
            "spec": "lessons/int/L07_salary_negotiation_50m_gross.yaml",
            "requires": ["L01", "L02", "L03", "L04", "L05", "L06"],
            "objectives": [
                "Làm chủ ma trận định lượng giá trị và chứng minh lợi tức đầu tư 50 triệu gross cho ngân hàng",
                "Thuần thục kịch bản đối đáp 3 vòng: Sàng lọc nhân sự, hội đồng kỹ thuật và chốt đãi ngộ",
                "Hóa giải hoàn toàn các đòn ép giá về số năm kinh nghiệm và kiểm tra đối soát phúc lợi ngoài lương"
            ],
            "example": "chốt mức lương 50 triệu gross tương đương 750 triệu một năm; chứng minh giá trị bảo vệ tài sản hàng tỷ đồng",
            "fix": ["Không khai báo lương cơ bản thấp mà neo giá trị vào tổng thu nhập và cam kết hiệu quả thử việc"]
        }
    ]
}

with open(r"D:\research-video\curriculum\int.yaml", "w", encoding="utf-8") as f:
    yaml.dump(curriculum, f, allow_unicode=True, sort_keys=False)

print("Created curriculum/int.yaml successfully!")
