"""Cổng lab (plan AF2, WP1/E53): mọi thư mục labs/<KHOÁ>/<Lxx>/ có đủ tệp, lời giải CHẠY THẬT qua labs/cham.sh (đúng đường người học đi)
và cho đúng mong_doi.txt; mỗi lab được một bài tham chiếu (không mồ côi); chữ kết quả mong đợi hiện trên màn hình (lint E53 kiểm).
Đối chứng âm: một tệp cố tình sai phải bị cham.sh chấm KHÁC.
Dùng: .venv/Scripts/python -B audit/review/lab_gate.py [KHOÁ ...]   (không đối số = mọi khoá)
In một dòng tổng; mã thoát 1 nếu có FAIL."""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
LABS = ROOT / "labs"
BASH = r"C:\Program Files\Git\bin\bash.exe"
if not Path(BASH).exists():
    BASH = "bash"
want = {a.upper() for a in sys.argv[1:]}


def referenced():
    refs = {}
    for f in sorted((ROOT / "lessons").glob("*/L*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        for sc in d.get("scenes") or []:
            lab = str(sc.get("lab") or "").strip().strip("/")
            if lab:
                refs.setdefault(lab, []).append(f.name)
    return refs


def cham(k, l, path):
    p = subprocess.run([BASH, str(LABS / "cham.sh"), k, l, str(path)], capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
    return p.returncode, (p.stdout + p.stderr).strip()


refs = referenced()
npass = nfail = 0
rows = []
for kd in sorted(p for p in LABS.iterdir() if p.is_dir()):
    if want and kd.name.upper() not in want:
        continue
    for ld in sorted(p for p in kd.iterdir() if p.is_dir()):
        rel = f"labs/{kd.name}/{ld.name}"
        errs = []
        for need in ("de.md", "mong_doi.txt"):
            if not (ld / need).is_file():
                errs.append(f"thiếu {need}")
        sols = sorted(ld.glob("loi_giai.*"))
        if len(sols) != 1:
            errs.append(f"cần đúng một loi_giai.*, có {len(sols)}")
        if rel not in refs:
            errs.append("mồ côi: không bài nào có cảnh practice trỏ tới")
        if not errs:
            sol = sols[0]
            exp = (ld / "mong_doi.txt").read_text(encoding="utf-8")
            if not exp.strip():
                errs.append("mong_doi.txt rỗng")
            elif sol.suffix == ".md":
                text = re.sub(r"\s+", " ", sol.read_text(encoding="utf-8"))
                for line in exp.splitlines():
                    w = re.sub(r"\s+", " ", line).strip()
                    if w and w not in text:
                        errs.append(f"loi_giai.md không chứa dòng đáp án “{w[:40]}”")
                        break
            else:
                code, out = cham(kd.name, ld.name, sol)
                if code != 0:
                    errs.append("lời giải KHÔNG cho đúng mong_doi: " + out[:200].replace("\n", " ⏎ "))
                else:
                    # đối chứng âm: sửa lời giải để đầu ra đổi → phải bị chấm KHÁC
                    bad = Path(tempfile.mkdtemp()) / f"x{sol.suffix}"
                    src = sol.read_text(encoding="utf-8")
                    if sol.suffix == ".java":
                        mut = re.sub(r"System\.out\.println\(", 'System.out.println("#"+', src, count=1)
                    elif sol.suffix == ".py":
                        mut = re.sub(r"print\(", 'print("#", ', src, count=1)
                    elif sol.suffix == ".sql":
                        mut = "SELECT 'sai';\n" + src
                    else:
                        mut = "echo sai\n" + src
                    bad.write_text(mut, encoding="utf-8")
                    c2, _ = cham(kd.name, ld.name, bad)
                    if c2 == 0:
                        errs.append("đối chứng âm: tệp cố tình sai vẫn được chấm ĐÚNG (cổng chấm vô hiệu)")
        if errs:
            nfail += 1
            rows.append(f"FAIL {rel}: " + "; ".join(errs))
        else:
            npass += 1
for r in rows:
    print(r)
orph = sorted(set(refs) - {f"labs/{k.name}/{l.name}" for k in LABS.iterdir() if k.is_dir() for l in k.iterdir() if l.is_dir()})
for o in orph:
    print(f"FAIL {o}: bài {refs[o]} trỏ tới thư mục lab không tồn tại")
    nfail += 1
print(f"lab_gate: {npass} PASS · {nfail} FAIL ({len(refs)} lab được bài tham chiếu)")
sys.exit(1 if nfail else 0)
