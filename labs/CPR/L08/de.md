# Lab CPR L08 — Đóng gói trường bit và kiểm tệp nhị phân 16 byte qua stdin

Viết chương trình C chuẩn C11 đọc `type` (4 bit), `len` (12 bit) và `count` (`1 <= count <= 128`), tiếp theo đọc `count` số tiền `amt` từ `stdin`.
Đóng gói `pk = ((type & 0xF) << 12) | (len & 0xFFF)`, ghi `count` bản ghi `Rec { uint64_t ts; uint16_t hdr, flag; uint32_t amt; }` xuống tệp `out.bin`, đọc lại bằng `fread`, tính `sum_amt` và in đúng 2 dòng:
1. `packed=<pk> type=<tách lại type> len=<tách lại len>`
2. `bytes=<nr * 16> count=<nr> sum_amt=<tổng amt đọc lại>`

Chấm tự động:
```bash
bash labs/cham.sh CPR L08 duong_dan/bai_cua_ban.c
```
