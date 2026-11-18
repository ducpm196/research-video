# Lab CS112 L07 — Danh sách kề, duyệt chiều rộng, chiều sâu và đếm vùng liên thông

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Không cần cài thêm thư viện.

Cách tạo tệp: mở một **trình soạn thảo chữ thuần** (Notepad, VS Code; không dùng Word), gõ nội dung, lưu với tên `do_thi.py` (đuôi `.py`, mã hoá UTF-8) vào **thư mục gốc của bộ khoá** (thư mục chứa `labs`), rồi mở Git Bash tại đó.

Đồ thị vô hướng 8 đỉnh `1…8`, các cạnh (số liệu minh hoạ, **khác ví dụ trong bài**): `(1,2) (1,3) (2,4) (3,4) (4,5) (6,7)`; đỉnh 8 không có cạnh nào.

1. **Danh sách kề**: từ điển `ke` gồm đỉnh → danh sách láng giềng (mỗi cạnh `(u, v)` thêm `v` vào danh sách của `u` **và** `u` vào danh sách của `v`); sắp xếp mỗi danh sách tăng dần bằng `.sort()`. In `danh sach ke 4: <láng giềng của 4>`.
2. **Duyệt chiều rộng** từ đỉnh 1 bằng hàng đợi (`from collections import deque`; `deque([s])`, lấy ra bằng `.popleft()`, xếp vào bằng `.append(x)`). Từ điển `d` ghi khoảng cách; đánh dấu một đỉnh (đặt `d[w]`) **ngay lúc xếp vào hàng đợi**. In `bfs tu 1: <thứ tự lấy ra khỏi hàng đợi>` và `khoang cach: <u>:<d[u]>` cho từng đỉnh theo thứ tự đó, cách nhau một dấu cách.
3. **Duyệt chiều sâu** bằng đệ quy từ đỉnh 1, xét láng giềng theo thứ tự trong danh sách kề (đã tăng dần), có tập `da_tham` các đỉnh đã thăm. In `dfs tu 1: <thứ tự thăm>`.
4. **Đếm vùng liên thông**: cho `u` từ 1 đến 8, nếu `u` chưa thăm thì tăng bộ đếm và duyệt sâu từ `u` (dùng chung một tập `da_tham`). In `so vung lien thong: <số>`.
5. In `6 toi duoc 1: co` nếu đỉnh 6 nằm trong các đỉnh duyệt chiều rộng tới được từ 1, ngược lại `6 toi duoc 1: khong`.

Chạy: `python do_thi.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh CS112 L07 do_thi.py`.
