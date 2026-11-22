# Lab EVT L05 — Mô hình tách ghi–đọc (CQRS) và độ trễ chiếu

Mô hình ghi nhận `600` sự kiện mỗi giây còn bộ chiếu xử lý `450` sự kiện mỗi giây trong `10` phút (`600` giây). Tính tổng sự kiện tồn chưa chiếu, độ trễ theo giây dữ liệu (lượng tồn chia cho nhịp ghi mỗi giây), và thời gian xả hết tồn nếu mở song song `2` bộ chiếu (`900/s`) trong lúc vẫn ghi `600/s`.

Định dạng đầu ra (3 dòng):
`backlog=<số nguyên>`
`data_lag_s=<1 chữ số>`
`drain_with_2_s=<1 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh EVT L05 duong_dan/bai_cua_ban.py
```
