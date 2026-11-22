# Lab SAR L01 — Ma trận đánh đổi cho bản ghi quyết định kiến trúc (ADR)

Chấm điểm hai phương án cơ sở dữ liệu theo bộ tiêu chí `(toàn vẹn ACID, nối bảng JOIN, mở rộng ghi)` với trọng số `(0.5, 0.2, 0.3)` cho dịch vụ ghi nhật ký phân tích tải cao: `RDBMS` đạt `(5, 5, 1)` và kho khoá-giá trị chia mảnh (`ShardedKV`) đạt `(3, 2, 5)`. Tính điểm từng phương án và chọn phương án ưu tiên.

Định dạng đầu ra (3 dòng):
`rdbms_score=<2 chữ số>`
`sharded_kv_score=<2 chữ số>`
`chosen=<RDBMS|ShardedKV>`

Chấm tự động:
```bash
bash labs/cham.sh SAR L01 duong_dan/bai_cua_ban.py
```
