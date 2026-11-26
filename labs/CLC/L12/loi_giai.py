import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
tom = lambda s: int(s[:2]) * 60 + int(s[3:])
out = tom(kv['end']) - tom(kv['start']); bud = 525600 * 0.0001
gr = round(float(kv['obj_new_b']) / float(kv['obj_old_b']))
print(f'outage_min={out}\nratio_99_99={out / bud:.1f}x\ngrowth_2010_2021={gr}x')
