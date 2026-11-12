"""Kiểm độc lập BNX L18 (JUnit 5 + Mockito). Đường khác với tools/checklib_bnx/l18.py:
- phí tính bằng bảng mức quét tuyến tính (không dùng chuỗi if của checklib) và bằng CHẠY THẬT mã Java trên màn hình;
- bốn ca kiểm chạy thật bằng JUnit Platform Console Standalone 1.14.4 (JDK 21): đọc bản báo, đếm ca đạt/trượt, mã thoát;
- đối tượng giả: Mockito 5.24.0 thật (verify times(1)), kiểm NGƯỢC (đổi thành times(2) thì phải trượt), và giả viết tay Java thuần;
- giờ chốt: chạy thật java.time.Clock.fixed, đối chiếu phép so phút thuần.
Thư viện ở audit/bnx/deps/l18 (so sha256 với README trước khi chạy). Thiếu jar / java / bash → SKIP (cổng FAIL, NOT_VERIFIED)."""
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import l18 as src  # noqa: E402

DEPS = ROOT / "audit" / "bnx" / "deps" / "l18"
SHA = {
    "junit-platform-console-standalone-1.14.4.jar": "7c6968cbcaf4301c729f202b23b7d736c5d88be625fc7d27ad5d746146a8bc28",
    "mockito-core-5.24.0.jar": "97a1f835ad84075255aa37809e4379eff541273c02c6201cbad49bd5950932cd",
    "byte-buddy-1.17.7.jar": "3575dcb8a98faf943d3c1595c47a16047c4fce8a83ebbb26262f1a2f67546357",
    "byte-buddy-agent-1.17.7.jar": "a9ba887dca252ad61b7d5153294f34e6f3bdf4b2736b04373d13615a695fc0ff",
    "objenesis-3.3.jar": "02dfd0b0439a5591e35b708ed2f5474eb0948f53abf74637e959b8e4ef69bfeb",
}
LEVELS = [(0, 0), (500_000, 5_000), (10_000_000, 5_500)]   # (từ mốc, phí) theo ĐỀ BÀI ghi trong chú thích của Phi.java


def fee(amount):
    """Phí theo đề: quét bảng mức, lấy mức cuối cùng có mốc ≤ số tiền."""
    f = None
    for lo, v in LEVELS:
        if amount >= lo:
            f = v
    return f


def line_match(want, got):
    rx = re.compile("^" + ".*".join(re.escape(p) for p in want.strip().split("…")) + "$")
    return bool(rx.match(got.strip()))


def screen_matches(screen, actual):
    lines, pos = actual.replace("\r\n", "\n").split("\n"), 0
    for w in [x for x in screen.strip("\n").split("\n") if x.strip()]:
        while pos < len(lines) and not line_match(w, lines[pos]):
            pos += 1
        if pos == len(lines):
            return False
        pos += 1
    return True


def count(so, what):
    m = re.search(r"\[\s*(\d+) tests " + what + r"\s*\]", so)
    return int(m.group(1)) if m else None


def workdir(d, files):
    (Path(d) / "lib").mkdir()
    for j in SHA:
        shutil.copy(DEPS / j, Path(d) / "lib" / j)
    for name, text in files.items():
        Path(d, name).write_text(text.strip("\n") + "\n", encoding="utf-8", newline="\n")


def sh(d, script):
    Path(d, "k.sh").write_text(script.strip("\n") + "\n", encoding="utf-8", newline="\n")
    r = subprocess.run([shutil.which("bash"), "k.sh"], cwd=d, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=240)
    return r.returncode, r.stdout.replace("\r\n", "\n"), r.stderr


