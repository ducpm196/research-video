# Lab PLC L10 — Máy ảo ngăn xếp giữ đúng thứ tự toán hạng trừ trên biểu thức hậu tố

Thực thi dãy lệnh máy ảo ngăn xếp `['PUSH 12', 'PUSH 3', 'PUSH 2', 'MUL', 'SUB']`, lấy `b = pop()` (số trừ) trước `a = pop()` (số bị trừ) để tính đúng `a - b`.

Định dạng đầu ra (1 dòng):
`vm_result=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh PLC L10 duong_dan/bai_cua_ban.py
```
