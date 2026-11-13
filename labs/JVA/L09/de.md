# Lab JVA L09 — Thống kê giao dịch

Trong Git Bash, viết `ThongKe` (tệp `ThongKe.java`, số liệu là số minh hoạ). Nhớ `import java.util.ArrayList;` và `import java.util.HashMap;`.

1. Mảng loại giao dịch `{"CK", "NAP", "CK", "RUT", "CK", "NAP", "CK"}`. Đếm số lần mỗi loại bằng `HashMap<String, Integer>` và `getOrDefault`.
2. Danh sách `ArrayList<Long>` gồm `300000, 900000, 120000, 450000`. Sắp **giảm dần** bằng `tien.sort((a, b) -> Long.compare(b, a));`.
3. In đúng năm dòng: `So giao dich: …` (độ dài mảng), `CK: …`, `NAP: …`, `RUT: …`, `Lon truoc: [...]` (in thẳng danh sách).

Chạy: `javac ThongKe.java && java ThongKe`. Chấm: `bash labs/cham.sh JVA L09 ThongKe.java`.
