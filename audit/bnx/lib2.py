"""BNX2 (L24–L36, đợt BNX2 2026-11-13): sổ chương trình chạy thật + sinh sổ mã trên màn hình, theo cách audit/bnk/lib.py `prog`.

    import lib2
    from lib2 import *                       # kéo theo mọi thứ của lib.py (st, sc, table, svg, code, out, lesson…)
    lib2.begin("L24")
    P1 = prog("DemSql", JAVA_CODE, lang="java")               # chạy THẬT lúc import (đệm ở audit/bnx/progcache/), P1.out = đầu ra thật
    P2 = prog("Chay", SH_CODE, lang="bash", files={"A.java": "A"}, timeout=300)   # script bash; files: tên tệp → tên prog cùng bài
    P3 = prog("A", JAVA_NEEDS_JAR, lang="java", kind="other")  # nguồn Java cần jar: không chạy riêng, chỉ ghi vào thư mục của script
    st(..., P1.show(lines=(1, 8)) + P1.out_html(), …)

`python -B audit/bnx/lib2.py gen-screen L24` sinh audit/bnx/screen/l24.yaml từ lessons/bnx/L24_*.yaml (fragment within / output of).
`python -B audit/bnx/lib2.py run L24` chạy mọi chương trình của bài (không đệm) và in so sánh với đầu ra đã đệm.
Đầu ra phải TẤT ĐỊNH (không in giờ, không in thời gian đo): đếm số câu SQL, số sự kiện, số lần gọi."""
import hashlib
import importlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.path.insert(0, str(ROOT / "audit"))
from lib import *  # noqa: E402,F401,F403
import lib as _lib  # noqa: E402
import lv  # noqa: E402


def st(show, say, focus=None, **kw):
    """Như lib.st, nhưng `focus` khai sai độ dài (không đúng một mục cho mỗi câu) thì bỏ để lib tự tính (E31 khỏi vỡ khi sửa lời)."""
    if focus is not None:
        n = len(lv.sentences(" ".join(say.split())))
        if not isinstance(focus, list) or len(focus) != n:
            focus = None
    return _lib.st(show, say, focus=focus, **kw)

CACHE_DIR = ROOT / "audit" / "bnx" / "progcache"
PROGRAMS = []
_CUR = {"lesson": None}
OTHERS = []


def begin(lid):
    _CUR["lesson"] = lid.upper()


def _bash():
    for c in (r"C:\Program Files\Git\bin\bash.exe", shutil.which("bash")):
        if c and Path(c).exists():
            return c
    return "bash"


def _py():
    v = ROOT / ".venv" / "Scripts" / "python.exe"
    return str(v) if v.exists() else sys.executable


def _run(cmd, cwd, timeout):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout, env=env, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout.replace("\r\n", "\n"), r.stderr.replace("\r\n", "\n")


class Prog:
    def __init__(self, lesson, name, code, lang, files, kind, extra):
        self.lesson, self.name, self.lang, self.files, self.kind, self.extra = lesson, name, lang, files or {}, kind, extra
        self.code = code.strip("\n")
        self.out = None

    @property
    def key(self):
        return f"{self.lesson}_{self.name}"

    def digest(self):
        h = hashlib.sha256()
        h.update(json.dumps([self.lang, self.code, sorted(self.files.items()),
                             [find(self.lesson, f).code for f in self.files.values()], sorted((k, str(v)) for k, v in self.extra.items())],
                            ensure_ascii=False).encode("utf-8"))
        return h.hexdigest()[:20]

    def execute(self):
        """Chạy đúng như cổng screen_code: thư mục tạm, ghi `files`, rồi chạy. Trả (rc, stdout, stderr)."""
        to = self.extra.get("timeout", 120)
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
            dp = Path(d)
            for fname, ref in self.files.items():
                (dp / fname).write_text(find(self.lesson, ref).code + "\n", encoding="utf-8", newline="\n")
            if self.lang == "java":
                cls = self.extra.get("java_class") or self.name
                (dp / f"{cls}.java").write_text(self.code + "\n", encoding="utf-8")
                rc, so, se = _run(["javac", "-encoding", "UTF-8", "-d", d, f"{cls}.java"], d, 120)
                if rc:
                    return rc, so, se
                return _run(["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", "-cp", d, cls], d, to)
            if self.lang == "python":
                (dp / "khoi.py").write_text(self.code + "\n", encoding="utf-8")
                return _run([_py(), "-I", "-X", "utf8", "-B", "khoi.py"], d, to)
            if self.lang == "bash":
                (dp / "khoi.sh").write_text(self.code + "\n", encoding="utf-8", newline="\n")
                return _run([_bash(), "khoi.sh"], d, to)
            raise ValueError(self.lang)

    # ── mảnh HTML ──
    def show(self, lines=None, title=None):
        return code(self.code, title, lines)

    def show_from(self, needle, n, title=None):
        """Hiện n dòng bắt đầu từ dòng đầu tiên có chứa `needle` (không phải đếm số dòng tay)."""
        ls = self.code.split(chr(10))
        i = next(k for k, l in enumerate(ls) if needle in l)
        return code(self.code, title, (i + 1, min(i + n, len(ls))))

    def out_html(self, text=None, title="Kết quả chạy thật"):
        return out(text if text is not None else self.out, title)


