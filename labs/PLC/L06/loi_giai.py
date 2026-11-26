import sys
s = sys.stdin.read().strip() or "ret:t_x,t_x:t_y,t_y:int"
constraints = [tuple(x.split(":")) for x in s.split(",")]
known = {}
for _ in range(len(constraints)):
    for lhs, rhs in constraints:
        if rhs in known: known[lhs] = known[rhs]
        elif rhs in ("int", "bool", "str"): known[lhs] = rhs
print(f"inferred_tx={known['t_x']} ret={known['ret']}")
