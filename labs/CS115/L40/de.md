# Lab CS115 L40 — UMAP: trọng số đối xứng hoá đồ thị 1 láng giềng gần nhất (1-NN)

Cho đồ thị 1 láng giềng gần nhất (**1-NN**, *1-Nearest Neighbor*) có các trọng số có hướng trong cụm `w01 = 1.0, w10 = 1.0` và giữa hai cụm `w12 = 0.02, w21 = 0.0`. Tính trọng số đối xứng `w_sym = w_ij + w_ji - w_ij * w_ji` cho cặp gần (`0-1`), cặp nối hai cụm (`1-2`) và kiểm điều kiện giữ cụm `w_near > 10 * w_cross`.

Định dạng đầu ra (2 dòng):
`w_near_01=<2 chữ số> w_cross_12=<4 chữ số>`
`keeps_cluster=<0 hoặc 1>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L40 duong_dan/bai_cua_ban.py
```
