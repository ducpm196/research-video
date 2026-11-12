# Thư viện ngoài của bài BNX L18 (JUnit 5 + Mockito)

Tải bằng `curl` từ Maven Central (`https://repo1.maven.org/maven2/`) ngày 2026-11-11. sha1 của từng tệp đã so khớp với tệp `.sha1` trên Maven Central.
Phiên bản byte-buddy, byte-buddy-agent, objenesis lấy đúng theo `mockito-core-5.24.0.pom`. Chạy trên JDK 21.0.13 (Temurin).

| Tệp | Phiên bản | Đường dẫn Maven | sha256 |
|---|---|---|---|
| junit-platform-console-standalone-1.14.4.jar | 1.14.4 (JUnit Jupiter 5.14.4) | org/junit/platform/junit-platform-console-standalone/1.14.4/ | 7c6968cbcaf4301c729f202b23b7d736c5d88be625fc7d27ad5d746146a8bc28 |
| mockito-core-5.24.0.jar | 5.24.0 | org/mockito/mockito-core/5.24.0/ | 97a1f835ad84075255aa37809e4379eff541273c02c6201cbad49bd5950932cd |
| byte-buddy-1.17.7.jar | 1.17.7 | net/bytebuddy/byte-buddy/1.17.7/ | 3575dcb8a98faf943d3c1595c47a16047c4fce8a83ebbb26262f1a2f67546357 |
| byte-buddy-agent-1.17.7.jar | 1.17.7 | net/bytebuddy/byte-buddy-agent/1.17.7/ | a9ba887dca252ad61b7d5153294f34e6f3bdf4b2736b04373d13615a695fc0ff |
| objenesis-3.3.jar | 3.3 | org/objenesis/objenesis/3.3/ | 02dfd0b0439a5591e35b708ed2f5474eb0948f53abf74637e959b8e4ef69bfeb |

Tải lại:
```
B=https://repo1.maven.org/maven2
curl -sfO $B/org/junit/platform/junit-platform-console-standalone/1.14.4/junit-platform-console-standalone-1.14.4.jar
curl -sfO $B/org/mockito/mockito-core/5.24.0/mockito-core-5.24.0.jar
curl -sfO $B/net/bytebuddy/byte-buddy/1.17.7/byte-buddy-1.17.7.jar
curl -sfO $B/net/bytebuddy/byte-buddy-agent/1.17.7/byte-buddy-agent-1.17.7.jar
curl -sfO $B/org/objenesis/objenesis/3.3/objenesis-3.3.jar
sha256sum *.jar
```
Dùng bởi `audit/bnx/ver/l18.py` (so sha256 rồi mới chạy) và `audit/bnx/screen/l18.yaml` (chép vào `lib/` của thư mục chạy tạm).
