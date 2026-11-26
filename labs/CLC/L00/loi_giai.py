import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
layers = set(kv['layers'].split(','))
cnt = lambda k: sum(1 for x in kv[k].split(',') if x in layers)
i, p, f, s = cnt('iaas'), cnt('paas'), cnt('faas'), cnt('saas')
print(f'iaas_layers={i}\npaas_faas_saas={p},{f},{s}\niaas_minus_saas={i - s}')
