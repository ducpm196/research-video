import math
k = math.sqrt(2 * (2 ** 64) * math.log(2))
bits_sec = 64 // 2
print(f'birthday_50pct_billions={k / 1e9:.2f}')
print(f'bit_security_collision={bits_sec}')
print(f'ratio_vs_32bit_hash={round(k / (2 ** bits_sec))}')
