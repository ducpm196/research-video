"""Sinh sổ screen_code cho CS115 (WP5, 2026-11-14): audit/review/screen_code/CS115.yaml.
Khối mã trên màn hình của CS115 chỉ là (a) dữ liệu đề của cảnh `practice` (danh sách Python hoặc bảng dữ liệu) và
(b) "Kết quả mong đợi" của lab. (b) là `output of: src:CS115:LAB_Lxx` với nguồn = lời giải thật của lab (labs/CS115/Lxx/loi_giai.py),
được cổng chạy thật và so từng dòng; (a) là `syntax python` (danh sách) hoặc `pseudo` (bảng dữ liệu viết tay).
Chạy: .venv/Scripts/python -B audit/cs115/gen_screen_cs115.py   (ghi sổ rồi gọi `screen_code.py check --course CS115`)."""
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SC = ROOT / "audit" / "review" / "screen_code.py"
OUT = ROOT / "audit" / "review" / "screen_code" / "CS115.yaml"


def py(*a):
    return subprocess.run([sys.executable, "-B", str(SC), *a], capture_output=True, text=True, encoding="utf-8", cwd=ROOT, env={"PYTHONIOENCODING": "utf-8", "PATH": __import__("os").environ["PATH"]})


def main():
    # 1) dựng sổ rỗng để cổng liệt kê MISSING kèm sha
    OUT.write_text("blocks: {}\n", encoding="utf-8")
    r = py("check", "--course", "CS115")
    rows = []
    for ln in r.stdout.splitlines():
        m = re.match(r"MISSING (CS115 L\d+ \S+ \d+ \d+) sha=([0-9a-f]{16}) \| (.*)", ln)
        if m:
            rows.append((m.group(1), m.group(2), m.group(3)))
    if not rows:
        print(r.stdout[-400:])
        raise SystemExit("không có khối MISSING")
    blocks, sources = {}, {}
    for key, sha, first in rows:
        lid = key.split()[1]
        lab = ROOT / "labs" / "CS115" / lid
        name = f"LAB_{lid}"
        if name not in sources:
            sources[name] = {
                "lang": "python",
                "reason": f"lời giải thật của lab labs/CS115/{lid} (lab_gate chạy lại qua labs/cham.sh); đầu ra là khối 'Kết quả mong đợi' hiện trên màn hình",
                "code": (lab / "loi_giai.py").read_text(encoding="utf-8"),
                "expect_stdout": (lab / "mong_doi.txt").read_text(encoding="utf-8"),
                "claims": ["Kết quả mong đợi (mong_doi.txt): mọi dòng hiện nguyên văn trên màn hình"],
            }
        if first.startswith(("f1: H =",)):
            blocks[key] = {"sha": sha, "kind": "pseudo", "reason": "bảng dữ liệu đề bài viết tay (nhãn hàm, H, v); lời giải của lab khai lại dữ liệu này bằng từ điển Python"}
        elif re.match(r"(he\d|x1, x2, x3|that) ?=", first):
            blocks[key] = {"sha": sha, "kind": "syntax", "lang": "python", "reason": "dữ liệu đề bài là mã Python hợp lệ; lab chép nguyên văn vào lời giải"}
        else:
            blocks[key] = {"sha": sha, "kind": "output", "of": f"src:CS115:{name}", "reason": f"khối kết quả chạy thật của lời giải lab {lid}"}
    OUT.write_text(yaml.safe_dump({"blocks": blocks, "sources": sources}, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8", newline="\n")
    r = py("check", "--course", "CS115")
    print("\n".join(r.stdout.splitlines()[-6:]))
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
