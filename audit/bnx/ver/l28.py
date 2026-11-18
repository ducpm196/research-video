"""Kiểm độc lập BNX L28 (PostgreSQL, MongoDB, MySQL so với Oracle và SQL Server). Đường khác với tools/checklib_bnx/l28.py:
- CHẠY LẠI THẬT (không đệm) mọi chương trình trên màn hình: ảnh Docker chính thức postgres:17-alpine, mongo:8, mysql:8.4 (ghim băm; mỗi lần một container, tự gỡ),
  Oracle và SQL Server trong container có sẵn của khoá (dbrun, bảng bnx_l28_tk / cơ sở dữ liệu bnx_l28 riêng, tự dọn);
- số dòng bị loại đọc từ kế hoạch thật của PostgreSQL ("Rows Removed by Filter") rồi đối chiếu n − 1: tính lại bằng vòng lặp đếm dòng không khớp trên dữ liệu dựng bằng Python;
- số bản ghi quét ở MongoDB đối chiếu 100 000; kết quả rút có điều kiện tính lại bằng hai cách (vòng lặp thuần và mô hình alg);
- lab chạy lại và so mong_doi.txt.
Thiếu Docker/ảnh/container → SKIP (rec None: cổng FAIL, NOT_VERIFIED), không PASS lặng lẽ."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import lib2  # noqa: E402
import l28 as src  # noqa: E402

LAB = ROOT / "labs" / "BNX" / "L28"


def vong_lap_loai(n, muc_tieu="K7"):
    """Dựng n dòng K1..Kn và đếm dòng KHÔNG khớp khi tìm một giá trị (quét tuần tự)."""
    return sum(1 for i in range(1, n + 1) if f"K{i}" != muc_tieu)


def run(rec):
    if not shutil.which("docker"):
        rec("L28", None, "thiếu docker: NOT_VERIFIED")
    else:
        ok_o = ok_m = False
        try:
            import dbrun
            ok_o, ok_m = dbrun.ready()
        except Exception as ex:
            rec("L28", None, f"không gọi được Oracle/SQL Server qua dbrun ({type(ex).__name__}): NOT_VERIFIED")
        if not (ok_o and ok_m):
            rec("L28", None, "container bnx-ora/bnx-mss chưa chạy (docker start bnx-ora bnx-mss): NOT_VERIFIED")
        else:
            lib2.verify_programs(rec, "L28")
            P = {q.name: q for q in lib2.PROGRAMS if q.lesson == "L28"}
            pg = P["ChayPg"].out
            rec("L28", pg.splitlines()[0].startswith("phien ban: 17."), "PostgreSQL chạy thật: " + pg.splitlines()[0])
            loai = {int(n): int(x) for n, x in re.findall(r"^(\d+) dong, khong chi muc:\nSeq Scan on \S+ \(actual rows=1 loops=1\)\n  Rows Removed by Filter: (\d+)$", pg, re.M)}
            rec("L28", loai == {1000: 999, 100000: 99999, 1000000: 999999}, f"dòng bị loại khi quét tuần tự: {loai}")
            rec("L28", all(loai[n] == alg.bnx_l28_removed(n, False) == vong_lap_loai(n) for n in (1000, 100000)), "n − 1: khớp mô hình và vòng lặp đếm dòng không khớp (10³, 10⁵)")
            idx = re.findall(r"co chi muc:\nIndex Scan using t(\d+)_so_idx on t\d+ \(actual rows=1 loops=1\)\n(?!  Rows Removed)", pg)
            rec("L28", sorted(map(int, idx)) == [1000, 100000, 1000000] and alg.bnx_l28_removed(1000000, True) == 0, "có chỉ mục: quét theo chỉ mục, không dòng nào bị loại, ở cả ba cỡ")
            rec("L28", pg.splitlines()[-1] == 'ERROR:  could not obtain lock on row in relation "tk"', "PostgreSQL NOWAIT: lỗi ngay")
            mg = P["ChayMg"].out.splitlines()
            rec("L28", mg[0].startswith("phien ban: 8.") and "co gd rut: 1" in mg and "khong chi muc: xem 100000 tai lieu" in mg and "co chi muc: xem 1 tai lieu" in mg, "MongoDB: bản ghi lồng nhau, truy vấn theo gd.loai, quét 100 000 / 1 bản ghi")
            rec("L28", mg[-3:] == ["rut 600 lan 1: 1", "rut 600 lan 2: 0", "so du con lai: 400"] and alg.bnx_l28_withdraw(1000, [600, 600]) == ([1, 0], 400), "MongoDB: rút có điều kiện 1, 0, còn 400 (khớp mô hình)")
            my = P["ChayMy"].out.splitlines()
            rec("L28", my[0].startswith("phien ban: 8.4") and "khong chi muc: ALL" in my and "co chi muc: ref" in my and any(l.startswith("ERROR 3572") for l in my), "MySQL: ALL → ref; NOWAIT báo ERROR 3572")
            kh = P["SoSanhKhoa"].out.splitlines()
            rec("L28", kh[0].startswith("Oracle: ORA-00054") and kh[1] == "SQL Server: Msg 1222: Lock request time out period exceeded.", "Oracle ORA-00054 và SQL Server Msg 1222 khi xin khoá không chờ")
            m1003 = dbrun.mss("CREATE TABLE #t (id INT); SELECT id FROM #t WHERE id = 1 FOR UPDATE NOWAIT;")
            rec("L28", "Msg 1003" in m1003 and "FOR UPDATE clause allowed only for DECLARE CURSOR" in m1003,
                "SQL Server thật: viết FOR UPDATE NOWAIT (kiểu Oracle) → Msg 1003 (FOR UPDATE chỉ cho con trỏ); cách đúng: SET LOCK_TIMEOUT 0 + WITH (UPDLOCK, ROWLOCK) → Msg 1222 (đã đo ở dòng trên)")
            rt = P["RutTien"].out.splitlines()
            rec("L28", rt[0] == "co dieu kien: 1 0 con 400" and rt[1].startswith("doc roi ghi: con 400") and alg.bnx_l28_lost_update(1000, 600, 600) == (400, 600), "rút có điều kiện 1 0 còn 400; đọc rồi ghi còn 400, chi 1200 chỉ trừ 600 (mất 600)")
    rec("L28", [alg.bnx_l28_removed(n, False) for n in (250000, 2500000)] == [249999, 2499999] and alg.bnx_l28_withdraw(900, [400, 400, 400]) == ([1, 1, 0], 100), "quiz: 249 999 và 2 499 999 dòng; 900 rút 400×3 → 1, 1, 0, còn 100")
    r = subprocess.run([sys.executable, "-X", "utf8", str(LAB / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8")
    rec("L28", r.returncode == 0 and r.stdout.strip() == (LAB / "mong_doi.txt").read_text(encoding="utf-8").strip(), "lab: loi_giai.py cho đúng mong_doi.txt")
    rec("L28", alg.bnx_l28_withdraw(700, [500, 500, 200]) == ([1, 0, 1], 0) and alg.bnx_l28_lost_update(700, 500, 500) == (200, 500), "lab: 1 0 1 còn 0; đọc rồi ghi còn 200, mất 500")
    # UPDATE có điều kiện ở hệ quan hệ cũng nguyên tử: sqlite thật, hai lần rút 600 từ 1000 (số dòng bị sửa 1 rồi 0)
    import sqlite3
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE tk (id INTEGER PRIMARY KEY, so_du INTEGER)")
    db.execute("INSERT INTO tk VALUES (1, 1000)")
    c1 = db.execute("UPDATE tk SET so_du = so_du - 600 WHERE id = 1 AND so_du >= 600").rowcount
    c2 = db.execute("UPDATE tk SET so_du = so_du - 600 WHERE id = 1 AND so_du >= 600").rowcount
    cuoi = db.execute("SELECT so_du FROM tk").fetchone()[0]
    rec("L28", (c1, c2, cuoi) == (1, 0, 400) and alg.bnx_l28_sql_update(1000, 600) == (1, 400) and alg.bnx_l28_sql_update(400, 600) == (0, 400), "UPDATE … WHERE so_du >= 600 ở hệ quan hệ (sqlite thật): số dòng bị sửa 1 rồi 0, còn 400")
    # bảng so bốn hệ trên màn hình: chữ của MySQL/Oracle/SQL Server là nguyên văn đầu ra thật; PostgreSQL ở ChayPg
    if "P" in locals() and all(k in P and P[k].out for k in ("ChayMy", "SoSanhKhoa", "ChayPg")):
        ban = ("ERROR 3572 (HY000) at line 1: Statement aborted because lock(s) could not be acquired immediately and NOWAIT is set.",
               "Oracle: ORA-00054: Failed to acquire a lock", "SQL Server: Msg 1222: Lock request time out period exceeded.", 'ERROR:  could not obtain lock on row in relation "tk"')
        rec("L28", ban[0] in P["ChayMy"].out and ban[1] in P["SoSanhKhoa"].out and ban[2] in P["SoSanhKhoa"].out and ban[3] in P["ChayPg"].out, "bảng so bốn hệ: chữ lỗi của MySQL/Oracle/SQL Server/PostgreSQL là nguyên văn đầu ra thật")
