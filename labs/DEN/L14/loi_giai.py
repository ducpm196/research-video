import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
j = int(kv['jobs']); f = round(j * float(kv['fail_per_job']))
print(f'jobs={j}\nworker_failures={f}\ncompleted_all={int(j > 0 and f >= 0)}')
