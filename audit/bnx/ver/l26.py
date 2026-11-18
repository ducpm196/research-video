"""Kiểm độc lập BNX L26 (Maven, Gradle và Jenkins). Đường khác với tools/checklib_bnx/l26.py:
- CHẠY LẠI THẬT (không đệm) mọi chương trình trên màn hình: Apache Maven 3.9.11 (dependency:tree, package, dựng hai lần so sha256), Groovy 4.0.27 (GroovyShell.parse)
  — thiếu Maven/Groovy → SKIP (rec None: cổng FAIL, NOT_VERIFIED), không PASS lặng lẽ;
- luật gần nhất thắng: bộ phân giải tự viết (hàng đợi) đối chiếu với cây Maven thật; số jar của ba dự án thử đếm lại bằng mục tiêu KHÁC (`dependency:tree`, không phải `dependency:list`);
- các pha dựng so với thứ tự trong tài liệu Maven (đã chép ở sources_l26.md);
- công thức số máy dựng tính lại bằng phân số (Fraction) và bằng mô phỏng hàng đợi từng phút (số hữu hạn máy đủ để không tồn đọng);
- lab chạy lại và so mong_doi.txt."""
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import lib2  # noqa: E402
import l26 as src  # noqa: E402

MVN = ROOT / "audit" / "bnx" / "deps" / "_tools" / "apache-maven-3.9.11" / "bin" / "mvn"
GROOVY = ROOT / "audit" / "bnx" / "deps" / "l26" / "groovy-4.0.27.jar"
LAB = ROOT / "labs" / "BNX" / "L26"


def hang_doi(builds_per_hour, minutes_per_build, agents, horizon_min=600):
    """Mô phỏng từng phút: mỗi phút tới builds_per_hour/60 lượt (phân số), mỗi máy xử lý 1 phút công việc mỗi phút. Trả khối lượng tồn cuối."""
    ton, den = Fraction(0), Fraction(builds_per_hour * minutes_per_build, 60)
    for _ in range(horizon_min):
        ton = max(Fraction(0), ton + den - agents)
    return ton


