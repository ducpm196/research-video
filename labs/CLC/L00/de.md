# Lab CLC L00 — Ma trận trách nhiệm chia sẻ 4 mô hình đám mây

Xét hệ thống gồm 5 lớp `['Hardware', 'OS', 'Runtime', 'App', 'Data']` (phần cứng, hệ điều hành, môi trường chạy, mã ứng dụng, dữ liệu). Tính số lớp khách hàng tự quản lý cho bốn mô hình: hạ tầng như dịch vụ (`IaaS`: khách hàng tự quản các lớp phía trên phần cứng), nền tảng như dịch vụ (`PaaS`: chỉ tự quản mã ứng dụng và dữ liệu), hàm theo sự kiện (`FaaS`: chỉ tự quản mã hàm ở lớp ứng dụng và dữ liệu), phần mềm như dịch vụ (`SaaS`: chỉ tự quản lớp dữ liệu), rồi tính mức chênh lệch số lớp giữa `IaaS` và `SaaS`.

Định dạng đầu ra (3 dòng):
`iaas_layers=<số>`
`paas_faas_saas=<a,b,c>`
`iaas_minus_saas=<số>`

Chấm tự động:
```bash
bash labs/cham.sh CLC L00 duong_dan/bai_cua_ban.py
```
