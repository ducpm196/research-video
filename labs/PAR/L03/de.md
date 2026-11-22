# Lab PAR L03 — Điều kiện tranh chấp 2 luồng tăng 3 lần: mất cập nhật còn 3 thay vì 6

Mô phỏng hai luồng cùng tăng biến đếm chung `c = 0` tổng cộng 3 lượt mỗi luồng nhưng bị đọc-cộng-ghi xen kẽ mất nửa số lần cập nhật so với phép cộng nguyên tử.

Định dạng đầu ra (1 dòng):
`racy_final=<số nguyên> expected_atomic=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh PAR L03 duong_dan/bai_cua_ban.py
```
