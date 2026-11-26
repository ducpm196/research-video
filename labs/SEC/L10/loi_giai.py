import math, sys
bits = int(sys.stdin.read().split('=')[1])
k = math.sqrt(2 * (2 ** bits) * math.log(2))
sec = bits // 2
print(f'birthday_50pct_billions={k / 1e9:.2f}')
print(f'bit_security_collision={sec}')
print(f'ratio_vs_32bit_hash={round(k / (2 ** sec))}')
