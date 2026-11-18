# Thư viện ngoài của bài BNX L24 (Hibernate ORM + H2)

Tải bằng Maven 3.9.11 (chạy thật ở `audit/bnx/deps/_tools/apache-maven-3.9.11`, tải từ Maven Central, sha512 khớp tệp `.sha512` của Central) ngày 2026-11-13:
`mvn -B dependency:copy-dependencies -DoutputDirectory=.` với `pom.xml` cùng thư mục (hibernate-core 7.1.0.Final, h2 2.3.232; các thư viện còn lại là phụ thuộc bắc cầu do Maven phân giải).
Chạy trên Temurin JDK 21.0.13. `.gitignore` đã bỏ tệp `.jar`; lấy lại bằng lệnh trên (cần Maven: giải nén `apache-maven-3.9.11-bin.zip` từ https://repo1.maven.org/maven2/org/apache/maven/apache-maven/3.9.11/).

| Tệp | sha256 |
|---|---|
| angus-activation-2.0.2.jar | 6dd3bcffc22bce83b07376a0e2e094e4964a3195d4118fb43e380ef35436cc1e |
| antlr4-runtime-4.13.2.jar | dd3e8a13a2d669bf84fb8d834de35ce4875f27157698d206241ec8488aadcaf7 |
| byte-buddy-1.17.6.jar | d26382a839cb26d5c62a0b0f04715bcef55a531f96ac6ce40de452a1c0539e70 |
| classmate-1.7.0.jar | cb868f231c5cceb89d795ea00e6e1b7a93b8f4ac1ce1d8be76dde322dff4a046 |
| h2-2.3.232.jar | 8dae62d22db8982c3dcb3826edb9c727c5d302063a67eef7d63d82de401f07d3 |
| hibernate-core-7.1.0.Final.jar | 3d290966bbc074597c26cd2a975827fe37d5fe2951f3394a0cafe9ccf21eee3a |
| hibernate-models-1.0.1.jar | bdb42c4979001742ebc098f3b206dd1057dc93be55c50a31c3f027d3eed06412 |
| istack-commons-runtime-4.1.2.jar | 7fd6792361f4dd00f8c56af4a20cecc0066deea4a8f3dec38348af23fc2296ee |
| jakarta.activation-api-2.1.3.jar | 01b176d718a169263e78290691fc479977186bcc6b333487325084d6586f4627 |
| jakarta.inject-api-2.0.1.jar | f7dc98062fccf14126abb751b64fab12c312566e8cbdc8483598bffcea93af7c |
| jakarta.persistence-api-3.2.0.jar | be8a26b0e75c84c1b7600f759256fbc68d60333d89ec0ce3f784fc3ffa09aa8c |
| jakarta.transaction-api-2.0.1.jar | 50c0a7c760c13ae6c042acf182b28f0047413db95b4636fb8879bcffab5ba875 |
| jakarta.xml.bind-api-4.0.2.jar | 0d6bcfe47763e85047acf7c398336dc84ff85ebcad0a7cb6f3b9d3e981245406 |
| jaxb-core-4.0.5.jar | ad3fd9bf00de3eda9859f70b6cfb011e2fe9904804e16a2665092888ece0fdca |
| jaxb-runtime-4.0.5.jar | 485d8940e76373a7f300815ea5504bf5b726c234425ad30971019d133124cca4 |
| jboss-logging-3.6.1.Final.jar | 5e08a4b092dc85b337f0910a740571d8720cfa565fabd880a8caf94a657ca416 |
| txw2-4.0.5.jar | 917355bc451481f30d043b24d123110517966af34383901773882810dca480e5 |
