# Lab PRJ L03 (Đạt / Chưa đạt theo labs/PRJ/SPEC.md) — Đối soát ba bên (Ngân hàng – NAPAS – Đối tác)

Viết chương trình Python đọc bản ghi giao dịch từ 3 nguồn độc lập qua `stdin` để thực hiện đối soát ba bên và phân loại hàng đợi tra soát (không sửa đè dữ liệu gốc).

## Định dạng đầu vào (`stdin`)
Mỗi dòng không rỗng có đúng 4 trường cách nhau bởi khoảng trắng:
`<nguon> <ma_gd> <so_tien> <trang_thai>`
- `<nguon>`: `BANK`, `NAPAS`, hoặc `PARTNER`.
- `<ma_gd>`: mã tham chiếu duy nhất của giao dịch trong nguồn đó.
- `<so_tien>`: số nguyên dương.
- `<trang_thai>`: `OK`, `FAIL`, hoặc `PENDING`.

## Quy tắc phân loại theo từng `<ma_gd>` (sắp tăng dần theo `<ma_gd>`)
1. **Khớp cả ba (`matched`)**: có mặt ở đủ cả 3 nguồn `BANK`, `NAPAS`, `PARTNER`, cùng `<so_tien>` và cả 3 đều có `<trang_thai> == OK`.
2. **Lệch trạng thái hoặc số tiền (`state_mismatch`)**: có mặt ở đủ cả 3 nguồn nhưng khác `<so_tien>` hoặc có ít nhất một nguồn khác `OK` -> thêm `<ma_gd>:mismatch_state` vào `queue`.
3. **Thiếu một hoặc hai chiều (`one_side`)**: chưa đủ mặt cả 3 nguồn -> gán nhãn vào `queue`:
   - Có ở `BANK` và `NAPAS`, thiếu `PARTNER` -> `<ma_gd>:miss_partner`
   - Chỉ có ở `NAPAS` (thiếu cả `BANK` và `PARTNER`) -> `<ma_gd>:extra_napas`
   - Có ở `NAPAS` và `PARTNER`, thiếu `BANK` -> `<ma_gd>:miss_bank`
   - Có ở `BANK` và `PARTNER`, thiếu `NAPAS` -> `<ma_gd>:miss_napas`
   - Các trường hợp thiếu hai chiều còn lại -> `<ma_gd>:one_side`

## Định dạng đầu ra (`stdout`, đúng 3 dòng)
1. `matched=<m> match_pct=<p>%` (`p` làm tròn 1 chữ số thập phân; nếu tổng mã `= 0` thì `0.0%`).
2. `discrepancies=<d> state_mismatch=<s> one_side=<o>` (`d = s + o`).
3. `queue=<item1>,<item2>,...` (sắp tăng dần theo `<ma_gd>`; nếu `d == 0` thì `queue=none`).

## Chấm tự động (kiểm cả `du_lieu.txt` và `ca_an/`)
```bash
bash labs/cham.sh PRJ L03 duong_dan/bai_cua_ban.py
```
