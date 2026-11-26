"""Phần A (L05, L06, L07, L14): bài sinh từ mẫu audit/cs112/src/Lxx_*.tpl.yaml + hình SVG một dòng.
Lệnh `extract` trích hình ra audit/cs112/fig/<Lxx>_<TÊN>.svg từ bài ĐANG CÓ (một lần, trước khi sửa mẫu), kiểm mẫu cũ + hình = bài cũ.
Lệnh `gen Lxx` ghép lại mẫu + hình thành bài bằng fill_tpl.py (không sửa bài sinh ra bằng tay).
Dùng: .venv/Scripts/python -B audit/cs112/regen_a.py extract|gen L05 [L06 …]"""
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1])); import _frozen  # noqa: E402,F401
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "audit" / "cs112" / "src"
FIG = ROOT / "audit" / "cs112" / "fig"
TPL = {"L05": "L05_cay", "L06": "L06_bam_dong", "L07": "L07_do_thi", "L14": "L14_quay_lui"}


def lesson_path(lid):
    return next((ROOT / "lessons" / "cs112").glob(lid + "_*.yaml"))


def rd(p):
    return p.read_bytes().decode("utf-8").replace("\r\n", "\n")


def extract(lid):
    tpl = rd(SRC / (TPL[lid] + ".tpl.yaml"))
    les = rd(lesson_path(lid))
    parts = re.split(r"\{\{([A-Za-z0-9_]+)\}\}", tpl)
    lits, names = parts[0::2], parts[1::2]
    pos = 0
    assert les.startswith(lits[0]), "bài không bắt đầu như mẫu"
    pos = len(lits[0])
    for i, name in enumerate(names):
        nxt = lits[i + 1]
        j = les.index(nxt, pos) if nxt else len(les)
        svg = les[pos:j]
        assert "\n" not in svg, f"{lid} {name}: hình nhiều dòng"
        (FIG / f"{lid}_{name}.svg").write_text(svg, encoding="utf-8", newline="")
        pos = j + len(nxt)
    assert pos == len(les), "còn dư văn bản cuối bài"
    print(lid, "trích", len(names), "hình:", names)


def gen(lid):
    tpl = SRC / (TPL[lid] + ".tpl.yaml")
    names = re.findall(r"\{\{([A-Za-z0-9_]+)\}\}", tpl.read_text(encoding="utf-8"))
    args = [f"{n}={FIG / (lid + '_' + n + '.svg')}" for n in dict.fromkeys(names)]
    py = ROOT / ".venv" / "Scripts" / "python.exe"
    subprocess.run([str(py), "-B", str(ROOT / "audit" / "cs112" / "fill_tpl.py"), str(tpl), str(lesson_path(lid))] + args, check=True)


if __name__ == "__main__":
    cmd, ids = sys.argv[1], sys.argv[2:]
    for i in ids:
        (extract if cmd == "extract" else gen)(i)
