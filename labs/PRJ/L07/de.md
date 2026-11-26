# Dự án PRJ L07 — Đường ống Outbox, Consistent Hashing & Circuit Breaker

Đọc từ luồng chuẩn (`stdin`) 4 dòng dạng `khoá=giá trị`:
- Dòng 1: `commit_ids=<id1,id2,...>`
- Dòng 2: `rollback_ids=<id3,...>`
- Dòng 3: `old_nodes=<int> new_nodes=<int> keys=<int>`
- Dòng 4: `events=<danh_sách_0_hoặc_1_cách_nhau_dấu_phẩy> threshold=<int>` (`1` = gọi thành công reset lỗi về `0`, `0` = gọi lỗi tăng bộ đếm)

Yêu cầu chương trình Python:
1. Tạo 2 bảng SQLite `ord(id INT)` và `outb(id INT)`; ghi các `commit_ids` vào cả 2 bảng trong giao dịch `with con:`, sau đó mở `BEGIN`, chèn `rollback_ids` rồi gọi `con.rollback()`. Kiểm tra `COUNT(ord) == COUNT(outb)`.
2. Dùng hàm băm `int(hashlib.sha256(s.encode()).hexdigest()[:8], 16)` đặt các nút ảo `'n0#0'..'n{n-1}#0'` lên vòng tròn băm và định tuyến khoá `'k0'..'k{keys-1}'` bằng `bisect.bisect`. Kiểm tra tỉ lệ khoá bị dời chỗ khi tăng từ `old_nodes` lên `new_nodes` có nhỏ hơn `30%` tổng số `keys` hay không.
3. Mô phỏng Circuit Breaker bắt đầu ở `CLOSED` (`fails = 0`), duyệt qua chuỗi `events`: gặp `1` thì đặt `fails = 0`, gặp `0` thì tăng `fails` lên 1 và mở `OPEN` khi `fails >= threshold`.

In đúng 3 dòng theo định dạng:
```
outbox_atomic_match=<0_hoặc_1>
ch_moved_lt_150=<0_hoặc_1>
cb_after_3fails=<CLOSED_hoặc_OPEN>
```

Chấm tự động:
```bash
bash labs/cham.sh PRJ L07 duong_dan/bai_cua_ban.py
```
