# Lab DBS L10 — SQLite: tối ưu JOIN giữa hai bảng bằng chỉ mục khoá nối

Cơ sở dữ liệu có sẵn bảng `R(id, k)` và `S(k, v)`. Tạo chỉ mục `idx_sk ON S(k)` rồi nối `R` với `S` theo `k` để đếm số dòng nối, xác minh chỉ mục qua `FROM sqlite_master WHERE name='idx_sk'` và tính tổng `S.v`.

In đúng 3 dòng: `joined_rows=<d>`, `idx_sk_ok=<d>`, `sum_v=<d>`.
Chấm tự động: `bash labs/cham.sh DBS L10 duong_dan/bai_cua_ban.sql`
