# Lab PLC L05 — Kiểm tra kiểu tĩnh trên cây biểu thức JSON

Đọc hai cây JSON `ast1|ast2` từ `stdin` (dùng `json.loads(...)` sau khi tách theo `|`).
Mỗi nút trong cây có dạng:
- Nút lá: `["lit", kieu]` (ví dụ `["lit", "int"]`, `["lit", "str"]`).
- Nút phép toán: `[phep, trai, phai]` (ví dụ `["+", [...], [...]]`).
Kiểm tra đệ quy mỗi cây: nút lá trả về `kieu`; nút phép toán hợp lệ (trả về `'int'`) chỉ khi cả hai nhánh con đều có kiểu `'int'`, ngược lại trả về `None`.

In đúng 1 dòng `ok_expr=<0|1> err_expr=<0|1>` (`1` nếu hợp lệ / không phải `None`, `0` nếu lỗi).
Chấm tự động: `bash labs/cham.sh PLC L05 duong_dan/bai_cua_ban.py`
