# Lab OSY L07 — Thuật toán Nhà băng (Banker) kiểm trạng thái an toàn

Đọc `stdin` 3 dòng riêng biệt: `avail=a,b,c`, `alloc=<r0;r1;...>`, `max=<r0;r1;...>`. Tính `need = max - alloc`, tìm dãy tiến trình an toàn theo chỉ số nhỏ nhất thoả `need <= work`. Nếu trạng thái **không** an toàn (`safe=0`), in `safe_seq=NONE` và `final_avail` bằng vector `work` tại thời điểm dừng.

In đúng 3 dòng: `safe=<0|1>`, `safe_seq=<P_csv>`, `final_avail=<csv>`.
Chấm tự động: `bash labs/cham.sh OSY L07 duong_dan/bai_cua_ban.py`
