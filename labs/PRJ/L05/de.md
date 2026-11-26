# Dự án PRJ L05 — Giải mã khung nhị phân & lập lịch đa nhân

Đọc cấu hình từ luồng chuẩn (`stdin`) gồm 2 dòng dạng khoá=giá trị:
- Dòng 1: `pid=<số_nguyên> plen=<độ_dài_tải> fill=<1_ký_tự_ASCII> q=<lượng_tử>`
- Dòng 2: `bursts=<b0 b1 ...>` (danh sách thời gian chạy của từng tác vụ)

Yêu cầu chương trình Python:
1. Đóng gói khung theo chuẩn `struct.pack('<HH', pid, plen)` ghép với `plen` byte ký tự `fill` (ASCII), rồi giải mã 4 byte đầu để lấy `(dec_id, dec_len)`.
2. Kiểm tra `header_valid` (`1` nếu `dec_id == pid` và tổng độ dài bộ đệm bằng `4 + dec_len`, ngược lại `0`).
3. Chạy thuật toán lập lịch Round Robin với lượng tử `q` trên danh sách `bursts` (giữ đúng thứ tự hàng đợi ban đầu), tính thời gian chờ trung bình `rr_avg_wait`.

In đúng 3 dòng theo định dạng mẫu (số thực làm tròn 2 chữ số thập phân):
```
frame_total_bytes=<int>
rr_avg_wait=<float:.2f>
header_valid=<0_hoặc_1>
```

Ví dụ minh hoạ khác bộ dữ liệu chấm (`pid=5 plen=10 fill=k q=3`, `bursts=6 4`):
- Tổng byte khung là `4 + 10 = 14`, chờ trung bình Round Robin là `(3 + 6) / 2 = 4.50`, `header_valid=1`.

Chấm tự động:
```bash
bash labs/cham.sh PRJ L05 duong_dan/bai_cua_ban.py
```
