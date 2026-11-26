import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
B, M = int(kv['base_kinds']), int(kv['addons_count'])
cost = int(kv['drink_cost'])
addons = tuple(int(v) for v in kv['extra'].split(','))
class Drink:
    def __init__(self, c, ex=()): self.c, self.ex = c, ex
    def total(self): return self.c + sum(self.ex)
d = Drink(cost, addons)
print(f'inherit_classes={B * (2 ** M)}')
print(f'compose_classes={B + M}')
print(f'espresso_milk_sugar={d.total()}')
