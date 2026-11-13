# Lab BNK L03 — Bốn yêu cầu, hai khoá

Số dư đầu **3 000 000**; mỗi yêu cầu chuyển **trừ 700 000**. Bốn yêu cầu đến theo thứ tự với khoá lũy đẳng `k1`, `k1`, `k2`, `k1` (hai lần thử lại cùng khoá `k1`).

Viết chương trình `XuLyTrung` (tệp `XuLyTrung.java`):
1. Hàm `static long chuyen(String khoa)`: nếu `khoa` chưa xử lý thì trừ 700 000 vào số dư và nhớ **phản hồi** (số dư sau khi trừ); nếu đã xử lý thì **trả lại đúng phản hồi đã nhớ**, không trừ nữa. (Gợi ý: `Map<String, Long>` và `computeIfAbsent`.)
2. Với từng khoá trong dãy, in một dòng đúng dạng `k1 -> 2300000`.

Chạy: `javac XuLyTrung.java && java XuLyTrung`. Chấm: `bash labs/cham.sh BNK L03 XuLyTrung.java`.
