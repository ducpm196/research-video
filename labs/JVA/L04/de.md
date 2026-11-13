# Lab JVA L04 — Tiết kiệm sáu tháng

Gửi **50 000 000 đồng**, lãi **0,6% mỗi tháng** (số minh hoạ), lãi nhập vào gốc mỗi tháng. Tính bằng số nguyên theo đồng: `lai = soDu * 6 / 1000`.

Viết chương trình `TietKiem` (tệp `TietKiem.java`):
1. Dùng một vòng lặp đếm chạy 6 tháng. Mỗi tháng in một dòng đúng dạng `Thang 1: lai 300000, so du 50300000`.
2. Sau vòng lặp in một dòng `Thang dau tien vuot 51 trieu: <số tháng>`. Gợi ý: một biến nhớ tháng đầu tiên số dư vượt 51 000 000, chỉ gán khi biến còn bằng 0.

Chạy: `javac TietKiem.java && java TietKiem`. Chấm: `bash labs/cham.sh JVA L04 TietKiem.java`.
