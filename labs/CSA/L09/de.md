# Lab CSA L09 (Mô phỏng Pipeline k tầng) — Chu kỳ lý tưởng và độ trễ xung đột

Viết chương trình Python tính số chu kỳ hoàn thành `N = 100` lệnh trên đường ống `k = 5` tầng (`k + N - 1`), so với thực thi không đường ống (`k * N`) và khi gặp 12 lần dừng 1 chu kỳ (stall), in đúng 3 dòng:
1. `cycles_no_pipe=500`
2. `cycles_pipe_ideal=104 speedup=4.81`
3. `cycles_with_12_stalls=116`

Chấm tự động:
```bash
bash labs/cham.sh CSA L09 duong_dan/bai_cua_ban.py
```
