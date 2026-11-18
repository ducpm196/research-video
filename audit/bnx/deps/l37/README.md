# Thư viện ngoài của bài BNX L37 (trình điều khiển JDBC của Oracle)

| Tệp | sha256 | sha1 |
|---|---|---|
| ojdbc11-23.26.4.0.0.jar | df977e9291499cd4ceee7d577462c285987dd2ad0216637c0865eb98956a9e6e | 109dbf464e05f2f1770ea05df582170f069c2d29 |

Nguồn: `com.oracle.database.jdbc:ojdbc11:23.26.4.0.0` trên Maven Central (https://repo1.maven.org/maven2/com/oracle/database/jdbc/ojdbc11/23.26.4.0.0/).
Tệp do phiên làm việc 2026-11-11 tải về (khi đó sha1 khớp tệp `.sha1` của Maven Central, ghi ở sổ `audit/bnx/screen/l06.yaml` cũ); phiên 2026-11-14 chép lại
từ thư mục tạm của phiên đó, kiểm lại sha1 `109dbf46…` khớp con số đã ghi, chưa tải lại từ mạng. Tải lại: `curl -sfLO <URL>/ojdbc11-23.26.4.0.0.jar`
(rồi so sha1 với `.sha1` cùng thư mục). `.gitignore` bỏ tệp `.jar`. Thiếu tệp này, nguồn `L37_ChayJdbc` thoát 97 (NOT_VERIFIED), không PASS lặng lẽ.
Chạy trên Temurin JDK 21.0.13, kết nối tới container `bnx-ora` (cổng 1521, dịch vụ FREEPDB1).
