dur = {'tim': 3, 'docA': 5, 'docB': 2, 'tonghop': 4, 'kiemtra': 1}
deps = {
    'tim': [], 'docA': ['tim'], 'docB': ['tim'],
    'tonghop': ['docA', 'docB'], 'kiemtra': ['tonghop'],
}
finish = {}
for node in ('tim', 'docA', 'docB', 'tonghop', 'kiemtra'):
    prev = max((finish[p] for p in deps[node]), default=0)
    finish[node] = dur[node] + prev
seq = sum(dur.values())
crit = finish['kiemtra']
print(f"sequential={seq}s critical_path={crit}s saved={seq - crit}s")
