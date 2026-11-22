# Lab DSY L05 [Mô phỏng phân tán] — Tính ngưỡng đa số và khả năng chịu hỏng cụm Raft

Viết chương trình Python tính kích thước đa số `N // 2 + 1` và số nút hỏng tối đa chịu được `N - (N // 2 + 1)` cho `N = 3, 4, 5, 7`, in đúng 3 dòng:
1. `quorum_4=3 max_fail_4=1`
2. `quorum_5=3 max_fail_5=2`
3. `odd_beats_even=1`

Chấm tự động:
```bash
bash labs/cham.sh DSY L05 duong_dan/bai_cua_ban.py
```
