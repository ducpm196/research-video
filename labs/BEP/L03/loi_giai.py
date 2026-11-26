import sys


def main() -> None:
    kv = {}
    for line in sys.stdin.read().splitlines():
        for tok in line.strip().split():
            if "=" in tok:
                k, v = tok.split("=", 1)
                kv[k] = v
    avg_ms = int(kv["warm_ms"]) + float(kv["cold_rate"]) * int(kv["cold_penalty"])
    owners = dict(p.split(":", 1) for p in kv["owners"].split(",") if ":" in p)
    allowed = blocked = 0
    for r in kv["reqs"].split(","):
        if ":" in r:
            u, did = r.split(":", 1)
            if owners.get(did) == u:
                allowed += 1
            else:
                blocked += 1
    print(f"avg_latency_ms={avg_ms:.1f}")
    print(f"allowed={allowed}")
    print(f"bola_blocked={blocked}")


if __name__ == "__main__":
    main()
