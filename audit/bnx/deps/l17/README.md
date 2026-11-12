# Thư viện ngoài của bài BNX L17 (Spring Security 7.1.2 chạy thật, không cần máy chủ web)

Tải bằng `curl` từ Maven Central (`https://repo1.maven.org/maven2/`) ngày 2026-11-11. Phiên bản Spring Framework (7.0.10), micrometer-observation (1.17.2)
và nimbus-jose-jwt (10.9.1) lấy đúng theo các tệp `.pom` của spring-security 7.1.2; commons-logging 1.3.5 và jspecify 1.0.1 theo `spring-core-7.0.10.pom`.
Chạy trên JDK 21.0.13 (Temurin). spring-test chỉ dùng cho yêu cầu/trả lời giả (MockHttpServletRequest/Response, MockServletContext).

| Tệp | Đường dẫn Maven | sha256 |
|---|---|---|
| commons-logging-1.3.5.jar | commons-logging/ | 6d7a744e4027649fbb50895df9497d109f98c766a637062fe8d2eabbb3140ba4 |
| jakarta.servlet-api-6.1.0.jar | jakarta/servlet/ | 8a31f465f3593bf2351531a5c952014eb839da96a605b5825b93dd54714c48c4 |
| jspecify-1.0.1.jar | org/jspecify/ | 070d75f261fe4c5b8202508366715f7f2d4660f88c8ef7e6d3575e48c9683b66 |
| micrometer-commons-1.17.2.jar | io/micrometer/ | af8c85e879025ce30c381e6810e14c4f52b4150894e36c815860d14763271348 |
| micrometer-observation-1.17.2.jar | io/micrometer/ | d3ff53cfa0532dc1af0de349073f9aeb985e01f4b88c1d904350178805859695 |
| nimbus-jose-jwt-10.9.1.jar | com/nimbusds/ | 33152ea83ec50d22706fdaf3b07acbcd716f9a68edcabdd7c4d02843cbdcdcf6 |
| spring-aop-7.0.10.jar | org/springframework/ | babf50a645f4f788e1267078cf891e472f657cabf65518055cf5214220574e3f |
| spring-beans-7.0.10.jar | org/springframework/ | bd67c6fc887afa30cbcb489ff4f82bf19f818e79ab1cf1bef98dff8a289108ec |
| spring-context-7.0.10.jar | org/springframework/ | f0065166b6a5101a871ab8702d6c4011cf39faed370a64e7ef14a3ad2bf2a99a |
| spring-core-7.0.10.jar | org/springframework/ | a236f31a7c07e3a1a8e7839ec5c0d47b5cc75709132db50416d5dad320341f12 |
| spring-expression-7.0.10.jar | org/springframework/ | 12067b66548f7613fa8938ca6051a6d1dd8c397bf478e0bb1adb9936358ec81d |
| spring-security-config-7.1.2.jar | org/springframework/security/ | 826af4e79495d54b761a5f0313774a07d36359e83dd5518d57d69bacd7bbf478 |
| spring-security-core-7.1.2.jar | org/springframework/security/ | 39df3dc77436d3e9308f89056c1a42605e08f0ad9ad208f7e34c4b16102886e1 |
| spring-security-crypto-7.1.2.jar | org/springframework/security/ | 4aaa60bb612d5fece004c07f893b3a8d707c207bbd8585d10e0015b5301cd864 |
| spring-security-oauth2-core-7.1.2.jar | org/springframework/security/ | aa50c141cb303bae1b87d761f9459930d75af280c43e80b7488d50e62dd1e216 |
| spring-security-oauth2-jose-7.1.2.jar | org/springframework/security/ | e956dcaf0342699b967b5ca301d628d0808e97c7e6614b822fe832f6eba762dc |
| spring-security-oauth2-resource-server-7.1.2.jar | org/springframework/security/ | a154ce053da747c0be4144794cf2bd835b6cd56e09d1b4b2a62dfdcda6d273fb |
| spring-security-web-7.1.2.jar | org/springframework/security/ | fc36d37695462dbe4fb32bd6820043afbf83ebcffce4974929bf79a29fcb5e73 |
| spring-test-7.0.10.jar | org/springframework/ | 73c18292b63e814c415c1c470fcc47be1e21442b80ee31a0bcd949e53d0c49bd |
| spring-web-7.0.10.jar | org/springframework/ | 76ddb03d236547f6852def8cb303e1cf2cd2c1954dec5bf2abd87d11b89dfee7 |

Tải lại: với mỗi tệp `<tên>-<phiên bản>.jar` ở bảng trên, `curl -sfO https://repo1.maven.org/maven2/<đường dẫn Maven><tên>/<phiên bản>/<tệp>`, rồi `sha256sum *.jar`.
Dùng bởi `audit/bnx/ver/l17.py` (so sha256 rồi mới chạy) và `audit/bnx/screen/l17.yaml` (chép vào `lib/` của thư mục chạy tạm; thiếu thì thoát 97, NOT_VERIFIED).
