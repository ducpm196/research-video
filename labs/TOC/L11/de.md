# Lab TOC L11 — Kiểm chứng nghịch lý đường chéo trên bảng 3×3 của bài toán dừng

Cho bảng dự đoán giả định 3×3 `rows = [[1, 0, 1], [0, 0, 1], [1, 1, 0]]` ứng với `H(P_i, P_j)` (`1` là dừng, `0` là lặp vô hạn). Duyệt từng hàng ứng viên `D = [d0, d1, d2]` trong `2^3 = 8` khả năng hành vi trên 3 đầu vào để kiểm chứng: nếu `D == row[idx]` thì bắt buộc `D[idx] == 1 - row[idx]` là điều không thể xảy ra.

Định dạng đầu ra (1 dòng):
`table_size=<số> candidates=<số> possible_matches=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh TOC L11 duong_dan/bai_cua_ban.py
```
