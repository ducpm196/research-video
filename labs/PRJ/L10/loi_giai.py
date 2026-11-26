import hashlib
import sys


def h(b: str) -> str:
    return hashlib.sha256(b.encode("utf-8")).hexdigest()


def merkle(xs: list[str]) -> str:
    hs = [h(x) for x in xs]
    return h(h(hs[0] + hs[1]) + h(hs[2] + hs[3]))


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
    pairs = []
    for item in kv["tasks"].split(";"):
        c_s, t_s = item.split(",")
        pairs.append((float(c_s), float(t_s)))
    kp = float(kv["kp"])
    target = float(kv["target"])
    steps = int(kv["steps"])
    leaves = kv["leaves"].split(",")
    tidx = int(kv["tamper_idx"])

    u = sum(c / t for c, t in pairs)
    n = len(pairs)
    bound = n * (2 ** (1.0 / n) - 1.0)

    x = 0.0
    for _ in range(steps):
        x += kp * (target - x)

    tampered = list(leaves)
    tampered[tidx] = tampered[tidx] + "*"
    r1 = merkle(leaves)
    r2 = merkle(tampered)

    print(f"rms_u={u:.2f} schedulable={int(u <= bound)}")
    print(f"pid_step5={x:.3f}")
    print(f"merkle_tamper_detected={int(r1 != r2)}")


if __name__ == "__main__":
    main()
