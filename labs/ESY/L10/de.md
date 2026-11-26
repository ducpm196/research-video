# Lab ESY L10 — Lập lịch ưu tiên cố định so với EDF

Đọc `H|C0,T0;C1,T1` từ stdin (ví dụ `16|4,8;2,4`). Mô phỏng `t=0..H-1` đếm số trễ hạn theo từng luật.
Quy ước lab: luật ưu tiên cố định luôn lấy theo thứ tự nhập (tác vụ 0 ưu tiên cao hơn tác vụ 1); nếu EDF trùng hạn thì chọn tác vụ có chỉ số nhỏ hơn; khi kết thúc ở `t = H`, mỗi tác vụ còn phần việc `rem[i] > 0` tính thêm một lần trễ hạn.
In đúng 1 dòng `U=<1 chữ số> fixed_misses=<int> edf_misses=<int>`.
