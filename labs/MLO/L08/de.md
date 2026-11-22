# Lab MLO L08 — Giám sát trôi dữ liệu bằng chỉ số ổn định quần thể (PSI)

Tính chỉ số ổn định quần thể (`PSI = tổng (a_i - e_i) * ln(a_i / e_i)`) khi phân bố 4 nhóm thu nhập từ huấn luyện `exp = [0.20, 0.30, 0.30, 0.20]` dịch sang hiện tại `cur = [0.10, 0.20, 0.35, 0.35]`, và kiểm mức cảnh báo theo dõi (`0.1 <= psi < 0.25`).

Định dạng đầu ra:
`psi=<3 chữ số> alert_moderate=<1 hoặc 0>`

Chấm tự động:
```bash
bash labs/cham.sh MLO L08 duong_dan/bai_cua_ban.py
```
