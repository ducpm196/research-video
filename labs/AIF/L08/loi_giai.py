import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
rc = int(kv['req_c']); idx = 0 if kv['check_var'] == 'A' else 1
models = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1) if ((not a or b) and (b or c) and (c == rc))]
ent = all(m[idx] == 1 for m in models)
print(f'kb_models={len(models)} entails_B={int(ent)}')
