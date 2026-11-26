import math, sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
b1 = kv['c_len'] * math.log2(kv['c_alpha'])
b2 = kv['w_len'] * math.log2(kv['w_dict'])
print(f'bits_8_lower={b1:.1f}')
print(f'bits_4_words={b2:.1f}')
print(f'words_stronger={int(b2 > b1)}')
