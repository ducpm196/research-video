cur_ver, cur_city = 0, ''
for ver, city in [(2, 'HN'), (5, 'DN'), (3, 'HCM')]:
    if ver > cur_ver:
        cur_ver, cur_city = ver, city
print(f'final_ver={cur_ver}')
print(f'final_city={cur_city}')
