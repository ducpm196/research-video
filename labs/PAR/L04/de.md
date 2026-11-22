# Lab PAR L04 — So sánh lập lịch chia đôi tĩnh và việc dài trước (LPT) trên 2 lõi

Trên danh sách 8 việc `jobs = [4, 9, 2, 8, 1, 7, 3, 6]` chia cho 2 lõi: tính thời gian hoàn thành tối đa (makespan) của chia khối nửa đầu–nửa sau và của thuật toán LPT (sắp giảm dần `sorted(jobs, reverse=True)` rồi gán cho lõi đang rảnh nhất).

Định dạng đầu ra (1 dòng):
`static_makespan=<số nguyên> lpt_makespan=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh PAR L04 duong_dan/bai_cua_ban.py
```
