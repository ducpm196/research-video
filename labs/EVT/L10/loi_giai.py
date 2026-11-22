a, b, c, d = 15, 30, 70, 25
seq = a + b + c + d
crit = a + max(b, c) + d
print(f'seq_ms={seq}')
print(f'critical_ms={crit}')
