import sys


def dfa(s: str) -> int:
    st = 0
    for ch in s:
        if ch not in ("a", "b"):
            return 0
        st = 1 if ch == "a" else (2 if st == 1 else 0)
    return int(st == 2)


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
    s1 = kv["s1"]
    s2 = kv["s2"]
    p = float(kv["p"])
    cores = int(kv["cores"])
    s_n = 1.0 / ((1.0 - p) + p / cores)
    s_inf = 1.0 / (1.0 - p) if p < 1.0 else float("inf")
    print(f"dfa_aaab={dfa(s1)} dfa_aba={dfa(s2)}")
    print(f"amdahl_8cores={s_n:.2f}")
    print(f"amdahl_inf={s_inf:.2f}")


if __name__ == "__main__":
    main()