def run(rec):
    if not MVN.exists() or not GROOVY.exists():
        rec("L26", None, "thiếu Maven (audit/bnx/deps/_tools) hoặc Groovy (audit/bnx/deps/l26): NOT_VERIFIED")
    else:
        lib2.verify_programs(rec, "L26")
        P = {q.name: q for q in lib2.PROGRAMS if q.lesson == "L26"}
        out = P["ChayCay"].out
        rec("L26", "commons-lang3:jar:3.9:compile" in out and "omitted for conflict with 3.9" in out and "3.12.0" in out, "cây Maven thật: commons-lang3 3.9 (trực tiếp) thắng 3.12.0 (bắc cầu), báo 'omitted for conflict with 3.9'")
        # cây chi tiết: dòng omitted nằm DƯỚI commons-text (nhánh của text), lang3 3.9 là nhánh riêng của dự án (sửa lỗi cây ghép của bản trước)
        verb = out.split("-- che do chi tiet (-Dverbose):")[1].strip().splitlines()
        rec("L26", len(verb) == 4 and verb[1].startswith("+- ") and "commons-text:jar:1.10.0" in verb[1] and verb[2].startswith("|  \\- (") and "3.12.0" in verb[2]
            and "omitted for conflict with 3.9" in verb[2] and verb[3].startswith("\\- ") and "commons-lang3:jar:3.9:compile" in verb[3],
            "cây chi tiết thật: dòng omitted là con của commons-text (bắc cầu), commons-lang3 3.9 là nhánh trực tiếp riêng; màn hình in nguyên cả hai lệnh, không ghép")
        # vòng đời: pha ≠ mục tiêu; đối chiếu help:describe thật (17 pha tới package, 6 pha có mục tiêu gắn vào)
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
            Path(d, "pom.xml").write_text(P["PomGoc"].code + "\n", encoding="utf-8")
            r = subprocess.run([str(MVN) + ".cmd", "-B", "help:describe", "-Dcmd=package"], cwd=d, capture_output=True, text=True, encoding="utf-8")
            pha = re.findall(r"^\* ([\w-]+): (.+)$", r.stdout, re.M)
            order = [p for p, _ in pha]
            tt = order.index("package") + 1
            gan = [(p, re.sub(r"^org\.apache\.maven\.plugins:maven-(\w+)-plugin:[\d.]+:", r"\1:", g)) for p, g in pha[:tt] if g != "Not defined"]
            rec("L26", r.returncode == 0 and tt == alg.bnx_l26_phase_count() == 17 and gan == alg.bnx_l26_phase_goals() and len(gan) == 6,
                f"help:describe -Dcmd=package thật: {tt} pha tới package, {len(gan)} pha có mục tiêu gắn vào = bảng trên màn hình (pha ≠ mục tiêu)")
        # bộ phân giải tự viết, đối chiếu cây thật
        tree = {("text", "1.10.0"): [("lang3", "3.12.0")]}
        chon = alg.bnx_l26_maven([("text", "1.10.0"), ("lang3", "3.9")], tree)
        rec("L26", chon == {"text": "1.10.0", "lang3": "3.9"} and P["GiaiPhuThuoc"].out.splitlines()[-1] == "{'text': '1.10.0', 'lang3': '3.9'}", "bộ phân giải tự viết (alg và bài) cho lang3 3.9, khớp Maven thật")
        rec("L26", alg.bnx_l26_gradle([("text", "1.10.0"), ("lang3", "3.9")], tree)["lang3"] == "3.12.0", "luật Gradle mặc định (cao nhất): cùng đồ thị này sẽ chọn lang3 3.12.0 (theo tài liệu; Gradle không chạy)")
        names = [re.match(r"--- (\w+):[\d.]+:(\w+) ", l).groups() for l in P["ChayVongDoi"].out.splitlines()]
        rec("L26", [b for a, b in names] == alg.bnx_l26_phases(), "các mục tiêu (phần mở rộng:mục tiêu) chạy thật của mvn package: " + " → ".join(b for a, b in names))
        rec("L26", P["ChayTaiLap"].out.splitlines() == ["khong dat outputTimestamp: KHAC", "co outputTimestamp: GIONG"], "dựng tái lập: không đặt outputTimestamp → khác; đặt → giống (sha256 jar so thật)")
        rec("L26", P["ChayKiem"].out.splitlines() == ["Jenkinsfile: cu phap hop le", "build.gradle: cu phap hop le", "JenkinsfileHong: loi cu phap"], "Groovy thật: Jenkinsfile và build.gradle hợp lệ, tệp thiếu ngoặc bị từ chối")
        # số jar: đếm lại bằng dependency:tree (khác dependency:list)
        got = {m[0]: int(m[1]) for m in re.findall(r"^(\w): 1 phu thuoc truc tiep -> (\d+) jar$", P["ChayQuyMo"].out, re.M)}
        rec("L26", set(got) == {"a", "b", "c"} and got["a"] < got["b"] < got["c"], f"số jar của ba dự án thử tăng dần: {got}")
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
            for k, pn in (("a", "PomA"), ("b", "PomB"), ("c", "PomC")):
                dd = Path(d, k)
                dd.mkdir()
                (dd / "pom.xml").write_text(P[pn].code + "\n", encoding="utf-8")
                r = subprocess.run([str(MVN) + ".cmd", "-B", "-q", "dependency:tree", "-DoutputFile=t.txt"], cwd=dd, capture_output=True, text=True, shell=False)
                n = len(re.findall(r":jar:", (dd / "t.txt").read_text(encoding="utf-8"))) if r.returncode == 0 else -1
                rec("L26", n - 1 == got[k], f"dự án {k}: dependency:tree đếm lại ra {n - 1} phụ thuộc (trừ dự án gốc), dependency:list ra {got[k]}")
    # công thức máy dựng: phân số + mô phỏng
    cases = [(4, 10), (400, 10), (40000, 10)]
    for b, m in cases:
        a = alg.bnx_l26_agents(b, m)
        want = -(-Fraction(b * m, 60) // 1)
        rec("L26", a == want and hang_doi(b, m, a) == 0 and (a == 1 or hang_doi(b, m, a - 1) > 0), f"{b} lượt/giờ × {m} phút: cần {a} máy; đủ (hàng đợi về 0) và thiếu 1 máy thì tồn đọng")
    rec("L26", alg.bnx_l26_agents(4, 10) == 1 and alg.bnx_l26_agents(400, 10) == 67 and alg.bnx_l26_agents(40000, 10) == 6667, "x1, x100, x10 000: 1, 67, 6 667 máy")
    # lab
    r = subprocess.run([sys.executable, "-X", "utf8", str(LAB / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8")
    rec("L26", r.returncode == 0 and r.stdout.strip() == (LAB / "mong_doi.txt").read_text(encoding="utf-8").strip(), "lab: loi_giai.py cho đúng mong_doi.txt")
    du_an = [("A", "1.0"), ("B", "1.0")]
    cay = {("A", "1.0"): [("X", "1.0"), ("Y", "2.0")], ("B", "1.0"): [("Y", "3.0"), ("Z", "1.0")], ("Z", "1.0"): [("X", "2.0")]}
    rec("L26", alg.bnx_l26_maven(du_an, cay) == {"A": "1.0", "B": "1.0", "X": "1.0", "Y": "2.0", "Z": "1.0"} and alg.bnx_l26_gradle(du_an, cay)["X"] == "2.0"
        and alg.bnx_l26_gradle(du_an, cay)["Y"] == "3.0", "lab: kết quả hai luật tính lại bằng alg")
