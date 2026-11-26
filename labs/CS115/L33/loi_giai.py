import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
def pick(spec):
    n_s, kind = spec.split(',')
    if kind == 'viz': return 'PCA/t-SNE'
    return 'Linear/Ridge' if int(n_s) < 1000 else 'Tree/Boosting'
print("s1=", pick(kv['s1']))
print("s2=", pick(kv['s2']))
print("s3=", pick(kv['s3']))
