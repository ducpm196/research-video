# Thư viện ngoài của bài BNX L30 (Resilience4j, chỉ để SO với bản cầu dao tự cài)

Tải bằng Maven 3.9.11 (`audit/bnx/deps/_tools`) ngày 2026-11-14: `mvn -B dependency:copy-dependencies -DoutputDirectory=.` với `pom.xml` cùng thư mục
(resilience4j-circuitbreaker 2.3.0; còn lại là phụ thuộc bắc cầu do Maven phân giải). Temurin JDK 21.0.13.

| Tệp | sha256 |
|---|---|
| annotations-13.0.jar | ace2a10dc8e2d5fd34925ecac03e4988b2c0f851650c94b8cef49ba1bd111478 |
| kotlin-stdlib-1.9.0.jar | 35aeffbe2db5aa446072cee50fcee48b7fa9e2fc51ca37c0cc7d7d0bc39d952e |
| kotlin-stdlib-common-1.9.0.jar | 283274204bd7c020789ec46f8f8e72af4244d7f550b3392a57e5ca006ad7aa2c |
| kotlin-stdlib-jdk7-1.9.0.jar | b7979a7aac94055f0d9f1fd3b47ce5ffe1cb6032a842ba9fbe7186f085289178 |
| kotlin-stdlib-jdk8-1.9.0.jar | a59fa24fdf1ffb594baecdbf0fd10010f977cea10236d487fe3464977a7377fa |
| resilience4j-circuitbreaker-2.3.0.jar | 5e9d6b821cf620b26b9144c5ea8d92a80c717ebda1500061231eed5017f56927 |
| resilience4j-core-2.3.0.jar | bdaf2c553265b9c1ac6967acf598e3f433cc592e85e7872bd24d1e6264a97b93 |
| slf4j-api-1.7.30.jar | cdba07964d1bb40a0761485c6b1e8c2f8fd9eb1d19c53928ac0d7f9510105c57 |
