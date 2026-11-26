import sys
from collections import defaultdict


def main() -> None:
    kv = dict(line.strip().split("=", 1) for line in sys.stdin.read().splitlines() if "=" in line)
    tol = float(kv["parity_tol"])
    fmap: dict[str, list[tuple[int, float]]] = defaultdict(list)
    for part in kv["features"].split(","):
        if part.count(":") == 2:
            eid, ts_s, val_s = part.split(":")
            fmap[eid].append((int(ts_s), float(val_s)))

    joined = missing = 0
    skews = []
    for part in kv["events"].split(","):
        if part.count(":") == 2:
            eid, ts_s, on_s = part.split(":")
            ev_ts, on_v = int(ts_s), float(on_s)
            cands = [(fts, fv) for fts, fv in fmap.get(eid, []) if fts <= ev_ts]
            if not cands:
                missing += 1
            else:
                _, off_v = max(cands, key=lambda x: x[0])
                joined += 1
                skews.append(abs(off_v - on_v))

    ms = max(skews) if skews else 0.0
    ok = int(missing == 0 and ms <= tol)
    print(f"joined_count={joined} missing_count={missing}")
    print(f"max_skew={ms:.6f}")
    print(f"parity_ok={ok}")


if __name__ == "__main__":
    main()
