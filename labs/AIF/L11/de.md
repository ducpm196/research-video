# Lab AIF L11 — Mạng Bayes cảm biến nhiệt: suy diễn hậu nghiệm

Đọc `stdin` chuỗi `p_h=<float> p_v=<float> a1=<0|1> a2=<0|1>`. Mạng Bayes gồm: nguyên nhân `H` (Quá nhiệt, xác suất `p_h`), `V` (Sụt áp, xác suất `p_v`) cùng trỏ vào chuông `A` với bảng điều kiện `P(A=1|H=1,V=1)=0.98`, `P(A=1|H=1,V=0)=0.90`, `P(A=1|H=0,V=1)=0.25`, `P(A=1|H=0,V=0)=0.005`; chuông `A` trỏ vào hai cảm biến `A1` (`P(A1=1|A=1)=0.85`, `P(A1=1|A=0)=0.04`) và `A2` (`P(A2=1|A=1)=0.75`, `P(A2=1|A=0)=0.02`). Tính xác suất hậu nghiệm `P(H=1 | A1, A2)` bằng liệt kê biên ẩn `V, A`.

In 1 dòng: `P_heat_given_A12=<.4f>`.
Chấm tự động: `bash labs/cham.sh AIF L11 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
