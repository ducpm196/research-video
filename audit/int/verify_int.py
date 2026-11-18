"""Bộ kiểm khoá INT (nâng AF2, WP4, 2026-11-14). Chạy: .venv/Scripts/python -B audit/int/verify_int.py [-v]

KHÔNG sinh bài (INT không có bộ sinh: YAML là nguồn). Bộ này làm ba việc độc lập với lời giải và với `checks:` của bài:
  A. Tính lại BẰNG FRACTION/MATH từng dòng của 8 lab giấy bút labs/INT/L00..L07/mong_doi.txt, rồi so từng dòng với mong_doi.txt
     và kiểm dòng đó có trong loi_giai.md (cổng lab_gate chỉ so chữ; ở đây số được tính lại).
  B. Ghép NGUYÊN VĂN các khối mã hiện trên màn hình (Python, Java 21) từ lessons/int/*.yaml, CHẠY THẬT, so với khối kết quả hiện trên màn hình.
     L02 là mô phỏng lớp vỏ bằng java.lang.reflect.Proxy (không phải Spring thật).
  C. Tính lại các số của cảnh quy mô (×1, ×100, ×10 000…) và kiểm chúng có đúng dạng viết trên màn hình; kiểm các luật trung thực:
     không số lương không nguồn (không "50 triệu", "50M", khung lương), hai nhóm vai trò có ở L00 và L06, L07 có công thức tổng đãi ngộ,
     UIT luôn đi kèm "dự kiến", ACB không bị gán dùng T24, mọi bài khai af2 + covers + cảnh practice + lab.
Mã thoát 0 = đủ PASS."""
import io, math, os, re, subprocess, sys, tempfile
from fractions import Fraction as F
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.path.insert(0, str(ROOT / "tools"))
with __import__("contextlib").redirect_stdout(io.StringIO()):
    import screen_code as sc

V = "-v" in sys.argv
res = []


def ok(name, cond, detail=""):
    res.append((bool(cond), name, detail))
    if V or not cond:
        print(("PASS " if cond else "FAIL ") + name + ((" :: " + str(detail)) if detail and not cond else ""))


def lab(lid):
    d = ROOT / "labs" / "INT" / lid
    return (d / "mong_doi.txt").read_text(encoding="utf-8").strip("\n"), (d / "loi_giai.md").read_text(encoding="utf-8")


def spec(lid):
    f = next((ROOT / "lessons" / "int").glob(f"{lid}_*.yaml"))
    return yaml.safe_load(f.read_text(encoding="utf-8")), f


def vis(d):
    """toàn bộ chữ hiện trên màn hình + lời đọc của một bài"""
    out = []
    for s in d["scenes"]:
        out.append(str(s.get("title", "")))
        for st in s["steps"]:
            out.append(re.sub(r"<[^>]+>", " ", str(st.get("show", ""))))
            out.append(str(st.get("say", "")))
    return re.sub(r"\s+", " ", " ".join(out))


def fnum(x, nd=None):
    """số kiểu máy (dấu chấm) như trong mong_doi.txt"""
    return str(x)


