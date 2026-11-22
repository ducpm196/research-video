# Lab CLC L08 — Tính cước truyền dữ liệu ra ngoài (Egress) 30 TB/tháng

Tính lượng GB tương ứng của `30 TB` (`1 TB = 1 024 GB`), chi phí hàng tháng ở mức `0,08 USD/GB`, và khoản tiết kiệm nếu mạng phân phối nội dung tại biên (`CDN`) hấp thụ `75%` lưu lượng khỏi máy chủ nguồn.

Định dạng đầu ra (3 dòng):
`egress_gb=<số>`
`monthly_usd=<2 chữ số>`
`cdn_saved_usd=<2 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CLC L08 duong_dan/bai_cua_ban.py
```
