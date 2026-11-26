"""Bộ chấm phụ trợ cho labs/cham.sh v2: so khớp có sai số số thực, gọi hàm (ham.json), bài giấy (.md), và chấm dự án (unittest / Surefire XML)."""
import argparse
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

NUM_RE = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?")


def norm_lines(text: str) -> list[str]:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def lines_close(got_line: str, want_line: str, sai_so: float) -> bool:
    if got_line == want_line:
        return True
    if sai_so <= 0:
        return False
    gm = list(NUM_RE.finditer(got_line))
    wm = list(NUM_RE.finditer(want_line))
    if len(gm) != len(wm) or not gm:
        return False
    if NUM_RE.sub("<N>", got_line) != NUM_RE.sub("<N>", want_line):
        return False
    for a, b in zip(gm, wm):
        try:
            va, vb = float(a.group(0)), float(b.group(0))
        except ValueError:
            return False
        if math.isnan(va) or math.isnan(vb) or abs(va - vb) > sai_so:
            return False
    return True


def compare_outputs(got_text: str, want_text: str, sai_so: float = 0.0) -> tuple[bool, str]:
    got = norm_lines(got_text)
    want = norm_lines(want_text)
    if len(got) != len(want):
        return False, f"so dong lech: duoc {len(got)}, mong doi {len(want)}"
    for i, (g, w) in enumerate(zip(got, want), 1):
        if not lines_close(g, w, sai_so):
            return False, f"dong {i}: mong doi {w!r}, nhan duoc {g!r}"
    return True, f"PASS ({len(want)} dong)"


def _values_match(got, want, sai_so: float) -> bool:
    if isinstance(want, bool) or isinstance(got, bool):
        return got is want
    if isinstance(want, (int, float)) and isinstance(got, (int, float)):
        if sai_so > 0 or isinstance(want, float) or isinstance(got, float):
            tol = sai_so if sai_so > 0 else 1e-9
            return not (math.isnan(got) or math.isnan(want)) and abs(float(got) - float(want)) <= tol
        return got == want
    if isinstance(want, list) and isinstance(got, list):
        return len(got) == len(want) and all(_values_match(g, w, sai_so) for g, w in zip(got, want))
    if isinstance(want, dict) and isinstance(got, dict):
        return set(got.keys()) == set(want.keys()) and all(_values_match(got[k], want[k], sai_so) for k in want)
    return got == want


def check_ham_json(sub_path: Path, ham_path: Path) -> tuple[bool, str]:
    data = json.loads(ham_path.read_text(encoding="utf-8"))
    cases = data.get("cases") if isinstance(data, dict) else data
    if not isinstance(cases, list) or not cases:
        return False, "ham.json rong hoac sai dinh dang"
    parent = str(sub_path.resolve().parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)
    spec = importlib.util.spec_from_file_location("bai_lam", str(sub_path.resolve()))
    if spec is None or spec.loader is None:
        return False, f"khong nap duoc mo-dun {sub_path}"
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        return False, f"loi nap {sub_path.name}: {type(e).__name__}: {e}"
    for idx, item in enumerate(cases, 1):
        goi = item.get("goi")
        if not goi:
            return False, f"ca {idx}: thieu truong 'goi'"
        want = item.get("bang")
        tol = float(item.get("sai_so", 0.0) or 0.0)
        try:
            got = eval(goi, mod.__dict__, {})  # noqa: S307
        except Exception as e:
            return False, f"ca {idx} ({goi}): loi thuc thi {type(e).__name__}: {e}"
        if not _values_match(got, want, tol):
            return False, f"ca {idx} ({goi}): mong doi {want!r}, nhan duoc {got!r}"
    return True, f"PASS ham.json ({len(cases)} ca)"


def check_paper(md_text: str, checklist_text: str) -> tuple[bool, str]:
    norm_md = re.sub(r"\s+", " ", md_text.replace("\r\n", "\n")).strip().lower()
    missing = []
    checked = 0
    for raw in checklist_text.replace("\r\n", "\n").splitlines():
        line = re.sub(r"^\s*[-*]\s*\[[ xX]\]\s*", "", raw).strip()
        if not line or line.startswith("#"):
            continue
        checked += 1
        needle = re.sub(r"\s+", " ", line).strip()
        if needle.lower() not in norm_md:
            missing.append(needle)
    if checked == 0:
        return False, "bang kiem rong"
    if missing:
        return False, f"thieu {len(missing)}/{checked} muc: {missing[0]!r}"
    return True, f"PASS ({checked} muc)"


