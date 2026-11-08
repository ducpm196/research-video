import pymupdf
import os

pdf_path = r"D:\research-video\resources\job\PHAM-MINH-DUC-SENIOR-INTEGRATION-CV.pdf"
avatar_path = r"D:\research-video\resources\job\avatar.jpg"

doc = pymupdf.open()

# Common CSS Styles
css = """
<style>
body {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 8.25pt;
    color: #222222;
    line-height: 1.27;
    margin: 0;
    padding: 0;
}
.header {
    border-bottom: 2.2px solid #003366;
    padding-bottom: 4px;
    margin-bottom: 3.5px;
}
h1 {
    font-size: 16.5pt;
    font-weight: 800;
    color: #003366;
    margin: 0;
    letter-spacing: 0.5px;
}
.subtitle {
    font-size: 9.0pt;
    font-weight: 700;
    color: #006699;
    margin-top: 1.5px;
    margin-bottom: 2.5px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}
.contact-info {
    font-size: 7.9pt;
    color: #444444;
    line-height: 1.35;
}
h2 {
    font-size: 9.1pt;
    font-weight: 700;
    color: #003366;
    border-bottom: 1.2px solid #003366;
    padding-bottom: 1.5px;
    margin-top: 4.5px;
    margin-bottom: 2.5px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}
.sub-tag {
    font-size: 7.9pt;
    font-weight: 700;
    color: #006699;
    text-transform: uppercase;
    margin-top: 2.5px;
    margin-bottom: 1.5px;
}
.exp-header {
    margin-top: 3.5px;
    margin-bottom: 1.5px;
}
.job-title {
    font-size: 8.6pt;
    font-weight: 700;
    color: #111111;
}
.company {
    font-size: 8.6pt;
    font-weight: 700;
    color: #006699;
}
.location-date {
    font-size: 7.8pt;
    color: #666666;
    font-style: italic;
}
ul {
    margin: 1.5px 0 2.0px 12px;
    padding: 0;
}
li {
    margin-bottom: 1.8px;
    text-align: justify;
}
b {
    color: #002244;
}
.project-box {
    margin-top: 3px;
    margin-bottom: 2.5px;
}
.project-title {
    font-size: 8.6pt;
    font-weight: 700;
    color: #003366;
}
.project-meta {
    font-size: 7.8pt;
    color: #555555;
    font-style: italic;
    margin-bottom: 1.5px;
}
.ref-card {
    background-color: #f7f9fa;
    border-left: 3px solid #006699;
    padding: 3.5px 8px;
    margin-bottom: 3.5px;
}
</style>
"""

# ==================== PAGE 1 ====================
page1 = doc.new_page(width=595, height=842) # A4
rect1 = pymupdf.Rect(35, 20, 560, 822)

