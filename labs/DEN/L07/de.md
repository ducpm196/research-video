# Lab DEN L07 — Chỉ mục ngược và công thức xếp hạng BM25

Cho kho 3 đoạn văn `docs = {1: 'may chu nhanh', 2: 'du lieu lon', 3: 'tim nhanh du lieu'}`. Dựng chỉ mục ngược từ tập đoạn văn này để lấy danh sách mã chứa từ `'nhanh'`, rồi tính điểm xếp hạng chuẩn `BM25` (`k1=1.2, b=0.75`) cho từ `'nhanh'` trong đoạn `1` (dùng công thức trực tiếp trên độ dài kho, không gán cứng).

Định dạng đầu ra (2 dòng):
`docs_with_nhanh=<danh sách ID>`
`bm25_doc1=<4 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh DEN L07 duong_dan/bai_cua_ban.py
```
