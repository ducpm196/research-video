import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
pol = {p.split(':')[0]: p.split(':')[1] for p in kv['policy'].split(',')}
acts = kv['actions'].split(',')
auto = [a for a in acts if pol.get(a) == 'allow']
print(f'auto_executed={auto} blocked={pol.get(kv["check"], "deny")}')