def find(lesson, name):
    for p in PROGRAMS:
        if p.lesson == lesson and p.name == name:
            return p
    raise KeyError(f"{lesson} {name}")


def prog(name, code, lang="java", out=None, files=None, kind="run", **extra):
    p = Prog(_CUR["lesson"], name, code, lang, files, kind, extra)
    PROGRAMS.append(p)
    if kind == "run":
        cf = CACHE_DIR / f"{p.lesson}.json"
        cache = json.loads(cf.read_text(encoding="utf-8")) if cf.exists() else {}
        dg = p.digest()
        ent = cache.get(p.name)
        if ent and ent["digest"] == dg:
            p.out = ent["out"]
        else:
            # nguồn Java đi kèm (files) phải đã đăng ký: chương trình đứng SAU các tệp nó dùng trong src
            rc, so, se = p.execute()
            if rc != 0 and not extra.get("allow_rc"):
                raise RuntimeError(f"{p.key}: mã thoát {rc}\n{se[-1500:]}\n{so[-500:]}")
            p.out = so.strip("\n")
            p.err = se
            cache[p.name] = {"digest": dg, "out": p.out}
            CACHE_DIR.mkdir(exist_ok=True)
            cf.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        if out is not None and out.strip("\n") != p.out:
            raise RuntimeError(f"{p.key}: out khai tay khác đầu ra thật")
    return p


def other(match, **entry):
    """Khối không phải mã chạy được (YAML, XML, Jenkinsfile, WSDL…) ở bài đang soạn: `match` = chuỗi có trong dòng đầu của khối."""
    OTHERS.append((_CUR["lesson"], match, entry))


