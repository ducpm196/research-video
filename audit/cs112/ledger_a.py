"""Điền sổ screen_code CS112 cho các khối MỚI của phần A (L00–L14) từ audit/cs112/ledger_specs_a.yaml.
Dùng: .venv/Scripts/python -B audit/cs112/ledger_a.py          (ghi vào audit/review/screen_code/CS112.yaml; chỉ đụng khoá L00–L14)
Spec: blocks: {"L00 scale 0 0": {kind: run, lang: python, auto: true}}  — auto: chạy chính khối trên màn hình bằng Python, lấy
stdout THẬT làm expect_stdout (khối kết quả `output of:` trên màn hình được cổng so với stdout thật đó, nên không tự khẳng định).
      kind: output, of: "CS112 L00 scale 0 0" | "src:CS112:L00_lab";  kind: pseudo, reason: …
labs: [L00, …]  → nguồn `<Lxx>_lab` = lời giải lab chạy thật, expect_stdout = mong_doi.txt.
Đọc lại tệp sổ ngay trước khi ghi (tác tử khác sửa phần L15+ song song); mục cũ cùng khoá được thay."""
import re
import subprocess
import sys
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import screen_code as sc  # noqa: E402

LEDGER = ROOT / "audit" / "review" / "screen_code" / "CS112.yaml"
SPECS = ROOT / "audit" / "cs112" / "ledger_specs_a.yaml"
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
LABPY = str(ROOT / "labs" / ".venv-pyt" / "Scripts" / "python.exe")


def run_py(code, numpy=False):
    p = subprocess.run([LABPY if numpy else PY, "-B", "-c", code], capture_output=True, text=True, encoding="utf-8",
                       env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    if p.returncode != 0:
        raise SystemExit("khối lỗi khi chạy:\n" + code + "\n" + p.stderr)
    return p.stdout.replace("\r\n", "\n").rstrip("\n")


def dump(key, entry):
    body = yaml.safe_dump({key: entry}, allow_unicode=True, sort_keys=False, width=100000, default_flow_style=False)
    return "\n".join("  " + l if l else l for l in body.rstrip("\n").split("\n")) + "\n"


def drop_entry(text, key):
    """Bỏ mục `  "<key>":` (và các dòng thụt sâu hơn đi kèm) khỏi văn bản sổ."""
    lines = text.split("\n")
    out, skip = [], False
    for l in lines:
        if re.match(r'^  ("?)' + re.escape(key) + r'\1:\s*$', l):
            skip = True
            continue
        if skip and (l.startswith("    ") or not l.strip()):
            continue
        skip = False
        out.append(l)
    return "\n".join(out)


def main():
    specs = yaml.safe_load(SPECS.read_text(encoding="utf-8"))
    blocks = sc.all_blocks("CS112")
    new_blocks, new_sources = {}, {}
    for lab in specs.get("labs") or []:
        d = ROOT / "labs" / "CS112" / lab
        sol = next(iter(sorted(d.glob("loi_giai.*"))))
        e = {"lang": "python", "expect_stdout": (d / "mong_doi.txt").read_text(encoding="utf-8").strip("\n"),
             "code": sol.read_text(encoding="utf-8").strip("\n"),
             "reason": f"lời giải lab {lab} chạy thật (như labs/cham.sh) và cho đúng mong_doi.txt"}
        if sol.suffix == ".py" and re.search(r"^\s*(import|from)\s+numpy", e["code"], re.M):
            e["python"] = "venv"
        new_sources[f"{lab}_lab"] = e
    for short, spec in (specs.get("blocks") or {}).items():
        key = "CS112 " + short
        if key not in blocks:
            raise SystemExit(f"không có khối {key} trên màn hình (kiểm bài đã vá chưa?)")
        t = blocks[key]
        e = {"sha": sc.digest(t)}
        spec = dict(spec)
        auto = spec.pop("auto", False)
        e.update(spec)
        e["prelude_keys"] = ["CS112 " + k for k in e["prelude_keys"]] if "prelude_keys" in e else None
        if e["prelude_keys"] is None: e.pop("prelude_keys")
        if auto:
            pre = "".join(blocks["CS112 " + k] + chr(10) for k in spec.get("prelude_keys") or [])
            e["expect_stdout"] = run_py(pre + t, numpy=spec.get("python") == "venv")
        new_blocks[key] = e
    # khối mới trên màn hình chưa có spec → báo (chỉ phần L00–L14)
    have = set((yaml.safe_load(LEDGER.read_text(encoding="utf-8")).get("blocks") or {}).keys()) | set(new_blocks)
    miss = [k for k in blocks if re.match(r"CS112 L(0\d|1[0-4]) ", k) and k not in have]
    text = LEDGER.read_text(encoding="utf-8")
    for k in list(new_blocks) + [f"{k}" for k in new_sources]:
        text = drop_entry(text, k)
    add_b = "".join(dump(k, v) for k, v in new_blocks.items())
    add_s = "".join(dump(k, v) for k, v in new_sources.items())
    if "\nsources:\n" not in text:
        raise SystemExit("sổ không có mục sources:")
    text = text.replace("\nsources:\n", "\n" + add_b + "sources:\n", 1)
    text = text.rstrip("\n") + "\n" + add_s
    LEDGER.write_text(text, encoding="utf-8", newline="\n")
    print(f"ghi {len(new_blocks)} khối, {len(new_sources)} nguồn; khối L00–L14 trên màn hình chưa có mục: {miss}")


if __name__ == "__main__":
    main()
