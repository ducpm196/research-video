"""Kiểm độc lập BNX L21 — tính lại bằng đường KHÁC checklib (phân số và vét cạn cho tỉ lệ nghĩa vụ trên thu nhập, dò từng ngày cho nhóm nợ,
tìm đường trên đồ thị cho máy trạng thái, `openssl dgst` cho mã băm, ký và kiểm chữ ký thật bằng cặp khoá RSA của openssl, biểu thức
chính quy cho trường đa trị; chạy thật mọi khối mã trên màn hình) rồi đối chiếu với alg.bnx_* mà `checks:` dùng."""
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402
import l21 as L  # noqa: E402
import lib2  # noqa: E402

LABDIR = ROOT / "labs" / "BNX" / "L21"


def extra(rec):
    """AF2 (nhánh B): quy mô đo thật ở 5, 500, 50 000 hồ sơ; lab chạy lại qua labs/cham.sh; mọi chương trình prog() chạy lại nguyên văn."""
    C = "L21"
    lib2.verify_programs(rec, C)
    # quy mô: tính lại bằng đường khác (dùng thuộc tính dựng tay, không dùng alg.bnx_l21_fp_of)
    he = ["Android 13", "Android 14", "iOS 17", "iOS 18"]
    man = ["720x1600", "1080x2400", "1170x2532", "1290x2796", "1440x3200", "1080x1920"]
    res = {}
    for n in (5, 500, 50_000):
        cnt = {}
        for i in range(n):
            h = int(hashlib.sha256(("hs%d" % i).encode()).hexdigest(), 16)
            k = hashlib.sha256(("|".join([he[h % 4], man[h // 4 % 6], "UTC+7"])).encode()).hexdigest()[:12]
            cnt[k] = cnt.get(k, 0) + 1
        res[n] = (len(cnt), sum(c for c in cnt.values() if c >= 3))
    out = next(p for p in lib2.PROGRAMS if p.key == "L21_QuyMo").out
    shown = {int(a): (int(b), int(c)) for a, b, c in re.findall(r"^(\d+) ho so, (\d+) ma khac nhau, (\d+) ho so bi gan co$", out, re.M)}
    rec(C, shown == res == {5: (5, 0), 500: (24, 500), 50_000: (24, 50_000)}, f"quy mô: chạy thật = tính lại tay = bảng trên màn hình {res}")
    rec(C, all(alg.bnx_l21_scale(n) == res[n] for n in res), "alg.bnx_l21_scale khớp số đo thật ở 5, 500, 50 000")
    rec(C, [-(-f // 40) for f in (0, 500, 50_000)] == [0, 13, 1250] == [alg.bnx_l21_reviewers(f, 40) for f in (0, 500, 50_000)],
        "người xét cần mỗi ngày (40 hồ sơ mỗi người): 0, 13, 1 250")
    # lab: chạy lời giải qua cham.sh, tự tính lại số bằng tay
    rec(C, (LABDIR / "mong_doi.txt").read_text(encoding="utf-8").strip() == next(p for p in lib2.PROGRAMS if p.key == "L21_LabL21").out,
        "mong_doi.txt = đầu ra thật của lời giải lab")
    a = hashlib.sha256(b"Hop dong vay 14000000 dong, ky han 24 thang\n").hexdigest()
    b = hashlib.sha256(b"Hop dong vay 14000000 dong, ky han 25 thang\n").hexdigest()
    exp = ["DTI: %.1f %%" % (6 * 100 / 14), "Diem: %d" % (20 + 25 + 20), "Quyet dinh: TU_CHOI", "Ma bam goc: " + a[:12], "Vi tri khac: %d" % sum(x != y for x, y in zip(a, b))]
    rec(C, (LABDIR / "mong_doi.txt").read_text(encoding="utf-8").strip().splitlines() == exp,
        "lab: năm dòng mong đợi khớp tính lại bằng tay (42,9 %; 65 điểm; TU_CHOI; mã băm; 60 vị trí)")
    bash = shutil.which("bash")
    if bash:
        r = subprocess.run([bash, str(ROOT / "labs" / "cham.sh"), "BNX", "L21", str(LABDIR / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8", timeout=120, cwd=str(ROOT))
        rec(C, r.stdout.strip().startswith("ĐÚNG"), f"labs/cham.sh BNX L21 loi_giai.py: {r.stdout.strip()[:60]}")
    else:
        rec(C, None, "thiếu bash: không chạy cham.sh")


def _run_py(code, post=""):
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", "-c", code + ("\n" + post if post else "")],
                       capture_output=True, text=True, encoding="utf-8", timeout=60)
    return r.returncode, r.stdout.replace("\r\n", "\n").strip("\n"), r.stderr


def _reach(edges, a, b):
    """Đường khác: tìm theo chiều rộng trên đồ thị cạnh."""
    seen, todo = {a}, [a]
    while todo:
        x = todo.pop(0)
        for u, v in edges:
            if u == x and v not in seen:
                seen.add(v)
                todo.append(v)
    return b in seen


def run(rec):
    C = "L21"
    extra(rec)
    # 1. máy trạng thái: chạy thật mã trên màn hình + đồ thị dựng tay
    rc, so, se = _run_py(L.STATE_PY + "\n" + L.STATE_RUN)
    rec(C, rc == 0 and so == L.STATE_OUT, f"chạy STATE_PY + STATE_RUN: {so.splitlines()}")
    edges = [("NOP", "CHAM_DIEM"), ("CHAM_DIEM", "THAM_DINH"), ("CHAM_DIEM", "TU_CHOI"), ("THAM_DINH", "DUYET"), ("THAM_DINH", "TU_CHOI"),
             ("THAM_DINH", "XET_TAY"), ("XET_TAY", "DUYET"), ("XET_TAY", "TU_CHOI"),
             ("DUYET", "DA_KY"), ("DA_KY", "GIAI_NGAN")]
    rc2, so2, _ = _run_py(L.STATE_PY, "print(sorted((a, b) for a in BUOC for b in BUOC[a]))")
    rec(C, rc2 == 0 and so2 == str(sorted(edges)), "bảng BUOC trên màn hình đúng bằng 10 cạnh dựng tay (hình SVG 1, có XET_TAY)")
    states = sorted({x for e in edges for x in e})
    same = all(alg.bnx_loan_path_ok([a, b])[0] == ((a, b) in edges) for a in states for b in states)
    rec(C, same and _reach(edges, "NOP", "GIAI_NGAN") and ("DUYET", "GIAI_NGAN") not in edges
        and not _reach([e for e in edges if e != ("DUYET", "DA_KY")], "NOP", "GIAI_NGAN"),
        "49 cặp trạng thái: alg khớp tập cạnh; NOP tới được GIAI_NGAN; bỏ cạnh DUYET→DA_KY thì không còn đường (không có đường tắt)")
    # 2. nhóm nợ: dò từng ngày 0..400 theo các khoảng của Điều 10 (đề giao) so với alg và mã trên màn hình
    rc, so, _ = _run_py(L.GROUP_PY)
    rec(C, rc == 0 and so == L.GROUP_OUT, f"chạy GROUP_PY: {so}")
    def grp(d):
        return 1 if d < 10 else 2 if 10 <= d <= 90 else 3 if 91 <= d <= 180 else 4 if 181 <= d <= 360 else 5
    rc, so, _ = _run_py(L.GROUP_PY, "print([nhom_no(n) for n in range(401)])")
    rec(C, rc == 0 and so.splitlines()[-1] == str([grp(d) for d in range(401)]) and all(alg.bnx_debt_group(d) == grp(d) for d in range(401)),
        "nhóm nợ 0..400 ngày: mã trên màn hình = alg = bảng khoảng (dưới 10; 10–90; 91–180; 181–360; trên 360)")
    # 3. tỉ lệ nghĩa vụ trên thu nhập và thẻ điểm
    f = Fraction(4_000_000 + 5_000_000, 20_000_000)
    rec(C, f == Fraction(9, 20) and f * 100 == 45 == alg.bnx_dti(20_000_000, 4_000_000, 5_000_000) and f <= Fraction(1, 2),
        "ví dụ giáo án: (4 + 5)/20 = 9/20 = 45% ≤ 50% (phân số = alg)")
    ok = True
    for inc in range(1, 41):
        for pay in range(0, 21):
            for new in range(0, 21):
                want = Fraction(pay + new, inc) <= Fraction(1, 2)
                ok &= alg.bnx_dti_pass(inc, pay, new, 50) == want
                if 2 * pay <= inc:   # nợ đang trả đã vượt ngưỡng thì hàm trả 0 (kẹp dưới), không so được
                    ok &= (new <= alg.bnx_max_new_payment(inc * 100, pay * 100, 50) / 100) == want
                else:
                    ok &= alg.bnx_max_new_payment(inc * 100, pay * 100, 50) == 0 and not want
    rec(C, ok, "vét 17 640 bộ (thu nhập, đang trả, khoản mới): bnx_dti_pass và bnx_max_new_payment khớp so phân số")
    table = {"thu": (15_000_000, 35, 20), "nhom": (25, 0), "thang": (24, 20, 10)}
    def score(inc, g, m):
        return (table["thu"][1] if inc >= table["thu"][0] else table["thu"][2]) + (table["nhom"][0] if g == 1 else table["nhom"][1]) \
            + (table["thang"][1] if m >= table["thang"][0] else table["thang"][2])
    rec(C, score(20_000_000, 1, 36) == 80 == sum((35, 25, 20)) == alg.bnx_scorecard(20_000_000, 1, 36)[3]
        and all(alg.bnx_scorecard(i, g, m)[3] == score(i, g, m) for i in (14_999_999, 15_000_000) for g in range(1, 6) for m in (23, 24)),
        "thẻ điểm: 35 + 25 + 20 = 80 ≥ 70; 20 tổ hợp quanh biên khớp bảng dựng tay")
    rc, so, _ = _run_py(L.DECIDE_PY + "\n" + L.DECIDE_RUN)
    rec(C, rc == 0 and so == L.DECIDE_OUT, f"chạy DECIDE_PY + DECIDE_RUN: {so.splitlines()}")
    post = ("import itertools\nprint([tham_dinh(i, p, n, g, m)[2] for i, p, n, g, m in itertools.product("
            "(12_000_000, 20_000_000), (0, 4_000_000), (5_000_000, 6_000_000, 6_190_000, 7_000_000), (1, 2, 3), (12, 36))])")
    rc, so, _ = _run_py(L.DECIDE_PY, post)
    import itertools
    mine = [alg.bnx_underwrite(i, p, n, g, m) for i, p, n, g, m in itertools.product(
        (12_000_000, 20_000_000), (0, 4_000_000), (5_000_000, 6_000_000, 6_190_000, 7_000_000), (1, 2, 3), (12, 36))]
    rec(C, rc == 0 and so == str(mine) and len(mine) == 96, "96 hồ sơ: bộ máy quyết định trên màn hình = alg.bnx_underwrite")
    rec(C, Fraction(10_190_000, 20_000_000) * 100 == Fraction(1019, 20) and 10_190_000 * 100 // 20_000_000 == 50
        and not alg.bnx_dti_pass(20_000_000, 4_000_000, 6_190_000) and alg.bnx_underwrite(20_000_000, 4_000_000, 6_190_000, 1, 36) == "TU_CHOI",
        "lỗi 2: 50,95% bị chia nguyên cắt còn 50 (qua sai); nhân chéo thì vượt → TU_CHOI")
    rec(C, Fraction(16, 30) > Fraction(1, 2) and round(1600 / 30, 1) == 53.3 and 30 // 2 - 6 == 9 == alg.bnx_max_new_payment(30, 6)
        and alg.bnx_debt_group(95) == 3 and 20 + 25 + 10 == 55 == alg.bnx_scorecard(12_000_000, 1, 12)[3],
        "quiz 1, 2: 16/30 ≈ 53,3% không qua, tối đa 9 triệu; 95 ngày → nhóm 3; 55 điểm")
    # 4. mã băm: hashlib (màn hình) so với openssl dgst (đường khác)
    rc, so, _ = _run_py(L.HASH_PY)
    rec(C, rc == 0 and so == L.HASH_OUT, f"chạy HASH_PY: {so.splitlines()}")
    ossl = shutil.which("openssl")
    bash = shutil.which("bash")
    if not ossl or not bash:
        rec(C, None, "NOT_VERIFIED: thiếu openssl hoặc bash — không kiểm được mã băm bằng đường khác và phép ký")
        return
    with tempfile.TemporaryDirectory() as d:
        dp = Path(d)
        (dp / "khoi.sh").write_text(L.SIGN_SH + "\n", encoding="utf-8", newline="\n")
        r = subprocess.run([bash, "khoi.sh"], cwd=d, capture_output=True, text=True, encoding="utf-8", timeout=120)
        rec(C, r.returncode == 0 and r.stdout.replace("\r\n", "\n").strip() == L.SIGN_OUT,
            f"chạy SIGN_SH (openssl thật): {r.stdout.split()} — gốc hợp lệ, bản sửa một ký tự thất bại, bản sao tên khác hợp lệ")
        raw, raw2 = (dp / "hd.txt").read_bytes(), (dp / "hd_sua.txt").read_bytes()
        rec(C, raw == L.HD.encode() and sum(x != y for x, y in zip(raw, raw2)) == 1 and len(raw) == len(raw2),
            "tệp hd.txt đúng bằng chuỗi hợp đồng của HASH_PY; hd_sua.txt khác đúng MỘT byte")
        o = subprocess.run([ossl, "dgst", "-sha256", "-r", "hd.txt", "hd_sua.txt"], cwd=d, capture_output=True, text=True).stdout.split()
        h1, h2 = o[0], o[2]
        rec(C, h1 == hashlib.sha256(raw).hexdigest() == alg.bnx_sha256_hex(L.HD) and h1[:16] == L.HASH_OUT.split()[0]
            and h2[:16] == L.HASH_OUT.splitlines()[1].split()[0] and h1.startswith("662097aa") and h2.startswith("93938eab"),
            f"mã băm: openssl dgst = hashlib = alg ({h1[:16]}…, bản sửa {h2[:16]}…)")
        rec(C, sum(1 for i in range(64) if h1[i] != h2[i]) == 60 == alg.bnx_hex_diff(h1, h2), "hai mã băm khác nhau ở 60/64 vị trí")
        sig = (dp / "hd.sig").read_bytes()
        (dp / "hd.sig2").write_bytes(sig[:-1] + bytes([sig[-1] ^ 1]))
        r3 = subprocess.run([ossl, "dgst", "-sha256", "-verify", "cong.pem", "-signature", "hd.sig2", "hd.txt"], cwd=d, capture_output=True, text=True)
        rec(C, len(sig) == 256 and r3.returncode != 0 and "Verification failure" in r3.stdout,
            "đối chứng: chữ ký RSA 2048 dài 256 byte; lật một bit của chữ ký thì kiểm thất bại")
    # 5. dấu vân tay thiết bị
    rc, so, _ = _run_py(L.FRAUD_PY)
    rec(C, rc == 0 and so == L.FRAUD_OUT, f"chạy FRAUD_PY: {so}")
    fa = hashlib.sha256(b"Android 14|1080x2400|UTC+7").hexdigest()[:12]
    fb = hashlib.sha256(b"Android 14|1170x2532|UTC+7").hexdigest()[:12]
    rec(C, fa == alg.bnx_device_fp(L.A1) == "f7286011deef" and fb == "3b0dc756fcb5" and fa != fb
        and alg.bnx_device_fp(dict(L.A1)) == fa,
        "dấu vân tay: băm chuỗi dựng tay = alg; hai máy cùng thuộc tính cho cùng mã (tín hiệu, không phải danh tính)")
    # 6. trường đa trị: biểu thức chính quy (đường khác) so với mã trên màn hình và alg
    rc, so, _ = _run_py(L.OFS_PY, "print(sorted((t, k, v) for t in truong for k, v in truong[t].items()))")
    rec(C, rc == 0 and "\n".join(so.splitlines()[:3]) == L.OFS_OUT, f"chạy OFS_PY: {so.splitlines()[:3]}")
    trip = sorted((m.group(1), (int(m.group(2)), int(m.group(3))), m.group(4)) for m in re.finditer(r"([A-Z.]+):(\d+):(\d+)=([^,]*)", L.OFS_MSG))
    a = alg.bnx_ofs_fields(L.OFS_MSG)
    rec(C, rc == 0 and so.splitlines()[-1] == str(trip) == str(sorted((t, k, v) for t in a for k, v in a[t].items())) and len(trip) == 4,
        "4 giá trị (tên, (mv, sv), giá trị): biểu thức chính quy = mã trên màn hình = alg")
    rc, so, _ = _run_py(L.OFS_PY, "print(ofs)")
    rec(C, rc == 0 and so.splitlines()[-1] == L.OFS_MSG, "chuỗi OFS mẫu trên màn hình đúng bằng chuỗi dùng trong checks")
    blocks = (L.STATE_PY, L.STATE_RUN, L.GROUP_PY, L.DECIDE_PY, L.DECIDE_RUN, L.HASH_PY, L.SIGN_SH, L.OFS_PY, L.FRAUD_PY)
    rec(C, all(len(l) <= 70 for t in blocks for l in t.split("\n")) and all(len(t.split("\n")) <= 12 for t in blocks),
        "mọi khối mã ≤ 12 dòng, dòng ≤ 70 ký tự")
