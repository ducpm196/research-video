tr = [{'has_grass': True}] * 90 + [{'has_grass': False}] * 10
sn = [{'has_grass': False}] * 25
acc = lambda ds: sum(1 for x in ds if x['has_grass']) / len(ds) * 100
print(f"spur_train={acc(tr):.0f}% counterexample_snow={acc(sn):.0f}%")