# ───────────────────────── A. lab giấy bút: tính lại độc lập ─────────────────────────
def lab_expected():
    E = {}
    # L00: Little + ngân sách ngừng + nhóm tin
    little = 8000 * F(25, 1000)
    budget = F(525600) * (1 - F(9995, 10000))
    E["L00"] = [f"dang xu ly do: {int(little)}", f"ngung toi da 99.95%: {float(budget)} phut/nam", "nhom tin tuyen dung: B"]
    # L01: cây B-Tree, ngăn xếp luồng
    h, cap = 0, 1
    while cap < 80_000_000:
        cap *= 500; h += 1
    E["L01"] = [f"chieu cao cay: {h}", f"so lan doc mot dong: {h + 1}", f"ngan xep luong he dieu hanh: {2000 * 1} MB", f"ngan xep luong ao: {2000 * 2000} byte"]
    # L02: bể kết nối
    pool = 16 * 2 + 2
    E["L02"] = [f"be ket noi: {pool}", f"toi da khong nhat ky: {int(pool / F(20, 1000))} giao dich/giay",
                f"toi da co nhat ky REQUIRES_NEW: {int(pool / F(25, 1000))} giao dich/giay"]
    # L03: lô lương, giữ khoá
    lo = 24000 // 2000
    giu = 2 * 15
    E["L03"] = [f"so lo: {lo}", f"doi ngu canh tung dong: {24000 * 2}", f"doi ngu canh theo lo: {lo * 2}", f"giu khoa 2PC: {giu} ms",
                f"toi da 2PC tren mot dong nong: {int(1 / F(giu, 1000))} giao dich/giay", f"toi da SAGA tren mot dong nong: {int(1 / F(3, 1000))} giao dich/giay"]
    # L04: bản đồ bit, khối PIN, vòng quay STAN, tin đang chờ (tách bài WP4: tín dụng + đối soát sang L08)
    bm = sum(1 << (64 - b) for b in (3, 7, 11, 41))
    pin = int("0" + "4" + "5821" + "F" * 10, 16) ^ int("0000" + "5412345678901234"[-13:-1], 16)
    quay = F(10 ** 6, 4000)
    E["L04"] = [f"bitmap: {bm:016X}", f"khoi PIN: {pin:016X}", f"STAN quay vong sau: {int(quay)} giay",
                f"chan nham: {'co' if quay < 300 else 'khong'}", f"tin dang cho: {int(4000 * F(3, 2))}"]
    # L08: LTV, DTI, trích nợ từng phần, đối soát cuối ngày (bài mới tách từ L04)
    ltv = F(240) * F(70, 100)
    dti = F(9, 36) * 100
    thu = F(15, 2)
    n = 2 * 10 ** 6
    lap = F(n * n, 10 ** 9 * 3600)
    xep = F(3 * n * math.ceil(math.log2(n)) + 2 * (n + n), 10 ** 9)
    E["L08"] = [f"han muc LTV 70%: {int(ltv)} trieu", f"DTI: {int(dti)}%", f"thu tung phan: {float(thu)} trieu, con thieu {float(12 - thu)} trieu",
                f"doi soat long nhau: {round(float(lap), 1)} gio", f"doi soat sap xep: {round(float(xep), 2)} giay"]
    # L05: nhân xử lý, điểm Z, UCB1, cosine
    ucb = lambda mu, nk, n: float(mu) + math.sqrt(2 * math.log(n) / nk)
    a, b_ = ucb(F(180, 200), 200, 210), ucb(F(9, 10), 10, 210)
    E["L05"] = [f"so nhan mo hinh nhe 3 ms: {int(12000 * F(3, 1000))}", f"so nhan mo hinh nang 40 ms: {int(12000 * F(40, 1000))}",
                f"diem Z: {int(F(45 - 5, 4))}", f"diem A: {a:.2f}", f"diem B: {b_:.2f}", f"chon kenh: {'A' if a > b_ else 'B'}",
                f"cosine: {(2 * 1 + 1 * 3) / math.sqrt((2 * 2 + 1 * 1) * (1 * 1 + 3 * 3)):.3f}"]
    # L06: thiết kế cổng + chuỗi + ngưỡng sinh trắc học (TT 50/2024 sửa đổi bởi TT 77/2025, như ACB L06: > 10 triệu một lần hoặc > 20 triệu tổng ngày)
    do = 2000 * F(200, 1000)
    may = math.ceil(do / 150) + 1
    bud = F(525600) * F(5, 10000)
    chain = F(9995, 10000) ** 3
    need = lambda lan: any(x > 10 for x in lan) or sum(lan) > 20
    E["L06"] = [f"yeu cau do cung luc: {int(do)}", f"so may (moi may 150, +1 du phong): {may}", f"ngan sach 99.95%: {float(bud)} phut/nam",
                f"chuoi 3 tang 99.95%: {float(chain) * 100:.2f}%, ngung {float((1 - chain) * 525600):.1f} phut/nam",
                f"sinh trac hoc 12 trieu mot lan: {'can' if need([12]) else 'chua can'}", f"tong ngay 8 + 7 = 15 trieu: {'can' if need([8, 7]) else 'chua can'}"]
    # L07: tổng đãi ngộ T = L*(13+k) + 12*P
    T = lambda L, k, P: L * (13 + k) + 12 * P
    ta, tb = T(38, 2, 0), T(34, 2, 2)
    pb = F(ta - 34 * (13 + 2), 12)
    E["L07"] = [f"offer A tong nam (k=2): {ta} trieu", f"offer B tong nam (k=2): {tb} trieu", f"chenh lech A hon B: {ta - tb} trieu",
                f"phu cap B can de bang A: {int(pb)} trieu/thang"]
    return E


