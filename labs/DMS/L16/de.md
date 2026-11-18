# Lab DMS L16 — Bậc, bổ đề bắt tay và điều kiện Euler bằng chương trình

Viết `dothi.py` (Python 3.11 trở lên); chạy: `python dothi.py`.

Bốn đồ thị, mỗi đồ thị là một danh sách cạnh (chép nguyên vào đầu tệp):

```python
DO_THI = [
    ('G1', [1, 2, 3, 4], [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]),
    ('G2', [1, 2, 3, 4, 5], [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]),
    ('G3', [1, 2, 3, 4, 5, 6], [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)]),
    ('G4', [1, 2, 3, 4, 5], [(1, 2), (1, 3), (1, 4), (1, 5)]),
]
```

Với mỗi đồ thị in một dòng:
`<tên>: bac=<bậc các đỉnh theo thứ tự đỉnh tăng dần, cách nhau dấu phẩy không có dấu cách> tong=<tổng bậc> canh=<số cạnh> le=<số đỉnh bậc lẻ> lien_thong=<1 nếu liên thông, 0 nếu không> ket_luan=<chu_trinh | duong_di | khong>`

Quy ước `ket_luan` (điều kiện Euler): đồ thị phải liên thông; `chu_trinh` nếu không có đỉnh bậc lẻ; `duong_di` nếu có đúng 2 đỉnh bậc lẻ; còn lại `khong`. Ví dụ định dạng: `G9: bac=2,2,2 tong=6 canh=3 le=0 lien_thong=1 ket_luan=chu_trinh`.

Gợi ý: bậc của đỉnh v = số cạnh có v là một đầu; kiểm liên thông bằng cách đi từ một đỉnh qua các cạnh (duyệt rộng hoặc sâu) rồi xem có tới mọi đỉnh không. Tổng bậc phải bằng hai lần số cạnh.

Cú pháp gợi ý (chưa học ở đâu trước đó): `sum(1 for e in canh if v in e)` nghĩa là: với mỗi cạnh `e` trong danh sách `canh`, nếu `v` là một đầu của `e` thì cộng thêm 1, tức đếm các cạnh chứa `v`. Viết bằng vòng lặp thường cũng được: `bac = 0`, `for e in canh:`, `if v in e:`, `bac = bac + 1`.

Chấm: `bash labs/cham.sh DMS L16 dothi.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
