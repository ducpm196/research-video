# Lab BEP L04 — Kiểm định tương thích Schema Registry (Protobuf/Avro)

Đọc từ `stdin` 2 dòng mô tả hai phiên bản lược đồ (`tag:type:req` cách nhau bởi dấu phẩy, `req` là `1` hoặc `0`):
- Dòng 1: `v1=<tag:type:req,...>`
- Dòng 2: `v2=<tag:type:req,...>`

Yêu cầu:
1. Kiểm tra `backward_ok` (`1` nếu mọi thẻ xuất hiện trong `v1` vẫn giữ nguyên `type` nếu còn ở `v2`, và mọi thẻ mới chỉ có ở `v2` đều có `req=0`; ngược lại `0`).
2. Kiểm tra `forward_ok` (`1` nếu mọi thẻ có ở `v1` đều giữ nguyên `type` nếu còn trong `v2`, và không xoá bất kỳ thẻ nào có `req=1` ở `v1`; ngược lại `0`).
3. Phân loại `status`: `FULL` nếu cả hai đều `1`, `BACKWARD_ONLY` nếu chỉ `backward_ok==1`, `FORWARD_ONLY` nếu chỉ `forward_ok==1`, hoặc `BREAKING` nếu cả hai đều `0`.

In đúng 3 dòng: `backward_ok=<0|1>`, `forward_ok=<0|1>`, `compat_status=<STR>`.

Chấm tự động: `bash labs/cham.sh BEP L04 duong_dan/bai_cua_ban.py`
