import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
errs = {p.split(':')[0]: int(p.split(':')[1]) for p in kv['errs'].split(',')}
tot = sum(errs.values()); print(f'top_cause_pct={errs[kv["top"]] / tot * 100:.1f}% total={tot}')
