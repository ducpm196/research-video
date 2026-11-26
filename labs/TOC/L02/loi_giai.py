import sys
from functools import reduce
s = sys.stdin.read().strip() or "10|110 101"
suf, ws = s.split("|")
w1, w2 = ws.split()
nfa = {("A", "0"): {"A"}, ("A", "1"): {"A"}}
nfa[("A", suf[0])].add("B")
nfa[("B", suf[1])] = {"C"}
st = frozenset({"A"}); q, seen, d = [st], {st}, {}
while q:
    S = q.pop(0)
    for b in "01":
        nx = frozenset().union(*(nfa.get((u, b), set()) for u in S))
        d[(S, b)] = nx
        if nx not in seen: seen.add(nx); q.append(nx)
run = lambda w: "C" in reduce(lambda u, c: d[(u, c)], w, st)
print(f"dfa_states={len(seen)} acc_110={int(run(w1))} acc_101={int(run(w2))}")
