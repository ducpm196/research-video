"""Cổng lab (plan AF5, WP-0.12): mọi thư mục labs/<KHOÁ>/<Lxx>/ khớp với labs/CONTRACT.yaml, có đủ tệp,
lời giải CHẠY THẬT qua labs/cham.sh (cả ca công khai lẫn ca_an/, hoặc dự án du_an/), mỗi lab được một bài tham chiếu;
đối chứng âm: tệp cố tình sai hoặc in cứng (hardcode khi có ca_an/) phải bị cham.sh từ chối.
Dùng: .venv/Scripts/python -B audit/review/lab_gate.py [--root DIR] [--du-an] [--no-contract] [KHOÁ ...]
In một dòng tổng; mã thoát 1 nếu có FAIL."""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
BASH = r"C:\Program Files\Git\bin\bash.exe"
if not Path(BASH).exists():
    BASH = "bash"

LAB_ENV = dict(os.environ)
if not shutil.which("sqlite3"):
    for cand in (
        Path(r"C:\tools\sqlite"),
        *sorted(Path(r"C:\Program Files\NVIDIA Corporation").glob("Nsight*/host-windows-x64"), reverse=True),
    ):
        if (cand / "sqlite3.exe").is_file():
            LAB_ENV["PATH"] = str(cand) + os.pathsep + LAB_ENV.get("PATH", "")
            print(f"[INFO] lab_gate: dùng sqlite3 tại {cand / 'sqlite3.exe'}")
            break
if not shutil.which("gcc") and Path(r"C:\tools\w64devkit\bin\gcc.exe").is_file():
    LAB_ENV["PATH"] = r"C:\tools\w64devkit\bin" + os.pathsep + LAB_ENV["PATH"]


