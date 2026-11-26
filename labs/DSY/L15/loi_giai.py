import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
fan = (kv['meta_mib'] * 1024) // kv['entry_kb']
tot = fan * fan
print(f'entries_per_table={fan}')
print(f'max_tablets_pow2={tot.bit_length() - 1}')
print(f'entries_sq_exact={tot}')
