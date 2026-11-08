# PHAM MINH DUC
**SENIOR BACKEND & BANKING INTEGRATION SOFTWARE ENGINEER**

<img src="avatar.jpg" alt="Pham Minh Duc" width="100" align="right" style="border-radius: 4px; border: 1px solid #003366;" />

📍 Ho Chi Minh City, Vietnam · 📅 DOB: 20/09/1996 · 📞 (+84) 965 141 282 · ✉ ducpm196@gmail.com · 🎯 Focus: Core Lending, Overdraft & Interbank Integration

---

## PROFESSIONAL SUMMARY
Dedicated Senior Backend & Banking Integration Engineer with **3+ years of intensive core banking, squad lending, and digital credit integration experience at OCB**, preceded by consumer lending fintech engineering at **Mirae Asset Finance** and enterprise Java/AEM development at **Sutrix Group**. Final-year Bachelor of Science candidate in **Artificial Intelligence at UIT (University of Information Technology – VNU-HCM)** (Articulated Degree Program, expected graduation November 2026, advancing from **FPT Polytechnic**).
- **Core Focus & Hands-on Delivery**: Key module engineer in **Squad Lending**, directly building core integration services for **Term Deposit Overdraft & Pledge**, **Payroll Overdraft**, **Cloud CA E-Sign (FPT)**, and **CIC B2B API**, enforcing distributed idempotency via Redis Mutex and automated CASA partial debit.
- **Enterprise Integration & Collaboration**: Collaborated closely with core banking and switch infrastructure teams to integrate lending workflows with **Temenos T24 (OFS XML via IBM MQ)** and **NAPAS 247 interbank payment switch (ISO 8583)**, with strict data integrity through idempotency, reversal and reconciliation handling.
- **Reliability & Optimization**: Hands-on experience tuning Oracle 19c SQL queries and PL/SQL procedures within squad services, resolving deadlock bottlenecks (`ORA-00060`), and integrating **Decision 2345 biometrics** into the lending flow; applied ML (anomaly detection) as a UIT academic project.

---

## CORE TECHNICAL COMPETENCIES

| Category | Technologies & Methodologies |
|:---|:---|
| **Programming Languages** | Java (Core 8/11/17/21, Virtual Threads), Go (Golang), Python, SQL, PL/SQL |
| **Lending & Overdraft Tech** | Squad Lending, Term Deposit Overdraft & Collateral Pledge, Payroll Overdraft, Card Limit Loan, CIC B2B API, Cloud CA (Digital Signature Gateway), LOS/LMS |
| **Core Banking & Switch** | Temenos T24 OFS XML, IBM MQ (JMS Correlation), NAPAS 247 (ISO 8583, TCP Sockets), HSM PIN Translation, 3-Way EOD Recon |
| **Frameworks & Architecture** | Spring Boot, Spring Cloud, Spring Security, Eclipse Vert.x, Fiber (Go), Event-Driven Architecture, SAGA Pattern, Outbox, CQRS |
| **Databases & Tuning** | Oracle 19c (PL/SQL Stored Procedures, Explain Plan, Index Tuning, Partitioning, Deadlock Resolution), PostgreSQL, Redis Cluster |
| **Streaming & Confluent** | Confluent Platform, Apache Kafka (EOS, Partitions), ksqlDB & Custom UDFs, Kafka Streams, Schema Registry (Avro), DLQ |
| **Enterprise CMS & Security** | Adobe Experience Manager (AEM Sites 6.x), Decision 2345 Biometrics, PCI-DSS, Docker, Kubernetes, CI/CD |
| **Applied AI & Banking ML** | Python, PyTorch, Scikit-Learn, ONNX Runtime, Isolation Forest (Fraud & Anomaly Detection), Semantic Vector Search |

---

## PROFESSIONAL WORK EXPERIENCE

### ORIENT COMMERCIAL BANK (OCB) — Ho Chi Minh City
**Senior Integration Application Specialist (Squad Lending & Core Integration)**  
*October 2023 – Present (3+ years)*

