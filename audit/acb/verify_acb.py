"""verify_acb.py — kiểm số, mã và đầu ra THẬT cho khoá ACB (Phỏng vấn Kỹ sư Tích hợp ACB), chuẩn AF2 (WP4, 2026-11-14).

ACB không có bộ sinh: YAML trong lessons/acb/ là nguồn. Bộ kiểm này làm bốn việc:
  1. mỗi khối mã Python HIỆN TRÊN MÀN HÌNH ở cảnh `code` được ghép NGUYÊN VĂN từ trên xuống rồi chạy thật; đầu ra thật phải bằng các khối
     "Kết quả khi chạy" hiện trên màn hình (ví dụ minh hoạ T24, NAPAS, CIC, HSM, Oracle, Kafka không chạy được trên máy: mã chỉ là MÔ PHỎNG
     bằng Python, sqlite3, hashlib, hmac, heapq thật, bài ghi rõ "mô phỏng" — không bịa đầu ra của sản phẩm thật);
  2. mỗi lab labs/ACB/Lxx/loi_giai.py chạy ra đúng mong_doi.txt (lab_gate.py còn chạy lại qua labs/cham.sh);
  3. mỗi con số ví dụ và quy mô (×1, ×100, ×10 000) của bài được tính lại độc lập bằng hàm riêng của bộ kiểm này;
  4. số liệu của lab KHÁC số của ví dụ trong bài (người học không chép lại được).
Chạy: .venv/Scripts/python -B audit/acb/verify_acb.py [L00 L01 …]   (không đối số = mọi bài). Mã thoát 1 nếu có FAIL.
Đầu vào luôn là số minh hoạ; không có số đo của ngân hàng nào."""
import hashlib
import hmac
import heapq
import html
import math
import re
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
LESSONS = ROOT / "lessons" / "acb"
LABS = ROOT / "labs" / "ACB"
PY = sys.executable
FAILS = []
N = 0


def ok(name, cond, detail=""):
    global N
    N += 1
    if not cond:
        FAILS.append(name)
        print(f"FAIL {name} {detail}")


# ---------------------------------------------------------------- hạ tầng
def code_blocks(show):
    """Khối mã trên màn hình: <div class="code"><div>dòng</div>…</div> (cùng cách audit/review/screen_code.py)."""
    out = []
    for m in re.finditer(r'<div class="code">((?:<div>.*?</div>)+)</div>', show, re.S):
        lines = re.findall(r"<div>(.*?)</div>", m.group(1), re.S)
        out.append("\n".join(html.unescape(re.sub(r"<[^>]+>", "", x)).rstrip() for x in lines))
    return out


def load(lid):
    p = next(LESSONS.glob(f"{lid}_*.yaml"))
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def scene(lid, sid):
    return next(s for s in load(lid)["scenes"] if s["id"] == sid)


def run_py(code, timeout=60):
    with tempfile.TemporaryDirectory() as t:
        f = Path(t) / "chay.py"
        f.write_text(code + "\n", encoding="utf-8")
        p = subprocess.run([PY, "-B", str(f)], capture_output=True, text=True, encoding="utf-8", timeout=timeout, cwd=t)
    return p.returncode, p.stdout.rstrip("\n"), p.stderr


def check_screen(lid, sid="code"):
    """Ghép các khối mã của cảnh từ trên xuống (mỗi step có ≥ 2 khối thì khối cuối là đầu ra, khối đầu là mã; step 1 khối là mã tiếp nối).
    Tại mỗi step có đầu ra: chạy chương trình ghép tới step đó; đầu ra thật phải bằng các khối kết quả đã hiện tới đó."""
    sc = scene(lid, sid)
    codes, outs, n_run = [], [], 0
    for i, st in enumerate(sc["steps"]):
        bl = code_blocks(str(st.get("show", "")))
        if not bl:
            continue
        codes.append(bl[0])
        if len(bl) >= 2:
            outs.append(bl[-1])
            rc, out, err = run_py("\n\n".join(codes))
            ok(f"{lid}.{sid}[{i}]: mã trên màn hình (ghép từ trên xuống) chạy được", rc == 0, err[-400:])
            want = "\n".join(outs)
            ok(f"{lid}.{sid}[{i}]: đầu ra hiện trên màn hình = đầu ra thật", out == want, f"\n--- thật:\n{out}\n--- hiện:\n{want}")
            n_run += 1
    ok(f"{lid}.{sid}: có khối mã chạy thật trên màn hình", n_run >= 1)
    return "\n\n".join(codes)


def check_de_format(lid, exp):
    """Định dạng dòng ghi trong de.md phải khớp mong_doi.txt (lỗi M2 của ACB L08: de.md ghi 'giai ngan lan 1: chi tien' còn mong_doi là
    'giai ngan lan 1 chi tien'). Với mỗi đoạn `…` trong de.md không có ô trống (< >, …) và có ≥ 3 từ ASCII thường: nếu 4 từ đầu (bỏ dấu : , .) trùng bốn từ đầu
    của một dòng mong đợi thì cả đoạn phải là một phần của dòng đó. Ngoài ra mọi dòng mong đợi dạng 'nhãn: giá trị' phải có nhãn nguyên văn trong de.md."""
    de = (LABS / lid / "de.md").read_text(encoding="utf-8")
    lines = exp.splitlines()
    bad = []
    for span in re.findall(r"`([^`\n]+)`", de):
        if any(c in span for c in "<>…") or not re.fullmatch(r"[a-z0-9 ,:.%_()=/+\-]+", span):
            continue
        w = span.split()
        if len(w) < 3:
            continue
        for ln in lines:
            norm = lambda ws: [x.strip(":,.") for x in ws[:4]]
            if norm(ln.split()) == norm(w) and span not in ln:
                bad.append((span, ln))
    ok(f"{lid} lab: định dạng trong de.md khớp mong_doi.txt", not bad, bad)
    labels = []
    for ln in lines:
        m = re.match(r"([a-z0-9 ()%.\-]+?): ", ln)
        if m and len(m.group(1).split()) >= 2 and not m.group(1)[0].isdigit():
            labels.append(m.group(1))
    miss = [x for x in labels if x not in de and x.replace(" ", "") not in de.replace(" ", "")]
    ok(f"{lid} lab: nhãn 'nhãn: giá trị' của mong_doi.txt có trong de.md", not miss, miss)


def check_lab(lid):
    d = LABS / lid
    sol = d / "loi_giai.py"
    exp = (d / "mong_doi.txt").read_text(encoding="utf-8").rstrip("\n")
    ok(f"{lid} lab: có de.md và mong_doi.txt", (d / "de.md").exists() and bool(exp))
    check_de_format(lid, exp)
    if sol.exists():
        rc, out, err = run_py(sol.read_text(encoding="utf-8"))
        ok(f"{lid} lab: lời giải chạy được", rc == 0, err[-300:])
        ok(f"{lid} lab: lời giải cho đúng mong_doi.txt", out == exp, f"\n--- thật:\n{out}\n--- mong đợi:\n{exp}")
    else:
        ok(f"{lid} lab: có loi_giai.md (giấy bút)", (d / "loi_giai.md").exists())
    return exp


