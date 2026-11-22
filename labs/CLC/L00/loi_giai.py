layers = ['Hardware', 'OS', 'Runtime', 'App', 'Data']
cust = {
    'IaaS': {'OS', 'Runtime', 'App', 'Data'},
    'PaaS': {'App', 'Data'},
    'FaaS': {'App', 'Data'},
    'SaaS': {'Data'},
}
n = {m: sum(1 for x in layers if x in cust[m]) for m in cust}
print(f"iaas_layers={n['IaaS']}")
print(f"paas_faas_saas={n['PaaS']},{n['FaaS']},{n['SaaS']}")
print(f"iaas_minus_saas={n['IaaS'] - n['SaaS']}")
