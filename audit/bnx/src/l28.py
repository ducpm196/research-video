import lib2
from lib2 import *
from l16 import _spoken  # ghép câu quá ngắn vào câu bên cạnh, giữ focus
from libj import jstep, nowrap
from labkit import write_lab, practice_steps, practice_scene

lib2.begin("L28")

# ── Mã chạy THẬT bằng ảnh Docker chính thức, mỗi lần một ảnh, dừng và xoá ngay (docker run --rm; tên bnx-l28-*): ──
#   PostgreSQL 17 (postgres:17-alpine, ghim băm), MongoDB 8 (mongo:8, ghim băm), MySQL 8.4 (mysql:8.4, ghim băm); Oracle và SQL Server dùng container có sẵn
#   bnx-ora, bnx-mss qua audit/bnx/dbrun.py (chỉ chạy thêm hai bảng riêng bnx_l28_*; không chạm gì khác). Đầu ra tất định (đệm ở audit/bnx/progcache/L28.json).
PG_IMG = "postgres:17-alpine@sha256:d3244e8ce3f165ee3c93d9c4a4b1d0fe48b3a89e2287b717fdcbbde92d405065"
MG_IMG = "mongo:8@sha256:0f64db83d5926400d1cbcbaf35fbf2b0dfa6a4eaa71e04a26481a38cd803b27b"

X_ASQL = prog("ASql", r'''
begin;
select 1 from tk where id = 1 for update;
\! touch /tmp/a.ok
select pg_sleep(30);
commit;
''', lang="sql", kind="other", reason="Phiên A của PostgreSQL: giữ khoá dòng 30 giây, đủ dài cho máy bận (tạo tệp /tmp/a.ok khi đã giữ khoá để phiên B biết lúc nào thử).",
    read_check="Chạy nguyên văn bởi psql trong container postgres (nguồn L28_ChayPg); đầu ra phiên B khớp từng dòng.")

SH_PG = prog("ChayPg", r'''
export MSYS_NO_PATHCONV=1
C=bnx-l28-pg
IMG=''' + PG_IMG + r'''
command -v docker >/dev/null || { echo "NOT_VERIFIED: thiếu docker" >&2; exit 97; }
docker image inspect $IMG >/dev/null 2>&1 || docker pull -q $IMG >/dev/null 2>&1 || { echo "NOT_VERIFIED: không có ảnh PostgreSQL" >&2; exit 97; }
docker rm -f $C >/dev/null 2>&1
docker run --rm -d --name $C -e POSTGRES_PASSWORD=bnx_pass $IMG >/dev/null
for i in $(seq 1 90); do
  [ "$(docker logs $C 2>&1 | grep -c 'ready to accept connections')" -ge 2 ] && break
  sleep 1
done
P="docker exec -i -e PGOPTIONS=-cmax_parallel_workers_per_gather=0 $C psql -U postgres -v ON_ERROR_STOP=1 -tA"
EX="explain (analyze, costs off, timing off, summary off)"
loc() { grep -E "Scan|Rows Removed"; }
echo "phien ban: $($P -c 'show server_version')"
for n in 1000 100000 1000000; do
  $P -q -c "create table t$n (id int primary key, so text)"
  $P -q -c "insert into t$n select g, 'K'||g from generate_series(1,$n) g"
  $P -q -c "analyze t$n"
  echo "$n dong, khong chi muc:"
  $P -c "$EX select * from t$n where so = 'K7'" | loc
  $P -q -c "create index on t$n(so)"
  $P -q -c "analyze t$n"
  echo "$n dong, co chi muc:"
  $P -c "$EX select * from t$n where so = 'K7'" | loc
done
$P -q -c "create table tk (id int primary key, so_du bigint)" -c "insert into tk values (1, 1000)"
docker cp a.sql $C:/a.sql
docker exec -d $C psql -U postgres -q -o /dev/null -f /a.sql
until docker exec $C test -f /tmp/a.ok; do sleep 0.5; done
$P -c "select * from tk where id = 1 for update nowait" 2>&1 | head -1
docker rm -f $C >/dev/null 2>&1
''', lang="bash", files={"a.sql": "ASql"}, timeout=900,
    claims=["không chỉ mục: quét tuần tự, loại bỏ N−1 dòng; có chỉ mục: quét theo chỉ mục, không loại dòng nào", "NOWAIT: báo lỗi could not obtain lock on row ngay khi dòng đang bị giữ"])

SH_MG = prog("ChayMg", r'''
export MSYS_NO_PATHCONV=1
C=bnx-l28-mg
IMG=''' + MG_IMG + r'''
command -v docker >/dev/null || { echo "NOT_VERIFIED: thiếu docker" >&2; exit 97; }
docker image inspect $IMG >/dev/null 2>&1 || docker pull -q $IMG >/dev/null 2>&1 || { echo "NOT_VERIFIED: không có ảnh MongoDB" >&2; exit 97; }
docker rm -f $C >/dev/null 2>&1
docker run --rm -d --name $C $IMG >/dev/null
for i in $(seq 1 90); do
  docker exec $C mongosh --quiet --eval "db.runCommand({ping: 1}).ok" 2>/dev/null | grep -q 1 && break
  sleep 1
done
js() { docker exec $C mongosh --quiet --eval "$1"; }
js 'print("phien ban: " + db.version())'
js '
db.tk.insertMany([
  {_id: "001", ten: "An", so_du: 1000, gd: [{so: 600, loai: "nap"}, {so: 50, loai: "rut"}]},
  {_id: "002", ten: "Binh", so_du: 300, gd: []}]);
print(JSON.stringify(db.tk.findOne({_id: "001"})));
print("co gd rut: " + db.tk.countDocuments({"gd.loai": "rut"}))'
js '
var lo = [];
for (var i = 1; i <= 100000; i++) lo.push({_id: "T" + i, so: "S" + i});
db.lon.insertMany(lo);
var kieu = () => JSON.stringify(db.lon.find({so: "S777"}).explain("executionStats").executionStats).match(/"totalDocsExamined":(\d+)/)[1];
print("khong chi muc: xem " + kieu() + " tai lieu");
db.lon.createIndex({so: 1});
print("co chi muc: xem " + kieu() + " tai lieu")'
js '
var rut = () => db.tk.updateOne({_id: "001", so_du: {$gte: 600}}, {$inc: {so_du: -600}}).modifiedCount;
print("rut 600 lan 1: " + rut());
print("rut 600 lan 2: " + rut());
print("so du con lai: " + db.tk.findOne({_id: "001"}).so_du)'
docker rm -f $C >/dev/null 2>&1
''', lang="bash", timeout=600,
    claims=["tài liệu lồng nhau đọc trong một lần; không chỉ mục xem 100000 tài liệu, có chỉ mục xem 1; cập nhật có điều kiện trên một tài liệu là nguyên tử"])

X_MYSQL_ASQL = prog("MysqlA", r'''
begin;
select 1 from tk where id = 1 for update;
select sleep(30);
commit;
''', lang="sql", kind="other", reason="Phiên A của MySQL: giữ khoá dòng 30 giây, đủ dài cho máy bận (container bị gỡ ngay sau khi phiên B thử).", read_check="Chạy nguyên văn bởi mysql trong container mysql (nguồn L28_ChayMy).")

SH_MY = prog("ChayMy", r'''
export MSYS_NO_PATHCONV=1
C=bnx-l28-my
IMG=''' + "mysql:8.4@sha256:a81d043930e51745522bd5c430961cf8286f0a23f0a9a2a6e0108f7ea71b0902" + r'''
command -v docker >/dev/null || { echo "NOT_VERIFIED: thiếu docker" >&2; exit 97; }
docker image inspect $IMG >/dev/null 2>&1 || docker pull -q $IMG >/dev/null 2>&1 || { echo "NOT_VERIFIED: không có ảnh MySQL" >&2; exit 97; }
docker rm -f $C >/dev/null 2>&1
docker run --rm -d --name $C -e MYSQL_ROOT_PASSWORD=bnx_pass -e MYSQL_DATABASE=bnx $IMG >/dev/null
for i in $(seq 1 180); do
  docker logs $C 2>&1 | grep -q 'Ready for start up' && break
  sleep 1
done
for i in $(seq 1 180); do
  docker exec $C mysqladmin -uroot -pbnx_pass ping 2>/dev/null | grep -q alive && break
  sleep 1
done
M="docker exec -i $C mysql -uroot -pbnx_pass bnx -N"
q() { $M -e "$1" 2>&1 | grep -v "Using a password"; }
wait_lock() { for i in $(seq 1 60); do [ "$(q "select count(*) from performance_schema.data_locks where lock_type = 'RECORD'" | tail -1)" -gt 0 ] 2>/dev/null && return; sleep 1; done; }
echo "phien ban: $(q 'select version()')"
q "create table tk (id int primary key, so varchar(20), so_du bigint)"
q "set session cte_max_recursion_depth = 100000; insert into tk select seq, concat('K', seq), seq * 10 from (with recursive s(seq) as (select 1 union all select seq + 1 from s where seq < 20000) select seq from s) x"
echo "so dong: $(q 'select count(*) from tk')"
echo "khong chi muc: $(q "explain select * from tk where so = 'K7'" | cut -f5)"
q "create index idx_so on tk(so)"
echo "co chi muc: $(q "explain select * from tk where so = 'K7'" | cut -f5)"
docker cp mysqla.sql $C:/mysqla.sql
docker exec -d $C sh -c "mysql -uroot -pbnx_pass bnx < /mysqla.sql > /dev/null 2>&1"
wait_lock
q "select * from tk where id = 1 for update nowait" | head -1
docker rm -f $C >/dev/null 2>&1
''', lang="bash", files={"mysqla.sql": "MysqlA"}, timeout=900,
    claims=["MySQL: không chỉ mục kiểu truy cập ALL, có chỉ mục ref; NOWAIT báo lỗi ngay khi dòng bị giữ"])

