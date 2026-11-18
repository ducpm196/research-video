Mã đủ của các ví dụ trong video BNX L25 (trên màn hình chỉ hiện đoạn trích).
Cần các tệp jar: spring-context, spring-jdbc, spring-tx, spring-aop, spring-beans, spring-core, aspectjweaver 1.9.24, h2 2.3.232 (Spring 7.0.10, JDK 21).
Dựng và chạy (Git Bash, jar đặt trong thư mục lib):
  javac -encoding UTF-8 -cp "lib/*" -d out *.java
  java -cp "out;lib/*" DemTx        # rồi DemCoLap, DemBe
Đầu ra khớp phần Kết quả chạy thật trong video.
