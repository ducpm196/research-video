# Lab CS115 L32 — t-SNE: đo độ bất đối xứng của độ lệch KL(P || Q)

Dùng lôgarit tự nhiên `ln` (`math.log`) tính độ lệch `KL(P || Q) = sum(p * ln(p / q))` và `KL(Q || P)` cho hai phân phối `P = [0.7, 0.3]`, `Q = [0.4, 0.6]`, kiểm chứng bất đối xứng và `KL >= 0`.

Định dạng đầu ra (2 dòng):
`KL_PQ=<6 chữ số> KL_QP=<6 chữ số>`
`asymmetric=<0 hoặc 1> nonneg=<0 hoặc 1>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L32 duong_dan/bai_cua_ban.py
```
