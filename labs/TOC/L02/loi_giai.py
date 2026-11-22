from functools import reduce
nfa = {('A', '0'): {'A'}, ('A', '1'): {'A', 'B'}, ('B', '0'): {'C'}}
st = frozenset({'A'}); q, seen, d = [st], {st}, {}
while q:
    S = q.pop(0)
    for b in '01':
        nx = frozenset().union(*(nfa.get((u, b), set()) for u in S))
        d[(S, b)] = nx
        if nx not in seen: seen.add(nx); q.append(nx)
run = lambda s: 'C' in reduce(lambda u, c: d[(u, c)], s, st)
print(f"dfa_states={len(seen)} acc_110={int(run('110'))}",
      f"acc_101={int(run('101'))}")