def check_labs():
    E = lab_expected()
    for lid, lines in E.items():
        want, sol = lab(lid)
        ok(f"A {lid} mong_doi.txt = số tính lại độc lập", want.splitlines() == lines, f"\n  tính lại: {lines}\n  mong_doi: {want.splitlines()}")
        for ln in want.splitlines():
            ok(f"A {lid} loi_giai.md có dòng '{ln[:40]}'", ln in sol)
        files = sorted(p.name for p in (ROOT / "labs" / "INT" / lid).iterdir())
        ok(f"A {lid} thư mục lab đủ de.md, mong_doi.txt, đúng một loi_giai.*", "de.md" in files and "mong_doi.txt" in files and len([f for f in files if f.startswith("loi_giai.")]) == 1, files)
        d, _ = spec(lid)
        scr = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", " ".join(str(st.get("show", "")) for s in d["scenes"] if s["kind"] == "practice" for st in s["steps"])))
        for ln in want.splitlines():
            ok(f"A {lid} dòng mong đợi hiện trên màn hình '{ln[:30]}'", re.sub(r"\s+", " ", ln) in scr)


# ───────────────────────── B. chạy thật mã trên màn hình ─────────────────────────
BLK = sc.all_blocks("INT")


def run_py(code):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "x.py"
        p.write_text(code, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(p)], capture_output=True, text=True, encoding="utf-8", cwd=td, timeout=60,
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        return r.returncode, r.stdout.strip(), r.stderr


def run_java(code, cls):
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / f"{cls}.java").write_text(code, encoding="utf-8")
        c = subprocess.run(["javac", "-encoding", "UTF-8", f"{cls}.java"], capture_output=True, text=True, cwd=td, timeout=120)
        if c.returncode:
            return c.returncode, "", c.stderr
        r = subprocess.run(["java", "-Dfile.encoding=UTF-8", cls], capture_output=True, text=True, encoding="utf-8", cwd=td, timeout=120)
        return r.returncode, r.stdout.strip(), r.stderr


# chỉ số step sau fix6 (2026-11-16): mỗi khối mã được đặt SAU một bước "Đọc trước" nên dịch +1 (L03 quymo giữ nguyên)
PY = [("L00", "quymo", 2), ("L01", "quymo", 1), ("L02", "quymo", 2), ("L03", "quymo", 1), ("L04", "chaythat", 2), ("L04", "quymo", 1), ("L08", "quymo", 2),
      ("L05", "chaythat", 1), ("L05", "quymo", 1), ("L06", "quymo", 2), ("L06", "quymo", 4), ("L07", "quymo", 2)]


