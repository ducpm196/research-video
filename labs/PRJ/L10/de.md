# Dự án PRJ L10 — Tổng hợp Chặng 11: PID, lập lịch RMS & cây Merkle

Đọc từ luồng chuẩn (`stdin`) 3 dòng:
- Dòng 1: `tasks=<C1,T1;C2,T2;...>` (thời lượng thực thi và chu kỳ của các tác vụ thời gian thực)
- Dòng 2: `kp=<float> target=<float> steps=<int>` (hệ số tỉ lệ, điểm đặt và số bước vòng lặp từ `x=0.0`)
- Dòng 3: `leaves=<tx0,tx1,tx2,tx3> tamper_idx=<int>` (4 nhãn lá và chỉ số lá cần thử chèn ký tự `'*'`)

Yêu cầu chương trình Python:
1. Tính tổng hệ số sử dụng CPU `U = sum(C_i / T_i)` và kiểm tra `U <= n * (2**(1/n) - 1)` với `n` là số tác vụ.
2. Chạy `steps` bước điều khiển tỉ lệ rời rạc `x += kp * (target - x)` bắt đầu từ `x = 0.0`.
3. Tính gốc Merkle SHA-256 trên danh sách 4 lá ban đầu và danh sách sau khi gắn thêm `'*'` vào phần tử `leaves[tamper_idx]`, kiểm tra hai gốc khác nhau (`merkle_tamper_detected=1`).

In đúng 3 dòng:
```
rms_u=<.2f> schedulable=<0_hoặc_1>
pid_step5=<.3f>
merkle_tamper_detected=<0_hoặc_1>
```

Chấm tự động:
```bash
bash labs/cham.sh PRJ L10 duong_dan/bai_cua_ban.py
```
