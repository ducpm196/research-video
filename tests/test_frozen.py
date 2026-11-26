"""Kiểm khoá generator (WP-0.10 / BN-04): mọi script sinh/nâng cấp phải từ chối chạy với mã lỗi != 0 khi không đặt AF5_ALLOW_GEN=1."""
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "audit/add_clear.py",
    "audit/group_bits.py",
    "audit/link_specs.py",
    "audit/review/af2_upgrader.py",
    "audit/s9_11/common.py",
    "audit/dms/af2/af2lib.py",
    "audit/bnk/fillout.py",
    "audit/bnx/addcur.py",
    "audit/cpr/cpr_builder.py",
    "audit/lnx/lnx_builder.py",
    "audit/prj/prj_builder.py",
    "audit/prj/gen_s6_11.py",
    "audit/mlp/gen_mlp.py",
    "audit/cs112/fill_tpl.py",
    "audit/cs112/gen_labs_b.py",
    "audit/cs112/regen_a.py",
    "audit/cs112/regen_b.py",
    "audit/pyt/autofill.py",
    "audit/pyt/make_fig_l11.py",
]
for pat in ("audit/*/af2/upgrade_*.py", "audit/*/fill_all.py", "audit/*/gen.py", "audit/*/gen_curriculum.py"):
    TARGETS += sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob(pat))
TARGETS = sorted(set(TARGETS))


def main() -> int:
    env = {k: v for k, v in os.environ.items() if k != "AF5_ALLOW_GEN"}
    bad = 0
    for rel in TARGETS:
        p = subprocess.run(
            [sys.executable, "-B", str(ROOT / rel)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            cwd=ROOT,
            timeout=15,
        )
        if p.returncode == 0 or "FROZEN" not in (p.stderr + p.stdout):
            print(f"FAIL {rel}: rc={p.returncode}, err={p.stderr[:120]!r}")
            bad += 1
    st = subprocess.run(
        ["git", "status", "--short", "lessons", "labs", "curriculum"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=ROOT,
    )
    print(f"test_frozen: {len(TARGETS) - bad}/{len(TARGETS)} FROZEN, {bad} FAIL")
    if bad:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
