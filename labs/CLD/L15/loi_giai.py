import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
ex = round(int(kv['machines']) * float(kv['head_pct']))
pct = float(kv['down_min']) / float(kv['win_min']) * 100
print(f'extra_machines={ex}\ndowntime_pct={pct:.2f}%')
