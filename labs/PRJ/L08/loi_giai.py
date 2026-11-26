import sys


def parse_kv(text: str) -> dict[str, str]:
    kv: dict[str, str] = {}
    for line in text.splitlines():
        for tok in line.strip().split():
            if "=" in tok:
                k, v = tok.split("=", 1)
                kv[k] = v
    return kv


def main() -> None:
    kv = parse_kv(sys.stdin.read())
    tp = int(kv["tp"])
    fp = int(kv["fp"])
    fn = int(kv["fn"])
    bins = []
    for part in kv["bins"].split(";"):
        n_s, a_s, c_s = part.split(",")
        bins.append((int(n_s), float(a_s), float(c_s)))

    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    tot = sum(n for n, _, _ in bins)
    ece = sum((n / tot) * abs(acc - conf) for n, acc, conf in bins) if tot else 0.0

    print(f"precision={p:.2f} recall={r:.2f}")
    print(f"f1={f1:.2f}")
    print(f"ece={ece:.2f}")


if __name__ == "__main__":
    main()
