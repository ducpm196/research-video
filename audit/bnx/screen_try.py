"""Thử sổ mã trên màn hình của một bài BNX TRƯỚC khi người điều phối gộp vào audit/review/screen_code/BNX.yaml.
Chép mọi sổ sang thư mục tạm, gộp audit/bnx/screen/lNN.yaml (các bài được chỉ định, hoặc mọi bài) vào BNX.yaml tạm, rồi chạy
`screen_code.py check --course BNX -v` với SC_REGDIR trỏ tới thư mục tạm. Dùng: python -B audit/bnx/screen_try.py [L03 L04 …]
Gộp thật (người điều phối): python -B audit/bnx/screen_try.py --merge"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / "audit" / "review" / "screen_code"
HEAD = "# Sổ mã trên màn hình khoá BNX (audit/review/screen_code.py). Gộp từ audit/bnx/screen/lNN.yaml bằng audit/bnx/screen_try.py --merge.\n"


def merged(want):
    blocks, sources = {}, {}
    base = REG / "BNX.yaml"
    if base.exists():
        b = yaml.safe_load(base.read_text(encoding="utf-8")) or {}
        blocks.update(b.get("blocks") or {})
        sources.update(b.get("sources") or {})
    for f in sorted((ROOT / "audit" / "bnx" / "screen").glob("l*.yaml")):
        if want and f.stem.upper() not in want:
            continue
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for k, v in (d.get("blocks") or {}).items():
            blocks[k] = v
        for k, v in (d.get("sources") or {}).items():
            sources[k] = v
    out = {"blocks": dict(sorted(blocks.items()))}
    if sources:
        out["sources"] = dict(sorted(sources.items()))
    return HEAD + yaml.dump(out, allow_unicode=True, sort_keys=False, width=140)


def main():
    args = sys.argv[1:]
    if "--merge" in args:
        (REG / "BNX.yaml").write_text(merged(set()), encoding="utf-8", newline="\n")
        print("đã gộp vào", REG / "BNX.yaml")
        return 0
    want = {a.upper() for a in args}
    with tempfile.TemporaryDirectory() as d:
        for f in REG.glob("*.yaml"):
            shutil.copy(f, d)
        Path(d, "BNX.yaml").write_text(merged(want), encoding="utf-8", newline="\n")
        env = dict(os.environ, SC_REGDIR=d, PYTHONIOENCODING="utf-8")
        return subprocess.run([sys.executable, "-B", str(ROOT / "audit" / "review" / "screen_code.py"), "check", "--course", "BNX", "-v"], env=env).returncode


if __name__ == "__main__":
    sys.exit(main())
