# Lab DSY L07 [Mô phỏng phân tán] — Mô phỏng hoàn chỉnh Map -> Shuffle -> Reduce

Viết 3 bước thuần Python xử lý đoạn văn `'a b a c b a'`: `map` phát `(w, 1)`, `shuffle` gom danh sách theo khoá, `reduce` cộng tổng, in đúng 3 dòng:
1. `mapped_pairs=6`
2. `unique_keys=3`
3. `reduced=a:3,b:2,c:1`

Chấm tự động:
```bash
bash labs/cham.sh DSY L07 duong_dan/bai_cua_ban.py
```
