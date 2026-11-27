# Lab ESY L02 — Chống dội phím bằng đếm mẫu liên tiếp

Đọc `k|m0,m1,...` từ stdin (ví dụ `5|0,1,0,1,1,0,1,1,1,1,1,1`), mỗi mẫu là một nhịp 1 ms, trạng thái sạch ban đầu là `0`. Chỉ đổi trạng thái khi gặp `k` mẫu giống nhau liên tiếp; `accepted_at_ms` là chỉ số mẫu đầu tiên đạt trạng thái `1` (in `-1` nếu chưa từng đạt). Đếm `raw_edges` và `clean_edges` theo số lần đổi chiều cả hai hướng (`a != b` giữa hai mẫu kề nhau) trước và sau chống dội.
In đúng 1 dòng `accepted_at_ms=<int> raw_edges=<int> clean_edges=<int>`.
