import hashlib, sys
lines = [ln.strip() for ln in sys.stdin.read().splitlines() if ln.strip()]
kv = dict(ln.split('=', 1) for ln in lines)
h = lambda s: hashlib.sha256(s.replace('\\n', '\n').encode()).hexdigest()[:12]
h1, h2 = h(kv['v1']), h(kv['v2'])
print(f'h1={h1} h2={h2} changed={int(h1 != h2)}')
