import sys


def main() -> None:
    kv = dict(line.strip().split("=", 1) for line in sys.stdin.read().splitlines() if "=" in line)
    flags = [x for x in kv["flags"].split(",") if x]
    actions = [x for x in kv["actions"].split(",") if x]
    dod_miss = int(kv["dod_missing"])

    defects = sum(1 for f in flags if f != "CLEAN")
    auto_cnt = sum(1 for a in actions if a.startswith("AUTO:"))
    ok = (defects == 0 and dod_miss == 0 and auto_cnt >= 1)
    print(f"security_defects={defects}")
    print(f"auto_fix_count={auto_cnt}")
    print(f"release_decision={'APPROVED' if ok else 'CHANGES_REQUESTED'}")


if __name__ == "__main__":
    main()
