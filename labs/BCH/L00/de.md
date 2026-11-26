# Lab BCH L00 — Cây quyết định nhu cầu chuỗi khối

Đọc `n|s,w,ttp,trust|s,w,ttp,trust` từ stdin (ví dụ `5|1,1,1,0|1,1,0,0`), trong đó: `s` = cần lưu trạng thái chung (`1` = có, `0` = không); `w` = nhiều bên cùng ghi (`1` = có, `0` = không); `ttp` = có bên mọi người cùng tin (`1` = có, `0` = không); `trust` = các bên đã tin nhau (`1` = đã tin nhau, `0` = chưa tin nhau — là phần bù của câu ④ “có không tin nhau không?”). Chỉ cần chuỗi khối (`1`) khi `s=1 and w=1 and ttp=0 and trust=0`.
Tính ngưỡng quá bán `n // 2 + 1` (ví dụ `5 // 2 + 1 = 3`) và đặt `central_ops=1` (chi phí hệ thống tập trung quy ước làm mốc đối chiếu = 1). Lưu ý: mọi ca (kể cả `n` khác 5 ở ca ẩn) đều giữ nguyên tên khoá đầu ra `maj_quorum_5=`.
In đúng 1 dòng `central_ops=1 maj_quorum_5=<int> school_need=0/1 rivals_need=0/1`.
