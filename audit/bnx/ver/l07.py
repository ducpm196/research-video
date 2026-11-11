"""Kiểm độc lập BNX L07 — chạy THẬT các hằng mã của audit/bnx/src/l07.py trên Oracle (bnx-ora, Oracle AI Database 26ai Free 23.26.3),
đọc con số và kế hoạch thực thi bằng biểu thức chính quy, đếm từng phân vùng bằng PARTITION FOR (đường khác), rồi so với alg.bnx_l07_*.

Quyền hàng đợi: người dùng bnx (vai trò DB_DEVELOPER_ROLE) KHÔNG gọi được DBMS_AQADM (PLS-00201). Đã cấp ngày 2026-11-11 bằng SYSTEM:
    docker exec -i bnx-ora sqlplus -s system/Bnx_Pass_2026@//localhost/FREEPDB1 <<'SQL'
    GRANT AQ_ADMINISTRATOR_ROLE TO bnx;
    GRANT AQ_USER_ROLE TO bnx;
    GRANT EXECUTE ON DBMS_AQ TO bnx;
    GRANT EXECUTE ON DBMS_AQADM TO bnx;
    SQL
Dựng lại container thì phải cấp lại (bộ kiểm báo FAIL kèm lệnh trên nếu thiếu quyền).
Bộ nhớ cột: INMEMORY_SIZE = 0 trên bản này; bật cần đặt tham số rồi khởi động lại instance (Oracle In-Memory Guide) — instance dùng chung với
các bài khác nên KHÔNG làm; bài chỉ khẳng định điều quan sát được (0, thuộc tính ENABLED). Phân mảnh: không chạy (cần nhiều cơ sở dữ liệu)."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402
import l07 as L  # noqa: E402

GRANTS = ("GRANT AQ_ADMINISTRATOR_ROLE TO bnx; GRANT AQ_USER_ROLE TO bnx; GRANT EXECUTE ON DBMS_AQ TO bnx; GRANT EXECUTE ON DBMS_AQADM TO bnx;")


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

    # 5. Hàng đợi
    roles = ora("SELECT role FROM session_roles WHERE role LIKE 'AQ%';")
    if "AQ_ADMINISTRATOR_ROLE" not in roles:
        rec("L07", False, "bnx thiếu quyền hàng đợi — cấp bằng SYSTEM: " + GRANTS)
        return
    o = ora(L.AQ_CLEAN + L.AQ_SETUP + L.AQ_ENQ + L.AQ_DEQ + "SELECT COUNT(*) AS so_thong_diep FROM bnx_l07_qt;")
    got, left = alg.bnx_l07_queue([("enq", 101), ("rollback",), ("enq", 102), ("commit",), ("deq",), ("commit",)])
    rec("L07", "ORA-" not in o and "PLS-" not in o, "Oracle: tạo hàng đợi, gửi, nhận không lỗi")
    rec("L07", _ints(o)[:1] == [alg.bnx_l07_queue([("enq", 101), ("rollback",), ("enq", 102), ("commit",)])[1]] == [1],
        f"Oracle: gửi 101 rồi hoàn tác, gửi 102 rồi chốt → còn {_ints(o)[:1]} = alg 1")
    rec("L07", "nhan: 102 200000" in o and got == [102], "Oracle: nhận đúng 102, 200 000 (alg: [102])")
    rec("L07", _ints(o)[-1:] == [left] == [0], f"Oracle: sau khi nhận và chốt còn {_ints(o)[-1:]} = 0")
    o = ora("""SELECT retention FROM user_queues WHERE name = 'BNX_L07_Q';
DECLARE eo DBMS_AQ.ENQUEUE_OPTIONS_T; mp DBMS_AQ.MESSAGE_PROPERTIES_T; id RAW(16);
BEGIN eo.visibility := DBMS_AQ.IMMEDIATE; DBMS_AQ.ENQUEUE('bnx_l07_q', eo, mp, bnx_l07_msg(103, 1), id); ROLLBACK; END;
/
SELECT COUNT(*) FROM bnx_l07_qt;""")
    rec("L07", _ints(o) == [0, 1], f"Oracle: thời gian lưu giữ mặc định 0; visibility IMMEDIATE rồi hoàn tác vẫn còn thông điệp {_ints(o)} = [0, 1] (vì thế bài ghi “mặc định”)")
    vis = ora("SET SERVEROUTPUT ON\nDECLARE eo DBMS_AQ.ENQUEUE_OPTIONS_T; BEGIN DBMS_OUTPUT.PUT_LINE(CASE eo.visibility WHEN DBMS_AQ.ON_COMMIT "
              "THEN 'ON_COMMIT' ELSE 'KHAC' END); END;\n/")
    rec("L07", "ON_COMMIT" in vis, "Oracle: ENQUEUE_OPTIONS_T mặc định visibility = ON_COMMIT (gửi là một phần của giao dịch)")

    # 6. Bộ nhớ cột (chỉ điều quan sát được)
    o = ora(L.PART_DDL + L.IM_CHECK)
    rec("L07", re.search(r"^0\s*$", o, re.M) is not None and "ENABLED" in o, "Oracle: INMEMORY_SIZE = 0, ALTER TABLE … INMEMORY → DEF_INMEMORY ENABLED")

    # 7. Chia mảnh minh hoạ (không phải cách của Oracle; bài ghi “minh hoạ”)
    rec("L07", [alg.bnx_l07_shard(a, 3) for a in (4, 5, 7, 8, 10)] == [a - 3 * (a // 3) for a in (4, 5, 7, 8, 10)] == [1, 2, 1, 2, 1],
        "chia mảnh minh hoạ: 4, 5, 7, 8, 10 → mảnh 1, 2, 1, 2, 1")

    # 8. Sổ mã: nguồn dọn hàng đợi trùng hằng
    import yaml
    reg = yaml.safe_load((ROOT / "audit" / "bnx" / "screen" / "l07.yaml").read_text(encoding="utf-8"))
    rec("L07", (reg.get("sources") or {}).get("L07_aq_clean", {}).get("code", "").strip("\n") == L.AQ_CLEAN.strip("\n"),
        "sổ screen/l07.yaml: nguồn L07_aq_clean trùng hằng AQ_CLEAN")
