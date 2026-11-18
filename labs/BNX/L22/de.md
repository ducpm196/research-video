# Lab BNX L22 — Từ đường dẫn tới tệp dựng (mô phỏng, không cần máy chủ AEM)

Máy bạn không có máy chủ AEM, nên ta mô phỏng bằng Python (số liệu và tên là số minh hoạ, khác ví dụ trong bài). Kho nội dung và danh sách tệp dựng cho sẵn:

```python
KHO = {"content": {"bank": {"en": {
    "the": {"sling:resourceType": "bank/components/card"},
    "vay": {"sling:resourceType": "bank/components/loan"}}}}}
TEP = ["/apps/bank/components/card/card.html",
       "/apps/bank/components/card/print.html",
       "/libs/bank/components/loan/loan.html"]
```

Viết `mau.py` (chép hai khai báo trên vào đầu tệp, rồi viết tiếp). Với mỗi địa chỉ trong danh sách bên dưới:

1. Tách địa chỉ tại dấu chấm đầu tiên: phần trước là đường dẫn tài nguyên (tên nút không có dấu chấm); phần sau chia theo dấu chấm, khúc cuối là phần mở rộng, khúc trước (nếu có) là **bộ chọn** (chỉ có tối đa một).
2. Đi từ gốc `KHO` xuống theo từng tên của đường dẫn để tìm nút. Không có nút thì kết quả là `KHONG CO TAI NGUYEN`.
3. Đọc `sling:resourceType` của nút. Tên ứng viên: bộ chọn (nếu có) rồi tới khúc cuối của kiểu tài nguyên. Với mỗi tên, thử `/apps/<kiểu>/<tên>.html` rồi `/libs/<kiểu>/<tên>.html`; tệp đầu tiên nằm trong `TEP` thì chọn. Không có tệp nào thì kết quả là `KHONG CO TEP DUNG`.

Địa chỉ: `/content/bank/en/the.html`, `/content/bank/en/the.print.html`, `/content/bank/en/vay.html`, `/content/bank/en/vay.print.html`, `/content/bank/en/thieu.html`.

In mỗi địa chỉ một dòng dạng `<tên cuối của địa chỉ> -> <kết quả>`, ví dụ `the.html -> /apps/...`.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L22 mau.py`.
