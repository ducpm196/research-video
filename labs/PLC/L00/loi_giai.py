import sys
s = sys.stdin.read().strip() or "x:1|y|(,1,+,2"
es, q, ts = s.split("|")
env = {k: int(v) for k, v in (p.split(":") for p in es.split(",") if p)}
tokens = ts.split(",")
def check_syntax(tks):
    depth = 0
    for tk in tks:
        if tk == "(": depth += 1
        elif tk == ")": depth -= 1
        if depth < 0: return False
    return depth == 0
syn_err = int(not check_syntax(tokens))
sem_err = int(q not in env)
print(f"syn_err={syn_err} sem_err={sem_err}")