# ── sinh sổ ──
def gen_screen(lid):
    import yaml
    import screen_code as sc
    f = next((ROOT / "lessons" / "bnx").glob(f"{lid}_*.yaml"))
    _, blocks = sc.blocks_of(f)
    progs = [p for p in PROGRAMS if p.lesson == lid]
    reg, unmatched, used = {}, [], set()
    labs, _ = sc._lab_sources("BNX")
    labkey = f"LAB_{lid}"
    for sid, ti, bi, t in blocks:
        k = f"BNX {lid} {sid} {ti} {bi}"
        frag, hit = sc._dedent_lines(t), None
        for p in progs:
            hl = p.code.split("\n")
            if any(sc._dedent_lines("\n".join(hl[i:i + len(frag)])) == frag for i in range(len(hl) - len(frag) + 1)):
                hit = {"sha": sc.digest(t), "kind": "fragment", "within": f"src:BNX:{p.key}", "reason": f"dãy dòng của chương trình {p.name} (nguồn chạy thật hoặc nguồn ghi vào thư mục chạy)"}
                used.add(p.key)
                break
        if hit is None and labkey in labs:
            h = sc._lab_hit("BNX", k, t, {lid: (labkey, labs[labkey])})
            if h:
                hit = h
                used.add(labkey)
        if hit is None:
            want = [l.strip() for l in t.split("\n") if l.strip()]
            same = {v["within"] for kk, v in reg.items() if kk.rsplit(" ", 1)[0] == k.rsplit(" ", 1)[0] and v.get("kind") == "fragment"}
            for p in sorted([q for q in progs if q.out is not None], key=lambda q: f"src:BNX:{q.key}" not in same):
                actual = [l.rstrip() for l in ((p.out or "") + "\n" + getattr(p, "err", "")).split("\n")]
                pos, ok = 0, bool(want)
                for w in want:
                    while pos < len(actual) and not sc._line_match(w, actual[pos]):
                        pos += 1
                    if pos == len(actual):
                        ok = False
                        break
                    pos += 1
                if ok:
                    hit = {"sha": sc.digest(t), "kind": "output", "of": f"src:BNX:{p.key}", "reason": f"đầu ra thật của chương trình {p.name} (dòng khớp cả dòng, đúng thứ tự; … là đoạn lược)"}
                    used.add(p.key)
                    break
        if hit is None:
            first = t.split("\n")[0]
            for ls, m, e in OTHERS:
                if ls == lid and m in t:
                    hit = dict(e, sha=sc.digest(t))
                    break
        if hit:
            reg[k] = hit
        else:
            unmatched.append((k, t.split("\n")[0][:80]))
    sources = {}
    for p in progs:
        e = {"lang": p.lang}
        if p.lang == "java":
            e["java_class"] = p.extra.get("java_class") or p.name
        if p.kind == "other":
            e["kind"] = "other"
            e["reason"] = p.extra.get("reason", f"{p.name}: nguồn cần thư viện ngoài, ghi nguyên văn vào thư mục chạy của chương trình chạy thật")
            e["read_check"] = p.extra.get("read_check", "Biên dịch và chạy cùng chương trình bash đi kèm (khối `files`); khớp từng ký tự đầu ra.")
        else:
            e["timeout"] = p.extra.get("timeout", 120)
            e["reason"] = p.extra.get("reason", f"{p.name}: chạy nguyên văn.")
            e["claims"] = p.extra.get("claims", [f"đầu ra thật của {p.name}"])
            e["expect_stdout"] = p.out
        if p.files:
            e["files"] = {fn: f"src:BNX:{find(lid, r).key}" for fn, r in p.files.items()}
        for kx in ("shim_sqlite3", "unverified_claims"):
            if kx in p.extra:
                e[kx] = p.extra[kx]
        e["code"] = p.code
        sources[p.key] = e
    if labkey in labs and labkey in used:
        sources[labkey] = labs[labkey]
    # nguồn Java kind other được dùng gián tiếp qua files nên luôn giữ
    outp = ROOT / "audit" / "bnx" / "screen" / f"{lid.lower()}.yaml"
    hdr = (f"# Sổ mã trên màn hình bài BNX {lid} (đợt BNX2, sinh bằng audit/bnx/lib2.py gen-screen {lid}; người điều phối gộp vào audit/review/screen_code/BNX.yaml).\n"
           "# Mã là hằng ở audit/bnx/src/ của bài; đầu ra là đầu ra THẬT (đệm ở audit/bnx/progcache). Thiếu thư viện ngoài (audit/bnx/deps) → nguồn thoát 97, NOT_VERIFIED.\n")
    outp.write_text(hdr + yaml.safe_dump({"blocks": reg, "sources": sources}, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8", newline="\n")
    print(f"{lid}: {len(blocks)} khối, ghi {len(reg)}, nguồn {len(sources)}, chưa khớp {len(unmatched)}")
    for k, first in unmatched:
        print("  CHƯA KHỚP", k, "|", first)
    return not unmatched


def verify_programs(rec, lid):
    """Dùng ở audit/bnx/ver/lNN.py: chạy lại MỌI chương trình (không đệm), so với đầu ra đã hiện; thiếu thư viện → SKIP."""
    for p in [q for q in PROGRAMS if q.lesson == lid and q.kind == "run"]:
        try:
            rc, so, se = p.execute()
        except FileNotFoundError as ex:
            rec(lid, None, f"{p.name}: thiếu công cụ {ex}")
            continue
        if rc == 97 or "NOT_VERIFIED" in se:
            rec(lid, None, f"{p.name}: NOT_VERIFIED (thiếu thư viện)")
            continue
        rec(lid, rc == 0 and so.strip("\n") == p.out, f"{p.name}: chạy lại cho đúng đầu ra đã hiện (rc={rc})")


def practice_steps2(*a, **kw):
    """labkit.practice_steps, nhưng step gợi ý (thứ 3) xoá bảng trước: kết quả mong đợi dài không đè lên gợi ý (lỗi tràn khung ở L30)."""
    from labkit import practice_steps
    steps = practice_steps(*a, **kw)
    for st_ in steps[2:]:
        st_["clear"] = True
    return steps


def practice_steps_giay(st_, course, lid, task_html, task_say, expected, hint_html="", hint_say="", pause=120):
    """Cảnh Tự làm cho bài GIẤY BÚT (loi_giai.md, không có lệnh chấm cham.sh): đề + dừng; đáp án để đối chiếu; gợi ý."""
    from labkit import out_html
    import html as _h
    s1 = st_(task_html, task_say, pause=pause)
    s2 = st_(out_html(expected, "Đáp án để đối chiếu")
             + f'<p class="note">Bài giấy bút: so từng dòng với <code>labs/{course.upper()}/{lid.upper()}/loi_giai.md</code> (có cả cách tính).</p>',
             "Đây là đáp án để đối chiếu. Bài này làm bằng giấy bút, nên bạn so từng dòng với lời giải trong thư mục thực hành, trong đó có cả cách tính.", clear=True)
    steps = [s1, s2]
    if hint_html:
        steps.append(st_(hint_html, hint_say, clear=True))
    return steps


if __name__ == "__main__":
    import lib2 as me   # cùng thể hiện với bài đã nhập (chạy dưới tên __main__ sẽ có PROGRAMS riêng)
    sys.stdout.reconfigure(encoding="utf-8")
    cmd, lids = sys.argv[1], [a.upper() for a in sys.argv[2:]]
    for lid in lids:
        importlib.import_module(lid.lower())
        if cmd == "gen-screen":
            me.gen_screen(lid)
        elif cmd == "run":
            for p in [q for q in me.PROGRAMS if q.lesson == lid and q.kind == "run"]:
                rc, so, se = p.execute()
                print(f"== {p.key} rc={rc} {'GIỐNG' if so.strip(chr(10)) == p.out else 'KHÁC'}")
                if so.strip(chr(10)) != p.out:
                    print(so)
                    print(se[-800:])
        elif cmd == "show":
            for p in [q for q in me.PROGRAMS if q.lesson == lid]:
                print("=====", p.key, p.kind)
                for i, l in enumerate(p.code.split(chr(10)), 1):
                    print(f"{i:3} {l}")
                if p.kind == "run":
                    print("--- out ---")
                    print(p.out)
