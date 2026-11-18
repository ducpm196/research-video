# Lab CS112 L18 — Đổi tiền với mệnh giá 1, 4, 6: bảng từ dưới lên, ghi nhớ từ trên xuống, tham lam sai

Cần: Python 3.11 trở lên. Tạo `doi_tien.py` (số liệu minh hoạ, khác ví dụ trong bài). Mệnh giá `(1, 4, 6)`.

1. Lập bảng `dp[a]` từ dưới lên: số đồng ít nhất để đổi số tiền `a`, với `a` từ 0 đến 20 (`dp[0] = 0`; `dp[a] = 1 + min(dp[a - c])` cho mọi mệnh giá `c <= a`). In `dp: ` và 13 số đầu (`a` từ 0 đến 12), cách nhau một dấu cách.
2. Dựng lại cách đổi 8: từ `a = 8` lùi theo đồng đã dùng (duyệt mệnh giá tăng dần, lấy đồng đầu tiên cho `1 + dp[a - c] == dp[a]`). In `Doi 8: dp <số đồng> dong (<các đồng, từ lớn tới nhỏ>), tham lam <số đồng> dong`, trong đó "tham lam" là lấy đồng lớn nhất còn vừa, lặp lại.
3. In `Tham lam sai o a = ` và danh sách các `a` từ 1 đến 20 mà tham lam cho nhiều đồng hơn `dp`, cách nhau dấu phẩy rồi dấu cách.
4. Đếm lời gọi: viết hàm đệ quy thô `f(a)` (không ghi nhớ) và hàm đệ quy có ghi nhớ bằng từ điển, mỗi hàm tăng một biến đếm mỗi lần được gọi (kể cả lần dừng ở `a == 0` và lần tra bảng). In `Goi f(20): tho <số>, ghi nho <số>`.

Cú pháp cần dùng ở mục 4 (nếu chưa gặp): từ điển `nho = {}` lưu kết quả đã tính: `nho[a] = giatri` ghi, `a in nho` hỏi đã có chưa, `nho[a]` đọc. Biến đếm dùng chung cho mọi lời gọi: đặt `dem = [0]` ở ngoài hàm, trong hàm viết `dem[0] += 1`; hoặc đặt `dem = 0` ở ngoài và viết `global dem` ở dòng đầu của hàm để hàm được sửa biến ngoài.

Chạy: `python doi_tien.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L18 doi_tien.py`.