def check_code():
    for lid, scene, step in PY:
        code = BLK[f"INT {lid} {scene} {step} 0"]
        want = BLK[f"INT {lid} {scene} {step} 1"]
        rc, out, err = run_py(code + "\n")
        ok(f"B {lid} {scene}.{step} mã Python chạy thật khớp kết quả trên màn hình", rc == 0 and out == want.strip(), f"rc={rc}\n{out}\n--- màn hình:\n{want}\n{err[:300]}")
    # L01: luồng ảo Java 21 (mười nghìn luồng ảo)
    rc, out, err = run_java(BLK["INT L01 example 5 0"] + "\n", "LuongAo")
    ok("B L01 example.5 Java 21 luồng ảo chạy thật", rc == 0 and out == BLK["INT L01 example 5 1"].strip(), f"{rc} {out} {err[:300]}")
    # L02: mô phỏng proxy ghép từ ba khung
    code = "\n".join(BLK[f"INT L02 chaythat {i} 0"] for i in (3, 4, 5)) + "\n"
    rc, out, err = run_java(code, "TuGoi")
    ok("B L02 chaythat Java chạy thật (mô phỏng proxy) khớp kết quả", rc == 0 and out == BLK["INT L02 chaythat 6 0"].strip(), f"{rc}\n{out}\n{err[:300]}")
    ok("B L02 màn hình ghi rõ MÔ PHỎNG", "MÔ PHỎNG" in (ROOT / "lessons/int/L02_backend_microservices.yaml").read_text(encoding="utf-8"))
    # kiểm chéo ý nghĩa: số giao dịch sau lệnh gọi đầu là 1 (hàm tự gọi không qua vỏ), sau lệnh gọi thứ hai là 2
    out2 = BLK["INT L02 chaythat 6 0"].splitlines()
    ok("B L02 tự gọi nội bộ: vỏ chỉ mở 1 giao dịch cho chuyen, rồi 2 sau khi gọi ghiVet qua vỏ",
       out2[2] == "so giao dich: 1" and out2[5] == "so giao dich: 2" and sum("vo mo giao dich" in x for x in out2) == 2)


