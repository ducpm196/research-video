class Account:
    def __init__(self, b): self._b = b
    def withdraw(self, a):
        if a <= 0 or a > self._b: raise ValueError('bad')
        self._b -= a
acc = Account(100); blk = 0
try: acc.withdraw(150)
except ValueError: blk = 1
b1 = acc._b; acc.withdraw(40)
print(f'overdraw_blocked={blk}')
print(f'balance_after_reject={b1}')
print(f'balance_after_valid_40={acc._b}')
