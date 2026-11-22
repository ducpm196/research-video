def reconcile(des, cur):
    miss = [p for p in des if p not in cur]
    return sorted(cur + miss), miss
des, cur = ['p1', 'p2', 'p3', 'p4'], ['p1', 'p3']
after, created = reconcile(des, cur)
print(f'created={created}')
print(f'converged={int(after == sorted(des))}')
