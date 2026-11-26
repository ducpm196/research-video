import math
import sys


def main() -> None:
    kv = {}
    for line in sys.stdin.read().splitlines():
        for tok in line.strip().split():
            if "=" in tok:
                k, v = tok.split("=", 1)
                kv[k] = v

    p_raw = [float(x) for x in kv["base"].split(",") if x]
    q_raw = [float(x) for x in kv["prod"].split(",") if x]
    sp, sq = sum(p_raw), sum(q_raw)
    eps = 1e-6
    ps = [max(x / sp, eps) for x in p_raw]
    qs = [max(x / sq, eps) for x in q_raw]
    psi = sum((q - p) * math.log(q / p) for p, q in zip(ps, qs))

    if psi >= 0.20:
        lvl = "SEVERE"
        old_f1, new_f1, margin = float(kv["old_f1"]), float(kv["new_f1"]), float(kv["margin"])
        dec = "PROMOTE_NEW" if new_f1 >= old_f1 + margin else "KEEP_OLD_ALERT"
    elif psi >= 0.10:
        lvl = "WARN"
        dec = "NO_RETRAIN"
    else:
        lvl = "STABLE"
        dec = "NO_RETRAIN"

    print(f"psi={psi:.4f}")
    print(f"drift_level={lvl}")
    print(f"retrain_decision={dec}")


if __name__ == "__main__":
    main()
