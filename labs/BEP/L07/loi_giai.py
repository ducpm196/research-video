import sys
from collections import defaultdict


def main() -> None:
    kv = {}
    for line in sys.stdin.read().splitlines():
        for tok in line.strip().split():
            if "=" in tok:
                k, v = tok.split("=", 1)
                kv[k] = v

    spans = []
    csum = defaultdict(int)
    for part in kv["spans"].split(","):
        if part.count(":") == 2:
            sid, pid, dur_s = part.split(":")
            dur = int(dur_s)
            spans.append((sid, pid, dur))
            if pid != "NONE":
                csum[pid] += dur
    best_sid, best_self = min(
        ((sid, dur - csum[sid]) for sid, _, dur in spans),
        key=lambda item: (-item[1], item[0]),
    )

    events = [x for x in kv["events"].split(",") if x]
    quota = int(kv["quota"])
    thresh = int(kv["cb_thresh"])
    fails = 0
    cb = "CLOSED"
    passed = 0
    for idx, ev in enumerate(events):
        if idx >= quota or cb == "OPEN":
            break
        if ev == "OK":
            fails = 0
            passed += 1
        else:
            fails += 1
            if fails >= thresh:
                cb = "OPEN"

    print(f"top_self_span={best_sid}")
    print(f"top_self_ms={best_self}")
    print(f"gw_passed={passed} cb_state={cb}")


if __name__ == "__main__":
    main()
