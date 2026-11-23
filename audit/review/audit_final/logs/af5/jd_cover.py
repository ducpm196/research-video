"""AF5 — đối chiếu từ khoá JD (resources/job/JD.md, kể cả phần NAB, Vingroup, Vingroup AI) với kho bài.
Với mỗi từ khoá: số bài có từ khoá trong TIÊU ĐỀ/MỤC TIÊU (dạy chính), số bài có trong thân bài (nhắc tới), 4 bài tiêu biểu.
Chỉ đọc. Chạy: .venv/Scripts/python -B audit/review/audit_final/logs/af5/jd_cover.py > logs/af5/jd_cover.out"""
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[5]
sys.stdout.reconfigure(encoding="utf-8")

# (nhóm JD, nhãn, biểu thức chính quy không phân biệt hoa thường)
KW = [
    ("ACB/VPB lõi", "Spring Boot", r"spring boot"),
    ("ACB/VPB lõi", "Stored procedure / PL-SQL / T-SQL", r"pl/sql|thủ tục lưu trữ|stored procedure|t-sql"),
    ("ACB/VPB lõi", "Oracle tuning / execution plan", r"kế hoạch thực thi|execution plan|explain plan"),
    ("ACB/VPB lõi", "Oracle Sharding / In-Memory / AQ / JSON", r"sharding|in-memory|advanced queu|\bAQ\b"),
    ("ACB/VPB lõi", "Swagger / OpenAPI", r"openapi|swagger"),
    ("ACB/VPB lõi", "Kafka", r"kafka"),
    ("ACB/VPB lõi", "RabbitMQ / ActiveMQ", r"rabbitmq|activemq"),
    ("ACB/VPB lõi", "Redis", r"redis"),
    ("ACB/VPB lõi", "Elasticsearch", r"elasticsearch"),
    ("ACB/VPB lõi", "Couchbase", r"couchbase"),
    ("ACB/VPB lõi", "PostgreSQL", r"postgresql|postgres"),
    ("ACB/VPB lõi", "MongoDB", r"mongodb"),
    ("ACB/VPB lõi", "MySQL", r"mysql"),
    ("ACB/VPB lõi", "gRPC", r"grpc"),
    ("ACB/VPB lõi", "Docker", r"docker"),
    ("ACB/VPB lõi", "Kubernetes", r"kubernetes|k8s"),
    ("ACB/VPB lõi", "GitLab CI / Jenkins / CI-CD", r"gitlab|jenkins|ci/cd"),
    ("ACB/VPB lõi", "Lũy đẳng / idempotency", r"lũy đẳng|idempoten"),
    ("ACB/VPB lõi", "Saga / Outbox", r"saga|outbox"),
    ("ACB/VPB lõi", "JPA / Hibernate", r"hibernate|\bjpa\b"),
    ("ACB/VPB lõi", "DDD / CQRS / Event Sourcing", r"\bddd\b|cqrs|event sourcing"),
    ("ACB/VPB lõi", "Circuit breaker / API gateway", r"circuit breaker|ngắt mạch|api gateway|cổng api"),
    ("ACB/VPB lõi", "ELK / Prometheus / Grafana", r"prometheus|grafana|logstash|kibana"),
    ("ACB/VPB lõi", "GitOps / ArgoCD / Vault", r"gitops|argocd|argo cd|vault"),
    ("ACB/VPB lõi", "SOAP / SFTP", r"\bsoap\b|sftp"),
    ("ACB/VPB lõi", "JSP / Servlet / JBoss / Tomcat", r"servlet|\bjsp\b|jboss|tomcat"),
    ("ACB/VPB lõi", "Spring Security / Spring Cloud", r"spring security|spring cloud"),
    ("ACB/VPB lõi", "SOLID / design pattern / clean code", r"solid|mẫu thiết kế|clean code"),
    ("ACB/VPB lõi", "Chuẩn hoá 3NF", r"3nf|dạng chuẩn"),
    ("ACB/VPB lõi", "Thanh toán quốc tế / SWIFT / ngoại tệ", r"swift|ngoại tệ"),
    ("ACB/VPB lõi", "Ví điện tử / thuế điện tử", r"ví điện tử|thuế điện tử"),
    ("ACB/VPB lõi", "Phê duyệt tín dụng / LOS", r"phê duyệt tín dụng|\blos\b|khởi tạo khoản vay"),
    ("ACB/VPB lõi", "SLA / OLA / L3", r"\bsla\b|\bola\b|hỗ trợ mức 3"),
    ("ACB/VPB lõi", "Agile / Scrum", r"agile|scrum"),
    ("NAB", "GraphQL (Supergraph / Subgraph / Federation)", r"graphql|supergraph|subgraph"),
    ("NAB", "TDD (Test-Driven Development)", r"\btdd\b|test-driven|kiểm thử đi trước|phát triển hướng kiểm thử"),
    ("NAB", "Kiểm thử thành phần / tích hợp (component / integration test)", r"kiểm thử tích hợp|integration test|component test|testcontainers"),
    ("NAB", "AWS", r"\baws\b|amazon web services"),
    ("NAB", "Azure", r"azure"),
    ("NAB", "Serverless / FaaS / Lambda", r"serverless|faas|lambda function|aws lambda|hàm không máy chủ"),
    ("NAB", "Secure coding / OWASP", r"owasp|lập trình an toàn|secure coding"),
    ("NAB", "Sơ đồ kiến trúc (C4 / UML / sequence)", r"\bc4\b|\buml\b|sơ đồ tuần tự|sequence diagram"),
    ("NAB", "Node.js", r"node\.js|nodejs"),
    ("NAB", "React", r"\breact\b"),
    ("NAB", "Groovy", r"groovy"),
    ("NAB", "Dẫn dắt nhóm / mentoring / code review", r"mentor|dẫn dắt|code review|rà soát mã"),
    ("NAB", "Tiếng Anh giao tiếp / đọc tài liệu", r"tiếng anh"),
    ("Vingroup backend", "Thrift", r"thrift"),
    ("Vingroup backend", "Protobuf / Avro / schema versioning / tương thích ngược", r"protobuf|protocol buffers|avro|schema registry|tương thích ngược"),
    ("Vingroup backend", "Workflow orchestration / workflow engine (Temporal, Camunda, Airflow)", r"temporal|camunda|airflow|workflow engine|điều phối quy trình|bpmn"),
    ("Vingroup backend", "Dead letter queue", r"dead letter|\bdlq\b|hàng đợi thư chết"),
    ("Vingroup backend", "Exponential backoff / retry", r"backoff|lùi theo cấp số|thử lại"),
    ("Vingroup backend", "Cache stampede / invalidation", r"stampede|dồn tải cache|vô hiệu cache|invalidation|bầy đàn"),
    ("Vingroup backend", "Webhook / push notification", r"webhook|push notification|thông báo đẩy"),
    ("Vingroup backend", "Distributed tracing / OpenTelemetry", r"tracing|opentelemetry|truy vết phân tán|jaeger|zipkin"),
    ("Vingroup backend", "Audit trail / audit log", r"audit trail|audit log|nhật ký kiểm toán|vết kiểm toán"),
    ("Vingroup backend", "RCA / post-incident / postmortem", r"\brca\b|postmortem|post-mortem|nguyên nhân gốc|hậu kiểm sự cố"),
    ("Vingroup backend", "High-load / throughput / latency", r"thông lượng|độ trễ|throughput|latency"),
    ("Vingroup backend", "AI coding tools (Cursor, Claude Code, Copilot)", r"cursor|claude code|copilot|trợ lý lập trình"),
    ("Vingroup backend", "Tích hợp suy luận AI/ML vào backend (inference serving)", r"phục vụ mô hình|model serving|suy luận|inference"),
    ("Vingroup backend", "Go / TypeScript", r"golang|\bgo\b \(|typescript"),
    ("Vingroup backend", "Data pipeline / ingestion", r"đường ống dữ liệu|data pipeline|ingestion|nạp dữ liệu"),
    ("Vingroup AI/MLOps", "ML pipeline tự động / orchestration", r"ml pipeline|đường ống học máy|kubeflow|mlflow"),
    ("Vingroup AI/MLOps", "Experiment tracking", r"experiment tracking|theo dõi thí nghiệm|theo dõi thử nghiệm"),
    ("Vingroup AI/MLOps", "Model registry / versioning", r"model registry|kho mô hình|sổ đăng ký mô hình|phiên bản mô hình"),
    ("Vingroup AI/MLOps", "Feature store", r"feature store|kho đặc trưng"),
    ("Vingroup AI/MLOps", "Drift detection", r"drift|trôi dữ liệu|trôi phân phối"),
    ("Vingroup AI/MLOps", "Retraining automation", r"huấn luyện lại|retrain"),
    ("Vingroup AI/MLOps", "A/B testing mô hình", r"a/b"),
    ("Vingroup AI/MLOps", "Edge / IoT", r"\bedge\b|điện toán biên|\biot\b"),
    ("Vingroup AI/MLOps", "Multi-cloud / on-premise", r"multi-cloud|đa đám mây|on-premise|tại chỗ"),
    ("Vingroup AI/MLOps", "Linux + Bash automation", r"\bbash\b"),
    ("Vingroup AI/MLOps", "NLP: intent recognition / hội thoại nhiều lượt", r"nhận diện ý định|intent|nhiều lượt|multi-turn"),
    ("Vingroup AI/MLOps", "Test automation UI/API (Selenium, Cypress, Playwright, Postman, REST Assured)", r"selenium|cypress|playwright|postman|rest assured"),
    ("Vingroup AI/MLOps", "AI governance / data governance", r"quản trị ai|ai governance|quản trị dữ liệu|data governance"),
    ("Vingroup AI/MLOps", "Agentic AI", r"tác tử|agent"),
    ("Vingroup AI/MLOps", "Speech AI (ASR/TTS)", r"nhận dạng tiếng nói|speech|tổng hợp tiếng nói"),
]

