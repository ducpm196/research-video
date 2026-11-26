"""Kiểm thử thật 5 nhánh lab Oracle tuỳ chọn (WP-3C) chạy trực tiếp trên container bnx-ora."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.stdout.reconfigure(encoding="utf-8")
import dbrun  # noqa: E402

PIN_DIGEST = "gvenzl/oracle-free@sha256:6d61d267a3b978c24c5ac1790e62e927416a0aec446bd86e4b3a1527562757bd"
R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


dig = subprocess.check_output(
    ["docker", "image", "inspect", "gvenzl/oracle-free:23-slim", "--format", "{{index .RepoDigests 0}}"],
    text=True,
    encoding="utf-8",
).strip()
rec("ORA:DIGEST", dig == PIN_DIGEST, f"pin ảnh Oracle: {dig}")

ok_o, _ = dbrun.ready()
rec("ORA:READY", ok_o, "bnx-ora sẵn sàng")

checks = [
    ("BNK:L05", ROOT / "labs" / "BNK" / "L05" / "oracle" / "thu.sql", ["4->9: khoa 4 roi 9", "9->4: khoa 4 roi 9", "tong_tien=3000"]),
    ("BNX:L06", ROOT / "labs" / "BNX" / "L06" / "oracle" / "thu.sql", ["chuyen 1->2 200000: OK", "chuyen 2->3 900000: loi so du khong du", "tong_tien=1300000"]),
    ("BNX:L07", ROOT / "labs" / "BNX" / "L07" / "oracle" / "thu.sql", ["tong_dong=3", "thang3_tien=250000", "PARTITION RANGE SINGLE"]),
    ("BNX:L37", ROOT / "labs" / "BNX" / "L37" / "oracle" / "thu.sql", ["chuoi 1: ghep 1 dong, bind 1 dong", "chuoi 2: ghep 4 dong, bind 0 dong"]),
    ("BNX:L38", ROOT / "labs" / "BNX" / "L38" / "oracle" / "thu.sql", ["sau_gui=2", "nhan=201 750000", "con_lai=1"]),
]

for code, sql_p, expects in checks:
    sql = sql_p.read_text(encoding="utf-8")
    out = dbrun.ora(sql, header=False)
    for exp in expects:
        rec(code, exp in out, f"Oracle trả về {exp!r}")

bad = [c for c, ok in R if not ok]
print(f"\nverify_oracle_labs: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
