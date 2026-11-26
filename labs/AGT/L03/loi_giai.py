import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
t = (kv['limit'] - kv['sys_tok']) // kv['turn_tok']; print(f'max_turns={t} full_after={kv["sys_tok"] + t * kv["turn_tok"]}')