PY_KHOA = prog("SoSanhKhoa", r'''
import sys, threading, time, re
sys.path.insert(0, "D:/research-video/audit/bnx")
import dbrun

dbrun.ora("""
BEGIN EXECUTE IMMEDIATE 'DROP TABLE bnx_l28_tk'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
CREATE TABLE bnx_l28_tk (id NUMBER PRIMARY KEY, so_du NUMBER);
INSERT INTO bnx_l28_tk VALUES (1, 1000);
COMMIT;
""")
a = threading.Thread(target=dbrun.ora, args=("""
DECLARE x NUMBER;
BEGIN
  SELECT so_du INTO x FROM bnx_l28_tk WHERE id = 1 FOR UPDATE;
  DBMS_SESSION.SLEEP(9);
  ROLLBACK;
END;
/
""",))
a.start()
time.sleep(5)
o = dbrun.ora("SELECT so_du FROM bnx_l28_tk WHERE id = 1 FOR UPDATE NOWAIT;")
a.join()
print("Oracle:", re.search(r"ORA-\d+: [^\n(]+", o).group(0).strip())
dbrun.ora("DROP TABLE bnx_l28_tk PURGE;")

dbrun.mss("IF DB_ID('bnx_l28') IS NULL CREATE DATABASE bnx_l28")
dbrun.mss("DROP TABLE IF EXISTS tk; CREATE TABLE tk (id INT PRIMARY KEY, so_du BIGINT); INSERT INTO tk VALUES (1, 1000)", db="bnx_l28")
giu = """BEGIN TRAN;
UPDATE tk SET so_du = so_du WHERE id = 1;
WAITFOR DELAY '00:00:09';
ROLLBACK"""
b = threading.Thread(target=dbrun.mss, args=(giu,), kwargs={"db": "bnx_l28"})
b.start()
time.sleep(5)
xin = """SET LOCK_TIMEOUT 0;
SELECT so_du FROM tk WITH (UPDLOCK, ROWLOCK) WHERE id = 1"""
o = dbrun.mss(xin, db="bnx_l28")
b.join()
m = re.search(r"Msg (\d+), Level \d+, State \d+, Server \S+, Line \d+\s*\n?(.+)", o)
print("SQL Server: Msg " + m.group(1) + ": " + m.group(2).strip())
dbrun.mss("DROP TABLE IF EXISTS tk", db="bnx_l28")
''', lang="python", timeout=300,
    claims=["Oracle: FOR UPDATE NOWAIT báo ORA-00054; SQL Server: LOCK_TIMEOUT 0 báo Msg 1222"], reason="Hai phiên song song trên Oracle (bnx-ora) và SQL Server (bnx-mss) của khoá BNX; bảng riêng bnx_l28_tk / cơ sở dữ liệu bnx_l28, tự dọn.")

# ── Lab (cham.sh, Python): rút tiền có điều kiện so với đọc rồi ghi ──
LAB_PY = r'''
def rut_co_dieu_kien(tk, so):
    if tk["so_du"] >= so:
        tk["so_du"] -= so
        return 1
    return 0


tk = {"so_du": 700}
kq = [rut_co_dieu_kien(tk, r) for r in (500, 500, 200)]
print("co dieu kien:", *kq, "con", tk["so_du"])

so_du = 700
doc_a = doc_b = so_du                 # hai bên cùng đọc trước khi ai ghi
so_du = doc_a - 500                   # A ghi
so_du = doc_b - 500                   # B ghi đè
mat = 500 + 500 - (700 - so_du)
print(f"doc roi ghi: A doc {doc_a}, B doc {doc_b}, ghi 200 va 200, con {so_du} (mat {mat})")
'''
LAB_OUT = """co dieu kien: 1 0 1 con 0
doc roi ghi: A doc 700, B doc 700, ghi 200 va 200, con 200 (mat 500)"""
LAB_DE = """# Lab BNX L28 — Rút tiền có điều kiện so với đọc rồi ghi

Tài khoản có số dư **700** (số minh hoạ). Trong cơ sở dữ liệu lưu bản ghi JSON, lệnh cập nhật có điều kiện kiểu `{so_du: {$gte: số rút}}` chỉ trừ khi còn đủ tiền, **kiểm và trừ trong một bước**.

Viết `mau.py`:
1. Hàm `rut_co_dieu_kien(tk, so)` (tk là từ điển `{"so_du": …}`): nếu `so_du >= so` thì trừ và trả `1`, ngược lại không đổi và trả `0`. Gọi lần lượt rút 500, 500, 200 rồi in `co dieu kien: <ba số> con <số dư>`, trong đó ba số (mỗi số là 1 hoặc 0, theo thứ tự ba lần rút) cách nhau bằng MỘT dấu cách.
2. Mô phỏng sai lầm đọc-rồi-ghi: A và B cùng đọc số dư 700; A ghi `700 − 500`, rồi B ghi đè `700 − 500`. In
   `doc roi ghi: A doc 700, B doc 700, ghi 200 va 200, con 200 (mat 500)` — số mất = tổng đã chi (500 + 500) trừ số thật bị trừ.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L28 mau.py`.
"""


PY_RUT = prog("RutTien", r'''
tk = {"so_du": 1000}

def rut_co_dieu_kien(so):
    if tk["so_du"] >= so:        # kiểm và trừ trong MỘT bước
        tk["so_du"] -= so
        return 1
    return 0

print("co dieu kien:", rut_co_dieu_kien(600), rut_co_dieu_kien(600), "con", tk["so_du"])
doc_a = doc_b = 1000             # hai bên cùng đọc trước khi ai ghi
so_du = doc_a - 600              # A ghi
so_du = doc_b - 600              # B ghi đè
print("doc roi ghi: con", so_du, ", chi ra 1200 nhung chi bi tru 600")
''', lang="python", claims=["rút có điều kiện: lần 1 được, lần 2 bị từ chối, còn 400; đọc rồi ghi: còn 400 nhưng đã chi 1200"])


def _mg_show(needle, n, title):
    """Hiện n dòng của SH_MG bắt đầu từ dòng `js '` ngay trước dòng chứa needle (để dấu nháy mở và nháy đóng cùng hiện)."""
    ls = SH_MG.code.split(chr(10))
    i = next(k for k, l in enumerate(ls) if needle in l)
    assert ls[i - 1].strip() == "js '", ls[i - 1]
    return SH_MG.show(lines=(i, i + n), title=title)


