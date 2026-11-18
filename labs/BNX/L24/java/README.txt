Mã Java đủ của bài 24 (các tệp trên màn hình chỉ hiện từng đoạn).
Cần JDK 21, Hibernate ORM 7.1.0.Final, H2 2.3.232 và các thư viện phụ thuộc (do Maven tải) trong thư mục lib.
Biên dịch: javac -encoding UTF-8 -cp "lib/*" -d out *.java
Chạy (Windows dùng dấu chấm phẩy, Linux dùng dấu hai chấm): java -cp "out;lib/*" DemSql
Các lớp chạy được: DemSql, DemN1, DemBan, DemLoi, DemNho, DemTrang. Đầu ra không in thời gian nên chạy lại ra y hệt.
