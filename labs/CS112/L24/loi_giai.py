import heapq

INF = float("inf")


def dijkstra(dinh, canh, s):
    d = {v: INF for v in dinh}
    d[s] = 0
    cha = {}
    chot = []
    xong = set()
    while True:
        con = [v for v in dinh if v not in xong and d[v] < INF]
        if not con:
            break
        u = min(con, key=lambda v: (d[v], dinh.index(v)))
        xong.add(u)
        chot.append(u)
        for a, b, w in canh:
            if a == u and b not in xong and d[u] + w < d[b]:
                d[b] = d[u] + w
                cha[b] = u
    return d, chot, cha


def bellman_ford(dinh, canh, s):
    d = {v: INF for v in dinh}
    d[s] = 0
    co_doi = 0
    for _ in range(len(dinh) - 1):
        doi = False
        for a, b, w in canh:
            if d[a] + w < d[b]:
                d[b] = d[a] + w
                doi = True
        if not doi:
            break
        co_doi += 1
    am = any(d[a] + w < d[b] for a, b, w in canh)
    return d, co_doi, am


D1 = ["S", "A", "B", "C", "D"]
E1 = [("S", "A", 7), ("S", "B", 2), ("B", "A", 3), ("A", "C", 1), ("B", "C", 8), ("C", "D", 2), ("B", "D", 9)]
d, chot, cha = dijkstra(D1, E1, "S")
print("Chot:", " ".join(chot))
print("d:", " ".join(f"{v}={d[v]}" for v in D1))
duong = ["D"]
while duong[-1] != "S":
    duong.append(cha[duong[-1]])
print("Duong toi D:", " ".join(reversed(duong)), "=", d["D"])

D2 = ["S", "A", "B", "C"]
E2 = [("A", "C", 2), ("B", "A", -2), ("S", "A", 2), ("S", "B", 3)]
dd, _, _ = dijkstra(D2, E2, "S")
bd, vong, _ = bellman_ford(D2, E2, "S")
print(f"Canh am: Dijkstra d[A] = {dd['A']}, Bellman-Ford d[A] = {bd['A']}, so vong co doi: {vong}")

D3 = ["S", "A", "B"]
E3 = [("S", "A", 1), ("A", "B", 1), ("B", "A", -3)]
print("Chu trinh am:", "CO" if bellman_ford(D3, E3, "S")[2] else "KHONG")
