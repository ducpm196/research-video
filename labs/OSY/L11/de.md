# Lab OSY L11 (Mô phỏng tập làm việc) — Phát hiện và chặn hiện tượng trì trệ

Viết chương trình Python kiểm tra hệ thống `1 000` khung vật lý khi `4` tiến trình mỗi tiến trình cần `300` trang (`D = 1200 > 1000`), và sau khi tạm dừng 1 tiến trình (`900 <= 1000`), in đúng 3 dòng:
1. `demand_4procs=1200 thrashing=1`
2. `demand_after_suspend=900 thrashing=0`
3. `free_frames_after=100`

Chấm tự động:
```bash
bash labs/cham.sh OSY L11 duong_dan/bai_cua_ban.py
```
