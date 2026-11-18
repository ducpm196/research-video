# Lab JVA L08 — Đối soát một tệp lệnh

Trong Git Bash, viết `DoiSoat` (tệp `DoiSoat.java`, số liệu là số minh hoạ). Hàm chính khai `throws Exception` (như ví dụ ghi rồi đọc tệp `DocTep.java` trong video).

Đầu tệp cần ba dòng nhập: `import java.nio.file.Files;`, `import java.nio.file.Path;`, `import java.util.Locale;`.

1. Ghi tệp `lenh.txt` bằng `Files.writeString(Path.of("lenh.txt"), …)` gồm **4 dòng**, mỗi dòng kết thúc bằng `\n`: `A001;1200000`, `A002;350000`, `A003;2000000`, `A004;75000`.
2. Đọc lại bằng `Files.readString`, tách dòng bằng `split("\n")`; mỗi dòng tách tiếp bằng `split(";")` rồi `Long.parseLong` phần số tiền.
3. In: `<số dòng> dong`; `Tong: <tổng, định dạng 3,625,000>`; `Tren 1 trieu: <số lệnh lớn hơn 1000000>`; rồi từng dòng `A001 | 1,200,000 dong`. Định dạng bằng `String.format(Locale.US, "%,d", …)`.

Chạy: `javac DoiSoat.java && java DoiSoat`. Chấm: `bash labs/cham.sh JVA L08 DoiSoat.java`.
