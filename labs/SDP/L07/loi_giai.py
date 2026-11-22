def greet(clock): return 'Chuc mung nam moi' if clock() == (1, 1) else 'Ngay binh thuong'
r1, r2 = greet(lambda: (1, 1)), greet(lambda: (5, 10))
det = int(r1 == greet(lambda: (1, 1)) and r1 != r2)
print(f'jan1={r1}')
print(f'may10={r2}')
print(f'deterministic={det}')
