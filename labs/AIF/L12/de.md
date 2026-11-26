# Lab AIF L12 — Lặp giá trị bất định 3 ô thẳng hàng tới ô đích +1.0

Đọc `stdin` chuỗi `r=<float> gamma=<float> iters=<int>`. Chạy `iters` vòng lặp Bellman đồng bộ trên 3 ô `[0, 1, 2]` với `U=[0.0, 0.0, 1.0]` cố định ô đích `U[2]=1.0`. Tại mỗi vòng từ giá trị cũ: `u1 = max(r + gamma*(0.7*u[2]+0.3*u[1]), r + gamma*(0.7*u[0]+0.3*u[1]))` và `u0 = max(r + gamma*(0.7*u[1]+0.3*u[0]), r + gamma*u[0])`, rồi gán `u[0], u[1] = u0, u1`.

In 1 dòng: `U0=<.3f> U1=<.3f>`.
Chấm tự động: `bash labs/cham.sh AIF L12 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
