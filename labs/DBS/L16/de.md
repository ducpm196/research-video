# Lab DBS L16 — SQLite thật: truy vấn đồ thị bạn-của-bạn vs cột JSON bán cấu trúc

Viết tập lệnh SQLite dựng bảng cạnh `Ban(u TEXT, v TEXT)` tìm bạn bậc 2 (`S1 -> S2 -> S3`) bằng SELF-JOIN và trích trường JSON `json_extract('{"role":"ai","tier":2}', '$.role')`, in đúng 3 dòng:
1. `friend_of_friend=S3`
2. `json_role=ai`
3. `nosql_fit=graph_doc`

Chấm tự động:
```bash
bash labs/cham.sh DBS L16 duong_dan/bai_cua_ban.sql
```
