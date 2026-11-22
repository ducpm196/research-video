# Lab CLC L09 — Tính chi phí xoay khoá chính theo mã hoá phong bì (KMS)

Kho dữ liệu có `2 TB` (`2 * 10^12 byte`) được bảo vệ bởi `25 000` khoá dữ liệu (`DEK`), mỗi khoá dài `32 byte`. Tính tổng số byte và KB cần bọc lại khi xoay khoá chính tại dịch vụ quản lý khoá (`KMS`), và xác nhận nhỏ hơn nhiều so với dữ liệu gốc.

Định dạng đầu ra (3 dòng):
`dek_bytes=<số>`
`dek_kb=<1 chữ số>`
`smaller_than_raw=<0|1>`

Chấm tự động:
```bash
bash labs/cham.sh CLC L09 duong_dan/bai_cua_ban.py
```
