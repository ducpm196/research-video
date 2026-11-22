# Lab AGT L09 — An toàn cho tác tử trước chèn lời nhắc gián tiếp

Cho bảng chính sách quyền công cụ `policy = {'read_file': 'allow', 'email_ext': 'confirm', 'pay_wire': 'confirm', 'exec_shell': 'deny'}` và danh sách `actions = ['read_file', 'email_ext', 'pay_wire', 'exec_shell']` do trang web lạ kích hoạt. Lọc các hành động tự động chạy (`'allow'`) và kiểm tra trạng thái của `'exec_shell'`.

Định dạng đầu ra (1 dòng):
`auto_executed=<danh sách> blocked=<trạng thái>`
