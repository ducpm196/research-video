# Lab CVI L09 — Phân đoạn ảnh: IoU, Dice và bẫy độ chính xác điểm ảnh

Trên một mặt nạ có `TP = 45, FP = 15, FN = 10`, tính IoU, Dice và xác nhận `Dice >= IoU`. Sau đó trên ảnh `100 × 100` có vật chỉ chiếm `2%` (`200` điểm ảnh), giả sử mô hình đoán toàn nền (`0` vật), tính độ chính xác điểm ảnh tổng thể và IoU thật của lớp vật.

Định dạng đầu ra (1 dòng):
`iou=<3 chữ số> dice=<3 chữ số> dice_ge_iou=<0 hoặc 1> acc_all_bg=<2 chữ số> iou_all_bg=<1 chữ số>`
