import sys

sources = {"BANK": {}, "NAPAS": {}, "PARTNER": {}}
for raw in sys.stdin.read().splitlines():
    ln = raw.strip()
    if not ln:
        continue
    src, tx_id, amt_s, status = ln.split()
    if src in sources:
        sources[src][tx_id] = (int(amt_s), status)

all_ids = sorted(set(sources["BANK"]) | set(sources["NAPAS"]) | set(sources["PARTNER"]))
matched = 0
state_mismatch = 0
one_side = 0
queue = []

for tx in all_ids:
    b = sources["BANK"].get(tx)
    n = sources["NAPAS"].get(tx)
    p = sources["PARTNER"].get(tx)
    if b is not None and n is not None and p is not None:
        if b == n == p and b[1] == "OK":
            matched += 1
        else:
            state_mismatch += 1
            queue.append(f"{tx}:mismatch_state")
    else:
        one_side += 1
        if b is not None and n is not None and p is None:
            queue.append(f"{tx}:miss_partner")
        elif n is not None and b is None and p is None:
            queue.append(f"{tx}:extra_napas")
        elif n is not None and p is not None and b is None:
            queue.append(f"{tx}:miss_bank")
        elif b is not None and p is not None and n is None:
            queue.append(f"{tx}:miss_napas")
        else:
            queue.append(f"{tx}:one_side")

tot = len(all_ids)
disc = state_mismatch + one_side
pct = (100.0 * matched / tot) if tot else 0.0

print(f"matched={matched} match_pct={pct:.1f}%")
print(f"discrepancies={disc} state_mismatch={state_mismatch} one_side={one_side}")
print("queue=" + (",".join(queue) if queue else "none"))
