# Lab LLM L07 — Sinh văn bản: nhiệt độ và lấy mẫu hạt nhân top-p

Cho dãy điểm thô `(3, 1.5, 0)`. Tính phân phối chuẩn hoá mũ (Softmax) ở nhiệt độ `T = 1.0` và `T = 0.6`. Sau đó cộng dồn xác suất lớn nhất ở `T = 1.0` theo danh sách giảm dần cho tới khi tổng `>= 0.85` và in tổng đó.

Định dạng đầu ra (1 dòng):
`T1=[<3 số làm tròn 3 chữ số>] T06=[<3 số làm tròn 3 chữ số>] top_p_sum=<3 chữ số>`
