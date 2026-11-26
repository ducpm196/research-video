import sys


def main() -> None:
    kv = {}
    for line in sys.stdin.read().splitlines():
        for tok in line.strip().split():
            if "=" in tok and (line.startswith("allow=") or line.startswith("required_slots=") or line.startswith("turns=")):
                if tok.startswith(("allow=", "max_steps=", "calls=", "required_slots=", "turns=")):
                    k, v = tok.split("=", 1)
                    kv[k] = v

    cur_intent = "NONE"
    slots: dict[str, str] = {}
    for t in kv["turns"].split(";"):
        if ":" not in t:
            continue
        it, rest = t.split(":", 1)
        if it != "KEEP" and it != cur_intent:
            cur_intent = it
            slots = {}
        for pair in rest.split(","):
            if "=" in pair:
                sk, sv = pair.split("=", 1)
                slots[sk] = sv

    req = {x for x in kv["required_slots"].split(",") if x}
    ready = int(req <= set(slots))

    allow = {x for x in kv["allow"].split(",") if x}
    max_s = int(kv["max_steps"])
    exec_cnt = blk_cnt = 0
    for c in kv["calls"].split(","):
        if ":" not in c:
            continue
        tool, arg_s = c.split(":", 1)
        try:
            arg_ok = int(arg_s) > 0
        except ValueError:
            arg_ok = False
        if exec_cnt < max_s and tool in allow and arg_ok:
            exec_cnt += 1
        else:
            blk_cnt += 1

    print(f"final_intent={cur_intent} slots_ready={ready}")
    print(f"executed_tools={exec_cnt}")
    print(f"blocked_tools={blk_cnt}")


if __name__ == "__main__":
    main()