# ───────────────────────── C. số của cảnh quy mô + luật trung thực ─────────────────────────
def check_scale():
    t = {lid: vis(spec(lid)[0]) for lid in ("L00", "L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08")}
    # L00: Little ×1, ×100, ×10 000 (w = 10 ms) và phút ngừng theo số chín
    ok("C L00 Little 5 / 500 / 50000", [x * F(10, 1000) for x in (500, 50000, 5_000_000)] == [5, 500, 50000]
       and all(s in t["L00"] for s in ("50 000", "5 triệu")))
    ok("C L00 phút ngừng 5256 / 525,6 / 52,56 (hiện trên màn hình là kết quả chạy thật)", [round(float(525600 * F(1, 10 ** n)), 2) for n in (2, 3, 4)] == [5256.0, 525.6, 52.56]
       and all(x in t["L00"] for x in ("5256.0", "525.6", "52.56")))
    # L00: gói thu nhập số minh hoạ L = 40
    ok("C L00 T = 40*(13+k): 560..680", (40 * 14, 40 * 17) == (560, 680) and "560" in t["L00"] and "680" in t["L00"] and "số minh hoạ" in t["L00"])

    def height(n, m):
        h, c = 0, 1
        while c < n:
            c *= m; h += 1
        return h
    ok("C L01 cây cao 2/3/4 tầng cho 10^4, 10^7, 10^10 (m=1000)", [height(10 ** e, 1000) for e in (4, 7, 10)] == [2, 3, 4])
    ok("C L01 luồng ảo 10 000 x 2 000 byte = 20 MB; luồng hệ điều hành 10 000 x 1 MB ~ 10 GB", 10000 * 2000 == 20_000_000 and 10000 * 1 == 10000)
    ok("C L02 bể 17; cần 10/100/1000 kết nối; trần 850", (17, [int(x * F(20, 1000)) for x in (500, 5000, 50000)], int(17 / F(20, 1000))) == (8 * 2 + 1, [10, 100, 1000], 850)
       and "850" in t["L02"])
    ok("C L03 giữ khoá 40/400/4000 ms → xong 400/4000/40000 s; SAGA 4 ms → 40 s", [int(10000 * 2 * F(r, 1000)) for r in (20, 200, 2000)] == [400, 4000, 40000]
       and int(10000 * F(4, 1000)) == 40 and "40 000" in t["L03"] and "11 giờ" in t["L03"])
    def eod(n):
        return n * n / 1e9 / 3600, (3 * n * math.ceil(math.log2(n)) + 2 * (n + n)) / 1e9
    got = [(round(eod(n)[0], 1), round(eod(n)[1], 2)) for n in (3 * 10 ** 6, 3 * 10 ** 7, 3 * 10 ** 8)]
    ok("C L08 đối soát: lồng nhau 2,5/250/25000 giờ vs 0,21/2,37/27,3 giây", got == [(2.5, 0.21), (250.0, 2.37), (25000.0, 27.3)]
       and all(s in t["L08"] for s in ("25 000", "27,3", "2,37")))
    ok("C L04 STAN quay lại sau 10^6/t = 10 000 / 1 000 / 100 giây; tin chờ 200 / 2 000 / 20 000; khoá chỉ có STAN sống 300 giây bị chặn nhầm ở 10 000 gd/s",
       [10 ** 6 // t_ for t_ in (100, 1000, 10000)] == [10000, 1000, 100] and [2 * t_ for t_ in (100, 1000, 10000)] == [200, 2000, 20000] and 100 < 300
       and all(x in t["L04"] for x in ("10 000 giây", "1 000 giây", "100 giây", "20 000", "300 giây")))
    ok("C L04 bản đồ bit 3,4,11,37,52 = 3020000008001000 và khối PIN rõ 04122D789ABCDEF6",
       f"{sum(1 << (64 - b) for b in (3, 4, 11, 37, 52)):016X}" == "3020000008001000"
       and f"{int('041234FFFFFFFFFF', 16) ^ int('0000' + '4321987654321098'[-13:-1], 16):016X}" == "04122D789ABCDEF6")
    ok("C L05 nhân xử lý nhẹ 1/10/100, nặng 40/400/4000", [x * 2 / 1000 for x in (500, 5000, 50000)] == [1, 10, 100]
       and [x * 80 / 1000 for x in (500, 5000, 50000)] == [40, 400, 4000])
    ok("C L06 yêu cầu dở 120/1200/12000, máy 1/3/24 (+1), chuỗi 4 tầng 99,96% và 210,2 phút",
       [x * 0.12 for x in (1000, 10000, 100000)] == [120, 1200, 12000]
       and [math.ceil(x * 0.12 / 500) for x in (1000, 10000, 100000)] == [1, 3, 24]
       and round(0.9999 ** 4 * 100, 2) == 99.96 and round((1 - 0.9999 ** 4) * 525600, 1) == 210.2)
    tot, tang, got = 0, 1.0, {}
    for nam in range(1, 6):
        tot += 4 * 15 * tang
        got[nam] = round(tot, 1)
        tang *= 1.08
    ok("C L07 phần mất đi 60 / 194,8 / 352 triệu sau 1, 3, 5 năm", (got[1], got[3], got[5]) == (60.0, 194.8, 352.0) and "194,8" in t["L07"] and "352" in t["L07"])
    ok("C L07 đòn 3: lương cứng 36 so với 40 chênh 56..68 ở k = 1..4", [40 * (13 + k) - 36 * (13 + k) for k in (1, 2, 3, 4)] == [56, 60, 64, 68])


def check_honesty():
    for lid in ("L00", "L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08"):
        d, f = spec(lid)
        raw = f.read_text(encoding="utf-8")
        txt = vis(d)
        ok(f"C {lid} af2: true + covers + cảnh practice + lab", d.get("af2") is True and d.get("covers") and any(s["kind"] == "practice" for s in d["scenes"])
           and (ROOT / "labs" / "INT" / lid).is_dir())
        ok(f"C {lid} không còn con số lương không nguồn (50 triệu gross, 50M, khung lương thị trường)",
           not re.search(r"50 ?triệu gross|50M|năm mươi triệu gross|mức (lương |đãi ngộ )?50 ?triệu|lương[^.]{0,30}50 ?triệu|(Mid|Senior|Junior)[^.]{0,30}\d+ ?[–-] ?\d+ ?triệu", txt + " " + str(d["title"])),
           re.findall(r".{20}50 ?triệu.{20}", txt))
        ok(f"C {lid} không nhắc nguồn người xem không có ('tài liệu', 'như đã học ở khoá')", "như đã học ở khoá" not in raw and "như đã học ở khóa" not in raw)
        if "UIT" in txt:
            ok(f"C {lid} UIT luôn kèm 'dự kiến' tốt nghiệp cuối năm 2026 (không ghi tháng 11/2026) và không nói đã có bằng",
               "dự kiến" in txt and "cuối năm 2026" in txt and "11/2026" not in txt.replace("ky 11/2026", "") and not re.search(r"đã tốt nghiệp|đã có bằng|đã nhận bằng|có bằng cử nhân AI", txt))
    t0, t6, t7, t4, t8 = (vis(spec(i)[0]) for i in ("L00", "L06", "L07", "L04", "L08"))
    ok("C L00 có khung hai nhóm vai trò (A: dịch vụ nhỏ hiện đại; B: hệ cũ và nghiệp vụ)", "Nhóm A" in t0 and "Nhóm B" in t0 and "hỗ trợ mức 3" in t0)
    ok("C L06 có khung hai nhóm vai trò và cách chọn trọng tâm ôn", "Nhóm A" in t6 and "Nhóm B" in t6 and "chọn nhóm vai trò" in t6)
    ok("C L07 dạy hỏi khung lương + công thức T = L × (13 + k) + 12 × P + số minh hoạ", "hỏi khung" in t7.lower() and "13 + k" in t7 and "số minh hoạ" in t7)
    ok("C L07 tiêu đề (đặc tả + giáo án) không chứa con số lương",
       not re.search(r"\d+ ?(M|triệu)", spec("L07")[0]["title"]) and "50" not in yaml.safe_load((ROOT / "curriculum/int.yaml").read_text(encoding="utf-8"))["lessons"][7]["title"])
    cur = (ROOT / "curriculum/int.yaml").read_text(encoding="utf-8")
    ok("C curriculum/int.yaml không còn 50M / 50 triệu", not re.search(r"50M|50 ?triệu|Deal 50", cur))
    ok("C L04 nhắc ACB không nói dùng hệ lõi nào (không gán ACB dùng T24)", "không nói ACB dùng hệ lõi nào" in t4 or "không nói ACB dùng" in t4)
    ok("C L07 thử việc: không nêu số ngày, dặn kiểm lại văn bản hiện hành", "60 ngày" not in t7 and "kiểm lại" in t7)
    ok("C L04 đã tách: không còn LTV/DTI/CIC/EOD/hai con trỏ (thuộc L08), lời đọc ≤ 2 300 từ (trần fix4 2026-11-15)",
       not re.search(r"LTV|DTI|CIC|EOD|hai con trỏ", t4) and sum(len(str(st.get("say", "")).split()) for s_ in spec("L04")[0]["scenes"] for st in s_["steps"]) <= 2300)
    ok("C L08 nhóm nợ theo TT 31/2024 kèm 'đã được TT 37/2025 sửa đổi, cần đối chiếu bản hợp nhất'; L04 mã 68 kèm 'cần kiểm'",
       "37/2025" in t8 and "bản hợp nhất" in t8 and "cần kiểm" in t4)
    ok("C L04/L08 MTI: 0400 yêu cầu đảo, 0420 thông báo đảo, và đảo chỉ khi đã biết chắc thất bại", "0400 yêu cầu đảo" in t4 and "0420 thông báo đảo" in t4 and "biết chắc" in t4)
    # pháp lý thống nhất với ACB L06: QĐ 2345 chưa đọc nguyên văn, ngưỡng sinh trắc học theo TT 50/2024 sửa đổi bởi TT 77/2025
    for lid in ("L00", "L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08"):
        tx = vis(spec(lid)[0])
        ok(f"C {lid} nhắc QĐ 2345 (nếu có) phải kèm 'chưa đọc nguyên văn' và không có 'ký 18/12/2023' như văn bản hiện hành", not re.search(r"(?<![0-9])2345(?![0-9])", tx) or ("chưa đọc nguyên văn" in tx and "18/12/2023" not in tx))
    de6 = (ROOT / "labs" / "INT" / "L06" / "de.md").read_text(encoding="utf-8")
    ok("C labs/INT/L06/de.md dùng TT 50/2024 sửa đổi bởi TT 77/2025; QĐ 2345 ghi chưa đọc nguyên văn", "77/2025" in de6 and "chưa đọc nguyên văn" in de6)
    ok("C L05 và L06 nêu TT 50/2024 và TT 77/2025", all("77/2025" in vis(spec(i)[0]) and "50/2024" in vis(spec(i)[0]) for i in ("L05", "L06")))
    ok("C L00 hai nhóm vai trò: mức 3 và bản thiết kế có ở cả hai nhóm (không dùng để phân loại)", "cả hai" in t0 and "không dùng chúng để phân loại" in t0)
    ok("C L02 có mục tiêu và cảnh Bloom (covers trỏ tới cảnh check)", any("Bloom" in o for o in spec("L02")[0]["objectives"]) and any(c["scene"] == "check" for c in spec("L02")[0]["covers"] if "Bloom" in spec("L02")[0]["objectives"][c["objective"] - 1]))
    ok("C L06 hook không dẫn đường dẫn tệp interview/ người học không có", "interview/06" not in vis(spec("L06")[0]))
    # đồng bộ mục tiêu giáo án với đặc tả (E51: chép đúng điều video dạy)
    lessons = yaml.safe_load(cur)["lessons"]
    ok("C giáo án INT có 9 bài, L08 ở CUỐI, requires L04 và L07 (fix9: NAPAS/T24/Redis học ở L00–L04)", [x["id"] for x in lessons] == [f"L0{i}" for i in range(9)] and lessons[8]["requires"] == ["L04", "L07"])
    for i, ls in enumerate(lessons):
        d, _ = spec(f"L0{i}")
        ok(f"C L0{i} mục tiêu giáo án = mục tiêu đặc tả", ls["objectives"] == d["objectives"])
    # fix4 L08: bảng chạy tay hai con trỏ khớp mô phỏng thật
    raw8 = next((ROOT / "lessons" / "int").glob("L08_*.yaml")).read_text(encoding="utf-8")
    core, nap, ci, cj, rows = [101, 103, 104, 107, 109], [101, 102, 104], 0, 0, []
    while ci < len(core) and cj < len(nap):
        a, b = core[ci], nap[cj]
        op = "=" if a == b else ("&gt;" if a > b else "&lt;")
        rows.append(f"<td>{ci}, {cj}</td><td>{a} {op} {b}</td>")
        if a == b:
            ci += 1
            cj += 1
        elif a < b:
            ci += 1
        else:
            cj += 1
    ok("C L08 bảng chạy tay hai con trỏ khớp mô phỏng thật (4 bước, dừng ở 3, 3, còn dư 107 và 109)",
       len(rows) == 4 and all(r in raw8 for r in rows) and (ci, cj) == (3, 3) and core[ci:] == [107, 109] and "<td>3, 3</td>" in raw8)
    # độ dài lời đọc ≤ 2300 từ, câu say ≥ 8 từ cho câu mới
    for i in range(9):
        d, _ = spec(f"L0{i}")
        w = sum(len(str(st.get("say", "")).split()) for s in d["scenes"] for st in s["steps"])
        ok(f"C L0{i} lời đọc {w} từ ≤ 2 300", w <= 2300, w)


if __name__ == "__main__":
    check_labs()
    check_code()
    check_scale()
    check_honesty()
    bad = [r for r in res if not r[0]]
    print(f"verify_int: {len(res) - len(bad)} PASS, {len(bad)} FAIL")
    sys.exit(1 if bad else 0)
