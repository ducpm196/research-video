# Lab PLC L01 — Bộ tách từ tố cho biểu thức 'total = 108 - cnt'

Dùng `re.findall` với mẫu nhận chữ danh định `[A-Za-z_]\w*`, số nguyên `\d+` và toán tử `[=+*/-]` để tách chuỗi `'total = 108 - cnt'` thành danh sách các từ tố.

Định dạng đầu ra (1 dòng):
`count=<số nguyên> toks=<danh sách từ tố>`

Chấm tự động:
```bash
bash labs/cham.sh PLC L01 duong_dan/bai_cua_ban.py
```
