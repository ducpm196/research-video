"""Kiểm độc lập BNX L36 (Phỏng vấn thiết kế hệ thống). Đường khác với tools/checklib_bnx/l36.py và với mã trên màn hình:
- CHẠY LẠI THẬT (không đệm) mọi chương trình trên màn hình (Python 3 + sqlite3) và so từng ký tự với đầu ra đã hiện;
- ước lượng ×1, ×100, ×10 000 tính lại bằng PHÂN SỐ (Fraction), trần bằng phép chia nguyên (không dùng math.ceil);
- khoá lũy đẳng: mô phỏng khác (ràng buộc UNIQUE của sqlite + bắt IntegrityError) và đếm số lần trừ tiền;
- đối soát: đếm bằng phép chia nguyên và bằng vòng lặp từng lệnh;
- bộ lọc chữ báo mức: tách từ (không dùng biểu thức chính quy), so với đầu ra; 10 câu tiếng Anh phải có NGUYÊN VĂN trong sources_l36.md (chuẩn hoá dấu nháy/khoảng trắng);
- lab: chạy loi_giai.py, so mong_doi.txt, tính lại số bằng Fraction."""
import re
import sqlite3
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import lib2  # noqa: E402
import l36 as src  # noqa: E402

LAB = ROOT / "labs" / "BNX" / "L36"


def tran_len(a, b):
    """Làm tròn lên a / b bằng phép chia nguyên (a, b là Fraction)."""
    q, r = divmod(a, b)
    return int(q) + (1 if r else 0)


def moc(khach, gdk, he, dinh_hs, byte, nut):
    gd = khach * he * gdk
    tb = F(gd, 86400)
    dinh = tb * dinh_hs
    return gd, tb, dinh, F(gd * byte, 10 ** 9), tran_len(dinh, nut)


def chuan(t):
    return re.sub(r"\s+", " ", t.replace("’", "'").replace("“", '"').replace("”", '"')).strip()