def lab_scene_has_expected(lid, exp):
    """mọi dòng của mong_doi.txt hiện trên màn hình cảnh practice (lint E53 cũng kiểm)"""
    sc = scene(lid, "practice")
    blocks = [b for st in sc["steps"] for b in code_blocks(str(st.get("show", "")))]
    ok(f"{lid} practice: kết quả mong đợi hiện nguyên văn trên màn hình", exp in blocks)


# ---------------------------------------------------------------- tính độc lập (không chép số từ bài)
def little(n, ms):
    return n * ms / 1000


def ceil_div(a, b):
    return -(-a // b)


def bando(truong):
    bits = 0
    for n in truong:
        bits |= 1 << (64 - n)
    return format(bits, "016X")


# ---------------------------------------------------------------- L00
def l00():
    tps = 10000
    ok("L00 phút/giờ", tps * 60 == 600000 and tps * 3600 == 36000000)
    ok("L00 toàn trình 120+35 < 200", 120 + 35 == 155 < 200)
    ok("L00 TTL 60 s = 60 000 ms", 60 * 1000 == 60000)
    for k, gio, bay, khoa in ((1, 360000, 15.5, 6000), (100, 36000000, 1550, 600000), (10000, 3600000000, 155000, 60000000)):
        n = 100 * k
        ok(f"L00 quy mô ×{k}", n * 3600 == gio and abs(little(n, 155) - bay) < 1e-6 and n * 60 == khoa)
    ok("L00 bồi hoàn 1 000 000 - 500 000 + 500 000", 1000000 - 500000 + 500000 == 1000000)
    ok("L00 lương năm 13/14/17 tháng (L = 40 là số minh hoạ, không còn 50 triệu gross)", 40 * 13 == 520 and 40 * (13 + 1) == 560 and 40 * (13 + 4) == 680 and "50 triệu gross" not in open(ROOT / "lessons/acb/L00_phong_van_tich_hop_acb.yaml", encoding="utf-8").read())
    ok("L00 lab khác ví dụ", 4000 != tps and 90 + 40 != 155 and 2 * 45 != 60)
    ok("L00 lab: 4000×60, ×60, 130 ms, 90 s", 4000 * 60 == 240000 and 240000 * 60 == 14400000 and 90 + 40 == 130 and 2 * 45 * 1000 == 90000)
    check_screen("L00")
    lab_scene_has_expected("L00", check_lab("L00"))


# ---------------------------------------------------------------- L01
def l01():
    ok("L01 ví dụ: 175 đang chờ, 28 lệnh/kết nối, 179 kết nối", little(5000, 35) == 175 and 1000 // 35 == 28 and ceil_div(5000, 28) == 179)
    for n, bay, kn in ((50, 1.75, 2), (5000, 175, 179), (500000, 17500, 17858)):
        ok(f"L01 quy mô lệnh/giây {n}", abs(little(n, 35) - bay) < 1e-9 and ceil_div(n, 28) == kn)
    ok("L01 hàng đợi ứ: 1 000/giây, 60 s → 60 000, chờ 15 s", 5000 - 4000 == 1000 and 1000 * 60 == 60000 and 60000 / 4000 == 15 and 1000 * 10 / 4000 == 2.5)
    ok("L01 lab khác ví dụ", (2000, 45) != (5000, 35))
    ok("L01 lab: 90 đang chờ, 22 lệnh/kết nối, 91 kết nối", little(2000, 45) == 90 and 1000 // 45 == 22 and ceil_div(2000, 22) == 91)
    check_screen("L01")
    lab_scene_has_expected("L01", check_lab("L01"))


# ---------------------------------------------------------------- L02
def l02():
    ok("L02 bản đồ bit {3,4,11,37}", bando([3, 4, 11, 37]) == "3020000008000000")
    ok("L02 bản đồ bit {2,3,4,7} = 0x72…", bando([2, 3, 4, 7]) == "7200000000000000" and 0x72 == 0b01110010)
    ok("L02 trường 1 = 'có bản đồ thứ hai' (0xF2)", [i + 1 for i in range(8) if (0xF2 >> (7 - i)) & 1] == [1, 2, 3, 4, 7])
    ok("L02 ví dụ: 960 đang chờ, đỉnh 12 000", little(8000, 120) == 960 and 8000 * 15 // 10 == 12000 and 60 * 1000 == 60000)
    for n, bay, dinh, khoa in ((80, 9.6, 120, 4800), (8000, 960, 12000, 480000), (800000, 96000, 1200000, 48000000)):
        ok(f"L02 quy mô {n}", abs(little(n, 120) - bay) < 1e-9 and n * 15 // 10 == dinh and n * 60 == khoa)
    # khoá có hạn: ttl 60, lệnh ở 0, 20, 61
    ket = {}

    def dat(k, t, ttl):
        if k in ket and ket[k] > t:
            return False
        ket[k] = t + ttl
        return True
    ok("L02 khoá 60 s: 0 → True, 20 → False, 61 → True", [dat("k", 0, 60), dat("k", 20, 60), dat("k", 61, 60)] == [True, False, True])
    ok("L02 lab khác ví dụ", [3, 4, 11, 37, 41] != [3, 4, 11, 37] and 80 != 60 and 2400 != 8000)
    ok("L02 lab: bitmap A, B, giải mã, 360", bando([3, 4, 11, 37, 41]) == "3020000008800000" and bando([1, 3, 4, 11, 37]) == "B020000008000000" and bando([64]) == "0000000000000001"
       and [n for n in range(1, 65) if int("5030000000000000", 16) >> (64 - n) & 1] == [2, 4, 11, 12] and 2400 * 150 // 1000 == 360)
    check_screen("L02")
    lab_scene_has_expected("L02", check_lab("L02"))


# ---------------------------------------------------------------- L03
def kenh(co_app, tien):
    if co_app:
        return "OTT_PUSH"
    return "SMS_BRANDNAME" if tien >= 50000 else "EMAIL"


def l03():
    ok("L03 chọn kênh bốn ca", [kenh(*x) for x in [(True, 20000), (False, 80000), (False, 30000), (None, 80000)]] == ["OTT_PUSH", "SMS_BRANDNAME", "EMAIL", "SMS_BRANDNAME"])
    h = []
    for it in [(2, "quang cao"), (1, "ma OTP"), (2, "tin thuong")]:
        heapq.heappush(h, it)
    ok("L03 hàng đợi ưu tiên: OTP ra trước", [heapq.heappop(h) for _ in range(3)] == [(1, "ma OTP"), (2, "quang cao"), (2, "tin thuong")])
    ok("L03 ví dụ: 833/giây, 70% = 35 000, còn 15 000, khoá 24 giờ", 50000 // 60 == 833 and 50000 * 70 // 100 == 35000 and 50000 - 35000 == 15000 and 86400 // 3600 == 24)
    for pm, ps_txt, tt, khoa in ((500, "8.3", 1, 720000), (50000, "833", 2, 72000000), (5000000, "83333", 167, 7200000000)):
        ps_ok = (f"{pm / 60:.1f}" == ps_txt) if pm == 500 else (str(int(pm / 60)) == ps_txt)
        ok(f"L03 quy mô {pm}/phút", ps_ok and math.ceil(pm / 60 / 500) == tt and pm * 60 * 24 == khoa)
    ok("L03 tiến trình ×10 000 = 167", math.ceil(5000000 / 60 / 500) == 167 and math.ceil(50000 / 60 / 500) == 2 and math.ceil(500 / 60 / 500) == 1)
    ok("L03 khoá 1 giờ ở ×10 000 = 300 triệu", 5000000 * 60 == 300000000)
    # xô thẻ (lab): 3 thẻ, +1/giây, bảy tin ở 0,0,0,0,1,1,2
    the, cuoi, kq = 3, 0, []
    for t in [0, 0, 0, 0, 1, 1, 2]:
        the = min(3, the + (t - cuoi))
        cuoi = t
        if the >= 1:
            the -= 1
            kq.append("gui")
        else:
            kq.append("tu_choi")
    ok("L03 lab: xô thẻ gui×3, tu_choi, gui, tu_choi, gui", kq == ["gui", "gui", "gui", "tu_choi", "gui", "tu_choi", "gui"])
    ok("L03 lab: miễn cước 58 500, tính cước tối đa 31 500", 90000 * 65 // 100 == 58500 and 90000 - 58500 == 31500)
    check_screen("L03")
    lab_scene_has_expected("L03", check_lab("L03"))


# ---------------------------------------------------------------- L04
def l04():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE so (id INT, ver INT)")
    db.execute("INSERT INTO so VALUES (1, 7)")
    sql = "UPDATE so SET ver = ver + 1 WHERE id = 1 AND ver = ?"
    ok("L04 khoá lạc quan: 1 rồi 0 dòng tác động, ver 8", [db.execute(sql, (7,)).rowcount, db.execute(sql, (7,)).rowcount] == [1, 0] and db.execute("SELECT ver FROM so").fetchone()[0] == 8)
    ok("L04 ví dụ prereq: lãi 35 triệu, rút sớm 458 904, mất ≈ 34,5 triệu", 500 * 7 // 100 == 35 and round(500000000 * 0.001 * 335 / 365) == 458904 and round((35000000 - 458904) / 1e6, 1) == 34.5)
    for n, thua, cho in ((2, 1, 0.02), (200, 199, 3.98), (20000, 19999, 399.98)):
        ok(f"L04 quy mô {n} người mua", n - 1 == thua and round((n - 1) * 0.02, 2) == cho)
    ok("L04 lab khác ví dụ", (3, 300000000, 200) != (7, 500000000, 335))
    ok("L04 lab: lãi dự kiến, lãi sớm, mất", 300000000 * 68 // 1000 == 20400000 and round(300000000 * 200 / 365000) == 164384 and 20400000 - 164384 == 20235616)
    check_screen("L04")
    lab_scene_has_expected("L04", check_lab("L04"))


# ---------------------------------------------------------------- L05
def lay_khoa(lich):
    khoa, cho = {}, {}
    for ai, tk in lich:
        giu = khoa.get(tk, ai)
        if giu != ai:
            cho[ai] = giu
        else:
            khoa[tk] = ai
    return cho


def l05():
    ok("L05 vòng chờ khi xin ngược thứ tự", lay_khoa([("A", 1), ("B", 2), ("A", 2), ("B", 1)]) == {"A": "B", "B": "A"})
    ok("L05 không vòng chờ khi cùng thứ tự", lay_khoa([("A", 1), ("B", 1), ("A", 2)]) == {"B": "A"})
    dau, sd = [], 10
    for p in [5, -3, 2, -1]:
        dau.append(sd)
        sd += p
    ok("L05 số dư đầu đoạn [10, 15, 12, 14], cuối 13", dau == [10, 15, 12, 14] and sd == 13)
    ok("L05 ví dụ: 150 tỉ, 1 000 lệnh/khối, 7+7+7+9 = 30", 10000 * 15000000 == 150000000000 and 10000 // 10 == 1000 and 7 + 7 + 7 + 9 == 30)
    for n, tt, khoi, moi in ((100, 0.5, 1, 0.5), (10000, 50, 10, 5), (1000000, 5000, 100, 50)):
        ok(f"L05 chi lương {n} lệnh", n * 5 / 1000 == tt and (n // khoi) * 5 / 1000 == moi)
    for n, tt, doan, moi in ((10000, 0.1, 1, 0.1), (1000000, 10, 4, 2.5), (100000000, 1000, 100, 10)):
        ok(f"L05 sao kê {n} bản ghi", n / 100000 == tt and tt / doan == moi)
    # chia 30 ngày thành 7+7+7+9: đoạn 9 ngày có n*9/30 bản ghi nên chậm nhất = 3,0 giây (không phải 2,5 giây của chia đều số bản ghi)
    ok("L05 sao kê ×100: đoạn 9 ngày 300 000 bản ghi = 3,0 giây; chia đều số bản ghi mới 2,5 giây", 1000000 * 9 // 30 == 300000 and 300000 / 100000 == 3.0 and 1000000 / 4 / 100000 == 2.5)
    l05 = (LESSONS / next(LESSONS.glob("L05_*.yaml")).name).read_text(encoding="utf-8")
    ok("L05 màn hình không còn 'xong trong khoảng 2,5 giây' cho chia 7+7+7+9 ngày", "xong trong khoảng $2{,}5$ giây" not in l05 and "hai giây rưỡi như ví dụ" not in l05)
    ok("L05 lab khác ví dụ", ([7, 3], [3, 7]) != ([1, 2], [2, 1]))
    goc, sap = {"A": [7, 3], "B": [3, 7]}, {"A": [3, 7], "B": [3, 7]}
    lich = lambda m: [("A", m["A"][0]), ("B", m["B"][0]), ("A", m["A"][1]), ("B", m["B"][1])]
    cv = lambda c: c.get("A") == "B" and c.get("B") == "A"
    ok("L05 lab: có vòng khi không sắp, không vòng khi sắp", cv(lay_khoa(lich(goc))) and not cv(lay_khoa(lich(sap))))
    d2, s2 = [], 20
    for p in [4, -6, 3, -2, 5]:
        d2.append(s2)
        s2 += p
    ok("L05 lab: đầu đoạn [20, 24, 18, 21, 19], cuối 24; 5 khối", d2 == [20, 24, 18, 21, 19] and s2 == 24 and ceil_div(2500, 500) == 5)
    check_screen("L05")
    lab_scene_has_expected("L05", check_lab("L05"))


# ---------------------------------------------------------------- L06
def can_quet(tien, tong):
    return tien > 10 or tong + tien > 20


def l06():
    tong, kq = 0, []
    for t in [8, 8, 8, 4]:
        q = can_quet(t, tong)
        tong = 0 if q else tong + t
        kq.append((q, tong))
    ok("L06 ngưỡng: 8,8,8,4 → thường, thường, quét, thường (tổng 8, 16, 0, 4)", kq == [(False, 8), (False, 16), (True, 0), (False, 4)])
    ok("L06 ví dụ: 8 + 14 = 22; 9 + 8 + 6 = 23", 8 + 14 == 22 > 20 and 9 + 8 == 17 and 9 + 8 + 6 == 23 > 20)
    for lan, bay, ve in ((5, 1.5, 900), (500, 150, 90000), (50000, 15000, 9000000)):
        ok(f"L06 quy mô {lan} lượt/giây", abs(lan * 0.3 - bay) < 1e-9 and lan * 180 == ve)
    ok("L06 vé hạn 60 s ở ×10 000 = 3 000 000", 50000 * 60 == 3000000)
    # kiểm vé: ba cổng (ký, hết hạn, đã dùng)
    KHOA = b"k"
    ky = lambda nd: hmac.new(KHOA, nd.encode(), hashlib.sha256).hexdigest()[:8]
    ve = {"id": "b1", "het_han": 180}
    ve["ky"] = ky("b1|50|180")
    da = set()

    def kiem(tien, now):
        if ve["ky"] != ky(ve["id"] + "|" + str(tien) + "|" + str(ve["het_han"])):
            return "ky"
        if now > ve["het_han"]:
            return "het han"
        if ve["id"] in da:
            return "da dung"
        da.add(ve["id"])
        return "ok"
    ok("L06 vé: ok, đã dùng, ký sai, hết hạn", [kiem(50, 100), kiem(50, 120), kiem(60, 100), kiem(50, 200)] == ["ok", "da dung", "ky", "het han"])
    ok("L06 lab khác ví dụ", [6, 7, 9, 15, 3] != [8, 8, 8, 4])
    t2, k2 = 0, []
    for t in [6, 7, 9, 15, 3]:
        q = can_quet(t, t2)
        t2 = 0 if q else t2 + t
        k2.append((q, t2))
    ok("L06 lab: 6,7,9,15,3 → (T,13?)", k2 == [(False, 6), (False, 13), (True, 0), (True, 0), (False, 3)])
    check_screen("L06")
    lab_scene_has_expected("L06", check_lab("L06"))
    # pháp lý: bài không nêu số điều của Quyết định 2345; mọi văn bản dẫn có hiệu lực/chú thích trong sổ
    txt = (LESSONS / next(LESSONS.glob("L06_*.yaml")).name).read_text(encoding="utf-8")
    ok("L06 nêu 'chưa đọc nguyên văn' cho Quyết định 2345", "chưa đọc nguyên văn" in txt)
    ok("L06 không nêu số điều của Quyết định 2345", not re.search(r"Điều\s+\d+", txt))


# ---------------------------------------------------------------- L07
def l07():
    ky = lambda khoa, nd: hmac.new(khoa, nd.encode(), hashlib.sha256).hexdigest()[:12]
    goi = '{"va": "888800123456", "tien": 1000000}'
    ok("L07 HMAC: nguyên vẹn khớp, sửa số tiền lệch", ky(b"k", goi) == ky(b"k", goi) and ky(b"k", goi) != ky(b"k", goi.replace("1000000", "9000000")))
    xl, kq = set(), []
    for m in ["evt_1", "evt_1"]:
        kq.append("bo qua" if m in xl else "gach no")
        xl.add(m)
    ok("L07 webhook gửi lại: gạch nợ một lần", kq == ["gach no", "bo qua"])
    a, b, i, j, thieu = [1, 2, 4], [1, 2, 3, 4], 0, 0, []
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i, j = i + 1, j + 1
        elif a[i] < b[j]:
            thieu.append(("A", a[i])); i += 1
        else:
            thieu.append(("B", b[j])); j += 1
    ok("L07 hai con trỏ: chỉ mã 3 có ở B, không còn phần dư", thieu == [("B", 3)] and a[i:] == [] and b[j:] == [])
    ok("L07 ví dụ prereq: VA 4 + 8 = 12 chữ số", len("8888" + "00123456") == 12)
    ok("L07 log2: N log2 N cho 300, 30 000, 3 000 000", [round(n * math.log2(n)) for n in (300, 30000, 3000000)] == [2469, 446180, 64549593])
    # tốc độ so sánh THỐNG NHẤT 1e9 phép/giây (1 tỉ, như INT L04/L08): 3 triệu² / 1e9 = 9 000 giây = 2,5 giờ
    for n, nest, t_nest, t_sort in ((300, 90000, 0.00009, 0.0000025), (30000, 900000000, 0.9, 0.00045), (3000000, 9 * 10 ** 12, 9000, 0.065)):
        ok(f"L07 quy mô N={n}", n * n == nest and abs(nest / 1e9 - t_nest) < 1e-12 and round(n * math.log2(n) / 1e9, 7 if n == 300 else 5 if n == 30000 else 3) == t_sort)
    ok("L07 9 000 giây = 2,5 giờ", 9000 / 3600 == 2.5)
    l07t = next(LESSONS.glob("L07_*.yaml")).read_text(encoding="utf-8")
    ok("L07 màn hình không còn giả định 10^8 phép/giây hay '25 giờ'", "10^8" not in l07t and "10⁸" not in l07t and "25 giờ" not in l07t and "90 nghìn giây" not in l07t)
    ok("L07 lab khác ví dụ", ["e1", "e2", "e1", "e3", "e2"] != ["evt_1", "evt_1"])
    core, napas, erp = [10, 11, 13, 15], [10, 11, 12, 13, 15, 16], [10, 13, 16]
    pl = {}
    for ma in sorted(set(core) | set(napas) | set(erp)):
        c, n, e = ma in core, ma in napas, ma in erp
        pl[ma] = "ALL" if c and n and e else "ROT" if c and n else "TREO" if n and not c and not e else "NAPAS" if c and not n else "LA"
    ok("L07 lab: phân loại 10 khớp, 11 rớt webhook, 12 treo, 13 khớp, 15 rớt, 16 bất thường", pl == {10: "ALL", 11: "ROT", 12: "TREO", 13: "ALL", 15: "ROT", 16: "LA"})
    check_screen("L07")
    lab_scene_has_expected("L07", check_lab("L07"))


# ---------------------------------------------------------------- L08
def l08():
    ok("L08 ví dụ: hạn mức 85 triệu, lãi suất 8,5%, lãi 30 ngày 349 315", 100000000 * 85 // 100 == 85000000 and 6.0 + 2.5 == 8.5 and round(50000000 * 8.5 / 100 * 30 / 365) == 349315)
    ok("L08 prereq: 90% × 100 triệu = 90 triệu, vượt 85 triệu 5 triệu", 100000000 * 90 // 100 == 90000000 and 90000000 - 85000000 == 5000000)
    for h, cic, trung, loss in ((100, 100 / 3600, 0.1, 5e6), (10000, 10000 / 3600, 10, 5e8), (1000000, 1000000 / 3600, 1000, 5e10)):
        ok(f"L08 quy mô {h} hồ sơ/giờ", abs(h * 0.001 - trung) < 1e-9 and abs(trung * 50e6 - loss) < 1e-3 and round(cic, 2 if h == 100 else 1 if h == 10000 else 0) == {100: 0.03, 10000: 2.8, 1000000: 278}[h])
    ok("L08 nhóm 2 = quá hạn 10–90 ngày (9 ngày vẫn nhóm 1)", 9 < 10 <= 90 < 91)
    # hai pha và giải ngân lũy đẳng
    def pha(k, c):
        if not k:
            return ["khoa so loi: dung"]
        return ["khoa so"] + (["cap han muc"] if c else ["cap han muc loi: nha khoa so"])
    ok("L08 hai pha: ba nhánh", pha(True, True) == ["khoa so", "cap han muc"] and pha(True, False) == ["khoa so", "cap han muc loi: nha khoa so"] and pha(False, True) == ["khoa so loi: dung"])
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE g (khoa TEXT PRIMARY KEY, tien INT)")
    kq = []
    for _ in range(2):
        try:
            db.execute("INSERT INTO g VALUES ('K1', 1)")
            kq.append("chi")
        except sqlite3.IntegrityError:
            kq.append("trung")
    ok("L08 khoá chính chặn giải ngân lần hai", kq == ["chi", "trung"])
    ok("L08 lab khác ví dụ", (240000000, 80, 4.8, 2.7, 120000000, 45) != (100000000, 85, 6.0, 2.5, 50000000, 30))
    ok("L08 lab: hạn mức 192 triệu, lãi suất 7,5, lãi 45 ngày 1 109 589", 240000000 * 80 // 100 == 192000000 and round(4.8 + 2.7, 1) == 7.5 and round(120000000 * 7.5 / 100 * 45 / 365) == 1109589)
    check_screen("L08")
    lab_scene_has_expected("L08", check_lab("L08"))
    txt = next(LESSONS.glob("L08_*.yaml")).read_text(encoding="utf-8")
    ok("L08 không dẫn văn bản chưa đọc nguyên văn (23/2025/NĐ-CP, 14/2017/TT-NHNN) như nguồn sự thật", "23/2025/NĐ-CP" not in txt and "14/2017/TT-NHNN" not in txt)


FUNCS = {"L00": l00, "L01": l01, "L02": l02, "L03": l03, "L04": l04, "L05": l05, "L06": l06, "L07": l07, "L08": l08}


def common():
    """kiểm chung mọi bài: khai af2 + covers; lời đọc ≤ 2 300 từ; không nêu tên ngân hàng khác làm nguồn; không hứa lương"""
    for lid in FUNCS:
        d = load(lid)
        ok(f"{lid} af2: true và có covers", d.get("af2") is True and len(d.get("covers") or []) >= len(d["objectives"]))
        words = sum(len(str(st.get("say", "")).split()) for sc in d["scenes"] for st in sc["steps"])
        ok(f"{lid} lời đọc ≤ 2 300 từ (đang {words})", words <= 2300)
        raw = next(LESSONS.glob(f"{lid}_*.yaml")).read_text(encoding="utf-8")
        ok(f"{lid} không hứa lương ('xứng đáng', 'tự tin chinh phục')", not re.search(r"xứng đáng|chinh phục mức|tự tin thương lượng", raw))
        ok(f"{lid} không dùng VPBank/MB làm nguồn sự thật", not re.search(r"VPBank|\bMB đăng", raw))


def fixes_r_int_acb():
    """Các sửa theo báo cáo người đọc R_INT_ACB (2026-11-14): kiểm trên chữ hiện trên màn hình + lời đọc + giáo án."""
    def whole(lid):
        d = load(lid)
        out = [str(d.get("title", "")), " ".join(map(str, d.get("objectives", [])))]
        for sc in d["scenes"]:
            out.append(str(sc.get("title", "")))
            for st in sc["steps"]:
                out.append(re.sub(r"<[^>]+>", " ", str(st.get("show", ""))))
                out.append(str(st.get("say", "")))
        return re.sub(r"\s+", " ", " ".join(out))
    t = {lid: whole(lid) for lid in FUNCS}
    cur = yaml.safe_load((ROOT / "curriculum" / "acb.yaml").read_text(encoding="utf-8"))["lessons"]
    for i, lid in enumerate(FUNCS):
        ok(f"{lid} mục tiêu giáo án = mục tiêu đặc tả (E51)", cur[i]["objectives"] == load(lid)["objectives"])
    # M1 / pháp lý: không còn 'Quyết định 2345' làm căn cứ chính trong tiêu đề, nhãn sơ đồ, recap; luôn kèm 'chưa đọc nguyên văn'
    d6 = load("L06")
    ok("L06 tiêu đề, nhãn sơ đồ, tên recap không còn 'Quyết định 2345'", "2345" not in d6["title"] and "2345" not in cur[6]["title"]
       and all("2345" not in (sc.get("title") or "") for sc in d6["scenes"])
       and all("2345" not in str(st.get("show", "")) or "chưa đọc nguyên văn" in str(st.get("show", "")) for sc in d6["scenes"] for st in sc["steps"]))
    ok("L06 quy tắc 'tổng về 0' ghi là giả định/ví dụ minh hoạ của mô phỏng", "giả định minh hoạ" in t["L06"] and "giả định của mô phỏng" in t["L06"])
    ok("không bài ACB nào còn 'năm mươi triệu gross'", all("năm mươi triệu gross" not in v for v in t.values()))
    # TT 31/2024: kèm nhắc TT 37/2025 sửa đổi; mục tiêu 5 L08 không gán chặn duyệt cho thông tư
    ok("L08 nhắc TT 37/2025 sửa đổi TT 31/2024 (cần đối chiếu bản hợp nhất)", t["L08"].count("37/2025") >= 2 and "đối chiếu bản hợp nhất" in t["L08"])
    reg = yaml.safe_load((ROOT / "audit" / "legal" / "registry.yaml").read_text(encoding="utf-8"))
    reg = reg.get("docs", reg) if isinstance(reg, dict) else reg
    ok("sổ pháp lý đã kiểm nguyên văn 37/2025/TT-NHNN", reg.get("37/2025/TT-NHNN", {}).get("status") == "HIEU_LUC" and reg.get("37/2025/TT-NHNN", {}).get("basis") == "ORIGINAL")
    o5 = load("L08")["objectives"][4]
    ok("L08 mục tiêu 5: thông tư chỉ định nghĩa nhóm nợ, chặn duyệt là chính sách ví dụ", "chính sách ví dụ" in o5 and "định nghĩa" in o5)
    ok("L00 quiz: '35 đến 40 triệu' gắn 'số minh hoạ'", "35 đến 40 triệu (số minh hoạ)" in t["L00"] and "một số minh hoạ" in t["L00"])
    ok("L00, L08: 'một số tin tuyển dụng' thay 'nhiều tin tuyển dụng'", "nhiều tin" not in t["L00"].lower() and "nhiều tin" not in t["L08"].lower())
    # L03: khử trùng NX đặt TRƯỚC khi gửi, xoá khi gửi lỗi, nêu rủi ro sập giữa chừng; không còn 'đặt sau khi nhà mạng xác nhận'
    ok("L03 khử trùng: NX đặt trước khi gửi, xoá khi lỗi, có rủi ro sập giữa chừng", "TRƯỚC khi gửi" in t["L03"] and "sập giữa lúc" in t["L03"]
       and "sau khi nhà mạng xác nhận" not in t["L03"])
    # L05: 7+7+7+9 ngày → đoạn 9 ngày 300 000 bản ghi → 3 giây (không phải 2,5)
    ok("L05 sao kê chia 7+7+7+9: 3 giây, không còn '2,5 giây' cho phép chia theo ngày", "300 nghìn bản ghi" in t["L05"] and "ba giây" in t["L05"] and "xong trong khoảng 2,5 giây" not in t["L05"])
    # L00/L02: nút nghẽn là thông lượng ghi
    ok("L00 và L02 nêu nút nghẽn là thông lượng ghi (không nói Redis không gánh nổi số khoá)", "thông lượng ghi" in t["L00"] and "thông lượng ghi" in t["L02"]
       and "không còn gánh nổi 60 triệu khoá" not in t["L00"] and "một cụm Redis không đủ" not in t["L02"])
    # MTI: 0400 yêu cầu đảo, 0420 thông báo đảo; thống nhất L00/L02
    for lid in ("L00", "L02"):
        ok(f"{lid} MTI: 0400 yêu cầu đảo, 0420 thông báo đảo, theo ISO 8583, đặc tả NAPAS cần kiểm", "0400" in t[lid] and "0420 là thông báo đảo" in t[lid] and "ISO 8583" in t[lid] and "cần kiểm" in t[lid])
    ok("L00 quiz: tra soát trước, đảo chỉ khi biết chắc thất bại", "tra soát trạng thái thật trước" in t["L00"] and "biết chắc giao dịch đã thất bại" in t["L00"])
    # L07: hai phân loại của lab hiện trên màn hình; giả định tốc độ 1e9
    ok("L07 màn hình có nhãn 'loi chuyen tien NAPAS, tra soat' và 'bat thuong'", "loi chuyen tien NAPAS, tra soat" in t["L07"] and "bat thuong" in t["L07"])
    ok("L04 không còn nhãn 'Fiber API Gateway'", "Fiber API Gateway" not in t["L04"])
    ok("L01 không còn 'Tuyệt đối không dùng chung một hàng đợi hai chiều'", "Tuyệt đối không dùng chung" not in t["L01"])
    ok("L00 mục tiêu 1 khớp màn hình về nguồn kiến trúc (OCB, không khẳng định là của ACB)", "kinh nghiệm làm ở OCB" in load("L00")["objectives"][0])
    ok("L00 hai nhóm vai trò: nói 'nghiêng về', nhóm kia cũng có hỗ trợ mức 3", "nghiêng về" in t["L00"] and "nhóm kia cũng có hỗ trợ mức 3" in t["L00"])


def fixes5():
    """Vòng 5 (2026-11-15), theo R3_INT_ACB: kiểm lại số/ý đã sửa bằng tính độc lập và kiểm chữ hiện trên màn hình + lời đọc."""
    def whole(lid):
        d = load(lid)
        out = [str(d.get("title", "")), " ".join(map(str, d.get("objectives", [])))]
        for sc in d["scenes"]:
            out.append(str(sc.get("title", "")))
            for st in sc["steps"]:
                out.append(re.sub(r"<[^>]+>", " ", str(st.get("show", ""))))
                out.append(str(st.get("say", "")))
        return re.sub(r"\s+", " ", " ".join(out))
    t = {lid: whole(lid) for lid in FUNCS}
    # L00: P99 không cộng được; mốc UIT; Squad Lending có nhãn chưa kiểm; lab không còn 'dat P99'
    ok("L00 không còn 'đạt P99' / 'dat P99' (P99 không cộng được từng đoạn)", "đạt P99" not in t["L00"] and "dat P99" not in t["L00"] and "P99 không cộng được" in t["L00"])
    lab = (LABS / "L00" / "loi_giai.py").read_text(encoding="utf-8") + (LABS / "L00" / "mong_doi.txt").read_text(encoding="utf-8")
    ok("L00 lab: đầu ra 'duoi 200', không còn 'P99'", "duoi 200" in lab and "P99" not in lab)
    ok("không bài ACB nào còn mốc 'tốt nghiệp 11/2026'", all("11/2026" not in v for v in t.values()) and "cuối năm 2026" in t["L00"])
    for lid, v in t.items():
        for m in re.finditer(r"Squad Lending", v):
            ctx = v[max(0, m.start() - 160): m.end() + 160]
            ok(f"{lid} 'Squad Lending' luôn kèm 'chưa kiểm' (tên nhóm lấy từ tin tuyển dụng, không phải chức danh thật)", "chưa kiểm" in ctx)
    # L01: không còn MV:SV và biểu thức sinh trong mã trên màn hình
    ok("L01 không còn 'MV:SV' và 'truong.items'", "MV:SV" not in t["L01"] and "truong.items" not in open(next(LESSONS.glob("L01_*.yaml")), encoding="utf-8").read())
    # L02: khử trùng lặp TRƯỚC giữ tiền (concept) và recap cùng thứ tự
    d2 = load("L02")
    sc2 = {s["id"]: s for s in d2["scenes"]}
    say = str(sc2["concept"]["steps"][0]["say"])
    ok("L02 concept: khử trùng lặp (bước hai) trước Core giữ tiền (bước ba)", say.index("khử trùng lặp trước tiên") < say.index("Core Banking giữ trước"))
    rec = re.sub(r"<[^>]+>", " ", str(sc2["recap"]["steps"][0]["show"]))
    ok("L02 recap: khử trùng lặp rồi giữ tiền", rec.index("khử trùng lặp") < rec.index("Giữ tiền"))
    # L03: ×100 cần 3 tiến trình ở đỉnh 1500/giây (ceil(1500/500)); ×10 000 cần 300 ở đỉnh gấp 1,8 lần trung bình
    tb100 = 50000 / 60
    dinh = 1500
    ok("L03 quy mô: trung bình 833 → 2 tiến trình, đỉnh 1500 → 3 tiến trình (ceil)", ceil_div(round(tb100), 500) == 2 and ceil_div(dinh, 500) == 3)
    ok("L03 quy mô ×10 000 ở đỉnh: 1500 × 100 = 150 000/giây → 300 tiến trình", ceil_div(dinh * 100, 500) == 300 and round(dinh / tb100, 2) == 1.8 and "300" in t["L03"])
    ok("L03 hook: thứ tự chỉ trong từng ngăn (phân vùng), không nói cả chủ đề", "theo đúng thứ tự trong từng chủ đề" not in t["L03"])
    # L04: 5 ms giữa hai yêu cầu (125 - 120), không còn '25 ms toàn bộ quy trình'
    ok("L04 hai yêu cầu cách nhau 5 ms (.125 - .120), không còn '25 mili giây' gán toàn quy trình", 125 - 120 == 5 and "25 mi li giây" not in t["L04"] and "25$ mili giây" not in t["L04"] and "$25$" not in t["L04"])
    # L05: 10 000 lệnh × 5 ms = 50 s (không phải 'hàng giờ'); 1e6 × 5 ms = 83 phút; sao kê chia theo ngày tối đa 30 đoạn ≈ 33,3 s
    ok("L05 tuần tự: 10 000 × 5 ms = 50 s, 1 000 000 × 5 ms = 83 phút", 10000 * 5 / 1000 == 50 and 1000000 * 5 / 1000 / 60 > 83 and "hơn một giờ" in t["L05"])
    ok("L05 sao kê ×10 000: chia đều 1e8/100/1e5 = 10 s; chia theo ngày ≤ 30 đoạn = 33,3 s", 1e8 / 100 / 1e5 == 10 and round(1e8 / 30 / 1e5, 1) == 33.3 and "33{,}3" in t["L05"] and "33 giây" in t["L05"])
    ok("L05 tiêu đề cảnh symbol không còn hứa 'Bulk Collect' (mã chỉ có FOR UPDATE)", all("Bulk Collect" not in str(s.get("title", "")) for s in load("L05")["scenes"] if s["id"] == "symbol"))
    ok("L05 mã khoá không còn khoa.get(tk, ai)", "khoa.get(tk, ai)" not in open(next(LESSONS.glob("L05_*.yaml")), encoding="utf-8").read().split("checks:")[0] + str(load("L05")["scenes"][5]))
    # L06: một câu hedge pháp lý thống nhất với INT (chưa đối chiếu nguyên văn; không nêu số điều/phụ lục; chưa kiểm biên trên/từ)
    ok("L06 hedge pháp lý: báo chí nêu; TT 50/2024 sửa bởi TT 77/2025 hoặc QĐ 2345; chưa đọc nguyên văn; chưa kiểm biên 'trên'/'từ'; không nêu số điều",
       all(k in t["L06"] for k in ("báo chí nêu", "Thông tư 77/2025", "Quyết định 2345", "chưa đọc nguyên văn", "chưa kiểm ranh giới trên hay từ", "không nêu số điều")))
    ok("L06 hạn vé 3 phút ghi 'ví dụ thiết kế'; có nhắc compare_digest; giải nghĩa VNeID và expires_at", "ví dụ thiết kế, không phải quy định" in t["L06"] and "compare_digest" in t["L06"]
       and "ứng dụng định danh điện tử" in t["L06"] and "số giây tính từ ngày 1/1/1970" in t["L06"])
    # L07: 0,065 s chỉ là phép so; 3·10^6·log2(3·10^6)/1e9; EOD, lũy đẳng giải nghĩa; compare_digest; LIKE chưa kiểm
    ok("L07 sắp xếp + trộn: 3e6 × log2(3e6) / 1e9 ≈ 0,065 s (chỉ phép so) và nói rõ chưa tính đọc/ghi", round(3e6 * math.log2(3e6) / 1e9, 3) == 0.065 and "chỉ tính phép so" in t["L07"] and "180 giây" in t["L07"])
    ok("L07 giải nghĩa EOD, lũy đẳng; nhắc compare_digest; 3 triệu = mọi đối tác; LIKE chưa kiểm", "End Of Day" in t["L07"] and "gửi lại bao nhiêu lần" in t["L07"] and "compare_digest" in t["L07"]
       and "mọi đối tác" in t["L07"] and "chưa kiểm" in t["L07"])
    # L08: luồng có bước Tra CIC qua mTLS và nhả khoá khi ký số lỗi; ctx, lũy đẳng giải nghĩa; tra CIC là trung bình
    ok("L08 luồng: Tra CIC (mTLS) → khoá sổ → ký số → mở hạn mức; ký số lỗi thì nhả khoá sổ", "1. Tra CIC" in t["L08"] and "mTLS" in t["L08"] and "Ký số lỗi hoặc hết hạn" in t["L08"] and "nhả khoá sổ" in t["L08"])
    ok("L08 giải nghĩa ctx và lũy đẳng; CIC/giây là số trung bình", "gói thông tin đi kèm mỗi lời gọi" in t["L08"] and "gửi lại bao nhiêu lần" in t["L08"] and "(trung bình)" in t["L08"] and "trung bình có hàng trăm lượt tra CIC" in t["L08"])
    ok("L08 tên lớp nhóm Squad Lending không còn trong tiêu đề bài và tên cảnh", all("Squad Lending" not in str(s.get("title", "")) for s in load("L08")["scenes"]) and "Squad Lending" not in load("L08")["title"])
    # L00 giải nghĩa 0200/0210, hai bốn bảy, TTL, OCB
    ok("L00 giải nghĩa 0200/0210, NAPAS 247 (24/7), TTL, OCB tại chỗ", "0200 là yêu cầu chuyển tiền, 0210 là phản hồi" in t["L00"] and "24 giờ mỗi ngày, 7 ngày mỗi tuần" in t["L00"]
       and "Thời gian sống (TTL)" in t["L00"] and "ngân hàng nơi bạn đang làm" in t["L00"])


def fixes6_l00_l02():
    """Sửa theo R4_ACB (2026-11-16) cho L00–L02: bảng 'Đọc trước' đúng số, cách chạy/chấm tệp, đối soát, số minh hoạ, đáp án quiz."""
    def whole(lid):
        d = load(lid)
        out = []
        for sc in d["scenes"]:
            out.append(str(sc.get("title", "")))
            for st in sc["steps"]:
                out.append(re.sub(r"<[^>]+>", " ", str(st.get("show", ""))))
                out.append(str(st.get("say", "")))
        return re.sub(r"\s+", " ", " ".join(out))
    t = {lid: whole(lid) for lid in ("L00", "L01", "L02")}
    # ví dụ trong bảng 'Đọc trước' (tính lại bằng Python thật)
    ok("L02 bảng: 1 << 3 = 8 = 0b1000; 0b0101 | 0b0010 = 0b0111; format(114, '04X') = '0072'; int('72', 16) = 114",
       (1 << 3) == 8 == 0b1000 and (0b0101 | 0b0010) == 0b0111 and format(114, "04X") == "0072" and int("72", 16) == 114
       and "<code>1 &lt;&lt; 3</code> là <code>1000</code> (nhị phân: chỉ dùng chữ số 0 và 1), bằng 8" in open(next(LESSONS.glob("L02_*.yaml")), encoding="utf-8").read())
    ok("L02 bảng: 01110010 >> 1 = 00111001 và & 1 = 1; range(1, 4) = [1, 2, 3]; ('a,b,c').split(',')[1] = 'b'",
       (0b01110010 >> 1) == 0b00111001 and ((0b01110010 >> 1) & 1) == 1 and list(range(1, 4)) == [1, 2, 3] and "a,b,c".split(",")[1] == "b")
    ok("L01 bảng: ',' .join(['x','y']) = 'x,y'; 'ab' + 'cd' = 'abcd'; từ điển cho['c1']", ",".join(["x", "y"]) == "x,y" and "ab" + "cd" == "abcd"
       and {"c1": "chuyen 5tr"}["c1"] == "chuyen 5tr")
    ok("L00 bảng: 10000 * 60 = 600000; print(155, 'ms') in '155 ms'", 10000 * 60 == 600000)
    # cách tạo/chạy tệp .py và chấm bằng cham.sh có trong L00 và nhắc lại ở L01, L02
    for lid in ("L00", "L01", "L02"):
        ok(f"{lid} có lệnh python mau.py và bash labs/cham.sh ACB {lid} mau.py trên màn hình", "python mau.py" in t[lid] and f"bash labs/cham.sh ACB {lid} mau.py" in t[lid])
    ok("L00 có cảnh dạy cách lưu/chạy/chấm tệp (chaytep) với bốn bước", any(s["id"] == "chaytep" and len(s["steps"]) == 1 for s in load("L00")["scenes"]) and "Open Git Bash here" in t["L00"])
    ok("L00 định nghĩa đối soát tại chỗ (so sổ giao dịch hai bên)", "hai bên so sổ giao dịch" in t["L00"])
    ok("L00, L02 ghi số 1 triệu / 800 000 lần ghi là 'số minh hoạ, cần đo' và nói 'một nút Redis'", "cần đo" in t["L00"] and "cần đo" in t["L02"] and "một nút Redis" in t["L00"] and "một nút Redis" in t["L02"] and "một cụm Redis" not in t["L00"])
    ok("L02 nêu luồng chuyển đi theo thứ tự thời gian (Core giữ tiền trước NAPAS); L00 nêu bốn tầng không phải thứ tự thời gian", "theo thứ tự thời gian" in t["L02"] and "chưa phải thứ tự thời gian" in t["L00"])
    ok("L02 định nghĩa nguyên tử và dịch mã PIN tại chỗ", "làm trọn một lệnh" in t["L02"] and "gọi là dịch mã PIN" in t["L02"] and "nhị phân" not in t["L02"].replace("phép toán nhị phân", "").replace("1000 (nhị phân: chỉ dùng chữ số 0 và 1)", ""))
    ok("L02 có hình bản đồ bit (SVG 8 ô: 0111 0010, trường 2, 3, 4, 7)", "Tám bit đầu của bản đồ bit" in t["L02"] and [i + 1 for i, b in enumerate("01110010") if b == "1"] == [2, 3, 4, 7])
    # đáp án đúng của quiz không dồn vào A: L01 C, L02 B
    ok("L01 quiz đáp án đúng C (mở hàng triệu hàng đợi riêng quá tải), L02 quiz đáp án đúng B (HSM giữ khoá)",
       "Đáp án chính xác là C" in open(next(LESSONS.glob("L01_*.yaml")), encoding="utf-8").read() and "Đáp án chính xác là B" in open(next(LESSONS.glob("L02_*.yaml")), encoding="utf-8").read())


def fixes7_l00_l02():
    """Sửa vòng 7 (R6_ACB, 2026-11-17) cho L00–L02 và giáo án: khoá chính, kho, chữ A–F hệ mười sáu, requires."""
    def raw(lid):
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", next(LESSONS.glob(f"{lid}_*.yaml")).read_text(encoding="utf-8")))
    t = {lid: raw(lid) for lid in ("L00", "L01", "L02")}
    ok("L00 giải nghĩa khoá chính (cột định danh duy nhất một dòng) và kho (thư mục chứa mã nguồn khoá học)", "khoá chính là cột định danh duy nhất một dòng" in t["L00"] and "Kho là thư mục chứa mã nguồn khoá học" in t["L00"])
    ok("L00 nói cách chạy python mau.py không cần kho", "không cần kho" in t["L00"])
    ok("L02 giải nghĩa A–F của hệ mười sáu và F2 = 15*16 + 2 = 242", 15 * 16 + 2 == 242 and int("F2", 16) == 242 and "A = 10" in t["L02"] and "F = 15" in t["L02"] and "= 242" in t["L02"])
    ok("L01 không còn 'dải tài khoản' và 'Hạch toán ghi nợ ghi có'", "dải tài khoản" not in t["L01"] and "Hạch toán ghi nợ ghi có" not in t["L01"])
    cur = {x["id"]: x for x in yaml.safe_load((ROOT / "curriculum" / "acb.yaml").read_text(encoding="utf-8"))["lessons"]}
    ok("giáo án: L06 requires có L03 (OTP), L07 requires có L04 (CIF)", "L03" in cur["L06"]["requires"] and "L04" in cur["L07"]["requires"])


def fixes8_l00_l02():
    """Sửa vòng 8 (2026-11-17) L00–L02: cách mở Git Bash, nguồn labs, lớp/giao dịch, giá trị vị trí 8-4-2-1."""
    def raw(lid):
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", next(LESSONS.glob(f"{lid}_*.yaml")).read_text(encoding="utf-8")))
    t = {lid: raw(lid) for lid in ("L00", "L01", "L02")}
    ok("L00 chaytep: bấm chuột phải, chọn Open Git Bash here; kho/labs lấy từ khoá học được giao", "Open Git Bash here" in t["L00"] and "bạn được giao" in t["L00"])
    ok("L00 pitfall: lớp và giao dịch giải nghĩa; có dòng nhắc nền (==, //, round, def, .replace)", "cùng thành công hoặc cùng bị huỷ" in t["L00"] and "lớp = khuôn mã Java" in t["L00"] and "Nhắc nền sẽ dùng lại" in t["L00"])
    ok("L00 định nghĩa sổ cái và nút Redis", "sổ ghi mọi khoản tiền vào ra" in t["L00"] and "một máy chạy Redis" in t["L00"])
    t7 = raw("L07")
    ok("L00 giải nghĩa lớp bọc của Spring (lớp trung gian mở giao dịch trước khi chạy hàm; gọi trong cùng lớp thì đi thẳng)", "gọi là lớp bọc, lớp này mở giao dịch trước khi chạy hàm" in t["L00"] and "đi thẳng, không qua lớp bọc" in t["L00"])
    ok("L07 bảng Đọc trước có def/return/print và .replace (tự đứng được)", "print(2 + 3)" in t7 and ".replace" in t7 and "def ky(noi_dung)" in t7 and "a9b9" in t7 and "1000000".replace("1000000", "9000000") == "9000000")
    ok("L02 bảng: 0111 = 4 + 2 + 1 = 7 (giá trị vị trí 8-4-2-1), 0010 = 2", 4 + 2 + 1 == 7 == 0b0111 and 0b0010 == 2 and "4 + 2 + 1 = 7" in t["L02"] and "8, 4, 2, 1" in t["L02"])


def main():
    want = [a.upper() for a in sys.argv[1:]] or list(FUNCS)
    for lid in want:
        FUNCS[lid]()
    if len(want) == len(FUNCS):
        common()
        fixes_r_int_acb()
        fixes5()
        fixes6_l00_l02()
        fixes7_l00_l02()
        fixes8_l00_l02()
    print(f"verify_acb: {N - len(FAILS)}/{N} PASS" + (f"; FAIL: {FAILS}" if FAILS else ""))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
