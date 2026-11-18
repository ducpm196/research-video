"""Kiểm độc lập BNX L07 — chạy THẬT các hằng mã của audit/bnx/src/l07.py trên Oracle (bnx-ora, Oracle AI Database 26ai Free 23.26.3),
đọc con số và kế hoạch thực thi bằng biểu thức chính quy, đếm từng phân vùng bằng PARTITION FOR (đường khác), rồi so với alg.bnx_l07_*.
Hàng đợi, bộ nhớ cột và phân mảnh đã chuyển sang bài L38 (audit/bnx/ver/l38.py).
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402
import l07 as L  # noqa: E402


def _ints(out):
    return [int(x) for x in re.findall(r"^\s*(\d+)\s*$", out, re.M)]


def _plan(out):
    """[(thao tác PARTITION RANGE …, Pstart, Pstop)] đọc từ bảng DBMS_XPLAN."""
    return [(m.group(1), int(m.group(2)), int(m.group(3)))
            for m in re.finditer(r"PARTITION RANGE (\w+)\s*\|[^|]*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", out)]


def run(rec):
    try:
        import dbrun
        ok_o, _ = dbrun.ready()
    except Exception as ex:  # noqa: BLE001
        rec("L07", None, f"không gọi được Docker: {type(ex).__name__}")
        return
    if not ok_o:
        rec("L07", None, "container bnx-ora chưa chạy")
        return
    ora = dbrun.ora
    v = ora("SELECT banner_full FROM v$version;")
    rec("L07", "Free" in v and "23.26" in v, "Oracle: đúng bản Oracle AI Database 26ai Free 23.26 (banner thật)")

    # 1. Phân vùng: nạp, đếm dòng và phân vùng
    dates = alg.bnx_l07_load(3650)
    o = ora(L.PART_DDL + L.PART_LOAD)
    t = _ints(o)
    rec("L07", t[:1] == [len(dates)] == [365 * 10], f"Oracle: số dòng thật {t[:1]} = alg 3 650")
    rec("L07", t[1:2] == [alg.bnx_l07_partitions(dates)] == [12], f"Oracle: số phân vùng thật {t[1:2]} = alg 12 (1 khai + 11 tự tạo)")

    # 2. Đường khác: đếm thẳng từng phân vùng tháng bằng PARTITION FOR, so với số ngày của tháng × 10
    q = "".join(f"SELECT COUNT(*) FROM bnx_l07_gd PARTITION FOR (DATE '2025-{m:02d}-15');\n" for m in range(1, 13))
    per = _ints(ora(q))
    want = [alg.bnx_l07_count(dates, f"2025-{m:02d}-01", f"2025-{m + 1:02d}-01" if m < 12 else "2026-01-01") for m in range(1, 13)]
    rec("L07", per == want == [alg.bnx_l07_month_days(2025, m) * 10 for m in range(1, 13)],
        f"Oracle: đếm thẳng 12 phân vùng {per} = số ngày mỗi tháng × 10 (alg)")
    o = ora(L.PART_CHECK)
    rec("L07", _ints(o) == [310, 310] and alg.bnx_l07_count(dates, "2025-03-01", "2025-04-01") == 310,
        f"Oracle: tháng 3 lọc theo ngày và đếm trong phân vùng: {_ints(o)} = 310")

    # 3. Kế hoạch thực thi
    p = _plan(ora(L.PLAN_MONTH))
    rec("L07", p and p[0] == ("SINGLE",) + alg.bnx_l07_prune("2025-03-01", "2025-04-01") == ("SINGLE", 3, 3),
        f"Oracle: kế hoạch tháng 3 thật {p[:1]} = PARTITION RANGE SINGLE 3..3 (alg)")
    p = _plan(ora(L.PLAN_ALL))
    rec("L07", p and p[0] == ("ALL", 1, alg.bnx_l07_max_partitions()), f"Oracle: không lọc ngày {p[:1]} = PARTITION RANGE ALL 1..1048575 (1024K − 1)")
    p = _plan(ora(L.PLAN_TRUNC))
    rec("L07", p and p[0][0] == "ALL", f"Oracle: TRUNC(ngay, 'MM') → {p[:1]}: không cắt tỉa")
    qz = ("EXPLAIN PLAN FOR\nSELECT COUNT(*) FROM bnx_l07_gd\n WHERE ngay >= DATE '2025-03-15' AND ngay < DATE '2025-05-15';\n"
          "SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY(NULL, NULL, 'BASIC +PARTITION'));\n"
          "SELECT COUNT(*) FROM bnx_l07_gd WHERE ngay >= DATE '2025-03-15' AND ngay < DATE '2025-05-15';")
    o = ora(qz)
    p = _plan(o)
    rec("L07", p and p[0] == ("ITERATOR",) + alg.bnx_l07_prune("2025-03-15", "2025-05-15") == ("ITERATOR", 3, 5),
        f"Oracle (câu đố 1): kế hoạch thật {p[:1]} = PARTITION RANGE ITERATOR 3..5")
    rec("L07", _ints(o)[-1:] == [alg.bnx_l07_count(dates, "2025-03-15", "2025-05-15")] == [610], f"Oracle (câu đố 1): đếm thật {_ints(o)[-1:]} = 610")
    rec("L07", round(100 * 310 / 3650, 1) == 8.5 and round(3650 / 310, 1) == 11.8, "④ 310/3650 ≈ 8,5 %, ⑤ 3650/310 ≈ 11,8 (tính từ số đếm thật)")

    qb = """VARIABLE d1 VARCHAR2(10)
