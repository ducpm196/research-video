bank = {'t1', 't2', 't3', 't4'}
napas = {'t1', 't2', 't3', 't5'}
partner = {'t1', 't2', 't3'}
uni = bank | napas | partner
matched = bank & napas & partner
diff = sorted(uni - matched)
q = []
for tx in diff:
    if tx in bank and tx not in partner:
        q.append(f'{tx}:miss_partner')
    elif tx in napas and tx not in bank:
        q.append(f'{tx}:extra_napas')
    else:
        q.append(f'{tx}:other')
print(f'matched={len(matched)} match_pct={100*len(matched)/len(uni):.1f}%')
print(f'discrepancies={len(diff)}')
print('queue=' + ','.join(q))
