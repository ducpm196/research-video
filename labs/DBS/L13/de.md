# Lab DBS L13 — SQLite: phát hiện bế tắc trên đồ thị chờ (Wait-For Graph)

Cơ sở dữ liệu có sẵn `Held(r, tx)` và `Wait(tx, r)`. Tạo khung nhìn đồ thị chờ (`CREATE VIEW WFG AS SELECT DISTINCT w.tx AS u, h.tx AS v FROM Wait w JOIN Held h ON w.r=h.r WHERE w.tx<>h.tx;`) rồi dùng CTE đệ quy (`WITH RECURSIVE r(s,t,d) AS (SELECT u,v,1 FROM WFG UNION ALL SELECT r.s, e.v, r.d+1 FROM r JOIN WFG e ON r.t=e.u WHERE r.d < 8)`) kiểm tra chu trình bế tắc (`EXISTS`).

In đúng 3 dòng: `wait_edges=<d>`, `deadlock_detected=<0|1>`, `victim_needed=<0|1>`.
Chấm tự động: `bash labs/cham.sh DBS L13 duong_dan/bai_cua_ban.sql`
