# Lab PAR L04 — Chia tĩnh so với việc dài trước (LPT) trên 2 lõi

Đọc danh sách độ dài việc `j0,j1,...` từ stdin (ví dụ `4,9,2,8,1,7,3,6`). So sánh thời gian hoàn thành (`makespan`, tức `C = max` thời gian 2 lõi) giữa chia nửa đầu–nửa sau và thuật toán việc dài trước (`LPT`: sắp giảm dần rồi gán việc tiếp theo cho lõi đang ít tải hơn, hoà chọn lõi 0).
In đúng 1 dòng `static_makespan=<int> lpt_makespan=<int>`.
