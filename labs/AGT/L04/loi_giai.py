import sys
lines = [ln.strip() for ln in sys.stdin.read().splitlines() if ln.strip()]
kv = dict(t.split('=') for t in lines[0].split())
for ln in lines[1:]: k, v = ln.split('=', 1); kv[k] = v
miss = (1.0 - float(kv['init_hit'])) * ((1.0 - float(kv['gain'])) ** int(kv['rounds']))
print(f'recall_after_3={(1.0 - miss)*100:.1f}% matched_quote={int(kv["quote"] in kv["src"])}')
