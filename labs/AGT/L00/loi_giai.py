import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
s = int(kv['steps']); print(f'task15_at96={(float(kv["p1"])**s)*100:.1f}% task15_at99={(float(kv["p2"])**s)*100:.1f}%')
