# Lab BEP L00 — GraphQL Supergraph DataLoader chống N+1

Đọc từ luồng chuẩn (`stdin`) 2 dòng:
- Dòng 1: `items=<o1:u1,o2:u2,...>` (danh sách cặp `mã_đơn:mã_người_dùng`)
- Dòng 2: `batch_limit=<int>` (kích thước tối đa mỗi lô khoá trong Subgraph tài khoản)

Yêu cầu:
1. Tính tổng truy vấn theo cách N+1 thô: `naive_queries = 1 + len(items)`.
2. Thu thập danh sách mã người dùng duy nhất `unique_keys` (giữ thứ tự xuất hiện hoặc sắp xếp), tính số lượt gọi Subgraph tài khoản theo lô tối đa `batch_limit` phần tử: `ceil(len(unique_keys) / batch_limit)`.
3. In đúng 3 dòng: `naive_queries=<int>`, `unique_keys=<int>`, `dataloader_queries=<int>` (`1 + số_lô_tài_khoản`).

Chấm tự động: `bash labs/cham.sh BEP L00 duong_dan/bai_cua_ban.py`
