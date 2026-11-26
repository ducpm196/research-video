import sys
raw = sys.stdin.read().strip().split('=', 1)[1]
cv, cc = 0, ''
for item in raw.split(','):
    vs, ct = item.split(':'); v = int(vs)
    if v > cv: cv, cc = v, ct
print(f'final_ver={cv}\nfinal_city={cc}')
