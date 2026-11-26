import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
def calc(x, rules):
    for r in rules: x = r(x)
    return round(x)
tax_fn = lambda p: p * (1.0 + kv['tax'])
disc_fn = lambda p: p * (1.0 - kv['disc'])
only_tax = calc(kv['base'], [tax_fn])
both_rules = calc(kv['base'], [tax_fn, disc_fn])
unchanged = int(calc(kv['base'], [tax_fn]) != only_tax)
print(f'with_tax_only={only_tax}')
print(f'with_tax_and_discount={both_rules}')
print(f'core_modified={unchanged}')
