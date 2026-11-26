"""Kiểm độc lập mọi khẳng định của khoá CPR: biên dịch & chạy thật mọi bài bằng GCC 16.2.0
và đối chiếu với mô hình checklib (alg.cpr_*)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.path.insert(0, str(ROOT / "audit" / "cpr"))
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
        out = ak.run_c(pinfo["code"], args=pinfo.get("args", ""), stdin=pinfo.get("stdin"))
        rec(lid, out == pinfo["expect"].strip("\n"), f"prog {pid}: chạy thật GCC khớp đầu ra")
    # Kiểm chạy trực tiếp lời giải lab (đọc du_lieu.txt) + chấm qua cham.sh (kèm ca_an/)
    sol = (ROOT / "labs" / "CPR" / lid / "loi_giai.c").read_text(encoding="utf-8")
    pub = (ROOT / "labs" / "CPR" / lid / "du_lieu.txt").read_text(encoding="utf-8")
    exp = (ROOT / "labs" / "CPR" / lid / "mong_doi.txt").read_text(encoding="utf-8").strip("\n")
    got = ak.run_c(sol, stdin=pub)
    rec(lid, got == exp, f"lab {lid}: chạy thật GCC với du_lieu.txt khớp mong_doi.txt")
    rc_cham, _ = ak.run_bash(f"cd '{ROOT.as_posix()}' && bash labs/cham.sh CPR {lid}")
    rec(lid, rc_cham == 0, f"lab {lid}: cham.sh (du_lieu.txt + ca_an/) PASS")

# Đối chiếu chéo mô hình toán với checklib
rec("CPR:ALG00", alg.cpr_sizeof_64() == {"char": 1, "short": 2, "int": 4, "long_long": 8, "ptr": 8}, "sizeof 64-bit khớp")
rec("CPR:ALG01", alg.cpr_u8_wrap(250, 10) == 4, "uint8_t quay vòng")
rec("CPR:ALG02", alg.cpr_stack_bytes([32, 48, 64]) == 144, "cộng khung ngăn xếp")
rec("CPR:ALG03", alg.cpr_str_bytes(31) == 32, "chuỗi + byte '\\0'")
rec("CPR:ALG05", alg.cpr_ptr_offset(3, 4) == 12 and alg.cpr_ptr_offset(3, 8) == 24, "bước nhảy con trỏ")
rec("CPR:ALG06", alg.cpr_heap_leak(5, 5) == 0, "cân bằng heap")
rec("CPR:ALG07", alg.cpr_struct_size([(1, 1), (4, 4), (1, 1)]) == (12, 6) and alg.cpr_struct_size([(4, 4), (1, 1), (1, 1)]) == (8, 2), "padding struct")
rec("CPR:ALG08", alg.cpr_pack_rec_bytes() == 16, "bản ghi nhị phân 16 byte")

bad = [c for c, ok in R if not ok]
print(f"\nverify_cpr: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
