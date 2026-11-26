# Lab CS115 L40 — UMAP: đối xứng hoá trọng số đồ thị 1-NN

Đọc `stdin` `w01=<f> w10=<f> w12=<f> w21=<f>`. Tính trọng số đối xứng `w_ij + w_ji - w_ij * w_ji` cho cặp nội cụm và nối cụm rồi kiểm `w_near > 10 * w_cross`.

In 2 dòng chuẩn: `w_near_01=<.2f> w_cross_12=<.4f>`, `keeps_cluster=<0|1>`.
Chấm tự động: `bash labs/cham.sh CS115 L40 duong_dan/bai_cua_ban.py`
