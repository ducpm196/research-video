# Lab PLC L05 — Kiểm kiểu tĩnh đệ quy trên cây phép toán (+, -, *, /) bắt lỗi int + str

Cài hàm đệ quy `check_tree(node)` cho cây phép toán gồm lá `('lit', kieu)` và nút `(op, trai, phai)` với `op` thuộc `{'+', '-', '*', '/'}`: chỉ hợp lệ khi hai nhánh cùng kiểu `'int'`. Kiểm tra cây đúng `('+', ('lit','int'), ('*', ('lit','int'), ('lit','int')))` và cây lỗi `('-', ('lit','int'), ('lit','str'))`.

Định dạng đầu ra (1 dòng):
`ok_expr=<0 hoặc 1> err_expr=<0 hoặc 1>`

Chấm tự động:
```bash
bash labs/cham.sh PLC L05 duong_dan/bai_cua_ban.py
```
