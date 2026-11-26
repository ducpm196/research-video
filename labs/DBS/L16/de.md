# Lab DBS L16 — SQLite: truy vấn đồ thị bạn-của-bạn vs cột JSON bán cấu trúc

Cơ sở dữ liệu có sẵn `Ban(u, v)` và bảng `Meta(doc TEXT)` chứa chuỗi JSON. Tìm bạn bậc 2 từ `'S1'`, trích trường bằng `json_extract(doc, '$.role')` từ `Meta` và xuất nhãn kết hợp.

In đúng 3 dòng: `friend_of_friend=<str>`, `json_role=<str>`, `nosql_fit=graph_doc`.
Chấm tự động: `bash labs/cham.sh DBS L16 duong_dan/bai_cua_ban.sql`