VARIABLE d2 VARCHAR2(10)
EXPLAIN PLAN FOR
SELECT COUNT(*) FROM bnx_l07_gd WHERE ngay >= TO_DATE(:d1, 'YYYY-MM-DD') AND ngay < TO_DATE(:d2, 'YYYY-MM-DD');
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY(NULL, NULL, 'BASIC +PARTITION'));"""
    o = ora(qb)
    rec("L07", re.search(r"PARTITION RANGE \w+\s*\|[^|]*\|\s*KEY\s*\|\s*KEY\s*\|", o) is not None,
        "Oracle: ngày qua biến gắn → Pstart/Pstop = KEY (chọn phân vùng lúc chạy)")
    o = ora("""ALTER TABLE bnx_l07_gd DROP PARTITION FOR (DATE '2025-01-15');
SELECT COUNT(*) FROM bnx_l07_gd;
SELECT COUNT(*) FROM user_tab_partitions WHERE table_name = 'BNX_L07_GD';""")
    rec("L07", _ints(o)[-2:] == [len(dates) - alg.bnx_l07_count(dates, "2025-01-01", "2025-02-01"), 11] == [3340, 11],
        f"Oracle: DROP PARTITION FOR tháng 1 xoá cả tháng bằng một lệnh → còn {_ints(o)[-2:]} = [3 340 dòng, 11 phân vùng]")
    ora(L.PART_DDL + L.PART_LOAD)

    # 4. JSON
    o = ora("SELECT CASE WHEN '{kenh:''app''}' IS JSON THEN 'Y' ELSE 'N' END AS l, "
            "CASE WHEN '{kenh:''app''}' IS JSON (STRICT) THEN 'Y' ELSE 'N' END AS c FROM dual;")
    rec("L07", re.search(r"^Y\s+N\s*$", o, re.M) is not None, "Oracle: IS JSON mặc định chế độ lỏng ({kenh:'app'} nhận), IS JSON (STRICT) từ chối")
    o = ora(L.JSON_DDL + L.JSON_QUERY)
    docs = {1: '{"kenh":"app","so_tien":500000}', 2: '{"kenh":"atm","so_tien":2000000}', 3: '{"kenh":"app"'}
    ok_ids, hit = alg.bnx_l07_json_ids(docs, "so_tien", 1000000)
    rows = re.findall(r"^\s*(\d+)\s+(\w+)\s*$", o, re.M)
    rec("L07", "ORA-02290: check constraint (BNX.BNX_L07_ISJ) violated" in o and 3 not in ok_ids, "Oracle: IS JSON từ chối chuỗi hỏng (alg: json.loads lỗi)")
    rec("L07", rows == [("2", "atm")] and hit == [2], f"Oracle: JSON_VALUE lọc so_tien > 1 000 000 → {rows} = alg [2]")

    # 5. Mẹo sinh dòng, mốc ngày và câu đố 2 (tháng 2: 10 ngày × 10 dòng, đọc đúng phân vùng 2)
    o = ora(L.ROWNUM_DEMO)
    rec("L07", _ints(o) == [1, 2, 3], f"Oracle: SELECT ROWNUM FROM dual CONNECT BY ROWNUM <= 3 → {_ints(o)} = [1, 2, 3]")
    qz2 = ("EXPLAIN PLAN FOR\nSELECT COUNT(*) FROM bnx_l07_gd\n WHERE ngay >= DATE '2025-02-10' AND ngay < DATE '2025-02-20';\n"
           "SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY(NULL, NULL, 'BASIC +PARTITION'));\n"
           "SELECT COUNT(*) FROM bnx_l07_gd WHERE ngay >= DATE '2025-02-10' AND ngay < DATE '2025-02-20';")
    o = ora(qz2)
    p = _plan(o)
    rec("L07", p and p[0] == ("SINGLE",) + alg.bnx_l07_prune("2025-02-10", "2025-02-20") == ("SINGLE", 2, 2),
        f"Oracle (câu đố 2): kế hoạch thật {p[:1]} = PARTITION RANGE SINGLE 2..2")
    rec("L07", _ints(o)[-1:] == [alg.bnx_l07_count(dates, "2025-02-10", "2025-02-20")] == [100], f"Oracle (câu đố 2): đếm thật {_ints(o)[-1:]} = 100")

    # 6. IS JSON lỏng / chặt trên ba chuỗi (lỗi 2), và bỏ phân vùng tự chốt (lỗi 3)
    cases = ["{\"a\":1}", "{a:1}", "{\"a\":1"]
    q = "".join(f"SELECT CASE WHEN '{c}' IS JSON THEN 'L:Y' ELSE 'L:N' END || CASE WHEN '{c}' IS JSON (STRICT) THEN 'S:Y' ELSE 'S:N' END AS r FROM dual;\n" for c in cases)
    rs = re.findall(r"^(L:[YN]S:[YN])\s*$", ora(q), re.M)
    rec("L07", rs == ["L:YS:Y", "L:YS:N", "L:NS:N"], f"Oracle: IS JSON lỏng/chặt trên chuỗi chuẩn, tên không nháy kép, chuỗi thiếu ngoặc → {rs}")
    o = ora(L.PART_DDL + L.PART_LOAD + L.DROP_PART)
    rec("L07", _ints(o)[-1:] == [len(dates) - alg.bnx_l07_count(dates, "2025-01-01", "2025-02-01")] == [3340],
        f"Oracle: bỏ phân vùng tháng 1 rồi ROLLBACK vẫn còn {_ints(o)[-1:]} = 3 340 dòng (lệnh tự chốt; mất 310)")
    ora(L.PART_DDL + L.PART_LOAD)
    rec("L07", L.DOCKER_RUN.count("gvenzl/oracle-free:23-slim") == 1 and "1521:1521" in L.DOCKER_RUN and "FREEPDB1" in L.DOCKER_RUN,
        "khối docker của bước làm thêm dùng đúng ảnh gvenzl/oracle-free:23-slim, cổng 1521, dịch vụ FREEPDB1 (như dbrun.py)")

    # ── AF2 (WP4): quy mô trên Oracle thật và lab sqlite ──
    import datetime as _dt
    import subprocess
    import dbrun as _db
    o = _db.ora(L.ORA_SCALE)
    nums = _ints(o)
    # đường khác: đếm bằng vòng lặp thuần trên danh sách ngày dựng từ công thức của bài
    days = [_dt.date(2025, 1, 1) + _dt.timedelta(days=(r - 1) // 1000) for r in range(1, 365001)]
    n_year, n_mar = len(days), sum(1 for d in days if d.year == 2025 and d.month == 3)
    rec("L07", nums[:2] == [n_year, n_mar] == [365000, 31000] and nums[:2] == [len(alg.bnx_l07_load(365000, per_day=1000)),
        alg.bnx_l07_month_rows(1000, 3)], f"Oracle thật: nạp 365 000 dòng → cả năm {nums[0]}, phân vùng tháng 3 {nums[1]} = đếm bằng vòng lặp Python")
    rec("L07", [alg.bnx_l07_month_rows(p, 3) for p in (10, 1000, 100000)] == [310, 31000, 3100000]
        and [p * 365 for p in (10, 1000, 100000)] == [3650, 365000, 36500000] and 31 / 365 == 310 / 3650 == 31000 / 365000,
        "ba mức quy mô: 310 / 31 000 / 3 100 000 dòng của tháng 3 (đã đo ở 3 650 và 365 000; mức 36 500 000 tính theo tỉ lệ 31/365)")
    clean = [x.strip() for x in L.ORA_SCALE_OUT.strip().split("\n")]
    rec("L07", [x.strip() for x in o.strip().split("\n") if x.strip()] == clean, "đầu ra hiện trên màn hình = đầu ra thật của sqlplus (từng dòng)")
    lab = ROOT / "labs" / "BNX" / "L07"
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", str(lab / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8")
    # mô hình thuần: kiểm JSON bằng thư viện json của Python (đường khác với json_valid của sqlite)
    import json
    DONG = [(1, '{"kenh":"atm","may":"A7","tien":500000}'), (2, '{"kenh":"app","thiet_bi":"d9","tien":200000}'), (3, '{"kenh":"atm","may":"B2"'),
            (4, '{"kenh":"app","thiet_bi":"d1","tien":900000}'), (5, '{"kenh":"atm","may":"A7","tien":300000}')]
    ok, bad = [], []
    for i, js in DONG:
        try:
            ok.append(json.loads(js))
        except ValueError:
            bad.append(i)
    want = [f"dong {i}: tu choi (JSON hong)" for i in bad] + [
        f"tong tien kenh atm: {sum(d['tien'] for d in ok if d['kenh'] == 'atm')}",
        f"so giao dich kenh app: {sum(1 for d in ok if d['kenh'] == 'app')}",
        f"may A7: {sum(1 for d in ok if d.get('may') == 'A7')} giao dich"]
    rec("L07", r.returncode == 0 and r.stdout.strip() == (lab / "mong_doi.txt").read_text(encoding="utf-8").strip() == "\n".join(want),
        "lab: lời giải sqlite chạy lại = mong_doi = mô hình thuần json.loads (dòng 3 bị từ chối; 800000 / 2 / 2)")
