# Lab AIF L11 — Mạng Bayes cảm biến nhiệt: suy diễn hậu nghiệm P(Nóng | A1, A2)

Cho bảng xác suất gốc mạng cảm biến: `P(Quá_nhiệt=1)=0.01`, `P(Sụt_áp=1)=0.04`; bảng chuông `Báo_động`: `(1,1)->0.98`, `(1,0)->0.90`, `(0,1)->0.25`, `(0,0)->0.005`; hai cảm biến báo tín hiệu `A1` (khi kêu: `0.85` / yên: `0.04`) và `A2` (khi kêu: `0.75` / yên: `0.02`). Tính `P(Quá_nhiệt=1 | A1=1, A2=1)` bằng liệt kê qua biến ẩn.

Định dạng đầu ra:
`P_heat_given_A12=<4 chữ số thập phân>`

Chấm tự động:
```bash
bash labs/cham.sh AIF L11 duong_dan/bai_cua_ban.py
```
