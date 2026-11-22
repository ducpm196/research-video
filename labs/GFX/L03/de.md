# Lab GFX L03 — Ánh xạ toạ độ thiết bị chuẩn hoá NDC [-1, 1] sang pixel màn hình

Cho màn hình rộng `W = 1280 px`, ánh xạ ba giá trị `x_ndc` trong `[-1.0, 0.25, 1.0]` sang chỉ số điểm ảnh `round((x + 1)/2 * W)`.
In đúng 1 dòng `ndc_to_px=[...]`.

Chấm tự động:
```bash
bash labs/cham.sh GFX L03 duong_dan/bai_cua_ban.py
```
