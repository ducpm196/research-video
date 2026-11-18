# Lab BNX L12 — Chạy lại nhật ký ví, kiểm bất biến và hạn mức tháng

Số liệu là số minh hoạ. Viết chương trình Python `mau.py` (chỉ dùng Python có sẵn). Dữ liệu cho sẵn, chép vào đầu tệp:

```python
bao_dam = 250_000                    # tài khoản đảm bảo đầu ngày
vi = {"X": 0, "Y": 250_000, "Z": 0}  # số dư ba ví đầu ngày
nhat_ky = [("nap", "X", 3_000_000), ("chuyen", "X", "Z", 1_200_000),
           ("rut", "Z", 400_000), ("nap", "Y", 500_000),
           ("rut", "Y", 2_000_000), ("chuyen", "Z", "Y", 300_000)]
```

**Phần 1 — chạy lại nhật ký.** Duyệt từng dòng theo thứ tự:
- `nap`: ví tăng và tài khoản đảm bảo tăng cùng số tiền;
- `rut`: ví giảm và tài khoản đảm bảo giảm cùng số tiền; nhưng nếu số dư ví **nhỏ hơn** số tiền rút thì **từ chối**: in `tu choi rut <ví> <số tiền>` và không đổi gì;
- `chuyen`: ví đi giảm, ví đến tăng, tài khoản đảm bảo không đổi.

Sau khi duyệt hết, in hai dòng: `vi <số dư X> <số dư Y> <số dư Z>` (ba số cách nhau một dấu cách, ví dụ dùng `print("vi", *vi.values())`) và `tong vi <tổng> dam bao <số> dat <True/False>` (đạt khi tài khoản đảm bảo ≥ tổng ví).

**Phần 2 — hạn mức tháng 50 000 000.** Cộng dồn lần lượt các giao dịch `20_000_000, 25_000_000, 10_000_000, 5_000_000`. Giao dịch nào làm tổng **vượt** hạn mức thì từ chối, giao dịch làm tổng **vừa bằng** hạn mức vẫn được nhận. Mỗi giao dịch in một dòng: `chap nhan <tiền> da dung <tổng đã dùng>` hoặc `tu choi <tiền> da dung <tổng đã dùng>`.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L12 mau.py`. Đầu ra viết không dấu để chạy được trên mọi cửa sổ lệnh.
