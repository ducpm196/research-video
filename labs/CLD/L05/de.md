# Lab CLD L05 — Vòng đối chiếu trạng thái mong muốn và thực tế

Viết hàm `reconcile(desired, running)` nhận trạng thái mong muốn `desired = ['p1', 'p2', 'p3', 'p4']` và trạng thái đang chạy `running = ['p1', 'p3']`. Tính danh sách các bản cần khởi tạo mới (`created`), cập nhật `running` khớp `desired`, và kiểm tra kết quả sau 1 vòng.

Định dạng đầu ra (2 dòng):
`created=<danh sách>`
`converged=<1 hoặc 0>`

Chấm tự động:
```bash
bash labs/cham.sh CLD L05 duong_dan/bai_cua_ban.py
```
