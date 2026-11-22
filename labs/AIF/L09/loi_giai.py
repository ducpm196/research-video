facts, order = {'X', 'Y'}, []
rules = [
    ({'X', 'Y'}, 'Z'), ({'X', 'W'}, 'Z'),
    ({'Y', 'Z'}, 'U'), ({'Z', 'U'}, 'W'), ({'W'}, 'V'),
]
while True:
    added = [c for pre, c in rules if pre <= facts and c not in facts]
    if not added: break
    facts.add(added[0]); order.append(added[0])
print("derived=" + ",".join(order))
