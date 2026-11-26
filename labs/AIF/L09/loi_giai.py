import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
facts = set(kv['facts'].split(',')); order = []
rules = [(set(r.split('>')[0].split('+')), r.split('>')[1]) for r in kv['rules'].split(',')]
while True:
    added = [c for pre, c in rules if pre <= facts and c not in facts]
    if not added: break
    facts.add(added[0]); order.append(added[0])
print('derived=' + ','.join(order))
