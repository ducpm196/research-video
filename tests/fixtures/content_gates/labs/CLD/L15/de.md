# Lab CLD L15 — Máy cần thêm khi tách luồng phục vụ quy mô lớn

Cho cụm `10 000` máy cần thêm phần dự phòng ở điểm giữa `25%` để tách luồng tương tác và xử lý lô, và giả lập mất `10` phút gián đoạn trong cửa sổ cập nhật lớn `14 400` phút. Tính số máy thêm và tỉ lệ phần trăm thời gian mất kết nối.

Định dạng đầu ra (2 dòng):
`extra_machines=<số nguyên>`
`downtime_pct=<2 chữ số>%`

Chấm tự động:
```bash
bash labs/cham.sh CLD L15 duong_dan/bai_cua_ban.py
```
