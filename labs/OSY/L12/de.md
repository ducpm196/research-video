# Lab OSY L12 (Mô phỏng inode) — Tính sức chứa tối đa của cấu trúc chỉ mục Unix

Viết chương trình Python tính số khối và dung lượng MiB/GiB cho khối `4 KiB` (`4 096 B`), con trỏ khối `4 B` (`1 024` con trỏ/khối), với 12 trực tiếp + 1 gián tiếp cấp 1 + 1 cấp 2, in đúng 3 dòng:
1. `direct_kib=48`
2. `single_ind_blocks=1024`
3. `double_ind_mib=4096`

Chấm tự động:
```bash
bash labs/cham.sh OSY L12 duong_dan/bai_cua_ban.py
```
