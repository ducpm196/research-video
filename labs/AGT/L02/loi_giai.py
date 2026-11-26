import sys
dur = {p.split(':')[0]: int(p.split(':')[1]) for p in sys.stdin.read().strip().split('=', 1)[1].split(',')}
seq = sum(dur.values()); crit = dur['tim'] + max(dur['docA'], dur['docB']) + dur['tonghop'] + dur['kiemtra']
print(f'sequential={seq}s critical_path={crit}s saved={seq - crit}s')
