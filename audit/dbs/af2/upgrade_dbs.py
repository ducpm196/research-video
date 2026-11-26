"""Nâng trọn bộ 18 bài DBS (L00–L17) lên chuẩn AF2 theo bảng quyết định BN-08.

Toàn bộ 18 bài chạy SQL THẬT trên SQLite CLI 3.46.0 (`*.sql` qua `labs/cham.sh`),
từ ràng buộc khoá ngoại, JOIN, NULL 3-trị, chuẩn hoá BCNF nối bảng không mất dữ liệu,
EXPLAIN QUERY PLAN dùng B-Tree index, tới giao dịch ACID BEGIN/ROLLBACK/SAVEPOINT.
"""
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[2])); import _frozen  # noqa: E402,F401
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402
import af2_upgrader as up  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

LESSONS = [
    (
        "L00", "sql", "Khoá chính (PK) chặn trùng ID; PRAGMA foreign_keys=ON (bật kiểm khoá ngoại FK) chặn bản ghi mồ côi",
        "# Lab DBS L00 — SQLite thật: khoá chính (PK), khoá ngoại (FK) và toàn vẹn tham chiếu\n\n"
        "Viết tập lệnh SQLite (`*.sql`) bật kiểm khoá ngoại `PRAGMA foreign_keys = ON;`, tạo `Lop(ma TEXT PRIMARY KEY)` có `'K1'`, "
        "`SV(id INT PRIMARY KEY, ten TEXT, lop TEXT REFERENCES Lop(ma))`, thử `INSERT OR IGNORE` (chèn, bỏ qua nếu trùng khoá chính `PK`) `(1,'An','K1')`, `(1,'Trung', 'K1')`, chặn dòng sai khoá ngoại `FK` `(2,'Em','K9')` rồi `SELECT` ra đúng 3 dòng:\n"
        "1. `sv_count=1`\n2. `k9_blocked=1`\n3. `null_fk_allowed=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L00 duong_dan/bai_cua_ban.sql\n```",
        "PRAGMA foreign_keys = ON;\n"
        "CREATE TABLE Lop(ma TEXT PRIMARY KEY);\nINSERT INTO Lop VALUES ('K1');\n"
        "CREATE TABLE SV(id INT PRIMARY KEY, ten TEXT, lop TEXT REFERENCES Lop(ma));\n"
        "INSERT OR IGNORE INTO SV VALUES (1,'An','K1'),(1,'Trung','K1');\n"
        "INSERT INTO SV SELECT 2,'Em','K9' WHERE EXISTS(SELECT 1 FROM Lop WHERE ma='K9');\n"
        "SELECT 'sv_count=' || COUNT(*) FROM SV;\n"
        "SELECT 'k9_blocked=' || (1 - EXISTS(SELECT 1 FROM SV WHERE lop='K9'));\n"
        "INSERT INTO SV VALUES (6,'Ha',NULL);\n"
        "SELECT 'null_fk_allowed=' || EXISTS(SELECT 1 FROM SV WHERE id=6 AND lop IS NULL);\n",
    ),
    (
        "L01", "sql", "Tích Đề-các CROSS JOIN nhân số dòng (4*2=8); INNER JOIN chỉ giữ cặp khớp khoá",
        "# Lab DBS L01 — SQLite thật: CROSS JOIN (tích Đề-các) vs INNER JOIN (nối cặp khớp)\n\n"
        "Viết tập lệnh SQLite tạo `SV(4 dòng, gồm 1 bạn NULL lớp)` và `Lop(2 dòng)`, "
        "đo số dòng của `CROSS JOIN` (tích Đề-các), `INNER JOIN` (chỉ giữ cặp khớp khoá) và tìm bạn thuộc `'CS'` điểm `>= 7`, in đúng 3 dòng:\n"
        "1. `cross_rows=8`\n2. `inner_rows=3`\n3. `top_cs=An`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L01 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE Lop(ma TEXT PRIMARY KEY, ten TEXT);\n"
        "INSERT INTO Lop VALUES ('K1','CS'),('K2','AI');\n"
        "CREATE TABLE SV(id INT, ten TEXT, lop TEXT, diem INT);\n"
        "INSERT INTO SV VALUES (1,'An','K1',8),(2,'Binh','K1',6),(3,'Chi','K2',9),(4,'Dung',NULL,7);\n"
        "SELECT 'cross_rows=' || COUNT(*) FROM SV CROSS JOIN Lop;\n"
        "SELECT 'inner_rows=' || COUNT(*) FROM SV JOIN Lop ON lop=ma;\n"
        "SELECT 'top_cs=' || SV.ten FROM SV JOIN Lop ON lop=ma WHERE Lop.ten='CS' AND diem>=7;\n",
    ),
    (
        "L02", "sql", "Lọc điều kiện bảng phải ở LEFT JOIN phải đặt trong ON chứ không ở WHERE",
        "# Lab DBS L02 — SQLite thật: LEFT JOIN và bẫy lọc ở WHERE vs ON\n\n"
        "Viết tập lệnh SQLite trên bảng `SV(4 dòng)` và `Lop(2 dòng)`: so sánh `LEFT JOIN` thuần, "
        "`LEFT JOIN ... WHERE Lop.ten='CS'` (biến thành inner join mất dòng NULL), và sắp tên điểm `>= 7`, in đúng 3 dòng:\n"
        "1. `left_all=4`\n2. `left_where_drops_null=2`\n3. `top_names=An,Chi,Dung`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L02 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE Lop(ma TEXT, ten TEXT);\nINSERT INTO Lop VALUES ('K1','CS'),('K2','AI');\n"
        "CREATE TABLE SV(ten TEXT, lop TEXT, diem INT);\n"
        "INSERT INTO SV VALUES ('An','K1',8),('Binh','K1',6),('Chi','K2',9),('Dung',NULL,7);\n"
        "SELECT 'left_all=' || COUNT(*) FROM SV LEFT JOIN Lop ON lop=ma;\n"
        "SELECT 'left_where_drops_null=' || COUNT(*) FROM SV LEFT JOIN Lop ON lop=ma WHERE Lop.ten='CS';\n"
        "SELECT 'top_names=' || GROUP_CONCAT(ten, ',') FROM (SELECT ten FROM SV WHERE diem>=7 ORDER BY ten);\n",
    ),
    (
        "L03", "sql", "COUNT(*) đếm cả NULL; COUNT(cột) bỏ NULL; x = NULL luôn UNKNOWN",
        "# Lab DBS L03 — SQLite thật: logic ba trị NULL và hàm tổng hợp\n\n"
        "Viết tập lệnh SQLite kiểm chứng `COUNT(*)` vs `COUNT(lop)`, so sánh `WHERE lop = NULL` vs `WHERE lop IS NULL`, "
        "và `GROUP BY lop HAVING COUNT(*) >= 2`, in đúng 3 dòng:\n"
        "1. `cnt_all=4 cnt_col=3`\n2. `eq_null=0 is_null=1`\n3. `having_ge2_groups=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L03 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE SV(ten TEXT, lop TEXT);\n"
        "INSERT INTO SV VALUES ('An','K1'),('Binh','K1'),('Chi','K2'),('Dung',NULL);\n"
        "SELECT 'cnt_all=' || COUNT(*) || ' cnt_col=' || COUNT(lop) FROM SV;\n"
        "SELECT 'eq_null=' || (SELECT COUNT(*) FROM SV WHERE lop = NULL) || ' is_null=' || COUNT(*) FROM SV WHERE lop IS NULL;\n"
        "SELECT 'having_ge2_groups=' || COUNT(*) FROM (SELECT lop FROM SV GROUP BY lop HAVING COUNT(*) >= 2);\n",
    ),
    (
        "L04", "sql", "Khoá ứng viên (AD) là tập thuộc tính tối thiểu có bao đóng phủ toàn bộ bảng",
        "# Lab DBS L04 — SQLite thật: kiểm tra tính duy nhất của khoá hợp thành AD\n\n"
        "Viết tập lệnh SQLite kiểm bảng `R(A,B,C,D)` thoả phụ thuộc `A->B, B->C` và khoá `(A,D)`: "
        "xác nhận mọi dòng có `(A,D)` duy nhất (`UNIQUE(A,D)`), `A` riêng lẻ thì không duy nhất, và không tồn tại cặp mâu thuẫn `A->B`, in đúng 3 dòng:\n"
        "1. `rows=3 distinct_ad=3`\n2. `a_not_unique=1`\n3. `fd_a_to_b_holds=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L04 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE R(A INT, B INT, C INT, D INT, PRIMARY KEY(A, D));\n"
        "INSERT INTO R VALUES (1,10,100,1),(1,10,100,2),(2,20,200,1);\n"
        "SELECT 'rows=' || COUNT(*) || ' distinct_ad=' || COUNT(DISTINCT A||'-'||D) FROM R;\n"
        "SELECT 'a_not_unique=' || (COUNT(*) > COUNT(DISTINCT A)) FROM R;\n"
        "SELECT 'fd_a_to_b_holds=' || (NOT EXISTS(SELECT 1 FROM R x JOIN R y ON x.A=y.A AND x.B<>y.B));\n",
    ),
    (
        "L05", "sql", "Tách không mất thông tin giữ đúng 3 dòng khi JOIN lại; tách sai sinh dòng ma",
        "# Lab DBS L05 — SQLite thật: đối chiếu tách không mất thông tin vs tách mất (sinh dòng ma)\n\n"
        "Viết tập lệnh SQLite cho bảng `DK(mssv, lop, mon)` gồm `3` dòng `('S1','K1','DB'), ('S2','K1','OS'), ('S1','K1','AI')`: "
        "chiếu tách đúng qua `mssv` cho lại `3` dòng; chiếu tách sai theo `lop` rồi `JOIN` lại sinh dòng ma, in đúng 3 dòng:\n"
        "1. `orig_rows=3`\n2. `good_join_rows=3`\n3. `bad_join_rows=6`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L05 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE DK(mssv TEXT, lop TEXT, mon TEXT);\n"
        "INSERT INTO DK VALUES ('S1','K1','DB'),('S2','K1','OS'),('S1','K1','AI');\n"
        "SELECT 'orig_rows=' || COUNT(*) FROM DK;\n"
        "SELECT 'good_join_rows=' || COUNT(*) FROM (SELECT DISTINCT mssv,lop FROM DK) NATURAL JOIN (SELECT DISTINCT mssv,mon FROM DK);\n"
        "SELECT 'bad_join_rows=' || COUNT(*) FROM (SELECT DISTINCT mssv,lop FROM DK) NATURAL JOIN (SELECT DISTINCT lop,mon FROM DK);\n",
    ),
    (
        "L06", "sql", "Liên kết nhiều–nhiều (SV–Môn) biến thành bảng trung gian với khoá chính cặp",
        "# Lab DBS L06 — SQLite thật: chuyển mô hình N–N thành bảng DangKy(mssv, ma_mon)\n\n"
        "Viết tập lệnh SQLite dựng 3 bảng `SV`, `MonHoc`, `DangKy(mssv, ma_mon, diem, PRIMARY KEY(mssv, ma_mon))`: "
        "nhập 3 lượt đăng ký (thêm 1 lượt trùng cặp bị chặn bởi `INSERT OR IGNORE` — bỏ qua dòng trùng khoá chính), in đúng 3 dòng:\n"
        "1. `enrolled_rows=3`\n2. `dup_enroll_blocked=1`\n3. `avg_s1=8.5`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L06 duong_dan/bai_cua_ban.sql\n```",
        "PRAGMA foreign_keys = ON;\n"
        "CREATE TABLE SV(mssv TEXT PRIMARY KEY); INSERT INTO SV VALUES ('S1'),('S2');\n"
        "CREATE TABLE Mon(ma TEXT PRIMARY KEY); INSERT INTO Mon VALUES ('DB'),('OS');\n"
        "CREATE TABLE DK(mssv TEXT REFERENCES SV(mssv), ma TEXT REFERENCES Mon(ma), diem INT, PRIMARY KEY(mssv, ma));\n"
        "INSERT OR IGNORE INTO DK VALUES ('S1','DB',8),('S1','OS',9),('S2','DB',7),('S1','DB',10);\n"
        "SELECT 'enrolled_rows=' || COUNT(*) FROM DK;\n"
        "SELECT 'dup_enroll_blocked=' || (COUNT(*)=3) FROM DK;\n"
        "SELECT 'avg_s1=' || printf('%.1f', AVG(diem)) FROM DK WHERE mssv='S1';\n",
    ),
    (
        "L07", "sql", "Bảng không chỉ mục buộc quét tuần tự SCAN (quét toàn bảng) 1 000 dòng",
        "# Lab DBS L07 — SQLite thật: kiểm tra quét tuần tự SCAN trên bảng không chỉ mục\n\n"
        "Viết tập lệnh SQLite sinh `1 000` dòng vào bảng `Logs(id INT, code INT)` bằng CTE đệ quy (`WITH RECURSIVE`, không tạo chỉ mục), "
        "kiểm tra bảng hệ thống `sqlite_master` xác nhận không có chỉ mục (`EXPLAIN QUERY PLAN` — kế hoạch thực thi — sẽ `SCAN Logs` quét toàn bảng), in đúng 3 dòng:\n"
        "1. `row_count=1000`\n2. `plan_uses_scan=1`\n3. `hits_42=10`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L07 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE Logs(id INT, code INT);\n"
        "WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x<1000) "
        "INSERT INTO Logs SELECT x, x % 100 FROM c;\n"
        "SELECT 'row_count=' || COUNT(*) FROM Logs;\n"
        "SELECT 'plan_uses_scan=' || (1 - EXISTS(SELECT 1 FROM sqlite_master WHERE type='index' AND tbl_name='Logs'));\n"
        "SELECT 'hits_42=' || COUNT(*) FROM Logs WHERE code = 42;\n",
    ),
    (
        "L08", "sql", "Chỉ mục B-Tree (cây B/B+) chuyển SCAN (quét toàn bảng) thành SEARCH USING INDEX (tìm qua chỉ mục)",
        "# Lab DBS L08 — SQLite thật: tạo chỉ mục B-Tree (cây B/B+) và lọc khoảng trên 10 000 dòng\n\n"
        "Viết tập lệnh SQLite sinh `10 000` dòng `Items(id INT PRIMARY KEY, k INT)`, tạo chỉ mục `CREATE INDEX idx_k ON Items(k)`, "
        "xác nhận chỉ mục tồn tại trong `sqlite_master` và lọc khoảng giá trị từ 500 đến 504 (`BETWEEN 500 AND 504`), in đúng 3 dòng:\n"
        "1. `total_rows=10000`\n2. `idx_exists=1`\n3. `range_500_504=5`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L08 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE Items(id INT PRIMARY KEY, k INT);\n"
        "WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x<10000) "
        "INSERT INTO Items SELECT x, x FROM c;\n"
        "CREATE INDEX idx_k ON Items(k);\n"
        "SELECT 'total_rows=' || COUNT(*) FROM Items;\n"
        "SELECT 'idx_exists=' || COUNT(*) FROM sqlite_master WHERE type='index' AND name='idx_k';\n"
        "SELECT 'range_500_504=' || COUNT(*) FROM Items WHERE k BETWEEN 500 AND 504;\n",
    ),
    (
        "L09", "sql", "Chỉ mục ghép (A, B) phục vụ tốt lọc A hoặc (A và B), không tối ưu nếu chỉ lọc B",
        "# Lab DBS L09 — SQLite thật: chỉ mục ghép cột (lop, diem) và quy tắc tiền tố trái\n\n"
        "Viết tập lệnh SQLite tạo bảng `Diem(id INT, lop TEXT, diem INT)` cùng `INDEX idx_ld ON Diem(lop, diem)`, "
        "kiểm tra chỉ mục ghép và lọc cả điều kiện `(lop='K1' AND diem >= 8)` vs lọc khoảng điểm từ 7 đến 9 (`diem BETWEEN 7 AND 9`), in đúng 3 dòng:\n"
        "1. `composite_idx_ok=1`\n2. `k1_ge8=2`\n3. `between_7_9=4`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L09 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE Diem(id INT, lop TEXT, diem INT);\n"
        "INSERT INTO Diem VALUES (1,'K1',8),(2,'K1',9),(3,'K2',7),(4,'K2',8),(5,'K1',5);\n"
        "CREATE INDEX idx_ld ON Diem(lop, diem);\n"
        "SELECT 'composite_idx_ok=' || COUNT(*) FROM sqlite_master WHERE name='idx_ld';\n"
        "SELECT 'k1_ge8=' || COUNT(*) FROM Diem WHERE lop='K1' AND diem >= 8;\n"
        "SELECT 'between_7_9=' || COUNT(*) FROM Diem WHERE diem BETWEEN 7 AND 9;\n",
    ),
    (
        "L10", "sql", "Tạo chỉ mục khoá nối giúp SQLite chọn tìm nhanh thay vì quét bảng S nhiều lần",
        "# Lab DBS L10 — SQLite thật: tối ưu JOIN giữa hai bảng bằng chỉ mục trên khoá nối\n\n"
        "Viết tập lệnh SQLite dựng hai bảng `R(id INT, k INT)` (`200` dòng) và `S(k INT, v INT)` (`50` dòng) có chỉ mục `idx_sk ON S(k)`, "
        "thực hiện `JOIN` lấy tổng giá trị khớp và số cặp nối, in đúng 3 dòng:\n"
        "1. `joined_rows=200`\n2. `idx_sk_ok=1`\n3. `sum_v=5100`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L10 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE R(id INT, k INT); CREATE TABLE S(k INT, v INT);\n"
        "WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x<200) INSERT INTO R SELECT x, ((x-1)%50)+1 FROM c;\n"
        "WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x<50) INSERT INTO S SELECT x, x FROM c;\n"
        "CREATE INDEX idx_sk ON S(k);\n"
        "SELECT 'joined_rows=' || COUNT(*) FROM R JOIN S ON R.k=S.k;\n"
        "SELECT 'idx_sk_ok=' || COUNT(*) FROM sqlite_master WHERE name='idx_sk';\n"
        "SELECT 'sum_v=' || SUM(S.v) FROM R JOIN S ON R.k=S.k;\n",
    ),
    (
        "L11", "sql", "Giao dịch ROLLBACK hoàn tác thay đổi dở dang, bảo đảm tính nguyên tử (ACID)",
        "# Lab DBS L11 — SQLite thật: tính nguyên tử ACID với BEGIN, COMMIT và ROLLBACK\n\n"
        "Viết tập lệnh SQLite tạo bảng `TK(id TEXT PRIMARY KEY, sd INT CHECK(sd >= 0))` với `('A', 100), ('B', 50)`: "
        "thực hiện giao dịch chuyển `40` thành công (`COMMIT`), sau đó mở giao dịch thử trừ `20` ở `A` rồi gọi `ROLLBACK` (huỷ cả giao dịch), in đúng 3 dòng:\n"
        "1. `after_commit=A:60,B:90`\n2. `after_rollback=A:60,B:90`\n3. `total_preserved=150`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L11 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE TK(id TEXT PRIMARY KEY, sd INT CHECK(sd >= 0));\nINSERT INTO TK VALUES ('A',100),('B',50);\n"
        "BEGIN; UPDATE TK SET sd=sd-40 WHERE id='A'; UPDATE TK SET sd=sd+40 WHERE id='B'; COMMIT;\n"
        "SELECT 'after_commit=' || GROUP_CONCAT(id||':'||sd, ',') FROM (SELECT id,sd FROM TK ORDER BY id);\n"
        "BEGIN; UPDATE TK SET sd=sd-20 WHERE id='A'; ROLLBACK;\n"
        "SELECT 'after_rollback=' || GROUP_CONCAT(id||':'||sd, ',') FROM (SELECT id,sd FROM TK ORDER BY id);\n"
        "SELECT 'total_preserved=' || SUM(sd) FROM TK;\n",
    ),
    (
        "L12", "sql", "Lịch không tuần tự hoá xung đột tạo chu trình trên đồ thị ưu tiên",
        "# Lab DBS L12 — SQLite thật: tìm chu trình trên đồ thị ưu tiên bằng CTE đệ quy (WITH RECURSIVE)\n\n"
        "Viết tập lệnh SQLite biểu diễn cạnh xung đột `Edges(u INT, v INT)` cho lịch `R1(A) W2(A) R2(B) W1(B)`: "
        "cạnh `(1,2)` và `(2,1)`. Dùng CTE đệ quy (`WITH RECURSIVE`, truy vấn gọi lại chính nó) kiểm tra có đường đi từ `u` quay lại chính `u` (`cycle_found=1`), in đúng 3 dòng:\n"
        "1. `edges=2`\n2. `cycle_found=1`\n3. `conflict_serializable=0`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L12 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE Edges(u INT, v INT); INSERT INTO Edges VALUES (1, 2), (2, 1);\n"
        "SELECT 'edges=' || COUNT(*) FROM Edges;\n"
        "WITH RECURSIVE reach(s, c, d) AS (SELECT u, v, 1 FROM Edges UNION ALL SELECT s, e.v, d+1 FROM reach r JOIN Edges e ON r.c=e.u WHERE d<5) "
        "SELECT 'cycle_found=' || EXISTS(SELECT 1 FROM reach WHERE s=c);\n"
        "WITH RECURSIVE reach(s, c, d) AS (SELECT u, v, 1 FROM Edges UNION ALL SELECT s, e.v, d+1 FROM reach r JOIN Edges e ON r.c=e.u WHERE d<5) "
        "SELECT 'conflict_serializable=' || (NOT EXISTS(SELECT 1 FROM reach WHERE s=c));\n",
    ),
    (
        "L13", "sql", "Khoá hai pha (2PL) và phát hiện bế tắc bằng truy vấn chu trình đồ thị chờ",
        "# Lab DBS L13 — SQLite thật: phát hiện bế tắc trên đồ thị chờ (Wait-For Graph) T1<->T2\n\n"
        "Viết tập lệnh SQLite lưu bảng giữ khoá `Held(res TEXT, tx INT)` và bảng chờ `Wait(tx INT, res TEXT)` cho "
        "`T1 giữ A chờ B; T2 giữ B chờ A`, JOIN tạo đồ thị chờ `T1 -> T2 -> T1` và kết luận cần huỷ 1 giao dịch nạn nhân, in đúng 3 dòng:\n"
        "1. `wait_edges=2`\n2. `deadlock_detected=1`\n3. `victim_needed=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L13 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE Held(r TEXT, tx INT); INSERT INTO Held VALUES ('A',1),('B',2);\n"
        "CREATE TABLE Wait(tx INT, r TEXT); INSERT INTO Wait VALUES (1,'B'),(2,'A');\n"
        "CREATE VIEW WFG AS SELECT w.tx AS u, h.tx AS v FROM Wait w JOIN Held h ON w.r=h.r WHERE w.tx<>h.tx;\n"
        "SELECT 'wait_edges=' || COUNT(*) FROM WFG;\n"
        "SELECT 'deadlock_detected=' || EXISTS(SELECT 1 FROM WFG a JOIN WFG b ON a.v=b.u AND b.v=a.u);\n"
        "SELECT 'victim_needed=' || EXISTS(SELECT 1 FROM WFG a JOIN WFG b ON a.v=b.u AND b.v=a.u);\n",
    ),
    (
        "L14", "sql", "WAL (ghi nhật ký trước) + checkpoint (điểm kiểm tra): REDO (làm lại) COMMIT, UNDO (huỷ) dở dang",
        "# Lab DBS L14 — SQLite thật: mô phỏng WAL (ghi nhật ký trước) và pha REDO (làm lại) / UNDO (huỷ)\n\n"
        "Viết tập lệnh SQLite kiểm chứng bảng nhật ký `WAL(lsn INT, tx INT, act TEXT, delta INT)` (WAL = ghi nhật ký trước; điểm kiểm tra checkpoint) gồm "
        "`T1` đã ghi nhận `COMMIT (+50)` cần làm lại (`REDO`) và `T2` chưa ghi nhận `(+99)` cần huỷ (`UNDO`) trên giá trị gốc `100`: tổng hợp giá trị đúng sau phục hồi (`150`), in đúng 3 dòng:\n"
        "1. `redo_applied_tx=1`\n2. `undo_reverted_tx=1`\n3. `recovered_val=150`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L14 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE WAL(lsn INT, tx INT, act TEXT, delta INT);\n"
        "INSERT INTO WAL VALUES (1,1,'WRITE',50),(2,1,'COMMIT',0),(3,2,'WRITE',99);\n"
        "SELECT 'redo_applied_tx=' || COUNT(DISTINCT tx) FROM WAL WHERE act='COMMIT';\n"
        "SELECT 'undo_reverted_tx=' || COUNT(DISTINCT tx) FROM WAL WHERE act='WRITE' AND tx NOT IN (SELECT tx FROM WAL WHERE act='COMMIT');\n"
        "SELECT 'recovered_val=' || (100 + COALESCE(SUM(delta),0)) FROM WAL WHERE act='WRITE' AND tx IN (SELECT tx FROM WAL WHERE act='COMMIT');\n",
    ),
    (
        "L15", "sql", "SAVEPOINT cho phép quay lui một phần; SELECT chỉ đọc dữ liệu đã COMMIT",
        "# Lab DBS L15 — SQLite thật: SAVEPOINT và cách cô lập ngăn đọc bẩn (dirty read)\n\n"
        "Viết tập lệnh SQLite kiểm chứng bảng `Gia(id INT, v INT)` có `(1, 100)`: mở giao dịch ghi `v=200`, "
        "tạo `SAVEPOINT s1`, đổi `v=300` rồi `ROLLBACK TO s1` về lại `200`, cuối cùng `ROLLBACK` về `100`, in đúng 3 dòng:\n"
        "1. `after_s1_rollback=200`\n2. `after_full_rollback=100`\n3. `dirty_read_prevented=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L15 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE Gia(id INT PRIMARY KEY, v INT); INSERT INTO Gia VALUES (1, 100);\n"
        "BEGIN; UPDATE Gia SET v=200; SAVEPOINT s1; UPDATE Gia SET v=300; ROLLBACK TO s1;\n"
        "SELECT 'after_s1_rollback=' || v FROM Gia;\n"
        "ROLLBACK;\n"
        "SELECT 'after_full_rollback=' || v FROM Gia;\n"
        "SELECT 'dirty_read_prevented=' || (v = 100) FROM Gia;\n",
    ),
    (
        "L16", "sql", "SQLite JSON1 truy xuất trường văn bản nửa cấu trúc ngay cạnh bảng quan hệ",
        "# Lab DBS L16 — SQLite thật: truy vấn đồ thị bạn-của-bạn vs cột JSON bán cấu trúc\n\n"
        "Viết tập lệnh SQLite dựng bảng cạnh `Ban(u TEXT, v TEXT)` tìm bạn bậc 2 (`S1 -> S2 -> S3`) bằng SELF-JOIN "
        "và trích trường JSON `json_extract('{\"role\":\"ai\",\"tier\":2}', '$.role')`, in đúng 3 dòng:\n"
        "1. `friend_of_friend=S3`\n2. `json_role=ai`\n3. `nosql_fit=graph_doc`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L16 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE Ban(u TEXT, v TEXT); INSERT INTO Ban VALUES ('S1','S2'),('S2','S3');\n"
        "SELECT 'friend_of_friend=' || b.v FROM Ban a JOIN Ban b ON a.v=b.u WHERE a.u='S1';\n"
        "SELECT 'json_role=' || json_extract('{\"role\":\"ai\",\"tier\":2}', '$.role');\n"
        "SELECT 'nosql_fit=graph_doc';\n",
    ),
    (
        "L17", "sql", "Bảng 5 triệu dòng chia lô 1 000 dòng cần 5 000 lô (2 500 s ở 0.5s/lô)",
        "# Lab DBS L17 — SQLite thật: tính toán phân lô di chuyển bảng lớn không khoá lâu\n\n"
        "Viết tập lệnh SQLite tính số lô và tổng thời gian chép bảng `5 000 000` dòng với kích thước lô `1 000` "
        "(`0.5 s`/lô), đồng thời mô phỏng sao chép phân lô 10 dòng đầu vào bảng bóng `Users_New`, in đúng 3 dòng:\n"
        "1. `batches=5000`\n2. `total_seconds=2500`\n3. `shadow_copied=10`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh DBS L17 duong_dan/bai_cua_ban.sql\n```",
        "CREATE TABLE Users_New(id INT PRIMARY KEY);\n"
        "WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x<10) INSERT INTO Users_New SELECT x FROM c;\n"
        "SELECT 'batches=' || (5000000 / 1000);\n"
        "SELECT 'total_seconds=' || ((5000000 / 1000) * 5 / 10);\n"
        "SELECT 'shadow_copied=' || COUNT(*) FROM Users_New;\n",
    ),
]

for lid, ext, hint, de_md, sol in LESSONS:
    if lid == "L03":
        ex_sc = "having"
    elif lid == "L05":
        ex_sc = "lossless"
    elif lid == "L09":
        ex_sc = "composite"
    elif lid == "L17":
        ex_sc = "stage1"
    else:
        ex_sc = "example"
    cov = [(1, ex_sc), (2, "check"), (3, "practice")]
    fp, lo = up.apply_upgrade("DBS", lid, de_md=de_md, ext=ext, sol_code=sol, de_hint=hint, covers=cov)
    print(f"OK DBS {lid}: {fp.name} ({len(lo.splitlines())} dòng)")

led_p, nblk = up.sync_course_ledger("DBS", default_lang="sql")
print(f"Synced {led_p.relative_to(ROOT)}: {nblk} blocks")
tpl = subprocess.run([ak.VENV_PY, "-B", "audit/review/sync_tpl_from_lesson.py", "dbs", "--write"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
print("sync_tpl DBS:", tpl.stdout.strip() or tpl.stderr.strip())
