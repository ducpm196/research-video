import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
ls = [set(kv[k].split(',')) for k in ('l1', 'l2', 'l3')]
sec = kv['secret']
print(f'in_final_view={int(sec in ls[-1])}\nleaked_in_layers={int(any(sec in l for l in ls))}')
