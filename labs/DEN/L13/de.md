# Lab DEN L13 — So sánh chi phí mạng của nối phát tán và nối xáo trộn

Nối bảng lớn `800 GB` (`GB = ghi-ga-byte`) với bảng nhỏ `2 GB` trên `50` máy. Tính tổng `GB` truyền qua mạng của cách phát tán bảng nhỏ (gửi bản sao tới `49` máy còn lại) so với xáo trộn đều cả hai bảng qua `50` máy (`49/50` phần mỗi bảng phải đi qua mạng).

Định dạng đầu ra (3 dòng):
`broadcast_gb=<số nguyên>`
`shuffle_gb=<2 chữ số>`
`network_saved_pct=<1 chữ số>%`

Chấm tự động:
```bash
bash labs/cham.sh DEN L13 duong_dan/bai_cua_ban.py
```
