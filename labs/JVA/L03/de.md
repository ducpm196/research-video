# Lab JVA L03 — Lãi theo bậc tiền gửi

Trong Git Bash, viết `BacLai` (tệp `BacLai.java`), số liệu là số minh hoạ:

1. Số tiền gửi `soTien` lấy từ dòng lệnh nếu có, không thì mặc định **10 000 000**: `args.length > 0 ? Long.parseLong(args[0]) : 10000000`.
2. Lãi suất theo phần nghìn mỗi tháng: dưới **10 000 000** là **3**; từ 10 000 000 tới dưới **100 000 000** là **4**; từ 100 000 000 trở lên là **5**. Chuỗi `if … else if … else`.
3. In một dòng: `<soTien> -> suat <suat>, lai thang: <soTien * suat / 1000>`.
4. Chạy không đối số (phải ra dòng ở `mong_doi.txt`), rồi thử đúng ba số ở biên: `java BacLai 9999999` → `9999999 -> suat 3, lai thang: 29999`; `java BacLai 100000000` → `100000000 -> suat 5, lai thang: 500000`.

Chạy: `javac BacLai.java && java BacLai`. Chấm: `bash labs/cham.sh JVA L03 BacLai.java` (chấm khi không đối số).
