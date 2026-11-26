"""Kiểm độc lập khoá AIP: chạy thật mọi khối example/check + toàn bộ lab (du_lieu.txt + ca_an/) qua cham.sh."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.stdout.reconfigure(encoding="utf-8")
import af2_kit as ak  # noqa: E402
import screen_code as sc_mod  # noqa: E402

R = []
for ypath in sorted((ROOT / "lessons" / "aip").glob("L*.yaml")):
    lid = ypath.name[:3]
    _, blks = sc_mod.blocks_of(ypath)
    pending_code = None
    for sid, ti, bi, txt in blks:
        if sid in ("example", "check") and ti == 0 and bi == 0:
            pending_code = txt
        elif sid in ("example", "check") and ti == 1 and bi == 0 and pending_code is not None:
            got = ak.run_py(pending_code)
            ok = (got == txt.strip("\n"))
            R.append((f"{lid}:{sid}", ok))
            print(("PASS" if ok else "FAIL"), f"{lid}:{sid}", "— chạy thật Python khớp đầu ra")
            pending_code = None
    p = subprocess.run([ak.BASH_EXE, str(ROOT / "labs" / "cham.sh"), "AIP", lid], cwd=ROOT, env=ak._tool_env(), capture_output=True, text=True, encoding="utf-8")
    ok_lab = (p.returncode == 0 and "PASS" in p.stdout)
    R.append((f"{lid}:lab", ok_lab))
    print(("PASS" if ok_lab else "FAIL"), f"{lid}:lab", "—", p.stdout.strip())

bad = [k for k, ok in R if not ok]
print(f"\nverify_aip: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
