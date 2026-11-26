import sys


def parse_schema(spec: str) -> dict[str, tuple[str, int]]:
    out = {}
    for item in spec.split(","):
        if item.count(":") == 2:
            tag, typ, req = item.split(":")
            out[tag] = (typ, int(req))
    return out


def main() -> None:
    kv = dict(line.strip().split("=", 1) for line in sys.stdin.read().splitlines() if "=" in line)
    v1 = parse_schema(kv["v1"])
    v2 = parse_schema(kv["v2"])

    same_shared = all(v2[t][0] == v1[t][0] for t in v1 if t in v2)
    no_new_req = all((t in v1) or (v2[t][1] == 0) for t in v2)
    no_drop_old_req = all((t in v2) or (v1[t][1] == 0) for t in v1)

    b_ok = int(same_shared and no_new_req and no_drop_old_req)
    # Specifically distinguish pure backward vs forward rules:
    # Backward (new v2 reads old v1): shared tags same type, new tags in v2 must be optional (req=0). Removing required old tags in v2 still fails forward, while adding required tag fails backward.
    # Let's adhere precisely to spec defined in prompt:
    b_ok = int(same_shared and no_new_req)
    f_ok = int(same_shared and no_drop_old_req)
    if b_ok and f_ok:
        st = "FULL"
    elif b_ok:
        st = "BACKWARD_ONLY"
    elif f_ok:
        st = "FORWARD_ONLY"
    else:
        st = "BREAKING"
    print(f"backward_ok={b_ok}")
    print(f"forward_ok={f_ok}")
    print(f"compat_status={st}")


if __name__ == "__main__":
    main()
