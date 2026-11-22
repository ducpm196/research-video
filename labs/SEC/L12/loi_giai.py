RULES = [('app','db',5432,'ALLOW'), ('*','*','*','DENY')]
def decide(s, d, p):
    for rs, rd, rp, act in RULES:
        if (rs in ('*', s)) and (rd in ('*', d)) and (rp in ('*', p)): return act
print(f'app_db_5432={decide("app","db",5432)}')
print(f'web_db_5432={decide("web","db",5432)}')
print(f'app_db_22={decide("app","db",22)}')
