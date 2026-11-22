cap, req = 6.0, 2.2
fit = int(cap // req)
wasted = (cap - fit * req) / cap * 100
print(f'pods_per_node={fit}')
print(f'stranded_pct={wasted:.1f}%')
