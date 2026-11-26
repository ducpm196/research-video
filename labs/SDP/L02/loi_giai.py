import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
class Account:
    def __init__(self, b):
        if b < 0: raise ValueError('bad')
        self._b = b
    @property
    def balance(self): return self._b
    def withdraw(self, a):
        if a <= 0 or a > self._b:
            raise ValueError('bad')
        self._b -= a
acc = Account(kv['init']); blk = 0
try:
    acc.withdraw(kv['over'])
except ValueError:
    blk = 1
b1 = acc.balance
acc.withdraw(kv['ok_draw'])
print(f'overdraw_blocked={blk}')
print(f'balance_after_reject={b1}')
print(f'balance_after_valid_40={acc.balance}')
