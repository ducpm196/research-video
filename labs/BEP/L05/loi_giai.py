import sys


def main() -> None:
    kv = {}
    for line in sys.stdin.read().splitlines():
        for tok in line.strip().split():
            if "=" in tok:
                k, v = tok.split("=", 1)
                kv[k] = v
    done = []
    failed = False
    for part in kv["steps"].split(","):
        if ":" in part:
            name, st = part.split(":", 1)
            if st == "FAIL":
                failed = True
                break
            done.append(name)
    base_ms = int(kv["base_ms"])
    cap_ms = int(kv["cap_ms"])
    max_ret = int(kv["max_retries"])
    total_wait = sum(min(cap_ms, base_ms * (2 ** k)) for k in range(max_ret)) if failed else 0
    comps = ",".join(f"undo_{x}" for x in reversed(done)) if (failed and done) else "NONE"
    print(f"compensations={comps}")
    print(f"backoff_total_ms={total_wait}")
    print(f"routed_dlq={int(failed)}")


if __name__ == "__main__":
    main()
