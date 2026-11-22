# Lab DSC L04 — Trung vị, khoảng tứ phân vị (IQR) và hàng rào Tukey trước ngoại lai

Từ dãy `[2.0, 4.0, 6.0, 8.0, 9.0, 10.0, 12.0, 80.0]` (`n = 8`), sắp xếp rồi tính trung bình, trung vị, hai điểm tứ phân vị `Q1, Q3` (trung vị nửa dưới & nửa trên) và ngưỡng rào trên `Q3 + 1.5 * IQR` (với `IQR = Q3 - Q1`), kiểm `max > rào trên`.

Định dạng đầu ra:
`mean=<1 chữ số> median=<1 chữ số> fence=<1 chữ số> outlier=<1 hoặc 0>`

Chấm tự động:
```bash
bash labs/cham.sh DSC L04 duong_dan/bai_cua_ban.py
```
