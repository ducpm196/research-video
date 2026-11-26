# Lab CS115 L23 — MLP: hàm ReLU chuẩn, bão hoà Sigmoid và chuẩn Xavier

Đọc `stdin` `sx=<f> arr=<v1,v2,v3> nin=<int> nout=<int>`. Tính đạo hàm `sigmoid(sx)*(1-sigmoid(sx))`, ReLU trên `arr` và độ lệch chuẩn khởi tạo Xavier `sqrt(2 / (nin + nout))`.

In 3 dòng chuẩn: `dsigmoid_10=<.6e>`, `relu=<list>`, `xavier_std=<.4f>`.
Chấm tự động: `bash labs/cham.sh CS115 L23 duong_dan/bai_cua_ban.py`