def build():
    write_lab("BNX", "L28", LAB_DE, "py", LAB_PY, LAB_OUT)
    hook = sc("hook", "hook", "Cùng một lệnh rút tiền, năm hệ cơ sở dữ liệu trả lời khác nhau", [
        st("""<p>Hai nhân viên cùng lúc thao tác trên một tài khoản. Nhân viên thứ hai xin khoá dòng <b>không chờ</b>. Chạy thật trên năm hệ:</p>
<div class="box key">PostgreSQL báo <code>could not obtain lock on row</code>; Oracle báo <code>ORA-00054</code>; SQL Server báo <code>Msg 1222</code>; MySQL báo <code>ERROR 3572</code>. MongoDB sửa một bản ghi là nguyên tử, nên bài này dùng <b>cập nhật có điều kiện</b> thay cho khoá (MongoDB cũng có giao dịch nhiều bản ghi); hệ quan hệ cũng viết được kiểu này.
Chọn hệ nào cho sổ tiền, và khi nào chọn hệ khác?</div>""",
           """Chào bạn, hai nhân viên cùng lúc thao tác trên một tài khoản, người thứ hai xin khoá dòng nhưng không chờ. Chạy thật trên năm hệ, bốn hệ quan hệ báo lỗi ngay, mỗi hệ một mã riêng. Cơ sở dữ liệu JSON sửa một bản ghi là nguyên tử, nên dùng cập nhật có điều kiện thay cho khoá. Chọn hệ nào cho sổ tiền?""", focus=[1, 2, 2, 2, 2]),
    ], checks=["alg.bnx_l28_withdraw(1000, [600, 600]) == ([1, 0], 400)"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        st(table(["khái niệm", "nghĩa (ví dụ)"],
                 [["① bảng, khoá, chỉ mục", "bảng gồm hàng cột; <b>khoá chính</b>: cột có giá trị riêng cho từng hàng; <b>khoá ngoại</b>: cột trỏ tới khoá chính của bảng khác; <b>JOIN</b> (nối bảng): ghép hàng hai bảng theo khoá; <b>chỉ mục</b>: danh mục tra nhanh theo một cột, như mục lục sách (chỉ mục trên cột <code>so</code> để tìm tài khoản)"],
                  ["② quét tuần tự", "đọc <b>từng dòng</b> từ đầu tới cuối để tìm dòng khớp (100 000 dòng thì đọc 100 000 dòng)"],
                  ["③ khoá dòng", "khi sửa hoặc xin giữ một dòng, người khác phải chờ hoặc bị từ chối (<code>SELECT … FOR UPDATE</code>)"],
                  ["④ bản ghi JSON lồng nhau", "một bản ghi chứa luôn danh sách con, không cần bảng thứ hai (tài khoản chứa mảng giao dịch)"],
                  ["⑤ nguyên tử", "một thao tác trọn vẹn: kiểm và sửa trong một bước, không ai chen giữa (trừ tiền chỉ khi còn đủ)"]]),
           """Trước hết ta cần hiểu năm điều. Khoá chính là cột có giá trị riêng cho từng hàng, khoá ngoại trỏ tới khoá chính bảng khác, nối bảng ghép hàng theo khoá. Chỉ mục là danh mục tra nhanh theo một cột, còn quét tuần tự là đọc từng dòng từ đầu tới cuối. Khoá dòng là khi một người giữ dòng thì người khác phải chờ hoặc bị từ chối. Bản ghi JSON lồng nhau chứa luôn danh sách con, và nguyên tử là kiểm và sửa trong một bước.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6"]),
    ], checks=["alg.bnx_l28_removed(100000, False) == 99999"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên", "nghĩa"],
                 [["<code>Seq Scan</code> / <code>Index Scan</code>", "quét tuần tự / quét theo chỉ mục (kế hoạch của PostgreSQL)"],
                  ["<code>Rows Removed by Filter</code>", "số dòng đã đọc rồi <b>bị loại</b> vì không khớp điều kiện"],
                  ["<code>COLLSCAN</code> / <code>IXSCAN</code>", "quét cả kho / quét theo chỉ mục (kế hoạch của cơ sở dữ liệu lưu bản ghi JSON)"],
                  ["<code>FOR UPDATE NOWAIT</code>", "xin giữ dòng để sửa và <b>không chờ</b>: bị giữ rồi thì báo lỗi ngay"],
                  ["<code>$gte</code>, <code>$inc</code>", "toán tử của bản ghi JSON: lớn hơn hoặc bằng; cộng thêm một lượng"],
                  ["<code>updateOne(điều kiện, thay đổi)</code>", "sửa một bản ghi đúng khi điều kiện còn đúng, trong một bước"]]),
           """Quét tuần tự và quét theo chỉ mục là hai cách đọc trong kế hoạch của PostgreSQL, và dòng bị loại cho biết bao nhiêu dòng đã đọc rồi bỏ. Hai tên thứ ba là cách đọc tương ứng ở cơ sở dữ liệu JSON. Xin giữ dòng không chờ nghĩa là dòng đã bị giữ thì báo lỗi ngay. Hai toán tử là lớn hơn hoặc bằng và cộng thêm.""",
           focus=["1.2", "1.3", "1.4", "1.5", ["1.6", "1.7"]], introduces=["bnx_gte"]),
        st(table(["viết trong lệnh", "đọc là", "ví dụ nhỏ"],
                 [["<code>docker run --rm -d --name C IMG</code>", "chạy một <b>hộp</b> từ ảnh <code>IMG</code>: <code>--rm</code> tự xoá hộp khi dừng, <code>-d</code> chạy nền, <code>--name</code> đặt tên", "<code>docker run --rm -d --name x postgres</code>"],
                  ["<code>docker exec -i C …</code>, <code>docker cp a.sql C:/a.sql</code>", "<code>exec</code> chạy lệnh trong hộp đang chạy (<code>-d</code>: chạy nền); <code>cp</code> chép tệp vào hộp", "<code>docker cp a.sql x:/a.sql</code>"],
                  ["<code>P=\"docker exec … psql -tA\"</code>, <code>&#36;P -q -c \"…\"</code>", "gán cả lệnh vào biến <code>P</code>, rồi <code>&#36;P</code> thay nó vào; <code>-c</code> chạy một câu SQL rồi thoát; <code>-q</code> ít chữ; <code>-tA</code> bỏ dòng tiêu đề và căn cột", "<code>&#36;n</code>, <code>&#36;EX</code> cũng là biến"]]),
           """Các lệnh Docker: chạy dựng hộp từ ảnh, tự xoá khi dừng và chạy nền; thực thi chạy việc trong hộp đang chạy; chép đưa tệp vào hộp. Biến chứa cả lệnh, kèm hai tuỳ chọn bỏ tiêu đề và căn cột.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st(table(["viết trong lệnh", "đọc là", "ví dụ nhỏ"],
                 [["<code>loc() { grep -E \"Scan|Rows Removed\"; }</code>, <code>… | loc</code>", "<code>loc</code> là hàm lọc: giữ dòng có chữ <code>Scan</code> hoặc <code>Rows Removed</code>; dấu <code>|</code> đưa đầu ra lệnh trái vào hàm", "<code>echo ab | grep a</code> in <code>ab</code>"],
                  ["<code>generate_series(1,&#36;n)</code>, <code>analyze</code>, <code>explain (analyze, …)</code>", "<code>generate_series(1,n)</code> sinh n dòng số từ 1 tới n; <code>analyze</code> cập nhật thống kê để kế hoạch đúng; <code>explain (analyze)</code> chạy thật rồi in kế hoạch", "<code>generate_series(1,3)</code> ra 1, 2, 3"],
                  ["<code>\\! touch /tmp/a.ok</code>, <code>pg_sleep(30)</code>", "<code>\\!</code> trong <code>psql</code> chạy lệnh của vỏ lệnh; <code>touch</code> tạo tệp rỗng làm tín hiệu; <code>pg_sleep(30)</code> ngủ 30 giây để giữ khoá", "phiên B thấy <code>/tmp/a.ok</code> là biết A đã giữ khoá"]]),
           """Hàm lọc giữ các dòng có chữ cho trước. Hàm sinh dãy số tạo ra từng ấy dòng, lệnh phân tích cập nhật thống kê, lệnh xem kế hoạch chạy thật rồi in cách đọc. Dòng cuối tạo tệp tín hiệu rồi ngủ giữ khoá ba mươi giây.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True, introduces=["bnx_explain"]),
        st(table(["viết trong mã", "đọc là", "ví dụ nhỏ"],
                 [["<code>DECLARE x NUMBER; BEGIN … END; /</code>", "khối của Oracle: <code>DECLARE</code> khai biến, <code>BEGIN … END</code> là thân; <code>SELECT … INTO x</code> chép kết quả vào biến <code>x</code>; <code>ROLLBACK</code> huỷ giao dịch; <code>/</code> ở dòng riêng ra lệnh chạy khối", "<code>DBMS_SESSION.SLEEP(9)</code> ngủ 9 giây"],
                  ["<code>dbrun.ora(…)</code>, <code>threading.Thread(target=…)</code>", "<code>dbrun.ora</code> là hàm riêng của khoá gửi SQL tới Oracle trong Docker (không phải lệnh của Oracle); <code>Thread</code> chạy hàm song song, <code>start()</code> bắt đầu, <code>join()</code> đợi xong; <code>args=(x,)</code>: bộ chứa đối số đưa cho hàm, dấu phẩy cuối để thành bộ một phần tử", "<code>a.start()</code> rồi <code>a.join()</code>"],
                  ["<code>SET LOCK_TIMEOUT 0</code>, <code>WITH (UPDLOCK, ROWLOCK)</code>", "của SQL Server: <code>LOCK_TIMEOUT 0</code> là không chờ khoá; <code>UPDLOCK, ROWLOCK</code> xin khoá cập nhật mức dòng", "thay cho <code>FOR UPDATE NOWAIT</code>"]]),
           """Cuối cùng là mã chạy trên Oracle và hệ thứ hai. Khối của Oracle khai biến, chép kết quả vào biến rồi huỷ giao dịch, dấu gạch chéo ra lệnh chạy. Luồng chạy hàm song song, nhận đối số trong một bộ. Hệ thứ hai đặt thời gian chờ khoá bằng không.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["alg.bnx_l28_removed(1000, False) == 999"])

    intu = sc("intuition", "intuition", "Hình dung: bảng và bản ghi lồng nhau, chỉ mục và khoá", [
        st(svg(1500, 520,
               txt(750, 40, "Cùng một tài khoản: hai bảng nối khoá ngoại, hay một bản ghi chứa luôn giao dịch", 26, "middle", "#1f2937", True),
               panel(40, 80, 680, 330, "hệ quan hệ (PostgreSQL, MySQL, Oracle, SQL Server)", C_BLUE, 24),
               box(80, 160, 280, 100, ["bảng tk", "001 | An | 1000"], C_AMBER, 22),
               box(400, 160, 280, 130, ["bảng gd", "001 | 600 | nap", "001 | 50 | rut"], C_GREEN, 22),
               arrow(365, 210, 395, 210, "#475569", None, 20),
               txt(380, 330, "đọc cả hai: nối bảng (JOIN)", 22, "middle", "#1f2937", True),
               txt(380, 370, "lỗi nhập sai bị chặn bởi khoá ngoại và ràng buộc", 20, "middle", "#475569"),
               panel(780, 80, 680, 330, "cơ sở dữ liệu lưu bản ghi JSON", C_PURPLE, 24),
               box(820, 160, 600, 190, ["một bản ghi", "{ _id: 001, ten: An, so_du: 1000,", "  gd: [ {600, nap}, {50, rut} ] }"], C_PURPLE, 22),
               txt(1120, 380, "đọc một lần; sửa một bản ghi là nguyên tử", 22, "middle", "#1f2937", True),
               txt(750, 470, "Đánh đổi: bản ghi lồng nhau đọc nhanh và gọn, nhưng hệ quan hệ chặt chẽ hơn khi nhiều bên cùng ghi nhiều bảng", 22, "middle", "#1f2937", True)),
           """Hình này đặt hai mô hình cạnh nhau cho cùng một tài khoản. Bên trái là hệ quan hệ: giao dịch ở bảng khác nối bằng khoá ngoại, muốn đọc cả hai thì nối bảng. Bên phải là cơ sở dữ liệu JSON: một bản ghi chứa luôn giao dịch, nên đọc một lần là đủ."""),
        st(svg(1500, 480,
               txt(750, 40, "Chỉ mục: số dòng bị đọc rồi bỏ khi tìm một giá trị duy nhất", 26, "middle", "#1f2937", True),
               box(40, 110, 640, 90, ["quét tuần tự: đọc từ dòng đầu", "tới hết bảng, loại các dòng không khớp"], C_RED, 22, True),
               box(780, 110, 680, 90, ["quét theo chỉ mục: đi theo cây", "tới thẳng dòng cần tìm"], C_GREEN, 22, True),
               box(40, 260, 640, 80, ["1 000 dòng: loại 999", "100 000 dòng: loại 99 999; 1 000 000 dòng: loại 999 999"], C_AMBER, 22),
               box(780, 260, 680, 80, ["mọi cỡ bảng trên: loại 0 dòng", "(đo thật ở phần ví dụ)"], C_GREEN, 22),
               txt(750, 410, "Đánh đổi: chỉ mục làm truy vấn nhanh nhưng làm mỗi lần ghi chậm hơn và tốn chỗ", 24, "middle", "#1f2937", True)),
           """Hình thứ hai là chỉ mục: quét tuần tự đọc từ dòng đầu tới hết bảng, còn quét theo chỉ mục đi theo cây tới thẳng dòng cần tìm."""),
    ], checks=["[alg.bnx_l28_removed(n, False) for n in (1000, 100000, 1000000)] == [999, 99999, 999999]", "alg.bnx_l28_removed(1000000, True) == 0"])

    form = sc("formula", "formula", "Suy ra từng bước: từ mô hình dữ liệu tới lựa chọn", [
        jstep([(("<code>js '…'</code>, <code>print(…)</code>",
                 "<code>js</code>: hàm của mã chạy thật, gửi đoạn lệnh trong cặp nháy đơn tới <code>mongosh</code> (dòng lệnh của MongoDB) trong hộp; <code>print</code> in một dòng",
                 "Hàm gửi đoạn lệnh vào cơ sở dữ liệu JSON, nên mỗi lần gọi chạy một đoạn; lệnh in ra một dòng."), "", ""),
               (("<code>db.tk.insertMany([{…}, {…}])</code>",
                 "chèn nhiều bản ghi vào tập <code>tk</code>; <code>[ ]</code>: danh sách, <code>{ }</code>: một bản ghi, <code>tên: giá trị</code>: một trường; <code>gd: [ … ]</code>: trường chứa danh sách bản ghi con",
                 "Chèn nhiều bản ghi: ngoặc vuông là danh sách, ngoặc nhọn là một bản ghi."), "", ""),
               (("<code>JSON.stringify(db.tk.findOne({_id: \"001\"}))</code>",
                 "<code>findOne(điều kiện)</code> lấy một bản ghi khớp; <code>JSON.stringify</code> đổi nó thành chữ JSON để in",
                 "Tìm một bản ghi rồi đổi nó thành chữ JSON để in."), "", ""),
               (("<code>db.tk.countDocuments({\"gd.loai\": \"rut\"})</code>",
                 "đếm bản ghi khớp điều kiện; <code>\"gd.loai\"</code>: đi vào trường lồng, tức trường <code>loai</code> của các phần tử trong <code>gd</code>",
                 "Đếm bản ghi khớp; tên có dấu chấm đi vào trường lồng."), "", "")], introduces=["bnx_mongosh"]),
        st("""<p><b>Bước 1. Mô hình dữ liệu.</b> Hệ quan hệ tách thông tin thành các bảng và nối bằng <b>khoá ngoại</b>: dữ liệu không lặp, ràng buộc chặt, nhưng đọc nhiều bảng phải nối. Bản ghi JSON chứa luôn danh sách con: đọc một lần, nhưng cùng dữ liệu có thể lặp ở nhiều bản ghi.</p>"""
           + _mg_show("db.tk.insertMany", 5, title="Bản ghi JSON lồng nhau (trích từ mã chạy thật)"),
           """Bước một là mô hình dữ liệu: hệ quan hệ tách thông tin thành các bảng nối bằng khoá ngoại, nên dữ liệu không lặp, ràng buộc chặt, nhưng đọc nhiều bảng phải nối. Bản ghi JSON chứa luôn danh sách con, đọc một lần là đủ, đổi lại dữ liệu có thể lặp.""", focus=[[1, 2], 3],
           clear=True),
        jstep([(("<code>for n in 1000 100000 1000000; do … done</code>",
                 "vòng lặp của vỏ lệnh: <code>n</code> lần lượt là ba giá trị; <code>$n</code> là giá trị hiện tại; các dòng giữa <code>do</code> và <code>done</code> chạy mỗi lần",
                 "Vòng lặp cho biến nhận ba cỡ bảng lần lượt."), "", ""),
               (("<code>create table t$n (id int primary key, so text)</code>",
                 "tạo bảng: <code>id int primary key</code> là cột số nguyên làm <b>khoá chính</b> (mỗi dòng một giá trị riêng); <code>so text</code> là cột chữ",
                 "Tạo bảng có cột số nguyên làm khoá chính, nên mỗi dòng một giá trị riêng, và một cột chữ."), "", ""),
               (("<code>insert into t$n select g, 'K'||g from generate_series(1,$n) g</code>",
                 "chèn kết quả của câu <code>select</code>: mỗi số <code>g</code> thành một dòng; <code>'K'||g</code> nối chữ K với số, ra <code>K1</code>, <code>K2</code>…",
                 "Chèn từng số thành một dòng, hai gạch đứng nối chữ cái với số."), "", ""),
               (("<code>where so = 'K7'</code>, <code>create index on t$n(so)</code>",
                 "<code>where</code> chỉ giữ dòng có cột <code>so</code> bằng <code>K7</code>; <code>create index on t(so)</code> tạo chỉ mục trên cột <code>so</code>",
                 "Điều kiện giữ dòng cần tìm, lệnh tạo chỉ mục lập danh mục tra nhanh."), "", "")]),
        st("""<p><b>Bước 2. Chỉ mục.</b> Muốn tìm một giá trị mà không đọc cả bảng, ta tạo chỉ mục trên cột đó. Câu lệnh <code>EXPLAIN</code> đặt trước truy vấn bắt hệ <b>in kế hoạch</b>: sẽ đọc bảng cách nào, <code>Seq Scan</code> hay <code>Index Scan</code>.</p>"""
           + SH_PG.show_from("for n in 1000", 11, title="ChayPg (trích): với mỗi cỡ bảng, xem kế hoạch trước và sau khi tạo chỉ mục"),
           """Bước hai là chỉ mục: muốn tìm một giá trị mà không đọc cả bảng, nên ta tạo chỉ mục trên cột đó. Lệnh xem kế hoạch bắt hệ in ra cách nó sẽ đọc bảng, với ba cỡ bảng, trước và sau khi tạo chỉ mục.""",
           clear=True),
        jstep([(("<code>begin; … commit;</code>",
                 "<code>begin</code> mở một <b>giao dịch</b>: các lệnh sau thành một khối; <code>commit</code> chốt khối; khoá được giữ tới lúc chốt",
                 "Mở giao dịch, nên các lệnh sau thành một khối; chốt khối thì khoá mới nhả."), "", ""),
               (("<code>select 1 from tk where id = 1 for update;</code>",
                 "chọn dòng <code>id = 1</code> và <b>khoá</b> nó; số <code>1</code> chỉ là giá trị bỏ đi, ta cần khoá chứ không cần dữ liệu",
                 "Chọn dòng cần giữ và khoá nó, số một chỉ là giá trị bỏ đi."), "", "")]),
        st("""<p><b>Bước 3. Hai người cùng sửa một dòng.</b> Ở hệ quan hệ, người thứ nhất giữ <b>khoá dòng</b> (<code>FOR UPDATE</code>). Người thứ hai có hai lựa chọn: chờ, hoặc <b>không chờ</b> (<code>NOWAIT</code>) và nhận lỗi ngay. Mỗi hệ báo lỗi bằng mã riêng, nên ứng dụng phải bắt đúng mã của hệ mình dùng.</p>"""
           + X_ASQL.show(title="Phiên A của PostgreSQL: giữ khoá một dòng trong 30 giây"),
           """Bước ba là hai người cùng sửa một dòng: người thứ nhất giữ khoá dòng, người thứ hai chờ hoặc không chờ và nhận lỗi ngay. Mỗi hệ báo lỗi bằng mã riêng, nên ứng dụng phải bắt đúng mã của hệ mình dùng.""", focus=[1, 2],
           clear=True),
        st("""<p><b>Bước 4. Cập nhật có điều kiện.</b> Ở cơ sở dữ liệu lưu bản ghi JSON, ghi trên một bản ghi là <b>nguyên tử</b>. Nên thay vì đọc rồi ghi, ta đưa điều kiện vào lệnh: chỉ khi <code>so_du &gt;= 600</code> thì cộng thêm −600. Hai lần rút 600 từ 1000: lần đầu khớp điều kiện, lần sau thì không.</p>"""
           + """$$1000 \\ge 600 \\Rightarrow 1000 - 600 = 400; \\qquad 400 \\ge 600 \\;\\text{sai} \\Rightarrow \\hl{\\text{từ chối}}$$
""",
           """Bước bốn là cập nhật có điều kiện: ở cơ sở dữ liệu JSON, ghi trên một bản ghi là nguyên tử. Nên thay vì đọc rồi ghi, ta đưa điều kiện vào lệnh sửa. Hai lần rút sáu trăm từ một nghìn thì lần đầu còn bốn trăm, lần sau không khớp nên bị từ chối.""", focus=[1, 1, 2],
           clear=True),
        st("""<p><b>Làm thử ở hệ quan hệ.</b> Cùng ý tưởng, một câu cập nhật có thêm điều kiện số dư:</p>
<p><code>UPDATE tk SET so_du = so_du - 600 WHERE id = 1 AND so_du &gt;= 600</code></p>
<p>Số dòng bị sửa là <b>1</b> khi còn đủ tiền, <b>0</b> khi bị từ chối.</p>""",
           """Hệ quan hệ cũng viết được kiểu này, bằng một câu cập nhật có thêm điều kiện số dư, và số dòng bị sửa bằng không nghĩa là bị từ chối.""", clear=True),
        st("""<p><b>Bước 5. Chọn.</b> Không có hệ tốt nhất; có hệ hợp với yêu cầu. Đọc theo từng tiêu chí:</p>"""
           + table(["yêu cầu", "nghiêng về", "vì sao (điều đo hoặc đã thấy ở bài)"],
                   [["sổ tiền: nhiều bảng, nhiều bên cùng ghi, phải kiểm toán", "hệ quan hệ", "khoá ngoại, giao dịch nhiều bảng, khoá dòng báo lỗi rõ"],
                    ["dữ liệu lồng nhau, đọc nguyên một bản ghi, ít nối", "bản ghi JSON", "đọc một lần; sửa một bản ghi nguyên tử; nhưng nhiều bản ghi cần giao dịch riêng"],
                    ["báo cáo quét nhiều dòng", "hệ quan hệ có chỉ mục, kế hoạch xem được", "tuỳ cỡ bảng mà quét tuần tự hay chỉ mục"]]),
           """Bước năm là chọn: không có hệ tốt nhất mà chỉ có hệ hợp với yêu cầu. Sổ tiền nhiều bảng, nhiều bên cùng ghi và phải kiểm toán, nên nghiêng về hệ quan hệ. Dữ liệu lồng nhau đọc nguyên một bản ghi thì nghiêng về bản ghi JSON, còn báo cáo quét nhiều dòng cần chỉ mục.""",
           focus=[[1], 1, 2], clear=True),
    ], checks=["alg.bnx_l28_withdraw(1000, [600, 600]) == ([1, 0], 400)", "alg.bnx_l28_removed(1000, True) == 0", "alg.bnx_l28_sql_update(1000, 600) == (1, 400) and alg.bnx_l28_sql_update(400, 600) == (0, 400)"])

    ex = sc("example", "example", "Ví dụ chạy thật trên năm hệ, từng phép tính", [
        st(SH_PG.out_html("""phien ban: 17.12
1000 dong, khong chi muc:
Seq Scan on t1000 (actual rows=1 loops=1)
  Rows Removed by Filter: 999
1000 dong, co chi muc:
Index Scan using t1000_so_idx on t1000 (actual rows=1 loops=1)""", "PostgreSQL 17 chạy trong Docker: hộp chương trình đóng sẵn gọi là ảnh (ảnh chính thức, ghim băm)")
           + """$$① \\; 1000 \\text{ dòng, không chỉ mục: loại } \\hl{999}; \\quad \\text{có chỉ mục: loại } \\hlg{0}$$""",
           """Ta chạy thật bằng Docker, công cụ chạy chương trình trong một hộp đóng sẵn gọi là ảnh, mỗi lần một ảnh. Phép tính thứ nhất là PostgreSQL với bảng một nghìn dòng: không chỉ mục thì quét tuần tự, loại chín trăm chín mươi chín dòng. Có chỉ mục thì không loại dòng nào.""", focus=[1, 2, 3],
           clear=True),
        st(SH_PG.out_html("""100000 dong, khong chi muc:
Seq Scan on t100000 (actual rows=1 loops=1)
  Rows Removed by Filter: 99999
1000000 dong, khong chi muc:
Seq Scan on t1000000 (actual rows=1 loops=1)
  Rows Removed by Filter: 999999
1000000 dong, co chi muc:
Index Scan using t1000000_so_idx on t1000000 (actual rows=1 loops=1)""", "Cùng truy vấn ở 10⁵ và 10⁶ dòng")
           + """$$② \\; 10^3 \\to 10^5 \\to 10^6 \\text{ dòng: loại } 999 \\to 99\\,999 \\to 999\\,999; \\; \\text{có chỉ mục luôn } \\hlg{0}$$""",
           """Phép tính thứ hai chạy cùng truy vấn ở các cỡ bảng lớn hơn. Số dòng bị loại tăng thẳng theo cỡ bảng, còn quét theo chỉ mục vẫn không loại dòng nào.""",
           clear=True),
        jstep([(("<code>docker exec -d $C psql -U postgres -q -o /dev/null -f /a.sql</code>",
                 "<code>-U postgres</code> đăng nhập người dùng postgres; <code>-o /dev/null</code> bỏ kết quả in ra; <code>-f</code> chạy các câu SQL trong tệp",
                 "Chạy tệp SQL nền, bỏ kết quả in ra."), "", ""),
               (("<code>until docker exec $C test -f /tmp/a.ok; do sleep 0.5; done</code>",
                 "<code>until</code>: lặp tới khi lệnh thành công; <code>test -f</code> hỏi tệp có tồn tại không; <code>sleep 0.5</code> nghỉ nửa giây giữa hai lần hỏi",
                 "Cứ nửa giây hỏi một lần tới khi tệp tín hiệu xuất hiện."), "", ""),
               (("<code>… 2&gt;&amp;1 | head -1</code>",
                 "<code>2&gt;&amp;1</code> gộp thông báo lỗi vào đầu ra; <code>head -1</code> giữ dòng đầu tiên",
                 "Gộp lỗi vào đầu ra, giữ dòng đầu tiên."), "", ""),
               (("<code>docker rm -f $C &gt;/dev/null 2&gt;&amp;1</code>",
                 "xoá hộp (<code>-f</code>: kể cả khi đang chạy); <code>&gt;/dev/null 2&gt;&amp;1</code> bỏ mọi chữ in ra",
                 "Xoá hộp kể cả khi đang chạy, bỏ mọi chữ in ra."), "", "")]),
        st(SH_PG.show_from("docker cp a.sql", 5, title="Phiên B của PostgreSQL: chờ phiên A giữ khoá, rồi xin khoá không chờ") + SH_PG.out_html("""ERROR:  could not obtain lock on row in relation "tk\"""", "PostgreSQL")
           + """$$③ \\; \\text{PostgreSQL: } \\hl{\\text{báo lỗi ngay}} \\text{ thay vì chờ}$$""",
           """Phép tính thứ ba là khoá dòng không chờ: phiên A giữ khoá, mã chờ tới khi chắc A đã giữ. Phiên B xin khoá không chờ, và PostgreSQL báo lỗi ngay.""", focus=[1, [3, 4]],
           clear=True),
        st(PY_KHOA.show_from("a = threading.Thread", 12, title="SoSanhKhoa.py (trích): phiên A giữ khoá 9 giây trên Oracle, phiên B xin không chờ"),
           """Phép tính thứ tư làm việc ấy trên hai hệ có sẵn của khoá: một nhánh chạy song song giữ khoá chín giây, nhánh chính đợi năm giây rồi xin khoá không chờ.""",
           clear=True),
        st(PY_KHOA.show_from('xin = """', 4, title="SoSanhKhoa.py (trích): phiên B của SQL Server xin khoá bằng câu lệnh riêng của nó")
           + """<div class="box key">SQL Server <b>không có</b> <code>FOR UPDATE NOWAIT</code>: viết như Oracle thì báo <code>Msg 1003</code> (<code>FOR UPDATE</code> chỉ dùng cho con trỏ). Cách tương đương: <code>SET LOCK_TIMEOUT 0</code> cộng <code>WITH (UPDLOCK, ROWLOCK)</code>.</div>""",
           """Hệ có sẵn thứ hai không có câu xin khoá kiểu Oracle: viết thế thì báo mã lỗi một nghìn không trăm lẻ ba. Cách tương đương là đặt thời gian chờ khoá bằng không rồi xin khoá cập nhật mức dòng.""",
           clear=True),
        jstep([(("<code>docker exec -d $C sh -c \"mysql -uroot -pbnx_pass bnx &lt; /mysqla.sql &gt; /dev/null 2&gt;&amp;1\"</code>",
                 "<code>sh -c \"…\"</code> chạy chuỗi trong nháy như một lệnh vỏ ngay trong hộp, vì dấu <code>&lt;</code> và <code>&gt;</code> cần vỏ xử lý; <code>-uroot</code>: người dùng; <code>-p…</code>: mật khẩu; <code>bnx</code>: tên cơ sở dữ liệu; <code>&lt; tệp</code>: lấy tệp làm đầu vào",
                 "Chạy lệnh trong vỏ của hộp, lấy tệp SQL làm đầu vào."), "", ""),
               (("<code>wait_lock</code>",
                 "hàm của mã chạy thật: hỏi MySQL liên tục tới khi có khoá bản ghi, tức phiên A đã giữ khoá",
                 "Hàm này hỏi tới khi có khoá bản ghi, nghĩa là phiên A đã giữ khoá."), "", ""),
               (("<code>q \"select … for update nowait\" | head -1</code>",
                 "<code>q</code>: hàm của mã chạy thật, chạy một câu SQL trong hộp; <code>nowait</code>: xin khoá không chờ",
                 "Hàm này chạy một câu truy vấn trong hộp, xin khoá không chờ."), "", "")]),
        st(SH_MY.show_from("docker cp mysqla.sql", 5, title="ChayMy (trích): phiên A của MySQL giữ khoá 30 giây; wait_lock đợi A giữ khoá rồi B xin không chờ"),
           """Với hệ quan hệ cuối ta làm cùng cách: phiên A chạy nền giữ khoá dòng ba mươi giây, mã chờ tới khi A đã giữ, rồi phiên B xin khoá không chờ.""",
           clear=True),
        st(PY_KHOA.out_html() + SH_MY.out_html("""phien ban: 8.4.13
ERROR 3572 (HY000) at line 1: Statement aborted because lock(s) … NOWAIT is set.""", "MySQL 8.4.13")
           + """$$④ \\; \\text{Oracle: ORA-00054}; \\;\\; \\text{SQL Server: Msg 1222}; \\;\\; \\text{MySQL: ERROR 3572}$$""",
           """Kết quả thật: Oracle báo mã bắt đầu bằng chữ O R A. Hệ thứ hai báo thông báo số một nghìn hai trăm hai mươi hai vì hết hạn chờ khoá. Hệ thứ ba báo lỗi ba nghìn năm trăm bảy mươi hai vì không lấy được khoá ngay.""",
           clear=True),
        st(table(["hệ", "báo gì khi xin khoá dòng không chờ (nguyên văn máy in)"],
                 [["PostgreSQL 17", "ERROR: could not obtain lock on row in relation &quot;tk&quot;"],
                  ["MySQL 8.4", "ERROR 3572 (HY000): Statement aborted because lock(s) could not be acquired immediately and NOWAIT is set."],
                  ["Oracle 26ai", "ORA-00054: Failed to acquire a lock"],
                  ["SQL Server 2022", "Msg 1222: Lock request time out period exceeded."]]),
           """Bảng này đặt bốn hệ cạnh nhau, mỗi hệ một mã lỗi, nên ứng dụng phải bắt lỗi theo mã chứ đừng theo chữ.""",
           clear=True),
        jstep([(("<code>var rut = () =&gt; db.tk.updateOne(…).modifiedCount;</code>",
                 "<code>var</code> khai biến; <code>() =&gt; …</code> là hàm ngắn không tham số: gọi <code>rut()</code> thì chạy phần sau mũi tên; <code>updateOne</code> sửa một bản ghi khớp; <code>modifiedCount</code> là số bản ghi đã sửa, 1 hoặc 0",
                 "Hàm ngắn không tham số: gọi nó thì sửa một bản ghi khớp và trả số bản ghi đã sửa."), "", ""),
               (("<code>print(\"rut 600 lan 1: \" + rut());</code>",
                 "gọi hàm rồi nối kết quả vào chuỗi để in",
                 "Gọi hàm rồi nối kết quả vào chuỗi để in."), "", ""),
               (("<code>db.tk.findOne({_id: \"001\"}).so_du</code>",
                 "lấy bản ghi rồi đọc trường <code>so_du</code> bằng dấu chấm",
                 "Lấy bản ghi rồi đọc trường số dư."), "", "")]),
        st(_mg_show("var rut", 4, title="Cập nhật có điều kiện, gõ trong mongosh là dòng lệnh của MongoDB (mã chạy thật)") + SH_MG.out_html("""rut 600 lan 1: 1
rut 600 lan 2: 0
so du con lai: 400""", "MongoDB 8")
           + """$$⑤ \\; 1000 \\to 400; \\;\\; \\text{lần 2: } \\hl{0} \\text{ bản ghi bị sửa}$$""",
           """Phép tính thứ năm là cập nhật có điều kiện: chỉ trừ khi số dư còn từ sáu trăm trở lên. Lần thứ nhất sửa một bản ghi, còn bốn trăm, lần thứ hai không bản ghi nào khớp nên không sửa gì.""", focus=[1, 4],
           clear=True),
    ], checks=["[alg.bnx_l28_removed(n, False) for n in (1000, 100000, 1000000)] == [999, 99999, 999999]", "alg.bnx_l28_withdraw(1000, [600, 600]) == ([1, 0], 400)"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: rút tiền có điều kiện so với đọc rồi ghi", [
        jstep([(("<code>tk = {\"so_du\": 1000}</code>, <code>tk[\"so_du\"] -= so</code>",
                 "từ điển: <code>tk[\"so_du\"]</code> là giá trị của khoá <code>so_du</code>; <code>-=</code> trừ bớt một lượng khỏi giá trị đó",
                 "Từ điển giữ số dư dưới một khoá; dấu trừ bằng trừ bớt."), "", ""),
               (("<code>def rut_co_dieu_kien(so): … return 1</code>",
                 "khai hàm; các dòng thụt vào là thân; <code>return</code> trả giá trị về chỗ gọi và dừng hàm",
                 "Khai hàm, lệnh trả về đưa giá trị về chỗ gọi."), "", ""),
               (("<code>doc_a = doc_b = 1000</code>",
                 "gán cùng một giá trị cho cả hai tên: hai bên cùng đọc số dư trước khi ai ghi",
                 "Gán cùng giá trị cho hai tên, nên hai bên cùng đọc số dư trước khi ai ghi."), "", ""),
               (("<code>print(\"con\", so_du)</code>, <code>#</code>",
                 "in các giá trị cách nhau một dấu cách; từ <code>#</code> tới hết dòng là ghi chú, máy bỏ qua",
                 "Lệnh in các giá trị cách nhau một dấu cách."), "", "")]),
        st(PY_RUT.show(lines=(1, 15), title="MÔ PHỎNG bằng Python, không phải tranh chấp thật — RutTien.py: cùng số dư 1000, hai lần rút 600"),
           """Đây là mô phỏng chứ không phải tranh chấp thật. Hàm rút có điều kiện kiểm và trừ trong một bước, nên lần thứ hai bị từ chối. Cách sai thì hai bên cùng đọc một nghìn rồi mỗi bên ghi một nghìn trừ sáu trăm, nên bên ghi sau đè lên bên trước.""",
           clear=True),
        st("""<div class="box warn"><b>MÔ PHỎNG</b> bằng Python: hai biến gán tay, <b>không phải</b> hai phiên tranh chấp thật trên cơ sở dữ liệu.</div>"""
           + PY_RUT.out_html(title="Kết quả mô phỏng") + table(["cách", "số dư cuối", "tiền đã chi ra", "tiền thực sự bị trừ"],
                                    [["cập nhật có điều kiện", "400", "600", "600"], ["đọc rồi ghi", "400", "1200", "600"]]),
           """Cả hai cách đều ra số dư bốn trăm. Khác biệt ở tiền đã chi: có điều kiện chi sáu trăm, còn đọc rồi ghi chi một nghìn hai trăm nhưng chỉ trừ sáu trăm, nên ngân hàng mất sáu trăm.""",
           focus=[1, 3], clear=True),
    ], checks=["alg.bnx_l28_withdraw(1000, [600, 600]) == ([1, 0], 400)", "alg.bnx_l28_lost_update(1000, 600, 600) == (400, 600)"])

    quymo = sc("quymo", "example", "Khi bảng lớn dần: số dòng bị đọc và bị loại", [
        st(table(["số dòng của bảng", "quét tuần tự: dòng bị loại", "quét theo chỉ mục: dòng bị loại", "nguồn số"],
                 [["1 000 (×1)", "999", "0", "đo thật PostgreSQL 17"],
                  ["100 000 (×100)", "99 999", "0", "đo thật PostgreSQL 17"],
                  ["1 000 000 (×1 000)", "999 999", "0", "đo thật PostgreSQL 17"],
                  ["10 000 000 (×10 000)", "9 999 999", "0", "suy ra: n − 1 (công thức), không chạy ở bài"]]),
           """Bảng này cho thấy vấn đề đổi thế nào khi bảng lớn dần, ba dòng đầu là số đo thật. Quét tuần tự loại gần một nghìn dòng ở một nghìn dòng, gần một trăm nghìn ở một trăm nghìn dòng, gần một triệu ở một triệu dòng. Dòng cuối suy ra từ công thức, còn quét theo chỉ mục luôn loại không dòng nào.""",
           focus=[0, "1.2", ["1.3", "1.4"], "1.5"]),
        st(table(["cách", "được", "mất", "chọn khi"],
                 [["quét tuần tự", "không cần chỉ mục; ghi nhanh", "chi phí đọc tăng theo cỡ bảng", "bảng nhỏ, hoặc truy vấn đọc phần lớn bảng"],
                  ["chỉ mục", "đọc một giá trị gần như không đổi theo cỡ bảng", "tốn chỗ; mỗi lần ghi phải cập nhật chỉ mục", "tìm ít dòng trong bảng lớn"],
                  ["tách bảng báo cáo / lập bản tóm tắt", "báo cáo nặng không tranh với giao dịch", "dữ liệu tóm tắt có thể cũ; thêm việc vận hành", "báo cáo quét nhiều dòng trên bảng giao dịch"]]),
           """Bảng thứ hai cho thấy phải chọn gì. Quét tuần tự ghi nhanh, nhưng chi phí đọc tăng theo cỡ bảng. Chỉ mục giữ chi phí đọc gần như không đổi, đổi lại tốn chỗ và làm mỗi lần ghi chậm hơn.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["[alg.bnx_l28_removed(n, False) for n in (1000, 100000, 1000000, 10000000)] == [999, 99999, 999999, 9999999]", "1000000 // 1000 == 1000 and 10000000 // 1000 == 10000"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người đã đi làm, lúc mới dựng).</b> Chuyển mã từ hệ này sang hệ khác mà <b class="red">chỉ đổi câu nối</b>. Cùng việc &laquo;xin khoá không chờ&raquo; mà mỗi hệ một cú pháp và một mã lỗi: ứng dụng bắt lỗi theo mã của hệ cũ sẽ không bắt được lỗi của hệ mới.
Cách chữa: gom việc bắt lỗi khoá vào một chỗ, và có ca kiểm cho từng hệ.</div>""",
           """Lỗi thứ nhất, lúc mới dựng: chuyển mã sang hệ khác mà chỉ đổi câu nối. Cùng việc xin khoá không chờ mà mỗi hệ một cú pháp và mã lỗi, nên bắt lỗi theo mã hệ cũ không bắt được lỗi hệ mới. Cách chữa là gom việc bắt lỗi khoá vào một chỗ, mỗi hệ một ca kiểm.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc tải tăng).</b> Quên chỉ mục: chạy tốt ở 10³ dòng, nhưng ở 10⁶ dòng mỗi truy vấn loại 999 999 dòng. Hoặc ngược lại, <b class="red">lập chỉ mục cho mọi cột</b> làm mỗi lần ghi chậm đi và tốn chỗ.
Chữa: đọc kế hoạch (<code>EXPLAIN</code>) của các truy vấn hay chạy, chỉ lập chỉ mục cho cột được tìm nhiều.</div>"""
           + SH_PG.out_html("""1000000 dong, khong chi muc:
Seq Scan on t1000000 (actual rows=1 loops=1)
  Rows Removed by Filter: 999999""", "Đã đo ở phần ví dụ"),
           """Lỗi thứ hai, khi tải tăng: quên chỉ mục, nên chạy tốt ở một nghìn dòng nhưng ở một triệu dòng mỗi truy vấn loại gần một triệu dòng. Lập chỉ mục cho mọi cột thì làm mỗi lần ghi chậm đi và tốn chỗ. Cách chữa là đọc kế hoạch và chỉ lập chỉ mục cho cột được tìm nhiều.""", focus=[1, 2, 3], clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc vận hành lâu dài).</b> Dùng <b class="red">đọc rồi ghi không điều kiện</b> cho số dư vì &laquo;ít khi hai người cùng sửa&raquo;. Mô phỏng: hai lần rút 600 từ 1000 chi ra 1200 mà chỉ trừ 600.
Hiếm gặp không có nghĩa là không gặp; sau nhiều tháng, đến một ngày tải cao lỗi xảy ra. Cách chữa: cập nhật có điều kiện (ở hệ quan hệ: <code>UPDATE … WHERE so_du &gt;= số rút</code>), hoặc khoá dòng rồi mới đọc.</div>""",
           """Lỗi thứ ba, khi vận hành lâu dài: đọc rồi ghi không điều kiện cho số dư vì ít khi hai người cùng sửa. Mô phỏng cho thấy hai lần rút sáu trăm từ một nghìn chi một nghìn hai trăm mà chỉ trừ sáu trăm. Cách chữa là thêm điều kiện số dư vào câu cập nhật, hoặc khoá dòng rồi mới đọc.""", clear=True),
    ], checks=["alg.bnx_l28_lost_update(1000, 600, 600) == (400, 600)", "alg.bnx_l28_removed(1000000, False) == 999999"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Bảng có 250 000 dòng, tìm một giá trị duy nhất. Quét tuần tự loại bao nhiêu dòng? Có chỉ mục loại bao nhiêu? Bảng có 2 500 000 dòng thì sao?"],
                  ["2", "Số dư 900. Ba lần rút 400, 400, 400 theo cách cập nhật có điều kiện: mỗi lần được (1) hay bị từ chối (0), và số dư cuối?"],
                  ["3", "Quyết định (số minh hoạ): dữ liệu hồ sơ khách gồm thông tin cá nhân, danh sách tài khoản, danh sách người thụ hưởng; mỗi lần mở hồ sơ cần đọc đủ ba phần; cập nhật hiếm, nhưng mỗi thay đổi phải ghi vết kiểm toán. Chọn: hệ quan hệ, bản ghi JSON, hay lai? Vì sao?"]]),
           """Đến lượt bạn, ba câu để làm ra giấy. Số dòng bị loại của bảng hai trăm năm mươi nghìn dòng, số dư cuối sau ba lần rút bốn trăm từ chín trăm, và chọn hệ cho hồ sơ khách cần ghi vết kiểm toán. Hãy dừng lại làm ra giấy rồi xem đáp án.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=30),
        st("""<p>Câu 1: loại n − 1 dòng khi quét tuần tự, 0 khi có chỉ mục.</p>
$$250\\,000 - 1 = \\hlg{249\\,999}; \\quad \\text{chỉ mục: } \\hlg{0}; \\quad 2\\,500\\,000 - 1 = \\hlg{2\\,499\\,999}$$""",
           """Đáp án câu một, quét tuần tự loại hai trăm bốn mươi chín nghìn chín trăm chín mươi chín dòng, có chỉ mục thì không loại dòng nào. Bảng lớn hơn mười lần loại hai triệu bốn trăm chín mươi chín nghìn chín trăm chín mươi chín dòng."""),
        st("""<p>Câu 2: lần nào còn đủ tiền thì trừ và được, không đủ thì từ chối.</p>
$$900 \\ge 400 \\Rightarrow 500\\;(1); \\;\\; 500 \\ge 400 \\Rightarrow 100\\;(1); \\;\\; 100 \\ge 400 \\text{ sai} \\Rightarrow \\hlg{0}; \\;\\; \\text{còn } \\hlg{100}$$""",
           """Đáp án câu hai, lần một chín trăm đủ bốn trăm nên được, còn năm trăm. Lần hai năm trăm vẫn đủ nên được, còn một trăm. Lần ba một trăm không đủ nên bị từ chối, số dư cuối là một trăm."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["hệ quan hệ", "ghi vết kiểm toán, ràng buộc chặt, giao dịch nhiều bảng", "mở hồ sơ phải nối ba bảng"],
                  ["bản ghi JSON", "mở hồ sơ đọc một lần", "vết kiểm toán và ràng buộc tự lo; thay đổi nhiều bản ghi cần giao dịch riêng"],
                  ["lai: hệ quan hệ làm nguồn sự thật có vết kiểm toán, bản JSON dựng sẵn để mở hồ sơ nhanh", "vừa chặt vừa nhanh", "hai nơi phải đồng bộ; bản JSON có thể cũ"]]),
           """Đáp án câu ba: hệ quan hệ ghi vết kiểm toán và ràng buộc chặt, đổi lại phải nối ba bảng. Bản ghi JSON mở hồ sơ đọc một lần, đổi lại vết kiểm toán phải tự lo. Cách lai phải đồng bộ hai nơi. Hợp lý là hệ quan hệ, vì kiểm toán nặng và cập nhật hiếm."""),
    ], checks=["alg.bnx_l28_removed(250000, False) == 249999 and alg.bnx_l28_removed(2500000, False) == 2499999", "alg.bnx_l28_withdraw(900, [400, 400, 400]) == ([1, 1, 0], 100)"])

    lab_pr = practice_scene(sc, "Tự làm: rút tiền có điều kiện và lỗi đọc rồi ghi", practice_steps(
        st, "BNX", "L28",
        """<p><b>Đề</b>: tài khoản có số dư <b>700</b>. Viết <code>mau.py</code>:</p>
<ol><li>hàm <code>rut_co_dieu_kien(tk, so)</code> trừ khi còn đủ, trả 1 hoặc 0; gọi với 500, 500, 200; in <code>co dieu kien: &lt;ba số cách nhau bằng dấu cách&gt; con &lt;số dư&gt;</code></li>
<li>mô phỏng đọc rồi ghi: A và B cùng đọc 700, mỗi bên ghi 700 − 500; in số dư cuối và số tiền mất</li></ol>
<p class="note">Số liệu khác ví dụ trong bài; định dạng hai dòng in nằm trong <code>de.md</code>.</p>""",
        """Đến phần bạn tự làm: viết hàm rút có điều kiện cho tài khoản bảy trăm, chạy ba lần rút năm trăm, năm trăm, hai trăm rồi in kết quả. Rồi mô phỏng lỗi đọc rồi ghi: hai bên cùng đọc bảy trăm, mỗi bên ghi bảy trăm trừ năm trăm, và in số dư cuối với số tiền mất. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> hàm rút: nếu <code>tk["so_du"] &gt;= so</code> thì trừ rồi trả 1, ngược lại trả 0. Mô phỏng sai: đặt <code>doc_a = doc_b = 700</code> trước, rồi gán <code>so_du = doc_a - 500</code> và <code>so_du = doc_b - 500</code>. Số mất = tổng đã chi trừ số thật bị trừ.
Lời giải đầy đủ ở <code>labs/BNX/L28/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, hàm rút kiểm số dư trước, đủ thì trừ rồi trả một, không đủ thì trả không. Với mô phỏng sai, đặt hai biến đọc cùng bằng bảy trăm rồi gán số dư bằng mỗi biến trừ năm trăm. Lời giải chỉ mở sau khi đã tự thử.""", pause=150), "BNX", "L28")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("mô hình dữ liệu theo yêu cầu", "chỉ mục + đọc kế hoạch", "khoá dòng, mã lỗi mỗi hệ một kiểu", "cập nhật có điều kiện", "chọn theo yêu cầu, đo trước"),
           """Mô hình dữ liệu chọn theo yêu cầu. Chỉ mục và lệnh xem kế hoạch quyết định truy vấn có gãy khi bảng lớn. Khoá dòng mỗi hệ báo lỗi một kiểu, còn cập nhật có điều kiện giữ số dư an toàn."""),
        st("""<div class='box key'><b>Tư duy:</b> không hỏi &laquo;hệ nào tốt nhất&raquo;, hỏi &laquo;<b>yêu cầu của tôi</b> là gì&raquo; rồi <b>đo</b>: đọc kế hoạch, thử khoá, thử rút hai lần. Cùng một việc, mỗi hệ một cách; điều chung là phải kiểm và trừ tiền trong <b>một bước nguyên tử</b>.</div>""",
           """Đừng hỏi hệ nào tốt nhất, hãy hỏi yêu cầu của mình rồi đo. Điều chung là phải kiểm và trừ tiền trong một bước nguyên tử."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["MongoDB, MySQL, PostgreSQL so với Oracle, SQL Server: khác gì?", "mô hình (quan hệ so với bản ghi JSON), kế hoạch và chỉ mục xem được bằng EXPLAIN/explain, khoá dòng và mã lỗi mỗi hệ một kiểu; chạy thật: 4 hệ quan hệ từ chối ngay, bản ghi JSON dùng cập nhật có điều kiện (hệ quan hệ cũng dùng được)"],
                  ["Khi nào chọn bản ghi JSON?", "dữ liệu lồng nhau đọc nguyên một bản ghi, ít nối, sửa trên một bản ghi; sổ tiền nhiều bảng và kiểm toán nghiêng về quan hệ"],
                  ["Truy vấn chậm bạn làm gì?", "đọc kế hoạch, thấy quét tuần tự trên bảng lớn thì lập chỉ mục đúng cột, đo lại; chỉ số dòng bị loại n − 1 cho biết quy mô"]]),
           """Người phỏng vấn thường hỏi ba câu: mô hình quan hệ khác bản ghi JSON thế nào, khi nào chọn bản ghi JSON, và truy vấn chậm thì làm gì.""", clear=True),
        st("""<p>Bài sau: <b>lưu sự kiện thay vì lưu số dư</b>, cùng phát lại, bản chụp và sự kiện bù.</p>""",
           """Ở bài hai mươi chín, ta tìm hiểu cách lưu sự kiện thay vì lưu số dư, cùng với phát lại, bản chụp và sự kiện bù.""",
           forward_ref=True),
    ], checks=["alg.bnx_l28_lost_update(1000, 600, 600) == (400, 600)"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L28", "co_so_du_lieu_so_sanh",
                  "Bài 28 — PostgreSQL, MongoDB, MySQL so với Oracle và SQL Server: mô hình, chỉ mục và khoá",
                  "curriculum/bnx.yaml L28; audit/bnx/verify_bnx.py L28; audit/bnx/sources_l28.md: hướng dẫn PostgreSQL 17 (SELECT: khoá dòng), "
                  "hướng dẫn MongoDB (Atomicity and Transactions) (đọc 2026-11-13); chạy thật bằng ảnh Docker chính thức PostgreSQL 17.12, MongoDB 8.3.17, MySQL 8.4.13 (ghim băm) và Oracle/SQL Server trong container của khoá",
                  ["Đọc kế hoạch của PostgreSQL và nhận ra quét tuần tự khác quét theo chỉ mục",
                   "So sánh lỗi khi xin khoá dòng không chờ ở PostgreSQL, MySQL, Oracle và SQL Server",
                   "Đọc một bản ghi JSON lồng nhau và hỏi theo trường lồng",
                   "Giải thích vì sao cập nhật có điều kiện trên một bản ghi ngăn rút quá số dư",
                   "Chọn loại cơ sở dữ liệu cho sổ tiền, dữ liệu lồng nhau và báo cáo theo yêu cầu",
                   "Đếm số dòng bị loại khi không có chỉ mục ở 10³, 10⁵ và 10⁶ dòng",
                   "Viết hàm rút tiền có điều kiện và tái hiện lỗi đọc rồi ghi"],
                  scenes, assumes=["bnx_nguyen_tu"],
                  covers=[(1, "example"), (2, "example"), (3, "formula"), (4, "check"), (5, "formula"), (6, "quymo"), (7, "practice")])
