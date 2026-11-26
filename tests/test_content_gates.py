"""Kiểm đơn vị cố định cho 11 cổng nội dung (WP-1) trên tests/fixtures/content_gates/."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures" / "content_gates"
sys.path.insert(0, str(ROOT / "audit" / "review"))
import content_gates as cg  # noqa: E402

EXPECTED = [
    ("G-PRACTICE", [("NET", "L03"), ("CPR", "L00"), ("LNX", "L00"), ("MLP", "L00"), ("PRJ", "L00")], [("BNX", "L26"), ("JVA", "L04"), ("ACB", "L03")]),
    ("G-LEAK-DE", [("LNX", "L06"), ("PRJ", "L04"), ("BNK", "L12")], [("BNX", "L26"), ("ACB", "L03")]),
    ("G-ANTI-PRINT", [("ZZ", "L00")], [("ZP", "L00")]),
    ("G-LABLANG", [("ZZ", "L00")], [("JVA", "L04"), ("PYT", "L04")]),
    ("G-COVERS", [("CSA", "L00"), ("MLP", "L04"), ("LNX", "L06")], [("BNX", "L26"), ("PYT", "L04")]),
    ("G-LEN", [("CPR", "L04"), ("LNX", "L05"), ("PRJ", "L04")], [("BNX", "L09"), ("JVA", "L04")]),
    ("G-PAD", [("AIF", "L10"), ("LLM", "L10"), ("PLC", "L03"), ("CS115", "L43")], [("BNX", "L26"), ("DMS", "L18")]),
    ("G-BOILER", [("MLP", "L08"), ("CLC", "L05")], [("DMS", "L18"), ("JVA", "L04")]),
    ("G-CHECKS", [("LNX", "L05"), ("MLP", "L12")], [("CS112", "L08"), ("DMS", "L18")]),
    ("G-SCORE", [("PRJ", "L04"), ("PRJ", "L07"), ("MLP", "L08")], [("BNX", "L09"), ("CS115", "L05")]),
    ("G-CODETABLE", [("CLC", "L05"), ("CLD", "L15"), ("LLM", "L10"), ("TOC", "L10")], [("JVA", "L04"), ("BNX", "L26")]),
]


def main() -> int:
    rows = cg.audit_root(FIX, set(), run_cham=True, ignore_duration=False)
    grid = {(c, l): res for c, l, res, _ in rows}
    bad = 0
    for gate, negs, poss in EXPECTED:
        for c, l in negs:
            errs = grid[(c, l)][gate]
            if not errs:
                print(f"FAIL NEG {gate} {c} {l}: expected FAIL, got PASS")
                bad += 1
        for c, l in poss:
            errs = grid[(c, l)][gate]
            if errs:
                print(f"FAIL POS {gate} {c} {l}: expected PASS, got {errs}")
                bad += 1
    print(f"test_content_gates: {len(EXPECTED)} cổng kiểm trên {len(grid)} bài mẫu, {bad} FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
