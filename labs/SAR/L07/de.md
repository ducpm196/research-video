# Lab SAR L07 — Bộ giới hạn tốc độ thùng token (Token Bucket)

Đọc `stdin` `cap=<int> rate=<int> burst=<int> total=<int> secs=<int>`. Bắt đầu với thùng đầy `cap` token: tại giây `t=0` phục vụ tối đa `cap` yêu cầu (không vượt `total`); ở mỗi giây `t=1..secs-1` nạp thêm `rate` token vào thùng (tối đa không vượt sức chứa `cap`, tức `min(cap, tok + rate)`) rồi phục vụ tối đa `burst` yêu cầu mỗi giây (giới hạn lưu lượng mỗi giây sau khi nạp, không vượt số token hiện có và phần còn lại của `total`). Đếm số yêu cầu nhận và từ chối trên tổng `total`.

In 3 dòng: `accepted=<d>`, `rejected=<d>`, `accept_pct=<.2f>%`.
Chấm tự động: `bash labs/cham.sh SAR L07 duong_dan/bai_cua_ban.py`