def run(rec):
    lib2.verify_programs(rec, "L36")
    P = {q.name: q for q in lib2.PROGRAMS if q.lesson == "L36"}
    # ── ước lượng ──
    ket = [moc(100000, 2, h, 10, 500, 2000) for h in (1, 100, 10000)]
    exp = []
    for h, (gd, tb, dinh, gb, nut) in zip((1, 100, 10000), ket):
        exp.append(f"x{h}: {gd} gd/ngay, tb {float(tb):.1f}/s, dinh {round(float(dinh))}/s")
        exp.append(f"      {float(gb):.1f} GB/ngay, {nut} nut ghi")
    rec("L36", P["UocLuong"].out.splitlines() == exp, "ước lượng ×1, ×100, ×10 000 tính lại bằng Fraction: khớp từng dòng của UocLuong")
    rec("L36", [k[0] for k in ket] == [200000, 20000000, 2000000000] and [k[4] for k in ket] == [1, 2, 116] and ket[2][2] > 231481 and ket[2][2] < 231482 and F(200000, 86400) == F(125, 54),
        "giao dịch mỗi ngày 200 000 / 20 triệu / 2 tỉ; số nút 1, 2, 116 (trần bằng chia nguyên); 200 000 : 86 400 = 125/54")
    rec("L36", [alg.bnx_l36_nut(100000, 2, h, 10, 2000) for h in (1, 100, 10000)] == [1, 2, 116] and [alg.bnx_l36_dinh(100000, 2, h, 10) for h in (1, 100, 10000)] == [23, 2315, 231481]
        and [alg.bnx_l36_gb(100000, 2, h, 500) for h in (1, 100, 10000)] == [0.1, 10.0, 1000.0] and [alg.bnx_l36_tb(100000, 2, h) for h in (1, 100, 10000)] == [2.3, 231.5, 23148.1], "checklib khớp Fraction: đỉnh 23, 2 315, 231 481; GB 0,1, 10, 1 000; trung bình 2,3, 231,5, 23 148,1")
    q1 = moc(300000, 3, 1, 6, 0, 1500)
    rec("L36", float(q1[1]) > 10.41 and float(q1[1]) < 10.42 and q1[2] == F(125, 2) and q1[4] == 1 and alg.bnx_l36_nut(300000, 3, 1, 6, 1500) == 1, "quiz câu 1: 900 000 : 86 400 = 10,4; đỉnh 62,5; một nút")
    # ── khoá lũy đẳng: UNIQUE + IntegrityError ──
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE tk (ma TEXT PRIMARY KEY, sd INTEGER)")
    db.execute("CREATE TABLE yc (k TEXT PRIMARY KEY)")
    db.executemany("INSERT INTO tk VALUES (?, ?)", [("A", 1000), ("B", 0)])
    tru = 0

    def gui(k, tien):
        nonlocal tru
        try:
            with db:
                if k is not None:
                    db.execute("INSERT INTO yc VALUES (?)", (k,))
                db.execute("UPDATE tk SET sd = sd - ? WHERE ma = 'A'", (tien,))
                db.execute("UPDATE tk SET sd = sd + ? WHERE ma = 'B'", (tien,))
            tru += 1
        except sqlite3.IntegrityError:
            pass
    gui(None, 300)
    gui(None, 300)
    kk = dict(db.execute("SELECT ma, sd FROM tk"))
    db.execute("UPDATE tk SET sd = 1000 WHERE ma = 'A'")
    db.execute("UPDATE tk SET sd = 0 WHERE ma = 'B'")
    tru = 0
    gui("K1", 300)
    gui("K1", 300)
    ck = dict(db.execute("SELECT ma, sd FROM tk"))
    rec("L36", kk == {"A": 400, "B": 600} and ck == {"A": 700, "B": 300} and tru == 1 and sum(kk.values()) == sum(ck.values()) == 1000, "UNIQUE + IntegrityError: không khoá 400/600 (trừ 2 lần), có khoá 700/300 (trừ 1 lần); tổng tiền luôn 1 000")
    ol = P["KhoaLuyDang"].out.splitlines()
    rec("L36", ol == ["khong khoa, gui 2 lan: {'A': 400, 'B': 600}", "co khoa K1, lan 1: da chuyen", "co khoa K1, lan 2: trung khoa, bo qua", "so du: {'A': 700, 'B': 300}", "cung khoa K1, 500: 422: cung khoa, noi dung khac"], "đầu ra KhoaLuyDang đúng năm dòng; cùng khoá khác nội dung bị từ chối với mã 422")
    # ── đối soát ──
    lech = {n: sum(1 for i in range(n) if i % 500 == 499) for n in (1000, 100000)}
    rec("L36", lech == {1000: 2, 100000: 200} and [alg.bnx_l36_lech(n) for n in (1000, 100000)] == [2, 200] and round(float(F(2 * 10, 60)), 1) == 0.3 and round(float(F(200 * 10, 60)), 1) == 33.3,
        "đối soát: 2 lệch ở 1 000 lệnh (0,3 giờ), 200 lệch ở 100 000 lệnh (33,3 giờ) — đếm từng lệnh = n // 500")
    rec("L36", P["DoiSoat"].out.splitlines() == ["1000 lenh: 2 lech, 200 dong treo; tay 0.3 gio", "100000 lenh: 200 lech, 20000 dong treo; tay 33.3 gio"] and alg.bnx_l36_gio(2) == 0.3 and alg.bnx_l36_gio(200) == 33.3, "đầu ra DoiSoat khớp; 200 đồng/20 000 đồng treo = 100 mỗi lệnh")
    # ── kiểm cân bằng ──
    rec("L36", P["KiemCanBang"].out.splitlines() == ["tb 125/54 = 2.3148 gd/s; dinh 23.1481", "tong tien dau: 1000", "tong tien 1 lan: 1000", "tong tien 2 lan sai: 1000"], "KiemCanBang: 125/54 = 2,3148; đỉnh 23,1481; tổng tiền 1 000 ở cả ba tình huống")
    # ── bộ lọc chữ báo mức: tách từ ──
    cau = [(m.group(1), m.group(2)) for m in re.finditer(r'\("([^"]+)",\s*((?:"[^"]*"\s*)+)\)', P["DocCau"].code.split("MUC = ")[0])]
    cau = [(n, chuan("".join(re.findall(r'"([^"]*)"', t)))) for n, t in cau]
    rec("L36", len(cau) == 10, "10 câu trong mã DocCau")
    exp2 = []
    for i, (nguon, c) in enumerate(cau, 1):
        tok = re.findall(r"[A-Za-z]+", c)
        muc = []
        for j, t in enumerate(tok):
            nxt = tok[j + 1] if j + 1 < len(tok) else ""
            if t == "MUST" and nxt == "NOT":
                muc.append("cam tuyet doi")
        if any(t == "MUST" and (k + 1 >= len(tok) or tok[k + 1] != "NOT") for k, t in enumerate(tok)):
            muc.append("bat buoc")
        if any(t == "SHOULD" and (k + 1 >= len(tok) or tok[k + 1] != "NOT") for k, t in enumerate(tok)):
            muc.append("nen")
        if "MAY" in tok:
            muc.append("tuy chon")
        if not muc and "must" in tok:
            muc.append("bat buoc (van thuong)")
        if not muc and ("Consider" in tok or "should" in tok):
            muc.append("nen (van thuong)")
        tu = [t for t in ["idempot", "payload", "retr", "conflict", "isolation", "serializ", "budget", "unique"] if t in c.lower()]
        exp2.append(f"{i} {nguon}: {' + '.join(muc or ['mo ta'])} | {','.join(tu)}")
    out = P["DocCau"].out.splitlines()
    rec("L36", out == exp2, "bộ lọc chữ báo mức (tách từ) khớp 10 dòng đầu ra")
    nhom = [l.split(": ", 1)[1].split(" | ")[0] for l in out]
    rec("L36", nhom.count("mo ta") == 6 and nhom[2] == "cam tuyet doi + bat buoc" and nhom[6] == "bat buoc (van thuong)" and nhom[7] == "nen (van thuong)" and nhom[8] == "nen" and len(nhom) == 10, "10 câu = 1 (cấm + bắt buộc) + 1 bắt buộc + 2 nên + 6 mô tả")
    md = chuan((ROOT / "audit" / "bnx" / "sources_l36.md").read_text(encoding="utf-8"))
    thieu = [i + 1 for i, (_, c) in enumerate(cau) if chuan(c) not in md]
    rec("L36", not thieu and all(chuan(e[1]) == c for e, (_, c) in zip(src.ENG, cau)), f"10 câu tiếng Anh có NGUYÊN VĂN trong sources_l36.md và khớp bảng trên màn hình (thiếu: {thieu})")
    # ── lab ──
    r = subprocess.run([sys.executable, "-I", str(LAB / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8", timeout=60)
    want = (LAB / "mong_doi.txt").read_text(encoding="utf-8").strip()
    g1 = moc(50000, 4, 1, 8, 0, 500)
    g2 = moc(50000, 4, 1000, 8, 0, 500)
    rec("L36", r.returncode == 0 and r.stdout.strip() == want and want.splitlines()[0] == f"x1: tb {float(g1[1]):.1f}/s, dinh {round(float(g1[2]))}/s, {g1[4]} nut -> mot nut"
        and want.splitlines()[1] == f"x1000: tb {float(g2[1]):.1f}/s, dinh {round(float(g2[2]))}/s, {g2[4]} nut -> chia theo khoa" and g1[4] == 1 and g2[4] == 38, "lab: loi_giai.py in đúng mong_doi.txt; ×1 → 1 nút (mot nut), ×1 000 → 38 nút (chia theo khoa) (Fraction)")
    rec("L36", want.splitlines()[2:] == ["lan 1: da chuyen", "lan 2: trung khoa, bo qua", "so du: A=300 B=200"] and 500 - 200 == 300, "lab: khoá K9 gửi hai lần, A = 300, B = 200")
    rec("L36", all((LAB / f).exists() for f in ("de.md", "mong_doi.txt", "loi_giai.py")), "lab: có de.md, mong_doi.txt, loi_giai.py")
    # ── sửa theo báo cáo người đọc R_BNX_L31_36 ──
    de = (LAB / "de.md").read_text(encoding="utf-8")
    d1_chua, d1_roi = float(g1[2]), round(float(g1[1]), 1) * 8
    d2_chua, d2_roi = float(g2[2]), round(float(g2[1]), 1) * 8
    rec("L36", round(d1_chua) == 19 and round(d1_roi) == 18 and round(d2_chua) == 18519 and round(d2_roi) == 18518 and "chưa làm tròn" in de and "18 thay vì 19" in de,
        "lab: đỉnh phải tính từ trung bình CHƯA làm tròn (19 và 18 519); từ trung bình đã làm tròn ra 18 và 18 518; de.md nói rõ điều đó")
    rec("L36", "so * 10 / 60" in P["DoiSoat"].code and "ghi_no[i] = 100" in P["DoiSoat"].code and "% 500 != 499" in P["DoiSoat"].code and F(2 * 10, 60) == F(1, 3) and 2 * 100 == 200,
        "đối soát: giả định hiện trên màn hình (500 lệnh một lệch, 10 phút mỗi lệnh lệch, 100 đồng treo) đúng là các hằng trong mã")
    rec("L36", "API v1" in src.ENG[3][0] and src.ENG[4][1].startswith("For API v1,") and "API v1" in src.ENG[4][0] and "API v1" in src.ENG[3][2] and "API v1" in src.ENG[4][2],
        "câu Stripe 4 và 5 mang điều kiện áp dụng API v1 (nhãn nguồn, bản dịch, và nguyên văn câu 5 có cụm 'For API v1,')")
    rec("L36", "422" in P["KhoaLuyDang"].out and "409" not in P["KhoaLuyDang"].out,
        "khoá lũy đẳng: cùng khoá khác nội dung in mã 422 (409 chỉ nói ở bảng: yêu cầu cùng khoá còn xử lý dở)")
    # ── vòng fix4: hằng số hiện trên màn hình, 62,5 vs 62,4, ví dụ nhỏ của bảng regex ──
    uoc = P["UocLuong"].code.split("\n")
    hang = {"KHACH": 100_000, "GD_KHACH": 2, "DINH": 10, "BYTE": 500, "NUT": 2000}
    rec("L36", "100_000, 2, 10" in "\n".join(uoc[2:6]) and "BYTE, NUT = 500, 2000" in "\n".join(uoc[2:6])
        and all(F(100_000 * 2 * k, 86_400) * hang["DINH"] / hang["NUT"] > 0 for k in (1, 100, 10_000)),
        "hằng số hiện ở dòng 3–6 của UocLuong.py: 100 000 khách, 2 gd, đỉnh 10, 500 byte, 2 000 gd/s mỗi nút")
    nut = [-(-(F(100_000 * 2 * k, 86_400) * 10) // 2000) for k in (1, 100, 10_000)]
    rec("L36", nut == [1, 2, 116] and F(900_000, 86_400) * 6 == F("62.5") and round(10.4 * 6, 1) == 62.4 and round(900_000 / 86_400, 1) == 10.4,
        "quiz 2: 900 000/86 400 ≈ 10,4167; ×6 = 62,5 (chưa làm tròn), 10,4 × 6 = 62,4; nút 1 / 2 / 116")
    rec("L36", re.search("MUST", "it MUST be") is not None and re.search(r"\bMAY\b", "MAYBE") is None and re.search(r"\bMAY\b", "it MAY be") is not None
        and re.search(r"\bMUST\b(?! NOT)", "MUST be") is not None and re.search(r"\bMUST\b(?! NOT)", "MUST NOT be") is None,
        "bảng regex: re.search, \b (MAY không khớp MAYBE), (?! NOT) (MUST khớp MUST be, không khớp MUST NOT)")
    kd = P["KhoaLuyDang"].code.split("\n")
    i0 = next(i for i, x in enumerate(kd) if "def chuyen" in x)
    rec("L36", 'return "da chuyen"' in kd[i0 + 15] and 'return "422' in kd[i0 + 8] and kd[i0 + 9].lstrip().startswith("db.execute(\"INSERT INTO yeu_cau"),
        "KhoaLuyDang.py: khung 1/2 (9 dòng từ def chuyen) kết thúc ở return 422; khung 2/2 (7 dòng) từ INSERT yeu_cau tới return 'da chuyen'")
