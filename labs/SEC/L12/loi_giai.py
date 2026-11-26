import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
RULES = [(kv['allow_src'], kv['allow_dst'], kv['allow_port'], 'ALLOW'), ('*', '*', '*', 'DENY')]
def decide(q):
    s, d, p = q.split(',')
    for rs, rd, rp, act in RULES:
        if rs in ('*', s) and rd in ('*', d) and rp in ('*', p):
            return act
print(f'app_db_5432={decide(kv["q1"])}')
print(f'web_db_5432={decide(kv["q2"])}')
print(f'app_db_22={decide(kv["q3"])}')
