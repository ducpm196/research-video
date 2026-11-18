def tham_lam(dinh, ke, thu_tu):
    mau = {}
    for v in thu_tu:
        da_dung = {mau[u] for u in ke[v] if u in mau}
        c = 0
        while c in da_dung:
            c = c + 1
        mau[v] = c
    return max(mau.values()) + 1

for V, E in ((10, 15), (7, 6), (12, 30)):
    print('V=' + str(V), 'E=' + str(E) + ': F=' + str(2 - V + E))
for V, E in ((7, 19), (8, 18), (6, 9)):
    print('V=' + str(V), 'E=' + str(E) + ':', 'khong phang' if E > 3 * V - 6 else 'chua ket luan')

n = 4
dinh = [('a', i) for i in range(n)] + [('b', i) for i in range(n)]
ke = {v: [u for u in dinh if u[0] != v[0] and u[1] != v[1]] for v in dinh}
xen_ke = [(s, i) for i in range(n) for s in 'ab']
a_truoc = [('a', i) for i in range(n)] + [('b', i) for i in range(n)]
print('do thi 4 cap (8 dinh): xen ke', tham_lam(dinh, ke, xen_ke), 'mau, a truoc b sau', tham_lam(dinh, ke, a_truoc), 'mau')

chu = list(range(5))
ke5 = {v: [(v + 1) % 5, (v - 1) % 5] for v in chu}
print('chu trinh 5 dinh: tham lam', tham_lam(chu, ke5, chu), 'mau, can tren', max(len(x) for x in ke5.values()) + 1)
