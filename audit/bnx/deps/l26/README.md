# Thư viện ngoài của bài BNX L26 (Maven, Gradle và Jenkins)

- Apache Maven 3.9.11: `audit/bnx/deps/_tools/README.md` (sha512/sha256 của tệp zip). Bài chạy THẬT Maven này (cần mạng lần đầu để tải plugin và phụ thuộc vào `~/.m2`).
- Apache Groovy 4.0.27 (chỉ để kiểm cú pháp tệp Jenkinsfile và build.gradle bằng `GroovyShell.parse`, không chạy): tải bằng Maven ngày 2026-11-13
  (`mvn -B dependency:copy-dependencies -DoutputDirectory=.` với `pom.xml` cùng thư mục).

| Tệp | sha256 |
|---|---|
| groovy-4.0.27.jar | c9103813240be47a6c48bcdda7c5ed2e5fc9ecba3251c6ab8122258230a97f9d |
