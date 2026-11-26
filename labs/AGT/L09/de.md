# Lab AGT L09 — An toàn quyền công cụ trước chèn lời nhắc gián tiếp

Đọc `stdin` `policy=<act:perm,...> actions=<a1,a2,...> check=<act>`. Lọc hành động phép `'allow'` chạy tự động và xuất trạng thái quyền của `check`.

In 1 dòng: `auto_executed=<list> blocked=<perm>`.
Chấm tự động: `bash labs/cham.sh AGT L09 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
