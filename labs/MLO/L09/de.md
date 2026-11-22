# Lab MLO L09 — Vòng phản hồi tự củng cố: hai mục dẫn đầu chiếm dần lượt chọn

Cho 5 mục ban đầu `[2, 2, 2, 2, 2]`. Mô phỏng 8 vòng luôn chỉ hiển thị 2 mục dẫn đầu (`top-2`, nếu hoà điểm ưu tiên mục có chỉ số nhỏ hơn) và mỗi vòng hai mục này được cộng thêm `+3` lượt bấm. Tính tỉ lệ (%) lượt bấm dồn vào 2 mục đầu.

Định dạng đầu ra:
`clicks=<danh sách 5 số> top2_share=<1 chữ số>%`

Chấm tự động:
```bash
bash labs/cham.sh MLO L09 duong_dan/bai_cua_ban.py
```
