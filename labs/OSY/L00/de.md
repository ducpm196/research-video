# Lab OSY L00 — Chế độ nhân, lời gọi hệ thống và chi phí chuyển ngữ cảnh

Đọc từ đầu vào chuẩn (`stdin`) `r1=<d> r2=<d> ctx_us=<d> is_sys=<0|1>` (`r1`, `r2` là số lần chuyển ngữ cảnh mỗi giây, `ctx_us` là chi phí mỗi lần tính bằng micro-giây). Tính phần trăm CPU tiêu tốn ở hai tần suất `r1`, `r2` và in cờ chuyển chế độ (`1` nếu `is_sys != 0`, ngược lại `0`).

In đúng 3 dòng (`<.2f>` là số thực 2 chữ số thập phân; giữ nguyên tên khoá cố định): `cpu_pct_1k=<.2f>`, `cpu_pct_50k=<.2f>`, `syscall_mode_switch=<0|1>`.
Chấm tự động: `bash labs/cham.sh OSY L00 duong_dan/bai_cua_ban.c`
