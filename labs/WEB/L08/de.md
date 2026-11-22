# Lab WEB L08 — Node.js thật: kiểm độ tươi Cache-Control & phản hồi ETag 304

Viết hàm Node.js đánh giá yêu cầu cache: `max-age=600`, tuổi bản lưu `700 s`, gửi `If-None-Match='"v42"'` so với ETag máy chủ `'"v42"'`, trả mã HTTP `304`, in đúng 3 dòng:
1. `is_stale=1`
2. `status_code=304`
3. `body_resent=0`

Chấm tự động:
```bash
bash labs/cham.sh WEB L08 duong_dan/bai_cua_ban.js
```