def check_surefire_xml(report_path: Path, min_tests: int = 1, kiem_dir: Path | None = None, mong_doi: Path | None = None) -> tuple[bool, str]:
    files = sorted(report_path.glob("TEST-*.xml")) if report_path.is_dir() else [report_path]
    files = [f for f in files if f.is_file()]
    if not files:
        return False, f"khong tim thay bao cao XML trong {report_path}"
    allowed_cls = set()
    if kiem_dir and kiem_dir.is_dir():
        for jf in kiem_dir.rglob("*.java"):
            allowed_cls.update(re.findall(r"class\s+([A-Za-z_][A-Za-z0-9_]*)", jf.read_text(encoding="utf-8", errors="replace")))
    tests = failures = errors = skipped = 0
    per_cls = []
    for f in files:
        root = ET.fromstring(f.read_text(encoding="utf-8"))
        suites = [root] if root.tag == "testsuite" else list(root.findall(".//testsuite"))
        for s in suites:
            cname = s.attrib.get("name", f.stem.removeprefix("TEST-"))
            simple = cname.rsplit(".", 1)[-1]
            if allowed_cls and simple not in allowed_cls:
                continue
            t = int(s.attrib.get("tests", 0))
            fl = int(s.attrib.get("failures", 0))
            er = int(s.attrib.get("errors", 0))
            sk = int(s.attrib.get("skipped", 0))
            tests += t
            failures += fl
            errors += er
            skipped += sk
            per_cls.append(f"{simple}: {t} ca, {fl + er} hỏng")
    if tests < min_tests:
        return False, f"it kiem thu hon toi thieu: {tests} < {min_tests}"
    if failures or errors:
        return False, f"FAIL tests={tests} failures={failures} errors={errors} skipped={skipped}"
    if mong_doi and mong_doi.is_file():
        want_txt = mong_doi.read_text(encoding="utf-8")
        if want_txt.strip():
            ok, msg = compare_outputs("\n".join(sorted(per_cls)), "\n".join(sorted(norm_lines(want_txt))))
            if not ok:
                return False, f"lech mong_doi.txt: {msg}"
    return True, f"PASS tests={tests} failures=0 errors=0 skipped={skipped}"


def run_py_project(proj_dir: Path, kiem_dir: Path) -> tuple[bool, str]:
    if not proj_dir.is_dir() or not kiem_dir.is_dir():
        return False, f"thieu thu muc du an ({proj_dir}) hoac kiem ({kiem_dir})"
    env = dict(os.environ)
    env["PYTHONPATH"] = str(proj_dir.resolve()) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    env["PYTHONIOENCODING"] = "utf-8"
    p = subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "unittest", "discover", "-s", str(kiem_dir.resolve()), "-t", str(kiem_dir.resolve())],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=60,
    )
    combined = (p.stdout or "") + "\n" + (p.stderr or "")
    m = re.search(r"Ran\s+(\d+)\s+test", combined)
    cnt = int(m.group(1)) if m else 0
    if p.returncode != 0 or cnt < 1 or "OK" not in combined:
        tail = " | ".join(l.strip() for l in combined.strip().splitlines()[-4:])
        return False, f"FAIL unittest rc={p.returncode} ran={cnt}: {tail}"
    return True, f"PASS unittest ran={cnt}"


def kiem_chuc_nang(fn, cases: list[tuple], sai_so: float = 1e-6) -> None:
    """Tiện ích kiểm từng hàm (args, expected) trong bài lab Python."""
    for idx, (args, want) in enumerate(cases, 1):
        got = fn(*args) if isinstance(args, tuple) else fn(args)
        if not _values_match(got, want, sai_so):
            raise AssertionError(f"ca {idx}: mong doi {want!r}, nhan {got!r}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--so", nargs=2, metavar=("GOT", "WANT"))
    ap.add_argument("--sai-so", type=float, default=0.0)
    ap.add_argument("--ham-json", nargs=2, metavar=("SUB_PY", "HAM_JSON"))
    ap.add_argument("--giay", nargs=2, metavar=("MD", "CHECKLIST"))
    ap.add_argument("--xml", metavar="DIR_OR_FILE")
    ap.add_argument("--kiem", type=Path, default=None)
    ap.add_argument("--mong-doi", type=Path, default=None)
    ap.add_argument("--min-tests", type=int, default=1)
    ap.add_argument("--py-du-an", nargs=2, metavar=("PROJ_DIR", "KIEM_DIR"))
    args = ap.parse_args()

    if args.so:
        ok, msg = compare_outputs(
            Path(args.so[0]).read_text(encoding="utf-8", errors="replace"),
            Path(args.so[1]).read_text(encoding="utf-8", errors="replace"),
            args.sai_so,
        )
    elif args.ham_json:
        ok, msg = check_ham_json(Path(args.ham_json[0]), Path(args.ham_json[1]))
    elif args.giay:
        ok, msg = check_paper(
            Path(args.giay[0]).read_text(encoding="utf-8", errors="replace"),
            Path(args.giay[1]).read_text(encoding="utf-8", errors="replace"),
        )
    elif args.xml:
        ok, msg = check_surefire_xml(Path(args.xml), args.min_tests, args.kiem, args.mong_doi)
    elif args.py_du_an:
        ok, msg = run_py_project(Path(args.py_du_an[0]), Path(args.py_du_an[1]))
    else:
        ap.print_help()
        return 2
    print(msg)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