html_page1 = f"""
{css}
<div>
    <div class="header">
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="vertical-align: middle; padding: 0;">
                    <h1>PHAM MINH DUC</h1>
                    <div class="subtitle">SENIOR BACKEND & BANKING INTEGRATION SOFTWARE ENGINEER</div>
                    <div class="contact-info">
                        📍 Ho Chi Minh City, Vietnam &nbsp;|&nbsp; 📅 DOB: 20/09/1996 &nbsp;|&nbsp; 📞 (+84) 965 141 282 &nbsp;|&nbsp; ✉ ducpm196@gmail.com<br>
                        🎯 <b>Focus</b>: Core Lending, Overdraft & Interbank Integration
                    </div>
                </td>
                <td style="width: 62px; height: 78px; padding: 0;">&nbsp;</td>
            </tr>
        </table>
    </div>

    <h2>PROFESSIONAL SUMMARY</h2>
    <p style="margin: 2px 0 2px 0; text-align: justify;">
        Dedicated Senior Backend & Banking Integration Engineer with <b>3+ years of intensive core banking, squad lending, and digital credit integration experience at OCB</b>, preceded by consumer lending fintech engineering at <b>Mirae Asset Finance</b> and enterprise Java/AEM development at <b>Sutrix Group</b>. Final-year Bachelor of Science candidate in <b>Artificial Intelligence at UIT (University of Information Technology – VNU-HCM)</b> (Articulated Degree Program, expected graduation November 2026, advancing from <b>FPT Polytechnic</b>).
    </p>
    <ul style="margin-top: 1px;">
        <li><b>Core Focus & Hands-on Delivery</b>: Key module engineer in <b>Squad Lending</b>, directly building core integration services for <b>Term Deposit Overdraft & Pledge</b>, <b>Payroll Overdraft</b>, <b>Cloud CA E-Sign (FPT)</b>, and <b>CIC B2B API</b>, enforcing distributed idempotency via Redis Mutex and automated CASA partial debit.</li>
        <li><b>Enterprise Integration & Collaboration</b>: Collaborated closely with core banking and switch infrastructure teams to integrate lending workflows with <b>Temenos T24 (OFS XML via IBM MQ)</b> and <b>NAPAS 247 interbank payment switch (ISO 8583)</b>, with strict data integrity through idempotency, reversal and reconciliation handling.</li>
        <li><b>Reliability & Optimization</b>: Hands-on experience tuning Oracle 19c SQL queries and PL/SQL procedures within squad services, resolving deadlock bottlenecks (<code>ORA-00060</code>), and integrating <b>Decision 2345 biometrics</b> into the lending flow; applied ML (anomaly detection) as a UIT academic project.</li>
    </ul>

    <h2>CORE TECHNICAL COMPETENCIES</h2>
    <div style="margin-top: 1px; margin-bottom: 2px;">
        <div style="margin-bottom: 1.5px;"><span style="font-weight: 700; color: #003366;">Languages & Runtimes:</span> Java (Core 8/11/17/21, Virtual Threads), Go (Golang), Python, SQL, PL/SQL</div>
        <div style="margin-bottom: 1.5px;"><span style="font-weight: 700; color: #003366;">Lending & Overdraft Tech:</span> Squad Lending, Term Deposit Overdraft & Collateral Pledge, Payroll Overdraft, Card Limit Loan, CIC B2B API, Cloud CA (Digital Signature Gateway), LOS/LMS</div>
        <div style="margin-bottom: 1.5px;"><span style="font-weight: 700; color: #003366;">Core Banking & Switch:</span> Temenos T24 OFS XML, IBM MQ (JMS Correlation), NAPAS 247 (ISO 8583, TCP Sockets), HSM PIN Translation, 3-Way EOD Recon</div>
        <div style="margin-bottom: 1.5px;"><span style="font-weight: 700; color: #003366;">Frameworks & Architecture:</span> Spring Boot, Spring Cloud, Spring Security, Eclipse Vert.x, Fiber (Go), Event-Driven Architecture, SAGA Pattern, Outbox, CQRS</div>
        <div style="margin-bottom: 1.5px;"><span style="font-weight: 700; color: #003366;">Databases & Tuning:</span> Oracle 19c (PL/SQL Stored Procedures, Explain Plan, Index Tuning, Partitioning, Deadlock Resolution), PostgreSQL, Redis Cluster</div>
        <div style="margin-bottom: 1.5px;"><span style="font-weight: 700; color: #003366;">Streaming & Confluent:</span> Confluent Platform, Apache Kafka (EOS, Partitions), ksqlDB & Custom UDFs, Kafka Streams, Schema Registry (Avro), DLQ</div>
        <div style="margin-bottom: 1.5px;"><span style="font-weight: 700; color: #003366;">Enterprise CMS & Security:</span> Adobe Experience Manager (AEM Sites 6.x), Decision 2345 Biometrics, PCI-DSS, Docker, Kubernetes, CI/CD</div>
        <div style="margin-bottom: 1.5px;"><span style="font-weight: 700; color: #003366;">Applied AI & Banking ML:</span> Python, PyTorch, Scikit-Learn, ONNX Runtime, Isolation Forest (Fraud & Anomaly Detection), Semantic Vector Search</div>
    </div>

    <h2>PROFESSIONAL WORK EXPERIENCE</h2>

    <div class="exp-header">
        <div><span class="company">ORIENT COMMERCIAL BANK (OCB)</span> &nbsp;—&nbsp; <span class="job-title">Senior Integration Application Specialist (Squad Lending & Core Integration)</span></div>
        <div class="location-date">Ho Chi Minh City, Vietnam &nbsp;|&nbsp; October 2023 – Present (3+ years)</div>
    </div>
    <div class="sub-tag">Direct Module Ownership & Implementation (Key Contributions)</div>
    <ul>
        <li><b>Squad Lending & Digital Overdraft Products</b>: Key module engineer in Squad Lending (Retail Lending Integration Gateway connecting Core T24 and digital channels). Directly built backend integration workflows for <b>Term Deposit Overdraft & Pledge</b> (automated two-phase collateral hold/lien marking on T24, dynamic LTV-based limit calculation, spread interest calculation, auto-release upon loan payoff) and <b>Payroll Overdraft</b> (batch payroll cashflow evaluation and instant limit issuance).</li>
        <li><b>Cloud CA Digital Signature & Decision 2345 Integration</b>: Directly integrated <b>Cloud CA Gateway (FPT E-Sign)</b> with Decision 2345 facial biometric authentication and OTP for paperless credit contract signing with ECM document sync.</li>
        <li><b>National Credit Information Center (CIC) B2B Client</b>: Built automated B2B client integrating with CIC via mTLS/VPN. Extracted debt history, automated SBV debt-group classification (Circular 11/2021/TT-NHNN, replaced by Circular 31/2024/TT-NHNN from 07/2024), and applied DTI underwriting checks.</li>
        <li><b>Idempotent Disbursement & Partial Debit Collection</b>: Implemented distributed Redis Mutex locks (<code>SET loan:disb:{{app_id}} 1 NX EX 300</code>) with SAGA compensation, mitigating double disbursement risk. Built automated batch collection engine supporting <b>Partial Debit</b> from CASA accounts on scheduled due dates.</li>
        <li><b>Oracle 19c Tuning & Deadlock Resolution</b>: Optimized PL/SQL stored procedures and SQL queries for lending and transfer modules. Enforced a deterministic lock order (locking account rows one at a time in ascending key order) plus foreign-key and composite index tuning, resolving <code>ORA-00060</code> deadlocks observed at peak hours.</li>
    </ul>
    <div class="sub-tag">Squad & Cross-Team Collaboration (Shared Enterprise Services)</div>
    <ul>
        <li><b>Core Banking T24 & IBM MQ Integration</b>: Collaborated with core integration team to connect lending modules to T24 OFS XML via IBM MQ. Handled multi-value fields (OfsDataField) for CASA and deposits, tracked request-reply flows via JMSCorrelationID, and handled SAGA timeout compensations.</li>
        <li><b>NAPAS 247 Interbank Switch Integration</b>: Collaborated with the Switch team to route real-time interbank loan disbursements and collections via NAPAS 247 (ISO 8583). Integrated transaction deduplication via Redis (transId 60s TTL) and reversal workflows under network timeouts.</li>
        <li><b>Kafka Event Streaming & Notification Hub</b>: Integrated lending event streams with the bank's Confluent Kafka cluster. Developed custom ksqlDB UDFs and notification consumers to route omnichannel alerts (OTT App Push, SMS, Email) with priority queues and DLQ.</li>
    </ul>
</div>
"""
res1 = page1.insert_htmlbox(rect1, html_page1)

