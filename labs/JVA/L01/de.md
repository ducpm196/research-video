# Lab JVA L01 — Số dư sau ba lệnh chuyển

Trong Git Bash, đứng trong thư mục làm việc của bạn. Viết chương trình `SoDu` (tệp `SoDu.java`), số liệu là số minh hoạ:

1. Dùng ba biến `long`: số dư đầu **1 500 000**, mỗi lệnh chuyển **250 000**, phí mỗi lệnh **2 200**. Tính `tongChuyen` và `tongPhi` cho **ba lệnh**, rồi **gán lại** `soDu = soDu - tongChuyen - tongPhi`. In ba dòng: `Tong chuyen: …`, `Tong phi: …`, `So du con lai: …`.
2. Cộng ba lần **800 000 000** hai cách: bằng biến `int` (in `Int: …`) và bằng biến `long` (in `Long: …`). Đoán trước kết quả `int`, rồi kiểm bằng `jshell`: gõ `800000000 + 800000000 + 800000000`.

Chạy: `javac SoDu.java && java SoDu`. Chấm: `bash labs/cham.sh JVA L01 SoDu.java`.
