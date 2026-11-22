# Lab CVI L11 — Học lối tắt trên đặc trưng giả: kiểm thử đổi nền

Tạo dữ liệu giả lập `train_set`: `100` ảnh bò gồm `90` con đứng trên nền cỏ (`has_grass=True`) và `10` con trên nền khác; tạo thêm `snow_set`: `25` ảnh bò trên nền tuyết (`has_grass=False`). Áp dụng bộ phân loại lối tắt `predict = has_grass` lên từng ảnh để tính tỉ lệ đoán trúng (%) trên cả hai tập.

Định dạng đầu ra (1 dòng):
`spur_train=<số nguyên>% counterexample_snow=<số nguyên>%`
