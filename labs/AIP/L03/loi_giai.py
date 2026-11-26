import math
import sys


def main() -> None:
    kv = {}
    for line in sys.stdin.read().splitlines():
        for tok in line.strip().split():
            if "=" in tok:
                k, v = tok.split("=", 1)
                kv[k] = v

    n_reqs = int(kv["n_reqs"])
    max_b = int(kv["max_batch"])
    fixed = float(kv["fixed_ms"])
    per_it = float(kv["per_item_ms"])
    wait = float(kv["wait_ms"])

    n_batches = math.ceil(n_reqs / max_b)
    total_ms = n_batches * fixed + n_reqs * per_it
    qps = n_reqs * 1000.0 / total_ms
    worst = wait + fixed + max_b * per_it

    params_m = float(kv["params_millions"])
    bits = int(kv["bits"])
    limit_mb = float(kv["edge_ram_mb"])
    model_mb = params_m * (bits / 8.0)
    fits = int(model_mb <= limit_mb)

    print(f"batches={n_batches} qps={qps:.1f}")
    print(f"worst_case_ms={worst:.1f}")
    print(f"model_mb={model_mb:.1f} fits_edge={fits}")


if __name__ == "__main__":
    main()