#### Direct Module Ownership & Implementation (Key Contributions)
- **Squad Lending & Digital Overdraft Products**: Key module engineer in Squad Lending (Retail Lending Integration Gateway connecting Core T24 and digital channels). Directly built backend integration workflows for **Term Deposit Overdraft & Pledge** (automated two-phase collateral hold/lien marking on T24, dynamic LTV-based limit calculation, spread interest calculation, auto-release upon loan payoff) and **Payroll Overdraft** (batch payroll cashflow evaluation and instant limit issuance).
- **Cloud CA Digital Signature & Decision 2345 Integration**: Directly integrated **Cloud CA Gateway (FPT E-Sign)** with Decision 2345 facial biometric authentication and OTP for paperless credit contract signing with ECM document sync.
- **National Credit Information Center (CIC) B2B Client**: Built automated B2B client integrating with CIC via mTLS/VPN. Extracted debt history, automated SBV debt-group classification (Circular 11/2021/TT-NHNN, replaced by Circular 31/2024/TT-NHNN from 07/2024), and applied DTI underwriting checks.
- **Idempotent Disbursement & Partial Debit Collection**: Implemented distributed Redis Mutex locks (`SET loan:disb:{app_id} 1 NX EX 300`) with SAGA compensation, mitigating double disbursement risk. Built automated batch collection engine supporting **Partial Debit** from CASA accounts on scheduled due dates.
- **Oracle 19c Tuning & Deadlock Resolution**: Optimized PL/SQL stored procedures and SQL queries for lending and transfer modules. Enforced a deterministic lock order (locking account rows one at a time in ascending key order) plus foreign-key and composite index tuning, resolving `ORA-00060` deadlocks observed at peak hours.

#### Squad & Cross-Team Collaboration (Shared Enterprise Services)
- **Core Banking T24 & IBM MQ Integration**: Collaborated with core integration team to connect lending modules to T24 OFS XML via IBM MQ. Handled multi-value fields (`OfsDataField`) for CASA and deposits, tracked request-reply flows via `JMSCorrelationID`, and handled SAGA timeout compensations.
- **NAPAS 247 Interbank Switch Integration**: Collaborated with the Switch team to route real-time interbank loan disbursements and collections via NAPAS 247 (ISO 8583). Integrated transaction deduplication via Redis (`transId` 60s TTL) and reversal workflows under network timeouts.
- **Kafka Event Streaming & Notification Hub**: Integrated lending event streams with the bank's Confluent Kafka cluster. Developed custom ksqlDB UDFs and notification consumers to route omnichannel alerts (OTT App Push, SMS, Email) with priority queues and DLQ.

---

### GROOO INTERNATIONAL — Ho Chi Minh City
**Backend Software Engineer (Fintech Lending / Outsource for Mirae Asset Finance)**  
*October 2022 – September 2023*
- **Client**: **Mirae Asset Finance Company (MAFC)** — Leading consumer finance institution; core backend engineer for digital lending.
- **Loan Origination & Management Systems (LOS/LMS)**: Engineered microservices for consumer loan approval, automated credit scoring, underwriting decision engine, and loan account management using Spring Boot, Spring Cloud, Kafka, Consul, Docker, and Kubernetes.
- **Automated Disbursement & Idempotency Engine (Direct Ownership)**: Developed automated loan disbursement gateway connecting to commercial banks and NAPAS. Enforced strict distributed idempotency and distributed state machines, preventing duplicate disbursement under network retries.
- **High-Performance Concurrency Optimization**: Optimized API throughput using Java advanced multithreading (`ForkJoinPool`, `CompletableFuture`, `ExecutorService`) to improve response times during peak campaigns.
- **Loan State Auditability & Security**: Implemented Event Sourcing and SAGA pattern for cross-service loan state management. Hardened security with Spring Security OAuth2, JWT blacklist in Redis, 2FA, and device fingerprinting to prevent loan application fraud.

