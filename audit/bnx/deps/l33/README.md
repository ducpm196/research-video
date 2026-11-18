# Thư viện ngoài của bài BNX L33 (Tomcat nhúng 10.1.61 + bộ biên dịch JSP Jasper)

Tải bằng Maven 3.9.11 (`audit/bnx/deps/_tools`) ngày 2026-11-14: `mvn -B dependency:copy-dependencies -DoutputDirectory=.` với `pom.xml` cùng thư mục
(tomcat-embed-core 10.1.61 và tomcat-embed-jasper 10.1.61 từ repo1.maven.org; còn lại là phụ thuộc bắc cầu do Maven phân giải). Temurin JDK 21.0.13.
`.gitignore` đã bỏ tệp `.jar`; lấy lại bằng lệnh trên (cần Maven: xem `audit/bnx/deps/_tools/README.md`). `tomcat-embed-core` chứa cả Servlet API (`jakarta.servlet`).

| Tệp | sha256 |
|---|---|
| ecj-3.33.0.jar | f7686c4960cf70c2ebc5c500a73a8cfc04541b730c18f1c5c21329889b137f45 |
| tomcat-annotations-api-10.1.61.jar | 8d408d675d89da99f86171ead3067f9e947accf722e3785e6775e9af387ff3a6 |
| tomcat-embed-core-10.1.61.jar | 57b8e4bdb3a49163c3a6a501929240531523c111ff53844c9f82efba60f789f7 |
| tomcat-embed-el-10.1.61.jar | a72e0e067ae4e5b9aba0b36c7812cbe268c555648355c9d3e662bbff0d07f972 |
| tomcat-embed-jasper-10.1.61.jar | 8275586cefddf6b736c5b2c6d6d7703a6da271af61bf7674d05bdab43455fc9a |
