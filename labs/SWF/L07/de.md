# Lab SWF L07 — Kiểm chứng bất biến của cây tìm kiếm nhị phân (BST) và Min-Heap (đống nhỏ nhất)

Viết chương trình Python kiểm duyệt giữa (inorder) một cây tìm kiếm nhị phân (BST) trả về `[2, 5, 7, 9, 12]` (tăng chặt) và kiểm bất biến min-heap `h[i] <= h[2i+1], h[2i+2]` trên mảng `[1, 4, 3, 7, 8]` vs mảng lỗi `[1, 5, 3, 2, 8]`, in đúng 3 dòng:
1. `bst_inorder_sorted=1`
2. `valid_heap=1`
3. `broken_heap=0`

Chấm tự động:
```bash
bash labs/cham.sh SWF L07 duong_dan/bai_cua_ban.py
```
