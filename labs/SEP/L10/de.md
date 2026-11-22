# Lab SEP L10 — Đếm số gói chịu ảnh hưởng bắc cầu trên cây phụ thuộc khi rút gói 'leftpad'

Cho đồ thị phụ thuộc ngược `rev = {'leftpad': ['tpl', 'cli'], 'tpl': ['web'], 'web': ['app'], 'cli': ['app'], 'app': []}`. Duyệt tìm tất cả các gói phía trên phụ thuộc trực tiếp hoặc bắc cầu vào `'leftpad'`.

Định dạng đầu ra (1 dòng):
`broken_upstream=<số nguyên> pkgs=<danh sách sắp xếp>`

Chấm tự động:
```bash
bash labs/cham.sh SEP L10 duong_dan/bai_cua_ban.py
```
