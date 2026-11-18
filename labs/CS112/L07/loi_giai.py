from collections import deque

CANH = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (6, 7)]
N = 8
ke = {u: [] for u in range(1, N + 1)}
for u, v in CANH:
    ke[u].append(v)
    ke[v].append(u)
for u in ke:
    ke[u].sort()
print("danh sach ke 4:", " ".join(map(str, ke[4])))


def bfs(s):
    d = {s: 0}
    hang = deque([s])
    thu_tu = []
    while hang:
        u = hang.popleft()
        thu_tu.append(u)
        for w in ke[u]:
            if w not in d:
                d[w] = d[u] + 1
                hang.append(w)
    return thu_tu, d


thu_tu, d = bfs(1)
print("bfs tu 1:", " ".join(map(str, thu_tu)))
print("khoang cach:", " ".join(f"{u}:{d[u]}" for u in thu_tu))


def dfs(u, da_tham, thu_tu):
    da_tham.add(u)
    thu_tu.append(u)
    for w in ke[u]:
        if w not in da_tham:
            dfs(w, da_tham, thu_tu)


kq = []
dfs(1, set(), kq)
print("dfs tu 1:", " ".join(map(str, kq)))
da_tham = set()
vung = 0
for u in range(1, N + 1):
    if u not in da_tham:
        vung += 1
        dfs(u, da_tham, [])
print("so vung lien thong:", vung)
print("6 toi duoc 1:", "co" if 6 in bfs(1)[1] else "khong")