---

### FREELANCE
**Backend Software Engineer / Consultant (Java Spring)**  
*January 2022 – September 2022*
- Designed and deployed robust web services with Spring Boot and Spring microservices, leveraging Apache Kafka for real-time synchronization. Containerized architectures using Docker and orchestrated deployments on Kubernetes with automated tests (JUnit 5, Mockito).

---

### SUTRIX GROUP — Ho Chi Minh City
**Software Engineer (Adobe Experience Manager & Core Java)**  
*January 2019 – December 2021*
- **Enterprise Client**: **Globe Telecom** — Developed high-traffic web applications using **Adobe Experience Manager (AEM Sites 6.4/6.5)** and **Core Java**. Engineered custom OSGi bundles, Sling Models, HTL components, JCR content repositories, and enterprise Spring services.
- Managed AWS infrastructure (EC2, S3, RDS, CloudWatch) and automated GitLab CI/CD. Achieved **Adobe Certified Expert - AEM Sites Developer**.

---

## NOTABLE FEATURED PROJECTS

### 1. Omnichannel Digital Lending & Overdraft Platform (Squad Lending)
- **Role**: Key Integration Engineer (Direct Module Lead) · **Tech**: Java 17, Spring Boot, Temenos T24 OFS XML, IBM MQ, Redis Mutex, FPT E-Sign, CIC B2B.
- **Direct Contribution & Impact**: Directly built backend integration workflows for Term Deposit Overdraft (two-phase T24 hold), Cloud CA signing (FPT E-Sign) with Decision 2345 Face Auth, and Redis Mutex disbursement lock with SAGA compensation. Delivered paperless loan origination with idempotent disbursement protection.

### 2. NAPAS 247 Interbank Payment Integration (Lending Side)
- **Role**: Integration Engineer, working with the Switch team · **Tech**: Java 17, Apache Kafka, Redis, ISO 8583.
- **Hands-on Contribution & Impact**: Integrated lending disbursement and collection flows with the Switch team's NAPAS 247 gateway: Redis atomic deduplication (`transId` 60s TTL) and SAGA rollback/reversal handling on network timeouts. The gateway, sockets and HSM are operated by the Switch team.

### 3. Applied AI: Anomaly Detection Prototype (UIT Academic Project)
- **Role**: Individual academic/personal project · **Tech**: Python, Scikit-Learn, PyTorch, ONNX Runtime.
- **Hands-on Contribution & Impact**: Anomaly-detection prototype (Isolation Forest exported to ONNX Runtime) built to study low-latency inference for transaction screening. Learning project, not a production OCB system.

---

## EDUCATION & CREDENTIALS

- **Bachelor of Science in Artificial Intelligence (Articulated Degree Program)**  
  *University of Information Technology (UIT) – Vietnam National University, Ho Chi Minh City (VNU-HCM)* · **June 2025 – November 2026 (expected)**
  - Core Focus: Advanced Data Structures & Algorithms, Distributed Systems, Machine Learning, Anomaly Detection (Advancing from FPT Polytechnic).
- **Associate Degree in Software Engineering (Programming Computers & Mobile Devices)**  
  *FPT Polytechnic* · **October 2016 – March 2019**
  - Foundation: Algorithms, Java Core, OOP, and Enterprise Systems.
- **Certification**: **Adobe Certified Expert** – Adobe Experience Manager Sites Developer (2020)

---

## PROFESSIONAL REFERENCES
- **Mr. Phan Anh Tuấn** – Deputy Head of Integration Applications, *Orient Commercial Bank (OCB)*  
  *Relationship*: Direct Line Manager at OCB. *(Contact details available upon request)*
- **Mr. Quan Quốc Bảo** – Head of Application Management, *Asia Commercial Bank (ACB)*  
  *Relationship*: Professional Reference via Senior Industry Network at ACB. *(Contact details available upon request)*
