import sys


def main() -> None:
    kv = {}
    for line in sys.stdin.read().splitlines():
        for tok in line.strip().split():
            if "=" in tok:
                k, v = tok.split("=", 1)
                kv[k] = v

    sla = float(kv["sla_pct"])
    down = float(kv["downtime_min"])
    budget = (1.0 - sla / 100.0) * 43200.0
    breached = int(down > budget)

    ola = int(kv["ola_l2_limit"])
    elap = int(kv["elapsed_min"])
    has_tr = int(kv["has_trace"])
    if elap > ola:
        action = "ESCALATE_L3" if has_tr else "NEED_TRACE"
    else:
        action = "KEEP_L2"

    vals = [float(x) for x in kv["edge_vals"].split(",") if x]
    guarded = sum(1 for x in vals if x <= 0)

    print(f"budget_min={budget:.2f} sla_breached={breached}")
    print(f"l3_action={action}")
    print(f"guarded_cases={guarded}")


if __name__ == "__main__":
    main()
