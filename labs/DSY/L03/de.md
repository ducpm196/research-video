# Lab DSY L03 [Mô phỏng phân tán] — Kiểm tra mọi cặp tập đại biểu (R, W) trên N = 3

Viết chương trình Python kiểm vét cạn mọi tập con `R` và `W` kích thước `(2, 2)` trên `3` nút `{0, 1, 2}`: tất cả 9 cặp đều giao nhau (`R+W=4 > 3`), trong khi `(1, 2)` có 3 cặp không giao (`R+W=3 <= 3`), in đúng 3 dòng:
1. `quorum_2_2_all_intersect=1`
2. `pair_1_2_disjoint_cases=3`
3. `n5_min_r_when_w3=3`

Chấm tự động:
```bash
bash labs/cham.sh DSY L03 duong_dan/bai_cua_ban.py
```