lessons = []
for cy in sorted((ROOT / "curriculum").glob("*.yaml")):
    if cy.name == "tracks.yaml":
        continue
    cur = yaml.safe_load(cy.read_text(encoding="utf-8"))
    C = cy.stem.upper()
    for l in cur.get("lessons") or []:
        head = " ".join([str(l.get("title") or ""), " ".join(map(str, l.get("objectives") or []))])
        body = ""
        sp = l.get("spec")
        if sp and (ROOT / sp).exists():
            raw = (ROOT / sp).read_text(encoding="utf-8")
            d = yaml.safe_load(raw)
            head += " " + str(d.get("title") or "") + " " + " ".join(map(str, d.get("objectives") or []))
            body = raw
        lessons.append((C, l.get("id"), head, body))

print(f"số bài đối chiếu: {len(lessons)}")
print("nhóm\ttừ khoá\tbài dạy chính (tiêu đề/mục tiêu)\tbài có nhắc\tbài tiêu biểu")
grp = None
for g, label, pat in KW:
    rx = re.compile(pat, re.I)
    main = [f"{c}:{i}" for c, i, h, b in lessons if rx.search(h)]
    ment = [(len(rx.findall(b)), f"{c}:{i}") for c, i, h, b in lessons if rx.search(b)]
    ment.sort(reverse=True)
    top = ", ".join(main[:6]) if main else "(thân bài) " + ", ".join(f"{k}×{n}" for n, k in ment[:4])
    print(f"{g}\t{label}\t{len(main)}\t{len(ment)}\t{top}")
