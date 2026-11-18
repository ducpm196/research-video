# Lab ACB L07 — HMAC, nhận webhook theo mã sự kiện và đối soát ba nguồn

Số liệu (số minh hoạ, khác ví dụ trong bài):
- Gói webhook `goi = '{"va": "770000009999", "tien": 2500000}'`; khoá bí mật `b"khoa-lab-07"`; mã xác thực = 12 ký tự hệ mười sáu đầu của HMAC-SHA256 (`hmac.new(khoa, noi_dung.encode(), hashlib.sha256).hexdigest()[:12]`). Kiểm hai lần: gói nguyên vẹn, và gói đã đổi `2500000` thành `9500000`.
- Mã sự kiện đến theo thứ tự: `e1, e2, e1, e3, e2`. Lần đầu thấy mã thì `gach no`, lần sau thì `bo qua`.
- Ba nguồn mã giao dịch (đã sắp xếp): Core `[10, 11, 13, 15]`, NAPAS `[10, 11, 12, 13, 15, 16]`, ERP `[10, 13, 16]`. Phân loại mỗi mã theo bảng: có cả ba → `MATCHED`; có ở Core và NAPAS, thiếu ERP → `rot webhook, goi gach no bo sung`; chỉ có ở NAPAS → `treo ghi co, hach toan bu`; có ở Core, không có ở NAPAS → `loi chuyen tien NAPAS, tra soat`; trường hợp khác → `bat thuong`.

Viết `mau.py` (Python 3) in đúng các dòng:

1. `hmac nguyen ven: <True|False>` và `hmac bi sua: <True|False>` — True nghĩa là mã tính lại bằng mã đã đính kèm.
2. Năm dòng `<mã sự kiện>: <gach no|bo qua>`.
3. Sáu dòng `<mã giao dịch>: <phân loại>` theo mã tăng dần.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh ACB L07 mau.py`.
