# Lab CS115 L26 — LDA tiêu chí Fisher: tỉ số độ lệch giữa lớp / tổng bình phương trong lớp

Cho hai lớp `c1 = [1, 2, 3]` và `c2 = [5, 6, 7]`. Tính tiêu chí Fisher `J = (m1 - m2)^2 / (s1^2 + s2^2)` trong đó `s_k^2 = sum((x - m_k)^2)` (tổng bình phương độ lệch chưa chia `n`), cùng số chiều tối đa `C - 1` cho bài toán 3 lớp.

Định dạng đầu ra (2 dòng):
`m1=<1 chữ số> m2=<1 chữ số> J=<2 chữ số>`
`max_dims_3class=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L26 duong_dan/bai_cua_ban.py
```
