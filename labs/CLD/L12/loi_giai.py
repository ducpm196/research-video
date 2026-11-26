import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
mins = int(kv['days']) * 24 * 60
print(f'budget_9995_min={mins * (1.0 - float(kv["slo1"])):.2f}')
print(f'budget_9999_min={mins * (1.0 - float(kv["slo2"])):.2f}')
