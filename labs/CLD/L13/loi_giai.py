layers = [
    {'app.py', 'key.env'},
    {'app.py', 'key.env', 'cfg.yml'},
    {'app.py', 'cfg.yml'},
]
in_final = int('key.env' in layers[-1])
leaked = int(any('key.env' in l for l in layers))
print(f'in_final_view={in_final}')
print(f'leaked_in_layers={leaked}')