def referenced():
    refs = {}
    for f in sorted((ROOT / "lessons").glob("*/L*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        for sc in d.get("scenes") or []:
            lab = str(sc.get("lab") or "").strip().strip("/")
            if lab:
                refs.setdefault(lab, []).append(f.name)
    return refs


def cham_cmd(lab_dir: Path, *extra: str):
    p = subprocess.run(
        [BASH, str(ROOT / "labs" / "cham.sh"), str(lab_dir), *extra],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=ROOT,
        env=LAB_ENV,
    )
    return p.returncode, (p.stdout + p.stderr).strip()


def make_hardcode_sub(sol: Path, exp_text: str, tmp: Path) -> Path | None:
    """Tạo lời giải giả chỉ in đáp án công khai (bỏ qua stdin) để kiểm chống hardcode với ca_an/."""
    lines = exp_text.rstrip("\n").splitlines()
    ext = sol.suffix.lower()
    out_f = tmp / f"hc{ext}"
    if ext == ".py":
        out_f.write_text("for ln in " + repr(lines) + ":\n    print(ln)\n", encoding="utf-8", newline="\n")
    elif ext == ".js":
        out_f.write_text("for (const ln of " + repr(lines) + ") console.log(ln);\n", encoding="utf-8", newline="\n")
    elif ext == ".sh":
        body = "\n".join(f"printf '%s\\n' '{ln.replace(chr(39), chr(39)+chr(34)+chr(39)+chr(34)+chr(39))}'" for ln in lines)
        out_f.write_text(body + "\n", encoding="utf-8", newline="\n")
    elif ext == ".c":
        escaped = "\\n".join(ln.replace("\\", "\\\\").replace('"', '\\"') for ln in lines)
        out_f.write_text(f'#include <stdio.h>\nint main(void){{printf("{escaped}\\n");return 0;}}\n', encoding="utf-8", newline="\n")
    elif ext == ".java":
        m = re.search(r"public\s+class\s+([A-Za-z_][A-Za-z0-9_]*)", sol.read_text(encoding="utf-8", errors="replace"))
        cls = m.group(1) if m else "Main"
        out_f = tmp / f"{cls}.java"
        prints = " ".join(f'System.out.println("{ln.replace(chr(92), chr(92)*2).replace(chr(34), chr(92)+chr(34))}");' for ln in lines)
        out_f.write_text(f"public class {cls} {{ public static void main(String[] a){{ {prints} }} }}\n", encoding="utf-8", newline="\n")
    else:
        return None
    return out_f


def mutated_bad(sol: Path, tmp: Path) -> Path:
    bad = tmp / f"x{sol.suffix}"
    src = sol.read_text(encoding="utf-8")
    if sol.suffix == ".java":
        mut = re.sub(r"System\.out\.println\(", 'System.out.println("#"+', src, count=1)
        if mut == src:
            mut = re.sub(r"(public\s+static\s+void\s+main\s*\([^)]*\)\s*\{)", r'\1\nSystem.out.println("#sai");', src, count=1)
    elif sol.suffix == ".py":
        mut = re.sub(r"print\(", 'print("#", ', src, count=1)
    elif sol.suffix == ".sql":
        mut = "SELECT 'sai';\n" + src
    elif sol.suffix == ".c":
        if "printf(" in src:
            mut = re.sub(r"\bprintf\(", 'printf("#", ', src, count=1)
        else:
            mut = re.sub(r"(int\s+main\s*\([^)]*\)\s*\{)", r'\1\n    puts("#sai");', src, count=1)
    elif sol.suffix == ".js":
        mut = "console.log('#sai');\n" + src
    else:
        mut = "echo sai\n" + src
    bad.write_text(mut, encoding="utf-8", newline="\n")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("courses", nargs="*")
    ap.add_argument("--root", type=Path, default=ROOT / "labs")
    ap.add_argument("--du-an", action="store_true")
    ap.add_argument("--no-contract", action="store_true")
    args = ap.parse_args()

    labs_dir = args.root.resolve()
    want = {a.upper() for a in args.courses}
    default_root = (labs_dir == (ROOT / "labs").resolve())
    refs = referenced() if default_root else {}

    contract = {}
    if default_root and not args.no_contract:
        cf = labs_dir / "CONTRACT.yaml"
        if not cf.is_file():
            print("FAIL thiếu labs/CONTRACT.yaml")
            return 1
        contract = (yaml.safe_load(cf.read_text(encoding="utf-8")) or {}).get("labs") or {}

    npass = nfail = 0
    rows = []
    seen_keys = set()

    if default_root:
        targets = [
            (kd.name, ld.name, ld)
            for kd in sorted(p for p in labs_dir.iterdir() if p.is_dir() and not p.name.startswith("."))
            if not want or kd.name.upper() in want
            for ld in sorted(p for p in kd.iterdir() if p.is_dir())
        ]
    else:
        # --root trỏ tới thư mục fixture chứa trực tiếp các thư mục lab (vd: tests/fixtures/labs)
        targets = [
            (ld.name, ld.name, ld)
            for ld in sorted(p for p in labs_dir.iterdir() if p.is_dir() and not p.name.startswith("."))
            if not want or ld.name.upper() in want
        ]

    for kname, lname, ld in targets:
        key = f"{kname}/{lname}"
        rel = f"labs/{key}" if default_root else str(ld)
        seen_keys.add(key)
        errs = []

        is_du_an = (ld / "loi_giai").is_dir() or (ld / "kiem").is_dir()
        if is_du_an and not args.du_an and not (contract.get(key, {}).get("mode") == "du_an"):
            continue

        if contract:
            ce = contract.get(key)
            if not ce:
                errs.append("thiếu mục trong labs/CONTRACT.yaml")
            else:
                ca_dir = ld / "ca_an"
                has_ca = ca_dir.is_dir() and (
                    bool(list(ca_dir.glob("*.in")))
                    or bool(list(ca_dir.glob("in_*.txt")))
                    or bool(list(ca_dir.glob("seed_*.sql")))
                    or (ca_dir / "ham.json").is_file()
                )
                if bool(ce.get("ca_an")) != has_ca:
                    errs.append(f"CONTRACT ca_an={ce.get('ca_an')} lệch thực tế ({has_ca})")

        if is_du_an:
            if not (ld / "kiem").is_dir() and not (ld / "loi_giai" / "pom.xml").is_file():
                errs.append("dự án thiếu kiem/")
            if not (ld / "loi_giai").is_dir():
                errs.append("dự án thiếu thư mục loi_giai/")
            if default_root and rel not in refs:
                errs.append("mồ côi: không bài nào có cảnh practice trỏ tới")
            if not errs:
                c, out = cham_cmd(ld, "--du-an", str(ld / "loi_giai"))
                if c != 0:
                    errs.append("dự án loi_giai FAIL: " + out[:200].replace("\n", " ⏎ "))
                elif (ld / "loi_sai").is_dir():
                    c2, _ = cham_cmd(ld, "--du-an", str(ld / "loi_sai"))
                    if c2 == 0:
                        errs.append("đối chứng âm dự án loi_sai vẫn PASS")
        else:
            if default_root:
                for need in ("de.md", "mong_doi.txt"):
                    if not (ld / need).is_file():
                        errs.append(f"thiếu {need}")
            elif not (ld / "mong_doi.txt").is_file() and not (ld / "bang_kiem.md").is_file():
                errs.append("thiếu mong_doi.txt / bang_kiem.md")

            sols = sorted(ld.glob("loi_giai.*"))
            if len(sols) != 1:
                errs.append(f"cần đúng một loi_giai.*, có {len(sols)}")
            if default_root and rel not in refs:
                errs.append("mồ côi: không bài nào có cảnh practice trỏ tới")
            if not errs:
                sol = sols[0]
                exp_p = (ld / "bang_kiem.md") if (sol.suffix == ".md" and (ld / "bang_kiem.md").is_file()) else (ld / "mong_doi.txt")
                exp = exp_p.read_text(encoding="utf-8")
                if not exp.strip():
                    errs.append(f"{exp_p.name} rỗng")
                elif sol.suffix == ".md":
                    c, out = cham_cmd(ld, str(sol))
                    if c != 0:
                        errs.append("loi_giai.md FAIL: " + out[:200])
                    else:
                        bad_md = Path(tempfile.mkdtemp()) / "empty.md"
                        bad_md.write_text("# trong\n", encoding="utf-8")
                        c2, _ = cham_cmd(ld, str(bad_md))
                        if c2 == 0:
                            errs.append("đối chứng âm .md rỗng vẫn PASS")
                else:
                    c, out = cham_cmd(ld, str(sol))
                    if c != 0:
                        errs.append("lời giải KHÔNG cho đúng mong_doi: " + out[:200].replace("\n", " ⏎ "))
                    else:
                        tmp = Path(tempfile.mkdtemp())
                        bad = mutated_bad(sol, tmp)
                        c2, _ = cham_cmd(ld, str(bad))
                        if c2 == 0:
                            errs.append("đối chứng âm: tệp cố tình sai vẫn được chấm ĐÚNG (cổng chấm vô hiệu)")
                        if (ld / "ca_an").is_dir():
                            ins = sorted((ld / "ca_an").glob("*.in"))
                            txts = sorted((ld / "ca_an").glob("in_*.txt"))
                            seeds = sorted((ld / "ca_an").glob("seed_*.sql"))
                            has_ham = (ld / "ca_an" / "ham.json").is_file()
                            if not (ins or txts or seeds or has_ham):
                                errs.append("thư mục ca_an/ rỗng")
                            for inf in ins:
                                if not inf.with_suffix(".out").is_file():
                                    errs.append(f"ca_an thiếu {inf.with_suffix('.out').name}")
                            for tin in txts:
                                k = tin.stem.removeprefix("in_")
                                if not (ld / "ca_an" / f"out_{k}.txt").is_file():
                                    errs.append(f"ca_an thiếu out_{k}.txt")
                            for sin in seeds:
                                k = sin.stem.removeprefix("seed_")
                                if not (ld / "ca_an" / f"out_{k}.txt").is_file():
                                    errs.append(f"ca_an thiếu out_{k}.txt")
                            hc = make_hardcode_sub(sol, exp, tmp)
                            if hc is not None:
                                c3, _ = cham_cmd(ld, str(hc))
                                if c3 == 0:
                                    errs.append("chống hardcode: lời giải in cứng mong_doi công khai vẫn PASS qua ca_an/")

        if errs:
            nfail += 1
            rows.append(f"FAIL {rel}: " + "; ".join(errs))
        else:
            npass += 1

    if contract and not want:
        for k in sorted(set(contract) - seen_keys):
            rows.append(f"FAIL labs/{k}: có trong CONTRACT.yaml nhưng thiếu thư mục")
            nfail += 1
    if default_root:
        existing = {f"labs/{k.name}/{l.name}" for k in labs_dir.iterdir() if k.is_dir() and not k.name.startswith(".") for l in k.iterdir() if l.is_dir()}
        for o in sorted(set(refs) - existing):
            if want and o.split("/")[1].upper() not in want:
                continue
            rows.append(f"FAIL {o}: bài {refs[o]} trỏ tới thư mục lab không tồn tại")
            nfail += 1

    for r in rows:
        print(r)
    print(f"lab_gate: {npass} PASS · {nfail} FAIL ({len(refs)} lab được bài tham chiếu)")
    return 1 if nfail else 0


if __name__ == "__main__":
    raise SystemExit(main())
