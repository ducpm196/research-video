# Lab BNK L11 — Bản tin phản hồi 0210

Một bản tin phản hồi `0210` có bốn trường: `3` = `"000000"`, `4` = `"000000250000"`, `11` = `"000042"`, `39` = `"00"` (mã phản hồi). Mọi trường có độ dài cố định.

Viết chương trình `iso_lab.py` (Python), gồm hai việc:
1. Dựng **bản đồ bit** 64 bit bằng cách bật bit `1 << (64 - số trường)` cho từng trường rồi in dạng `"%016X"`.
2. In **độ dài** của cả bản tin: mã loại `0210` (4 ký tự) + bản đồ (16 ký tự) + các trường nối theo thứ tự tăng dần.

Chạy: `python iso_lab.py`. Chấm: `bash labs/cham.sh BNK L11 iso_lab.py`.
