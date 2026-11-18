# Lab DMS L17 — Cây: kiểm tra, đếm lá và công thức Cayley bằng chương trình

Viết `cay.py` (Python 3.11 trở lên); chạy: `python cay.py`.

Bốn đồ thị trên 6 đỉnh 1..6 (chép nguyên vào đầu tệp):

```python
DO_THI = [
    ('H1', [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]),
    ('H2', [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6)]),
    ('H3', [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]),
    ('H4', [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)]),
]
```

Với mỗi đồ thị in một dòng `<tên>: n=6 m=<số cạnh> lien_thong=<0|1> chu_trinh=<0|1> la_cay=<0|1>`.
- `lien_thong`: có đường đi giữa hai đỉnh bất kỳ không.
- `chu_trinh`: có chu trình không (gợi ý: thêm lần lượt từng cạnh vào nhóm đỉnh; nếu một cạnh nối hai đỉnh ĐÃ cùng nhóm thì có chu trình).
- `la_cay`: bằng 1 khi liên thông và không có chu trình.

Sau bốn dòng, in tiếp ba dòng:
5. `H1: so la = <số>` — lá là đỉnh bậc 1
6. `H3: so la = <số>`
7. `cay co nhan 8 dinh (cong thuc Cayley): <số>` — `8 ** 6`

Để ý H2: có 5 cạnh = n − 1 nhưng KHÔNG phải cây.

Gợi ý khung (vòng lặp thường, không cần cú pháp nâng cao): cho mỗi đỉnh một nhãn nhóm `nhom = {v: v for v in range(1, 7)}` (từ điển: đỉnh → nhãn, lúc đầu mỗi đỉnh một nhóm); với mỗi cạnh `(u, v)`: nếu `nhom[u] == nhom[v]` thì có chu trình; nếu khác thì đổi mọi đỉnh mang nhãn `nhom[v]` sang nhãn `nhom[u]`. Cuối cùng còn một nhãn duy nhất nghĩa là liên thông.

Chấm: `bash labs/cham.sh DMS L17 cay.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
