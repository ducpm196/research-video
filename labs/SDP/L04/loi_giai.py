B, M = 3, 4
class Drink:
    def __init__(self, cost, addons=()): self.cost, self.addons = cost, addons
    def total(self): return self.cost + sum(self.addons)
d = Drink(30, (5, 2))
print(f'inherit_classes={B * (2 ** M)}')
print(f'compose_classes={B + M}')
print(f'espresso_milk_sugar={d.total()}')
