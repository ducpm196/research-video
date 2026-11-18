# Thư viện ngoài của bài BNX L25 (Spring Framework 7.0.10 + AspectJ weaver + H2)

Tải bằng Maven 3.9.11 (`audit/bnx/deps/_tools`) ngày 2026-11-13: `mvn -B dependency:copy-dependencies -DoutputDirectory=.` với `pom.xml` cùng thư mục
(spring-context 7.0.10, spring-jdbc 7.0.10, aspectjweaver 1.9.24, h2 2.3.232; còn lại là phụ thuộc bắc cầu do Maven phân giải). Temurin JDK 21.0.13.

| Tệp | sha256 |
|---|---|
| aspectjweaver-1.9.24.jar | 75e4227fb7dc5f97c3d4689cd1c2439f4db0bd18cea2fa242c4656cd93c599aa |
| commons-logging-1.3.5.jar | 6d7a744e4027649fbb50895df9497d109f98c766a637062fe8d2eabbb3140ba4 |
| h2-2.3.232.jar | 8dae62d22db8982c3dcb3826edb9c727c5d302063a67eef7d63d82de401f07d3 |
| jspecify-1.0.1.jar | 070d75f261fe4c5b8202508366715f7f2d4660f88c8ef7e6d3575e48c9683b66 |
| micrometer-commons-1.16.8.jar | 66ebb98b23ec65300b5b670f8ff49e1cc1400e71ebb7881390cd10bc6ed492ad |
| micrometer-observation-1.16.8.jar | e9640e8a4c77fe458deada6db9b8e1c094e519ebc333a3d005c15eebb1be942c |
| spring-aop-7.0.10.jar | babf50a645f4f788e1267078cf891e472f657cabf65518055cf5214220574e3f |
| spring-beans-7.0.10.jar | bd67c6fc887afa30cbcb489ff4f82bf19f818e79ab1cf1bef98dff8a289108ec |
| spring-context-7.0.10.jar | f0065166b6a5101a871ab8702d6c4011cf39faed370a64e7ef14a3ad2bf2a99a |
| spring-core-7.0.10.jar | a236f31a7c07e3a1a8e7839ec5c0d47b5cc75709132db50416d5dad320341f12 |
| spring-expression-7.0.10.jar | 12067b66548f7613fa8938ca6051a6d1dd8c397bf478e0bb1adb9936358ec81d |
| spring-jdbc-7.0.10.jar | bc4ba6bd242f2db2642938960ae27589b53dd6a611d700a260af7b3383cd0c6c |
| spring-tx-7.0.10.jar | 9442610a8ed3d44e70fa97f49896ea810c831da62620101450f0feb522edb4cd |