# Embed candidate avatar portrait into header top-right
img_rect = pymupdf.Rect(503, 24, 560, 100) # 57 width, 76 height (exact 3:4 aspect ratio)
page1.insert_image(img_rect, filename=avatar_path)

# Thin elegant navy border (#003366) around photo
shape = page1.new_shape()
shape.draw_rect(img_rect)
shape.finish(color=(0/255, 51/255, 102/255), width=0.8)
shape.commit()

# ==================== PAGE 2 ====================
page2 = doc.new_page(width=595, height=842) # A4
rect2 = pymupdf.Rect(35, 20, 560, 822)

html_page2 = f"""
{css}
<div>
    <div class="exp-header" style="margin-top: 0;">
        <div><span class="company">GROOO INTERNATIONAL</span> &nbsp;—&nbsp; <span class="job-title">Backend Software Engineer (Fintech Lending / Outsource for Mirae Asset Finance)</span></div>
        <div class="location-date">Ho Chi Minh City, Vietnam &nbsp;|&nbsp; October 2022 – September 2023</div>
    </div>
    <ul>
        <li><b>Client: Mirae Asset Finance Company (MAFC)</b> — Leading consumer finance institution; core backend engineer for digital lending.</li>
        <li><b>Loan Origination & Management Systems (LOS/LMS)</b>: Engineered microservices for consumer loan approval, automated credit scoring, underwriting decision engine, and loan account management using Spring Boot, Spring Cloud, Kafka, Consul, Docker, and Kubernetes.</li>
        <li><b>Automated Disbursement & Idempotency Engine (Direct Ownership)</b>: Developed automated loan disbursement gateway connecting to commercial banks and NAPAS. Enforced strict distributed idempotency and distributed state machines, preventing duplicate disbursement under network retries.</li>
        <li><b>High-Performance Concurrency Optimization</b>: Optimized API throughput using Java advanced multithreading (ForkJoinPool, CompletableFuture, ExecutorService) to improve response times during peak campaigns.</li>
        <li><b>Loan State Auditability & Security</b>: Implemented Event Sourcing and SAGA pattern for cross-service loan state management. Hardened security with Spring Security OAuth2, JWT blacklist in Redis, 2FA, and device fingerprinting to prevent loan application fraud.</li>
    </ul>

    <div class="exp-header">
        <div><span class="company">FREELANCE</span> &nbsp;—&nbsp; <span class="job-title">Backend Software Engineer / Consultant (Java Spring)</span> &nbsp;|&nbsp; <span class="location-date">January 2022 – September 2022</span></div>
    </div>
    <ul>
        <li>Designed and deployed robust web services with Spring Boot and Spring microservices, leveraging Apache Kafka for real-time synchronization. Containerized architectures using Docker and orchestrated deployments on Kubernetes with automated tests (JUnit 5, Mockito).</li>
    </ul>

    <div class="exp-header">
        <div><span class="company">SUTRIX GROUP</span> &nbsp;—&nbsp; <span class="job-title">Software Engineer (Adobe Experience Manager & Core Java)</span></div>
        <div class="location-date">Ho Chi Minh City, Vietnam &nbsp;|&nbsp; January 2019 – December 2021</div>
    </div>
    <ul>
        <li><b>Enterprise Client: Globe Telecom</b> — Developed high-traffic web applications using <b>Adobe Experience Manager (AEM Sites 6.4/6.5)</b> and <b>Core Java</b>. Engineered custom OSGi bundles, Sling Models, HTL components, JCR content repositories, and enterprise Spring services.</li>
        <li>Managed AWS infrastructure (EC2, S3, RDS, CloudWatch) and automated GitLab CI/CD. Achieved <b>Adobe Certified Expert - AEM Sites Developer</b>.</li>
    </ul>

    <h2>NOTABLE FEATURED PROJECTS</h2>

    <div class="project-box">
        <div class="project-title">1. Omnichannel Digital Lending & Overdraft Platform (Squad Lending)</div>
        <div class="project-meta">Role: Key Integration Engineer (Direct Module Lead) &nbsp;|&nbsp; Tech: Java 17, Spring Boot, Temenos T24 OFS XML, IBM MQ, Redis Mutex, FPT E-Sign, CIC B2B</div>
        <ul>
            <li><b>Direct Contribution & Impact</b>: Directly built backend integration workflows for Term Deposit Overdraft (two-phase T24 hold), Cloud CA signing (FPT E-Sign) with Decision 2345 Face Auth, and Redis Mutex disbursement lock with SAGA compensation. Delivered paperless loan origination with idempotent disbursement protection.</li>
        </ul>
    </div>

    <div class="project-box">
        <div class="project-title">2. NAPAS 247 Interbank Payment Integration (Lending Side)</div>
        <div class="project-meta">Role: Integration Engineer, working with the Switch team &nbsp;|&nbsp; Tech: Java 17, Apache Kafka, Redis, ISO 8583</div>
        <ul>
            <li><b>Hands-on Contribution & Impact</b>: Integrated lending disbursement and collection flows with the Switch team's NAPAS 247 gateway: Redis atomic deduplication (transId 60s TTL) and SAGA rollback/reversal handling on network timeouts. The gateway, sockets and HSM are operated by the Switch team.</li>
        </ul>
    </div>

    <div class="project-box">
        <div class="project-title">3. Applied AI: Anomaly Detection Prototype (UIT Academic Project)</div>
        <div class="project-meta">Role: Individual academic/personal project &nbsp;|&nbsp; Tech: Python, Scikit-Learn, PyTorch, ONNX Runtime</div>
        <ul>
            <li><b>Hands-on Contribution & Impact</b>: Anomaly-detection prototype (Isolation Forest exported to ONNX Runtime) built to study low-latency inference for transaction screening. Learning project, not a production OCB system.</li>
        </ul>
    </div>

    <h2>EDUCATION & CREDENTIALS</h2>
    <div style="margin-top: 3px;">
        <div><span style="font-weight: 700; color: #003366; font-size: 8.6pt;">Bachelor of Science in Artificial Intelligence (Articulated Degree Program)</span> &nbsp;|&nbsp; <span style="font-size: 7.8pt; color: #666666; font-style: italic;">June 2025 – November 2026 (expected)</span></div>
        <div style="font-size: 8.2pt; color: #222222;"><b>University of Information Technology (UIT) – Vietnam National University, HCMC (VNU-HCM)</b></div>
        <div style="font-size: 7.7pt; color: #555555; margin-bottom: 2.5px;">Advanced Algorithms, Distributed Systems, Machine Learning, Anomaly Detection (Advancing from FPT Polytechnic).</div>
    </div>
    <div style="margin-top: 2.5px;">
        <div><span style="font-weight: 700; color: #003366; font-size: 8.6pt;">Associate Degree in Software Engineering (Programming Computers & Mobile Devices)</span> &nbsp;|&nbsp; <span style="font-size: 7.8pt; color: #666666; font-style: italic;">October 2016 – March 2019</span></div>
        <div style="font-size: 8.2pt; color: #222222;"><b>FPT Polytechnic</b> (Foundation in Algorithms, Java Core, OOP, and Enterprise Systems).</div>
    </div>
    <div style="margin-top: 2.5px; margin-bottom: 2px;">
        <div style="font-weight: 700; color: #003366; font-size: 8.2pt;">Certification: <b>Adobe Certified Expert</b> (AEM Sites Developer, 2020)</div>
    </div>

    <h2>PROFESSIONAL REFERENCES</h2>
    <div style="margin-top: 4px;">
        <div class="ref-card">
            <span style="font-weight: 700; color: #003366; font-size: 8.5pt;">Mr. Phan Anh Tuấn</span> &nbsp;—&nbsp; <span style="font-weight: 700; color: #333333; font-size: 8.3pt;">Deputy Head of Integration Applications</span> &nbsp;|&nbsp; <span style="color: #006699; font-weight: 700;">Orient Commercial Bank (OCB)</span>
            <div style="font-size: 7.6pt; color: #555555; font-style: italic; margin-top: 1px;">Relationship: Direct Line Manager at OCB &nbsp;|&nbsp; Contact details available upon request</div>
        </div>
        <div class="ref-card">
            <span style="font-weight: 700; color: #003366; font-size: 8.5pt;">Mr. Quan Quốc Bảo</span> &nbsp;—&nbsp; <span style="font-weight: 700; color: #333333; font-size: 8.3pt;">Head of Application Management</span> &nbsp;|&nbsp; <span style="color: #006699; font-weight: 700;">Asia Commercial Bank (ACB)</span>
            <div style="font-size: 7.6pt; color: #555555; font-style: italic; margin-top: 1px;">Relationship: Professional Reference via Senior Industry Network &nbsp;|&nbsp; Contact details available upon request</div>
        </div>
    </div>
</div>
"""
res2 = page2.insert_htmlbox(rect2, html_page2)

doc.save(pdf_path)
print(f"Successfully generated updated PDF with avatar: {pdf_path}")
print(f"Total pages: {len(doc)}")
print(f"Page 1: unused_height = {res1[0]:.2f}, scale = {res1[1]}")
print(f"Page 2: unused_height = {res2[0]:.2f}, scale = {res2[1]}")
