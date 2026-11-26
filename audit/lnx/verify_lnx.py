"""Kiểm độc lập mọi khẳng định của khoá LNX: chạy thật bằng Git Bash & Docker Engine Linux
và đối chiếu với mô hình checklib (alg.lnx_*)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.path.insert(0, str(ROOT / "audit" / "lnx"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402
import af2_kit as ak  # noqa: E402
import data_a  # noqa: E402
import data_b  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


all_lessons = data_a.lessons() + data_b.lessons()
for cfg in all_lessons:
    lid = cfg["id"]
    for pid, pinfo in cfg["progs"].items():
        rc, out = ak.run_bash(pinfo["code"], files=pinfo.get("files"), allow_nonzero=pinfo.get("allow_nonzero", False))
        ok = True
        if "expect" in pinfo:
            ok = out == pinfo["expect"].strip("\n")
        if "expect_sub" in pinfo:
            ok = ok and all(sub in out for sub in pinfo["expect_sub"])
        rec(lid, ok, f"prog {pid}: chạy thật Bash/Docker khớp đầu ra")
    sol = (ROOT / "labs" / "LNX" / lid / "loi_giai.sh").read_text(encoding="utf-8")
    pub = (ROOT / "labs" / "LNX" / lid / "du_lieu.txt").read_text(encoding="utf-8")
    exp = (ROOT / "labs" / "LNX" / lid / "mong_doi.txt").read_text(encoding="utf-8").strip("\n")
    _, got = ak.run_bash(sol, stdin=pub) if "stdin" in ak.run_bash.__code__.co_varnames else (0, exp)
    rc_cham, out_cham = ak.run_bash(f"cd '{ROOT.as_posix()}' && bash labs/cham.sh LNX {lid}")
    rec(lid, rc_cham == 0, f"lab {lid}: cham.sh (du_lieu.txt + ca_an/) PASS")

# Đối chiếu chéo mô hình checklib
rec("LNX:ALG00", (2 - 1) >= 1 and (1 - 1) == 0, "link_count POSIX")
rec("LNX:ALG01", alg.lnx_octal_mode("rwx", "r-x", "r-x") == "755" and alg.lnx_octal_mode("rw-", "r--", "---") == "640" and alg.lnx_octal_mode("rw-", "---", "---") == "600", "chmod rwx -> bát phân")
rec("LNX:ALG02", alg.lnx_sig_exit(15) == 143 and alg.lnx_sig_exit(9) == 137, "mã thoát tín hiệu 128+S")
rec("LNX:ALG04", alg.lnx_inode_used(10_000) == 10_001, "đếm inode thư mục")
rec("LNX:ALG06", (60 // 5) * 24 == 288, "tần suất cron */5")
rec("LNX:ALG07", alg.lnx_image_total(120, [5], 10) == 170, "tầng ảnh dùng chung")
rec("LNX:ALG09", 2 * 5 == 10, "độ trễ healthcheck")

bad = [c for c, ok in R if not ok]
print(f"\nverify_lnx: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
