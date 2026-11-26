import heapq
import sys


def dijkstra(edges, src, dst):
    if any(w < 0 for _, _, w in edges):
        raise ValueError("negative edge")
    g = {}
    for u, v, w in edges:
        g.setdefault(u, []).append((v, w))
    dist = {src: 0}
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == dst:
            return d
        if d > dist.get(u, 10**18):
            continue
        for v, w in g.get(u, []):
            nd = d + w
            if nd < dist.get(v, 10**18):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1


def main():
    src, dst = "A", "D"
    direct = 0
    edges = []
    probes = []
    pts = []
    for raw in sys.stdin:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        tag = parts[0]
        if tag == "QUERY":
            src, dst = parts[1], parts[2]
        elif tag == "DIRECT":
            direct = int(parts[1])
        elif tag == "EDGE":
            edges.append((parts[1], parts[2], int(parts[3])))
        elif tag == "PROBE":
            probes.append((parts[1], parts[2], int(parts[3])))
        elif tag == "POINT":
            pts.append((float(parts[1]), float(parts[2])))

    best = dijkstra(edges, src, dst)
    pct = 100.0 * (direct - best) / direct if (direct > 0 and best >= 0) else 0.0
    neg_rejected = 0
    if probes:
        try:
            dijkstra(probes, probes[0][0], probes[0][1])
        except ValueError:
            neg_rejected = 1

    if pts:
        mx = sum(x for x, _ in pts) / len(pts)
        my = sum(y for _, y in pts) / len(pts)
        den = sum((x - mx) ** 2 for x, _ in pts)
        if den == 0:
            w, b = 0.0, my
        else:
            w = sum((x - mx) * (y - my) for x, y in pts) / den
            b = my - w * mx
        mse = sum((w * x + b - y) ** 2 for x, y in pts) / len(pts)
    else:
        w = b = mse = 0.0

    print(f"min_cost={best} saved_pct={pct:.1f}%")
    print(f"neg_rejected={neg_rejected}")
    print(f"ols_w={w:.1f} ols_b={b:.1f} mse={mse:.2f}")


if __name__ == "__main__":
    main()
