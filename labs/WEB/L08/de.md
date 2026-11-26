# Lab WEB L08 — Node.js: kiểm độ tươi Cache-Control & phản hồi ETag 304

Đọc `stdin` `max_age=<n> age=<n> cli_etag=<str> srv_etag=<str>`. Đánh giá bản lưu quá hạn khi `age >= max_age`; nếu đã quá hạn thì trả mã `304` khi `cli_etag` trùng `srv_etag` (ngược lại `200`), còn nếu vẫn tươi (`is_stale=0`) thì không gọi mạng (`status_code=0`, `body_resent=0`).

In đúng 3 dòng: `is_stale=<0|1>`, `status_code=<0|200|304>`, `body_resent=<0|1>`.
Chấm tự động: `bash labs/cham.sh WEB L08 duong_dan/bai_cua_ban.js`
