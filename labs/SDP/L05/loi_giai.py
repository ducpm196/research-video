def calc(x, rules):
    for r in rules: x = r(x)
    return round(x)
sig0 = calc.__code__.co_code
tax10 = lambda p: p * 1.10; disc5 = lambda p: p * 0.95
print(f'with_tax_only={calc(200000, [tax10])}')
print(f'with_tax_and_discount={calc(200000, [tax10, disc5])}')
print(f'core_modified={int(calc.__code__.co_code != sig0)}')
