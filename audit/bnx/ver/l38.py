"""Kiểm độc lập BNX L38 (Hàng đợi AQ, bộ nhớ cột và phân mảnh Oracle). Đường khác với tools/checklib_bnx/l38.py và với mã trên màn hình:
- CHẠY LẠI THẬT (không đệm) mọi chương trình Python trên màn hình và so từng ký tự với đầu ra đã hiện;
- hàng đợi: chạy THẬT các hằng AQ_* của audit/bnx/src/l38.py trên Oracle (bnx-ora, Oracle AI Database 26ai Free 23.26.3), đọc con số bằng biểu thức chính quy,
  đọc thẳng nội dung bảng hàng đợi (user_data) làm đường khác, kiểm thời gian lưu giữ mặc định và visibility mặc định, rồi so với alg.bnx_l38_queue;
- bộ nhớ cột: chỉ điều quan sát được (INMEMORY_SIZE = 0, user_tables.inmemory = ENABLED); số ô theo hàng/cột tính lại bằng công thức, không dùng chương trình;
- phân mảnh: đếm cặp xuyên mảnh bằng tổ hợp (cỡ từng lớp dư), đổi 3 → 4 mảnh bằng chu kỳ 12;
- lab: chạy loi_giai.py, so mong_doi.txt, tính lại bằng mô hình danh sách thuần.
Quyền hàng đợi: người dùng bnx cần AQ_ADMINISTRATOR_ROLE, AQ_USER_ROLE, EXECUTE ON DBMS_AQ/DBMS_AQADM (cấp bằng SYSTEM ngày 2026-11-11):
    docker exec -i bnx-ora sqlplus -s system/Bnx_Pass_2026@//localhost/FREEPDB1   # rồi gõ:
    GRANT AQ_ADMINISTRATOR_ROLE TO bnx; GRANT AQ_USER_ROLE TO bnx; GRANT EXECUTE ON DBMS_AQ TO bnx; GRANT EXECUTE ON DBMS_AQADM TO bnx;
Bộ nhớ cột: INMEMORY_SIZE = 0 trên bản này; bật cần đặt tham số rồi khởi động lại instance (Oracle In-Memory Guide), instance dùng chung nên KHÔNG làm."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import lib2  # noqa: E402
import l38 as L  # noqa: E402

LAB = ROOT / "labs" / "BNX" / "L38"


def _ints(out):
    return [int(x) for x in re.findall(r"^\s*(\d+)\s*$", out, re.M)]


def run(rec):
    lib2.verify_programs(rec, "L38")
    P = {q.name: q for q in lib2.PROGRAMS if q.lesson == "L38"}
    # ── bộ nhớ cột: mô hình đếm ô, tính lại bằng công thức ──
    rec("L38", P["DemO"].out.splitlines() == [f"{n} dong: hang {n * 8} o, cot {n} o, cung tong True" for n in (1000, 100000)]
        and [alg.bnx_l38_cells(n, 8, "hang") for n in (1000, 100000, 50000)] == [8000, 800000, 400000]
        and [alg.bnx_l38_cells(n, 8, "cot") for n in (1000, 100000, 50000)] == [1000, 100000, 50000] and 8 * 1000 // 1000 == 8,
        "mô hình đếm ô (8 cột): 1 000 dòng 8 000 ô / 1 000 ô; 100 000 dòng 800 000 / 100 000; quiz 50 000 dòng 400 000 / 50 000 (tính lại bằng công thức)")
    # ── phân mảnh: tổ hợp ──
    def cheo(tk, m):
        lop = [tk // m + (1 if r < tk % m else 0) for r in range(m)]
        return tk * (tk - 1), tk * (tk - 1) - sum(s * (s - 1) for s in lop)
    kq = [cheo(60, m) for m in (1, 3, 30)]
    exp = [f"{m} manh: {x}/{n} lenh xuyen manh, {100 * x / n:.1f}%" for m, (n, x) in zip((1, 3, 30), kq)]
    rec("L38", P["XuyenManh"].out.splitlines() == exp and kq == [(3540, 0), (3540, 2400), (3540, 3480)] and [alg.bnx_l38_cross(60, m) for m in (1, 3, 30)] == kq,
        "đếm xuyên mảnh bằng cỡ lớp dư: 60 tài khoản, 1/3/30 mảnh → 0, 2 400, 3 480 trên 3 540 cặp (67,8 % và 98,3 %)")
    rec("L38", cheo(12, 4) == (132, 108) and 4 * 3 * 2 == 24 and alg.bnx_l38_cross(12, 4) == (132, 108), "quiz câu 3: 12 tài khoản, 4 mảnh → 132 cặp, 24 cùng mảnh, 108 xuyên mảnh")
    # chu kỳ 12: trong 12 mã liên tiếp chỉ mã dư 0, 1, 2 giữ nguyên mảnh (a mod 3 = a mod 4), 9 mã đổi; 1 000 = 83 × 12 + 4, bốn mã cuối dư 0, 1, 2, 3 → thêm 1 mã đổi
    moved = 83 * 9 + 1
    rec("L38", moved == 748 and "748/1000" in P["DoiManh"].out and alg.bnx_l38_moved(1000, 3, 4) == 748 and moved / 1000 == 0.748,
        "đổi 3 → 4 mảnh: mỗi chu kỳ 12 mã có 9 mã đổi mảnh; 1 000 = 83 × 12 + 4 → 83 × 9 + 1 = 748 mã đổi mảnh (74,8 %)")
    # ── mô hình hàng đợi (danh sách thuần) ──
    def mo_hinh(ops):
        hang, cho, nhan = [], [], []
        for o in ops:
            if o == "gui101" or o == "gui102":
                cho.append(int(o[3:]))
            elif o == "huy":
                cho = []
            elif o == "chot":
                hang, cho = hang + cho, []
            elif o == "nhan" and hang:
                nhan.append(hang.pop(0))
        return nhan, len(hang)
    ca1 = ["gui101", "huy", "gui102", "chot"]
    rec("L38", mo_hinh(ca1) == ([], 1) and mo_hinh(ca1 + ["nhan"]) == ([102], 0) and P["MoHinh"].out.splitlines() == ["([], 1)", "([102], 0)"],
        "mô hình danh sách thuần: ca 1 → ([], 1), ca 2 → ([102], 0); khớp đầu ra MoHinh")
    rec("L38", alg.bnx_l38_queue([("enq", 301), ("commit",), ("enq", 302), ("rollback",), ("deq",), ("commit",)]) == ([301], 0), "quiz câu 2: gửi 301 chốt, gửi 302 hoàn tác, nhận → 301, còn 0")
    # ── Oracle thật ──
    try:
        import dbrun
        ok_o, _ = dbrun.ready()
    except Exception as ex:  # noqa: BLE001
        rec("L38", None, f"không gọi được Docker: {type(ex).__name__}")
        ok_o = False
    if not ok_o:
        rec("L38", None, "container bnx-ora chưa chạy")
    else:
        ora = dbrun.ora
        v = ora("SELECT banner_full FROM v$version;")
        rec("L38", "Free" in v and "23.26" in v, "Oracle: đúng bản Oracle AI Database 26ai Free 23.26 (banner thật)")
        roles = ora("SELECT role FROM session_roles WHERE role LIKE 'AQ%';")
        if "AQ_ADMINISTRATOR_ROLE" not in roles:
            rec("L38", False, "bnx thiếu quyền hàng đợi — cấp bằng SYSTEM: GRANT AQ_ADMINISTRATOR_ROLE TO bnx; GRANT AQ_USER_ROLE TO bnx; GRANT EXECUTE ON DBMS_AQ TO bnx; GRANT EXECUTE ON DBMS_AQADM TO bnx;")
        else:
            o = ora(L.AQ_CLEAN + L.AQ_SETUP + L.AQ_ENQ)
            rec("L38", "ORA-" not in o and "PLS-" not in o, "Oracle: tạo hàng đợi, gửi không lỗi")
            gui = alg.bnx_l38_queue([("enq", 101), ("rollback",), ("enq", 102), ("commit",)])
            rec("L38", _ints(o)[-1:] == [gui[1]] == [1], f"Oracle: gửi 101 rồi hoàn tác, gửi 102 rồi chốt → còn {_ints(o)[-1:]} = alg 1")
            o2 = ora("SELECT q.user_data.ma_gd AS ma_gd, q.user_data.so_tien AS so_tien FROM bnx_l38_qt q;")
            rec("L38", re.findall(r"^\s*(\d+)\s+(\d+)\s*$", o2, re.M) == [("102", "200000")], "Oracle (đường khác): đọc thẳng bảng hàng đợi (user_data) → một dòng (102, 200000)")
            o3 = ora(L.AQ_DEQ)
            got, left = alg.bnx_l38_queue([("enq", 101), ("rollback",), ("enq", 102), ("commit",), ("deq",), ("commit",)])
            rec("L38", "nhan: 102 200000" in o3 and got == [102], "Oracle: nhận đúng 102, 200 000 (alg: [102])")
            rec("L38", _ints(o3)[-1:] == [left] == [0], f"Oracle: sau khi nhận và chốt còn {_ints(o3)[-1:]} = 0")
            o4 = ora("""SELECT retention FROM user_queues WHERE name = 'BNX_L38_Q';
