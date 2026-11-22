# Lab CSA L11 (Mô phỏng Cache ánh xạ trực tiếp) — Tách thẻ (Tag), chỉ số (Index), độ dời (Offset) và đếm trúng/trượt

Viết chương trình Python mô phỏng cache ánh xạ trực tiếp có `8` dòng (`index` = chỉ số `3 bit`), kích thước khối `16 byte` (`offset` = độ dời `4 bit`, phần còn lại là `tag` = thẻ). Cho chuỗi địa chỉ `[0x00, 0x04, 0x80, 0x08]`, đếm tổng số trượt do xung đột ghi đè lên ngăn đã có dữ liệu (`conflict_at_0x80` = tổng xung đột tại chỉ số 0 khi `0x80` và `0x08` lần lượt đẩy nhau), in đúng 3 dòng:
1. `split_0x84=tag:1,idx:0,off:4`
2. `hits=1 misses=3`
3. `conflict_at_0x80=2`

Chấm tự động:
```bash
bash labs/cham.sh CSA L11 duong_dan/bai_cua_ban.py
```
