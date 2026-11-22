# Lab TOC L12 — Kiểm tra hai điều kiện Định lý Rice trên một họ hàm cụ thể

Xét tính chất ngữ nghĩa `T`: 'hàm luôn trả về số chẵn với mọi đầu vào x thuộc {0, 1, 2}'. Dùng ba hàm thử `f1(x)=2`, `f2(x)=1+1`, `f3(x)=x+1` để kiểm tra bằng máy: (1) có hàm thỏa `T`; (2) có hàm không thỏa `T`; (3) hai hàm viết khác cú pháp (`f1` vs `f2`) cho cùng đầu ra trên `{0, 1, 2}`.

Định dạng đầu ra (1 dòng):
`has_yes=<0 hoặc 1> has_no=<0 hoặc 1> syn_diff_same_sem=<0 hoặc 1> rice_applies=<0 hoặc 1>`

Chấm tự động:
```bash
bash labs/cham.sh TOC L12 duong_dan/bai_cua_ban.py
```
