import sys
n = int(sys.stdin.read().split('=')[1])
c2, c3 = 2 * n, 3 * (n // 2); hd = 100.0 * (c2 - n) / n
print(f'cap_2region={c2}\ncap_3region={c3}\nheadroom_2region={hd:.1f}%')
