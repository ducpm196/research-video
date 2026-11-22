# Lab DVO L00 (Mô phỏng vòng phản hồi) — Tìm kiếm nhị phân bằng lệnh git bisect

Viết chương trình Python tính số bước tối đa (`ceil(log2(N))`) của `git bisect` (lệnh Git chia đôi lịch sử tìm lần lưu thay đổi gây lỗi) khi quy mô lô thay đổi là `3`, `300`, và kiểm tra kết quả tìm đúng vị trí commit hỏng đầu tiên `bad = 187` trong `0..299`, in đúng 3 dòng:
1. `bisect_steps_3=2`
2. `bisect_steps_300=9`
3. `found_bad_commit=187`

Chấm tự động:
```bash
bash labs/cham.sh DVO L00 duong_dan/bai_cua_ban.py
```
