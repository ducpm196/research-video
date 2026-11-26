# Lab OSY L11 — Phát hiện và chặn hiện tượng trì trệ (Thrashing)

Đọc `stdin` `cap=<int> n_procs=<int> per_proc=<int> suspend=<int>`. Tính tổng cầu tập làm việc trước và sau khi tạm dừng `suspend` tiến trình.

In đúng 3 dòng (giữ nguyên tên khoá cố định `demand_4procs` ứng với tổng cầu ban đầu): `demand_4procs=<d> thrashing=<0|1>`, `demand_after_suspend=<d> thrashing=<0|1>`, `free_frames_after=<d>`.
Chấm tự động: `bash labs/cham.sh OSY L11 duong_dan/bai_cua_ban.py`
