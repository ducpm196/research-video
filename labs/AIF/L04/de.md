# Lab AIF L04 — Leo đồi dốc nhất trên bàn cờ 4-Hậu (mỗi cột một hậu)

Theo quy ước bài học (`b[c]` là hàng của quân hậu ở cột `c`), cho bàn cờ xuất phát `b0 = [2, 2, 1, 3]` (đếm cặp ăn nhau cùng hàng hoặc cùng đường chéo). Chạy thuật toán leo đồi dốc nhất: ở mỗi vòng, duyệt hết cả `4 × 4` láng giềng dời 1 hậu trong cùng cột để chọn láng giềng có ít xung đột nhất, dừng khi không còn láng giềng nào tốt hơn trạng thái hiện tại.

Định dạng đầu ra:
`init_conflicts=<số> final_conflicts=<số> final_board=<danh sách>`

Chấm tự động:
```bash
bash labs/cham.sh AIF L04 duong_dan/bai_cua_ban.py
```
