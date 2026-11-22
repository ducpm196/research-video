RBAC = {'accountant': {'read', 'create'}, 'auditor': {'read'}}
can = lambda role, act: int(act in RBAC.get(role, set()))
print(f'accountant_create={can("accountant", "create")}')
print(f'auditor_read={can("auditor", "read")}')
print(f'auditor_create_denied={1 - can("auditor", "create")}')