DECLARE eo DBMS_AQ.ENQUEUE_OPTIONS_T; mp DBMS_AQ.MESSAGE_PROPERTIES_T; id RAW(16);
BEGIN eo.visibility := DBMS_AQ.IMMEDIATE; DBMS_AQ.ENQUEUE('bnx_l38_q', eo, mp, bnx_l38_msg(103, 1), id); ROLLBACK; END;
/
SELECT COUNT(*) FROM bnx_l38_qt;""")
            rec("L38", _ints(o4) == [0, 1], f"Oracle: thời gian lưu giữ mặc định 0; visibility IMMEDIATE rồi hoàn tác vẫn còn thông điệp {_ints(o4)} = [0, 1] (vì thế bài ghi “mặc định”)")
            vis = ora("SET SERVEROUTPUT ON\nDECLARE eo DBMS_AQ.ENQUEUE_OPTIONS_T; BEGIN DBMS_OUTPUT.PUT_LINE(CASE eo.visibility WHEN DBMS_AQ.ON_COMMIT "
                      "THEN 'ON_COMMIT' ELSE 'KHAC' END); END;\n/")
            rec("L38", "ON_COMMIT" in vis, "Oracle: ENQUEUE_OPTIONS_T mặc định visibility = ON_COMMIT (gửi là một phần của giao dịch)")
            ora(L.AQ_CLEAN)
        o = ora(L.IM_CHECK)
        rec("L38", re.search(r"^0\s*$", o, re.M) is not None and "ENABLED" in o, "Oracle: INMEMORY_SIZE = 0, ALTER TABLE … INMEMORY → user_tables.inmemory = ENABLED")
    # ── lab ──
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", str(LAB / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8", timeout=60)
    want = (LAB / "mong_doi.txt").read_text(encoding="utf-8").strip().splitlines()
    hang, trong = [], []
    for ma, tien, chot in [(201, 750000, True), (202, 300000, False), (203, 120000, True), (204, 900000, True)]:
        if chot:
            hang.append((ma, tien))
    sau_gui = len(hang)
    nhan = [hang.pop(0) for _ in range(2)]
    lenh = [(3, 8), (4, 9), (7, 11), (10, 14), (6, 13)]
    xm = sum(1 for a, b in lenh if a % 4 != b % 4)
    exp = [f"sau gui: {sau_gui} thong diep"] + [f"nhan: {m} {t}" for m, t in nhan] + [f"con lai: {len(hang)}", f"xuyen manh: {xm}/5"]
    rec("L38", r.returncode == 0 and r.stdout.strip().splitlines() == want == exp and xm == 3,
        "lab: loi_giai.py in đúng mong_doi.txt; mô hình danh sách thuần ra cùng 5 dòng (3 thông điệp, nhận 201 và 203, còn 1, 3/5 xuyên mảnh)")
    rec("L38", all((LAB / f).exists() for f in ("de.md", "mong_doi.txt", "loi_giai.py")), "lab: có de.md, mong_doi.txt, loi_giai.py")
    ex = {q.name: q.out for q in lib2.PROGRAMS if q.lesson == "L38"}
    rec("L38", all(k in (ROOT / "audit" / "bnx" / "sources_l38.md").read_text(encoding="utf-8") for k in ("L38OBS", "L38AQ", "L38IM", "L38SHARD")),
        "sources_l38.md có đủ mục nguồn L38OBS, L38AQ, L38IM, L38SHARD")
    _ = ex
    # ── vòng fix4: AQ/DBMS_* giải nghĩa tại chỗ, "thời gian lưu giữ 0" nói rõ nghĩa ──
    _t = " ".join(next((ROOT / "lessons" / "bnx").glob("L38_*.yaml")).read_text(encoding="utf-8").split())
    rec("L38", "Advanced Queuing, hàng đợi nâng cao" in _t and "thời gian lưu giữ là 0 (hàng đợi không giữ lại thông điệp đã nhận)" in _t and "thời gian lưu giữ mặc định là không" in _t,
        "bài giải nghĩa AQ (hàng đợi nâng cao), tên DBMS_ (gói có sẵn, ADM quản trị) và 'thời gian lưu giữ 0' (không giữ lại thông điệp đã nhận)")
