# Lab PRJ L01 (Đạt / Chưa đạt theo labs/PRJ/SPEC.md) — Lõi chuyển khoản bút toán kép

Viết chương trình Python đọc danh sách tài khoản và các lệnh chuyển khoản từ `stdin`, cài đặt lõi chuyển khoản trên SQLite (`:memory:`) bảo đảm thứ tự khoá tăng dần, kiểm số dư khả dụng trong giao dịch nguyên tử và ghi sổ bút toán kép.

## Định dạng đầu vào (`stdin`)
Mỗi dòng không rỗng là một trong hai lệnh:
- `ACC <id> <so_du_dau>`: khởi tạo tài khoản `<id>` với số dư nguyên `>= 0`.
- `TX <tx_id> <nguon> <dich> <so_tien> <phi>`: thực hiện giao dịch `<tx_id>` chuyển `<so_tien>` từ `<nguon>` sang `<dich>`, kèm phí `<phi>` nộp vào tài khoản `FEE`.

## Quy tắc giao dịch (bắt buộc)
1. Nếu `<nguon>` hoặc `<dich>` chưa tồn tại, `<nguon> == <dich>`, `<so_tien> <= 0`, `<phi> < 0`, hoặc số dư hiện tại của `<nguon>` nhỏ hơn `<so_tien> + <phi>`: từ chối giao dịch (kết quả `False`), không thay đổi số dư và không ghi dòng nào vào bảng bút toán.
2. Nếu hợp lệ: sắp thứ tự hai tài khoản `sorted([nguon, dich])` khi khoá (và kiểm trong giao dịch nguyên tử `with db:` của SQLite), trừ `<so_tien> + <phi>` ở `<nguon>`, cộng `<so_tien>` ở `<dich>`, cộng `<phi>` ở `FEE` (nếu `<phi> > 0` thì tài khoản `FEE` bắt buộc phải tồn tại, thiếu thì từ chối giao dịch), và ghi đủ 2 dòng (hoặc 3 dòng khi `<phi> > 0`) vào bảng bút toán để tổng đại số mọi bút toán luôn bằng `0`.

## Định dạng đầu ra (`stdout`, đúng 4 dòng)
1. `tx_results=<r1>,<r2>,...` (`True` hoặc `False` theo thứ tự từng lệnh `TX`, nếu không có `TX` thì `tx_results=none`).
2. `ledger_sum=<tong>` (phải bằng `0`).
3. `total_money=<tong_tien_toan_he_thong>`
4. `balances=<id1>:<bal1>,<id2>:<bal2>,...` (sắp tăng dần theo `<id>`).

## Chấm tự động (kiểm cả `du_lieu.txt` và `ca_an/`)
```bash
bash labs/cham.sh PRJ L01 duong_dan/bai_cua_ban.py
```