def run_java(parts):
    """Ghép các khối mã thành Main.java (như cổng screen_code), javac rồi java."""
    with tempfile.TemporaryDirectory() as d:
        Path(d, "Main.java").write_text("\n".join(p.strip("\n") for p in parts) + "\n", encoding="utf-8")
        r = subprocess.run(["javac", "-encoding", "UTF-8", "-d", d, "Main.java"], cwd=d, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode:
            return r.returncode, r.stderr
        r = subprocess.run(["java", "-Dstdout.encoding=UTF-8", "-cp", d, "Main"], cwd=d, capture_output=True, text=True, encoding="utf-8", errors="replace")
        return r.returncode, r.stdout.replace("\r\n", "\n")


def run(rec):
    # ── phần không cần công cụ: đề bài, bốn ca, phép tính ──
    cases = [("mienPhi", 200_000, 0), ("phiVua", 2_000_000, 5_000), ("phiCao", 50_000_000, 5_500), ("bien", 10_000_000, 5_500)]
    rec("L18", all(fee(a) == w == alg.bnx_jt_fee(a) for _, a, w in cases) and cases == alg.bnx_jt_fee_cases(),
        "giá trị mong đợi của bốn ca khớp ĐỀ (bảng mức quét tuyến tính) và khớp alg")
    pts = [0, 1, 199_999, 200_000, 499_999, 500_000, 500_001, 2_000_000, 9_999_999, 10_000_000, 10_000_001, 20_000_000, 50_000_000]
    diff = [a for a in pts if alg.bnx_jt_fee(a, True) != fee(a)]
    rec("L18", all(alg.bnx_jt_fee(a) == fee(a) for a in pts) and diff == [10_000_000] and alg.bnx_jt_fee(10_000_000, True) == 5_000,
        "hàm phí của alg khớp đề ở 13 điểm; bản lỗi `<=` chỉ sai tại đúng 10 000 000 (trả 5000 thay vì 5500)")
    rec("L18", len({fee(a) for a in pts}) == 3 == len(LEVELS) == alg.bnx_jt_fee_branches(), "① 2 mốc → 3 nhánh (ba mức phí khác nhau) → ít nhất 3 ca")
    rec("L18", (5_500 - 5_000, 20_000 * 500) == (500, 10_000_000) and fee(10_000_000) - alg.bnx_jt_fee(10_000_000, True) == 500,
        "hook/③: thu thiếu 5500 − 5000 = 500 đồng; 20 000 giao dịch × 500 = 10 000 000 (số minh hoạ)")
    rec("L18", [fee(a) for a in (499_999, 500_000, 9_999_999)] == [0, 5_000, 5_000] == [alg.bnx_jt_fee(a, True) for a in (499_999, 500_000, 9_999_999)],
        "câu 1: 499 999 → 0, 500 000 → 5000, 9 999 999 → 5000; bản lỗi cũng trả đúng → không ca nào trượt")
    rec("L18", 20_000_000 + fee(20_000_000) == 20_005_500 and alg.bnx_jt_transfer(20_000_000) == (5_500, [("TK01", 20_005_500)]),
        "câu 2: chuyển 20 000 000 → cổng được gọi 1 lần với 20 005 500")
    rec("L18", (100 * 10, 100 * 2000, 90 * 10 + 10 * 2000, 200_000 // 1000) == (1000, 200_000, 20_900, 200)
        == (alg.bnx_jt_suite_ms(100, 0), alg.bnx_jt_suite_ms(0, 100), alg.bnx_jt_suite_ms(90, 10), alg.bnx_jt_suite_ms(0, 100) // alg.bnx_jt_suite_ms(100, 0)),
        "câu 3 (số minh hoạ): 1 000 / 200 000 / 20 900 mili giây; toàn thật chậm gấp 200 lần")
    rec("L18", all(alg.bnx_jt_before_cutoff(h, m) == ((h, m) < (22, 0)) for h in range(24) for m in range(60)),
        "giờ chốt 22:00: alg khớp phép so cặp (giờ, phút) với mọi phút trong ngày")
    blocks = (src.JAVA_PHI, src.JAVA_PHITEST, src.SH_PHI, src.SH_FIX, src.JAVA_DV, src.JAVA_DVTEST, src.JAVA_TUCHOI, src.SH_MOCK, src.JAVA_FAKE,
              src.JAVA_CLOCK, src.OUT_PHI, src.OUT_FIX, src.OUT_MOCK, src.OUT_FAKE, src.OUT_CLOCK)
    lines = [l for c in blocks for l in c.strip("\n").split("\n")]
    rec("L18", max(map(len, lines)) <= 70 and all(len(c.strip("\n").split("\n")) <= 12 for c in blocks),
        f"khối mã/đầu ra ≤ 12 dòng, dòng dài nhất {max(map(len, lines))} ký tự (≤ 70)")

    # ── Java thuần (không cần thư viện ngoài) ──
    if not (shutil.which("javac") and shutil.which("java")):
        rec("L18", None, "NOT_VERIFIED: thiếu javac/java")
        return
    probe = "public class Main { public static void main(String[] a) { for (long x : new long[]{%s}) System.out.println(Phi.tinh(x)); } }" % ", ".join(f"{a}L" for a in pts)
    rc, so = run_java([src.JAVA_PHI, probe])
    got = [int(x) for x in so.split()] if rc == 0 else []
    rec("L18", rc == 0 and got == [alg.bnx_jt_fee(a, True) for a in pts] and [a for a, g in zip(pts, got) if g != fee(a)] == [10_000_000],
        "Phi.java trên màn hình chạy thật ở 13 điểm = alg (bản lỗi); chỉ lệch đề tại đúng 10 000 000")
    rc, so = run_java([src.JAVA_PHI.replace("<= 10_000_000", "< 10_000_000"), probe])
    rec("L18", rc == 0 and [int(x) for x in so.split()] == [fee(a) for a in pts], "Phi.java sau khi sửa `<=` thành `<` khớp đề ở cả 13 điểm")
    rc, so = run_java([src.JAVA_PHI, src.JAVA_DV, src.JAVA_FAKE])
    rec("L18", rc == 0 and so.split() == ["5000", "1", "2005000"] and screen_matches(src.OUT_FAKE, so)
        and alg.bnx_jt_transfer(2_000_000) == (5_000, [("TK01", 2_000_000 + fee(2_000_000))]),
        "đối tượng giả viết tay (Java thuần) chạy thật: phí 5000, gọi 1 lần, số tiền 2005000 = alg; màn hình khớp")
    rc, so = run_java([src.JAVA_CLOCK])
    rec("L18", rc == 0 and so.split() == ["true", "false"] and screen_matches(src.OUT_CLOCK, so)
        and alg.bnx_jt_before_cutoff(21, 59) and not alg.bnx_jt_before_cutoff(22, 0),
        "Clock.fixed chạy thật: 21:59 → true, 22:00 → false (không phụ thuộc giờ máy); màn hình khớp")

    # ── JUnit Platform + Mockito thật ──
    miss = [j for j in SHA if not (DEPS / j).exists()]
    if miss or not shutil.which("bash"):
        rec("L18", None, f"NOT_VERIFIED: thiếu {'bash' if not miss else miss} (tải lại theo audit/bnx/deps/l18/README.md)")
        return
    rec("L18", all(hashlib.sha256((DEPS / j).read_bytes()).hexdigest() == h for j, h in SHA.items()),
        "năm tệp jar ở audit/bnx/deps/l18 đúng sha256 ghi trong README (JUnit Console 1.14.4, Mockito 5.24.0, byte-buddy 1.17.7, agent 1.17.7, objenesis 3.3)")
    with tempfile.TemporaryDirectory() as d:
        workdir(d, {"Phi.java": src.JAVA_PHI, "PhiTest.java": src.JAVA_PHITEST})
        rc, so, se = sh(d, src.SH_PHI)
        ok_tree = {m.group(1): m.group(2) for m in re.finditer(r"-- (\w+)\(\) \[(OK|X)\]", so)}
        mine = {n: ("OK" if alg.bnx_jt_fee(a, True) == fee(a) else "X") for n, a, _ in cases}
        rec("L18", rc == 1 and (count(so, "found"), count(so, "successful"), count(so, "failed")) == (4, 3, 1) == (4,) + alg.bnx_jt_fee_run(True)[:2],
            f"JUnit thật: 4 ca, 3 đạt, 1 trượt, mã thoát 1 (được: {count(so, 'found')}/{count(so, 'successful')}/{count(so, 'failed')}, rc={rc})")
        rec("L18", ok_tree == mine and "bien() [X] expected: <5500> but was: <5000>" in so and alg.bnx_jt_fee_run(True)[2] == [("bien", 5_500, 5_000)],
            f"từng ca theo bản báo = dự đoán từ đề {ok_tree}; ca bien ghi expected: <5500> but was: <5000>")
        order = re.findall(r"-- (\w+)\(\) \[", so)
        rec("L18", screen_matches(src.OUT_PHI, so) and order == ["phiCao", "phiVua", "bien", "mienPhi"] and "PhiTest.bien(PhiTest.java:8)" in so,
            f"màn hình (OUT_PHI) khớp đầu ra thật; thứ tự chạy {order} khác thứ tự viết; dấu vết chỉ PhiTest.java:8")
        rc, so, se = sh(d, src.SH_FIX)
        fixed = Path(d, "Phi.java").read_text(encoding="utf-8")
        rec("L18", rc == 0 and "if (soTien < 10_000_000) return 5_000;" in fixed and "<=" not in fixed
            and (count(so, "found"), count(so, "successful"), count(so, "failed")) == (4, 4, 0) == (4,) + alg.bnx_jt_fee_run(False)[:2]
            and screen_matches(src.OUT_FIX, so), "khối sửa (sed + chạy lại) chạy thật: 4 ca, 4 đạt, 0 trượt, mã thoát 0; màn hình khớp")
    with tempfile.TemporaryDirectory() as d:
        workdir(d, {"Phi.java": src.JAVA_PHI, "ChuyenTien.java": src.JAVA_DV, "ChuyenTienTest.java": src.JAVA_DVTEST, "TuChoiTest.java": src.JAVA_TUCHOI})
        rc, so, se = sh(d, src.SH_MOCK)
        rec("L18", rc == 0 and (count(so, "found"), count(so, "successful"), count(so, "failed")) == (2, 2, 0)
            and "goiCongDungMotLan() [OK]" in so and "congTuChoiThiNemLoi() [OK]" in so and screen_matches(src.OUT_MOCK, so),
            "Mockito thật: verify(cong, times(1)).chuyen(\"TK01\", 2_005_000) đạt ở cả hai ca (cổng nhận và cổng từ chối); màn hình khớp")
        # kiểm ngược: phép kiểm tương tác phải TRƯỢT khi đòi sai số lần / sai tham số (nếu không, 'đạt' ở trên vô nghĩa)
        Path(d, "ChuyenTienTest.java").write_text(src.JAVA_DVTEST.strip("\n").replace("times(1)", "times(2)") + "\n", encoding="utf-8", newline="\n")
        Path(d, "TuChoiTest.java").write_text(src.JAVA_TUCHOI.strip("\n").replace('.chuyen("TK01", 2_005_000);', '.chuyen("TK01", 2_000_000);') + "\n",
                                              encoding="utf-8", newline="\n")
        rc, so, se = sh(d, src.SH_MOCK)
        rec("L18", rc == 1 and count(so, "failed") == 2 and "Wanted 2 times" in so and "But was 1 time" in so and "2005000L" in so,
            "kiểm ngược: đòi times(2) → trượt 'Wanted 2 times … But was 1 time'; đòi sai số tiền 2 000 000 → trượt (lời gọi thật là 2005000L)")
