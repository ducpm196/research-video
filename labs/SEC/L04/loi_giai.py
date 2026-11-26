import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
RBAC = {'accountant': {'read', 'create'}, 'auditor': {'read'}}
can = lambda pair: int(pair.split(':')[1] in RBAC.get(pair.split(':')[0], set()))
print(f'accountant_create={can(kv["r1"])}')
print(f'auditor_read={can(kv["r2"])}')
print(f'auditor_create_denied={1 - can(kv["deny_check"])}')
