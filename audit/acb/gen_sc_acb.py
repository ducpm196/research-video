"""Thêm vào sổ audit/review/screen_code/ACB.yaml các khối mã MỚI (cảnh `code` và đầu ra mong đợi của lab), bằng văn bản (không dump lại cả tệp).
Mỗi cảnh `code` = MỘT nguồn chạy thật `Lxx_code` (ghép các khối mã theo thứ tự) + expect_stdout (ghép các khối kết quả); khối mã là `fragment within`,
khối kết quả là `output of`. Lab: nguồn `LAB_Lxx` = loi_giai.py, expect_stdout = mong_doi.txt; khối mong đợi là `output of` nguồn đó.
Chạy lại được (xoá phần GEN-WP4 cũ rồi ghi lại). Dùng sau khi sửa khối mã của cảnh `code` hoặc lab:
  .venv/Scripts/python -B audit/acb/gen_sc_acb.py   rồi   audit/review/screen_code.py check --course ACB"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "review"))
sys.stdout.reconfigure(encoding="utf-8")
import screen_code as sc  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / "audit" / "review" / "screen_code" / "ACB.yaml"
raw = REG.read_bytes().decode("utf-8")
crlf = "\r\n" in raw
text = raw.replace("\r\n", "\n")
# bỏ phần sinh trước đó
text = re.sub(r"\n  # GEN-WP4 begin.*?# GEN-WP4 end\n", "\n", text, flags=re.S)
text = re.sub(r"\n  # GEN-WP4-SRC begin.*?# GEN-WP4-SRC end\n?", "\n", text, flags=re.S)

import hashlib, yaml  # noqa: E402
# lấy sha từ chính bộ trích của công cụ
rows = []
import subprocess
out = subprocess.run([sys.executable, "-B", str(ROOT / "audit/review/screen_code.py"), "inventory", "--course", "ACB"], capture_output=True, text=True, encoding="utf-8",
                     env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"}).stdout
sha = {}
for ln in out.splitlines():
    p = ln.split("\t")
    if len(p) >= 7 and p[0] == "ACB":
        sha[f"ACB {p[1]} {p[2]} {p[3]} {p[4]}"] = p[6]

blocks_txt, src_txt = [], []


def ind(s, n):
    return "\n".join((" " * n + x) if x.strip() else "" for x in s.split("\n"))


import html as _h
def blocks_of_step(show):
    res = []
    for m in re.finditer(r'<div class="code">((?:<div>.*?</div>)+)</div>', show, re.S):
        lines = re.findall(r"<div>(.*?)</div>", m.group(1), re.S)
        res.append("\n".join(_h.unescape(x).rstrip() for x in lines))
    return res


for n in range(9):
    lid = f"L0{n}"
    d = yaml.safe_load(next((ROOT / "lessons" / "acb").glob(f"{lid}_*.yaml")).read_text(encoding="utf-8"))
    scn = {s["id"]: s for s in d["scenes"]}
    if "code" in scn:
        codes, outs, ent = [], [], []
        for si, st in enumerate(scn["code"]["steps"]):
            bl = blocks_of_step(str(st.get("show", "")))
            if not bl:
                continue
            if len(bl) >= 2:
                codes.append(bl[0]); outs.append(bl[-1])
                ent.append((f"ACB {lid} code {si} 0", "frag")); ent.append((f"ACB {lid} code {si} {len(bl) - 1}", "out"))
            else:
                codes.append(bl[0]); ent.append((f"ACB {lid} code {si} 0", "frag"))
        src_txt.append(f"  {lid}_code:\n    lang: python\n    reason: >-\n      Cảnh `code` của bài {lid}: các khối mã Python hiện trên màn hình ghép NGUYÊN VĂN theo thứ tự (mô phỏng, chạy thật bằng Python/sqlite3/hashlib/heapq của máy; "
                       f"hệ thống ngân hàng thật không chạy trên máy). Khối kết quả là đầu ra thật của chương trình này.\n    code: |\n" + ind("\n\n".join(codes), 6)
                       + "\n    expect_stdout: |\n" + ind("\n".join(outs), 6) + "\n    no_claim_reason: \"đầu ra so với expect_stdout\"\n")
        for key, kind in ent:
            assert key in sha, key
            if kind == "frag":
                blocks_txt.append(f'  "{key}":\n    sha: {sha[key]}\n    kind: fragment\n    within: src:ACB:{lid}_code\n    reason: "khối mã của cảnh code {lid}, là dãy dòng liên tiếp của nguồn chạy thật (mô phỏng, ghi rõ trên màn hình)"\n')
            else:
                blocks_txt.append(f'  "{key}":\n    sha: {sha[key]}\n    kind: output\n    of: src:ACB:{lid}_code\n    reason: "đầu ra THẬT của chương trình {lid}_code (mô phỏng chạy bằng Python)"\n')
    # lab
    lab = ROOT / "labs" / "ACB" / lid
    sol = (lab / "loi_giai.py")
    if sol.exists():
        key = f"ACB {lid} practice 1 0"
        assert key in sha, key
        blocks_txt.append(f'  "{key}":\n    sha: {sha[key]}\n    kind: output\n    of: src:ACB:LAB_{lid}\n    reason: "kết quả mong đợi của lab LAB_{lid}: đầu ra THẬT của lời giải (chạy như labs/cham.sh)"\n')
        src_txt.append(f"  LAB_{lid}:\n    lang: python\n    code: |\n" + ind(sol.read_text(encoding="utf-8").rstrip("\n"), 6)
                       + "\n    expect_stdout: |\n" + ind((lab / "mong_doi.txt").read_text(encoding="utf-8").rstrip("\n"), 6)
                       + "\n    no_claim_reason: \"đầu ra so với expect_stdout\"\n")

# chèn: khối vào cuối mục blocks (ngay trước dòng `sources:`), nguồn vào cuối tệp
i = text.index("\nsources:\n")
text = text[:i] + "\n  # GEN-WP4 begin (audit/acb: sinh bởi gen_sc_acb.py, 2026-11-14)\n" + "".join(blocks_txt) + "  # GEN-WP4 end\n" + text[i:]
text = text.rstrip("\n") + "\n  # GEN-WP4-SRC begin\n" + "".join(src_txt) + "  # GEN-WP4-SRC end\n"
REG.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))
print("đã ghi", len(blocks_txt), "mục khối,", len(src_txt), "nguồn")
