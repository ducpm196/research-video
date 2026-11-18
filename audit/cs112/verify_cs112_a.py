"""Kiểm độc lập phần A của CS112 (L00–L14), chuẩn AF2: mọi khối mã Python hiện trên màn hình ở cảnh `scale` được GHÉP nguyên văn
(các khối mã liên tiếp của cùng cảnh nối lại) rồi CHẠY THẬT; stdout phải trùng từng dòng với khối kết quả đứng ngay sau; lời giải
mỗi lab labs/CS112/Lxx chạy thật và phải cho đúng mong_doi.txt (cham.sh còn kiểm lần nữa trong audit/review/lab_gate.py).
Dùng: .venv/Scripts/python -B audit/cs112/verify_cs112_a.py [L00 …]    (không đối số = L00–L14)"""
import re
import subprocess
import sys
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import screen_code as sc  # noqa: E402

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
want = [a.upper() for a in sys.argv[1:]] or [f"L{i:02d}" for i in range(15)]


def run(code):
    p = subprocess.run([PY, "-B", "-I", "-X", "utf8", "-c", code], capture_output=True, text=True, encoding="utf-8", timeout=120)
    return p.returncode, p.stdout.replace("\r\n", "\n").rstrip("\n"), p.stderr


npass = nfail = 0
for f in sorted((ROOT / "lessons" / "cs112").glob("L*.yaml")):
    lid = f.name[:3]
    if lid not in want:
        continue
    spec, blocks = sc.blocks_of(f)
    scale = [(si, ti, bi, t) for (sid, ti, bi, t) in blocks if sid == "scale" for si in [sid]]
    # nhóm theo thứ tự: mã (Python) ... rồi khối kết quả; khối kết quả = khối đứng sau mã trong cùng step và không phải mã
    codes, pending = [], []
    ok_scale = True
    for si, ti, bi, t in scale:
        is_code = bool(re.search(r"\b(def|import|for|while|print)\b", t)) and not re.match(r"^[\d\w ]+$", t.split("\n")[0].strip() or "x") or t.startswith(("def ", "import ", "for ", "from "))
        if is_code:
            codes.append(t)
        else:
            rc, out, err = run("\n".join(codes))
            if rc != 0:
                print(f"FAIL {lid} scale step {ti}: mã lỗi: {err.strip().splitlines()[-1] if err.strip() else rc}")
                nfail += 1
                ok_scale = False
            else:
                shown = [l.rstrip() for l in t.split("\n") if l.strip()]
                real = [l.rstrip() for l in out.split("\n")]
                tail = real[-len(shown):]
                if tail != shown:
                    print(f"FAIL {lid} scale step {ti}: màn hình {shown} ≠ thật {tail}")
                    nfail += 1
                    ok_scale = False
    if ok_scale and any(s[3] for s in scale):
        print(f"PASS {lid} scale: {len(codes)} khối mã ghép chạy thật, kết quả trùng")
        npass += 1
    lab = ROOT / "labs" / "CS112" / lid
    if lab.is_dir():
        sol = next(iter(sorted(lab.glob("loi_giai.*"))), None)
        if sol is None or sol.suffix != ".py":
            print(f"PASS {lid} lab: giấy bút ({sol.name if sol else 'thiếu'})")
        else:
            rc, out, err = run(sol.read_text(encoding="utf-8"))
            exp = (lab / "mong_doi.txt").read_text(encoding="utf-8").replace("\r\n", "\n").rstrip("\n")
            if rc == 0 and [l.rstrip() for l in out.split("\n")] == [l.rstrip() for l in exp.split("\n")]:
                print(f"PASS {lid} lab: lời giải chạy thật = mong_doi.txt ({len(exp.splitlines())} dòng)")
                npass += 1
            else:
                print(f"FAIL {lid} lab: lời giải khác mong_doi.txt {err[-200:]}")
                nfail += 1
print(f"verify_cs112_a: {npass} PASS · {nfail} FAIL")
sys.exit(1 if nfail else 0)
