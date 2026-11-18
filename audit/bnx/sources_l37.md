# Nguồn của bài BNX L37 (soạn 2026-11-14; cùng định dạng bảng với audit/bnx/sources.md, để người điều phối gộp)

Bài tách từ phần SQL Server, chèn mã, JDBC của L06 cũ (3 054 từ). Mọi kết quả trên màn hình là đầu ra THẬT: SQL Server 2022 (bnx-mss, `@@VERSION` = Microsoft SQL Server 2022 (RTM-CU27-GDR) (KB5129300) 16.0.4315.2, Developer Edition trên Linux), Oracle AI Database 26ai Free 23.26.3 (bnx-ora) qua JDBC `ojdbc11-23.26.4.0.0`, Temurin JDK 21.0.13. `audit/bnx/ver/l37.py` chạy lại tất cả.

| Mã | Dữ kiện | Nguồn | Mức |
|---|---|---|---|
| [S1] | `SET XACT_ABORT`: khi OFF, thường chỉ câu lệnh gây lỗi bị huỷ và giao dịch tiếp tục; khi ON, lỗi lúc chạy huỷ cả giao dịch. Mặc định của phiên là OFF (đo bằng `@@OPTIONS & 16384` = 0) | Microsoft Learn, "SET XACT_ABORT (Transact-SQL)" — learn.microsoft.com/sql/t-sql/statements/set-xact-abort-transact-sql | CITED + OBSERVED |
| [S2] | `BEGIN TRY…END TRY BEGIN CATCH…END CATCH`, `THROW` (một mình trong khối CATCH ném lại lỗi), `@@TRANCOUNT` | Microsoft Learn, "TRY...CATCH", "THROW", "@@TRANCOUNT (Transact-SQL)" | CITED |
| [S3] | `sp_executesql`: chạy câu lệnh Unicode ghép sẵn, có tham số khai riêng (`@stmt`, `@params`) | Microsoft Learn, "sp_executesql (Transact-SQL)" | CITED + OBSERVED (0 dòng với chuỗi tấn công) |
| [S4] | `LEAST`/`GREATEST` có từ SQL Server 2022 | Microsoft Learn, "LEAST (Transact-SQL)" | CITED |
| [S5] | Chèn mã (SQL injection): chuỗi `X' OR '1'='1` ghép vào câu lệnh làm điều kiện luôn đúng; đo 2, 200, 20 000 dòng lộ ra ở bảng 2, 200, 20 000 dòng; truyền tham số lộ 0 dòng | đo trên SQL Server thật, `ver/l37.py` mục 3–4 | OBSERVED |
| [S6] | Java `CallableStatement` (`{call …(?,…)}`, `registerOutParameter`, `getString`), `PreparedStatement` (`?`, `setString`), `DriverManager.getConnection`, try-with-resources tự đóng `AutoCloseable`, `System.getenv` | Java SE 21 API, gói `java.sql`, `java.lang.System` (docs.oracle.com/en/java/javase/21/docs/api/) | CITED; chạy thật qua ojdbc |
| [S7] | Trình điều khiển `com.oracle.database.jdbc:ojdbc11:23.26.4.0.0`; sha1 `109dbf464e05f2f1770ea05df582170f069c2d29` khớp tệp `.sha1` Maven Central do phiên 2026-11-11 ghi; tệp chép lại từ thư mục tạm của phiên đó, chưa tải lại từ mạng | `audit/bnx/deps/l37/README.md` | OBSERVED (nguồn gốc tệp: một lần kiểm sha1, chưa kiểm lại với mạng) |
| [S8] | Mã lỗi Oracle `ORA-20001` từ `RAISE_APPLICATION_ERROR(-20001, …)` đến Java qua `SQLException.getErrorCode()` = 20001 (số dương, không dấu âm) | đo bằng chương trình `Goi` (đầu ra `500000: loi 20001`) | OBSERVED |
| [L37SCOPE] | Bài chỉ chạy JDBC với Oracle (thư viện sẵn có); lệnh gọi `CallableStatement` là chuẩn JDBC, với SQL Server chỉ đổi địa chỉ kết nối và thư viện — điều này bài KHÔNG chạy thử (nói rõ "ta chạy thử với Oracle"). Số tiền, tên tài khoản, kích thước bảng đều là số minh hoạ | — | không phải sự kiện sản phẩm |
