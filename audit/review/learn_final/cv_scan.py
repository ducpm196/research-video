# Đo độ phủ CV → bài học: mỗi thuật ngữ kỹ thuật trên CV xuất hiện ở bài nào, bao nhiêu lần.
# Chạy: PYTHONIOENCODING=utf-8 .venv/Scripts/python -B audit/review/learn_final/cv_scan.py > audit/review/learn_final/logs/cv_scan.out
# "Có bài dạy" (ước lượng máy) = ít nhất một bài nhắc thuật ngữ từ 3 lần trở lên; người điều phối đọc lại các mục yếu.
import sys, re, glob, os
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TERMS = [  # (nhóm CV, nhãn, biểu thức chính quy không phân biệt hoa thường)
 ("Ngôn ngữ", "Virtual Threads / luồng ảo", r"virtual thread|luồng ảo"),
 ("Ngôn ngữ", "Go (Golang), goroutine", r"\bgolang\b|goroutine|\bGo\b(?! to)"),
 ("Ngôn ngữ", "Fiber (Go)", r"\bfiber\b"),
 ("Ngôn ngữ", "Python", r"\bpython\b"),
 ("Ngôn ngữ", "PL/SQL", r"pl/sql|plsql"),
 ("Java nâng cao", "ForkJoinPool", r"forkjoin"),
 ("Java nâng cao", "CompletableFuture", r"completablefuture"),
 ("Java nâng cao", "ExecutorService / bể luồng", r"executorservice|bể luồng|thread pool"),
 ("Tín dụng", "Thấu chi (overdraft)", r"thấu chi|overdraft"),
 ("Tín dụng", "Phong toả / lien / hold sổ tiết kiệm", r"phong to[ảa]|phong tỏa|\blien\b"),
 ("Tín dụng", "LTV", r"\bLTV\b|tỉ lệ cấp vốn|tỷ lệ cho vay trên"),
 ("Tín dụng", "Lãi spread / biên độ", r"spread|biên độ lãi"),
 ("Tín dụng", "Thấu chi lương / chi lương", r"thấu chi lương|chi lương|payroll"),
 ("Tín dụng", "Vay trên hạn mức thẻ / thẻ ảo", r"hạn mức thẻ|thẻ ảo"),
 ("Tín dụng", "CIC", r"\bCIC\b"),
 ("Tín dụng", "Nhóm nợ / TT 31/2024", r"nhóm nợ|31/2024"),
 ("Tín dụng", "DTI", r"\bDTI\b"),
 ("Tín dụng", "Ký số / Cloud CA / chữ ký số", r"cloud ca|ký số|chữ ký số"),
 ("Tín dụng", "LOS / LMS (khởi tạo, quản lý khoản vay)", r"\bLOS\b|\bLMS\b|khởi tạo khoản vay"),
 ("Tín dụng", "Chấm điểm tín dụng / thẩm định", r"chấm điểm tín dụng|credit scor|thẩm định"),
 ("Tín dụng", "Trích nợ từng phần (partial debit)", r"trích nợ từng phần|partial debit|thu nợ từng phần"),
 ("Tín dụng", "Giải ngân", r"giải ngân"),
 ("Tín dụng", "ECM / lưu hồ sơ hợp đồng", r"\bECM\b"),
 ("Core & Switch", "T24 OFS", r"\bOFS\b"),
 ("Core & Switch", "IBM MQ", r"ibm mq|\bMQ\b"),
 ("Core & Switch", "JMSCorrelationID / mã tương quan", r"correlation|mã tương quan"),
 ("Core & Switch", "Trường đa trị (multi-value)", r"multi-value|đa trị|đa giá trị"),
 ("Core & Switch", "NAPAS", r"napas"),
 ("Core & Switch", "ISO 8583", r"8583"),
 ("Core & Switch", "TCP socket", r"socket"),
 ("Core & Switch", "HSM / dịch khối PIN", r"\bHSM\b"),
 ("Core & Switch", "Đối soát (ba bên, cuối ngày)", r"đối soát"),
 ("Core & Switch", "Đảo giao dịch (reversal)", r"reversal|đảo giao dịch|\b0420\b|\b0400\b"),
 ("Framework", "Spring Boot", r"spring boot"),
 ("Framework", "Spring Cloud", r"spring cloud"),
 ("Framework", "Spring Security", r"spring security"),
 ("Framework", "Eclipse Vert.x / vòng lặp sự kiện", r"vert\.?x|event loop|vòng lặp sự kiện"),
 ("Framework", "Consul / khám phá dịch vụ", r"consul|service discovery|khám phá dịch vụ"),
 ("Kiến trúc", "SAGA", r"saga"),
 ("Kiến trúc", "Outbox", r"outbox"),
 ("Kiến trúc", "CQRS", r"cqrs"),
 ("Kiến trúc", "Event Sourcing", r"event sourcing|nguồn sự kiện|lưu sự kiện làm nguồn"),
 ("Kiến trúc", "Lũy đẳng (idempotency)", r"lũy đẳng|luỹ đẳng|idempoten"),
 ("Kiến trúc", "Máy trạng thái", r"máy trạng thái|state machine"),
 ("Kiến trúc", "Khoá Redis SET NX EX / mutex", r"\bNX\b|mutex|khoá phân tán|khóa phân tán"),
 ("CSDL", "Kế hoạch thực thi (Explain Plan)", r"explain plan|kế hoạch thực thi"),
 ("CSDL", "Chỉ mục ghép / tinh chỉnh chỉ mục", r"chỉ mục ghép|composite index|chỉ mục"),
 ("CSDL", "Phân vùng bảng (partitioning)", r"phân vùng|partition"),
 ("CSDL", "ORA-00060 / bế tắc", r"ora-00060|bế tắc|deadlock"),
 ("CSDL", "Chỉ mục khoá ngoại", r"khoá ngoại|khóa ngoại|foreign key"),
 ("CSDL", "PostgreSQL", r"postgres"),
 ("CSDL", "Redis Cluster", r"redis cluster|cụm redis|hash slot|khe băm"),
 ("Streaming", "Confluent Platform", r"confluent"),
 ("Streaming", "Kafka EOS (exactly-once)", r"exactly.once|đúng một lần|read_committed"),
 ("Streaming", "ksqlDB / UDF", r"ksqldb|\bUDF\b"),
 ("Streaming", "Kafka Streams", r"kafka streams"),
 ("Streaming", "Schema Registry / Avro", r"schema registry|avro"),
 ("Streaming", "DLQ", r"\bDLQ\b|dead.letter|hàng đợi thư chết"),
 ("Streaming", "Hàng đợi ưu tiên / thông báo đa kênh", r"hàng đợi ưu tiên|priority queue|đa kênh|omnichannel"),
 ("Bảo mật", "QĐ 2345 / sinh trắc học", r"2345|sinh trắc"),
 ("Bảo mật", "PCI-DSS", r"pci"),
 ("Bảo mật", "OAuth2", r"oauth"),
 ("Bảo mật", "JWT / danh sách đen JWT", r"\bJWT\b"),
 ("Bảo mật", "2FA / MFA / OTP", r"\b2FA\b|\bMFA\b|\bOTP\b|nhiều yếu tố"),
 ("Bảo mật", "Dấu vân tay thiết bị (device fingerprint)", r"device fingerprint|vân tay thiết bị|dấu vân thiết bị"),
 ("Bảo mật", "mTLS / VPN", r"mtls|\bVPN\b"),
 ("Hạ tầng", "Docker", r"docker"),
 ("Hạ tầng", "Kubernetes", r"kubernetes"),
 ("Hạ tầng", "CI/CD, GitLab CI", r"ci/cd|gitlab"),
 ("Hạ tầng", "AWS EC2 / S3 / RDS / CloudWatch", r"\bEC2\b|\bS3\b|\bRDS\b|cloudwatch"),
 ("Hạ tầng", "JUnit 5 / Mockito", r"junit|mockito"),
 ("AEM", "Adobe Experience Manager", r"\bAEM\b|experience manager"),
 ("AEM", "OSGi / Sling / HTL / JCR", r"osgi|sling|\bHTL\b|\bJCR\b"),
 ("AI", "PyTorch", r"pytorch"),
 ("AI", "Scikit-Learn", r"scikit|sklearn"),
 ("AI", "ONNX Runtime", r"onnx"),
 ("AI", "Isolation Forest / phát hiện bất thường", r"isolation forest|rừng cô lập|phát hiện bất thường"),
 ("AI", "Tìm kiếm vector ngữ nghĩa", r"vector search|tìm kiếm vector|tìm theo vector|vector nhúng|embedding"),
]
docs = {}
for p in sorted(glob.glob(os.path.join(ROOT, "lessons", "*", "L*.yaml"))):
    C = os.path.basename(os.path.dirname(p)).upper()
    docs[f"{C}:{os.path.basename(p)[:3]}"] = open(p, encoding="utf-8").read()
print(f"# quét {len(docs)} đặc tả bài; ngưỡng 'có bài dạy' = một bài nhắc ≥ 3 lần")
print("| Nhóm CV | Thuật ngữ | Số bài nhắc | Số bài nhắc ≥3 lần | Ba bài nhắc nhiều nhất | Xếp loại máy |")
print("|---|---|---:|---:|---|---|")
weak = []
for grp, label, rx in TERMS:
    r = re.compile(rx, re.I)
    cnt = {u: len(r.findall(t)) for u, t in docs.items()}
    hit = {u: c for u, c in cnt.items() if c}
    strong = [u for u, c in hit.items() if c >= 3]
    top = sorted(hit.items(), key=lambda x: -x[1])[:3]
    cls = "CÓ" if strong else ("MỎNG" if hit else "KHÔNG")
    if cls != "CÓ":
        weak.append((cls, grp, label))
    print(f"| {grp} | {label} | {len(hit)} | {len(strong)} | {', '.join(f'{u} ({c})' for u, c in top)} | {cls} |")
print()
print("# mục yếu:", len(weak))
for w in weak:
    print("-", *w)
