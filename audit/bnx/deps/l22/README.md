# Phụ thuộc của bài BNX L22 (Adobe Experience Manager: JCR, Sling, HTL, OSGi)

Chỉ để **biên dịch** lớp Sling Model hiện trên màn hình (`TrangModel.java`) và đọc chú thích của nó bằng phản chiếu. Không chạy máy chủ AEM hay Sling.
Tải bằng `curl` từ Maven Central ngày 2026-11-12; sha1 cục bộ trùng tệp `.sha1` do Maven Central công bố; JDK dùng: Temurin 21.0.13.

| Tệp | Phiên bản | sha256 | Kích thước (byte) | URL |
|---|---|---|---|---|
| `org.apache.sling.api-3.0.2.jar` | org.apache.sling:org.apache.sling.api:3.0.2 | `8b8b14abc3f273e35f5622152f83aa20951ed012c266b690d9a1487ab799ebae` | 257773 | https://repo1.maven.org/maven2/org/apache/sling/org.apache.sling.api/3.0.2/org.apache.sling.api-3.0.2.jar |
| `org.apache.sling.models.api-2.0.0.jar` | org.apache.sling:org.apache.sling.models.api:2.0.0 | `d7bbd7449c5cc2ba58ca055c0d96c67221d6cfe4ca03aa559b29094510b152f8` | 47803 | https://repo1.maven.org/maven2/org/apache/sling/org.apache.sling.models.api/2.0.0/org.apache.sling.models.api-2.0.0.jar |

sha1 (Maven Central): `9fd8164d14808bf9c93cb8c65670896a40482fdd` (sling.api), `9a6e53cd6ec9385aab1d1fac3e42ae28320890e3` (models.api).

Dùng: `audit/bnx/ver/l22.py` (kiểm sha256 rồi `javac -proc:none -cp "audit/bnx/deps/l22/*"`) và nguồn `L22_model` trong `audit/bnx/screen/l22.yaml`.
Thiếu tệp: bộ kiểm trả SKIP (cổng FAIL, NOT_VERIFIED); khối bash thoát 97. Không cài vào `.venv`, không sửa `requirements.txt`.
