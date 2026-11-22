# Lab AIF L01 — Tìm đường ngắn nhất theo chiều rộng và kiểm đích khi sinh nút

Chạy tìm theo chiều rộng từ đỉnh `S` tới đích `G` trên đồ thị có hướng `{'S':['A','B'], 'A':['C','D'], 'B':['G'], 'C':['G'], 'D':[], 'G':[]}`. Theo đúng quy ước kiểm đích ngay khi sinh nút kề: đếm độ dài đường ngắn nhất (`shortest`), số nút đã lấy ra mở rộng (`expanded`, gồm `S, A, B`), và số nút đã thăm (`visited`).

Định dạng đầu ra:
`shortest=<số> expanded=<số> visited=<số>`

Chấm tự động:
```bash
bash labs/cham.sh AIF L01 duong_dan/bai_cua_ban.py
```
