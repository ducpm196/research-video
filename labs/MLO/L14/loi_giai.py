import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
sp = float(kv['p_old']) / float(kv['p_new'])
cfg = math.prod(int(x) for x in kv['dims'].split(','))
sh = int(kv['ml_lines']) / int(kv['total_lines']) * 100
print(f'p999_speedup={sp:.0f}x configs={cfg} ml_code={sh:.1f}%')
